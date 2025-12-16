"""
Inline Variable Refactoring Module for Bash

Replaces usages of a variable with its assigned value.

Usage:
    from rp.rp_ptpython import bash_inline as inline
    result = inline.inline_variable(code, cursor_pos)
    # Returns: (new_code, new_cursor, should_prompt_delete) or None

Bash-specific considerations:
    - Variables are assigned as VAR=value (no spaces around =)
    - Variables are used as $VAR or ${VAR}
    - No real scoping (except 'local' in functions)
    - Command substitution: VAR=$(cmd) or VAR=`cmd`
"""
from typing import Tuple, Optional, List
import tree_sitter_bash as tsbash
from tree_sitter import Language, Parser, Tree, Node

_PARSER: Optional[Parser] = None


def _get_parser() -> Parser:
    global _PARSER
    if _PARSER is None:
        _PARSER = Parser(Language(tsbash.language()))
    return _PARSER


def parse(code: str) -> Tree:
    return _get_parser().parse(bytes(code, "utf8"))


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def find_node_at_cursor(tree: Tree, pos: int) -> Optional[Node]:
    """Find the smallest node at cursor position."""
    best = None
    best_size = float('inf')

    def visit(node: Node):
        nonlocal best, best_size
        if node.start_byte <= pos < node.end_byte or node.start_byte == pos == node.end_byte:
            size = node.end_byte - node.start_byte
            if size < best_size:
                best = node
                best_size = size
            for child in node.children:
                visit(child)

    visit(tree.root_node)
    return best


def find_variable_at_cursor(tree: Tree, code: str, pos: int) -> Optional[Tuple[str, int, int, Node, bool]]:
    """
    Find variable at cursor.

    Returns: (name, start, end, node, is_assignment) or None
    """
    node = find_node_at_cursor(tree, pos)
    if not node:
        return None

    # Direct variable_name node
    if node.type == 'variable_name':
        name = code[node.start_byte:node.end_byte]
        parent = node.parent
        # Check if this is in an assignment (left side)
        is_assignment = parent and parent.type == 'variable_assignment'
        if is_assignment:
            return (name, node.start_byte, node.end_byte, node, True)
        # If inside an expansion ($VAR or ${VAR}), return the expansion's span
        if parent and parent.type in ('simple_expansion', 'expansion'):
            return (name, parent.start_byte, parent.end_byte, parent, False)
        return (name, node.start_byte, node.end_byte, node, False)

    # Simple expansion: $VAR
    if node.type == 'simple_expansion':
        for child in node.children:
            if child.type == 'variable_name':
                name = code[child.start_byte:child.end_byte]
                return (name, node.start_byte, node.end_byte, node, False)

    # Expansion: ${VAR}
    if node.type == 'expansion':
        for child in node.children:
            if child.type == 'variable_name':
                name = code[child.start_byte:child.end_byte]
                return (name, node.start_byte, node.end_byte, node, False)

    # Check parent
    parent = node.parent
    if parent:
        if parent.type == 'variable_assignment':
            for child in parent.children:
                if child.type == 'variable_name':
                    name = code[child.start_byte:child.end_byte]
                    return (name, child.start_byte, child.end_byte, child, True)
        elif parent.type in ('simple_expansion', 'expansion'):
            for child in parent.children:
                if child.type == 'variable_name':
                    name = code[child.start_byte:child.end_byte]
                    return (name, parent.start_byte, parent.end_byte, parent, False)

    return None


def get_assignment_value(assignment_node: Node, code: str) -> Optional[str]:
    """Get the value part of an assignment (after the =)."""
    # variable_assignment has children: variable_name, and value(s)
    found_name = False
    value_parts = []

    for child in assignment_node.children:
        if child.type == 'variable_name':
            found_name = True
            continue
        if found_name and child.type not in ('=',):
            value_parts.append(code[child.start_byte:child.end_byte])

    if value_parts:
        return ''.join(value_parts)

    # Try getting everything after =
    text = code[assignment_node.start_byte:assignment_node.end_byte]
    if '=' in text:
        return text.split('=', 1)[1]

    return None


