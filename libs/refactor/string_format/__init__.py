#!/usr/bin/env python3.10
"""
Python string format conversion utilities.

This module provides functions to convert between different Python string formatting styles:
- Convert str.format() expressions to f-strings
- Convert f-strings to str.format() expressions

Examples:
    # Convert str.format() expressions to f-strings
    >>> from rp.libs.refactorings.string_format import format_to_fstring
    >>> code = 'print("Hello, {0}!".format(name))'
    >>> format_to_fstring(code)
    'print(f"Hello, {name}!")'

    # Convert f-strings to str.format() expressions
    >>> from rp.libs.refactorings.string_format import fstring_to_format
    >>> code = 'print(f"Hello, {name}!")'
    >>> fstring_to_format(code)
    'print("Hello, {0}!".format(name))'

Written with Claude-Code May 16 2025
"""

from .format_to_fstring_converter import convert_string as format_to_fstring
from .fstring_converter import convert_string as fstring_to_format

__all__ = ["format_to_fstring", "fstring_to_format"]


def format_to_fstring(code: str) -> str:
    """
    Convert str.format() expressions in Python code to f-strings.

    Args:
        code: Python code as a string

    Returns:
        Code with str.format() expressions converted to f-strings

    Examples:
        >>> format_to_fstring('print("Hello, {0}!".format(name))')
        'print(f"Hello, {name}!")'
        
        >>> format_to_fstring('print("Value: {0:.2f}".format(value))')
        'print(f"Value: {value:.2f}")'
    """
    return format_to_fstring(code)


def fstring_to_format(code: str) -> str:
    """
    Convert f-strings in Python code to str.format() expressions.

    Args:
        code: Python code as a string

    Returns:
        Code with f-strings converted to str.format() expressions

    Examples:
        >>> fstring_to_format('print(f"Hello, {name}!")')
        'print("Hello, {0}!".format(name))'
        
        >>> fstring_to_format('print(f"Value: {value:.2f}")')
        'print("Value: {0:.2f}".format(value))'
    """
    return fstring_to_format(code)
