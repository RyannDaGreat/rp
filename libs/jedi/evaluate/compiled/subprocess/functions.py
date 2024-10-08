from __future__ import print_function
import sys
import os

from rp.libs.jedi._compatibility import find_module, cast_path, force_unicode, \
    iter_modules, all_suffixes
from rp.libs.jedi.evaluate.compiled import access
from rp.libs.jedi import parser_utils


def get_sys_path():
    return list(map(cast_path, sys.path))


def load_module(evaluator, **kwargs):
    return access.load_module(evaluator, **kwargs)


def get_compiled_method_return(evaluator, id, attribute, *args, **kwargs):
    handle = evaluator.compiled_subprocess.get_access_handle(id)
    #RYAN MOD: Catch all annoying warnings from libraries that warn that certain things are deprecated....I DONT CARE
    import warnings
    with warnings.catch_warnings():
        output = getattr(handle.access, attribute)(*args, **kwargs)
    return output


def create_simple_object(evaluator, obj):
    return access.create_access_path(evaluator, obj)


def get_module_info(evaluator, sys_path=None, full_name=None, **kwargs):
    """
    Returns Tuple[Union[NamespaceInfo, FileIO, None], Optional[bool]]
    """
    if sys_path is not None:
        sys.path, temp = sys_path, sys.path
    try:
        return find_module(full_name=full_name, **kwargs)
    except ImportError:
        return None, None
    finally:
        if sys_path is not None:
            sys.path = temp


def list_module_names(evaluator, search_path):
    return [
        force_unicode(name)
        for module_loader, name, is_pkg in iter_modules(search_path)
    ]


def get_builtin_module_names(evaluator):
    return list(map(force_unicode, sys.builtin_module_names))


def _test_raise_error(evaluator, exception_type):
    """
    Raise an error to simulate certain problems for unit tests.
    """
    raise exception_type


def _test_print(evaluator, stderr=None, stdout=None):
    """
    Force some prints in the subprocesses. This exists for unit tests.
    """
    if stderr is not None:
        print(stderr, file=sys.stderr)
        sys.stderr.flush()
    if stdout is not None:
        print(stdout)
        sys.stdout.flush()


def _get_init_path(directory_path):
    """
    The __init__ file can be searched in a directory. If found return it, else
    None.
    """
    for suffix in all_suffixes():
        path = os.path.join(directory_path, '__init__' + suffix)
        if os.path.exists(path):
            return path
    return None


def safe_literal_eval(evaluator, value):
    return parser_utils.safe_literal_eval(value)
