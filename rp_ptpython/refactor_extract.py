"""
Extract Variable Refactoring Module

Pure functions for extracting expressions into variables.
All functions are designed to be easily testable with simple str/int/list IO.
"""
from typing import Tuple, Optional, List, Callable
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Tree, Node

# Lazy-initialized parser for testability
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
# VALID NODE TYPES
# =============================================================================

EXTRACTABLE_TYPES = {
    'integer', 'float', 'string', 'true', 'false', 'none',
    'concatenated_string', 'identifier', 'attribute', 'subscript',
    'binary_operator', 'unary_operator', 'boolean_operator',
    'not_operator', 'comparison_operator', 'call',
    'list', 'tuple', 'set', 'dictionary',
    'list_comprehension', 'set_comprehension', 'dictionary_comprehension',
    'generator_expression', 'lambda', 'conditional_expression',
    'await', 'parenthesized_expression',
}

STATEMENT_TYPES = {
    'expression_statement', 'assignment', 'augmented_assignment',
    'return_statement', 'if_statement', 'for_statement', 'while_statement',
    'with_statement', 'try_statement', 'assert_statement', 'raise_statement',
    'pass_statement', 'break_statement', 'continue_statement',
    'import_statement', 'import_from_statement',
    'function_definition', 'async_function_definition',
    'class_definition', 'decorated_definition', 'match_statement',
}


# =============================================================================
# PURE HELPER FUNCTIONS - Node queries
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
    """Find smallest node containing the byte range."""
    best = None
    def visit(node: Node):
        nonlocal best
        if node.start_byte <= start and end <= node.end_byte:
            if best is None or (node.end_byte - node.start_byte) < (best.end_byte - best.start_byte):
                best = node
            for child in node.children:
                visit(child)
    visit(tree.root_node)
    return best


def find_smallest_extractable(tree: Tree, start: int, end: int) -> Optional[Node]:
    """Find smallest extractable expression containing the byte range."""
    best = None
    def visit(node: Node):
        nonlocal best
        if node.start_byte <= start and end <= node.end_byte:
            if node.type in EXTRACTABLE_TYPES:
                if not is_assignment_target(node) and not is_definition_name(node):
                    if best is None or (node.end_byte - node.start_byte) < (best.end_byte - best.start_byte):
                        best = node
            for child in node.children:
                visit(child)
    visit(tree.root_node)
    return best


def find_containing_statement(node: Node) -> Optional[Node]:
    """Walk up tree to find containing statement."""
    current = node
    while current:
        if current.type in STATEMENT_TYPES:
            return current
        current = current.parent
    return None


def find_containing_scope(node: Node) -> Optional[Node]:
    """Find containing function/class/module scope."""
    current = node.parent
    while current:
        if current.type in ('function_definition', 'async_function_definition', 'class_definition', 'module'):
            return current
        current = current.parent
    return None


# =============================================================================
# PURE HELPER FUNCTIONS - Node predicates
# =============================================================================

def is_assignment_target(node: Node) -> bool:
    """Check if node is on the left side of an assignment."""
    parent = node.parent
    while parent:
        if parent.type in ('assignment', 'augmented_assignment'):
            left = parent.child_by_field_name('left')
            if left and left.start_byte <= node.start_byte and node.end_byte <= left.end_byte:
                return True
            return False
        parent = parent.parent
    return False


def is_definition_name(node: Node) -> bool:
    """Check if node is a name being defined (function/class/param/loop var)."""
    if node.type != 'identifier':
        return False
    parent = node.parent
    if not parent:
        return False

    # Function/class name
    if parent.type in ('function_definition', 'async_function_definition', 'class_definition'):
        name_node = parent.child_by_field_name('name')
        if name_node and name_node.start_byte == node.start_byte:
            return True

    # Parameter
    if parent.type in ('parameters', 'lambda_parameters', 'typed_parameter',
                       'default_parameter', 'typed_default_parameter',
                       'list_splat_parameter', 'dictionary_splat_parameter'):
        return True

    # For loop variable
    if parent.type == 'for_statement':
        for child in parent.children:
            if child.type == 'in' and node.end_byte <= child.start_byte:
                return True

    # Import name
    if parent.type in ('dotted_name', 'aliased_import', 'import_statement', 'import_from_statement'):
        return True

    return False


# =============================================================================
# PURE HELPER FUNCTIONS - String utilities
# =============================================================================

