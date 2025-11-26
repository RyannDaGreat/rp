"""
Lexer interface and implementation.
Used for syntax highlighting.
"""
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from six.moves import range

from rp.prompt_toolkit.token import Token
from rp.prompt_toolkit.filters import to_cli_filter
from .utils import split_lines

import re
import six

# <CLAUDE CODE START: Lazy imports for multi-language highlighting - imports deferred until needed>
# Lexer imports moved inside LazyLexer classes to avoid slow startup
# <CLAUDE CODE END: Lazy imports for multi-language highlighting>

__all__ = (
    'Lexer',
    'SimpleLexer',
    'PygmentsLexer',
    'LazyPygmentsLexer',
    'SyntaxSync',
    'SyncFromStart',
    'RegexSync',
)


class Lexer(with_metaclass(ABCMeta, object)):
    """
    Base class for all lexers.
    """
    @abstractmethod
    def lex_document(self, cli, document):
        """
        Takes a :class:`~prompt_toolkit.document.Document` and returns a
        callable that takes a line number and returns the tokens for that line.
        """


class SimpleLexer(Lexer):
    """
    Lexer that doesn't do any tokenizing and returns the whole input as one token.

    :param token: The `Token` for this lexer.
    """
    # `default_token` parameter is deprecated!
    def __init__(self, token=Token, default_token=None):
        self.token = token

        if default_token is not None:
            self.token = default_token

    def lex_document(self, cli, document):
        lines = document.lines

        def get_line(lineno):
            " Return the tokens for the given line. "
            try:
                return [(self.token, lines[lineno])]
            except IndexError:
                return []
        return get_line


class SyntaxSync(with_metaclass(ABCMeta, object)):
    """
    Syntax synchroniser. This is a tool that finds a start position for the
    lexer. This is especially important when editing big documents; we don't
    want to start the highlighting by running the lexer from the beginning of
    the file. That is very slow when editing.
    """
    @abstractmethod
    def get_sync_start_position(self, document, lineno):
        """
        Return the position from where we can start lexing as a (row, column)
        tuple.

        :param document: `Document` instance that contains all the lines.
        :param lineno: The line that we want to highlight. (We need to return
            this line, or an earlier position.)
        """

class SyncFromStart(SyntaxSync):
    """
    Always start the syntax highlighting from the beginning.
    """
    def get_sync_start_position(self, document, lineno):
        return 0, 0


class RegexSync(SyntaxSync):
    """
    Synchronize by starting at a line that matches the given regex pattern.
    """
    # Never go more than this amount of lines backwards for synchronisation.
    # That would be too CPU intensive.
    MAX_BACKWARDS = 500

    # Start lexing at the start, if we are in the first 'n' lines and no
    # synchronisation position was found.
    FROM_START_IF_NO_SYNC_POS_FOUND = 100

    def __init__(self, pattern):
        assert isinstance(pattern, six.text_type)
        self._compiled_pattern = re.compile(pattern)

    def get_sync_start_position(self, document, lineno):
        " Scan backwards, and find a possible position to start. "
        pattern = self._compiled_pattern
        lines = document.lines

        # Scan upwards, until we find a point where we can start the syntax
        # synchronisation.
        for i in range(lineno, max(-1, lineno - self.MAX_BACKWARDS), -1):
            match = pattern.match(lines[i])
            if match:
                return i, match.start()

        # No synchronisation point found. If we aren't that far from the
        # beginning, start at the very beginning, otherwise, just try to start
        # at the current line.
        if lineno < self.FROM_START_IF_NO_SYNC_POS_FOUND:
            return 0, 0
        else:
            return lineno, 0

    @classmethod
    def from_pygments_lexer_cls(cls, lexer_cls):
        """
        Create a :class:`.RegexSync` instance for this Pygments lexer class.
        """
        patterns = {
            # For Python, start highlighting at any class/def block.
            'Python':   r'^\s*(class|def)\s+',
            'Python 3': r'^\s*(class|def)\s+',

            # For HTML, start at any open/close tag definition.
            'HTML': r'<[/a-zA-Z]',

            # For javascript, start at a function.
            'JavaScript': r'\bfunction\b'

            # TODO: Add definitions for other languages.
            #       By default, we start at every possible line.
        }
        p = patterns.get(lexer_cls.name, '^')
        return cls(p)


def longest_common_prefix(a,b):
    #Written by Ryan Burgert, 2020. Written for efficiency's sake.
    #Works for strings, lists and tuples (and possibly other datatypes, but not numpy arrays)
    #This implementation is two orders of magnitude faster than anything I could find on the web/stack overflow/etc, especially for strings
    #It has complexity O(len(output of this function)), and a very good time constant (because it doesn't directly iterate through every element in a python loop)
    #On my computer, this function was able to compare two strings of length 1,000,000 in 0.00454 second. Here's the test I used: string='a'*10**7;tic();longest_common_prefix(string,string);ptoc() [[[tic() starts a timer, ptoc() prints out the elapsed time]]]
    #
    #EXAMPLES:
    #   longest_common_prefix('abcderty','abcdefoaisjd')                --> abcde
    #   longest_common_prefix('abcderty','abcsdefoa')                   --> abc
    #   longest_common_prefix('abcderty','asbcsdefoa')                  --> a
    #   longest_common_prefix('abcderty','aasbcsdefoa')                 --> a
    #   longest_common_prefix('aaaabdcderty','aasbcsdefoa')             --> aa
    #   longest_common_prefix(list('aaaabdcderty'),list('aasbcsdefoa')) --> ['a', 'a']
    
    len_a=len(a)
    len_b=len(b)
    out_max=min(len_a,len_b)
    s=0#Start index
    i=1#Length of proposed additional match
    while s+i<out_max and a[s:s+i]==b[s:s+i]:
        s+=i
        i*=2
    while i:
        if a[s:s+i]==b[s:s+i]:
            s+=i
        i//=2
    assert a[:s]==b[:s]
    return a[:s]



class LazyLexer:
    """
    Lazy wrapper for Pygments lexers to avoid slow initialization and imports.
    This class was Lazy lexers written by Claude, Aug 5 2025. Resulted in massive pterm boot speed boost. Pygments initializations were taking the majority of the time.
    """
    def __init__(self, lexer_module_path, lexer_class_name, *args, **kwargs):
        self.lexer_module_path = lexer_module_path
        self.lexer_class_name = lexer_class_name
        self.args = args
        self.kwargs = kwargs
        self._lexer = None
        self._lexer_class = None
    
    def _get_lexer_class(self):
        if self._lexer_class is None:
            import importlib
            module = importlib.import_module(self.lexer_module_path)
            self._lexer_class = getattr(module, self.lexer_class_name)
        return self._lexer_class
    
    def _get_lexer(self):
        if self._lexer is None:
            lexer_class = self._get_lexer_class()
            self._lexer = lexer_class(*self.args, **self.kwargs)
        return self._lexer
    
    def get_tokens_unprocessed(self, text):
        return self._get_lexer().get_tokens_unprocessed(text)
    
    def __getattr__(self, name):
        return getattr(self._get_lexer(), name)


class LazyBashLexer(LazyLexer):
    """
    Special lazy wrapper for BashLexer that adds system commands on initialization.
    This class was Lazy lexers written by Claude, Aug 5 2025. Resulted in massive pterm boot speed boost. Pygments initializations were taking the majority of the time.
    """
    _system_commands_added = False  # Class variable to track if we've already modified BashLexer globally
    
    def _get_lexer(self):
        if self._lexer is None:
            # Add system commands to global BashLexer class if not already done
            if not LazyBashLexer._system_commands_added:
                self._add_system_commands_to_pterm_bash_highlighter()
                LazyBashLexer._system_commands_added = True
            
            # Now initialize the lexer (which will inherit the modified tokens)
            lexer_class = self._get_lexer_class()
            self._lexer = lexer_class(*self.args, **self.kwargs)
        return self._lexer
    
    def _add_system_commands_to_pterm_bash_highlighter(self):
        """
        This function lets us syntax-highlight any system commands in the !<shell stuff> in pterm seen upon boot
        It can't update them over time right now, it's a one-time thing
        """
        import pygments.lexers.shell as shell
        import re
        import rp
        Name = shell.Name
        commands = rp.get_system_commands(use_cache=True) + ['!']
        shell.BashLexer.tokens['basic'] += [(r'(^|!|\b)(' + '|'.join(re.escape(x) for x in commands) + r')(?=[\s)\`]|$)', Name.Function),]


