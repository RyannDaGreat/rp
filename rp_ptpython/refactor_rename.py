"""
Rename Variable Refactoring Module

Pure functions for renaming variables/identifiers.
Uses the same inline prompt pattern as extract variable.

Usage:
    from rp.rp_ptpython import refactor_rename as rename

    # Check if cursor is on a renamable identifier
    can_rename, error, info = rename.check_rename(code, cursor_pos)

    # Get all occurrences to preview
    occurrences = rename.find_occurrences(code, cursor_pos)

    # Perform rename
    new_code = rename.rename_identifier(code, cursor_pos, new_name)

Supported:
    - Variables
    - Function names
    - Class names
    - Parameters
    - All occurrences in scope
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
    """Find the smallest node containing the cursor position."""
    best = None
    best_size = float('inf')

    def visit(node: Node):
        nonlocal best, best_size
        # Node must contain cursor (inclusive on both ends)
        if node.start_byte <= pos < node.end_byte or (node.start_byte == pos == node.end_byte):
            size = node.end_byte - node.start_byte
            if size < best_size:
                best = node
                best_size = size
            for child in node.children:
                visit(child)

    visit(tree.root_node)
    return best


def find_identifier_at_cursor(tree: Tree, code: str, pos: int) -> Optional[Tuple[str, int, int]]:
    """
    Find identifier at cursor position.

    Returns: (name, start, end) or None
    """
    node = find_node_at_cursor(tree, pos)
    if not node:
        return None

    # If we're on an identifier, use it
    if node.type == 'identifier':
        name = code[node.start_byte:node.end_byte]
        return (name, node.start_byte, node.end_byte)

    # Check if we're on a function/class definition name
    if node.type in ('function_definition', 'async_function_definition', 'class_definition'):
        for child in node.children:
            if child.type == 'identifier':
                name = code[child.start_byte:child.end_byte]
                return (name, child.start_byte, child.end_byte)

    return None


def find_containing_scope(node: Node) -> Node:
    """Find the containing scope (function, class, or module)."""
    current = node.parent
    while current:
        if current.type in ('function_definition', 'async_function_definition',
                           'class_definition', 'module'):
            return current
        current = current.parent
    return node


def find_definition_scope(tree: Tree, code: str, name: str, pos: int) -> Node:
    """
    Find the scope where the identifier is defined.
    Falls back to module scope if not found.
    """
    # Start from cursor position and walk up
    node = find_node_at_cursor(tree, pos)
    if not node:
        return tree.root_node

    current = node
    while current:
        # Check if this scope defines the name
        if current.type in ('function_definition', 'async_function_definition'):
            # Check parameters
            for child in current.children:
                if child.type == 'parameters':
                    for param in child.children:
                        if param.type == 'identifier':
                            if code[param.start_byte:param.end_byte] == name:
                                return current
                        elif param.type in ('default_parameter', 'typed_parameter',
                                          'typed_default_parameter'):
                            for p in param.children:
                                if p.type == 'identifier':
                                    if code[p.start_byte:p.end_byte] == name:
                                        return current
                                    break

            # Check function name
            for child in current.children:
                if child.type == 'identifier':
                    if code[child.start_byte:child.end_byte] == name:
                        return current.parent or current
                    break

        elif current.type == 'class_definition':
            # Check class name
            for child in current.children:
                if child.type == 'identifier':
                    if code[child.start_byte:child.end_byte] == name:
                        return current.parent or current
                    break

        elif current.type == 'for_statement':
            # Check loop variable
            for child in current.children:
                if child.type == 'identifier':
                    if code[child.start_byte:child.end_byte] == name:
                        return current
                elif child.type == 'in':
                    break

        # Check local assignments in block
        if current.type in ('module', 'block', 'function_definition',
                           'async_function_definition', 'class_definition'):
            for child in current.children:
                if child.type == 'expression_statement':
                    for c in child.children:
                        if c.type == 'assignment':
                            for cc in c.children:
                                if cc.type == 'identifier':
                                    if code[cc.start_byte:cc.end_byte] == name:
                                        return current
                                    break
                                elif cc.type == '=':
                                    break

        current = current.parent

    return tree.root_node


def find_all_occurrences(tree: Tree, code: str, name: str, scope: Node) -> List[Tuple[int, int]]:
    """
    Find all occurrences of identifier within scope.

    Returns: List of (start, end) byte positions
    """
    occurrences = []

    def visit(node: Node):
        # Check bounds
        if node.end_byte < scope.start_byte or node.start_byte > scope.end_byte:
            return

        if node.type == 'identifier':
            if code[node.start_byte:node.end_byte] == name:
                occurrences.append((node.start_byte, node.end_byte))

        for child in node.children:
            visit(child)

    visit(scope)
    return occurrences


def is_valid_identifier(name: str) -> Tuple[bool, Optional[str]]:
    """Check if name is a valid Python identifier."""
    if not name:
        return False, "Name cannot be empty"
    if not name.isidentifier():
        return False, "'%s' is not a valid identifier" % name
    if name in ('False', 'True', 'None', 'and', 'as', 'assert', 'async', 'await',
                'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
                'except', 'finally', 'for', 'from', 'global', 'if', 'import',
                'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise',
                'return', 'try', 'while', 'with', 'yield'):
        return False, "'%s' is a reserved keyword" % name
    return True, None


# =============================================================================
# IMPORT HANDLING
# =============================================================================

def _get_import_context(tree: Tree, code: str, pos: int) -> Optional[dict]:
    """
    Check if cursor is on an import name and return context info.

    Returns dict with:
        - 'type': 'import' or 'from_import'
        - 'name': the identifier name at cursor
        - 'is_alias': True if cursor is on alias (after 'as')
        - 'is_module_name': True if cursor is on the module/dotted name (before 'as')
        - 'import_node': the import_statement or import_from_statement node
        - 'aliased_import_node': the aliased_import node if applicable
        - 'dotted_name_node': the dotted_name node for the module
        - 'alias_identifier_node': the identifier node for alias if exists
        - 'has_existing_alias': True if there's already an 'as' clause
    """
    node = find_node_at_cursor(tree, pos)
    if not node:
        return None

    # If we landed on dotted_name with a single identifier, use that identifier
    if node.type == 'dotted_name':
        identifiers = [c for c in node.children if c.type == 'identifier']
        if len(identifiers) == 1:
            node = identifiers[0]
        else:
            # For multi-part dotted names, find which identifier we're on
            for ident in identifiers:
                if ident.start_byte <= pos < ident.end_byte:
                    node = ident
                    break
            else:
                return None

    if node.type != 'identifier':
        return None

    name = code[node.start_byte:node.end_byte]

    # Walk up to find import context
    current = node.parent
    while current:
        if current.type == 'import_statement':
            return _analyze_import_statement(current, node, name, code)
        elif current.type == 'import_from_statement':
            return _analyze_from_import_statement(current, node, name, code)
        current = current.parent

    return None


def _analyze_import_statement(import_node: Node, ident_node: Node, name: str, code: str) -> Optional[dict]:
    """Analyze 'import x' or 'import x as y' statement."""
    # Check if identifier is part of an aliased_import
    parent = ident_node.parent

    if parent.type == 'aliased_import':
        # Cursor is directly on the alias identifier (after 'as')
        dotted_name_node = None
        alias_node = None
        for child in parent.children:
            if child.type == 'dotted_name':
                dotted_name_node = child
            elif child.type == 'identifier':
                alias_node = child

        return {
            'type': 'import',
            'name': name,
            'is_alias': True,
            'is_module_name': False,
            'import_node': import_node,
            'aliased_import_node': parent,
            'dotted_name_node': dotted_name_node,
            'alias_identifier_node': alias_node,
            'has_existing_alias': True,
        }

    elif parent.type == 'dotted_name':
        # Check if dotted_name is inside an aliased_import
        grandparent = parent.parent
        if grandparent and grandparent.type == 'aliased_import':
            # Cursor is on the module name inside an aliased import
            # e.g., cursor on 'numpy' in 'import numpy as np'
            # This is not renamable - user should rename the alias
            alias_node = None
            for child in grandparent.children:
                if child.type == 'identifier':
                    alias_node = child

            return {
                'type': 'import',
                'name': name,
                'is_alias': False,
                'is_module_name': True,
                'import_node': import_node,
                'aliased_import_node': grandparent,
                'dotted_name_node': parent,
                'alias_identifier_node': alias_node,
                'has_existing_alias': True,  # There IS an existing alias
            }

        # Simple import without alias: import numpy
        # The identifier could be the module name or part of dotted path
        # For renaming, we only care about the LAST part of the dotted name
        # which is what gets used in code
        last_ident = None
        for child in parent.children:
            if child.type == 'identifier':
                last_ident = child

        # Only allow renaming the last identifier in the dotted name
        if last_ident and ident_node.start_byte == last_ident.start_byte:
            return {
                'type': 'import',
                'name': name,
                'is_alias': False,
                'is_module_name': True,
                'import_node': import_node,
                'aliased_import_node': None,
                'dotted_name_node': parent,
                'alias_identifier_node': None,
                'has_existing_alias': False,
            }

    return None


def _analyze_from_import_statement(import_node: Node, ident_node: Node, name: str, code: str) -> Optional[dict]:
    """Analyze 'from x import y' or 'from x import y as z' statement."""
    parent = ident_node.parent

    # Check if we're on the module being imported from (not supported for rename)
    # We only support renaming the imported names, not the source module
    for child in import_node.children:
        if child.type == 'dotted_name':
            # This is the source module (after 'from')
            # Skip until we hit 'import' keyword
            pass
        if child.type == 'import':
            break

    if parent.type == 'aliased_import':
        # from x import foo as f - check if we're on alias or name
        dotted_name_node = None
        alias_node = None
        for child in parent.children:
            if child.type == 'dotted_name':
                dotted_name_node = child
            elif child.type == 'identifier':
                alias_node = child

        is_alias = (alias_node is not None and
                    ident_node.start_byte == alias_node.start_byte)
        is_imported_name = not is_alias

        return {
            'type': 'from_import',
            'name': name,
            'is_alias': is_alias,
            'is_module_name': is_imported_name,  # Actually the imported name, not module
            'import_node': import_node,
            'aliased_import_node': parent,
            'dotted_name_node': dotted_name_node,
            'alias_identifier_node': alias_node,
            'has_existing_alias': True,
        }

    elif parent.type == 'dotted_name':
        # Check if this dotted_name comes after the 'import' keyword
        # (i.e., it's an imported name, not the source module)
        found_import_keyword = False
        for child in import_node.children:
            if child.type == 'import':
                found_import_keyword = True
            elif found_import_keyword and child.type == 'dotted_name':
                if child.start_byte == parent.start_byte:
                    # This is an imported name without alias
                    return {
                        'type': 'from_import',
                        'name': name,
                        'is_alias': False,
                        'is_module_name': True,
                        'import_node': import_node,
                        'aliased_import_node': None,
                        'dotted_name_node': parent,
                        'alias_identifier_node': None,
                        'has_existing_alias': False,
                    }
            elif found_import_keyword and child.type == 'aliased_import':
                # Check inside aliased_import
                for ac in child.children:
                    if ac.type == 'dotted_name' and ac.start_byte == parent.start_byte:
                        # We're on the imported name inside an aliased_import
                        alias_node = None
                        for ac2 in child.children:
                            if ac2.type == 'identifier':
                                alias_node = ac2
                        return {
                            'type': 'from_import',
                            'name': name,
                            'is_alias': False,
                            'is_module_name': True,
                            'import_node': import_node,
                            'aliased_import_node': child,
                            'dotted_name_node': parent,
                            'alias_identifier_node': alias_node,
                            'has_existing_alias': alias_node is not None,
                        }

    return None


def _find_dotted_usages(tree: Tree, code: str, dotted_name: str, exclude_range: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Find all usages of a dotted name like 'os.path' in code.

    For dotted imports, the usage appears as attribute access:
        os.path -> attribute node with object='os' and attribute='path'

    Tree structure for `os.path`:
        attribute [start:end]
            identifier 'os'     (the object)
            .
            identifier 'path'   (the attribute name)

    Returns list of (start, end) byte positions for the full dotted access.
    """
    parts = dotted_name.split('.')
    if len(parts) < 2:
        return []

    usages = []

    def find_attribute_chain(node: Node) -> Optional[Tuple[int, int]]:
        """Check if node is an attribute access matching our dotted name."""
        if node.type != 'attribute':
            return None

        # Build the chain by walking down the object side
        # and collecting attribute names
        chain = []
        current = node
        full_start = node.start_byte
        full_end = node.end_byte

        while current:
            if current.type == 'attribute':
                # Get children - structure is: object, '.', attribute_name
                children = list(current.children)
                # Find the attribute name (the LAST identifier, after the '.')
                attr_name = None
                obj_node = None
                for i, child in enumerate(children):
                    if child.type == '.':
                        # Everything before is object, after is attribute
                        if i + 1 < len(children) and children[i + 1].type == 'identifier':
                            attr_name = code[children[i + 1].start_byte:children[i + 1].end_byte]
                        if i > 0:
                            obj_node = children[0]  # First child is the object
                        break

                if attr_name:
                    chain.insert(0, attr_name)

                if obj_node:
                    current = obj_node
                else:
                    break
            elif current.type == 'identifier':
                chain.insert(0, code[current.start_byte:current.end_byte])
                break
            else:
                break

        if chain == parts:
            return (full_start, full_end)
        return None

    def visit(node: Node):
        # Skip excluded range (the import statement)
        if node.start_byte >= exclude_range[0] and node.end_byte <= exclude_range[1]:
            return

        result = find_attribute_chain(node)
        if result:
            usages.append(result)
            return  # Don't visit children of matched node

        for child in node.children:
            visit(child)

    visit(tree.root_node)
    return usages