def get_line_indent(code: str, byte_offset: int) -> str:
    """Get indentation string for the line containing byte_offset."""
    line_start = code.rfind('\n', 0, byte_offset) + 1
    indent_end = line_start
    while indent_end < len(code) and code[indent_end] in ' \t':
        indent_end += 1
    return code[line_start:indent_end]


def is_valid_identifier(name: str) -> Tuple[bool, Optional[str]]:
    """
    Check if name is a valid Python identifier or tuple unpacking pattern.
    Returns (is_valid, error_message).
    """
    name = name.strip()
    if not name:
        return False, "Variable name cannot be empty"

    if ',' in name:
        parts = [p.strip() for p in name.split(',')]
        for part in parts:
            if not part:
                return False, "Empty name in tuple unpacking"
            if not part.isidentifier():
                return False, f"'{part}' is not a valid identifier"
    elif not name.isidentifier():
        return False, f"'{name}' is not a valid identifier"

    return True, None


# =============================================================================
# MAIN API FUNCTIONS
# =============================================================================

def check_extractable(code: str, start: int, end: int) -> Tuple[bool, Optional[str], Optional[Tuple[int, int]]]:
    """
    Check if selection can be extracted as a variable.

    Args:
        code: Full source code
        start: Selection start byte
        end: Selection end byte

    Returns:
        (is_valid, error_message, expanded_bounds)
        - If valid with exact bounds: (True, None, None)
        - If valid but bounds expanded: (True, None, (new_start, new_end))
        - If invalid: (False, error_message, None)
    """
    if start >= end:
        return False, "Empty selection", None

    if not code[start:end].strip():
        return False, "Empty selection", None

    tree = parse(code)
    node = find_node_at(tree, start, end)
    expanded = None

    if not node:
        node = find_smallest_extractable(tree, start, end)
        if not node:
            return False, "No extractable expression found", None
        expanded = (node.start_byte, node.end_byte)

    if node.type not in EXTRACTABLE_TYPES:
        node = find_smallest_extractable(tree, start, end)
        if not node:
            return False, "Not an extractable expression", None
        expanded = (node.start_byte, node.end_byte)

    if is_assignment_target(node):
        return False, "Cannot extract assignment target", None

    if is_definition_name(node):
        return False, "Cannot extract definition name", None

    return True, None, expanded


def _normalize_whitespace(text: str) -> str:
    """Normalize whitespace for expression comparison.

    Collapses all whitespace sequences to single spaces, strips leading/trailing.
    This allows matching expressions with different formatting.
    """
    import re
    return re.sub(r'\s+', ' ', text.strip())


def _nodes_structurally_equal(node1: Node, node2: Node, code: str) -> bool:
    """
    Check if two AST nodes are structurally equal.

    Compares node types and leaf values recursively, ignoring whitespace differences.
    """
    if node1.type != node2.type:
        return False

    children1 = [c for c in node1.children if c.type not in ('(', ')', '[', ']', '{', '}', ',', ':')]
    children2 = [c for c in node2.children if c.type not in ('(', ')', '[', ']', '{', '}', ',', ':')]

    if len(children1) != len(children2):
        return False

    # Leaf nodes - compare text (normalized)
    if not children1:
        text1 = _normalize_whitespace(code[node1.start_byte:node1.end_byte])
        text2 = _normalize_whitespace(code[node2.start_byte:node2.end_byte])
        return text1 == text2

    # Recursively compare children
    for c1, c2 in zip(children1, children2):
        if not _nodes_structurally_equal(c1, c2, code):
            return False

    return True


def find_duplicates(code: str, start: int, end: int) -> List[Tuple[int, int]]:
    """
    Find other occurrences of the same expression in scope.

    Args:
        code: Full source code
        start: Expression start byte
        end: Expression end byte

    Returns:
        List of (start, end) tuples for duplicate expressions

    Note: Matches expressions with different whitespace/formatting as long as
    they have the same AST structure.
    """
    tree = parse(code)
    node = find_node_at(tree, start, end)
    if not node:
        return []

    expr_type = node.type

    scope = find_containing_scope(node)
    scope_start = scope.start_byte if scope else 0
    scope_end = scope.end_byte if scope else len(code)

    duplicates = []

    def visit(n: Node):
        if n.start_byte == start and n.end_byte == end:
            return  # Skip original
        if n.start_byte < scope_start or n.end_byte > scope_end:
            return  # Out of scope
        if n.type == expr_type:
            # Use structural comparison instead of text comparison
            if _nodes_structurally_equal(node, n, code):
                if not is_assignment_target(n):
                    duplicates.append((n.start_byte, n.end_byte))
        for child in n.children:
            visit(child)

    visit(tree.root_node)
    return duplicates