class LanguageInjectionMixin:
    """
    Shared functionality for language injection across different tokenizers.
    Provides language lexer initialization and tokenizer caching for recursive injection.

    This mixin enables syntax highlighting of embedded languages within strings using
    a simple comment-style annotation syntax. Supports 46 languages with full recursive
    nesting capabilities.

    Note: Language injection implementation developed with the assistance of Claude 4.5.

    Supported Languages:
        Shell:      bash, sh, shell, zsh
        Web:        javascript/js, html, css, xml, yaml/yml, json, typescript/ts
        Databases:  sql
        Backend:    python/py, ruby/rb, php, perl/pl, java, scala, kotlin/kt
        Systems:    c, cpp/c++/cxx, rust/rs, go/golang, csharp/cs
        Mobile:     swift, objc/objectivec, dart
        Other:      makefile/make, markdown/md, diff/patch

    Features:
        - Recursive language injection (any depth)
        - Python f-strings with interpolations preserved
        - Bash single and double-quoted strings
        - Bash variable interpolations ($var, $(cmd), ${var}) preserved
        - Adjacent string concatenation in bash
        - Correct token position ordering

    Featured Example - Shell mode with multi-nested injection:
        >>> # Shell mode (! prefix) with Python containing bash containing nested code
        >>> code = \"\"\"
        ... HELLO=123
        ... rp exec "
        ...     print(123)
        ...     $HELLO
        ...     '''
        ...         echo hello
        ...     '''#sh
        ... "#py
        ... \"\"\"
        >>> # Result: Three nesting levels:
        >>> #   1. Bash (shell mode) with $HELLO preserved as bash variable
        >>> #   2. Python code with print() highlighted
        >>> #   3. Nested shell script with echo highlighted

    Basic Examples:
        >>> # Python with embedded SQL
        >>> code = \"\"\"
        ... query = '''
        ... SELECT * FROM users WHERE age > 18
        ... '''#sql
        ... \"\"\"

        >>> # Python f-string with embedded SQL (interpolations preserved as Python)
        >>> code = \"\"\"
        ... query = f'''
        ... SELECT * FROM {table_name} WHERE id = {user_id}
        ... '''#sql
        ... \"\"\"

        >>> # Bash with embedded Python (single quotes)
        >>> code = "python3 -c 'print(\"hello\")'#py"

        >>> # Bash with embedded SQL (double quotes with variables preserved)
        >>> code = 'echo "SELECT * FROM $table WHERE id=$id"#sql'

        >>> # Adjacent bash strings treated as concatenated
        >>> code = 'echo "SELECT""FROM""users"#sql'

        >>> # Triple-nested: Python -> Bash -> HTML
        >>> code = \"\"\"
        ... cmd = f'''
        ... echo '<html><body>Hello World</body></html>'#html
        ... '''#bash
        ... \"\"\"

        >>> # Bash with command substitution preserved
        >>> code = 'echo "Hello $(whoami) world"#html'
    """
    def _init_language_lexers(self, primary_lexer=None):
        """Initialize all language lexers for injection support."""
        lexer_options = {'stripnl': False, 'stripall': False, 'ensurenl': False}

        # Create lazy lexers - imports and initialization deferred until first use
        self.bash_lexer = LazyBashLexer('pygments.lexers', 'BashLexer', **lexer_options)
        self.javascript_lexer = LazyLexer('pygments.lexers', 'JavascriptLexer', **lexer_options)
        self.html_lexer = LazyLexer('pygments.lexers', 'HtmlLexer', **lexer_options)
        self.sql_lexer = LazyLexer('pygments.lexers', 'SqlLexer', **lexer_options)
        self.json_lexer = LazyLexer('pygments.lexers', 'JsonLexer', **lexer_options)
        self.css_lexer = LazyLexer('pygments.lexers', 'CssLexer', **lexer_options)
        self.xml_lexer = LazyLexer('pygments.lexers', 'XmlLexer', **lexer_options)
        self.yaml_lexer = LazyLexer('pygments.lexers', 'YamlLexer', **lexer_options)
        self.ruby_lexer = LazyLexer('pygments.lexers', 'RubyLexer', **lexer_options)
        self.php_lexer = LazyLexer('pygments.lexers', 'PhpLexer', **lexer_options)
        self.cpp_lexer = LazyLexer('pygments.lexers', 'CppLexer', **lexer_options)
        self.c_lexer = LazyLexer('pygments.lexers', 'CLexer', **lexer_options)
        self.rust_lexer = LazyLexer('pygments.lexers', 'RustLexer', **lexer_options)
        self.go_lexer = LazyLexer('pygments.lexers', 'GoLexer', **lexer_options)
        self.csharp_lexer = LazyLexer('pygments.lexers', 'CSharpLexer', **lexer_options)
        self.java_lexer = LazyLexer('pygments.lexers', 'JavaLexer', **lexer_options)
        self.makefile_lexer = LazyLexer('pygments.lexers', 'MakefileLexer', **lexer_options)
        self.perl_lexer = LazyLexer('pygments.lexers', 'PerlLexer', **lexer_options)
        self.typescript_lexer = LazyLexer('pygments.lexers', 'TypeScriptLexer', **lexer_options)
        self.swift_lexer = LazyLexer('pygments.lexers', 'SwiftLexer', **lexer_options)
        self.kotlin_lexer = LazyLexer('pygments.lexers', 'KotlinLexer', **lexer_options)
        self.scala_lexer = LazyLexer('pygments.lexers', 'ScalaLexer', **lexer_options)
        self.objc_lexer = LazyLexer('pygments.lexers', 'ObjectiveCLexer', **lexer_options)
        self.dart_lexer = LazyLexer('pygments.lexers', 'DartLexer', **lexer_options)
        self.markdown_lexer = LazyLexer('pygments.lexers', 'MarkdownLexer', **lexer_options)
        self.diff_lexer = LazyLexer('pygments.lexers', 'DiffLexer', **lexer_options)

        # Use primary_lexer for python if provided, otherwise create lazy lexer
        if primary_lexer is not None:
            self.python_lexer = primary_lexer
        else:
            self.python_lexer = LazyLexer('pygments.lexers', 'Python3Lexer', **lexer_options)

        # Map language identifiers to lexers
        self.language_lexers = {
            # Shell scripting
            'bash': self.bash_lexer, 'sh': self.bash_lexer, 'shell': self.bash_lexer, 'zsh': self.bash_lexer,

            # Web development
            'javascript': self.javascript_lexer, 'js': self.javascript_lexer,
            'html': self.html_lexer,
            'css': self.css_lexer,
            'xml': self.xml_lexer,
            'yaml': self.yaml_lexer, 'yml': self.yaml_lexer,
            'json': self.json_lexer,
            'typescript': self.typescript_lexer, 'ts': self.typescript_lexer,

            # Databases
            'sql': self.sql_lexer,

            # Backend languages
            'python': self.python_lexer, 'py': self.python_lexer,
            'ruby': self.ruby_lexer, 'rb': self.ruby_lexer,
            'php': self.php_lexer,
            'perl': self.perl_lexer, 'pl': self.perl_lexer,
            'java': self.java_lexer,
            'scala': self.scala_lexer,
            'kotlin': self.kotlin_lexer, 'kt': self.kotlin_lexer,

            # Systems programming
            'c': self.c_lexer,
            'cpp': self.cpp_lexer, 'c++': self.cpp_lexer, 'cxx': self.cpp_lexer,
            'rust': self.rust_lexer, 'rs': self.rust_lexer,
            'go': self.go_lexer, 'golang': self.go_lexer,
            'csharp': self.csharp_lexer, 'cs': self.csharp_lexer,

            # Mobile development
            'swift': self.swift_lexer,
            'objc': self.objc_lexer, 'objectivec': self.objc_lexer,
            'dart': self.dart_lexer,

            # Other useful formats
            'makefile': self.makefile_lexer, 'make': self.makefile_lexer,
            'markdown': self.markdown_lexer, 'md': self.markdown_lexer,
            'diff': self.diff_lexer, 'patch': self.diff_lexer,
        }

        self._language_tokenizers_cache = {}

    def _get_language_tokenizer(self, lang):
        """
        Get or create a wrapped tokenizer for the specified language.
        This enables recursive language injection by wrapping each language's lexer
        in the appropriate tokenizer that can detect nested language tags.
        """
        lang_lower = lang.lower()

        # Return from cache if already created
        if lang_lower in self._language_tokenizers_cache:
            return self._language_tokenizers_cache[lang_lower]

        # Get the lexer for this language
        if lang_lower not in self.language_lexers:
            return None

        lexer = self.language_lexers[lang_lower]

        # Wrap it in appropriate tokenizer for recursive support
        # Use BashTokenizer for bash to enable language injection in bash strings
        if lang_lower in ('bash', 'sh', 'shell', 'zsh'):
            tokenizer = BashTokenizer(lexer)
        else:
            tokenizer = FastPygmentsTokenizer(lexer)

        # Cache it
        self._language_tokenizers_cache[lang_lower] = tokenizer

        return tokenizer


