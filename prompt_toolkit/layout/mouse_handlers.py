from __future__ import unicode_literals

from collections import defaultdict

__all__ = (
    'MouseHandlers',
)


class _Rect:
    """
    Internal rectangle class for efficient mouse handler regions.
    """
    def __init__(self, x_min, x_max, y_min, y_max, handler):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.handler = handler
    
    def contains(self, x, y):
        """
        Check if the point (x, y) is within this rectangle.
        """
        return (self.x_min <= x < self.x_max and 
                self.y_min <= y < self.y_max)


class RectDict:
    """
    Dictionary-like class that efficiently stores rectangle regions and their handlers.
    """
    def __init__(self, default_factory):
        self._default_factory = default_factory
        self._default_value = default_factory()
        self._rects = []
        
    def __getitem__(self, key):
        """
        Get handler for a specific (x, y) position.
        """
        x, y = key
        
        # Check through rectangles in order (most recently added first)
        for rect in self._rects:
            if rect.contains(x, y):
                return rect.handler
                
        # Return default value if no rectangle contains this point
        return self._default_value
    
    def __setitem__(self, key, value):
        """
        For individual points (legacy support and special cases)
        """
        x, y = key
        # Create a 1x1 rectangle for this point
        rect = _Rect(x, x+1, y, y+1, value)
        self._rects.insert(0, rect)


class MouseHandlers(object):
    """
    Two dimentional raster of callbacks for mouse events.
    """
    def __init__(self):
        def dummy_callback(cli, mouse_event):
            """
            :param mouse_event: `MouseEvent` instance.
            """

        # Map (x,y) tuples to handlers using our optimized RectDict
        self.mouse_handlers = RectDict(lambda: dummy_callback)

    def set_mouse_handler_for_range(self, x_min, x_max, y_min, y_max, handler=None):
        """
        Set mouse handler for a region.
        """
        # Add rectangle directly to the RectDict's internal rect list - O(1) operation
        rect = _Rect(x_min, x_max, y_min, y_max, handler)
        self.mouse_handlers._rects.insert(0, rect)
