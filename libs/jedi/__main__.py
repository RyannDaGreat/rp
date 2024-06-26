import sys
from os.path import join, dirname, abspath, isdir


def _start_linter():
    """
    This is a pre-alpha API. You're not supposed to use it at all, except for
    testing. It will very likely change.
    """
    import rp.libs.jedi

    if '--debug' in sys.argv:
        rp.libs.jedi.set_debug_function()

    for path in sys.argv[2:]:
        if path.startswith('--'):
            continue
        if isdir(path):
            import fnmatch
            import os

            paths = []
            for root, dirnames, filenames in os.walk(path):
                for filename in fnmatch.filter(filenames, '*.py'):
                    paths.append(os.path.join(root, filename))
        else:
            paths = [path]

        try:
            for path in paths:
                for error in rp.libs.jedi.Script(path=path)._analysis():
                    print(error)
        except Exception:
            if '--pdb' in sys.argv:
                import traceback
                traceback.print_exc()
                import pdb
                pdb.post_mortem()
            else:
                raise


if len(sys.argv) == 2 and sys.argv[1] == 'repl':
    # don't want to use __main__ only for repl yet, maybe we want to use it for
    # something else. So just use the keyword ``repl`` for now.
    print(join(dirname(abspath(__file__)), 'api', 'replstartup.py'))
elif len(sys.argv) > 1 and sys.argv[1] == 'linter':
    _start_linter()