def find_all_assignments(tree: Tree, code: str, var_name: str) -> List[Tuple[int, int, str, Node]]:
    """
    Find all assignments to var_name.

    Returns: List of (start_byte, end_byte, value_text, assignment_node)
    """
    assignments = []

    def visit(node: Node):
        if node.type == 'variable_assignment':
            for child in node.children:
                if child.type == 'variable_name':
                    if code[child.start_byte:child.end_byte] == var_name:
                        value = get_assignment_value(node, code)
                        if value is not None:
                            assignments.append((
                                node.start_byte,
                                node.end_byte,
                                value,
                                node
                            ))
                    break

        for child in node.children:
            visit(child)

    visit(tree.root_node)
    assignments.sort(key=lambda x: x[0])
    return assignments


def is_simple_expansion(node: Node) -> bool:
    """
    Check if an expansion node is simple (just ${VAR}) vs complex (${VAR:-default}, ${#VAR}, etc).

    Complex expansions have operators like :-, :+, :?, #, ##, %, %%, /, etc.
    """
    if node.type == 'simple_expansion':
        return True  # $VAR is always simple

    if node.type == 'expansion':
        # Count meaningful children (skip $, {, })
        meaningful = [c for c in node.children if c.type not in ('$', '{', '}', 'variable_name')]
        # If there are other children besides the variable name, it's complex
        return len(meaningful) == 0

    return False


def find_all_usages(tree: Tree, code: str, var_name: str, include_complex: bool = False) -> List[Tuple[int, int, Node]]:
    """
    Find all usages (reads) of var_name: $VAR, ${VAR}.

    By default, skips complex expansions like ${VAR:-default}, ${#VAR}, etc.
    Set include_complex=True to include them.

    Returns: List of (start_byte, end_byte, node)
    """
    usages = []

    def visit(node: Node):
        # $VAR
        if node.type == 'simple_expansion':
            for child in node.children:
                if child.type == 'variable_name':
                    if code[child.start_byte:child.end_byte] == var_name:
                        usages.append((node.start_byte, node.end_byte, node))
                    break

        # ${VAR} - only if simple (no operators)
        if node.type == 'expansion':
            if include_complex or is_simple_expansion(node):
                for child in node.children:
                    if child.type == 'variable_name':
                        if code[child.start_byte:child.end_byte] == var_name:
                            usages.append((node.start_byte, node.end_byte, node))
                        break

        for child in node.children:
            visit(child)

    visit(tree.root_node)
    usages.sort(key=lambda x: x[0])
    return usages


def get_line_range(code: str, start: int, end: int) -> Tuple[int, int]:
    """Get the full line range containing start:end (for deletion)."""
    line_start = code.rfind('\n', 0, start) + 1
    line_end = code.find('\n', end)
    if line_end == -1:
        line_end = len(code)
    else:
        line_end += 1  # Include the newline
    return line_start, line_end


def is_usage_inside_quotes(usage_node: Node, code: str) -> Optional[str]:
    """
    Check if the usage ($VAR or ${VAR}) is inside a quoted string.

    Returns the quote character ('"' or "'") if inside quotes, None otherwise.
    """
    # Look backwards from usage start to find an opening quote
    start = usage_node.start_byte

    # Check for double-quoted string context by looking at parent nodes
    current = usage_node.parent
    while current:
        if current.type == 'string':
            # We're inside a string - check if it's double-quoted
            text = code[current.start_byte:current.end_byte]
            if text.startswith('"'):
                return '"'
            elif text.startswith("'"):
                return "'"
            elif text.startswith("$'"):
                return "'"
        current = current.parent

    # Also check by scanning backwards for unmatched quote
    quote_char = None
    i = start - 1
    while i >= 0:
        c = code[i]
        if c == '"' and (i == 0 or code[i-1] != '\\'):
            if quote_char == '"':
                quote_char = None
            elif quote_char is None:
                quote_char = '"'
        elif c == "'" and (i == 0 or code[i-1] != '\\'):
            if quote_char == "'":
                quote_char = None
            elif quote_char is None:
                quote_char = "'"
        elif c == '\n':
            # Don't look past line boundaries for this simple check
            break
        i -= 1

    return quote_char


def strip_quotes(value: str) -> str:
    """Remove surrounding quotes from a value if present."""
    if len(value) >= 2:
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
    return value


