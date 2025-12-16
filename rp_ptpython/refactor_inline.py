"""
Inline Variable Refactoring Module

Pure functions for inlining variable assignments.
Replaces usages of a variable with its assigned value.

Usage:
    from rp.rp_ptpython import refactor_inline as inline

    # From definition: inline all usages until next reassignment
    result = inline.inline_variable(code, cursor_pos)

    # From usage: inline just this one usage
    result = inline.inline_variable(code, cursor_pos)

    # Returns: (new_code, new_cursor, should_prompt_delete) or None

Supports:
    - Sequential reassignments: each assignment's value is valid until next assignment
    - Inline from definition OR from usage
    - Prompts to delete definition if it becomes unused

Design Decisions for Scope & Control Flow:
==========================================

1. SEQUENTIAL REASSIGNMENTS (fully supported):

   x = a         # Assignment 0
   x = f(x)      # Assignment 1: x on RHS reads from Assignment 0
   print(x)      # Usage reads from Assignment 1

   When inlining Assignment 0, we inline into Assignment 1's RHS (since
   RHS is evaluated before LHS is assigned). Result:

   x = f(a)
   print(x)

2. CONDITIONAL ASSIGNMENTS (conservative approach):

   if condition:
       x = a     # Assignment in branch
   else:
       x = b     # Different assignment in branch
   print(x)      # Which value? Unknown at parse time!

   PyCharm's approach: Only inline usages BEFORE any modification.
   Our approach: Same - we only track linear control flow. Assignments
   in different branches are found but usages after the conditional
   block cannot be deterministically mapped to either assignment.

   In practice:
   - Cursor on `x = a`: Only usages within that if-branch are inlined
   - Cursor on `x = b`: Only usages within that else-branch are inlined
   - Cursor on `print(x)`: We pick the LAST assignment by position,
     which may not be semantically correct. User should be aware.

3. LOOPS (conservative approach):

   for i in items:
       x = process(i)
       use(x)

   Each iteration reassigns x. We treat this like sequential assignments.
   Inlining works within the loop body as expected.

4. SCOPE BOUNDARIES:

   We find the containing scope (function/class/module) and only look
   for assignments/usages within that scope. Inner functions create
   new scopes and are handled separately.

Why this approach?
- Simple to implement and understand
- Matches user expectations for the common case (sequential code)
- Fails conservatively for ambiguous cases rather than incorrectly
- PyCharm uses similar conservative logic

References:
- PyCharm Inline: https://www.jetbrains.com/help/pycharm/inline.html
  "If the initial value is modified somewhere in the code, only the
  occurrences before modification will be inlined."
"""
from typing import Tuple, Optional, List
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Tree, Node

_PARSER: Optional[Parser] = None


def _get_parser() -> Parser:
    global _PARSER
    if _PARSER is None:
        _PARSER = Parser(Language(tspython.language()))
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


def find_identifier_at_cursor(tree: Tree, code: str, pos: int) -> Optional[Tuple[str, int, int, Node]]:
    """Find identifier at cursor. Returns (name, start, end, node) or None."""
    node = find_node_at_cursor(tree, pos)
    if node and node.type == 'identifier':
        return (code[node.start_byte:node.end_byte], node.start_byte, node.end_byte, node)
    return None


def is_assignment_target(node: Node) -> bool:
    """Check if this identifier is on the left side of an assignment or augmented assignment."""
    parent = node.parent
    if not parent:
        return False

    if parent.type == 'assignment':
        # Check if we're before the '='
        for child in parent.children:
            if child.type == '=':
                return node.end_byte <= child.start_byte
        return False

    if parent.type == 'augmented_assignment':
        # In augmented assignment, the first identifier is the target
        # Note: the target is BOTH read and written, so this is special
        for child in parent.children:
            if child.type == 'identifier':
                return child == node
            # Stop at the operator (+=, -=, etc.)
            if child.type in ('+=', '-=', '*=', '/=', '//=', '%=', '**=',
                             '&=', '|=', '^=', '>>=', '<<=', '@='):
                break
        return False

    return False


def get_assignment_value(assignment: Node, code: str) -> Optional[str]:
    """Get the right-hand side value of an assignment."""
    found_equals = False
    for child in assignment.children:
        if child.type == '=':
            found_equals = True
        elif found_equals:
            return code[child.start_byte:child.end_byte]
    return None


