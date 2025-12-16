"""
Backslash Commands Module

Provides a command mode for applying text transformations to selections.
When text is selected and \ is pressed, enters command mode where you can
type a command name and press Enter to apply it to the selection.

Usage:
    1. Select some text
    2. Press \
    3. Type command name (e.g., 'rl' for reverse_lines)
    4. Press Enter to apply, Escape to cancel

Example:
    Select:     line3        After \rl:    line1
                line2                      line2
                line1                      line3
"""
from typing import Callable, Dict, Tuple, Optional


# =============================================================================
# COMMAND REGISTRY
# =============================================================================

# Commands are {shortcut: (full_name, description, transform_fn)}
# transform_fn takes text and returns transformed text
COMMANDS: Dict[str, Tuple[str, str, Callable[[str], str]]] = {}


def register(shortcut: str, name: str, description: str):
    """Decorator to register a backslash command."""
    def decorator(fn: Callable[[str], str]):
        COMMANDS[shortcut] = (name, description, fn)
        return fn
    return decorator


# =============================================================================
# BUILT-IN COMMANDS
# =============================================================================

@register('rl', 'reverse_lines', 'Reverse line order')
def reverse_lines(text: str) -> str:
    #   a\n b\n c  ->  c\n b\n a
    return '\n'.join(reversed(text.split('\n')))


@register('sl', 'sort_lines', 'Sort lines alphabetically')
def sort_lines(text: str) -> str:
    #   c\n a\n b  ->  a\n b\n c
    return '\n'.join(sorted(text.split('\n')))


@register('slu', 'sort_lines_unique', 'Sort lines and remove duplicates')
def sort_lines_unique(text: str) -> str:
    #   b\n a\n b  ->  a\n b
    return '\n'.join(sorted(set(text.split('\n'))))


@register('u', 'unique', 'Remove duplicate lines (preserve order)')
def unique_lines(text: str) -> str:
    #   a\n b\n a  ->  a\n b
    seen = set()
    result = []
    for line in text.split('\n'):
        if line not in seen:
            seen.add(line)
            result.append(line)
    return '\n'.join(result)


@register('uc', 'upper', 'Convert to UPPERCASE')
def upper(text: str) -> str:
    return text.upper()


@register('lc', 'lower', 'Convert to lowercase')
def lower(text: str) -> str:
    return text.lower()


@register('tc', 'title', 'Convert To Title Case')
def title(text: str) -> str:
    return text.title()


@register('stp', 'strip', 'Strip leading/trailing whitespace')
def strip(text: str) -> str:
    return text.strip()


@register('stpl', 'strip_lines', 'Strip each line')
def strip_lines(text: str) -> str:
    return '\n'.join(line.strip() for line in text.split('\n'))


@register('ind', 'indent', 'Indent by 4 spaces')
def indent(text: str) -> str:
    return '\n'.join('    ' + line for line in text.split('\n'))


@register('ded', 'dedent', 'Remove one level of indentation')
def dedent(text: str) -> str:
    lines = text.split('\n')
    result = []
    for line in lines:
        if line.startswith('    '):
            result.append(line[4:])
        elif line.startswith('\t'):
            result.append(line[1:])
        else:
            result.append(line)
    return '\n'.join(result)


@register('rev', 'reverse', 'Reverse text')
def reverse_text(text: str) -> str:
    #   abc  ->  cba
    return text[::-1]


@register('sq', 'squeeze', 'Squeeze multiple blank lines to one')
def squeeze(text: str) -> str:
    import re
    return re.sub(r'\n{3,}', '\n\n', text)


@register('nb', 'no_blanks', 'Remove blank lines')
def no_blanks(text: str) -> str:
    return '\n'.join(line for line in text.split('\n') if line.strip())


@register('num', 'number', 'Add line numbers')
def number_lines(text: str) -> str:
    #   a\n b  ->  1: a\n 2: b
    lines = text.split('\n')
    width = len(str(len(lines)))
    return '\n'.join(f'{i+1:>{width}}: {line}' for i, line in enumerate(lines))


@register('unnum', 'unnumber', 'Remove line numbers')
def unnumber_lines(text: str) -> str:
    #   1: a\n 2: b  ->  a\n b
    import re
    return '\n'.join(re.sub(r'^\s*\d+:\s?', '', line) for line in text.split('\n'))


@register('j', 'join', 'Join lines with space')
def join_lines(text: str) -> str:
    #   a\n b\n c  ->  a b c
    return ' '.join(text.split('\n'))


@register('jc', 'join_comma', 'Join lines with comma')
def join_comma(text: str) -> str:
    #   a\n b\n c  ->  a, b, c
    return ', '.join(line.strip() for line in text.split('\n') if line.strip())