def get_insertion_point(code: str, start: int, end: int) -> Tuple[int, str]:
    """
    Find where to insert the variable assignment.

    Args:
        code: Full source code
        start: Expression start byte
        end: Expression end byte

    Returns:
        (insertion_byte, indentation_string)
    """
    tree = parse(code)
    node = find_node_at(tree, start, end)
    if not node:
        node = find_smallest_containing(tree, start, end)
    if not node:
        return 0, ""

    stmt = find_containing_statement(node)
    if not stmt:
        return 0, ""

    line_start = code.rfind('\n', 0, stmt.start_byte) + 1
    indent = get_line_indent(code, stmt.start_byte)
    return line_start, indent


def perform_extraction(
    code: str,
    start: int,
    end: int,
    var_name: str,
    replace_all: bool = False
) -> Tuple[str, int]:
    """
    Perform the extract variable refactoring.

    Args:
        code: Full source code
        start: Expression start byte
        end: Expression end byte
        var_name: Name for the new variable
        replace_all: Whether to replace all occurrences in scope

    Returns:
        (new_code, cursor_position)

    Raises:
        ValueError: If extraction is not possible
    """
    tree = parse(code)
    node = find_node_at(tree, start, end)
    if not node:
        raise ValueError("Cannot extract: invalid selection")

    expr_text = code[start:end]

    # Collect all replacements
    replacements = [(start, end)]
    if replace_all:
        replacements.extend(find_duplicates(code, start, end))

    # Sort to find first occurrence
    replacements_sorted = sorted(replacements)
    first_start, first_end = replacements_sorted[0]

    # Get insertion point (before first occurrence when replacing all)
    if replace_all and first_start < start:
        insertion_byte, indent = get_insertion_point(code, first_start, first_end)
    else:
        insertion_byte, indent = get_insertion_point(code, start, end)

    # Build assignment line
    assignment = f"{indent}{var_name} = {expr_text}\n"

    # Calculate offset adjustment for replacements before insertion point
    var_len = len(var_name)
    offset_delta = 0
    for rep_start, rep_end in replacements:
        if rep_start < insertion_byte:
            offset_delta += var_len - (rep_end - rep_start)

    adjusted_insertion = insertion_byte + offset_delta

    # Apply replacements in reverse order (to maintain offsets)
    new_code = code
    for rep_start, rep_end in sorted(replacements, reverse=True):
        new_code = new_code[:rep_start] + var_name + new_code[rep_end:]

    # Insert assignment
    new_code = new_code[:adjusted_insertion] + assignment + new_code[adjusted_insertion:]

    # Cursor at end of assignment line
    cursor = adjusted_insertion + len(assignment)

    return new_code, cursor


# =============================================================================
# STATE MANAGEMENT
# =============================================================================

class ExtractVariableState:
    """State for the extract variable UI with live preview."""
    __slots__ = ('active', 'name', 'name_cursor', 'selection', 'error', 'replace_all', 'duplicate_count', 'original_code')

    def __init__(self):
        self.reset()

    def reset(self):
        self.active = False
        self.name = ""
        self.name_cursor = 0
        self.selection = None  # (start, end) or None
        self.error = None  # error message or None
        self.replace_all = False
        self.duplicate_count = 0
        self.original_code = ""

    def start(self, selection: Tuple[int, int], duplicate_count: int, original_code: str = ""):
        """Enter extract variable mode."""
        self.active = True
        self.name = ""
        self.name_cursor = 0
        self.selection = selection
        self.error = None
        self.replace_all = False
        self.duplicate_count = duplicate_count
        self.original_code = original_code

    def show_error(self, error: str, recoverable: bool = False):
        """Show an error. If recoverable, keep selection so user can fix."""
        self.active = True
        self.error = error
        if not recoverable:
            self.selection = None

    def has_valid_selection(self) -> bool:
        """Check if we have a valid selection (not just showing an error)."""
        return self.selection is not None

    def add_char(self, char: str):
        """Add a character at cursor position."""
        self.error = None
        self.name = self.name[:self.name_cursor] + char + self.name[self.name_cursor:]
        self.name_cursor += 1

    def delete_char(self):
        """Delete character before cursor."""
        self.error = None
        if self.name_cursor > 0:
            self.name = self.name[:self.name_cursor-1] + self.name[self.name_cursor:]
            self.name_cursor -= 1

    def cursor_left(self):
        if self.name_cursor > 0: self.name_cursor -= 1

    def cursor_right(self):
        if self.name_cursor < len(self.name): self.name_cursor += 1

    def delete_forward(self):
        """Delete character at cursor."""
        self.error = None
        if self.name_cursor < len(self.name):
            self.name = self.name[:self.name_cursor] + self.name[self.name_cursor+1:]

    def toggle_mode(self):
        """Toggle replace all mode."""
        if self.duplicate_count > 0:
            self.replace_all = not self.replace_all

    def get_preview(self) -> Optional[Tuple[str, int]]:
        """Get live preview of the extraction. Returns (new_code, new_cursor) or None."""
        if not self.active or not self.original_code or not self.selection:
            return None
        var_name = self.name.strip()
        if not var_name:
            return None
        # Validate it's a valid identifier
        valid, _ = is_valid_identifier(var_name)
        if not valid:
            return None
        try:
            start, end = self.selection
            return perform_extraction(self.original_code, start, end, var_name, self.replace_all)
        except Exception:
            return None