def _rename_import(code: str, tree: Tree, import_ctx: dict, new_name: str) -> Optional[Tuple[str, int]]:
    """
    Handle renaming in import context.

    Returns: (new_code, new_cursor_pos) or None
    """
    old_name = import_ctx['name']

    if import_ctx['is_alias']:
        # Renaming an existing alias: just update the alias and usages
        # import numpy as np -> import numpy as npy
        # from x import foo as f -> from x import foo as func
        alias_node = import_ctx['alias_identifier_node']
        if not alias_node:
            return None

        # Find all usages of the alias and rename them
        scope = tree.root_node  # Import aliases are module-scoped
        occurrences = find_all_occurrences(tree, code, old_name, scope)

        if not occurrences:
            return None

        # Sort in reverse order for safe replacement
        occurrences.sort(reverse=True)

        new_code = code
        for start, end in occurrences:
            new_code = new_code[:start] + new_name + new_code[end:]

        # Calculate cursor position at end of new alias in import
        new_cursor = alias_node.start_byte + len(new_name)

        return new_code, new_cursor

    else:
        # Renaming a module/imported name that doesn't have an alias yet,
        # or has an alias but cursor is on the original name
        if import_ctx['has_existing_alias']:
            # Cursor is on original name but there's already an alias
            # Just update usages (which use the alias), leave import alone
            # Actually, if there's an alias, the alias is what's used in code
            # So renaming the original name wouldn't make sense
            # User should rename the alias instead
            return None

        # No existing alias - we need to add one
        # import numpy -> import numpy as np
        # from x import foo -> from x import foo as f
        dotted_name_node = import_ctx['dotted_name_node']
        if not dotted_name_node:
            return None

        # Get the full dotted name from the import
        full_dotted_name = code[dotted_name_node.start_byte:dotted_name_node.end_byte]

        # Find where to insert " as new_name"
        insert_pos = dotted_name_node.end_byte

        # Get import statement range to exclude from search
        import_node = import_ctx['import_node']
        exclude_range = (import_node.start_byte, import_node.end_byte)

        # Check if this is a dotted import (e.g., os.path)
        if '.' in full_dotted_name:
            # For dotted imports, find attribute access usages
            usages = _find_dotted_usages(tree, code, full_dotted_name, exclude_range)
        else:
            # Simple import - find identifier usages
            scope = tree.root_node
            occurrences = find_all_occurrences(tree, code, old_name, scope)

            # Filter out occurrences in import statement
            usages = []
            for start, end in occurrences:
                if start >= import_node.start_byte and end <= import_node.end_byte:
                    continue
                usages.append((start, end))

        # Sort in reverse order for safe replacement
        usages.sort(reverse=True)

        new_code = code

        # Replace usages first (in reverse order)
        for start, end in usages:
            new_code = new_code[:start] + new_name + new_code[end:]

        # Now insert the alias clause
        alias_clause = " as " + new_name
        new_code = new_code[:insert_pos] + alias_clause + new_code[insert_pos:]

        # Cursor at end of new alias
        new_cursor = insert_pos + len(alias_clause)

        return new_code, new_cursor