def prepare_inline_value(value: str, usage_node: Node, code: str) -> str:
    """
    Prepare a value for inlining at a specific usage location.

    Handles:
    - Usage inside quotes: strip value's quotes to avoid double-quoting
    - Usage outside quotes: keep or add quotes as needed
    """
    inside_quote = is_usage_inside_quotes(usage_node, code)

    if inside_quote:
        # Usage is already inside quotes like "$VAR"
        # Strip the value's quotes to avoid ""value""
        return strip_quotes(value)
    else:
        # Usage is not inside quotes
        # If value is quoted, we can use it as-is
        # If value is unquoted and has spaces, it might need quoting
        # But generally, just use the value as-is since that's what was assigned
        return value


# =============================================================================
# MAIN INLINE FUNCTION
# =============================================================================

def check_inline(code: str, cursor_pos: int) -> Tuple[bool, Optional[str], Optional[dict]]:
    """
    Check if inline is possible at cursor.

    Returns: (can_inline, error_message, info_dict)
    """
    tree = parse(code)
    result = find_variable_at_cursor(tree, code, cursor_pos)

    if not result:
        return False, "Cursor must be on a variable", None

    name, start, end, node, is_assignment = result

    # Find all assignments and usages
    assignments = find_all_assignments(tree, code, name)
    usages = find_all_usages(tree, code, name)

    if not assignments:
        return False, f"No assignment found for '{name}'", None

    if not usages:
        return False, f"No usages found for '{name}'", None

    return True, None, {
        'name': name,
        'is_assignment': is_assignment,
        'assignment_count': len(assignments),
        'usage_count': len(usages),
    }


def inline_variable(code: str, cursor_pos: int, delete_if_unused: bool = True) -> Optional[Tuple[str, int, bool]]:
    """
    Inline the variable at cursor.

    If cursor is on an assignment: inline all usages of that assignment's value.
    If cursor is on a usage: inline just that usage with the most recent assignment's value.

    Returns: (new_code, new_cursor, should_prompt_delete) or None
    """
    tree = parse(code)
    result = find_variable_at_cursor(tree, code, cursor_pos)

    if not result:
        return None

    name, v_start, v_end, node, is_assignment = result

    assignments = find_all_assignments(tree, code, name)
    usages = find_all_usages(tree, code, name)

    if not assignments:
        return None

    if is_assignment:
        # Find which assignment we're on
        assign_idx = None
        for i, (a_start, a_end, a_value, a_node) in enumerate(assignments):
            if a_start <= cursor_pos <= a_end:
                assign_idx = i
                break

        if assign_idx is None:
            return None

        assign_start, assign_end, value, assign_node = assignments[assign_idx]

        # Find usages that come after this assignment but before next assignment
        next_assign_start = float('inf')
        if assign_idx + 1 < len(assignments):
            next_assign_start = assignments[assign_idx + 1][0]

        relevant_usages = [
            (u_start, u_end, u_node) for u_start, u_end, u_node in usages
            if assign_end < u_start < next_assign_start
        ]

        if not relevant_usages:
            return None

        # Replace usages in reverse order
        new_code = code
        for u_start, u_end, u_node in reversed(relevant_usages):
            # Prepare the value for this specific usage context
            inline_value = prepare_inline_value(value, u_node, new_code)
            new_code = new_code[:u_start] + inline_value + new_code[u_end:]

        # Check if we should delete the assignment
        should_delete = False
        remaining_usages = [u for u in usages if u[0] not in [r[0] for r in relevant_usages]]
        # Check if any remaining usages are for this assignment
        usages_after = [u for u in remaining_usages if u[0] > assign_end]
        if not usages_after and delete_if_unused:
            should_delete = True
            # Delete the assignment line
            line_start, line_end = get_line_range(new_code, assign_start, assign_end)
            # Recalculate positions after replacements
            # This is tricky - for now, just indicate deletion is needed

        new_cursor = assign_start
        return new_code, new_cursor, should_delete

    else:
        # Cursor is on a usage - find the assignment that applies
        usage_pos = v_start

        # Find the most recent assignment before this usage
        assign_idx = None
        for i in range(len(assignments) - 1, -1, -1):
            if assignments[i][1] < usage_pos:
                assign_idx = i
                break

        if assign_idx is None:
            return None

        value = assignments[assign_idx][2]

        # Prepare the value for this specific usage context
        inline_value = prepare_inline_value(value, node, code)

        new_code = code[:v_start] + inline_value + code[v_end:]
        new_cursor = v_start + len(inline_value)

        return new_code, new_cursor, False
