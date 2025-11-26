from __future__ import unicode_literals
from .base import DEFAULT_ATTRS, Attrs

__all__ = (
    'split_token_in_parts',
    'merge_attrs',
)


def _blend_colors(fg_color, fg_alpha, bg_color):
    """
    Blend foreground color with background color using alpha compositing.

    :param fg_color: Foreground color as hex string (e.g., 'ff0000')
    :param fg_alpha: Alpha value 0.0-1.0 (1.0 = opaque)
    :param bg_color: Background color as hex string (e.g., '0000ff')
    :return: Blended color as hex string
    """
    if fg_alpha >= 1.0 or bg_color is None:
        return fg_color
    if fg_color is None:
        return bg_color

    # Handle ANSI color names - don't blend them
    if not fg_color.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')):
        return fg_color
    if not bg_color.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')):
        return fg_color

    # Convert hex to RGB
    fr = int(fg_color[0:2], 16)
    fg = int(fg_color[2:4], 16)
    fb = int(fg_color[4:6], 16)

    br = int(bg_color[0:2], 16)
    bg = int(bg_color[2:4], 16)
    bb = int(bg_color[4:6], 16)

    # Alpha blend: result = fg * alpha + bg * (1 - alpha)
    r = int(fr * fg_alpha + br * (1 - fg_alpha))
    g = int(fg * fg_alpha + bg * (1 - fg_alpha))
    b = int(fb * fg_alpha + bb * (1 - fg_alpha))

    # Convert back to hex
    return '{:02x}{:02x}{:02x}'.format(r, g, b)


def split_token_in_parts(token):
    """
    Take a Token, and turn it in a list of tokens, by splitting
    it on ':' (taking that as a separator.)
    """
    result = []
    current = []
    for part in token + (':', ):
        if part == ':':
            if current:
                result.append(tuple(current))
                current = []
        else:
            current.append(part)

    return result


def merge_attrs(list_of_attrs):
    """
    Take a list of :class:`.Attrs` instances and merge them into one.
    Every `Attr` in the list can override the styling of the previous one.

    Uses proper None-checking to ensure that None values don't override
    existing values (allowing proper style layering). Supports alpha blending
    for colors with alpha < 1.0.
    """
    result = DEFAULT_ATTRS

    for attr in list_of_attrs:
        # Determine new color value (with potential alpha blending)
        new_color = result.color
        new_color_alpha = result.color_alpha
        if attr.color is not None:
            if attr.color_alpha < 1.0:
                # Alpha blend with previous color
                new_color = _blend_colors(attr.color, attr.color_alpha, result.color)
                new_color_alpha = 1.0  # Result is fully opaque after blending
            else:
                new_color = attr.color
                new_color_alpha = attr.color_alpha

        # Determine new bgcolor value (with potential alpha blending)
        new_bgcolor = result.bgcolor
        new_bgcolor_alpha = result.bgcolor_alpha
        if attr.bgcolor is not None:
            if attr.bgcolor_alpha < 1.0:
                # Alpha blend with previous bgcolor
                new_bgcolor = _blend_colors(attr.bgcolor, attr.bgcolor_alpha, result.bgcolor)
                new_bgcolor_alpha = 1.0  # Result is fully opaque after blending
            else:
                new_bgcolor = attr.bgcolor
                new_bgcolor_alpha = attr.bgcolor_alpha

        result = Attrs(
            color=new_color,
            bgcolor=new_bgcolor,
            bold=attr.bold if attr.bold is not None else result.bold,
            underline=attr.underline if attr.underline is not None else result.underline,
            italic=attr.italic if attr.italic is not None else result.italic,
            blink=attr.blink if attr.blink is not None else result.blink,
            reverse=attr.reverse if attr.reverse is not None else result.reverse,
            color_alpha=new_color_alpha,
            bgcolor_alpha=new_bgcolor_alpha,
            undercurl=attr.undercurl if attr.undercurl is not None else result.undercurl,
            underline_color=attr.underline_color if attr.underline_color is not None else result.underline_color,
            faded=attr.faded if attr.faded is not None else result.faded,
            fastblink=attr.fastblink if attr.fastblink is not None else result.fastblink,
            hide=attr.hide if attr.hide is not None else result.hide,
            strike=attr.strike if attr.strike is not None else result.strike,
            overlined=attr.overlined if attr.overlined is not None else result.overlined,
            underdouble=attr.underdouble if attr.underdouble is not None else result.underdouble,
            underdots=attr.underdots if attr.underdots is not None else result.underdots,
            underdash=attr.underdash if attr.underdash is not None else result.underdash)

    return result