# =============================================================================
# PURE API
# =============================================================================

def check_rename(code: str, cursor_pos: int) -> Tuple[bool, Optional[str], Optional[dict]]:
    """
    Check if rename refactoring is possible at cursor position.

    Returns: (can_rename, error_message, info_dict)
    """
    tree = parse(code)

    # Check import context first (imports may not be found by find_identifier_at_cursor)
    import_ctx = _get_import_context(tree, code, cursor_pos)
    if import_ctx:
        # For imports with existing alias, cursor on original name is not renamable
        if import_ctx['has_existing_alias'] and not import_ctx['is_alias']:
            return False, "Rename the alias instead (after 'as')", None
        # Import renames are always module-scoped
        name = import_ctx['name']
        scope = tree.root_node
        occurrences = find_all_occurrences(tree, code, name, scope)
        return True, None, {
            'name': name,
            'occurrence_count': len(occurrences),
            'scope_count': len(occurrences),
            'is_import': True,
        }

    # Regular identifier check
    result = find_identifier_at_cursor(tree, code, cursor_pos)
    if not result:
        return False, "Cursor must be on an identifier", None

    name, start, end = result

    # Don't rename built-in names (simple check)
    builtins = {'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict',
                'set', 'tuple', 'bool', 'type', 'isinstance', 'hasattr', 'getattr',
                'setattr', 'open', 'input', 'sum', 'min', 'max', 'abs', 'all', 'any'}
    if name in builtins:
        return False, "Cannot rename built-in '%s'" % name, None

    # Get scope-based count
    scope = find_definition_scope(tree, code, name, cursor_pos)
    scope_occurrences = find_all_occurrences(tree, code, name, scope)

    # Get everywhere count (whole file)
    all_occurrences = find_all_occurrences(tree, code, name, tree.root_node)

    return True, None, {
        'name': name,
        'occurrence_count': len(all_occurrences),
        'scope_count': len(scope_occurrences),
        'is_import': False,
    }


