"""
Semantic syntax highlighting using Jedi type inference.

Highlights callables (functions, classes) in bold cyan based on actual runtime types,
not just regex patterns.
"""
from __future__ import unicode_literals
from rp.prompt_toolkit.token import Token

__all__ = ['get_jedi_tokens']


def get_jedi_tokens(code, globals_dict, locals_dict):
    """
    Get semantic tokens for code using Jedi type inference.

    Args:
        code: Python code to highlight
        globals_dict: Global namespace for type inference
        locals_dict: Local namespace for type inference

    Returns:
        List of (Token, text) tuples for highlighting

    For now, just highlights callables in bold cyan.
    """
    import jedi

    if not code.strip():
        return []

    try:
        # Parse code with Jedi
        script = jedi.Script(code, environment=jedi.get_default_environment())

        # Get all names (references)
        names = script.get_names(all_scopes=True, references=True)

        # Build set of (line, column) positions for callables
        callable_positions = set()
        for name in names:
            try:
                inferred = name.infer()
                if inferred and inferred[0].type in ('function', 'class'):
                    # Store position (line, column)
                    callable_positions.add((name.line, name.column))
            except:
                pass

        return callable_positions

    except Exception:
        return set()


def highlight_callables_in_tokens(tokens, code, globals_dict, locals_dict):
    """
    Post-process Pygments tokens to highlight callables in bold cyan.

    Args:
        tokens: List of (Token, text) from Pygments lexer
        code: Original code string
        globals_dict: Global namespace
        locals_dict: Local namespace

    Returns:
        Modified list of (Token, text) with callables highlighted
    """
    callable_positions = get_jedi_tokens(code, globals_dict, locals_dict)

    if not callable_positions:
        return tokens

    # Build line->column->text map from tokens
    line = 1
    column = 0
    result_tokens = []

    for token_type, text in tokens:
        # Check if this token starts at a callable position
        if '\n' not in text:
            # Single line token
            is_callable = (line, column) in callable_positions
            if is_callable:
                # Highlight as bold cyan
                result_tokens.append((Token.Callable, text))
            else:
                result_tokens.append((token_type, text))
            column += len(text)
        else:
            # Multi-line token - split it
            parts = text.split('\n')
            for i, part in enumerate(parts):
                if i > 0:
                    result_tokens.append((token_type, '\n'))
                    line += 1
                    column = 0
                if part:
                    is_callable = (line, column) in callable_positions
                    if is_callable:
                        result_tokens.append((Token.Callable, part))
                    else:
                        result_tokens.append((token_type, part))
                    column += len(part)

    return result_tokens