def is_in_conditional_branch(node: Node) -> bool:
    """
    Check if node is inside an if/elif/else branch, try/except, or similar.

    Returns True if the node's value depends on control flow that can't
    be determined at parse time.
    """
    current = node.parent
    while current:
        # if_statement contains: 'if', condition, ':', block, [elif...], [else...]
        if current.type == 'if_statement':
            # Check if we're in the block (not the condition)
            for child in current.children:
                if child.type == 'block' and child.start_byte <= node.start_byte < child.end_byte:
                    return True
                if child.type == 'else_clause' and child.start_byte <= node.start_byte < child.end_byte:
                    return True
                if child.type == 'elif_clause' and child.start_byte <= node.start_byte < child.end_byte:
                    return True

        # try_statement: try block, except handlers, else, finally
        if current.type == 'try_statement':
            for child in current.children:
                if child.type in ('block', 'except_clause', 'else_clause', 'finally_clause'):
                    if child.start_byte <= node.start_byte < child.end_byte:
                        return True

        # match_statement (Python 3.10+)
        if current.type == 'match_statement':
            return True

        current = current.parent

    return False


def find_all_assignments(tree: Tree, code: str, var_name: str, scope: Node) -> List[Tuple[int, int, str, Node]]:
    """
    Find all assignments to var_name in order.

    Returns: List of (start_byte, end_byte, value_text, assignment_node)

    Note: This finds regular assignments (x = ...) only.
    Augmented assignments (x += ...) are tracked separately as "modifications".
    """
    assignments = []

    def visit(node: Node):
        if node.start_byte < scope.start_byte or node.end_byte > scope.end_byte:
            return

        if node.type == 'assignment':
            # Check if left side is our variable
            for child in node.children:
                if child.type == 'identifier':
                    if code[child.start_byte:child.end_byte] == var_name:
                        value = get_assignment_value(node, code)
                        if value:
                            assignments.append((child.start_byte, child.end_byte, value, node))
                    break
                elif child.type == '=':
                    break

        for child in node.children:
            visit(child)

    visit(scope)
    assignments.sort(key=lambda x: x[0])
    return assignments


def find_all_modifications(tree: Tree, code: str, var_name: str, scope: Node) -> List[int]:
    """
    Find all augmented assignments (+=, -=, etc.) to var_name.

    Returns: List of byte positions where the variable is modified.
    These positions break the chain of usages for a previous assignment.
    """
    modifications = []

    def visit(node: Node):
        if node.start_byte < scope.start_byte or node.end_byte > scope.end_byte:
            return

        if node.type == 'augmented_assignment':
            # Check if left side is our variable
            for child in node.children:
                if child.type == 'identifier':
                    if code[child.start_byte:child.end_byte] == var_name:
                        modifications.append(child.start_byte)
                    break

        for child in node.children:
            visit(child)

    visit(scope)
    modifications.sort()
    return modifications


def find_all_usages(tree: Tree, code: str, var_name: str, scope: Node) -> List[Tuple[int, int, Node]]:
    """
    Find all usages (reads) of var_name, excluding assignment targets.

    Returns: List of (start_byte, end_byte, node)
    """
    usages = []

    def visit(node: Node):
        if node.start_byte < scope.start_byte or node.end_byte > scope.end_byte:
            return

        if node.type == 'identifier':
            if code[node.start_byte:node.end_byte] == var_name:
                if not is_assignment_target(node):
                    usages.append((node.start_byte, node.end_byte, node))

        for child in node.children:
            visit(child)

    visit(scope)
    usages.sort(key=lambda x: x[0])
    return usages


def is_usage_in_assignment_rhs(usage_node: Node, assignment_node: Node) -> bool:
    """Check if a usage is in the RHS of a specific assignment."""
    # Walk up from usage to see if we hit this assignment
    current = usage_node.parent
    while current:
        if current == assignment_node:
            return True
        if current.type == 'assignment':
            # Hit a different assignment
            return False
        current = current.parent
    return False


