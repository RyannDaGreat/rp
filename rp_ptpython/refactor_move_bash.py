"""
Move Selection Refactoring for Bash

Pure functions for moving selections through the bash syntax tree.
Supports moving command arguments, array elements, etc.

Usage:
    from rp.rp_ptpython import refactor_move_bash as move_bash

    code = '!echo hello world'
    result = move_bash.move(code, 12, 17, 17, 12, -1)  # Select 'world', move left
    # Returns: ('!echo world hello', ...)
"""
from typing import Tuple, Optional, List
try:
    import tree_sitter_bash as tsbash
    from tree_sitter import Language, Parser, Tree, Node
    _SUPPORTED = True
except ImportError:
    _SUPPORTED = False

_PARSER = None


def _get_parser():
    global _PARSER
    if _PARSER is None and _SUPPORTED:
        _PARSER = Parser(Language(tsbash.language()))
    return _PARSER


def parse(code: str) -> Optional['Tree']:
    """Parse bash code into tree-sitter tree."""
    parser = _get_parser()
    if not parser:
        return None
    # Strip leading ! for rp bash mode
    bash_code = code[1:] if code.startswith('!') else code
    return parser.parse(bytes(bash_code, "utf8"))


# Node types that contain movable siblings in bash
SIBLING_CONTAINERS = {
    'command',           # echo hello world -> arguments
    'pipeline',          # cmd1 | cmd2 | cmd3
    'array',             # (a b c)
    'concatenation',     # $a$b$c
}

# Statement containers (line-based)
STATEMENT_CONTAINERS = {
    'program',           # top-level statements
    'compound_statement', # { ... }
    'subshell',          # ( ... )
    'if_statement',
    'elif_clause',
    'else_clause',
    'while_statement',
    'for_statement',
    'case_statement',
}

# Content node types (not punctuation)
CONTENT_TYPES = {
    'word', 'string', 'raw_string', 'number',
    'simple_expansion', 'expansion', 'command_substitution',
    'concatenation', 'array', 'command', 'pipeline', 'list',
}


def get_content_children(node: 'Node') -> List['Node']:
    """Get children that are content (not punctuation)."""
    if node.type == 'command':
        return [c for c in node.children if c.type == 'word']
    if node.type == 'pipeline':
        return [c for c in node.children if c.type == 'command']
    if node.type in STATEMENT_CONTAINERS:
        return [c for c in node.children if c.type in ('command', 'pipeline', 'list', 'if_statement', 'while_statement', 'for_statement')]
    return [c for c in node.children if c.type in CONTENT_TYPES or c.type == 'word']


def find_smallest_containing(tree: 'Tree', start: int, end: int) -> Optional['Node']:
    """Find smallest node containing byte range."""
    best = None
    def visit(node):
        nonlocal best
        if node.start_byte <= start and end <= node.end_byte:
            if best is None or (node.end_byte - node.start_byte) < (best.end_byte - best.start_byte):
                best = node
            for child in node.children:
                visit(child)
    visit(tree.root_node)
    return best


def find_selected_siblings(siblings: List['Node'], start: int, end: int) -> List[int]:
    """Find indices of siblings overlapping with selection."""
    indices = []
    for i, sib in enumerate(siblings):
        if sib.end_byte > start and sib.start_byte < end:
            indices.append(i)
    return indices


def find_movable(tree: 'Tree', start: int, end: int):
    """Find movable element and siblings. Returns (selected_indices, container, siblings) or None."""
    node = find_smallest_containing(tree, start, end)
    while node:
        parent = node.parent
        if parent and (parent.type in SIBLING_CONTAINERS or parent.type in STATEMENT_CONTAINERS):
            siblings = get_content_children(parent)
            if len(siblings) > 1:
                selected = find_selected_siblings(siblings, start, end)
                if selected and len(selected) < len(siblings):
                    if len(selected) == 1 or selected == list(range(selected[0], selected[-1] + 1)):
                        return (selected, parent, siblings)
        node = parent
    return None


def move_element(code: str, start: int, end: int, direction: int):
    """
    Move selected element left (-1) or right (+1).
    Returns (new_code, new_start, new_end) or None.
    """
    # Adjust for ! prefix
    has_bang = code.startswith('!')
    if has_bang:
        bash_code = code[1:]
        start -= 1
        end -= 1
    else:
        bash_code = code

    tree = parse(code)
    if not tree:
        return None

    result = find_movable(tree, start, end)
    if not result:
        return None

    selected_indices, container, siblings = result
    if not selected_indices:
        return None

    first_idx = selected_indices[0]
    last_idx = selected_indices[-1]

    if direction < 0:
        if first_idx == 0:
            return None
        swap_idx = first_idx - 1
    else:
        if last_idx >= len(siblings) - 1:
            return None
        swap_idx = last_idx + 1

    # Get group bounds and text
    group_start = siblings[first_idx].start_byte
    group_end = siblings[last_idx].end_byte
    group_text = bash_code[group_start:group_end]

    # Get swap element
    swap_node = siblings[swap_idx]
    swap_text = bash_code[swap_node.start_byte:swap_node.end_byte]

    if direction < 0:
        # Moving left: [swap] [gap] [group] -> [group] [gap] [swap]
        gap = bash_code[swap_node.end_byte:group_start]
        new_bash = bash_code[:swap_node.start_byte] + group_text + gap + swap_text + bash_code[group_end:]
        new_start = swap_node.start_byte
        new_end = swap_node.start_byte + len(group_text)
    else:
        # Moving right: [group] [gap] [swap] -> [swap] [gap] [group]
        gap = bash_code[group_end:swap_node.start_byte]
        new_bash = bash_code[:group_start] + swap_text + gap + group_text + bash_code[swap_node.end_byte:]
        new_start = group_start + len(swap_text) + len(gap)
        new_end = new_start + len(group_text)

    # Restore ! prefix and adjust positions
    if has_bang:
        new_code = '!' + new_bash
        new_start += 1
        new_end += 1
    else:
        new_code = new_bash

    return new_code, new_start, new_end


def move(code: str, start: int, end: int, cursor_pos: int, anchor_pos: int, direction: int):
    """
    Move selection with cursor preservation.
    Returns (new_code, new_cursor, new_anchor, new_end) or None.
    """
    if not _SUPPORTED:
        return None

    result = move_element(code, start, end, direction)
    if not result:
        return None

    new_code, new_start, new_end = result
    cursor_at_end = cursor_pos >= end or cursor_pos > anchor_pos

    if cursor_at_end:
        return (new_code, new_end, new_start, new_end)
    else:
        return (new_code, new_start, new_end, new_end)
