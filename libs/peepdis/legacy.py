from copy import deepcopy
import re
from termcolor import colored
from types import (
    BuiltinMethodType,
    BuiltinFunctionType,
    FunctionType,
    MethodType,
    ModuleType,
)
import sys


def peep(obj, builtins=False, privates=False, docstrings=False,
         truncate_len=250):
    if not isinstance(obj, ModuleType):
        obj = deepcopy(obj)
    obj_dir = dir(obj)
    output = OutputStrWrapper(truncate_len)
    if builtins is False:
        _is_magic = lambda x: (x.startswith("__") and x.endswith("__"))
        obj_dir = [x for x in obj_dir if not _is_magic(x)]

    if privates is False:
        _is_private = lambda x: (x.startswith("_") and not x.endswith("_"))
        obj_dir = [x for x in obj_dir if not _is_private(x)]

    # check if debugging and define output function
    gettrace = getattr(sys, "gettrace", None)
    if gettrace():
        debug = True
    else:
        debug = False

    print(colored(getattr(obj, "__name__", ""), "red"))
    doc = getattr(obj, "__doc__", "")
    if callable(obj):
        try:
            print(obj())
        except Exception as e:
            if _positional_exception(e):
                msg = "(requires positional arguments)"
                msg_color = "grey"
            else:
                msg = f"RAISES EXCEPTION : {e}"
                msg_color = "red"
            output.add(
                colored(f"{obj}(): ", "magenta"),
                colored(msg, msg_color),
                colored(doc, "green"),
            )
            print(colored(msg, "grey"))
        print(colored(obj.__doc__, "green"))

    for item in obj_dir:
        attr = getattr(obj, item)
        doc = ""
        try:
            if docstrings and attr.__doc__ is not None:
                doc = "\n" + attr.__doc__
            eval_str = str(attr)
            eval_str = "" if eval_str == "None" else eval_str
            if callable(attr) is False:
                eval_str = _fix_if_multiline(eval_str)
                output.add(
                    colored(f"{item}: ", "cyan"),
                    eval_str,
                    colored(doc, "green")
                )
        except (Exception, BaseException) as e:
            output.add(
                colored(f"{item}: ", "cyan"),
                colored(f"RAISES EXCEPTION : {e}", "red"),
                colored(doc, "green"),
            )
            continue
        if callable(attr):
            try:
                msg = str(attr())
                msg = _fix_if_multiline(msg)
                output.add(
                    colored(f"{item}(): ", "magenta"),
                    msg,
                    colored(doc, "green")
                )
            except (Exception, BaseException) as e:
                if _positional_exception(e):
                    msg = "(requires positional arguments)"
                    msg_color = "grey"
                else:
                    msg = f"RAISES EXCEPTION : {e}"
                    msg_color = "red"
                output.add(
                    colored(f"{item}(): ", "magenta"),
                    colored(msg, msg_color),
                    colored(doc, "green"),
                )
                continue
    return output


class OutputStrWrapper:
    def __init__(self, max_len):
        self._max_len = max_len
        self._output_str = ''

    def add(self, *args):
        str_ = _shorten(*args, max_len=self._max_len)
        self._output_str += str_ + '\n'

    def __repr__(self):
        return str(self._output_str)

    def __str__(self):
        return repr(self)


class Peeper:
    def __init__(
        self, obj, builtins=False, privates=False, docstrings=False, truncate_len=250
    ):
        pass


def _shorten(*args, max_len):
    str_ = "".join(args)
    if max_len:
        if len(str_) > max_len:
            str_ = str_[:max_len] + " ..."
    return str_


def _fix_if_multiline(msg):
    if "\n" in msg:
        return "\n" + msg
    else:
        return msg


def _positional_exception(e):
    e = str(e).lower()
    msgs = ('required argument', 'positional argument', 'missing argument',
            'requires argument', 'must be given', 'takes exactly')
    re_msgs = (r'exactly . argument', r'at least .* argument', )
    if any([msg in e for msg in msgs]):
        return True
    if any([re.compile(msg).search(e) for msg in re_msgs]):
        return True
    else:
        return False


if __name__ == '__main__':
    print(peep('asdf'))
    import numpy as np
    arr = np.array([1, 2, 3])
    print(peep(arr))