def find_occurrences(code: str, cursor_pos: int) -> List[Tuple[int, int]]:
    """
    Find all occurrences of the identifier at cursor.

    Returns: List of (start, end) positions
    """
    tree = parse(code)
    result = find_identifier_at_cursor(tree, code, cursor_pos)

    if not result:
        return []

    name, _, _ = result
    scope = find_definition_scope(tree, code, name, cursor_pos)
    return find_all_occurrences(tree, code, name, scope)


def rename_identifier(code: str, cursor_pos: int, new_name: str, everywhere: bool = True) -> Optional[Tuple[str, int]]:
    """
    Rename the identifier at cursor position.

    Args:
        code: Source code
        cursor_pos: Cursor position
        new_name: New name for the identifier
        everywhere: If True, rename all occurrences in file. If False, only in scope.

    Handles special cases:
        - import numpy -> import numpy as np (when renaming numpy to np)
        - import numpy as np -> import numpy as npy (when renaming np to npy)
        - from x import foo -> from x import foo as f (when renaming foo to f)
        - from x import foo as f -> from x import foo as func (when renaming f to func)

    Returns: (new_code, new_cursor_pos) or None if cannot rename
    """
    # Validate new name
    valid, error = is_valid_identifier(new_name)
    if not valid:
        return None

    tree = parse(code)

    # Check for import context first - it has special node handling
    import_ctx = _get_import_context(tree, code, cursor_pos)
    if import_ctx:
        old_name = import_ctx['name']
        if old_name == new_name:
            return None  # No change needed
        return _rename_import(code, tree, import_ctx, new_name)

    # Normal rename - requires identifier at cursor
    result = find_identifier_at_cursor(tree, code, cursor_pos)

    if not result:
        return None

    old_name, _, _ = result
    if old_name == new_name:
        return None  # No change needed

    # Normal variable/function/class rename
    if everywhere:
        # Rename all occurrences in the entire file
        scope = tree.root_node
    else:
        # Rename only in the definition scope
        scope = find_definition_scope(tree, code, old_name, cursor_pos)
    occurrences = find_all_occurrences(tree, code, old_name, scope)

    if not occurrences:
        return None

    # Sort in reverse order for safe replacement
    occurrences.sort(reverse=True)

    # Replace all occurrences
    new_code = code
    for start, end in occurrences:
        new_code = new_code[:start] + new_name + new_code[end:]

    # Calculate new cursor position
    # Find the occurrence that was at or after cursor
    length_diff = len(new_name) - len(old_name)
    new_cursor = cursor_pos

    for start, end in sorted(occurrences):
        if start <= cursor_pos:
            if cursor_pos <= end:
                # Cursor was inside this occurrence
                new_cursor = start + len(new_name)
                break
            else:
                new_cursor += length_diff

    return new_code, new_cursor


