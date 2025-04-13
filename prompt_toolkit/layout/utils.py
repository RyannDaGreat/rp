from __future__ import unicode_literals

from rp.prompt_toolkit.utils import get_cwidth
from rp.prompt_toolkit.token import Token

__all__ = (
    'token_list_len',
    'token_list_width',
    'token_list_to_text',
    'explode_tokens',
    'split_lines',
    'find_window_for_buffer_name',
)


def token_list_len(tokenlist):
    """
    Return the amount of characters in this token list.

    :param tokenlist: List of (token, text) or (token, text, mouse_handler)
                      tuples.
    """
    ZeroWidthEscape = Token.ZeroWidthEscape
    return sum(len(item[1]) for item in tokenlist if item[0] != ZeroWidthEscape)


def token_list_width(tokenlist):
    """
    Return the character width of this token list.
    (Take double width characters into account.)

    :param tokenlist: List of (token, text) or (token, text, mouse_handler)
                      tuples.
    """
    ZeroWidthEscape = Token.ZeroWidthEscape
    return sum(get_cwidth(c) for item in tokenlist for c in item[1] if item[0] != ZeroWidthEscape)


def token_list_to_text(tokenlist):
    """
    Concatenate all the text parts again.
    """
    ZeroWidthEscape = Token.ZeroWidthEscape
    try:
        return ''.join(item[1] for item in tokenlist if item[0] != ZeroWidthEscape)
    except TypeError:
        return ''
# r.print_stack_trace: ERROR: Traceback (most recent call last):
#   File "/usr/local/lib/python3.7/site-packages/rp/r.py", line 4496, in python_input
#     code_obj = Đ_python_input_eventloop.run()
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/interface.py", line 415, in run
#     self.eventloop.run(self.input, self.create_eventloop_callbacks())
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/eventloop/posix.py", line 159, in run
#     t()
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/interface.py", line 333, in redraw
#     self._redraw()
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/interface.py", line 358, in _redraw
#     self.renderer.render(self, self.layout, is_done=self.is_done)
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/renderer.py", line 436, in render
#     extended_height=size.rows,
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/layout/containers.py", line 157, in write_to_screen
#     c.write_to_screen(cli, screen, mouse_handlers, WritePosition(xpos, ypos, width, s))
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/layout/containers.py", line 348, in write_to_screen
#     c.write_to_screen(cli, screen, mouse_handlers, WritePosition(xpos, ypos, s, height))
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/layout/containers.py", line 157, in write_to_screen
#     c.write_to_screen(cli, screen, mouse_handlers, WritePosition(xpos, ypos, width, s))
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/layout/containers.py", line 428, in write_to_screen
#     width = fl.content.preferred_width(cli, write_position.width).preferred
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/layout/containers.py", line 1646, in preferred_width
#     return self.content.preferred_width(cli, max_available_width)
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/layout/containers.py", line 980, in preferred_width
#     cli, max_available_width - total_margin_width)
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/layout/controls.py", line 249, in preferred_width
#     text = token_list_to_text(self._get_tokens_cached(cli))
#   File "/usr/local/lib/python3.7/site-packages/rp/prompt_toolkit/layout/utils.py", line 44, in token_list_to_text
#     return ''.join(item[1] for item in tokenlist if item[0] != ZeroWidthEscape)
# TypeError: sequence item 1: expected str instance, NoneType found
# The prompt_toolkit version of pseudo_terminal crashed; reverting to the command-line version... 


def iter_token_lines(tokenlist):
    """
    Iterator that yields tokenlists for each line.
    """
    line = []
    for token, c in explode_tokens(tokenlist):
        line.append((token, c))

        if c == '\n':
            yield line
            line = []

    yield line


def split_lines(tokenlist):
    """
    Take a single list of (Token, text) tuples and yield one such list for each
    line. Just like str.split, this will yield at least one item.

    :param tokenlist: List of (token, text) or (token, text, mouse_handler)
                      tuples.
    """
    try:
        line = []

        for item in tokenlist:
            # For (token, text) tuples.
            if len(item) == 2:
                token, string = item
                try:
                    parts = string.split('\n')
                except:
                    parts=[]

                for part in parts[:-1]:
                    if part:
                        line.append((token, part))
                    yield line
                    line = []

                line.append((token, parts[-1]))
                    # Note that parts[-1] can be empty, and that's fine. It happens
                    # in the case of [(Token.SetCursorPosition, '')].

            # For (token, text, mouse_handler) tuples.
            #     I know, partly copy/paste, but understandable and more efficient
            #     than many tests.
            else:
                token, string, mouse_handler = item
                parts = string.split('\n')

                for part in parts[:-1]:
                    if part:
                        line.append((token, part, mouse_handler))
                    yield line
                    line = []

                line.append((token, parts[-1], mouse_handler))

        # Always yield the last line, even when this is an empty line. This ensures
        # that when `tokenlist` ends with a newline character, an additional empty
        # line is yielded. (Otherwise, there's no way to differentiate between the
        # cases where `tokenlist` does and doesn't end with a newline.)
        yield line
    except:return


class _ExplodedList(list):
    """
    Wrapper around a list, that marks it as 'exploded'.

    As soon as items are added or the list is extended, the new items are
    automatically exploded as well.
    """
    def __init__(self, *a, **kw):
        super(_ExplodedList, self).__init__(*a, **kw)
        self.exploded = True

    def append(self, item):
        self.extend([item])

    def extend(self, lst):
        super(_ExplodedList, self).extend(explode_tokens(lst))

    def insert(self, index, item):
        raise NotImplementedError  # TODO

    # TODO: When creating a copy() or [:], return also an _ExplodedList.

    def __setitem__(self, index, value):
        """
        Ensure that when `(Token, 'long string')` is set, the string will be
        exploded.
        """
        if not isinstance(index, slice):
            index = slice(index, index + 1)
        value = explode_tokens([value])
        super(_ExplodedList, self).__setitem__(index, value)


def explode_tokens(tokenlist):
    """
    Turn a list of (token, text) tuples into another list where each string is
    exactly one character.

    It should be fine to call this function several times. Calling this on a
    list that is already exploded, is a null operation.

    :param tokenlist: List of (token, text) tuples.
    """
    # When the tokenlist is already exploded, don't explode again.
    if getattr(tokenlist, 'exploded', False):
        return tokenlist

    result = []

    for token, string in tokenlist:
        for c in string:
            result.append((token, c))

    return _ExplodedList(result)


def find_window_for_buffer_name(cli, buffer_name):
    """
    Look for a :class:`~prompt_toolkit.layout.containers.Window` in the Layout
    that contains the :class:`~prompt_toolkit.layout.controls.BufferControl`
    for the given buffer and return it. If no such Window is found, return None.
    """
    from rp.prompt_toolkit.interface import CommandLineInterface
    assert isinstance(cli, CommandLineInterface)

    from .containers import Window
    from .controls import BufferControl

    for l in cli.layout.walk(cli):
        if isinstance(l, Window) and isinstance(l.content, BufferControl):
            if l.content.buffer_name == buffer_name:
                return l
