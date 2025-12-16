"""
Move Selection Refactoring Module

Pure functions for moving selections through the syntax tree.
Supports moving arguments, list elements, statements, etc.
All functions are designed to be easily testable with simple str/int/list IO.

Usage:
    from rp.rp_ptpython import refactor_move as move

    # Move single element
    code = 'foo(a, b, c)'
    result = move.move_up(code, 7, 8)  # Select 'b'
    # Returns: ('foo(b, a, c)', 4, 5)  # (new_code, new_start, new_end)

    # Move multiple adjacent elements as a group
    code = 'foo(a, b, c, d, e)'
    result = move.move_up(code, 7, 14)  # Select 'b, c, d'
    # Returns: ('foo(b, c, d, a, e)', 4, 11)

    # Move multiple lines
    code = 'x = 1\\ny = 2\\nz = 3'
    result = move.move_down(code, 6, 11)  # Select 'y = 2'
    # Returns: ('x = 1\\nz = 3\\ny = 2', 12, 17)

    # Check if selection can be moved
    can_move, error, expanded = move.check_movable(code, start, end)

    # Expand partial selection to movable element
    bounds = move.expand_to_movable(code, start, end)

Supported contexts:
    - Function arguments: foo(a, b, c)
    - Function parameters: def f(x, y, z):
    - List elements: [1, 2, 3]
    - Tuple elements: (a, b, c)
    - Set elements: {1, 2, 3}
    - Dict pairs: {a: 1, b: 2}
    - Import names: from x import a, b
    - Statements: Lines within blocks
    - Keyword arguments: foo(a=1, b=2)
    - Function definitions: def foo(): / def bar():
    - Class definitions: class A: / class B:
    - Methods inside classes
    - Multiple adjacent elements move as a group
"""
from typing import Tuple, Optional, List
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Tree, Node

# Lazy-initialized parser
_PARSER: Optional[Parser] = None


def _get_parser() -> Parser:
    global _PARSER
    if _PARSER is None:
        _PARSER = Parser(Language(tspython.language()))
    return _PARSER


def parse(code: str) -> Tree:
    """Parse Python code into a tree-sitter tree."""
    return _get_parser().parse(bytes(code, "utf8"))


# =============================================================================
# NODE TYPES THAT CONTAIN MOVABLE SIBLINGS
# =============================================================================

# Containers where children can be reordered (comma-separated)
SIBLING_CONTAINERS = {
    'argument_list',      # foo(a, b, c)
    'parameters',         # def foo(a, b, c):
    'expression_list',    # a, b, c = ...
    'tuple',              # (a, b, c)
    'list',               # [a, b, c]
    'set',                # {a, b, c}
    'dictionary',         # {a: 1, b: 2}  - pairs are children
    'subscript',          # a[b, c] - for multi-dimensional indexing
    'import_from_statement',  # from x import a, b, c
    'global_statement',   # global a, b, c
    'nonlocal_statement', # nonlocal a, b, c
    'print_statement',    # legacy python 2
    'with_clause',        # with a, b:
    'assert_statement',   # assert a, b (message)
}

# Containers where children are statements (line-based)
STATEMENT_CONTAINERS = {
    'module',
    'block',
    'if_statement',
    'elif_clause',
    'else_clause',
    'for_statement',
    'while_statement',
    'try_statement',
    'except_clause',
    'finally_clause',
    'with_statement',
    'function_definition',
    'async_function_definition',
    'class_definition',
    'match_statement',
    'case_clause',
}

# Node types that are actual content (not punctuation/keywords)
CONTENT_TYPES = {
    # Expressions
    'identifier', 'integer', 'float', 'string', 'true', 'false', 'none',
    'concatenated_string', 'attribute', 'subscript', 'call',
    'binary_operator', 'unary_operator', 'boolean_operator',
    'not_operator', 'comparison_operator',
    'list', 'tuple', 'set', 'dictionary',
    'list_comprehension', 'set_comprehension', 'dictionary_comprehension',
    'generator_expression', 'lambda', 'conditional_expression',
    'await', 'parenthesized_expression', 'named_expression',
    'list_splat', 'dictionary_splat', 'keyword_argument',
    'default_parameter', 'typed_parameter', 'typed_default_parameter',
    'list_splat_pattern', 'dictionary_splat_pattern',
    'pair',  # dict key-value pair
    'slice', 'starred_expression',

    # Statements
    'expression_statement', 'assignment', 'augmented_assignment',
    'return_statement', 'yield', 'raise_statement', 'pass_statement',
    'break_statement', 'continue_statement', 'assert_statement',
    'import_statement', 'import_from_statement', 'future_import_statement',
    'global_statement', 'nonlocal_statement', 'type_alias_statement',
    'if_statement', 'for_statement', 'while_statement',
    'try_statement', 'with_statement', 'match_statement',
    'function_definition', 'async_function_definition', 'class_definition',
    'decorated_definition', 'delete_statement', 'exec_statement',
    'print_statement',

    # Import parts
    'dotted_name', 'aliased_import',
}

