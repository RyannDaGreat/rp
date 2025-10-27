"""
Jedi completion utilities for rp's pseudo terminal.

This module contains all Jedi-specific logic for generating completions
and metadata, separated from the main completer for clarity.
"""
from __future__ import unicode_literals
from collections import namedtuple
import rp

__all__ = ['JediInfo', 'get_jedi_interpreter', 'get_jedi_display_meta', 'format_jedi_value_description']

JediInfo = namedtuple('JediInfo', ['interpreter', 'line', 'column'])
JediInfo.__doc__ = """Jedi interpreter with position info."""


def truncate_with_ellipsis(text, max_len):
    """Truncate text to max_len, appending '...' if truncated."""
    if len(text) > max_len:
        return text[:max_len] + '...'
    return text


def format_jedi_value_description(value, class_name):
    """
    Format runtime value into useful display metadata for Jedi completions.
    Uses rp's type checkers to avoid importing packages.

    Returns:
        String with value details (e.g., 'list[5]', 'ndarray(3x224x224) float32', 'str = "hello"')
    """
    try:
        # Numpy arrays: show shape and dtype
        if rp.is_numpy_array(value):
            shape_str = 'x'.join(str(d) for d in value.shape)
            return 'ndarray(%s) %s' % (shape_str, value.dtype)

        # Torch tensors: show shape, dtype, and device
        if rp.is_torch_tensor(value):
            shape_str = 'x'.join(str(d) for d in value.shape)
            dtype_str = str(value.dtype).replace('torch.', '')
            device_str = str(value.device)
            return 'Tensor(%s) %s on %s' % (shape_str, dtype_str, device_str)

        # PIL Images: show size and mode
        if rp.is_image(value) and hasattr(value, 'size') and hasattr(value, 'mode'):
            return 'Image %dx%d %s' % (value.size[0], value.size[1], value.mode)

        # Pandas DataFrames: show shape
        if class_name == 'DataFrame' and hasattr(value, 'shape'):
            return 'DataFrame(%dx%d)' % (value.shape[0], value.shape[1])

        # Pandas Series: show length and dtype
        if class_name == 'Series' and hasattr(value, 'shape') and hasattr(value, 'dtype'):
            return 'Series[%d] %s' % (value.shape[0], value.dtype)

        # Lists/tuples: show length and first few items
        if class_name in ('list', 'tuple'):
            length = len(value)
            if length == 0:
                return '%s[0]' % class_name
            elif length <= 3:
                items = ', '.join(repr(v) for v in value)
                return '%s[%d]: [%s]' % (class_name, length, truncate_with_ellipsis(items, 100))
            else:
                return '%s[%d]' % (class_name, length)

        # Dicts: show length and sample keys
        if class_name == 'dict':
            length = len(value)
            if length == 0:
                return 'dict[0]'
            elif length <= 3:
                keys = ', '.join(repr(k) for k in list(value.keys())[:3])
                return 'dict[%d]: {%s}' % (length, truncate_with_ellipsis(keys, 100))
            else:
                return 'dict[%d]' % length

        # Sets: show length
        if class_name == 'set':
            return 'set[%d]' % len(value)

        # Strings: show actual value
        if class_name == 'str':
            return 'str = ' + truncate_with_ellipsis(repr(value), 150)

        # Numbers/bools: show actual value
        if class_name in ('int', 'float', 'bool', 'complex'):
            return '%s = %s' % (class_name, repr(value))

        # Bytes: show length and preview
        if class_name == 'bytes':
            if len(value) <= 20:
                return 'bytes = ' + repr(value)
            else:
                return 'bytes[%d] = %s...' % (len(value), repr(value[:20]))

        # None
        if class_name == 'NoneType':
            return 'None'

    except:
        pass

    # Fallback: just return class name
    return class_name


