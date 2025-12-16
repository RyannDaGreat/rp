"""
Rename Variable Refactoring Module for Bash

Uses tree-sitter-bash for parsing. Handles bash variable semantics:
- $VAR, ${VAR}, ${VAR:-default}, etc.
- VAR=value assignments
- local VAR, export VAR, declare VAR

Bash has no real scoping - variables are global unless explicitly 'local'.
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


# Bash reserved words that cannot be variable names
BASH_RESERVED = {
    'if', 'then', 'else', 'elif', 'fi', 'case', 'esac', 'for', 'select',
    'while', 'until', 'do', 'done', 'in', 'function', 'time', 'coproc',
    '!', '{', '}', '[[', ']]',
}


def find_node_at_cursor(tree: Tree, pos: int) -> Optional[Node]:
    """Find the smallest node containing the cursor position."""
    best = None
    best_size = float('inf')

    def visit(node: Node):
        nonlocal best, best_size
        if node.start_byte <= pos < node.end_byte or (node.start_byte == pos == node.end_byte):
            size = node.end_byte - node.start_byte
            if size < best_size:
                best = node
                best_size = size
            for child in node.children:
                visit(child)

    visit(tree.root_node)
    return best


def find_variable_at_cursor(tree: Tree, code: str, pos: int) -> Optional[Tuple[str, int, int]]:
    """
    Find variable name at cursor position.

    Returns: (name, start, end) or None
    Handles: $VAR, ${VAR}, VAR=, etc.
    """
    node = find_node_at_cursor(tree, pos)
    if not node:
        return None

    # Direct variable_name node
    if node.type == 'variable_name':
        name = code[node.start_byte:node.end_byte]
        return (name, node.start_byte, node.end_byte)

    # Simple expansion: $VAR
    if node.type == 'simple_expansion':
        for child in node.children:
            if child.type == 'variable_name':
                name = code[child.start_byte:child.end_byte]
                return (name, child.start_byte, child.end_byte)
            elif child.type == 'special_variable_name':
                # $?, $$, $!, etc. - not renamable
                return None

    # Expansion: ${VAR}, ${VAR:-default}, etc.
    if node.type == 'expansion':
        for child in node.children:
            if child.type == 'variable_name':
                name = code[child.start_byte:child.end_byte]
                return (name, child.start_byte, child.end_byte)

    # Word that might be a variable name in assignment context
    if node.type == 'word':
        parent = node.parent
        if parent and parent.type == 'variable_assignment':
            # Check if this word is the name part (before =)
            name_node = None
            for child in parent.children:
                if child.type == 'variable_name':
                    name_node = child
                    break
            if name_node and node.start_byte == name_node.start_byte:
                name = code[node.start_byte:node.end_byte]
                return (name, node.start_byte, node.end_byte)

    # Check parent for variable context
    parent = node.parent
    if parent:
        if parent.type == 'variable_assignment':
            for child in parent.children:
                if child.type == 'variable_name':
                    if child.start_byte <= pos < child.end_byte:
                        name = code[child.start_byte:child.end_byte]
                        return (name, child.start_byte, child.end_byte)
        elif parent.type in ('simple_expansion', 'expansion'):
            for child in parent.children:
                if child.type == 'variable_name':
                    name = code[child.start_byte:child.end_byte]
                    return (name, child.start_byte, child.end_byte)

    return None


def is_valid_bash_identifier(name: str) -> Tuple[bool, Optional[str]]:
    """Check if name is a valid bash variable identifier."""
    if not name:
        return False, "Name cannot be empty"
    # Bash variable names: letters, digits, underscores, cannot start with digit
    if name[0].isdigit():
        return False, "Variable name cannot start with a digit"
    for c in name:
        if not (c.isalnum() or c == '_'):
            return False, f"Invalid character '{c}' in variable name"
    if name in BASH_RESERVED:
        return False, f"'{name}' is a reserved word"
    return True, None


def find_all_occurrences(tree: Tree, code: str, name: str) -> List[Tuple[int, int]]:
    """
    Find all occurrences of variable in bash code.

    Finds:
    - variable_name nodes matching the name
    - In assignments: VAR=value
    - In expansions: $VAR, ${VAR}
    """
    occurrences = []

    def visit(node: Node):
        if node.type == 'variable_name':
            if code[node.start_byte:node.end_byte] == name:
                occurrences.append((node.start_byte, node.end_byte))

        for child in node.children:
            visit(child)

    visit(tree.root_node)
    return occurrences


def check_rename(code: str, cursor_pos: int) -> Tuple[bool, Optional[str], Optional[dict]]:
    """
    Check if rename refactoring is possible at cursor position.

    Returns: (can_rename, error_message, info_dict)
    """
    tree = parse(code)
    result = find_variable_at_cursor(tree, code, cursor_pos)

    if not result:
        return False, "Cursor must be on a variable name", None

    name, start, end = result

    # Check for special variables
    if name.startswith('$') or name in ('?', '!', '#', '*', '@', '-', '0'):
        return False, f"Cannot rename special variable '{name}'", None

    occurrences = find_all_occurrences(tree, code, name)

    return True, None, {
        'name': name,
        'occurrence_count': len(occurrences),
    }


def find_occurrences(code: str, cursor_pos: int) -> List[Tuple[int, int]]:
    """Find all occurrences of the variable at cursor."""
    tree = parse(code)
    result = find_variable_at_cursor(tree, code, cursor_pos)

    if not result:
        return []

    name, _, _ = result
    return find_all_occurrences(tree, code, name)


def rename_variable(code: str, cursor_pos: int, new_name: str) -> Optional[Tuple[str, int]]:
    """
    Rename the variable at cursor position.

    Returns: (new_code, new_cursor_pos) or None if cannot rename
    """
    valid, error = is_valid_bash_identifier(new_name)
    if not valid:
        return None

    tree = parse(code)
    result = find_variable_at_cursor(tree, code, cursor_pos)

    if not result:
        return None

    old_name, _, _ = result
    if old_name == new_name:
        return None

    occurrences = find_all_occurrences(tree, code, old_name)

    if not occurrences:
        return None

    # Sort in reverse order for safe replacement
    occurrences.sort(reverse=True)

    new_code = code
    for start, end in occurrences:
        new_code = new_code[:start] + new_name + new_code[end:]

    # Calculate new cursor position
    length_diff = len(new_name) - len(old_name)
    new_cursor = cursor_pos

    for start, end in sorted(occurrences):
        if start <= cursor_pos:
            if cursor_pos <= end:
                new_cursor = start + len(new_name)
                break
            else:
                new_cursor += length_diff

    return new_code, new_cursor


# =============================================================================
# UI STATE
# =============================================================================

class BashRenameState:
    """State for the rename prompt UI."""
    def __init__(self):
        self.active = False
        self.name = ""
        self.name_cursor = 0
        self.old_name = ""
        self.cursor_pos = 0
        self.error = None
        self.occurrence_count = 0
        self.original_code = ""
        self.shell_prefix = False  # True if code starts with !

    def start(self, old_name: str, cursor_pos: int, count: int, original_code: str = "", shell_prefix: bool = False):
        self.active = True
        self.name = old_name
        self.name_cursor = len(old_name)
        self.old_name = old_name
        self.cursor_pos = cursor_pos
        self.error = None
        self.occurrence_count = count
        self.original_code = original_code
        self.shell_prefix = shell_prefix

    def reset(self):
        self.active = False
        self.name = ""
        self.name_cursor = 0
        self.old_name = ""
        self.cursor_pos = 0
        self.error = None
        self.occurrence_count = 0
        self.original_code = ""
        self.shell_prefix = False

    def has_valid_input(self) -> bool:
        return len(self.name.strip()) > 0

    def add_char(self, char: str):
        self.name = self.name[:self.name_cursor] + char + self.name[self.name_cursor:]
        self.name_cursor += 1

    def delete_char(self):
        if self.name_cursor > 0:
            self.name = self.name[:self.name_cursor-1] + self.name[self.name_cursor:]
            self.name_cursor -= 1

    def cursor_left(self):
        if self.name_cursor > 0:
            self.name_cursor -= 1

    def cursor_right(self):
        if self.name_cursor < len(self.name):
            self.name_cursor += 1

    def delete_forward(self):
        if self.name_cursor < len(self.name):
            self.name = self.name[:self.name_cursor] + self.name[self.name_cursor+1:]

    def toggle_mode(self):
        """Bash has no scope-based rename, so this is a no-op."""
        pass

    def get_preview(self) -> Optional[Tuple[str, int]]:
        """Get live preview of the rename."""
        if not self.active or not self.original_code:
            return None
        new_name = self.name.strip()
        if not new_name or new_name == self.old_name:
            return None
        valid, _ = is_valid_bash_identifier(new_name)
        if not valid:
            return None
        # Handle shell prefix (!)
        if self.shell_prefix:
            bash_code = self.original_code[1:]
            adj_pos = max(0, self.cursor_pos - 1)
            result = rename_variable(bash_code, adj_pos, new_name)
            if result:
                # Prepend ! back and adjust cursor
                return ('!' + result[0], result[1] + 1)
            return None
        return rename_variable(self.original_code, self.cursor_pos, new_name)


state = BashRenameState()


def handle_start(code: str, cursor_pos: int, shell_prefix: bool = False) -> bool:
    """Start rename mode. Returns True if started."""
    # Handle shell prefix (!)
    if shell_prefix:
        bash_code = code[1:] if code.startswith('!') else code
        adj_pos = max(0, cursor_pos - 1)
    else:
        bash_code = code
        adj_pos = cursor_pos

    can_rename, error, info = check_rename(bash_code, adj_pos)

    if not can_rename:
        state.active = True
        state.error = error
        return False

    state.start(
        info['name'],
        cursor_pos,  # Store original position for preview
        info['occurrence_count'],
        code,  # Store original code with ! for preview/restore
        shell_prefix
    )
    return True


def handle_confirm(code: str) -> Optional[Tuple[str, int]]:
    """Handle Enter. Perform the rename."""
    if not state.active:
        return None

    new_name = state.name.strip()
    valid, error = is_valid_bash_identifier(new_name)

    if not valid:
        state.error = error
        return None

    if new_name == state.old_name:
        state.reset()
        return None

    result = rename_variable(code, state.cursor_pos, new_name)
    state.reset()
    return result


def handle_cancel():
    """Handle Escape/Ctrl+C."""
    state.reset()
