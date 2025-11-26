"""Tree-sitter semantic analysis - replaces AST for parameter/kwarg detection."""
from typing import Set, Tuple
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Tree, Node

PY_LANGUAGE = Language(tspython.language())
PARSER = Parser(PY_LANGUAGE)


def parse_code(code: str) -> Tree:
    return PARSER.parse(bytes(code, "utf8"))


def extract_parameter_positions(tree: Tree, code: str) -> Set[Tuple[int, int, int]]:
    """Find all parameter positions: regular, keyword-only, positional-only, *args, **kwargs, lambda."""
    positions = set()
    param_scopes = {}  # {name: [(start_line, end_line), ...]}

    def add_param(name: str, scope_start: int, scope_end: int):
        if name not in param_scopes:
            param_scopes[name] = []
        param_scopes[name].append((scope_start, scope_end))

    def extract_param_name(param_node: Node) -> str:
        """Extract identifier from any parameter node type."""
        if param_node.type == 'identifier':
            return code[param_node.start_byte:param_node.end_byte]
        for child in param_node.children:
            if child.type == 'identifier':
                return code[child.start_byte:child.end_byte]
        return None

    def visit_func(node: Node):
        """Visit function/lambda nodes to build param scopes."""
        if node.type in ('function_definition', 'async_function_definition', 'lambda'):
            scope_start = node.start_point[0] + 1
            scope_end = node.end_point[0] + 1

            for child in node.children:
                if child.type in ('parameters', 'lambda_parameters'):
                    for param_node in child.children:
                        if param_node.type in ('identifier', 'typed_parameter', 'default_parameter',
                                               'typed_default_parameter', 'list_splat_parameter',
                                               'list_splat_pattern', 'dictionary_splat_parameter',
                                               'dictionary_splat_pattern'):
                            name = extract_param_name(param_node)
                            if name:
                                add_param(name, scope_start, scope_end)

        for child in node.children:
            visit_func(child)

    def find_identifiers(node: Node):
        """Find all identifier references and check if they're parameters in scope."""
        if node.type == 'identifier':
            name = code[node.start_byte:node.end_byte]
            line = node.start_point[0] + 1

            if name in param_scopes:
                for scope_start, scope_end in param_scopes[name]:
                    if scope_start <= line <= scope_end:
                        positions.add((line, node.start_point[1], node.end_byte - node.start_byte))
                        break

        for child in node.children:
            find_identifiers(child)

    visit_func(tree.root_node)
    find_identifiers(tree.root_node)
    return positions


def extract_kwarg_positions(tree: Tree, code: str) -> Set[Tuple[int, int, int]]:
    """Find keyword argument positions in function calls: foo(x=5, y=10)."""
    positions = set()

    def visit(node: Node):
        if node.type == 'keyword_argument' and node.children:
            name_node = node.children[0]
            line = name_node.start_point[0] + 1
            col = name_node.start_point[1]
            length = name_node.end_byte - name_node.start_byte
            positions.add((line, col, length))

        for child in node.children:
            visit(child)

    visit(tree.root_node)
    return positions


def extract_scope_positions(tree: Tree, code: str) -> Tuple[Set[Tuple[int, int, int]], Set[Tuple[int, int, int]], Set[Tuple[int, int, int]]]:
    """
    Find global/local/nonlocal variable positions.

    Returns (global_positions, local_positions, nonlocal_positions)
    """
    global_vars = set()  # Names declared global or defined at module level
    nonlocal_vars = set()  # Names declared nonlocal
    local_vars = {}  # {scope_key: set(var_names)} where scope_key = (start_byte, end_byte)

    # Pass 1a: Find all global/nonlocal declarations first
    def find_global_nonlocal(node: Node):
        if node.type == 'global_statement':
            for child in node.children:
                if child.type == 'identifier':
                    global_vars.add(code[child.start_byte:child.end_byte])
        elif node.type == 'nonlocal_statement':
            for child in node.children:
                if child.type == 'identifier':
                    nonlocal_vars.add(code[child.start_byte:child.end_byte])
        for child in node.children:
            find_global_nonlocal(child)

    find_global_nonlocal(tree.root_node)

    # Helper to extract all identifiers from assignment patterns (handles unpacking)
    def extract_pattern_identifiers(pattern_node):
        """Recursively extract identifiers from pattern_list, list_pattern, etc."""
        identifiers = []
        if pattern_node.type == 'identifier':
            identifiers.append(code[pattern_node.start_byte:pattern_node.end_byte])
        elif pattern_node.type in ('pattern_list', 'list_pattern', 'tuple_pattern'):
            for child in pattern_node.children:
                identifiers.extend(extract_pattern_identifiers(child))
        return identifiers

    # Pass 1b: Build scope tree and find variable assignments
    def find_assignments(node: Node, current_scope_key=None):
        # Update current scope
        if node.type in ('function_definition', 'async_function_definition', 'lambda'):
            current_scope_key = (node.start_byte, node.end_byte)
            if current_scope_key not in local_vars:
                local_vars[current_scope_key] = set()

        # Find variable assignments
        if node.type in ('assignment', 'augmented_assignment'):
            # Get left side - first child is the target (could be identifier or pattern)
            if node.children:
                target = node.children[0]
                var_names = extract_pattern_identifiers(target)

                for var_name in var_names:
                    # Don't track if it's declared global or nonlocal
                    if var_name not in global_vars and var_name not in nonlocal_vars:
                        if current_scope_key:
                            # Function-local assignment
                            if current_scope_key not in local_vars:
                                local_vars[current_scope_key] = set()
                            local_vars[current_scope_key].add(var_name)
                        else:
                            # Module-level assignment
                            global_vars.add(var_name)

        for child in node.children:
            find_assignments(child, current_scope_key)

    find_assignments(tree.root_node)

    # Pass 2: Classify all identifier references
    global_positions = set()
    local_positions = set()
    nonlocal_positions = set()

    def get_scope_key(node: Node):
        """Walk up the tree to find the enclosing function/lambda scope key."""
        current = node.parent
        while current:
            if current.type in ('function_definition', 'async_function_definition', 'lambda'):
                return (current.start_byte, current.end_byte)
            current = current.parent
        return None  # Module level

    def classify_identifiers(node: Node):
        if node.type == 'identifier':
            name = code[node.start_byte:node.end_byte]
            line = node.start_point[0] + 1
            col = node.start_point[1]
            length = node.end_byte - node.start_byte
            pos = (line, col, length)

            # Skip if it's part of a declaration statement
            parent = node.parent
            if parent and parent.type in ('global_statement', 'nonlocal_statement'):
                return

            # Get scope by walking up the tree
            scope_key = get_scope_key(node)

            # Classify based on scope and declarations
            if name in nonlocal_vars:
                nonlocal_positions.add(pos)
            elif name in global_vars:
                global_positions.add(pos)
            elif scope_key:
                if scope_key in local_vars and name in local_vars[scope_key]:
                    local_positions.add(pos)
                # else: could be from enclosing scope, builtin, or import - don't classify

        for child in node.children:
            classify_identifiers(child)

    classify_identifiers(tree.root_node)

    return (global_positions, local_positions, nonlocal_positions)
