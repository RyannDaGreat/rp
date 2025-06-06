from collections import OrderedDict
from termcolor import colored
from typing import Any, Callable, Dict, List, Tuple, Type, Union

from peepdis.preferences import _PreferencesMixin


class Arg(_PreferencesMixin):
    def __init__(self, name, value: Any = None, type_: Type = None, method: str = None):
        self.name = name
        self.value = value
        self.type_ = type_
        self.method = method

    def get_colored(self):
        return colored(str(self), self._color_scheme[str(self.method)])

    def __str__(self):
        annotation_str = "="
        if self._display_type_annotations:
            annotation_str = f": {self.type_} = "
        str_ = self.name + annotation_str + str(self.value)
        return str_

    def __eq__(self, other):
        return self.value == other


class ArgDict(OrderedDict, _PreferencesMixin):
    def __init__(self, names: Union[Dict, List, Tuple]):
        super().__init__()
        if "self" in names:
            names.remove("self")
        if "return" in names:
            names.remove("return")
        if isinstance(names, dict):
            for name, arg in names:
                self[name] = Arg(name, arg)
        else:
            for name in names:
                self[name] = Arg(name)
        self.returns = None

    def get_colored(self):
        return [arg.get_colored() for arg in self.values()]

    def update_positional(self, *args):
        for i, arg in enumerate(args):
            self[i].value = arg
            self[i].method = "specified"

    def update_kwargs(self, **kwargs):
        for name, arg in kwargs:
            self[name].value = arg
            self[name].method = "specified"

    def generate_args(self):
        return {name: arg.value for name, arg in self.items()}

    @property
    def null_args(self):
        nulls = tuple([k for k, v in self.items() if v.value is None])
        return nulls

    @property
    def is_full(self):
        if self.null_args:
            return False
        else:
            return True

    def __getitem__(self, key):
        if isinstance(key, int):
            key = list(self.keys())[key]
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if not isinstance(value, Arg):
            raise TypeError(f"`ArgDict` values must be type `Arg`, not: {type(value)}")
        if isinstance(key, int):
            key = list(self.keys())[key]
        super().__setitem__(key, value)


class Output(_PreferencesMixin):
    _types = {float, int, list, dict, str, tuple}
    _magics = {"__dict__", "__module__", "__weakref__", "__slotnames__"}
    _builtins = {x for type_ in _types for x in dir(type_)} | _magics

    def __init__(
        self,
        name: str,
        value: Any,
        args: ArgDict = None,
        callable_: bool = False,
        error: bool = False,
        args_missing: bool = False,
        unsupported_callable: bool = False,
    ):
        self.name = name
        self.value = value
        self.args = args if args else ArgDict([])
        self.callable_ = callable_
        self.error = error
        self.args_missing = args_missing
        self.unsupported_callable = unsupported_callable
        self.builtin = True if name in self._builtins else False

    def print(self):
        print(*self.get_colored())

    def get_colored(self):
        # color name and arguments
        base_color = self._color_scheme[self.obj_type]
        base = colored(self.name, base_color)
        if self.callable_:
            open_parenthesis = colored("(", base_color)
            close_parenthesis = colored(")", base_color)
            args = colored(", ", base_color).join(self.args.get_colored())
            base += open_parenthesis + args + close_parenthesis
        colon = colored(":", base_color)
        base += colon
        # color output message
        msg = colored(self.value, self._color_scheme[self.output_type])
        return base, msg

    @property
    def obj_type(self):
        if self.builtin:
            return "builtin"
        if self.callable_:
            return "callable_"
        else:
            return "attr"

    @property
    def output_type(self):
        if self.unsupported_callable:
            return "null"
        elif self.args_missing:
            return "null"
        elif self.error:
            return "error"
        elif self.builtin:
            return "builtin"
        else:
            return "message"
