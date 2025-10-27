"""
Shared types for completion system.

Extracted to avoid circular imports between completer.py and bash_completer.py.
"""
from collections import namedtuple

__all__ = ('Candidate', 'CacheInfo')


class Candidate:
    """
    Completion candidate with all metadata.

    Handles smart defaults:
    - display defaults to name
    - match_text defaults to name
    """
    __slots__ = ('name', 'priority', 'is_dir', 'is_text_file', '_display', 'display_meta', 'display_style', '_match_text')

    def __init__(self, name, priority=0, is_dir=None, is_text_file=None,
                 display=None, display_meta=None, display_style=None, match_text=None):
        self.name = name
        self.priority = priority
        self.is_dir = is_dir
        self.is_text_file = is_text_file
        self._display = display
        self.display_meta = display_meta
        self.display_style = display_style
        self._match_text = match_text

    @property
    def display(self):
        """Display text in menu (defaults to name)."""
        return self._display if self._display is not None else self.name

    @property
    def match_text(self):
        """Text to fuzzy match against (defaults to name)."""
        return self._match_text if self._match_text is not None else self.name

    def __repr__(self):
        return 'Candidate({!r}, priority={})'.format(self.name, self.priority)


# Cache key info for a document
CacheInfo = namedtuple('CacheInfo', ['cache_text', 'cache_pos', 'origin', 'name_origin'])
CacheInfo.__doc__ = """Cache key info for a document."""
