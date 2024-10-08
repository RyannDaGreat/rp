import re

from rp.libs.parso.python.token import PythonTokenTypes
from rp.libs.parso.python import tree
from rp.libs.parso.tree import search_ancestor, Leaf

from rp.libs.jedi._compatibility import Parameter
from rp.libs.jedi import debug
from rp.libs.jedi import settings
from rp.libs.jedi.api import classes
from rp.libs.jedi.api import helpers
from rp.libs.jedi.api import keywords
from rp.libs.jedi.api.file_name import file_name_completions
from rp.libs.jedi.evaluate import imports
from rp.libs.jedi.evaluate.helpers import evaluate_call_of_leaf, parse_dotted_names
from rp.libs.jedi.evaluate.filters import get_global_filters
from rp.libs.jedi.evaluate.gradual.conversion import convert_contexts
from rp.libs.jedi.parser_utils import get_statement_of_position, cut_value_at_position


def get_call_signature_param_names(call_signatures):
    # add named params
    for call_sig in call_signatures:
        for p in call_sig.params:
            # Allow protected access, because it's a public API.
            if p._name.get_kind() in (Parameter.POSITIONAL_OR_KEYWORD,
                                      Parameter.KEYWORD_ONLY):
                yield p._name


def filter_names(evaluator, completion_names, stack, like_name):
    comp_dct = {}
    if settings.case_insensitive_completion:
        like_name = like_name.lower()
    for name in completion_names:
        string = name.string_name
        if settings.case_insensitive_completion:
            string = string.lower()

        if string.startswith(like_name):
            new = classes.Completion(
                evaluator,
                name,
                stack,
                len(like_name)
            )
            k = (new.name, new.complete)  # key
            if k in comp_dct and settings.no_completion_duplicates:
                comp_dct[k]._same_name_completions.append(new)
            else:
                comp_dct[k] = new
                yield new


def get_user_scope(module_context, position):
    """
    Returns the scope in which the user resides. This includes flows.
    """
    user_stmt = get_statement_of_position(module_context.tree_node, position)
    if user_stmt is None:
        def scan(scope):
            for s in scope.children:
                if s.start_pos <= position <= s.end_pos:
                    if isinstance(s, (tree.Scope, tree.Flow)) \
                            or s.type in ('async_stmt', 'async_funcdef'):
                        return scan(s) or s
                    elif s.type in ('suite', 'decorated'):
                        return scan(s)
            return None

        scanned_node = scan(module_context.tree_node)
        if scanned_node:
            return module_context.create_context(scanned_node, node_is_context=True)
        return module_context
    else:
        return module_context.create_context(user_stmt)


def get_flow_scope_node(module_node, position):
    node = module_node.get_leaf_for_position(position, include_prefixes=True)
    while not isinstance(node, (tree.Scope, tree.Flow)):
        node = node.parent

    return node