def find_usages_for_assignment(assignments: List[Tuple[int, int, str, Node]],
                                usages: List[Tuple[int, int, Node]],
                                assignment_idx: int,
                                modifications: Optional[List[int]] = None) -> List[Tuple[int, int, Node]]:
    """
    Find usages that belong to a specific assignment.

    A usage belongs to assignment N if it reads the value assigned by N.
    This includes usages on the RHS of assignment N+1 (since RHS is evaluated
    before the new assignment takes effect).

    IMPORTANT: Usages in the RHS of assignment N itself do NOT belong to N -
    they read the PREVIOUS value (e.g., `x = f(x)` - the x in f(x) reads
    the value from before this assignment).

    Args:
        modifications: List of positions where augmented assignments (+=, etc.)
                      occur. Usages after a modification don't belong to earlier
                      assignments.
    """
    if assignment_idx >= len(assignments):
        return []

    assign_end = assignments[assignment_idx][1]  # End of the LHS identifier
    assign_node = assignments[assignment_idx][3]
    modifications = modifications or []

    result = []
    for u_start, u_end, u_node in usages:
        # Must be after this assignment's LHS
        if u_start <= assign_end:
            continue

        # CRITICAL: Skip usages in the RHS of THIS assignment
        # (they read the previous value, not the one being assigned)
        if is_usage_in_assignment_rhs(u_node, assign_node):
            continue

        # Check if a modification (augmented assignment) comes between
        # this assignment and this usage - if so, usage doesn't belong to us
        modification_between = False
        for mod_pos in modifications:
            if assign_end < mod_pos < u_start:
                modification_between = True
                break
        if modification_between:
            continue

        # Check if it belongs to this assignment or a later one
        belongs_to_this = True

        # Check subsequent assignments
        for later_idx in range(assignment_idx + 1, len(assignments)):
            later_start, later_end, later_value, later_node = assignments[later_idx]

            # If usage is before the later assignment's LHS, it belongs to us
            if u_start < later_start:
                break

            # If usage is in the RHS of the later assignment, it still belongs to us
            # (the previous value is used to compute the new value)
            if is_usage_in_assignment_rhs(u_node, later_node):
                break

            # Usage is after the later assignment completed, doesn't belong to us
            belongs_to_this = False
            break

        if belongs_to_this:
            result.append((u_start, u_end, u_node))

    return result


def find_assignment_for_usage(assignments: List[Tuple[int, int, str, Node]],
                              usages: List[Tuple[int, int, Node]],
                              usage_pos: int,
                              usage_node: Node,
                              modifications: Optional[List[int]] = None) -> Optional[int]:
    """
    Find which assignment a usage belongs to.
    """
    # Check each assignment to see if this usage belongs to it
    for i in range(len(assignments)):
        relevant = find_usages_for_assignment(assignments, usages, i, modifications)
        for u_start, u_end, u_node in relevant:
            if u_start == usage_pos:
                return i
    return None


def get_containing_scope(node: Node) -> Node:
    """Find containing scope (function/class/module)."""
    current = node.parent
    while current:
        if current.type in ('function_definition', 'async_function_definition',
                           'class_definition', 'module'):
            return current
        current = current.parent
    return node


def get_line_range(code: str, node: Node) -> Tuple[int, int]:
    """Get the full line range for a node (for deletion)."""
    line_start = code.rfind('\n', 0, node.start_byte) + 1
    line_end = code.find('\n', node.end_byte)
    if line_end == -1:
        line_end = len(code)
    else:
        line_end += 1  # Include the newline
    return line_start, line_end


def needs_parens(value_text: str, parent: Node) -> bool:
    """Check if inlined value needs parentheses."""
    if not parent:
        return False

    # Lambda always needs parens when called or used in expressions
    if value_text.lstrip().startswith('lambda '):
        # Lambda needs parens in most contexts except simple assignment RHS
        if parent.type in ('call', 'argument_list', 'binary_operator',
                          'boolean_operator', 'comparison_operator',
                          'unary_operator', 'subscript', 'attribute'):
            return True

    # Operators need parens when nested in other operators
    has_op = any(op in value_text for op in ['+', '-', '*', '/', '%', '&', '|', '^'])
    has_op = has_op or ' and ' in value_text or ' or ' in value_text

    if has_op and parent.type in ('binary_operator', 'boolean_operator',
                                   'comparison_operator', 'unary_operator'):
        return True

    return False