class BashTokenizer(LanguageInjectionMixin):
    """
    Bash tokenizer with language injection support for strings.

    Supports language injection in both single-quoted and double-quoted bash strings
    using the '#lang' annotation syntax. Automatically handles bash variable interpolations
    and adjacent string concatenation.

    Implementation developed with the assistance of Claude 4.5.

    Features:
        - Single-quoted strings: No expansion, full content highlighted
        - Double-quoted strings: Variables ($var, $(cmd), ${var}) preserved as bash
        - Adjacent strings: "hello""world" concatenated before highlighting
        - All 46 languages supported (inherited from LanguageInjectionMixin)
        - Recursive injection: bash strings can contain other languages with their own injections

    Single-Quoted String Examples:
        >>> # Python code in single-quoted bash string
        >>> bash_code = "python3 -c 'print(123)'#py"
        >>> # Result: 'print' and '123' highlighted as Python

        >>> # HTML in single-quoted bash string
        >>> bash_code = "echo '<div>Hello</div>'#html"
        >>> # Result: '<div>', 'Hello', '</div>' highlighted as HTML

    Double-Quoted String Examples:
        >>> # SQL with bash variable (variable NOT highlighted as SQL)
        >>> bash_code = 'echo "SELECT * FROM $table"#sql'
        >>> # Result: 'SELECT', 'FROM' highlighted as SQL, '$table' as bash variable

        >>> # Multiple variables preserved
        >>> bash_code = 'echo "SELECT * FROM $table WHERE id=$id"#sql'
        >>> # Result: SQL keywords highlighted, both $table and $id preserved

        >>> # Command substitution preserved
        >>> bash_code = 'echo "Hello $(whoami) world"#html'
        >>> # Result: 'Hello' and 'world' highlighted as HTML, '$(whoami)' preserved

        >>> # Variable expansion ${} syntax preserved
        >>> bash_code = 'echo "User: ${USER}"#html'
        >>> # Result: 'User: ' highlighted as HTML, '${USER}' preserved

    Adjacent String Concatenation Examples:
        >>> # Adjacent strings treated as one concatenated string
        >>> bash_code = 'echo "hello""world"#html'
        >>> # Result: 'hello' and 'world' both highlighted as HTML (concatenated)

        >>> # SQL fragments concatenated
        >>> bash_code = 'echo "SELECT""FROM""users"#sql'
        >>> # Result: All three keywords highlighted as SQL

        >>> # Mixed: adjacent strings with variables
        >>> bash_code = 'echo "hello"$name"world"#html'
        >>> # Result: 'hello' and 'world' highlighted, $name preserved

    Recursive Injection Examples:
        >>> # Bash containing Python with nested strings
        >>> python_code = \"\"\"
        ... cmd = f'''
        ... python3 -c 'print(123)'#py
        ... '''#bash
        ... \"\"\"
        >>> # Result: Python code inside bash string is highlighted as Python
    """
    def __init__(self, bash_lexer=None):
        if bash_lexer is None:
            from pygments.lexers import BashLexer
            bash_lexer = BashLexer(stripnl=False, stripall=False, ensurenl=False)
        self.bash_lexer = bash_lexer
        self.old_text = ''
        self.token_cache = []

        # Initialize shared language lexers
        self._init_language_lexers()

    def get_tokens_unprocessed(self, text, start_pos=0):
        """Tokenize bash code with language injection support."""
        from pygments.token import Token

        raw_tokens = list(self.bash_lexer.get_tokens_unprocessed(text))

        i = 0
        while i < len(raw_tokens):
            pos, token_type, token_text = raw_tokens[i]

            # Check for quoted strings (single or double)
            if token_type == Token.Literal.String.Single or token_type == Token.Literal.String.Double:
                # Collect all consecutive tokens for this string
                # For single quotes: Pygments returns one token
                # For double quotes: Pygments may return multiple tokens if there are $var, $(cmd), ${var}
                string_tokens = [(pos, token_type, token_text)]
                interpolation_tokens = []  # For double-quoted strings with $var expansion
                j = i + 1

                # Collect tokens until we find something that's not part of the string
                while j < len(raw_tokens):
                    next_pos, next_type, next_text = raw_tokens[j]

                    # For double-quoted strings, collect interpolations separately
                    if token_type == Token.Literal.String.Double:
                        # Check if this is an adjacent double-quoted string (bash concatenation)
                        if next_type == Token.Literal.String.Double:
                            string_tokens.append((next_pos, next_type, next_text))
                            j += 1
                            continue
                        # Check if this is a variable expansion to skip
                        elif next_type in (Token.Name.Variable, Token.Keyword, Token.Literal.String.Interpol):
                            # Collect the entire interpolation
                            if next_text == '$(':
                                # Command substitution: collect until closing )
                                interp_tokens = [(next_pos, next_type, next_text)]
                                j += 1
                                paren_count = 1
                                while j < len(raw_tokens) and paren_count > 0:
                                    p, t, txt = raw_tokens[j]
                                    interp_tokens.append((p, t, txt))
                                    if t == Token.Keyword and txt == ')':
                                        paren_count -= 1
                                    j += 1
                                interpolation_tokens.extend(interp_tokens)
                                continue
                            elif next_text == '${':
                                # Variable expansion: collect until closing }
                                interp_tokens = [(next_pos, next_type, next_text)]
                                j += 1
                                while j < len(raw_tokens):
                                    p, t, txt = raw_tokens[j]
                                    interp_tokens.append((p, t, txt))
                                    if t == Token.Literal.String.Interpol and txt == '}':
                                        j += 1
                                        break
                                    j += 1
                                interpolation_tokens.extend(interp_tokens)
                                continue
                            elif next_text.startswith('$'):
                                # Simple variable: $var
                                interpolation_tokens.append((next_pos, next_type, next_text))
                                j += 1
                                continue

                    # Not part of the string, stop collecting
                    break

                # Check if there's a language tag after the string
                if j < len(raw_tokens):
                    comment_pos, comment_type, comment_text = raw_tokens[j]
                    if (comment_type == Token.Comment.Single or comment_type == Token.Text) and comment_text.startswith('#'):
                        lang = comment_text[1:].strip()
                        if lang.lower() in self.language_lexers:
                            # Determine quote type
                            if token_type == Token.Literal.String.Single:
                                opening_quote = "'"
                                closing_quote = "'"
                                # Single-quoted: entire content in one token, strip quotes
                                inner_content = token_text[1:-1] if token_text.startswith("'") and token_text.endswith("'") else token_text
                            else:  # Double-quoted
                                opening_quote = '"'
                                closing_quote = '"'

                            # Get language tokenizer
                            language_tokenizer = self._get_language_tokenizer(lang)
                            if language_tokenizer:
                                injected_suffix = (':', 'InjectedLanguage')

                                if token_type == Token.Literal.String.Single:
                                    # Single-quoted: simple case, no interpolations
                                    yield (pos + start_pos, token_type, opening_quote)

                                    content_start = pos + start_pos + len(opening_quote)
                                    for content_pos, content_type, content_text in language_tokenizer.get_tokens_unprocessed(inner_content):
                                        marked_type = content_type + injected_suffix
                                        yield (content_start + content_pos, marked_type, content_text)

                                    closing_pos = pos + start_pos + len(token_text) - len(closing_quote)
                                    yield (closing_pos, token_type, closing_quote)

                                    # Yield comment tag
                                    yield (comment_pos + start_pos, comment_type, comment_text)

                                    # Skip both string and comment tokens
                                    i = j + 1
                                    continue
                                else:
                                    # Double-quoted: complex case with potential interpolations
                                    # Check if this is a simple string (no interpolations)
                                    if len(string_tokens) == 1 and not interpolation_tokens:
                                        # Simple case: entire string in one token like "hello world"
                                        # Extract content between quotes
                                        full_text = token_text
                                        if full_text.startswith('"') and full_text.endswith('"') and len(full_text) >= 2:
                                            inner_content = full_text[1:-1]

                                            # Yield opening quote
                                            yield (pos + start_pos, token_type, '"')

                                            # Yield highlighted content
                                            content_start = pos + start_pos + 1
                                            for content_pos, content_type, content_text in language_tokenizer.get_tokens_unprocessed(inner_content):
                                                marked_type = content_type + injected_suffix
                                                yield (content_start + content_pos, marked_type, content_text)

                                            # Yield closing quote
                                            closing_pos = pos + start_pos + len(full_text) - 1
                                            yield (closing_pos, token_type, '"')

                                            # Yield comment tag
                                            yield (comment_pos + start_pos, comment_type, comment_text)

                                            i = j + 1
                                            continue

                                    # Complex case: multiple tokens with interpolations or adjacent strings
                                    # For adjacent strings like "hello""world", concatenate contents and highlight as one
                                    tokens_to_yield = []

                                    # Separate complete strings (like "hello") from fragments (like just "hello )
                                    # Complete strings have both opening and closing quotes
                                    fragments = []  # List of (pos, content_without_quotes)
                                    quote_positions = []  # List of (pos, quote_char) for rendering

                                    for str_pos, str_type, str_text in string_tokens:
                                        if str_text == '"':
                                            # Standalone opening or closing quote
                                            quote_positions.append((str_pos, '"'))
                                        elif str_text.startswith('"') and str_text.endswith('"') and len(str_text) >= 2:
                                            # Complete string like "hello"
                                            quote_positions.append((str_pos, '"'))
                                            fragments.append((str_pos + 1, str_text[1:-1]))  # Strip quotes
                                            quote_positions.append((str_pos + len(str_text) - 1, '"'))
                                        elif str_text.startswith('"'):
                                            # Fragment starting with quote like "hello
                                            quote_positions.append((str_pos, '"'))
                                            fragments.append((str_pos + 1, str_text[1:]))
                                        elif str_text.endswith('"'):
                                            # Fragment ending with quote like world"
                                            fragments.append((str_pos, str_text[:-1]))
                                            quote_positions.append((str_pos + len(str_text) - 1, '"'))
                                        else:
                                            # Middle fragment with no quotes
                                            fragments.append((str_pos, str_text))

                                    # Concatenate all content fragments for highlighting
                                    concatenated_content = ''.join(f[1] for f in fragments)

                                    # Highlight the concatenated content
                                    if concatenated_content:
                                        content_tokens = list(language_tokenizer.get_tokens_unprocessed(concatenated_content))

                                        # Map highlighted tokens back to original positions in source
                                        for tok_pos, tok_type, tok_text in content_tokens:
                                            # Find which fragment(s) this token spans
                                            current_offset = 0
                                            tok_start_in_concat = tok_pos
                                            tok_end_in_concat = tok_pos + len(tok_text)

                                            for frag_pos, frag_text in fragments:
                                                frag_start = current_offset
                                                frag_end = current_offset + len(frag_text)

                                                # Check if this token overlaps with this fragment
                                                if tok_start_in_concat < frag_end and tok_end_in_concat > frag_start:
                                                    # Calculate the overlap
                                                    overlap_start = max(tok_start_in_concat, frag_start)
                                                    overlap_end = min(tok_end_in_concat, frag_end)

                                                    # Extract the overlapping text
                                                    text_start_in_token = overlap_start - tok_start_in_concat
                                                    text_end_in_token = text_start_in_token + (overlap_end - overlap_start)
                                                    overlap_text = tok_text[text_start_in_token:text_end_in_token]

                                                    # Calculate position in original source
                                                    pos_in_fragment = overlap_start - frag_start
                                                    actual_pos = frag_pos + pos_in_fragment

                                                    marked_type = tok_type + injected_suffix
                                                    tokens_to_yield.append((actual_pos + start_pos, marked_type, overlap_text))

                                                current_offset = frag_end

                                    # Add quote tokens
                                    for q_pos, q_char in quote_positions:
                                        tokens_to_yield.append((q_pos + start_pos, Token.Literal.String.Double, q_char))

                                    # Add interpolations as-is (bash variables/commands)
                                    for interp_pos, interp_type, interp_text in interpolation_tokens:
                                        tokens_to_yield.append((interp_pos + start_pos, interp_type, interp_text))

                                    # Add comment tag
                                    tokens_to_yield.append((comment_pos + start_pos, comment_type, comment_text))

                                    # Sort by position and yield
                                    tokens_to_yield.sort(key=lambda t: t[0])
                                    for token in tokens_to_yield:
                                        yield token

                                    # Skip all processed tokens
                                    i = j + 1
                                    continue

            # Regular token
            yield (pos + start_pos, token_type, token_text)
            i += 1