class Completion:
    def __init__(self, evaluator, module, code_lines, position, call_signatures_callback):
        self._evaluator = evaluator
        self._module_context = module
        self._module_node = module.tree_node
        self._code_lines = code_lines

        # The first step of completions is to get the name
        self._like_name = helpers.get_on_completion_name(self._module_node, code_lines, position)
        # The actual cursor position is not what we need to calculate
        # everything. We want the start of the name we're on.
        self._original_position = position
        self._position = position[0], position[1] - len(self._like_name)
        self._call_signatures_callback = call_signatures_callback

    def completions(self):
        leaf = self._module_node.get_leaf_for_position(self._position, include_prefixes=True)
        string, start_leaf = _extract_string_while_in_string(leaf, self._position)
        if string is not None:
            completions = list(file_name_completions(
                self._evaluator, self._module_context, start_leaf, string,
                self._like_name, self._call_signatures_callback,
                self._code_lines, self._original_position
            ))
            if completions:
                return completions

        completion_names = self._get_context_completions(leaf)

        completions = filter_names(self._evaluator, completion_names,
                                   self.stack, self._like_name)

        return sorted(completions, key=lambda x: (x.name.startswith('__'),
                                                  x.name.startswith('_'),
                                                  x.name.lower()))

    def _get_context_completions(self, leaf):
        """
        Analyzes the context that a completion is made in and decides what to
        return.

        Technically this works by generating a parser stack and analysing the
        current stack for possible grammar nodes.

        Possible enhancements:
        - global/nonlocal search global
        - yield from / raise from <- could be only exceptions/generators
        - In args: */**: no completion
        - In params (also lambda): no completion before =
        """

        grammar = self._evaluator.grammar
        self.stack = stack = None

        try:
            self.stack = stack = helpers.get_stack_at_position(
                grammar, self._code_lines, leaf, self._position
            )
        except helpers.OnErrorLeaf as e:
            value = e.error_leaf.value
            if value == '.':
                # After ErrorLeaf's that are dots, we will not do any
                # completions since this probably just confuses the user.
                return []

            # If we don't have a context, just use global completion.
            return self._global_completions()

        allowed_transitions = \
            list(stack._allowed_transition_names_and_token_types())

        if 'if' in allowed_transitions:
            leaf = self._module_node.get_leaf_for_position(self._position, include_prefixes=True)
            previous_leaf = leaf.get_previous_leaf()

            indent = self._position[1]
            if not (leaf.start_pos <= self._position <= leaf.end_pos):
                indent = leaf.start_pos[1]

            if previous_leaf is not None:
                stmt = previous_leaf
                while True:
                    stmt = search_ancestor(
                        stmt, 'if_stmt', 'for_stmt', 'while_stmt', 'try_stmt',
                        'error_node',
                    )
                    if stmt is None:
                        break

                    type_ = stmt.type
                    if type_ == 'error_node':
                        first = stmt.children[0]
                        if isinstance(first, Leaf):
                            type_ = first.value + '_stmt'
                    # Compare indents
                    if stmt.start_pos[1] == indent:
                        if type_ == 'if_stmt':
                            allowed_transitions += ['elif', 'else']
                        elif type_ == 'try_stmt':
                            allowed_transitions += ['except', 'finally', 'else']
                        elif type_ == 'for_stmt':
                            allowed_transitions.append('else')

        completion_names = []
        current_line = self._code_lines[self._position[0] - 1][:self._position[1]]
        if not current_line or current_line[-1] in ' \t.;':
            completion_names += self._get_keyword_completion_names(allowed_transitions)

        if any(t in allowed_transitions for t in (PythonTokenTypes.NAME,
                                                  PythonTokenTypes.INDENT)):
            # This means that we actually have to do type inference.

            nonterminals = [stack_node.nonterminal for stack_node in stack]

            nodes = []
            for stack_node in stack:
                if stack_node.dfa.from_rule == 'small_stmt':
                    nodes = []
                else:
                    nodes += stack_node.nodes

            if nodes and nodes[-1] in ('as', 'def', 'class'):
                # No completions for ``with x as foo`` and ``import x as foo``.
                # Also true for defining names as a class or function.
                return list(self._get_class_context_completions(is_function=True))
            elif "import_stmt" in nonterminals:
                level, names = parse_dotted_names(nodes, "import_from" in nonterminals)

                only_modules = not ("import_from" in nonterminals and 'import' in nodes)
                completion_names += self._get_importer_names(
                    names,
                    level,
                    only_modules=only_modules,
                )
            elif nonterminals[-1] in ('trailer', 'dotted_name') and nodes[-1] == '.':
                dot = self._module_node.get_leaf_for_position(self._position)
                completion_names += self._trailer_completions(dot.get_previous_leaf())
            else:
                completion_names += self._global_completions()
                completion_names += self._get_class_context_completions(is_function=False)

            if 'trailer' in nonterminals:
                call_signatures = self._call_signatures_callback()
                completion_names += get_call_signature_param_names(call_signatures)

        return completion_names

    def _get_keyword_completion_names(self, allowed_transitions):
        for k in allowed_transitions:
            if isinstance(k, str) and k.isalpha():
                yield keywords.KeywordName(self._evaluator, k)

    def _global_completions(self):
        context = get_user_scope(self._module_context, self._position)
        debug.dbg('global completion scope: %s', context)
        flow_scope_node = get_flow_scope_node(self._module_node, self._position)
        filters = get_global_filters(
            self._evaluator,
            context,
            self._position,
            origin_scope=flow_scope_node
        )
        completion_names = []
        for filter in filters:
            completion_names += filter.values()
        return completion_names

    def _trailer_completions(self, previous_leaf):
        user_context = get_user_scope(self._module_context, self._position)
        evaluation_context = self._evaluator.create_context(
            self._module_context, previous_leaf
        )
        contexts = evaluate_call_of_leaf(evaluation_context, previous_leaf)
        completion_names = []
        debug.dbg('trailer completion contexts: %s', contexts, color='MAGENTA')
        for context in contexts:
            for filter in context.get_filters(
                    search_global=False,
                    origin_scope=user_context.tree_node):
                completion_names += filter.values()

        python_contexts = convert_contexts(contexts)
        for c in python_contexts:
            if c not in contexts:
                for filter in c.get_filters(
                        search_global=False,
                        origin_scope=user_context.tree_node):
                    completion_names += filter.values()
        return completion_names

    def _get_importer_names(self, names, level=0, only_modules=True):
        names = [n.value for n in names]
        i = imports.Importer(self._evaluator, names, self._module_context, level)
        return i.completion_names(self._evaluator, only_modules=only_modules)

    def _get_class_context_completions(self, is_function=True):
        """
        Autocomplete inherited methods when overriding in child class.
        """
        leaf = self._module_node.get_leaf_for_position(self._position, include_prefixes=True)
        cls = tree.search_ancestor(leaf, 'classdef')
        if isinstance(cls, (tree.Class, tree.Function)):
            # Complete the methods that are defined in the super classes.
            random_context = self._module_context.create_context(
                cls,
                node_is_context=True
            )
        else:
            return

        if cls.start_pos[1] >= leaf.start_pos[1]:
            return

        filters = random_context.get_filters(search_global=False, is_instance=True)
        # The first dict is the dictionary of class itself.
        next(filters)
        for filter in filters:
            for name in filter.values():
                # TODO we should probably check here for properties
                if (name.api_type == 'function') == is_function:
                    yield name


def _extract_string_while_in_string(leaf, position):
    if leaf.type == 'string':
        match = re.match(r'^\w*(\'{3}|"{3}|\'|")', leaf.value)
        quote = match.group(1)
        if leaf.line == position[0] and position[1] < leaf.column + match.end():
            return None, None
        if leaf.end_pos[0] == position[0] and position[1] > leaf.end_pos[1] - len(quote):
            return None, None
        return cut_value_at_position(leaf, position)[match.end():], leaf

    leaves = []
    while leaf is not None and leaf.line == position[0]:
        if leaf.type == 'error_leaf' and ('"' in leaf.value or "'" in leaf.value):
            return ''.join(l.get_code() for l in leaves), leaf
        leaves.insert(0, leaf)
        leaf = leaf.get_previous_leaf()
    return None, None
