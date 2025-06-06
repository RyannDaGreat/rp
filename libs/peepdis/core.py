from copy import deepcopy
from inspect import getfullargspec
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, MethodType

from typing import Any, Callable, Dict, Tuple, Type

from peepdis.preferences import _PreferencesMixin
from peepdis.datastructures import Arg, ArgDict, Output


# TODO: feature to check for state modifications by copying, then running method, then checking equality on attributes
# TODO: FIX for correct output from debug script
# TODO: should attrs and methods include builtins or should there be a
# TODO: verbose=False should exclude anything that's null, and builtins=False should exclude anything that's builtin. Verbose should be used to filter after eval
# TODO: ensure that forge is only forging positional args
# TODO: for data structures that contain multiple types, attempt to forge them, maybe using hypothesis strategies?


def peep(obj, verbose=False, forge=False):
    peeper = Peeper(obj)
    peeper.peep(forge)
    peeper.print(verbose)


class PeeperMixin(dict):
    def __init__(self, obj):
        super().__init__()
        self.obj = deepcopy(obj)
        self.dir = set(dir(obj))


class Peeper(PeeperMixin, _PreferencesMixin):
    def __init__(self, obj):
        # TODO: should I replace self with CallablePeeper?
        super().__init__(obj)
        self.attrs = dict()
        self.methods = dict()
        self.errors = dict()
        self.builtins = dict()

    def peep(self, forge=False):
        for name in self.dir:
            output = self.evaluate(name, forge=forge)
            self._index(output)

    def results(self, verbose=False):
        if verbose:
            return dict(self)
        else:
            return {name: self[name] for name in self if name not in self.builtins}

    def print(self, verbose=False):
        for name, output in self.results(verbose).items():
            print(*output.get_colored())

    def evaluate(self, name, *args, forge=False, **kwargs) -> Output:
        attr = getattr(self.obj, name)
        if not callable(attr):
            return Output(name, attr)
        # TODO: consider different paths for builtins
        unique_callables = (FunctionType, MethodType)
        builtin_callables = (BuiltinFunctionType, BuiltinMethodType)
        if isinstance(attr, unique_callables):
            peeper_class = CallablePeeper
        else:
            peeper_class = BuiltinCallablePeeper
        if name == "plot":
            a = 5
        try:
            peeper = peeper_class(attr)
            return peeper.evaluate(*args, forge=forge, **kwargs)
        except Exception as e:
            if "unsupported callable" in str(e):
                output_str = "(unsupported callable)"
                return Output(
                    name, output_str, callable_=True, unsupported_callable=True
                )
            else:
                raise ValueError(f"Unexpected error for method {name}")

    def _index(self, output: Output):
        self[output.name] = output
        if output.builtin:
            self.builtins[output.name] = self[output.name].value
        elif output.callable_:
            self.methods[output.name] = self[output.name].value
        elif output.error:
            self.errors[output.name] = self[output.name].value
        else:
            self.attrs[output.name] = self[output.name].value


class BuiltinCallablePeeper(PeeperMixin):
    # TODO: will need to merge with CallablePeeper in the future
    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj)
        # TODO: move ArgDict instantiation up here and fix numbering

    def evaluate(self, *args, forge=False, **kwargs) -> Output:
        # TODO: figure out how to set up args in this case (no access to positional arg names)
        arg_names = [i for i in range(len(args))]
        arg_names += list(kwargs.values())
        self.args = ArgDict(arg_names)
        self.args.update_positional(*args)
        self.args.update_kwargs(**kwargs)
        obj = deepcopy(self.obj)
        try:
            output_str = repr(obj(*args, **kwargs))
        except Exception as e:
            output_str = repr(e)
            error = True
            if "argument" in str(e):
                args_missing = True
                if ":" in str(e):
                    missing_arg_str = output_str.split(":")[1][:-2]
                    output_str = f"(missing args: {missing_arg_str})"
                else:
                    output_str = f"(missing args)"
            else:
                args_missing = False
                output_str = repr(e)
        else:
            error = False
            args_missing = False
        return Output(
            obj.__name__,
            output_str,
            self.args,
            callable_=True,
            error=error,
            args_missing=args_missing,
        )


class CallablePeeper(PeeperMixin):
    _ordinary_callables = (FunctionType, MethodType)
    _builtin_callables = (BuiltinFunctionType, BuiltinMethodType)
    _forgery_dict = {"int": 0, "str": "abc", "list": [0, 1], "None": None}

    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj)
        if isinstance(obj, self._ordinary_callables):
            self.spec = getfullargspec(obj)    # TODO: test on arrays, dataframes, and sklearn models (seemed to work on sklearn)
            self.args = ArgDict(self.spec.args)
            self._collect_args(*args, **kwargs)
        elif isinstance(obj, self._builtin_callables):
            self.args = ArgDict([])

    def _collect_args(self, *args, **kwargs):
        if self.spec.defaults:
            for i, arg in enumerate(self.spec.defaults[::-1]):
                self.args[-1 - i].value = arg
                self.args[-1 - i].method = "default"
        for i, arg in enumerate(args):
            self.args[i].value = arg
            self.args[i].method = "specified"
        for name, arg in kwargs.items():
            self.args[name].value = arg
            self.args[name].method = "specified"

    def evaluate(self, *args, forge=False, **kwargs) -> Output:
        obj = deepcopy(self.obj)
        if forge:
            self.forge_args()
        self.args.update_positional(*args)
        self.args.update_kwargs(**kwargs)
        arg_dict = self.args.generate_args()
        try:
            output_str = repr(obj(**arg_dict))
        except Exception as e:
            output_str = repr(e)
            error = True
            if "missing" in str(e) and "argument" in str(e):
                missing_arg_str = output_str.split(":")[1][:-2]
                output_str = f"(missing args: {missing_arg_str})"
                args_missing = True
            else:
                args_missing = False
                output_str = repr(e)
        else:
            error = False
            args_missing = False
        return Output(
            obj.__name__,
            output_str,
            self.args,
            callable_=True,
            error=error,
            args_missing=args_missing,
        )

    def forge_args(self, *args, **kwargs):
        """ Attempt to generate arguments to call the method """
        # TODO: currently forging kwargs and causing errors. Only forge positionals
        type_dict = self._infer_types()
        self.args.returns = type_dict.pop("returns", None)
        for name in self.args.null_args:
            type_ = type_dict.get(name, None)
            if not type_:
                # TODO: fill in with brute force
                continue
            self.args[name].value = self._forgery_dict[type_]
            self.args[name].method = "forged"
            self.args[name].type_ = type_
        for i, arg in enumerate(args):
            self.args[i].value = arg
            self.args[i].method = "specified"
        for name, arg in kwargs.items():
            self.args[name].value = arg
            self.args[name].method = "specified"
        return self.args

    def _infer_types(self, brute_force=True):
        """ Infer the argument types from the type annotations """
        # TODO: modify state of self.args rather than calling in forge_args
        type_dict = dict(self.spec.annotations)
        type_dict = {k: v.__name__ for k, v in type_dict}
        type_dict.pop("self", None)
        return type_dict

    def _brute_force_types(self):
        # TODO: iterate through missing arguments, trying different things
        # make a new class to do this?
        pass

