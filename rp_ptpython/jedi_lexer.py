"""
Lexer wrapper that adds Jedi-based semantic highlighting.

Wraps the base Pygments lexer and post-processes tokens to highlight:
- Callables (functions, classes) - same as builtin functions (Token.Name.Builtin)
- Modules - yellow/orange (Token.Name.Constant)
- Unused variables - orange (Token.Name.Exception) - TODO
"""
from __future__ import unicode_literals
from rp.prompt_toolkit.layout.lexers import Lexer
from rp.prompt_toolkit.token import Token
from rp.rp_ptpython.async_jedi_highlighter import AsyncJediHighlighter

__all__ = ['JediLexer']


class JediLexer(Lexer):
    """
    Lexer wrapper that adds semantic highlighting using Jedi type inference.

    Wraps a base lexer (usually LazyPygmentsLexer) and post-processes tokens to add:
    - Callables: highlighted same as builtin functions (Token.Callable)
    - Modules: highlighted as constants (Token.Module - usually yellow/orange)
    - Parameters: highlighted with warm colors (Token.Parameter - brownish/golden)
    - Unused variables: highlighted in orange (Token.Name.Exception) - TODO

    Uses AsyncJediHighlighter to run Jedi in background thread (max 1/sec) and
    difflib to translate cached positions for instant updates.
    """

    def __init__(self, base_lexer, get_globals, get_locals, get_enabled=None, get_gray_unreachable=None,
                 get_treesitter_enabled=None, get_jedi_enabled=None):
        """
        Initialize Jedi lexer.

        Args:
            base_lexer: Base lexer to wrap (e.g., LazyPygmentsLexer)
            get_globals: Function that returns global namespace dict
            get_locals: Function that returns local namespace dict
            get_enabled: Function that returns whether ANY semantic highlighting is enabled
            get_gray_unreachable: Function that returns whether to gray out unreachable code
            get_treesitter_enabled: Function that returns whether tree-sitter highlighting is enabled
            get_jedi_enabled: Function that returns whether Jedi highlighting is enabled
        """
        self.base_lexer = base_lexer
        self.get_globals = get_globals
        self.get_locals = get_locals
        self.get_enabled = get_enabled or (lambda: True)
        self.get_gray_unreachable = get_gray_unreachable or (lambda: True)
        self.get_treesitter_enabled = get_treesitter_enabled or (lambda: True)
        self.get_jedi_enabled = get_jedi_enabled or (lambda: True)

        # Async Jedi highlighter (shared across all lex_document calls)
        # Redraw callback will be set in lex_document when cli is available
        self.async_highlighter = AsyncJediHighlighter()

    def lex_document(self, cli, document):
        """
        Lex document with semantic highlighting.

        Returns a callable that takes a line number and returns tokens.
        """
        # Set redraw callback (triggers UI refresh when Jedi results arrive)
        if not self.async_highlighter.redraw_callback:
            # Use cli.request_redraw() to trigger UI update
            self.async_highlighter.redraw_callback = lambda: cli.request_redraw()

        # Get base tokens
        base_get_line = self.base_lexer.lex_document(cli, document)

        # NOTE: SyntaxErrorProcessor triggers refresh_analysis

        def get_line_with_highlights(lineno):
            """Get tokens for line with semantic highlighting.

            Fetches FRESH results each time so when background Jedi completes
            and triggers redraw, we use the new results.
            """
            base_tokens = base_get_line(lineno)

            # Check if semantic highlighting is enabled
            if not self.get_enabled():
                return base_tokens

            # Fetch CURRENT results from async_highlighter (not captured!)
            with self.async_highlighter.lock:
                results = self.async_highlighter.cached_results
                # Handle multiple tuple formats
                if len(results) == 9:
                    callable_positions, module_positions, unused_var_positions, parameter_positions, unreachable_positions, kwarg_positions, global_positions, local_positions, nonlocal_positions = results
                elif len(results) == 6:
                    callable_positions, module_positions, unused_var_positions, parameter_positions, unreachable_positions, kwarg_positions = results
                    global_positions = set()
                    local_positions = set()
                    nonlocal_positions = set()
                elif len(results) == 5:
                    callable_positions, module_positions, unused_var_positions, parameter_positions, unreachable_positions = results
                    kwarg_positions = set()
                    global_positions = set()
                    local_positions = set()
                    nonlocal_positions = set()
                else:
                    callable_positions, module_positions, unused_var_positions, parameter_positions = results
                    unreachable_positions = set()
                    kwarg_positions = set()
                    global_positions = set()
                    local_positions = set()
                    nonlocal_positions = set()

            if not (callable_positions or module_positions or unused_var_positions or parameter_positions or unreachable_positions or kwarg_positions or global_positions or local_positions or nonlocal_positions):
                return base_tokens

            # Post-process tokens on this line
            result_tokens = []
            column = 0

            for token_type, text in base_tokens:
                # Check if this token starts at a semantic position
                # (line numbers are 1-indexed in Jedi, 0-indexed in prompt_toolkit)
                match_key = (lineno + 1, column, len(text))

                is_callable = match_key in callable_positions
                is_module = match_key in module_positions
                is_unused = match_key in unused_var_positions
                is_parameter = match_key in parameter_positions
                is_unreachable = match_key in unreachable_positions
                is_kwarg = match_key in kwarg_positions
                is_global = match_key in global_positions
                is_local = match_key in local_positions
                is_nonlocal = match_key in nonlocal_positions

                # Only highlight names (not keywords, not in definitions, NOT in strings)
                # Include Function and Function.Magic for dunder methods like __init__
                is_name_token = token_type in (Token.Name, Token.Name.Builtin, Token.Name.Other,
                                               Token.Name.Namespace, Token.Name.Function, Token.Name.Function.Magic)
                # Don't apply semantic highlighting inside strings (including injected strings)
                is_string_token = token_type in Token.String or token_type in Token.Literal.String

                if is_unreachable and self.get_gray_unreachable():
                    # Unreachable code has highest priority - dim everything (even strings/comments)
                    result_tokens.append((Token.Unreachable, text))
                elif is_string_token:
                    # Never apply semantic highlighting inside strings
                    result_tokens.append((token_type, text))
                elif is_kwarg and is_name_token:
                    # Highlight keyword arguments in function calls
                    result_tokens.append((Token.KwargName, text))
                elif is_parameter and is_name_token:
                    # Check if parameter is unused - dim it if so
                    if is_unused:
                        result_tokens.append((Token.Parameter.Unused, text))
                    else:
                        result_tokens.append((Token.Parameter, text))
                elif is_unused and is_name_token:
                    # Highlight other unused variables (not parameters)
                    result_tokens.append((Token.Name.Exception, text))
                elif is_callable and is_name_token:
                    # Highlight callables same as builtin functions
                    result_tokens.append((Token.Callable, text))
                elif is_module and is_name_token:
                    # Highlight modules in yellow/orange (Token.Name.Constant often yellow)
                    result_tokens.append((Token.Module, text))
                elif is_global and is_name_token:
                    # Highlight global variables
                    result_tokens.append((Token.Global, text))
                elif is_local and is_name_token:
                    # Highlight local variables
                    result_tokens.append((Token.Local, text))
                elif is_nonlocal and is_name_token:
                    # Highlight nonlocal variables
                    result_tokens.append((Token.Nonlocal, text))
                else:
                    result_tokens.append((token_type, text))

                column += len(text)

            return result_tokens

        return get_line_with_highlights