@register('sp', 'split', 'Split on spaces to lines')
def split_spaces(text: str) -> str:
    #   a b c  ->  a\n b\n c
    return '\n'.join(text.split())


@register('spc', 'split_comma', 'Split on commas to lines')
def split_comma(text: str) -> str:
    #   a, b, c  ->  a\n b\n c
    return '\n'.join(part.strip() for part in text.split(','))


@register('q', 'quote', 'Quote each line')
def quote_lines(text: str) -> str:
    #   a\n b  ->  "a"\n "b"
    return '\n'.join(f'"{line}"' for line in text.split('\n'))


@register('uq', 'unquote', 'Remove quotes from each line')
def unquote_lines(text: str) -> str:
    #   "a"\n 'b'  ->  a\n b
    lines = []
    for line in text.split('\n'):
        s = line.strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            lines.append(s[1:-1])
        else:
            lines.append(line)
    return '\n'.join(lines)


@register('c', 'comment', 'Comment lines with #')
def comment_lines(text: str) -> str:
    #   a\n b  ->  # a\n # b
    return '\n'.join('# ' + line for line in text.split('\n'))


@register('unc', 'uncomment', 'Remove # comments')
def uncomment_lines(text: str) -> str:
    #   # a\n # b  ->  a\n b
    import re
    return '\n'.join(re.sub(r'^(\s*)#\s?', r'\1', line) for line in text.split('\n'))


@register('len', 'length', 'Show length of text')
def show_length(text: str) -> str:
    lines = text.split('\n')
    return f"[{len(text)} chars, {len(lines)} lines]"


# =============================================================================
# COMMANDS USING RP MODULE
# =============================================================================

@register('min', 'minify', 'Minify Python code')
def minify(text: str) -> str:
    import rp
    return rp.minify_python_code(text)


@register('bla', 'black', 'Format with black')
def black_format(text: str) -> str:
    import rp
    return rp.autoformat_code(text)


@register('sc', 'strip_comments', 'Strip Python comments')
def strip_comments(text: str) -> str:
    from rp import strip_python_comments
    return strip_python_comments(text)


@register('sdo', 'strip_docstrings', 'Strip Python docstrings')
def strip_docstrings(text: str) -> str:
    from rp import strip_python_docstrings
    return strip_python_docstrings(text)


@register('sim', 'sort_imports', 'Sort imports with isort')
def sort_imports(text: str) -> str:
    import rp
    return rp.isort(text)


@register('al', 'align', 'Align lines on = or :')
def align_lines(text: str) -> str:
    import rp
    return rp.align_lines(text)


@register('und', 'unindent', 'Remove common leading indentation')
def unindent(text: str) -> str:
    import rp
    return rp.unindent(text)


@register('tts', 'tabs_to_spaces', 'Convert tabs to 4 spaces')
def tabs_to_spaces(text: str) -> str:
    return text.replace('\t', '    ')


@register('cim', 'clean_imports', 'Clean/organize imports')
def clean_imports(text: str) -> str:
    import rp
    return rp.clean_imports(text)


@register('rms', 'remove_star', 'Expand star imports')
def remove_star(text: str) -> str:
    import rp
    return rp.remove_star_imports(text)


@register('rmfs', 'remove_fstrings', 'Convert f-strings to .format()')
def remove_fstrings(text: str) -> str:
    import rp
    return rp.remove_fstrings(text)


@register('sw', 'strip_whitespace', 'Strip trailing whitespace from lines')
def strip_whitespace(text: str) -> str:
    return '\n'.join(line.rstrip() for line in text.split('\n'))


@register('sbl', 'strip_blank_lines', 'Remove blank lines')
def strip_blank_lines(text: str) -> str:
    from rp import strip_blank_lines
    return strip_blank_lines(text)


@register('mla', 'multi_line_args', 'Split function args to multiple lines')
def multi_line_args(text: str) -> str:
    import rp
    return rp.multi_line_args(text)


@register('fi', 'from_import_swap', 'Swap import/from import style')
def from_import_swap(text: str) -> str:
    import rp
    return rp.import_from_swap(text)


@register('ya', 'yapf', 'Format with yapf')
def yapf_format(text: str) -> str:
    import rp
    return rp.yapf_format(text)


@register('23p', 'python2to3', 'Convert Python 2 to 3')
def python_2_to_3(text: str) -> str:
    import rp
    return rp.python_2_to_3(text)


@register('rcl', 'reverse_columns', 'Reverse columns in each line')
def reverse_columns(text: str) -> str:
    import rp
    return rp.reverse_columns(text)


