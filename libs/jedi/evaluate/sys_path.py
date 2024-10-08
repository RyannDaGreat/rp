import os

from rp.libs.jedi._compatibility import unicode, force_unicode, all_suffixes
from rp.libs.jedi.evaluate.cache import evaluator_method_cache
from rp.libs.jedi.evaluate.base_context import ContextualizedNode
from rp.libs.jedi.evaluate.helpers import is_string
from rp.libs.jedi.common.utils import traverse_parents
from rp.libs.jedi.parser_utils import get_cached_code_lines
from rp.libs.jedi.file_io import FileIO
from rp.libs.jedi import settings
from rp.libs.jedi import debug


def _abs_path(module_context, path):
    if os.path.isabs(path):
        return path

    module_path = module_context.py__file__()
    if module_path is None:
        # In this case we have no idea where we actually are in the file
        # system.
        return None

    base_dir = os.path.dirname(module_path)
    path = force_unicode(path)
    return os.path.abspath(os.path.join(base_dir, path))


def _paths_from_assignment(module_context, expr_stmt):
    """
    Extracts the assigned strings from an assignment that looks as follows::

        sys.path[0:0] = ['module/path', 'another/module/path']

    This function is in general pretty tolerant (and therefore 'buggy').
    However, it's not a big issue usually to add more paths to Jedi's sys_path,
    because it will only affect Jedi in very random situations and by adding
    more paths than necessary, it usually benefits the general user.
    """
    for assignee, operator in zip(expr_stmt.children[::2], expr_stmt.children[1::2]):
        try:
            assert operator in ['=', '+=']
            assert assignee.type in ('power', 'atom_expr') and \
                len(assignee.children) > 1
            c = assignee.children
            assert c[0].type == 'name' and c[0].value == 'sys'
            trailer = c[1]
            assert trailer.children[0] == '.' and trailer.children[1].value == 'path'
            # TODO Essentially we're not checking details on sys.path
            # manipulation. Both assigment of the sys.path and changing/adding
            # parts of the sys.path are the same: They get added to the end of
            # the current sys.path.
            """
            execution = c[2]
            assert execution.children[0] == '['
            subscript = execution.children[1]
            assert subscript.type == 'subscript'
            assert ':' in subscript.children
            """
        except AssertionError:
            continue

        cn = ContextualizedNode(module_context.create_context(expr_stmt), expr_stmt)
        for lazy_context in cn.infer().iterate(cn):
            for context in lazy_context.infer():
                if is_string(context):
                    abs_path = _abs_path(module_context, context.get_safe_value())
                    if abs_path is not None:
                        yield abs_path


def _paths_from_list_modifications(module_context, trailer1, trailer2):
    """ extract the path from either "sys.path.append" or "sys.path.insert" """
    # Guarantee that both are trailers, the first one a name and the second one
    # a function execution with at least one param.
    if not (trailer1.type == 'trailer' and trailer1.children[0] == '.'
            and trailer2.type == 'trailer' and trailer2.children[0] == '('
            and len(trailer2.children) == 3):
        return

    name = trailer1.children[1].value
    if name not in ['insert', 'append']:
        return
    arg = trailer2.children[1]
    if name == 'insert' and len(arg.children) in (3, 4):  # Possible trailing comma.
        arg = arg.children[2]

    for context in module_context.create_context(arg).eval_node(arg):
        if is_string(context):
            abs_path = _abs_path(module_context, context.get_safe_value())
            if abs_path is not None:
                yield abs_path


@evaluator_method_cache(default=[])
def check_sys_path_modifications(module_context):
    """
    Detect sys.path modifications within module.
    """
    def get_sys_path_powers(names):
        for name in names:
            power = name.parent.parent
            if power is not None and power.type in ('power', 'atom_expr'):
                c = power.children
                if c[0].type == 'name' and c[0].value == 'sys' \
                        and c[1].type == 'trailer':
                    n = c[1].children[1]
                    if n.type == 'name' and n.value == 'path':
                        yield name, power

    if module_context.tree_node is None:
        return []

    added = []
    try:
        possible_names = module_context.tree_node.get_used_names()['path']
    except KeyError:
        pass
    else:
        for name, power in get_sys_path_powers(possible_names):
            expr_stmt = power.parent
            if len(power.children) >= 4:
                added.extend(
                    _paths_from_list_modifications(
                        module_context, *power.children[2:4]
                    )
                )
            elif expr_stmt is not None and expr_stmt.type == 'expr_stmt':
                added.extend(_paths_from_assignment(module_context, expr_stmt))
    return added