def get_jedi_display_meta(jc, globals_dict=None, locals_dict=None):
    """
    Generate detailed display_meta from Jedi completion.

    Args:
        jc: Jedi completion object
        globals_dict: Global namespace (to get actual values)
        locals_dict: Local namespace (to get actual values)

    Returns:
        String with detailed type info (e.g., 'Func: print(x, y)', 'Object: int = 42', 'Module: sys')
    """
    MAX_META_LENGTH = 200
    jtype = jc.type

    # Functions: show signature
    if jtype == 'function':
        try:
            sigs = jc.get_signatures()
            if sigs:
                sig_str = sigs[0].to_string()
                return 'Func: ' + truncate_with_ellipsis(sig_str, MAX_META_LENGTH - 6)
        except:
            pass
        return 'Func'

    # Modules: show module path
    if jtype == 'module':
        try:
            module_path = rp.get_module_path_from_name(jc.full_name)
            if module_path:
                # Make relative to home
                import os
                if module_path.startswith(os.path.expanduser('~')):
                    module_path = '~' + module_path[len(os.path.expanduser('~')):]
                return 'Module: ' + truncate_with_ellipsis(module_path, MAX_META_LENGTH - 8)
        except:
            pass
        return 'Module: ' + jc.full_name

    # Instances or statements: show class name and value details
    if jtype in ('instance', 'statement'):
        try:
            inferred = jc.infer()
            if inferred:
                class_name = inferred[0].name
                # Try to get value using full_name
                value = None
                try:
                    value = eval(jc.full_name, globals_dict or {}, locals_dict or {})
                except:
                    pass

                # Format the value if we have it
                if value is not None:
                    value_info = format_jedi_value_description(value, class_name)
                    return 'Object: ' + value_info

                # No value, just show class name
                if class_name and class_name != jc.name:
                    return 'Object: ' + class_name
        except:
            pass
        return 'Object'

    # Classes: show __init__ signature
    if jtype == 'class':
        try:
            sigs = jc.get_signatures()
            if sigs:
                sig_str = sigs[0].to_string()
                return 'Class: ' + truncate_with_ellipsis(sig_str, MAX_META_LENGTH - 7)
        except:
            pass
        # Fallback: show if builtin
        try:
            if jc.module_name in ('builtins', '__builtin__'):
                return 'Class: builtin'
        except:
            pass
        return 'Class'

    # Params, keywords, etc.
    return jtype.capitalize()


def _get_module_being_completed(code, cursor_pos):
    """
    Extract the module name being completed (e.g., 'torch' from 'torch.nn.').

    Returns module name or None if not completing on a module attribute.
    """
    import re

    # Get text before cursor
    text_before = code[:cursor_pos]

    # Match pattern like "module_name." at the end
    # This catches: torch., numpy.linalg., sys.path., etc.
    match = re.search(r'([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\.$', text_before)
    if match:
        full_path = match.group(1)
        # Return the root module name (first part)
        return full_path.split('.')[0]

    return None


def get_jedi_interpreter(code, cursor_pos, globals_dict, locals_dict, allow_dynamic_imports=False):
    """
    Get Jedi Interpreter for the given code.

    Args:
        code: The Python code string
        cursor_pos: The cursor position in the code
        globals_dict: Global namespace dictionary
        locals_dict: Local namespace dictionary
        allow_dynamic_imports: When False, prevent Jedi from importing unloaded modules (default: False)

    Returns:
        JediInfo with interpreter, line, column

    Raises:
        ValueError: If completing on an unimported module and allow_dynamic_imports is False
    """
    import jedi
    import sys

    # Check if we're completing on a module that hasn't been imported yet
    # This prevents Jedi from doing slow imports (especially on NFS)
    if not allow_dynamic_imports:
        module_name = _get_module_being_completed(code, cursor_pos)
        if module_name:
            # Check if module is in the runtime namespaces or already imported
            in_namespace = module_name in globals_dict or module_name in locals_dict
            in_sys_modules = module_name in sys.modules

            if not in_namespace and not in_sys_modules:
                # Module not imported yet - don't let Jedi import it
                raise ValueError("Module '{0}' not imported yet - refusing to import for completion".format(module_name))

    # Compute line and column from cursor position
    line = code.count("\n", 0, cursor_pos) + 1
    column = cursor_pos - code.rfind("\n", 0, cursor_pos) - 1

    # Create an Interpreter for runtime-like completions
    interpreter = jedi.Interpreter(code, namespaces=[globals_dict, locals_dict])

    return JediInfo(interpreter=interpreter, line=line, column=column)
