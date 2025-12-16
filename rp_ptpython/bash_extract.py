"""
Extract Variable Refactoring Module for Bash

Extracts selected expressions into a variable assignment.
Handles bash-specific patterns like command substitution, arithmetic, etc.
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


# Node types that can be extracted
EXTRACTABLE_TYPES = {
    'word', 'string', 'raw_string', 'concatenation',
    'command_substitution', 'process_substitution',
    'arithmetic_expansion', 'expansion', 'simple_expansion',
    'number', 'array',
}


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
                if best is None or (node.end_byte - node.start_byte) < (best.end_byte - best.start_byte):
                    best = node
            for child in node.children:
                visit(child)
    visit(tree.root_node)
    return best


def find_containing_command(node: Node) -> Optional[Node]:
    """Find the containing command or statement."""
    current = node
    while current:
        if current.type in ('command', 'pipeline', 'list', 'compound_statement',
                           'if_statement', 'while_statement', 'for_statement',
                           'case_statement', 'function_definition'):
            return current
        current = current.parent
    return None


def get_line_start(code: str, byte_offset: int) -> int:
    """Get the start position of the line containing byte_offset."""
    return code.rfind('\n', 0, byte_offset) + 1


def get_line_indent(code: str, byte_offset: int) -> str:
    """Get indentation string for the line containing byte_offset."""
    line_start = get_line_start(code, byte_offset)
    indent_end = line_start
    while indent_end < len(code) and code[indent_end] in ' \t':
        indent_end += 1
    return code[line_start:indent_end]


def find_duplicate_expressions(tree: Tree, code: str, expr: str, exclude_start: int) -> List[Tuple[int, int]]:
    """Find other occurrences of the same expression."""
    # Simple text-based search for identical strings
    duplicates = []
    pos = 0
    while True:
        idx = code.find(expr, pos)
        if idx == -1:
            break
        if idx != exclude_start:
            duplicates.append((idx, idx + len(expr)))
        pos = idx + 1
    return duplicates


def is_valid_bash_identifier(name: str) -> Tuple[bool, Optional[str]]:
    """Check if name is a valid bash variable identifier."""
    if not name:
        return False, "Name cannot be empty"
    if name[0].isdigit():
        return False, "Variable name cannot start with a digit"
    for c in name:
        if not (c.isalnum() or c == '_'):
            return False, f"Invalid character '{c}' in variable name"
    return True, None


def check_extract(code: str, start: int, end: int) -> Tuple[bool, Optional[str], Optional[dict]]:
    """
    Check if extract refactoring is possible for selection.

    Returns: (can_extract, error_message, info_dict)
    """
    if start >= end:
        return False, "No selection", None

    tree = parse(code)

    # Find an extractable node
    node = find_smallest_extractable(tree, start, end)
    if not node:
        # Even if no AST node, allow extracting raw text
        pass

    selected = code[start:end].strip()
    if not selected:
        return False, "Selection is empty", None

    # Find duplicates
    duplicates = find_duplicate_expressions(tree, code, selected, start)

    return True, None, {
        'selected': selected,
        'duplicate_count': len(duplicates),
    }


def is_inside_quotes(code: str, start: int, end: int) -> Optional[str]:
    """
    Check if selection is inside quotes.
    Returns the quote character if inside quotes, None otherwise.
    """
    # Look for quote before start
    for i in range(start - 1, -1, -1):
        if code[i] in '"\'':
            # Found a quote, check if it's opening
            # Count quotes from line start
            line_start = code.rfind('\n', 0, i) + 1
            quote_char = code[i]
            count = 0
            for j in range(line_start, i + 1):
                if code[j] == quote_char and (j == 0 or code[j-1] != '\\'):
                    count += 1
            if count % 2 == 1:  # Odd count means we're inside
                return quote_char
            break
        elif code[i] == '\n':
            break
    return None


def classify_selection(code: str, start: int, end: int) -> str:
    """
    Classify what kind of bash expression is selected.

    Returns one of:
        'quoted_string' - "..." or '...'
        'command_sub'   - $(...) or `...`
        'variable'      - $VAR or ${VAR}
        'multi_word'    - multiple unquoted words (needs array)
        'single_word'   - single unquoted word
        'command'       - looks like a full command (starts at line beginning)
        'quoted_content' - content inside quotes (needs special handling)
    """
    selected = code[start:end].strip()

    # Check if we're selecting content inside quotes
    inside_quote = is_inside_quotes(code, start, end)
    if inside_quote:
        return 'quoted_content'

    # Check if it's a quoted string
    if (selected.startswith('"') and selected.endswith('"')) or \
       (selected.startswith("'") and selected.endswith("'")):
        return 'quoted_string'

    # Check if it's a command substitution
    if (selected.startswith('$(') and selected.endswith(')')) or \
       (selected.startswith('`') and selected.endswith('`')):
        return 'command_sub'

    # Check if it's an arithmetic expansion
    if selected.startswith('$((') and selected.endswith('))'):
        return 'arithmetic'

    # Check if it's a variable reference
    if selected.startswith('$'):
        return 'variable'

    # Check if it's a process substitution <() or >()
    if (selected.startswith('<(') or selected.startswith('>(')) and selected.endswith(')'):
        return 'process_sub'

    # Check if it's a brace expansion {a,b,c} or {1..10}
    if selected.startswith('{') and selected.endswith('}') and (',' in selected or '..' in selected):
        return 'brace_expansion'

    # Check if it contains glob characters (should not be quoted)
    if any(c in selected for c in '*?['):
        return 'glob'

    # Check if selection is at line start (likely a command)
    line_start = get_line_start(code, start)
    content_start = line_start
    while content_start < len(code) and code[content_start] in ' \t':
        content_start += 1
    if start == content_start:
        return 'command'

    # Check for multiple words (spaces in unquoted context)
    # Simple heuristic: if there's whitespace not inside quotes, it's multi-word
    in_quote = None
    has_space = False
    for c in selected:
        if c in '"\'':
            if in_quote == c:
                in_quote = None
            elif in_quote is None:
                in_quote = c
        elif c in ' \t' and in_quote is None:
            has_space = True
            break

    return 'multi_word' if has_space else 'single_word'


def extract_variable(code: str, start: int, end: int, var_name: str, replace_all: bool = True) -> Optional[Tuple[str, int]]:
    """
    Extract selected expression into a variable with correct bash semantics.

    Handles:
        - Quoted strings: VAR="value"
        - Command substitution: VAR=$(cmd)
        - Multiple words: VAR=(word1 word2); use "${VAR[@]}"
        - Single words: VAR=word
        - Commands: VAR=$(command); capture output

    Returns: (new_code, new_cursor_pos) or None
    """
    valid, error = is_valid_bash_identifier(var_name)
    if not valid:
        return None

    if start >= end:
        return None

    selected = code[start:end]
    if not selected.strip():
        return None

    tree = parse(code)
    selection_type = classify_selection(code, start, end)

    # Find where to insert the assignment
    node = find_smallest_containing(tree, start, end)
    if node:
        containing = find_containing_command(node)
        if containing:
            insert_pos = get_line_start(code, containing.start_byte)
        else:
            insert_pos = get_line_start(code, start)
    else:
        insert_pos = get_line_start(code, start)

    indent = get_line_indent(code, start)

    # Determine assignment and replacement based on selection type
    if selection_type == 'quoted_content':
        # Content inside quotes - expand selection to include the surrounding quotes
        # Find the opening quote
        quote_start = start - 1
        while quote_start >= 0 and code[quote_start] not in '"\'':
            quote_start -= 1
        quote_char = code[quote_start] if quote_start >= 0 else '"'
        # Find the closing quote
        quote_end = end
        while quote_end < len(code) and code[quote_end] != quote_char:
            quote_end += 1
        if quote_end < len(code):
            quote_end += 1  # Include the closing quote
        # Use the full quoted string
        selected = code[quote_start:quote_end]
        start = quote_start
        end = quote_end
        assignment = f'{indent}{var_name}={selected}\n'
        replacement = f'"${var_name}"'
    elif selection_type == 'quoted_string':
        # Already quoted, use as-is
        assignment = f'{indent}{var_name}={selected}\n'
        replacement = f'"${var_name}"'
    elif selection_type == 'command_sub':
        # Command substitution, use as-is
        assignment = f'{indent}{var_name}={selected}\n'
        replacement = f'"${var_name}"'
    elif selection_type == 'variable':
        # Variable reference - wrap in quotes for safety
        assignment = f'{indent}{var_name}={selected}\n'
        replacement = f'"${var_name}"'
    elif selection_type == 'arithmetic':
        # Arithmetic expansion - use as-is
        assignment = f'{indent}{var_name}={selected}\n'
        replacement = f'"${var_name}"'
    elif selection_type == 'process_sub':
        # Process substitution - can't really extract, just store as-is
        assignment = f'{indent}{var_name}={selected}\n'
        replacement = f'${var_name}'  # No quotes - it's a file path
    elif selection_type == 'brace_expansion':
        # Brace expansion - MUST NOT be quoted, use array
        assignment = f'{indent}{var_name}=({selected})\n'
        replacement = f'"${{{var_name}[@]}}"'
    elif selection_type == 'glob':
        # Glob pattern - MUST NOT be quoted, use array to capture matches
        assignment = f'{indent}{var_name}=({selected})\n'
        replacement = f'"${{{var_name}[@]}}"'
    elif selection_type == 'command':
        # Full command - capture output with $()
        # Don't replace the command itself, just prepend the assignment
        assignment = f'{indent}{var_name}=$({selected})\n'
        replacement = None  # Signal to not do replacement
    elif selection_type == 'multi_word':
        # Multiple words - use array
        assignment = f'{indent}{var_name}=({selected})\n'
        replacement = f'"${{{var_name}[@]}}"'
    else:  # single_word
        # Single word - quote it for safety
        assignment = f'{indent}{var_name}="{selected}"\n'
        replacement = f'"${var_name}"'

    # For now, only replace the original selection (not duplicates for complex cases)
    # Duplicate replacement for multi-word arrays would be complex
    if selection_type == 'multi_word':
        replace_all = False

    # If replacement is None (e.g., command extraction), just prepend assignment
    if replacement is None:
        new_code = assignment + code
        new_cursor = len(indent) + len(var_name)
        return new_code, new_cursor

    # Find duplicates if replacing all
    replacements = [(start, end)]
    if replace_all:
        duplicates = find_duplicate_expressions(tree, code, selected, start)
        replacements.extend(duplicates)

    # Sort in reverse order for replacement
    replacements.sort(reverse=True)

    # Build new code
    new_code = code

    # Replace all occurrences with variable reference
    for s, e in replacements:
        new_code = new_code[:s] + replacement + new_code[e:]

    # Calculate offset adjustment for insertion point
    offset_adjust = 0
    for s, e in sorted(replacements):
        if s < insert_pos:
            old_len = e - s
            new_len = len(replacement)
            offset_adjust += new_len - old_len

    adjusted_insert = insert_pos + offset_adjust

    # Insert assignment
    new_code = new_code[:adjusted_insert] + assignment + new_code[adjusted_insert:]

    # New cursor at end of variable name in assignment
    new_cursor = adjusted_insert + len(indent) + len(var_name)

    return new_code, new_cursor


# =============================================================================
# UI STATE
# =============================================================================

class BashExtractState:
    """State for extract variable UI."""
    def __init__(self):
        self.active = False
        self.name = ""
        self.name_cursor = 0
        self.start = 0
        self.end = 0
        self.error = None
        self.duplicate_count = 0
        self.replace_all = True
        self.original_code = ""
        self.shell_prefix = False  # True if code starts with !

    def start_extract(self, start: int, end: int, duplicate_count: int, original_code: str, shell_prefix: bool = False):
        self.active = True
        self.name = ""
        self.name_cursor = 0
        self.start = start
        self.end = end
        self.error = None
        self.duplicate_count = duplicate_count
        self.replace_all = duplicate_count > 0
        self.original_code = original_code
        self.shell_prefix = shell_prefix

    def reset(self):
        self.active = False
        self.name = ""
        self.name_cursor = 0
        self.start = 0
        self.end = 0
        self.error = None
        self.duplicate_count = 0
        self.replace_all = True
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
        """Toggle replace all mode."""
        if self.duplicate_count > 0:
            self.replace_all = not self.replace_all

    def get_preview(self) -> Optional[Tuple[str, int]]:
        """Get live preview of the extraction."""
        if not self.active or not self.original_code:
            return None
        var_name = self.name.strip()
        if not var_name:
            return None
        valid, _ = is_valid_bash_identifier(var_name)
        if not valid:
            return None
        # Handle shell prefix (!)
        if self.shell_prefix:
            bash_code = self.original_code[1:]
            adj_start = max(0, self.start - 1)
            adj_end = max(0, self.end - 1)
            result = extract_variable(bash_code, adj_start, adj_end, var_name, self.replace_all)
            if result:
                # Prepend ! back and adjust cursor
                return ('!' + result[0], result[1] + 1)
            return None
        return extract_variable(self.original_code, self.start, self.end, var_name, self.replace_all)


state = BashExtractState()


def handle_start(code: str, start: int, end: int, shell_prefix: bool = False) -> Optional[Tuple[int, int]]:
    """
    Start extract mode.

    Returns: (expanded_start, expanded_end) if started, or None
    """
    # Handle shell prefix (!)
    if shell_prefix:
        bash_code = code[1:] if code.startswith('!') else code
        adj_start = max(0, start - 1)
        adj_end = max(0, end - 1)
    else:
        bash_code = code
        adj_start = start
        adj_end = end

    can_extract, error, info = check_extract(bash_code, adj_start, adj_end)

    if not can_extract:
        state.active = True
        state.error = error
        return None

    # Try to expand to a full AST node
    tree = parse(bash_code)
    node = find_smallest_extractable(tree, adj_start, adj_end)
    if node:
        expanded_start = node.start_byte
        expanded_end = node.end_byte
    else:
        expanded_start = adj_start
        expanded_end = adj_end

    # Store original positions with ! offset for proper restore
    if shell_prefix:
        state.start_extract(
            start,  # Original start position (with !)
            expanded_end + 1 if node else end,  # Adjust back for !
            info['duplicate_count'],
            code,  # Original code with !
            shell_prefix
        )
        return (expanded_start + 1, expanded_end + 1)  # Adjust for caller
    else:
        state.start_extract(
            expanded_start,
            expanded_end,
            info['duplicate_count'],
            code,
            shell_prefix
        )
        return (expanded_start, expanded_end)


def handle_confirm(code: str) -> Optional[Tuple[str, int]]:
    """Handle Enter. Perform the extraction."""
    if not state.active:
        return None

    var_name = state.name.strip()
    valid, error = is_valid_bash_identifier(var_name)

    if not valid:
        state.error = error
        return None

    result = extract_variable(code, state.start, state.end, var_name, state.replace_all)
    state.reset()
    return result


def handle_cancel():
    """Handle Escape/Ctrl+C."""
    state.reset()