@register('spl', 'splitlines', 'Split into lines (normalize newlines)')
def splitlines(text: str) -> str:
    return '\n'.join(text.splitlines())


@register('lj', 'line_join', 'Join lines with backslash continuation')
def line_join(text: str) -> str:
    lines = text.split('\n')
    return ' \\\n'.join(lines)


@register('irp', 'inline_rp', 'Inline rp.* calls')
def inline_rp(text: str) -> str:
    import rp
    return rp.inline_rp(text)


@register('qrp', 'qualify_rp', 'Qualify rp.* calls')
def qualify_rp(text: str) -> str:
    import rp
    return rp.qualify_rp(text)


@register('rpr', 'repr', 'Wrap in repr()')
def wrap_repr(text: str) -> str:
    return repr(text)


@register('tbp', 'toggle_parens', 'Toggle big parenthesis style')
def toggle_big_parens(text: str) -> str:
    import rp
    return rp.toggle_big_parenthesis(text)


@register('en', 'enumerate', 'Wrap iterable in enumerate()')
def wrap_enumerate(text: str) -> str:
    return f'enumerate({text.strip()})'


@register('ac', 'align_char', 'Align on specific character')
def align_char(text: str) -> str:
    import rp
    return rp.align_char(text)


# Delete empty lines variants
@register('d0l', 'del_empty_0', 'Delete lines with 0+ spaces only')
def del_empty_0(text: str) -> str:
    return '\n'.join(l for l in text.split('\n') if l.strip())


@register('d1l', 'del_empty_1', 'Delete lines with <=1 char')
def del_empty_1(text: str) -> str:
    return '\n'.join(l for l in text.split('\n') if len(l.strip()) > 1)


@register('d2l', 'del_empty_2', 'Delete lines with <=2 chars')
def del_empty_2(text: str) -> str:
    return '\n'.join(l for l in text.split('\n') if len(l.strip()) > 2)


# =============================================================================
# WRAP IN CONTROL STRUCTURES
# =============================================================================

@register('fo', 'for', 'Wrap in for loop')
def wrap_for(text: str) -> str:
    #   x        ->   for i in x:
    #                     pass
    import rp
    indent = rp.get_indent(text) if '\n' in text else ''
    return f'{indent}for i in {text.strip()}:\n{indent}    pass'


@register('de', 'def', 'Wrap in function def')
def wrap_def(text: str) -> str:
    #   code     ->   def func():
    #                     code
    import rp
    indented = rp.indent(text, '    ')
    return f'def func():\n{indented}'


@register('wh', 'while', 'Wrap in while loop')
def wrap_while(text: str) -> str:
    #   cond     ->   while cond:
    #                     pass
    import rp
    indent = rp.get_indent(text) if '\n' in text else ''
    return f'{indent}while {text.strip()}:\n{indent}    pass'


@register('wi', 'with', 'Wrap in with statement')
def wrap_with(text: str) -> str:
    #   expr     ->   with expr:
    #                     pass
    import rp
    indent = rp.get_indent(text) if '\n' in text else ''
    return f'{indent}with {text.strip()}:\n{indent}    pass'


@register('if', 'if', 'Wrap in if statement')
def wrap_if(text: str) -> str:
    #   cond     ->   if cond:
    #                     pass
    import rp
    indent = rp.get_indent(text) if '\n' in text else ''
    return f'{indent}if {text.strip()}:\n{indent}    pass'


@register('try', 'try', 'Wrap in try/except')
def wrap_try(text: str) -> str:
    #   code     ->   try:
    #                     code
    #                 except Exception as e:
    #                     raise
    import rp
    indented = rp.indent(text, '    ')
    return f'try:\n{indented}\nexcept Exception as e:\n    raise'


@register('cl', 'class', 'Wrap in class def')
def wrap_class(text: str) -> str:
    #   code     ->   class MyClass:
    #                     code
    import rp
    indented = rp.indent(text, '    ')
    return f'class MyClass:\n{indented}'


@register('lam', 'lambda', 'Wrap in lambda')
def wrap_lambda(text: str) -> str:
    #   expr     ->   lambda: expr
    return f'lambda: {text.strip()}'


@register('ret', 'return', 'Wrap in return')
def wrap_return(text: str) -> str:
    #   expr     ->   return expr
    return f'return {text.strip()}'


@register('pr', 'print', 'Wrap in print()')
def wrap_print(text: str) -> str:
    #   expr     ->   print(expr)
    return f'print({text.strip()})'


@register('li', 'list', 'Wrap in list()')
def wrap_list(text: str) -> str:
    return f'list({text.strip()})'