def discover_buildout_paths(evaluator, script_path):
    buildout_script_paths = set()

    for buildout_script_path in _get_buildout_script_paths(script_path):
        for path in _get_paths_from_buildout_script(evaluator, buildout_script_path):
            buildout_script_paths.add(path)

    return buildout_script_paths


def _get_paths_from_buildout_script(evaluator, buildout_script_path):
    file_io = FileIO(buildout_script_path)
    try:
        module_node = evaluator.parse(
            file_io=file_io,
            cache=True,
            cache_path=settings.cache_directory
        )
    except IOError:
        debug.warning('Error trying to read buildout_script: %s', buildout_script_path)
        return

    from rp.libs.jedi.evaluate.context import ModuleContext
    module = ModuleContext(
        evaluator, module_node, file_io,
        string_names=None,
        code_lines=get_cached_code_lines(evaluator.grammar, buildout_script_path),
    )
    for path in check_sys_path_modifications(module):
        yield path


def _get_parent_dir_with_file(path, filename):
    for parent in traverse_parents(path):
        if os.path.isfile(os.path.join(parent, filename)):
            return parent
    return None


def _get_buildout_script_paths(search_path):
    """
    if there is a 'buildout.cfg' file in one of the parent directories of the
    given module it will return a list of all files in the buildout bin
    directory that look like python files.

    :param search_path: absolute path to the module.
    :type search_path: str
    """
    project_root = _get_parent_dir_with_file(search_path, 'buildout.cfg')
    if not project_root:
        return
    bin_path = os.path.join(project_root, 'bin')
    if not os.path.exists(bin_path):
        return

    for filename in os.listdir(bin_path):
        try:
            filepath = os.path.join(bin_path, filename)
            with open(filepath, 'r') as f:
                firstline = f.readline()
                if firstline.startswith('#!') and 'python' in firstline:
                    yield filepath
        except (UnicodeDecodeError, IOError) as e:
            # Probably a binary file; permission error or race cond. because
            # file got deleted. Ignore it.
            debug.warning(unicode(e))
            continue


def remove_python_path_suffix(path):
    for suffix in all_suffixes():
        if path.endswith(suffix):
            path = path[:-len(suffix)]
            break
    return path


def transform_path_to_dotted(sys_path, module_path):
    """
    Returns the dotted path inside a sys.path as a list of names. e.g.

    >>> from os.path import abspath
    >>> transform_path_to_dotted([abspath("/foo")], abspath('/foo/bar/baz.py'))
    (('bar', 'baz'), False)

    Returns (None, False) if the path doesn't really resolve to anything.
    The second return part is if it is a package.
    """
    # First remove the suffix.
    module_path = remove_python_path_suffix(module_path)

    # Once the suffix was removed we are using the files as we know them. This
    # means that if someone uses an ending like .vim for a Python file, .vim
    # will be part of the returned dotted part.

    is_package = module_path.endswith(os.path.sep + '__init__')
    if is_package:
        # -1 to remove the separator
        module_path = module_path[:-len('__init__') - 1]

    def iter_potential_solutions():
        for p in sys_path:
            if module_path.startswith(p):
                # Strip the trailing slash/backslash
                rest = module_path[len(p):]
                # On Windows a path can also use a slash.
                if rest.startswith(os.path.sep) or rest.startswith('/'):
                    # Remove a slash in cases it's still there.
                    rest = rest[1:]

                if rest:
                    split = rest.split(os.path.sep)
                    if not all(split):
                        # This means that part of the file path was empty, this
                        # is very strange and is probably a file that is called
                        # `.py`.
                        return
                    yield tuple(split)

    potential_solutions = tuple(iter_potential_solutions())
    if not potential_solutions:
        return None, False
    # Try to find the shortest path, this makes more sense usually, because the
    # user usually has venvs somewhere. This means that a path like
    # .tox/py37/lib/python3.7/os.py can be normal for a file. However in that
    # case we definitely want to return ['os'] as a path and not a crazy
    # ['.tox', 'py37', 'lib', 'python3.7', 'os']. Keep in mind that this is a
    # heuristic and there's now ay to "always" do it right.
    return sorted(potential_solutions, key=lambda p: len(p))[0], is_package