# =============================================================================
# PURE API
# =============================================================================

def check_inline(code: str, cursor_pos: int) -> Tuple[bool, Optional[str], Optional[dict]]:
    """
    Check if inline is possible at cursor.

    Returns: (can_inline, error_message, info_dict)
    """
    tree = parse(code)
    ident = find_identifier_at_cursor(tree, code, cursor_pos)

    if not ident:
        return False, "Cursor must be on an identifier", None

    name, start, end, node = ident
    scope = get_containing_scope(node)
    assignments = find_all_assignments(tree, code, name, scope)
    usages = find_all_usages(tree, code, name, scope)
    modifications = find_all_modifications(tree, code, name, scope)

    if not assignments:
        return False, f"No assignment found for '{name}'", None

    is_target = is_assignment_target(node)

    if is_target:
        # Cursor on definition - find which assignment
        assign_idx = None
        for i, (s, e, v, n) in enumerate(assignments):
            if s == start:
                assign_idx = i
                break

        if assign_idx is None:
            return False, "Could not find assignment", None

        relevant_usages = find_usages_for_assignment(assignments, usages, assign_idx, modifications)
        if not relevant_usages:
            return False, f"No usages of '{name}' to inline (before next reassignment)", None

        # Check if assignment is in a conditional branch
        assign_node = assignments[assign_idx][3]
        in_conditional = is_in_conditional_branch(assign_node)

        return True, None, {
            'name': name,
            'value': assignments[assign_idx][2],
            'usage_count': len(relevant_usages),
            'is_definition': True,
            'in_conditional': in_conditional
        }
    else:
        # Cursor on usage - find which assignment it belongs to
        assign_idx = find_assignment_for_usage(assignments, usages, start, node, modifications)

        if assign_idx is None:
            return False, f"No assignment found before this usage of '{name}'", None

        # Check if the source assignment is in a conditional branch
        assign_node = assignments[assign_idx][3]
        in_conditional = is_in_conditional_branch(assign_node)

        return True, None, {
            'name': name,
            'value': assignments[assign_idx][2],
            'usage_count': 1,
            'is_definition': False,
            'in_conditional': in_conditional
        }