# Punctuation and keywords to skip
SKIP_TYPES = {
    ',', '(', ')', '[', ']', '{', '}', ':', ';',
    'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try',
    'except', 'finally', 'with', 'as', 'import', 'from', 'return',
    'yield', 'raise', 'pass', 'break', 'continue', 'global', 'nonlocal',
    'assert', 'del', 'exec', 'print', 'in', 'not', 'and', 'or', 'is',
    'lambda', 'await', 'async', 'match', 'case', 'type',
    'comment', 'NEWLINE', 'INDENT', 'DEDENT', 'ERROR',
}


# =============================================================================
# PURE HELPER FUNCTIONS
# =============================================================================

def find_node_at(tree: Tree, start: int, end: int) -> Optional[Node]:
    """Find node with exact byte range."""
    def find(node: Node) -> Optional[Node]:
        if node.start_byte == start and node.end_byte == end:
            return node
        for child in node.children:
            if child.start_byte <= start and end <= child.end_byte:
                result = find(child)
                if result:
                    return result
        return None
    return find(tree.root_node)


def find_smallest_containing(tree: Tree, start: int, end: int) -> Optional[Node]:
    """Find smallest node containing the byte range (prefers deeper nodes on tie)."""
    best = None
    best_depth = -1
    def visit(node: Node, depth: int):
        nonlocal best, best_depth
        if node.start_byte <= start and end <= node.end_byte:
            size = node.end_byte - node.start_byte
            best_size = (best.end_byte - best.start_byte) if best else float('inf')
            # Prefer smaller, or same size but deeper (more specific)
            if best is None or size < best_size or (size == best_size and depth > best_depth):
                best = node
                best_depth = depth
            for child in node.children:
                visit(child, depth + 1)
    visit(tree.root_node, 0)
    return best


def get_content_children(node: Node) -> List[Node]:
    """Get children that are actual content (not punctuation/keywords)."""
    return [c for c in node.children if c.type in CONTENT_TYPES]


def get_sibling_index(node: Node, siblings: List[Node]) -> int:
    """Find index of node in siblings list by byte position."""
    for i, sib in enumerate(siblings):
        if sib.start_byte == node.start_byte and sib.end_byte == node.end_byte:
            return i
    return -1


def find_selected_siblings(siblings: List[Node], start: int, end: int) -> List[int]:
    """
    Find indices of all siblings that overlap with selection.
    Returns list of indices (may be multiple for multi-element selection).
    """
    indices = []
    for i, sib in enumerate(siblings):
        # Check if sibling overlaps with selection
        if sib.end_byte > start and sib.start_byte < end:
            indices.append(i)
    return indices


def find_movable_group(tree: Tree, start: int, end: int) -> Optional[Tuple[List[int], Node, List[Node]]]:
    """
    Find movable element(s) and their siblings.
    Supports selecting multiple adjacent siblings to move as a group.

    Returns: (selected_indices, container_node, siblings_list) or None
    """
    node = find_smallest_containing(tree, start, end)
    if not node:
        return None

    # Check if we're directly at a container (selection spans multiple children)
    if node.type in SIBLING_CONTAINERS or node.type in STATEMENT_CONTAINERS:
        siblings = get_content_children(node)
        if len(siblings) > 1:
            selected = find_selected_siblings(siblings, start, end)
            if selected and len(selected) < len(siblings):  # Not all selected
                if len(selected) == 1 or selected == list(range(selected[0], selected[-1] + 1)):
                    return (selected, node, siblings)

    # Walk up tree looking for a movable context
    current = node
    while current:
        parent = current.parent
        if not parent:
            break

        # Check if parent is a container with movable siblings
        if parent.type in SIBLING_CONTAINERS or parent.type in STATEMENT_CONTAINERS:
            siblings = get_content_children(parent)
            if len(siblings) > 1:
                # Find which siblings are selected
                selected = find_selected_siblings(siblings, start, end)
                if selected:
                    # Check if selected siblings are contiguous
                    if len(selected) == 1 or selected == list(range(selected[0], selected[-1] + 1)):
                        return (selected, parent, siblings)

        current = parent

    return None