class FastPygmentsTokenizer(LanguageInjectionMixin):
    """
    Fast Python tokenizer with language injection support.

    Provides syntax highlighting for Python code with support for embedding other
    languages within string literals using the '#lang' annotation syntax. Handles
    f-string interpolations correctly, preserving Python expressions while highlighting
    the string content in the target language.

    Language injection features developed with the assistance of Claude 4.5.

    Features:
        - Support for all Python string types (', ", ''', \"\"\")
        - F-string interpolations preserved as Python tokens
        - All 46 languages supported (inherited from LanguageInjectionMixin)
        - Recursive injection for nested language strings
        - Incremental tokenization with caching for performance
        - Correct token position ordering for cursor positioning

    Basic String Examples:
        >>> # SQL in regular Python string
        >>> code = \"\"\"
        ... query = '''
        ... SELECT * FROM users WHERE age > 18
        ... '''#sql
        ... \"\"\"
        >>> # Result: 'SELECT', 'FROM', 'users', 'WHERE', 'age', '18' highlighted as SQL

        >>> # JavaScript in Python string
        >>> code = \"\"\"
        ... script = '''
        ... function hello() { return 'world'; }
        ... '''#js
        ... \"\"\"
        >>> # Result: JavaScript keywords and syntax highlighted

        >>> # HTML in Python string
        >>> code = 'html = "<div>Hello</div>"#html'
        >>> # Result: '<div>', 'Hello', '</div>' highlighted as HTML

    F-String Examples (Interpolations Preserved):
        >>> # SQL with Python variables preserved
        >>> code = \"\"\"
        ... query = f'''
        ... SELECT * FROM {table_name} WHERE id = {user_id}
        ... '''#sql
        ... \"\"\"
        >>> # Result: SQL keywords highlighted, {table_name} and {user_id} as Python

        >>> # HTML with Python expressions preserved
        >>> code = \"\"\"
        ... html = f'''
        ... <div class="{css_class}">{content}</div>
        ... '''#html
        ... \"\"\"
        >>> # Result: HTML tags highlighted, {css_class} and {content} as Python

        >>> # Bash with Python variables
        >>> code = \"\"\"
        ... cmd = f'''
        ... echo "Processing {filename}"
        ... '''#bash
        ... \"\"\"
        >>> # Result: Bash syntax highlighted, {filename} as Python

    Nested/Recursive Injection Examples:
        >>> # Python -> Bash -> HTML (triple-nested)
        >>> code = \"\"\"
        ... cmd = f'''
        ... echo '<html><body>Hello World</body></html>'#html
        ... '''#bash
        ... \"\"\"
        >>> # Result: Python (outer) -> Bash (middle) -> HTML (inner) all highlighted

        >>> # Python -> Bash -> SQL
        >>> code = \"\"\"
        ... script = '''
        ... mysql -e 'SELECT * FROM users'#sql
        ... '''#bash
        ... \"\"\"
        >>> # Result: SQL keywords highlighted within bash within Python

        >>> # Complex nesting with f-strings
        >>> code = \"\"\"
        ... cmd = f'''
        ... echo "SELECT * FROM {table}"#sql
        ... '''#bash
        ... \"\"\"
        >>> # Result: SQL highlighted, {table} as Python, all within bash

    Shebang Syntax Examples:
        >>> # Alternative annotation using #! (hashbang)
        >>> code = \"\"\"
        ... query = '''#!sql
        ... SELECT * FROM users
        ... '''
        ... \"\"\"
        >>> # Result: SQL highlighting with #! on first line

        >>> # Shebang paths work too
        >>> code = \"\"\"
        ... script = '''#!/bin/bash
        ... echo "hello"
        ... '''
        ... \"\"\"
        >>> # Result: Bash highlighting (extracts 'bash' from path)

    DOCTYPE Syntax Examples:
        >>> # HTML can use <!DOCTYPE html> as language marker
        >>> code = \"\"\"
        ... page = '''<!DOCTYPE html>
        ... <html><body>Hello</body></html>
        ... '''
        ... \"\"\"
        >>> # Result: Full HTML highlighting including DOCTYPE
    """
    def __init__(self,pygments_lexer=None):
        if pygments_lexer is None:
            # Lazy import of default lexer
            import six
            if six.PY2:
                from pygments.lexers import PythonLexer
                pygments_lexer = PythonLexer()
            else:
                from pygments.lexers import Python3Lexer
                pygments_lexer = Python3Lexer()
        self.old_text=''
        self.token_cache=[]
        self.pygments_lexer=pygments_lexer

        # Initialize shared language lexers, using pygments_lexer as the primary Python lexer
        self._init_language_lexers(primary_lexer=pygments_lexer)

    def _set_new_text(self,text):
        # from rp import longest_common_prefix
        #Used to invalidate the token_cache
        prefix=longest_common_prefix(text,self.old_text)
        length=len(prefix)
        # self.token_cache=[token for token in self.token_cache if token[0]<length]
        from bisect import bisect_left
        try:
            del self.token_cache[max(0,bisect_left(self.token_cache,(length,))-1):]
        except:
            self.token_cache=[]
        try:
            while self.token_cache[-1][1]!='\n':
            # for _ in range(10):
                self.token_cache.pop()
            #Snip off the tail just to be sure its correct, in particular because '"HELLO"' is treated as 3 tokens ('"','HELLO','"') we need to make sure the beginning quote is kept when re-highlighting
        except:
            pass
        self.old_text=text
    def get_tokens_unprocessed(self,text):

        if text.startswith('!'):
            #ORIGINAL CODE: Not for nested languages! 

            # yield (0, Token.Keyword, text)
            #Yields something like [(0, Token.Keyword, 'def'), (3, Token.Text, ' '), (4, Token.Name.Function, 'f'), (5, Token.Punctuation, '('), (6, Token.Punctuation, ')'), (7, Token.Punctuation, ':'), (8, Token.Keyword, 'pass')]
            self._set_new_text(text)
            # from rp import text_to_speech
            # text_to_speech(len(self.token_cache))
            yield from self.token_cache
            # for token in self.token_cache:
                # yield token
            if not self.token_cache:
                start_pos=0
            else:
                start_pos=self.token_cache[-1][0]+len(self.token_cache[-1][2])
            if start_pos>=len(text):
                return#We're aleady at the end of the string; we're done. no more tokens.
            else:
                for token in self.pygments_lexer.get_tokens_unprocessed(text[start_pos:]):
                    token=(token[0]+start_pos,token[1],token[2])
                    # start,species,data=token
                    # start+=start_pos
                    # token=start,species,data
                    self.token_cache.append(token)
                    yield token
            return


        # yield (0, Token.Keyword, text)
        #Yields something like [(0, Token.Keyword, 'def'), (3, Token.Text, ' '), (4, Token.Name.Function, 'f'), (5, Token.Punctuation, '('), (6, Token.Punctuation, ')'), (7, Token.Punctuation, ':'), (8, Token.Keyword, 'pass')]
        self._set_new_text(text)
        # from rp import text_to_speech
        # text_to_speech(len(self.token_cache))
        yield from self.token_cache
        # for token in self.token_cache:
            # yield token
        if not self.token_cache:
            start_pos=0
        else:
            start_pos=self.token_cache[-1][0]+len(self.token_cache[-1][2])
        if start_pos>=len(text):
            return#We're aleady at the end of the string; we're done. no more tokens.
        else:
            # <CLAUDE CODE START: Improved Multi-language string highlighting implementation>
            # Get the raw tokens from the Pygments lexer
            raw_tokens = list(self.pygments_lexer.get_tokens_unprocessed(text[start_pos:]))
            
            # Process tokens for special language highlighting
            i = 0
            while i < len(raw_tokens):
                pos, token_type, token_text = raw_tokens[i]
                adjusted_pos = pos + start_pos
                
                # Define string token types to look for
                string_token_types = [
                    Token.Literal.String,
                    Token.Literal.String.Doc,
                    Token.Literal.String.Double,
                    Token.Literal.String.Single,
                    Token.Literal.String.Backtick,
                    Token.Literal.String.Heredoc,
                ]
                
                # Check if this is a string token
                if any(token_type == t or str(token_type).startswith(str(t) + '.') for t in string_token_types):
                    # This is the start of a string - collect all consecutive string tokens
                    # Check if previous token was an f-string prefix
                    string_tokens = []
                    if i > 0 and raw_tokens[i-1][1] == Token.Literal.String.Affix:
                        string_tokens.append(raw_tokens[i-1])
                    string_tokens.append((pos, token_type, token_text))
                    string_start = i
                    current_pos = pos + len(token_text)
                    j = i + 1
                    
                    # Collect all consecutive string tokens (including f-string parts, tracking interpolations)
                    interpolation_tokens = []  # Tokens inside {expr} - keep as Python
                    while j < len(raw_tokens):
                        next_pos, next_type, next_text = raw_tokens[j]

                        # For f-strings: collect interpolated expressions separately
                        if (next_type == Token.Literal.String.Interpol or next_type == Token.Punctuation) and next_text in '{}':
                            if next_text == '{':
                                # Start of interpolation - collect until matching }
                                interp_tokens = [(next_pos, next_type, next_text)]
                                brace_count = 1
                                j += 1
                                while j < len(raw_tokens) and brace_count > 0:
                                    p, t, txt = raw_tokens[j]
                                    interp_tokens.append((p, t, txt))
                                    if t == Token.Punctuation or t == Token.Literal.String.Interpol:
                                        if txt == '{': brace_count += 1
                                        elif txt == '}': brace_count -= 1
                                    j += 1
                                interpolation_tokens.extend(interp_tokens)
                                current_pos = interp_tokens[-1][0] + len(interp_tokens[-1][2])
                                continue

                        # If not consecutive or not a string token, break
                        if next_pos != current_pos or not any(next_type == t or str(next_type).startswith(str(t) + '.') for t in string_token_types):
                            break

                        # Add this string token to our collection
                        string_tokens.append((next_pos, next_type, next_text))
                        current_pos = next_pos + len(next_text)
                        j += 1
                    
                    # Helper: yield tokens in position order (interleaving language and Python)
                    def yield_with_interpolations_as_python(lang_tokens):
                        # Adjust interpolation positions
                        interp_adjusted = [(t[0] + start_pos, t[1], t[2]) for t in interpolation_tokens]

                        # Merge and sort by position
                        all_tokens = sorted(lang_tokens + interp_adjusted, key=lambda t: t[0])

                        # Yield in position order
                        for token in all_tokens:
                            self.token_cache.append(token)
                            yield token

                    if len(string_tokens) > 0 or '#!' in token_text:
                        # Combine all string tokens into a single string
                        combined_text = ''.join(t[2] for t in string_tokens)
                        combined_start = string_tokens[0][0]
                        combined_pos = combined_start + start_pos
                        
                        # Detect quote type and extract content
                        opening_quotes = ""
                        closing_quotes = ""
                        content = combined_text
                        
                        # Identify opening quotes, including prefix modifiers (r, f, etc.)
                        # Regular expressions would be better here, but we'll use simple string checks
                        prefix = ""
                        
                        # Check for r-strings, f-strings, etc.
                        if any(combined_text.lower().startswith(p) for p in ['r', 'f', 'b', 'u', 'fr', 'rf', 'br', 'rb']):
                            # Extract the prefix (r, f, etc.)
                            for p in ['fr', 'rf', 'br', 'rb', 'r', 'f', 'b', 'u']:
                                if combined_text.lower().startswith(p):
                                    prefix_end = len(p)
                                    prefix = combined_text[:prefix_end]
                                    content = combined_text[prefix_end:]
                                    break
                        
                        # Now check for the actual quotes
                        if content.startswith('"""'):
                            opening_quotes = prefix + '"""'
                            content = content[3:]
                        elif content.startswith("'''"):
                            opening_quotes = prefix + "'''"
                            content = content[3:]
                        elif content.startswith('"'):
                            opening_quotes = prefix + '"'
                            content = content[1:]
                        elif content.startswith("'"):
                            opening_quotes = prefix + "'"
                            content = content[1:]
                        elif not prefix and combined_text.startswith('"""'):
                            # No prefix detected but still starts with quotes
                            opening_quotes = '"""'
                            content = combined_text[3:]
                        elif not prefix and combined_text.startswith("'''"):
                            opening_quotes = "'''"
                            content = combined_text[3:]
                        elif not prefix and combined_text.startswith('"'):
                            opening_quotes = '"'
                            content = combined_text[1:]
                        elif not prefix and combined_text.startswith("'"):
                            opening_quotes = "'"
                            content = combined_text[1:]
                        else:
                            # Failed to detect opening quotes
                            opening_quotes = ""
                            content = combined_text
                        
                        # Identify closing quotes
                        if content.endswith('"""'):
                            closing_quotes = '"""'
                            content = content[:-3]
                        elif content.endswith("'''"):
                            closing_quotes = "'''"
                            content = content[:-3]
                        elif content.endswith('"'):
                            closing_quotes = '"'
                            content = content[:-1]
                        elif content.endswith("'"):
                            closing_quotes = "'"
                            content = content[:-1]
                        
                        # Check for language tag in the content
                        bang_pos = combined_text.find('#!')
                        doctype_pos = combined_text.lower().find('<!doctype html')
                        language_found = False

                        # Check for <!DOCTYPE html> first (case-insensitive)
                        if doctype_pos >= 0:
                            # Treat <!DOCTYPE html> as an HTML language marker
                            lang = 'html'

                            # Find the end of the DOCTYPE declaration (usually ">")
                            doctype_end = combined_text.find('>', doctype_pos)
                            if doctype_end == -1:
                                doctype_end = len(combined_text)
                            else:
                                doctype_end += 1  # Include the ">"

                            # If we recognize this language, use its lexer
                            if lang.lower() in self.language_lexers:
                                language_found = True

                                # Process using HTML lexer
                                tokens_to_yield = []

                                # Calculate the positions of different parts
                                if opening_quotes:
                                    # 1. Opening quotes as string literal
                                    opening_len = len(opening_quotes)
                                    chars_seen = 0

                                    for str_pos, str_type, str_text in string_tokens:
                                        if chars_seen >= opening_len:
                                            break

                                        # Check if this token is entirely part of opening quotes
                                        if chars_seen + len(str_text) <= opening_len:
                                            # Entire token is part of opening quotes
                                            tokens_to_yield.append(
                                                (str_pos + start_pos, str_type, str_text)
                                            )
                                            chars_seen += len(str_text)
                                        else:
                                            # Token spans opening quotes and content
                                            # Split it: yield only the opening quotes part
                                            quote_part = str_text[:opening_len - chars_seen]
                                            tokens_to_yield.append(
                                                (str_pos + start_pos, str_type, quote_part)
                                            )
                                            chars_seen = opening_len
                                            break

                                    # 2. Process entire content with HTML highlighting
                                    language_tokenizer = self._get_language_tokenizer(lang)
                                    content_start = combined_pos + len(opening_quotes)

                                    # Extract content without closing quotes
                                    html_content = combined_text[len(opening_quotes):]
                                    if closing_quotes and html_content.endswith(closing_quotes):
                                        html_content = html_content[:-len(closing_quotes)]

                                    # Highlight the HTML content
                                    injected_suffix = (':', 'InjectedLanguage')
                                    for content_pos, content_type, content_text in language_tokenizer.get_tokens_unprocessed(html_content):
                                        marked_type = content_type + injected_suffix
                                        tokens_to_yield.append(
                                            (content_start + content_pos, marked_type, content_text)
                                        )

                                    # 3. Add closing quotes if present
                                    if closing_quotes:
                                        closing_pos = combined_pos + len(combined_text) - len(closing_quotes)
                                        tokens_to_yield.append(
                                            (closing_pos, Token.Literal.String, closing_quotes)
                                        )

                                # Yield all tokens
                                yield from yield_with_interpolations_as_python(tokens_to_yield)

                                # Skip all the tokens we've processed
                                i = j
                                continue

                        elif bang_pos >= 0:
                            # Extract language identifier
                            first_line_end = combined_text.find('\n', bang_pos)
                            if first_line_end == -1:
                                first_line_end = len(combined_text)
                            
                            lang_tag = combined_text[bang_pos+2:first_line_end].strip()
                            lang = lang_tag.split()[0].split('/')[-1] if '/' in lang_tag else lang_tag
                            
                            # If we recognize this language, use its lexer
                            if lang.lower() in self.language_lexers:
                                language_found = True
                                
                                # Process using language-specific lexer
                                tokens_to_yield = []
                                
                                # Calculate the positions of different parts
                                if opening_quotes:
                                    # 1. Opening quotes as string literal
                                    # Split opening quotes from string_tokens correctly
                                    opening_len = len(opening_quotes)
                                    chars_seen = 0

                                    for str_pos, str_type, str_text in string_tokens:
                                        if chars_seen >= opening_len:
                                            break

                                        # Check if this token is entirely part of opening quotes
                                        if chars_seen + len(str_text) <= opening_len:
                                            # Entire token is part of opening quotes
                                            tokens_to_yield.append(
                                                (str_pos + start_pos, str_type, str_text)
                                            )
                                            chars_seen += len(str_text)
                                        else:
                                            # Token spans opening quotes and content
                                            # Split it: yield only the opening quotes part
                                            quote_part = str_text[:opening_len - chars_seen]
                                            tokens_to_yield.append(
                                                (str_pos + start_pos, str_type, quote_part)
                                            )
                                            chars_seen = opening_len
                                            break
                                    
                                    # 2. Content before the language tag, if any
                                    if bang_pos > len(opening_quotes):
                                        prefix = combined_text[len(opening_quotes):bang_pos]
                                        tokens_to_yield.append(
                                            (combined_pos + len(opening_quotes), Token.Text, prefix)
                                        )
                                    
                                    # 3. The language tag as a hashbang
                                    shebang_text = combined_text[bang_pos:first_line_end].strip()
                                    injected_suffix = (':', 'InjectedLanguage')
                                    tokens_to_yield.append(
                                        (combined_pos + bang_pos, Token.Comment.Hashbang + injected_suffix, shebang_text)
                                    )
                                    
                                    # 4. Add the newline if present
                                    if first_line_end < len(combined_text):
                                        tokens_to_yield.append(
                                            (combined_pos + first_line_end, Token.Text, '\n')
                                        )
                                        
                                        # 5. Content after the first line with language-specific highlighting
                                        remaining_content = combined_text[first_line_end+1:]
                                        if closing_quotes and remaining_content.endswith(closing_quotes):
                                            remaining_content = remaining_content[:-len(closing_quotes)]
                                        
                                        # Use language-specific tokenizer for the main content (enables recursive injection)
                                        language_tokenizer = self._get_language_tokenizer(lang)
                                        content_tokens = language_tokenizer.get_tokens_unprocessed(remaining_content)
                                        
                                        # Add with adjusted positions
                                        # Append :Token.InjectedLanguage to add background overlay
                                        content_start = combined_pos + first_line_end + 1
                                        injected_suffix = (':', 'InjectedLanguage')
                                        for content_pos, content_type, content_text in content_tokens:
                                            marked_type = content_type + injected_suffix
                                            tokens_to_yield.append(
                                                (content_start + content_pos, marked_type, content_text)
                                            )
                                    
                                    # 6. Add closing quotes if present
                                    if closing_quotes:
                                        # Calculate position from the end of combined_text
                                        closing_pos = combined_pos + len(combined_text) - len(closing_quotes)
                                        tokens_to_yield.append(
                                            (closing_pos, Token.Literal.String, closing_quotes)
                                        )
                                
                                # Yield all tokens (skipping f-string interpolations)
                                yield from yield_with_interpolations_as_python(tokens_to_yield)
                                
                                # Skip all the tokens we've processed
                                i = j
                                continue
                        
                        # Check for trailing comment-style language tag
                        elif j < len(raw_tokens) and raw_tokens[j][1] == Token.Comment.Single:
                            comment_pos, comment_type, comment_text = raw_tokens[j]
                            if comment_text.startswith('#'):
                                lang = comment_text[1:].strip()
                                if lang.lower() in self.language_lexers:
                                    language_found = True
                                    
                                    # Process using language-specific lexer with comment tag
                                    tokens_to_yield = []

                                    # 1. Opening quotes
                                    if opening_quotes:
                                        tokens_to_yield.append(
                                            (combined_pos, Token.Literal.String, opening_quotes)
                                        )

                                    # 2. Content with language-specific highlighting (enables recursive injection)
                                    # For f-strings with interpolations: process each string fragment separately
                                    language_tokenizer = self._get_language_tokenizer(lang)
                                    injected_suffix = (':', 'InjectedLanguage')

                                    if interpolation_tokens:
                                        # Process each string token fragment through the language lexer
                                        # Skip first token if it's the opening quotes, skip last if closing quotes
                                        string_content_tokens = string_tokens[:]
                                        # Remove prefix if present
                                        if string_content_tokens and string_content_tokens[0][1] == Token.Literal.String.Affix:
                                            string_content_tokens = string_content_tokens[1:]
                                        # Remove opening quotes
                                        if string_content_tokens and string_content_tokens[0][2] in ('"""', "'''", '"', "'"):
                                            string_content_tokens = string_content_tokens[1:]
                                        # Remove closing quotes
                                        if string_content_tokens and string_content_tokens[-1][2] in ('"""', "'''", '"', "'"):
                                            string_content_tokens = string_content_tokens[:-1]

                                        # Highlight each fragment
                                        for str_pos, str_type, str_text in string_content_tokens:
                                            frag_tokens = list(language_tokenizer.get_tokens_unprocessed(str_text))

                                            # If lexer returned no tokens (e.g., just whitespace), yield original
                                            if not frag_tokens:
                                                tokens_to_yield.append(
                                                    (str_pos + start_pos, str_type + injected_suffix, str_text)
                                                )
                                            else:
                                                for frag_pos, frag_type, frag_text in frag_tokens:
                                                    marked_type = frag_type + injected_suffix
                                                    final_pos = str_pos + start_pos + frag_pos
                                                    tokens_to_yield.append(
                                                        (final_pos, marked_type, frag_text)
                                                    )
                                    else:
                                        # No interpolations - process normally
                                        content_tokens = language_tokenizer.get_tokens_unprocessed(content)
                                        content_start = combined_pos + len(opening_quotes)
                                        for content_pos, content_type, content_text in content_tokens:
                                            marked_type = content_type + injected_suffix
                                            tokens_to_yield.append(
                                                (content_start + content_pos, marked_type, content_text)
                                            )
                                    
                                    # 3. Closing quotes
                                    if closing_quotes:
                                        # Calculate closing position based on combined_text length
                                        # For f-strings with interpolations, string_tokens has multiple elements
                                        # and the last element is the closing quotes
                                        # For regular strings, Pygments returns one token with the entire string
                                        # so we need to calculate the position
                                        if interpolation_tokens:
                                            # F-string: use actual position from string_tokens
                                            closing_pos = string_tokens[-1][0] + start_pos
                                        else:
                                            # Regular string: calculate from combined_text length
                                            closing_pos = combined_pos + len(combined_text) - len(closing_quotes)
                                        tokens_to_yield.append(
                                            (closing_pos, Token.Literal.String, closing_quotes)
                                        )
                                    
                                    # 4. The language tag comment
                                    tokens_to_yield.append(
                                        (comment_pos + start_pos, Token.Comment.Single, comment_text)
                                    )
                                    
                                    # Yield all tokens (skipping f-string interpolations)
                                    yield from yield_with_interpolations_as_python(tokens_to_yield)
                                    
                                    # Skip all the tokens we've processed including the comment
                                    i = j + 1
                                    continue
                    
                    # If no language tag was found, or language not supported,
                    # just yield all collected string tokens normally
                    if not language_found:
                        # Merge string and interpolation tokens, sorted by position
                        all_tokens = []
                        for str_pos, str_type, str_text in string_tokens:
                            all_tokens.append((str_pos + start_pos, str_type, str_text))
                        for token in interpolation_tokens:
                            all_tokens.append((token[0] + start_pos, token[1], token[2]))

                        # Sort by position and yield
                        all_tokens.sort(key=lambda t: t[0])
                        for token in all_tokens:
                            self.token_cache.append(token)
                            yield token
                        i = j
                        continue
                
                # Regular token processing for non-string tokens
                adjusted_token = (pos + start_pos, token_type, token_text)
                self.token_cache.append(adjusted_token)
                yield adjusted_token
                i += 1
            # <CLAUDE CODE END: Improved Multi-language string highlighting implementation>