def inline_variable(code: str, cursor_pos: int, delete_if_unused: bool = False) -> Optional[Tuple[str, int, bool]]:
    """
    Inline variable at cursor.

    If cursor is on assignment target: inline all usages until next reassignment
    If cursor is on usage: inline just this usage

    Args:
        code: Source code
        cursor_pos: Cursor position
        delete_if_unused: If True, delete the assignment if no usages remain

    Returns: (new_code, new_cursor, should_prompt_delete) or None
             should_prompt_delete is True if definition has no more usages
    """
    tree = parse(code)
    ident = find_identifier_at_cursor(tree, code, cursor_pos)

    if not ident:
        return None

    name, start, end, node = ident
    scope = get_containing_scope(node)
    assignments = find_all_assignments(tree, code, name, scope)
    usages = find_all_usages(tree, code, name, scope)
    modifications = find_all_modifications(tree, code, name, scope)

    if not assignments:
        return None

    is_target = is_assignment_target(node)

    if is_target:
        # Inline from definition - replace all usages until next reassignment
        assign_idx = None
        for i, (s, e, v, n) in enumerate(assignments):
            if s == start:
                assign_idx = i
                break

        if assign_idx is None:
            return None

        value_text = assignments[assign_idx][2]
        assign_node = assignments[assign_idx][3]
        relevant_usages = find_usages_for_assignment(assignments, usages, assign_idx, modifications)

        if not relevant_usages:
            return None

        # Replace usages in reverse order
        new_code = code
        for u_start, u_end, u_node in reversed(relevant_usages):
            parent = u_node.parent
            if needs_parens(value_text, parent):
                replacement = f'({value_text})'
            else:
                replacement = value_text
            new_code = new_code[:u_start] + replacement + new_code[u_end:]

        # Check if we should delete the assignment
        # We inlined all usages that belonged to this assignment.
        # The assignment can be deleted if no NEW usages were created.
        #
        # Tricky case: `x = f(x)` inlined to `print(f(x))` - the `x` inside
        # `f(x)` reads from BEFORE the assignment, not from it. After inlining,
        # the copied `x` is positionally after the assignment but still reads
        # from before. We handle this by checking if the ONLY remaining usages
        # are inside the inlined copies of the RHS value.

        should_prompt = False
        if delete_if_unused:
            new_tree = parse(new_code)
            new_assignments = find_all_assignments(new_tree, new_code, name, new_tree.root_node)
            new_usages = find_all_usages(new_tree, new_code, name, new_tree.root_node)
            new_modifications = find_all_modifications(new_tree, new_code, name, new_tree.root_node)

            # Find this assignment in new code by matching the value
            for i, (s, e, v, n) in enumerate(new_assignments):
                if v == value_text:
                    remaining = find_usages_for_assignment(new_assignments, new_usages, i, new_modifications)

                    # Check if all remaining usages are inside inlined copies of the RHS
                    # (i.e., they contain the same value_text pattern)
                    all_in_rhs_copies = True
                    for u_start, u_end, u_node in remaining:
                        # Walk up to see if this usage is inside a copy of value_text
                        # Simple heuristic: check if the usage is within a substring
                        # that matches our value pattern
                        context_start = max(0, u_start - len(value_text))
                        context_end = min(len(new_code), u_end + len(value_text))
                        context = new_code[context_start:context_end]
                        if value_text not in context:
                            all_in_rhs_copies = False
                            break

                    if not remaining or all_in_rhs_copies:
                        # Safe to delete - no usages, or all usages are inside
                        # inlined copies (which read from before this assignment)
                        stmt_node = n.parent
                        if stmt_node and stmt_node.type == 'expression_statement':
                            line_start, line_end = get_line_range(new_code, stmt_node)
                            new_code = new_code[:line_start] + new_code[line_end:]
                    break
        else:
            # Just check if we should prompt
            new_tree = parse(new_code)
            new_assignments = find_all_assignments(new_tree, new_code, name, new_tree.root_node)
            new_usages = find_all_usages(new_tree, new_code, name, new_tree.root_node)
            new_modifications = find_all_modifications(new_tree, new_code, name, new_tree.root_node)

            for i, (s, e, v, n) in enumerate(new_assignments):
                if v == value_text:
                    remaining = find_usages_for_assignment(new_assignments, new_usages, i, new_modifications)
                    # Same heuristic for prompting
                    all_in_rhs_copies = True
                    for u_start, u_end, u_node in remaining:
                        context_start = max(0, u_start - len(value_text))
                        context_end = min(len(new_code), u_end + len(value_text))
                        context = new_code[context_start:context_end]
                        if value_text not in context:
                            all_in_rhs_copies = False
                            break
                    should_prompt = not remaining or all_in_rhs_copies
                    break

        return new_code, cursor_pos, should_prompt

    else:
        # Inline from usage - replace just this one usage
        assign_idx = find_assignment_for_usage(assignments, usages, start, node, modifications)

        if assign_idx is None:
            return None

        value_text = assignments[assign_idx][2]
        parent = node.parent

        if needs_parens(value_text, parent):
            replacement = f'({value_text})'
        else:
            replacement = value_text

        new_code = code[:start] + replacement + code[end:]
        new_cursor = start + len(replacement)

        # Check if this was the last usage of that assignment
        relevant_usages = find_usages_for_assignment(assignments, usages, assign_idx, modifications)
        should_prompt = len(relevant_usages) == 1  # This was the only one

        return new_code, new_cursor, should_prompt


def delete_assignment(code: str, cursor_pos: int) -> Optional[Tuple[str, int]]:
    """
    Delete the assignment at cursor (the whole line).

    Returns: (new_code, new_cursor) or None
    """
    tree = parse(code)
    ident = find_identifier_at_cursor(tree, code, cursor_pos)

    if not ident:
        return None

    name, start, end, node = ident

    if not is_assignment_target(node):
        return None

    # Find the assignment node
    assign_node = node.parent
    if assign_node and assign_node.type == 'assignment':
        stmt_node = assign_node.parent
        if stmt_node and stmt_node.type == 'expression_statement':
            line_start, line_end = get_line_range(code, stmt_node)
            new_code = code[:line_start] + code[line_end:]
            return new_code, line_start

    return None