# =============================================================================
# UI STATE (for inline prompt, like extract variable)
# =============================================================================

class RenameState:
    """State for the rename prompt UI with live preview."""
    def __init__(self):
        self.active = False
        self.name = ""          # New name being typed
        self.name_cursor = 0    # Cursor position in name input
        self.old_name = ""      # Original name
        self.cursor_pos = 0     # Original cursor position in code
        self.error = None
        self.occurrence_count = 0
        self.scope_count = 0    # Count in current scope only
        self.everywhere = True  # True = everywhere, False = scope-based
        self.is_import = False  # True if renaming an import
        self.original_code = ""  # Store original for preview/cancel

    def start(self, old_name: str, cursor_pos: int, count: int, scope_count: int = 0, is_import: bool = False, original_code: str = ""):
        self.active = True
        self.name = old_name    # Start with old name
        self.name_cursor = len(old_name)  # Cursor at end
        self.old_name = old_name
        self.cursor_pos = cursor_pos
        self.error = None
        self.occurrence_count = count
        self.scope_count = scope_count if scope_count else count
        self.everywhere = True  # Default to everywhere
        self.is_import = is_import
        self.original_code = original_code

    def reset(self):
        self.active = False
        self.name = ""
        self.name_cursor = 0
        self.old_name = ""
        self.cursor_pos = 0
        self.error = None
        self.occurrence_count = 0
        self.scope_count = 0
        self.everywhere = True
        self.is_import = False
        self.original_code = ""

    def toggle_mode(self):
        """Toggle between everywhere and scope-based rename."""
        if not self.is_import:  # Imports are always file-wide
            self.everywhere = not self.everywhere

    def get_count(self) -> int:
        """Get current occurrence count based on mode."""
        return self.occurrence_count if self.everywhere else self.scope_count

    def has_valid_input(self) -> bool:
        return len(self.name.strip()) > 0

    def add_char(self, char: str):
        """Add a character at cursor position."""
        self.name = self.name[:self.name_cursor] + char + self.name[self.name_cursor:]
        self.name_cursor += 1

    def delete_char(self):
        """Delete character before cursor."""
        if self.name_cursor > 0:
            self.name = self.name[:self.name_cursor-1] + self.name[self.name_cursor:]
            self.name_cursor -= 1

    def cursor_left(self):
        if self.name_cursor > 0: self.name_cursor -= 1

    def cursor_right(self):
        if self.name_cursor < len(self.name): self.name_cursor += 1

    def delete_forward(self):
        """Delete character at cursor."""
        if self.name_cursor < len(self.name):
            self.name = self.name[:self.name_cursor] + self.name[self.name_cursor+1:]

    def get_preview(self) -> Optional[Tuple[str, int]]:
        """Get live preview of the rename. Returns (new_code, new_cursor) or None."""
        if not self.active or not self.original_code:
            return None
        new_name = self.name.strip()
        if not new_name or new_name == self.old_name:
            return None
        # Validate it's a valid identifier
        valid, _ = is_valid_identifier(new_name)
        if not valid:
            return None
        return rename_identifier(self.original_code, self.cursor_pos, new_name, self.everywhere)


