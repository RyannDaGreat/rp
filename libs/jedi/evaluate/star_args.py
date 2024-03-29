"""
This module is responsible for evaluating *args and **kwargs for signatures.

This means for example in this case::

    def foo(a, b, c): ...

    def bar(*args):
        return foo(1, *args)

The signature here for bar should be `bar(b, c)` instead of bar(*args).
"""

from rp.libs.jedi._compatibility import Parameter
from rp.libs.jedi.evaluate.utils import to_list
from rp.libs.jedi.evaluate.names import ParamNameWrapper


def _iter_nodes_for_param(param_name):
    from rp.libs.parso.python.tree import search_ancestor
    from rp.libs.jedi.evaluate.arguments import TreeArguments

    execution_context = param_name.parent_context
    function_node = execution_context.tree_node
    module_node = function_node.get_root_node()
    start = function_node.children[-1].start_pos
    end = function_node.children[-1].end_pos
    for name in module_node.get_used_names().get(param_name.string_name):
        if start <= name.start_pos < end:
            # Is used in the function
            argument = name.parent
            if argument.type == 'argument' \
                    and argument.children[0] == '*' * param_name.star_count:
                # No support for Python <= 3.4 here, but they are end-of-life
                # anyway
                trailer = search_ancestor(argument, 'trailer')
                if trailer is not None:  # Make sure we're in a function
                    context = execution_context.create_context(trailer)
                    if _goes_to_param_name(param_name, context, name):
                        contexts = _to_callables(context, trailer)

                        args = TreeArguments.create_cached(
                            execution_context.evaluator,
                            context=context,
                            argument_node=trailer.children[1],
                            trailer=trailer,
                        )
                        for c in contexts:
                            yield c, args
                    else:
                        assert False


def _goes_to_param_name(param_name, context, potential_name):
    if potential_name.type != 'name':
        return False
    from rp.libs.jedi.evaluate.names import TreeNameDefinition
    found = TreeNameDefinition(context, potential_name).goto()
    return any(param_name.parent_context == p.parent_context
               and param_name.start_pos == p.start_pos
               for p in found)


def _to_callables(context, trailer):
    from rp.libs.jedi.evaluate.syntax_tree import eval_trailer

    atom_expr = trailer.parent
    index = atom_expr.children[0] == 'await'
    # Eval atom first
    contexts = context.eval_node(atom_expr.children[index])
    for trailer2 in atom_expr.children[index + 1:]:
        if trailer == trailer2:
            break
        contexts = eval_trailer(context, contexts, trailer2)
    return contexts


def _remove_given_params(arguments, param_names):
    count = 0
    used_keys = set()
    for key, _ in arguments.unpack():
        if key is None:
            count += 1
        else:
            used_keys.add(key)

    for p in param_names:
        if count and p.maybe_positional_argument():
            count -= 1
            continue
        if p.string_name in used_keys and p.maybe_keyword_argument():
            continue
        yield p


@to_list
def process_params(param_names, star_count=3):  # default means both * and **
    used_names = set()
    arg_callables = []
    kwarg_callables = []

    kw_only_names = []
    kwarg_names = []
    arg_names = []
    original_arg_name = None
    original_kwarg_name = None
    for p in param_names:
        kind = p.get_kind()
        if kind == Parameter.VAR_POSITIONAL:
            if star_count & 1:
                arg_callables = _iter_nodes_for_param(p)
                original_arg_name = p
        elif p.get_kind() == Parameter.VAR_KEYWORD:
            if star_count & 2:
                kwarg_callables = list(_iter_nodes_for_param(p))
                original_kwarg_name = p
        elif kind == Parameter.KEYWORD_ONLY:
            if star_count & 2:
                kw_only_names.append(p)
        elif kind == Parameter.POSITIONAL_ONLY:
            if star_count & 1:
                yield p
        else:
            if star_count == 1:
                yield ParamNameFixedKind(p, Parameter.POSITIONAL_ONLY)
            elif star_count == 2:
                kw_only_names.append(ParamNameFixedKind(p, Parameter.KEYWORD_ONLY))
            else:
                used_names.add(p.string_name)
                yield p

    longest_param_names = ()
    found_arg_signature = False
    found_kwarg_signature = False
    for func_and_argument in arg_callables:
        func, arguments = func_and_argument
        new_star_count = star_count
        if func_and_argument in kwarg_callables:
            kwarg_callables.remove(func_and_argument)
        else:
            new_star_count = 1

        for signature in func.get_signatures():
            found_arg_signature = True
            if new_star_count == 3:
                found_kwarg_signature = True
            args_for_this_func = []
            for p in process_params(
                    list(_remove_given_params(
                        arguments,
                        signature.get_param_names(resolve_stars=False)
                    )), new_star_count):
                if p.get_kind() == Parameter.VAR_KEYWORD:
                    kwarg_names.append(p)
                elif p.get_kind() == Parameter.VAR_POSITIONAL:
                    arg_names.append(p)
                elif p.get_kind() == Parameter.KEYWORD_ONLY:
                    kw_only_names.append(p)
                else:
                    args_for_this_func.append(p)
            if len(args_for_this_func) > len(longest_param_names):
                longest_param_names = args_for_this_func

    for p in longest_param_names:
        if star_count == 1 and p.get_kind() != Parameter.VAR_POSITIONAL:
            yield ParamNameFixedKind(p, Parameter.POSITIONAL_ONLY)
        else:
            if p.get_kind() == Parameter.POSITIONAL_OR_KEYWORD:
                used_names.add(p.string_name)
            yield p

    if not found_arg_signature and original_arg_name is not None:
        yield original_arg_name
    elif arg_names:
        yield arg_names[0]

    for p in kw_only_names:
        if p.string_name in used_names:
            continue
        yield p
        used_names.add(p.string_name)

    for func, arguments in kwarg_callables:
        for signature in func.get_signatures():
            found_kwarg_signature = True
            for p in process_params(
                    list(_remove_given_params(
                        arguments,
                        signature.get_param_names(resolve_stars=False)
                    )), star_count=2):
                if p.get_kind() != Parameter.KEYWORD_ONLY or not kwarg_names:
                    yield p

    if not found_kwarg_signature and original_kwarg_name is not None:
        yield original_kwarg_name
    elif kwarg_names:
        yield kwarg_names[0]


class ParamNameFixedKind(ParamNameWrapper):
    def __init__(self, param_name, new_kind):
        super(ParamNameFixedKind, self).__init__(param_name)
        self._new_kind = new_kind

    def get_kind(self):
        return self._new_kind
