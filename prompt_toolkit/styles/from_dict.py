"""
Tool for creating styles from a dictionary.

This is very similar to the Pygments style dictionary, with some additions:
- Support for reverse and blink.
- Support for ANSI color names. (These will map directly to the 16 terminal
  colors.)
"""
try:
    from collections.abc import Mapping #Python 3.9 and below
except ImportError:
    from collections import Mapping #Python 3.10+

from .base import Style, DEFAULT_ATTRS, NONE_ATTRS, ANSI_COLOR_NAMES
from .defaults import DEFAULT_STYLE_EXTENSIONS
from .utils import merge_attrs, split_token_in_parts
from six.moves import range

__all__ = (
    'style_from_dict',
)


def _colorformat(text):
    """
    Parse/validate color format.

    Like in Pygments, but also support the ANSI color names.
    (These will map to the colors of the 16 color palette.)

    Returns tuple (color, alpha) where alpha is 0.0-1.0 (default 1.0).
    Supports #RRGGBBAA format for colors with alpha.
    """
    if text[0:1] == '#':
        col = text[1:]
        if col in ANSI_COLOR_NAMES:
            return (col, 1.0)
        elif len(col) == 8:
            # #RRGGBBAA format
            color = col[:6]
            alpha = int(col[6:8], 16) / 255.0
            return (color, alpha)
        elif len(col) == 6:
            return (col, 1.0)
        elif len(col) == 3:
            return (col[0]*2 + col[1]*2 + col[2]*2, 1.0)
    elif text == '':
        return (text, 1.0)

    raise ValueError('Wrong color format %r' % text)


def style_from_dict(style_dict, include_defaults=True):
    """
    Create a ``Style`` instance from a dictionary or other mapping.

    The dictionary is equivalent to the ``Style.styles`` dictionary from
    pygments, with a few additions: it supports 'reverse' and 'blink'.

    Usage::

        style_from_dict({
            Token: '#ff0000 bold underline',
            Token.Title: 'blink',
            Token.SomethingElse: 'reverse',
        })

    :param include_defaults: Include the defaults (built-in) styling for
        selected text, etc...)
    """
    assert isinstance(style_dict, Mapping)

    if include_defaults:
        s2 = {}
        s2.update(DEFAULT_STYLE_EXTENSIONS)
        s2.update(style_dict)
        style_dict = s2

    # Expand token inheritance and turn style description into Attrs.
    token_to_attrs = {}

    # (Loop through the tokens in order. Sorting makes sure that
    # we process the parent first.)
    for ttype, styledef in sorted(style_dict.items()):
        # Start from NONE_ATTRS so only specified attributes are set
        attrs = NONE_ATTRS

        if 'noinherit' not in styledef:
            for i in range(1, len(ttype) + 1):
                try:
                    attrs = token_to_attrs[ttype[:-i]]
                except KeyError:
                    pass
                else:
                    break

        # Now update with the given attributes.
        for part in styledef.split():
            if part == 'noinherit':
                pass
            elif part == 'bold':
                attrs = attrs._replace(bold=True)
            elif part == 'nobold':
                attrs = attrs._replace(bold=False)
            elif part == 'italic':
                attrs = attrs._replace(italic=True)
            elif part == 'noitalic':
                attrs = attrs._replace(italic=False)
            elif part == 'underline':
                attrs = attrs._replace(underline=True)
            elif part == 'nounderline':
                attrs = attrs._replace(underline=False)

            # prompt_toolkit extensions. Not in Pygments.
            elif part == 'blink':
                attrs = attrs._replace(blink=True)
            elif part == 'noblink':
                attrs = attrs._replace(blink=False)
            elif part == 'reverse':
                attrs = attrs._replace(reverse=True)
            elif part == 'noreverse':
                attrs = attrs._replace(reverse=False)
            elif part == 'undercurl':
                attrs = attrs._replace(undercurl=True)
            elif part == 'noundercurl':
                attrs = attrs._replace(undercurl=False)

            # Additional fansi-compatible styles
            elif part in ('faded', 'dim'):
                attrs = attrs._replace(faded=True)
            elif part in ('nofaded', 'nodim'):
                attrs = attrs._replace(faded=False)
            elif part == 'fastblink':
                attrs = attrs._replace(fastblink=True)
            elif part == 'nofastblink':
                attrs = attrs._replace(fastblink=False)
            elif part == 'hide':
                attrs = attrs._replace(hide=True)
            elif part == 'nohide':
                attrs = attrs._replace(hide=False)
            elif part == 'strike':
                attrs = attrs._replace(strike=True)
            elif part == 'nostrike':
                attrs = attrs._replace(strike=False)
            elif part == 'overlined':
                attrs = attrs._replace(overlined=True)
            elif part == 'nooverlined':
                attrs = attrs._replace(overlined=False)
            elif part == 'underdouble':
                attrs = attrs._replace(underdouble=True)
            elif part == 'nounderdouble':
                attrs = attrs._replace(underdouble=False)
            elif part == 'underdots':
                attrs = attrs._replace(underdots=True)
            elif part == 'nounderdots':
                attrs = attrs._replace(underdots=False)
            elif part == 'underdash':
                attrs = attrs._replace(underdash=True)
            elif part == 'nounderdash':
                attrs = attrs._replace(underdash=False)

            # Pygments properties that we ignore.
            elif part in ('roman', 'sans', 'mono'):
                pass
            elif part.startswith('border:'):
                pass

            # Colors.

            elif part.startswith('fg:'):
                color, color_alpha = _colorformat(part[3:])
                attrs = attrs._replace(color=color, color_alpha=color_alpha)
            elif part.startswith('bg:'):
                bgcolor, bgcolor_alpha = _colorformat(part[3:])
                attrs = attrs._replace(bgcolor=bgcolor, bgcolor_alpha=bgcolor_alpha)
            elif part.startswith('underline_color:'):
                ucolor, _ = _colorformat(part[16:])
                attrs = attrs._replace(underline_color=ucolor)
            else:
                color, color_alpha = _colorformat(part)
                attrs = attrs._replace(color=color, color_alpha=color_alpha)

        token_to_attrs[ttype] = attrs

    return _StyleFromDict(token_to_attrs)


class _StyleFromDict(Style):
    """
    Turn a dictionary that maps `Token` to `Attrs` into a style class.

    :param token_to_attrs: Dictionary that maps `Token` to `Attrs`.
    """
    def __init__(self, token_to_attrs):
        self.token_to_attrs = token_to_attrs

    def get_attrs_for_token(self, token):
        # Split Token.
        list_of_attrs = []
        for token in split_token_in_parts(token):
            list_of_attrs.append(self.token_to_attrs.get(token, DEFAULT_ATTRS))
        return merge_attrs(list_of_attrs)

    def invalidation_hash(self):
        return id(self.token_to_attrs)