# Global state instance
state = RenameState()


# =============================================================================
# HIGH-LEVEL HANDLERS
# =============================================================================

def handle_start(code: str, cursor_pos: int) -> bool:
    """
    Start rename mode.

    Returns: True if started, False if cannot rename at cursor
    """
    can_rename, error, info = check_rename(code, cursor_pos)

    if not can_rename:
        state.active = True
        state.error = error
        return False

    state.start(
        info['name'],
        cursor_pos,
        info['occurrence_count'],
        info.get('scope_count', info['occurrence_count']),
        info.get('is_import', False),
        code  # Save original for live preview
    )
    return True


def handle_char(char: str) -> bool:
    """Handle character input. Returns True if handled."""
    if not state.active:
        return False
    if state.error:
        state.error = None
    if char.isalnum() or char == '_':
        state.add_char(char)
    return True


def handle_backspace() -> bool:
    """Handle backspace. Returns True if handled."""
    if not state.active:
        return False
    if state.error:
        state.error = None
    state.delete_char()
    return True


def handle_confirm(code: str) -> Optional[Tuple[str, int]]:
    """
    Handle Enter. Perform the rename.

    Returns: (new_code, new_cursor) or None
    """
    if not state.active:
        return None

    new_name = state.name.strip()
    valid, error = is_valid_identifier(new_name)

    if not valid:
        state.error = error
        return None

    if new_name == state.old_name:
        state.reset()
        return None  # No change

    result = rename_identifier(code, state.cursor_pos, new_name, state.everywhere)
    state.reset()
    return result


def handle_toggle_mode():
    """Handle Tab - toggle between everywhere and scope-based rename."""
    if state.active:
        state.toggle_mode()


def handle_cancel():
    """Handle Escape/Ctrl+C."""
    state.reset()