@register('tu', 'tuple', 'Wrap in tuple()')
def wrap_tuple(text: str) -> str:
    return f'tuple({text.strip()})'


@register('se', 'set', 'Wrap in set()')
def wrap_set(text: str) -> str:
    return f'set({text.strip()})'


@register('di', 'dict', 'Wrap in dict()')
def wrap_dict(text: str) -> str:
    return f'dict({text.strip()})'


@register('so', 'sorted', 'Wrap in sorted()')
def wrap_sorted(text: str) -> str:
    return f'sorted({text.strip()})'


@register('le', 'len', 'Wrap in len()')
def wrap_len(text: str) -> str:
    return f'len({text.strip()})'


@register('str', 'str', 'Wrap in str()')
def wrap_str(text: str) -> str:
    return f'str({text.strip()})'


@register('int', 'int', 'Wrap in int()')
def wrap_int(text: str) -> str:
    return f'int({text.strip()})'


@register('not', 'not', 'Wrap in not')
def wrap_not(text: str) -> str:
    return f'not {text.strip()}'


@register('as', 'assert', 'Wrap in assert')
def wrap_assert(text: str) -> str:
    return f'assert {text.strip()}'


# =============================================================================
# STATE CLASS
# =============================================================================

class BackslashCommandState:
    """State for backslash command input mode."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.active = False
        self.command = ""           # Command being typed
        self.cursor = 0             # Cursor position in command
        self.error = None
        self.original_code = ""     # Full buffer before
        self.selection_start = 0
        self.selection_end = 0
        self.selected_text = ""

    def start(self, original_code: str, selection_start: int, selection_end: int):
        """Start command mode with selection."""
        self.active = True
        self.command = ""
        self.cursor = 0
        self.error = None
        self.original_code = original_code
        self.selection_start = selection_start
        self.selection_end = selection_end
        self.selected_text = original_code[selection_start:selection_end]

    def add_char(self, char: str):
        self.command = self.command[:self.cursor] + char + self.command[self.cursor:]
        self.cursor += 1

    def delete_char(self):
        if self.cursor > 0:
            self.command = self.command[:self.cursor-1] + self.command[self.cursor:]
            self.cursor -= 1

    def cursor_left(self):
        if self.cursor > 0:
            self.cursor -= 1

    def cursor_right(self):
        if self.cursor < len(self.command):
            self.cursor += 1

    def delete_forward(self):
        if self.cursor < len(self.command):
            self.command = self.command[:self.cursor] + self.command[self.cursor+1:]

    def get_matching_commands(self) -> list:
        """Get commands that match current input."""
        if not self.command:
            return list(COMMANDS.keys())
        return [k for k in COMMANDS if k.startswith(self.command)]

    def get_preview(self) -> Optional[Tuple[str, int]]:
        """Get preview of transformation. Returns (new_full_code, cursor_pos) or None."""
        if not self.active or not self.command:
            return None

        if self.command not in COMMANDS:
            return None

        _, _, transform_fn = COMMANDS[self.command]
        try:
            transformed = transform_fn(self.selected_text)
            new_code = (self.original_code[:self.selection_start] +
                       transformed +
                       self.original_code[self.selection_end:])
            new_cursor = self.selection_start + len(transformed)
            return (new_code, new_cursor)
        except Exception:
            return None

    def execute(self) -> Optional[Tuple[str, int]]:
        """Execute the command. Returns (new_code, cursor_pos) or None."""
        return self.get_preview()

    def get_status(self) -> str:
        """Get status line text."""
        if self.error:
            return f"\\{self.command}: {self.error}"

        matches = self.get_matching_commands()
        if not self.command:
            hint = "Type command (Tab for list)"
        elif len(matches) == 0:
            hint = "No matching command"
        elif len(matches) == 1 and matches[0] == self.command:
            name, desc, _ = COMMANDS[self.command]
            hint = f"{name}: {desc}"
        else:
            hint = ', '.join(matches[:5])
            if len(matches) > 5:
                hint += f'... (+{len(matches)-5})'

        # Show cursor in command
        cmd_display = self.command[:self.cursor] + '|' + self.command[self.cursor:]
        return f"\\{cmd_display}  [{hint}]"


# Global state instance
state = BackslashCommandState()


def get_all_commands() -> str:
    """Return formatted list of all commands for help."""
    lines = ["Backslash Commands (select text, press \\, type command, Enter):"]
    for shortcut in sorted(COMMANDS.keys()):
        name, desc, _ = COMMANDS[shortcut]
        lines.append(f"  \\{shortcut:<6} {name:<20} {desc}")
    return '\n'.join(lines)
