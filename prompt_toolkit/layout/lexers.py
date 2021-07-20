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

__all__ = (
    'Lexer',
    'SimpleLexer',
    'PygmentsLexer',
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



from pygments.lexers import Python3Lexer
class FastPygmentsTokenizer:
    def __init__(self,pygments_lexer=Python3Lexer()):
        self.old_text=''
        self.token_cache=[]
        self.pygments_lexer=pygments_lexer
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

        # Instantiate the Pygments lexer.
        self.pygments_lexer = pygments_lexer_cls(
            stripnl=False,
            stripall=False,
            ensurenl=False)

        self.fast_pygments_lexer=self.pygments_lexer
        self.fast_pygments_lexer=FastPygmentsTokenizer(self.pygments_lexer)

        # Create syntax sync instance.
        self.syntax_sync = syntax_sync or RegexSync.from_pygments_lexer_cls(pygments_lexer_cls)

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
                for _, t, v in self.fast_pygments_lexer.get_tokens_unprocessed(text):
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