# t=FastPygmentsTokenizer()
# print(list(t.get_tokens_unprocessed('((HELLO))')))
# print(list(t.get_tokens_unprocessed('((HELLO)))')))
# print(list(t.get_tokens_unprocessed('((HO)))')))

        
        
        
        

class PygmentsLexer(Lexer):
    """
    Lexer that calls a pygments lexer.

    Example::

        from pygments.lexers import HtmlLexer
        lexer = PygmentsLexer(HtmlLexer)

    Note: Don't forget to also load a Pygments compatible style. E.g.::

        from rp.prompt_toolkit.styles.from_pygments import style_from_pygments
        from pygments.styles import get_style_by_name
        style = style_from_pygments(get_style_by_name('monokai'))

    :param pygments_lexer_cls: A `Lexer` from Pygments.
    :param sync_from_start: Start lexing at the start of the document. This
        will always give the best results, but it will be slow for bigger
        documents. (When the last part of the document is display, then the
        whole document will be lexed by Pygments on every key stroke.) It is
        recommended to disable this for inputs that are expected to be more
        than 1,000 lines.
    :param syntax_sync: `SyntaxSync` object.
    """
    # Minimum amount of lines to go backwards when starting the parser.
    # This is important when the lines are retrieved in reverse order, or when
    # scrolling upwards. (Due to the complexity of calculating the vertical
    # scroll offset in the `Window` class, lines are not always retrieved in
    # order.)
    MIN_LINES_BACKWARDS = 50

    # When a parser was started this amount of lines back, read the parser
    # until we get the current line. Otherwise, start a new parser.
    # (This should probably be bigger than MIN_LINES_BACKWARDS.)
    REUSE_GENERATOR_MAX_DISTANCE = 100

    def __init__(self, pygments_lexer_cls, sync_from_start=True, syntax_sync=None):
        assert syntax_sync is None or isinstance(syntax_sync, SyntaxSync)

        self.pygments_lexer_cls = pygments_lexer_cls
        self.sync_from_start = to_cli_filter(sync_from_start)

        self.old_text=""

        # Instantiate the Pygments lexer. (Python)
        self.pygments_lexer = pygments_lexer_cls(
            stripnl=False,
            stripall=False,
            ensurenl=False,
        )
        self.fast_pygments_lexer=self.pygments_lexer
        self.fast_pygments_tokenizer=FastPygmentsTokenizer(self.pygments_lexer)

        # Create lazy Bash lexer and tokenizer - only initialized when needed
        self._lazy_bash_lexer = None
        self._lazy_bash_tokenizer = None

        # Create syntax sync instance.
        self.syntax_sync = syntax_sync or RegexSync.from_pygments_lexer_cls(pygments_lexer_cls)

    @property
    def fast_bash_lexer(self):
        if self._lazy_bash_lexer is None:
            self._lazy_bash_lexer = LazyBashLexer(
                'pygments.lexers',
                'BashLexer',
                stripnl=False,
                stripall=False,
                ensurenl=False,
            )
        return self._lazy_bash_lexer

    @property
    def fast_bash_tokenizer(self):
        if self._lazy_bash_tokenizer is None:
            self._lazy_bash_tokenizer = BashTokenizer(self.fast_bash_lexer)
        return self._lazy_bash_tokenizer

    def get_lexer(self, document):
        text = document.text
        if text.startswith("!"):
            return self.fast_bash_lexer  # Bash
        else:
            return self.fast_pygments_lexer  # Python

    # <CLAUDE CODE START: Update tokenizer selection to check for language tags>
    def get_tokenizer(self, document):
        text = document.text
        if text.startswith("!"):
            return self.fast_bash_tokenizer  # Bash
        # Check for multiline string with language shebang
        elif '"""#!' in text or "'''#!" in text or ('#!' in text and ('"""' in text or "'''" in text)):
            # Return Python lexer for now, we'll handle language-specific highlights later
            return self.fast_pygments_tokenizer  # Python
        else:
            return self.fast_pygments_tokenizer  # Python
    # <CLAUDE CODE END: Update tokenizer selection to check for language tags>

    @classmethod
    def from_filename(cls, filename, sync_from_start=True):
        """
        Create a `Lexer` from a filename.
        """
        # Inline imports: the Pygments dependency is optional!
        from pygments.util import ClassNotFound
        from pygments.lexers import get_lexer_for_filename

        try:
            pygments_lexer = get_lexer_for_filename(filename)
        except ClassNotFound:
            return SimpleLexer()
        else:
            return cls(pygments_lexer.__class__, sync_from_start=sync_from_start)

    def lex_document(self, cli, document):
        """
        Create a lexer function that takes a line number and returns the list
        of (Token, text) tuples as the Pygments lexer returns for that line.
        """
        # Cache of already lexed lines.
        cache = {}

        # Pygments generators that are currently lexing.
        line_generators = {}  # Map lexer generator to the line number.

        def get_syntax_sync():
            " The Syntax synchronisation objcet that we currently use. "
            if self.sync_from_start(cli):
                return SyncFromStart()
            else:
                return self.syntax_sync

        def find_closest_generator(i):
            " Return a generator close to line 'i', or None if none was fonud. "
            for generator, lineno in line_generators.items():
                if lineno < i and i - lineno < self.REUSE_GENERATOR_MAX_DISTANCE:
                    return generator

        def create_line_generator(start_lineno, column=0):
            """
            Create a generator that yields the lexed lines.
            Each iteration it yields a (line_number, [(token, text), ...]) tuple.
            """
            def get_tokens():
                text = '\n'.join(document.lines[start_lineno:])[column:]
                text = '\n'.join(document.lines[0:])[0:]

                # We call `get_tokens_unprocessed`, because `get_tokens` will
                # still replace \r\n and \r by \n.  (We don't want that,
                # Pygments should return exactly the same amount of text, as we
                # have given as input.)
                for _, t, v in self.get_tokenizer(document).get_tokens_unprocessed(text):
                    yield t, v

            return enumerate(split_lines(get_tokens()), start_lineno)

        def get_generator(i):
            """
            Find an already started generator that is close, or create a new one.
            """
            # Find closest line generator.
            generator = find_closest_generator(i)
            if generator:
                return generator

            # No generator found. Determine starting point for the syntax
            # synchronisation first.

            # Go at least x lines back. (Make scrolling upwards more
            # efficient.)
            i = max(0, i - self.MIN_LINES_BACKWARDS)

            if i == 0:
                row = 0
                column = 0
            else:
                row, column = get_syntax_sync().get_sync_start_position(document, i)

            # Find generator close to this point, or otherwise create a new one.
            generator = find_closest_generator(i)
            if generator:
                return generator
            else:
                generator = create_line_generator(row, column)

            # If the column is not 0, ignore the first line. (Which is
            # incomplete. This happens when the synchronisation algorithm tells
            # us to start parsing in the middle of a line.)
            if column:
                next(generator)
                row += 1

            line_generators[generator] = row
            return generator

        def get_line(i):
            " Return the tokens for a given line number. "
            try:
                return cache[i]
            except KeyError:
                generator = get_generator(i)

                # Exhaust the generator, until we find the requested line.
                for num, line in generator:
                    cache[num] = line
                    if num == i:
                        line_generators[generator] = i

                        # Remove the next item from the cache.
                        # (It could happen that it's already there, because of
                        # another generator that started filling these lines,
                        # but we want to synchronise these lines with the
                        # current lexer's state.)
                        if num + 1 in cache:
                            del cache[num + 1]

                        return cache[num]
            return []
        self.old_text=document.text#For speed's sake: Ryan Burgert
        return get_line


class LazyPygmentsLexer(Lexer):
    """
    Lazy wrapper for PygmentsLexer that defers lexer imports until first use.
    This class was Written by Claude, Aug 5 2025. Resulted in massive pterm boot speed boost. Pygments initializations were taking the majority of the time.
    """
    
    def __init__(self):
        self._real_lexer = None
    
    def _get_real_lexer(self):
        if self._real_lexer is None:
            # Import only when needed
            import six
            if six.PY2:
                from pygments.lexers import PythonLexer
                lexer_class = PythonLexer
            else:
                from pygments.lexers import Python3Lexer as PythonLexer
                lexer_class = PythonLexer
            
            # Create the actual PygmentsLexer
            self._real_lexer = PygmentsLexer(lexer_class)
        return self._real_lexer
    
    def lex_document(self, cli, document):
        return self._get_real_lexer().lex_document(cli, document)
    
    def __getattr__(self, name):
        return getattr(self._get_real_lexer(), name)