# Global state instance
state = ExtractVariableState()


# =============================================================================
# STATUS MESSAGE (for transient errors like black formatting)
# =============================================================================

_status_message: Optional[str] = None


def set_status(msg: str):
    """Set a transient status message (dismissed on any key)."""
    global _status_message
    _status_message = msg


def get_status() -> Optional[str]:
    """Get current status message."""
    return _status_message


def clear_status():
    """Clear status message (call on any keypress)."""
    global _status_message
    _status_message = None


def dismiss_on_keypress():
    """Call at start of any key handler to dismiss transient messages."""
    clear_status()


# =============================================================================
# HIGH-LEVEL HANDLERS (for minimal key_bindings.py integration)
# =============================================================================

# Characters allowed in variable names (including comma/space for tuple unpacking)
ALLOWED_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_, ')


def handle_start(code: str, start: int, end: int) -> Optional[Tuple[int, int]]:
    """
    Handle Ctrl+R: Start extract variable mode.

    Args:
        code: Buffer text
        start: Selection start
        end: Selection end

    Returns:
        New (start, end) if selection was expanded, None otherwise.
        Sets state.active=True on success, shows error on failure.
    """
    valid, error, expanded = check_extractable(code, start, end)

    if not valid:
        state.show_error(error, recoverable=False)
        return None

    # Use expanded bounds if provided
    if expanded:
        start, end = expanded

    # Count duplicates
    dups = find_duplicates(code, start, end)
    state.start((start, end), len(dups), code)  # Save original code for preview

    return expanded


def handle_char(char: str) -> bool:
    """
    Handle character input in extract variable mode.

    Returns:
        True if handled (block further processing), False to pass through.
    """
    if not state.active:
        return False

    # Error with no valid selection = dismiss on any key
    if state.error and not state.has_valid_selection():
        state.reset()
        return True  # Block the key

    # Clear validation errors on input
    if state.error:
        state.error = None

    # Add allowed characters at cursor position
    if char in ALLOWED_CHARS:
        state.add_char(char)

    return True  # Block all chars in this mode


def handle_backspace() -> bool:
    """
    Handle backspace in extract variable mode.

    Returns:
        True if handled, False to pass through.
    """
    if not state.active:
        return False

    if state.error and not state.has_valid_selection():
        state.reset()
        return True

    if state.error:
        state.error = None

    state.delete_char()

    return True


def handle_confirm(code: str) -> Optional[Tuple[str, int]]:
    """
    Handle Enter: Confirm extraction.

    Args:
        code: Current buffer text

    Returns:
        (new_code, cursor_position) on success, None on error.
        State is reset on success, error shown on failure.
    """
    if not state.active or not state.has_valid_selection():
        state.reset()
        return None

    var_name = state.name.strip()

    # Validate name
    valid, error = is_valid_identifier(var_name)
    if not valid:
        state.error = error
        return None  # Keep state for user to fix

    # Perform extraction
    start, end = state.selection
    try:
        new_code, cursor = perform_extraction(code, start, end, var_name, state.replace_all)
        state.reset()
        return new_code, cursor
    except Exception as e:
        state.error = str(e)
        return None


def handle_cancel():
    """Handle Escape/Ctrl+C/Ctrl+D: Cancel extraction."""
    state.reset()


def handle_toggle_replace_all():
    """Handle Tab: Toggle replace all mode."""
    state.toggle_mode()