def find_smallest_movable(tree: Tree, start: int, end: int) -> Optional[Tuple[List[int], Node, List[Node]]]:
    """
    Find smallest movable element(s) containing selection.
    Supports multi-element selections (adjacent siblings move as group).

    Returns: (selected_indices, container_node, siblings_list) or None
    """
    # First try to find movable group
    result = find_movable_group(tree, start, end)
    if result:
        return result

    # Try finding any containing movable context by walking up
    node = find_smallest_containing(tree, start, end)
    while node:
        parent = node.parent
        if parent and (parent.type in SIBLING_CONTAINERS or parent.type in STATEMENT_CONTAINERS):
            siblings = get_content_children(parent)
            if len(siblings) > 1:
                idx = get_sibling_index(node, siblings)
                if idx >= 0:
                    return ([idx], parent, siblings)
        node = parent

    return None


# =============================================================================
# PURE MOVE FUNCTIONS
# =============================================================================

def check_movable(code: str, start: int, end: int) -> Tuple[bool, Optional[str], Optional[Tuple[int, int]]]:
    """
    Check if selection can be moved.

    Returns: (can_move, error_message, expanded_bounds)
    - If movable with exact bounds: (True, None, None)
    - If movable but bounds expanded: (True, None, (new_start, new_end))
    - If not movable: (False, error_message, None)
    """
    if start >= end:
        return False, "Empty selection", None

    tree = parse(code)
    result = find_smallest_movable(tree, start, end)

    if not result:
        return False, "No movable element found", None

    element, container, siblings = result

    if len(siblings) < 2:
        return False, "Need multiple siblings to move", None

    # Check if bounds need expansion
    if element.start_byte != start or element.end_byte != end:
        return True, None, (element.start_byte, element.end_byte)

    return True, None, None


def move_element(code: str, start: int, end: int, direction: int) -> Optional[Tuple[str, int, int]]:
    """
    Move selected element(s) up/left (direction=-1) or down/right (direction=+1).
    Supports moving multiple adjacent siblings as a group.

    Args:
        code: Source code
        start: Selection start byte
        end: Selection end byte
        direction: -1 for up/left, +1 for down/right

    Returns: (new_code, new_start, new_end) or None if can't move
    """
    tree = parse(code)
    result = find_smallest_movable(tree, start, end)

    if not result:
        return None

    selected_indices, container, siblings = result

    if not selected_indices:
        return None

    first_idx = selected_indices[0]
    last_idx = selected_indices[-1]

    # Calculate target index for the group
    if direction < 0:
        # Moving up: swap with element before the group
        if first_idx == 0:
            return None  # Already at start
        swap_idx = first_idx - 1
    else:
        # Moving down: swap with element after the group
        if last_idx >= len(siblings) - 1:
            return None  # Already at end
        swap_idx = last_idx + 1

    # For statement containers, handle full lines
    if container.type in STATEMENT_CONTAINERS:
        return _swap_group_statements(code, siblings, selected_indices, swap_idx, direction)
    else:
        return _swap_group_siblings(code, siblings, selected_indices, swap_idx, direction)


def _swap_group_siblings(code: str, siblings: List[Node], selected_indices: List[int],
                         swap_idx: int, direction: int) -> Tuple[str, int, int]:
    """Swap a group of siblings with an adjacent sibling."""
    first_idx = selected_indices[0]
    last_idx = selected_indices[-1]

    # Get the group bounds (from first selected to last selected)
    group_start = siblings[first_idx].start_byte
    group_end = siblings[last_idx].end_byte
    group_text = code[group_start:group_end]

    # Get the swap element
    swap_node = siblings[swap_idx]
    swap_text = code[swap_node.start_byte:swap_node.end_byte]

    if direction < 0:
        # Moving up: swap_node is before group
        # [swap] [gap1] [group] -> [group] [gap1] [swap]
        gap = group_start - swap_node.end_byte
        new_code = (code[:swap_node.start_byte] + group_text +
                   code[swap_node.end_byte:group_start] + swap_text +
                   code[group_end:])
        # Group moved to swap's position
        new_start = swap_node.start_byte
        new_end = swap_node.start_byte + len(group_text)
    else:
        # Moving down: swap_node is after group
        # [group] [gap1] [swap] -> [swap] [gap1] [group]
        gap = swap_node.start_byte - group_end
        new_code = (code[:group_start] + swap_text +
                   code[group_end:swap_node.start_byte] + group_text +
                   code[swap_node.end_byte:])
        # Group moved to after swap's original position (adjusted)
        new_start = group_start + len(swap_text) + gap
        new_end = new_start + len(group_text)

    return new_code, new_start, new_end


def _get_line_bounds(code: str, node: Node) -> Tuple[int, int]:
    """Get full line bounds for a statement node (including indentation)."""
    line_start = code.rfind('\n', 0, node.start_byte) + 1
    line_end = _find_statement_end(code, node)
    return line_start, line_end


def _swap_group_statements(code: str, siblings: List[Node], selected_indices: List[int],
                           swap_idx: int, direction: int) -> Tuple[str, int, int]:
    """Swap a group of statement siblings with an adjacent statement."""
    first_idx = selected_indices[0]
    last_idx = selected_indices[-1]

    # Get line bounds for the group
    group_line_start, _ = _get_line_bounds(code, siblings[first_idx])
    _, group_line_end = _get_line_bounds(code, siblings[last_idx])
    group_text = code[group_line_start:group_line_end]

    # Get line bounds for swap element
    swap_line_start, swap_line_end = _get_line_bounds(code, siblings[swap_idx])
    swap_text = code[swap_line_start:swap_line_end]

    if direction < 0:
        # Moving up: swap is before group
        # Include newline between swap and group
        between = code[swap_line_end:group_line_start]
        new_code = (code[:swap_line_start] + group_text + between + swap_text + code[group_line_end:])
        new_start = swap_line_start
        new_end = swap_line_start + len(group_text)
    else:
        # Moving down: swap is after group
        between = code[group_line_end:swap_line_start]
        new_code = (code[:group_line_start] + swap_text + between + group_text + code[swap_line_end:])
        new_start = group_line_start + len(swap_text) + len(between)
        new_end = new_start + len(group_text)

    return new_code, new_start, new_end


def _find_statement_end(code: str, node: Node) -> int:
    """Find the end of a statement, handling multi-line statements."""
    # Start from node end, look for the line end
    pos = node.end_byte
    while pos < len(code) and code[pos] != '\n':
        pos += 1
    return pos


# =============================================================================
# HIGH-LEVEL API
# =============================================================================

def move_up(code: str, start: int, end: int) -> Optional[Tuple[str, int, int]]:
    """Move selection up/left in the syntax tree."""
    return move_element(code, start, end, -1)


def move_down(code: str, start: int, end: int) -> Optional[Tuple[str, int, int]]:
    """Move selection down/right in the syntax tree."""
    return move_element(code, start, end, +1)


def move(code: str, start: int, end: int, cursor_pos: int, anchor_pos: int,
         direction: int) -> Optional[Tuple[str, int, int, int]]:
    """
    Move selection with cursor position preservation.

    Args:
        code: Source code
        start: Selection start (lower bound)
        end: Selection end (upper bound)
        cursor_pos: Current cursor position
        anchor_pos: Selection anchor position
        direction: -1 for up/left, +1 for down/right

    Returns: (new_code, new_cursor_pos, new_anchor_pos, new_selection_end) or None
             new_cursor_pos and new_anchor_pos preserve which side the cursor was on
    """
    result = move_element(code, start, end, direction)
    if not result:
        return None

    new_code, new_start, new_end = result

    # Preserve cursor side: was cursor at end or start of selection?
    cursor_at_end = cursor_pos >= end or cursor_pos > anchor_pos

    if cursor_at_end:
        return (new_code, new_end, new_start, new_end)
    else:
        return (new_code, new_start, new_end, new_end)


def expand_to_movable(code: str, start: int, end: int) -> Optional[Tuple[int, int]]:
    """
    Expand selection to the smallest movable element.

    Returns: (new_start, new_end) or None if no movable element found
    """
    tree = parse(code)
    result = find_smallest_movable(tree, start, end)
    if result:
        selected_indices, container, siblings = result
        first_idx = selected_indices[0]
        last_idx = selected_indices[-1]
        return (siblings[first_idx].start_byte, siblings[last_idx].end_byte)
    return None
