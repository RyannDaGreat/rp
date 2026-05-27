"""
Jedi completion utilities for rp's pseudo terminal.

This module contains all Jedi-specific logic for generating completions
and metadata, separated from the main completer for clarity.
"""
from __future__ import unicode_literals
from collections import namedtuple
import rp

__all__ = ['JediInfo', 'get_jedi_interpreter', 'get_jedi_display_meta', 'format_jedi_value_description',
           'forwarder', 'apply_signature_special_cases', 'synthesize_target_completions',
           'synthesize_scope_completions']

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


# ══════════════════════════════════════════════════════════════════════════════
#  Call-forwarding registry — lets pterm "see through" wrapper functions to the
#  underlying callable, for BOTH signature display and completions.
#
#  Add a wrapper with @forwarder('module.path.name', 'alias.name', ...):
#      a forwarder returns list[jedi.Name] for the wrapped target (or None to skip).
#      lookup matches the full_name first, then the basename.
#
#  Detection:
#      * Explicit registry — for wrappers we can't AST-analyze (C-implemented like
#        functools.partial). Manually mapped to a hand-rolled resolver.
#      * AST fallback (_ast_forwarder) — handles any Python-source wrapper whose
#        body is a single call `target(...**y)` where target is either:
#          (a) a wrapper positional parameter — resolved from the callsite, e.g.
#              `def f(x, **y): x(**y)` + `f(load_image, ...)`  →  load_image, OR
#          (b) a global Name — resolved via func.__globals__, e.g.
#              `def f(**y): load_image(**y)`                   →  load_image.
#        This subsumes the old `_arg0_forwarder` (gather_args_call shape) and
#        `_kwargs_ast_forwarder` (user-defined **kwargs passthrough).
#
#  Consumers:
#      apply_signature_special_cases() — swaps in target's sig, appending an
#          ellipsis param (visual passthrough marker) and any wrapper-private
#          non-passthrough kwargs (e.g. partial's *args bindings).
#      synthesize_target_completions() — surfaces target's kwargs as completions
# ══════════════════════════════════════════════════════════════════════════════

_FORWARDERS = {}

def forwarder(*full_names):
    """Register a forwarder under one or more jedi full_names."""
    def deco(fn):
        for n in full_names: _FORWARDERS[n] = fn
        return fn
    return deco

def _resolve_forwarder_target(interpreter, code, sig):
    """Query. Find the wrapped target's Names via registered forwarder (matched by full_name or basename), or AST-fallback."""
    if sig is None: return None
    full = getattr(sig, 'full_name', None) or ''
    fwd = _FORWARDERS.get(full) or _FORWARDERS.get(full.rpartition('.')[-1])
    if fwd: return fwd(interpreter, code, sig)
    return _ast_forwarder(interpreter, code, sig)


# ────── Built-in forwarders ──────

@forwarder('functools.partial')
def _arg0_forwarder(interpreter, code, sig):
    """
    [C] For wrappers shaped like `fn(target, *args, **kw)` where target is positional arg 0.
    Used only for C-implemented wrappers (functools.partial) — Python-source wrappers
    matching this shape are handled generically by _ast_forwarder.
    """
    end = _scan_call_argN_end(code, 0, *sig.bracket_start)
    if end is None: return None
    return interpreter.infer(*end) or None


def _ast_forwarder(interpreter, code, sig):
    """
    [C] Fallback for any Python-source wrapper whose body is a single forwarding call.

    Detects two shapes:

      (a) Wrapper-parameter target — `def f(x, ..., **y): x(**y)`:
          target is resolved from the callsite's argument bound to that parameter.
          Example:
              >>> def f(x, **y):
              ...     x(**y)
              >>> f(load_image, |)        # cursor at |
              load_image(location, use_cache=False, ...)

      (b) Global target — `def f(**y): load_image(**y)`:
          target is resolved via func.__globals__.
          Example:
              >>> def f(**y):
              ...     load_image(**y)
              >>> f(|)
              load_image(location, use_cache=False, ...)

    After level-1 resolution, follows global-forwarder chains transitively via
    `_chase_forwarder_chain` — so `outer → middle → load_image` resolves all the way.

    Subsumes the old _arg0_forwarder (for gather_args_call) and _kwargs_ast_forwarder
    (for user-defined kwargs passthrough). Returns [jedi.Name | _RuntimeName] or None.

    Uses _RuntimeName for global targets to avoid spinning up a sibling jedi.Interpreter,
    which would corrupt parso's shared parse cache and break the caller's interpreter.
    """
    func = _lookup_runtime_func(interpreter, getattr(sig, 'full_name', '') or '')
    if func is None: return None
    descriptor = _find_unique_forward_target(func)
    if descriptor is None: return None
    kind, ref = descriptor
    if kind == 'param':
        end = _scan_call_argN_end(code, ref, *sig.bracket_start)
        if end is None: return None
        inferred = interpreter.infer(*end)
        if not inferred: return None
        return [_chased_or_original(interpreter, n) for n in inferred]
    if kind == 'global':
        target_obj = func.__globals__.get(ref)
        if target_obj is None or not callable(target_obj): return None
        return [_RuntimeName(_chase_forwarder_chain(target_obj))]
    return None

def _chased_or_original(interpreter, jedi_name):
    """[C] Query. If `jedi_name`'s runtime callable can be chased to a deeper terminal, wrap as _RuntimeName; else return as-is."""
    full = getattr(jedi_name, 'full_name', '') or ''
    fn = _lookup_runtime_func(interpreter, full)
    if fn is None: return jedi_name
    terminal = _chase_forwarder_chain(fn)
    if terminal is fn: return jedi_name
    return _RuntimeName(terminal)

def _chase_forwarder_chain(func, _seen=None):
    """
    [C] Query. Follow a global-target forwarder chain from `func` to its terminal callable.

    At each hop, runs `_find_unique_forward_target` on the current callable. If the
    descriptor is a global target, looks it up via __globals__ and continues. If it's
    a wrapper-parameter target, stops here — there's no callsite at this depth to bind
    the parameter against. Cycle-safe via id() tracking.

    Example:
        >>> def outer(**y): middle(**y)
        >>> def middle(**y): load_image(**y)
        >>> _chase_forwarder_chain(outer) is load_image
        True
    """
    if _seen is None: _seen = set()
    if id(func) in _seen: return func
    _seen.add(id(func))
    descriptor = _find_unique_forward_target(func)
    if descriptor is None: return func
    kind, ref = descriptor
    if kind != 'global': return func
    nxt = (getattr(func, '__globals__', {}) or {}).get(ref)
    if nxt is None or not callable(nxt): return func
    return _chase_forwarder_chain(nxt, _seen)


# ────── Helpers ──────

def _scan_call_argN_end(code, arg_index, line, paren_col):
    """
    [C] Query. (line, col) at end of arg `arg_index` of the call whose '(' is at (line, paren_col), or None.

    Walks character-by-character, tracking string/comment context and bracket nesting,
    advancing through `arg_index` top-level commas before locating the end of the next arg.

    Generalizes the old _scan_call_arg0_end (which was hardcoded to arg 0).
    """
    pos = sum(len(l)+1 for l in code.split('\n')[:line-1]) + paren_col + 1
    PAIRS, depth, j, seen_commas = dict(zip(')]}', '([{')), {'(': 0, '[': 0, '{': 0}, pos, 0
    arg_start = pos
    while j < len(code):
        c = code[j]
        if c in '"\'':
            j += 1
            while j < len(code) and code[j] != c:
                if code[j] == '\\': j += 1
                j += 1
        elif c == '#':
            j = code.find('\n', j)
            if j == -1: return None
        elif c in '([{': depth[c] += 1
        elif c in ')]}':
            if c == ')' and not any(depth.values()):
                if seen_commas < arg_index: return None
                break
            depth[PAIRS[c]] -= 1
        elif c == ',' and not any(depth.values()):
            if seen_commas == arg_index: break
            seen_commas += 1
            arg_start = j + 1
        j += 1
    if seen_commas < arg_index: return None
    while j > arg_start and code[j-1].isspace(): j -= 1
    return code.count('\n', 0, j) + 1, j - code.rfind('\n', 0, j) - 1

def _lookup_runtime_func(interpreter, full_name):
    """
    [C] Query. Find the actual Python function object behind a jedi full_name.

    Resolution order:
      1. Basename match in any namespace — covers `from rp import gather_args_call`.
      2. Dotted-path walk from any namespace root — covers `import rp` followed by
         `rp.gather_args_call` or `rp.r.gather_args_call` (full_name being the latter).
    """
    if not full_name: return None
    parts = full_name.split('.')
    name = parts[-1]
    namespaces = getattr(interpreter, 'namespaces', ()) or ()
    for ns in namespaces:
        if name in ns and callable(ns[name]): return ns[name]
    for ns in namespaces:
        if parts[0] not in ns: continue
        obj = ns[parts[0]]
        try:
            for p in parts[1:]: obj = getattr(obj, p)
        except AttributeError:
            continue
        if callable(obj): return obj
    return None

def _walk_body_skip_nested(fn_node):
    """[C] Query. Walk every descendant of a FunctionDef's body EXCEPT nested function/lambda definitions."""
    import ast as ast_mod
    NESTED = (ast_mod.FunctionDef, ast_mod.AsyncFunctionDef, ast_mod.Lambda)
    def _rec(node):
        if isinstance(node, NESTED): return
        yield node
        for child in ast_mod.iter_child_nodes(node):
            for x in _rec(child): yield x
    for stmt in fn_node.body:
        for node in _rec(stmt): yield node

def _find_unique_forward_target(func):
    """
    [C] Query. Detect a single forwarding-target descriptor for `func`, or None.

    Searches the wrapper's direct body (skipping nested defs/lambdas) for Call
    nodes whose .func is a Name and which include at least one `**name` keyword
    expansion. Among such candidates:
      * Prefer the unique one whose target is a wrapper positional parameter:
            returns ('param', index)
      * Else if exactly one candidate's target is a resolvable global:
            returns ('global', name)
      * Otherwise: returns None.

    The param-over-global precedence handles helpers in the wrapper body
    (e.g. `gather_args_call` calls `gather_args(...)` for prep, then `func(...)`
    for the actual forward — `func` is the param target that wins).

    Example (param):
        >>> def f(x, **y): x(**y)
        >>> _find_unique_forward_target(f)
        ('param', 0)

    Example (global):
        >>> def f(**y): load_image(**y)
        >>> _find_unique_forward_target(f)
        ('global', 'load_image')

    Example (param wins over global):
        >>> def gac(func, *args, **kwargs):
        ...     out_args, out_kwargs = gather_args(func, *args, **kwargs)
        ...     return func(*out_args, **out_kwargs)
        >>> _find_unique_forward_target(gac)
        ('param', 0)
    """
    import inspect, ast as ast_mod, textwrap
    try: src = textwrap.dedent(inspect.getsource(func))
    except (OSError, TypeError): return None
    try: tree = ast_mod.parse(src)
    except SyntaxError: return None
    if not tree.body or not isinstance(tree.body[0], (ast_mod.FunctionDef, ast_mod.AsyncFunctionDef)):
        return None
    fn = tree.body[0]
    pos_param_names = [a.arg for a in (fn.args.posonlyargs + fn.args.args)]
    globals_dict = getattr(func, '__globals__', {}) or {}
    # Collect every **-expansion Call whose .func is a Name. Classify as ('param', N),
    # ('global', name), or ('unknown', name) — unknown still counts as a candidate so
    # multi-call forwarders don't silently collapse to "the one we could resolve".
    candidates = []
    for node in _walk_body_skip_nested(fn):
        if not isinstance(node, ast_mod.Call): continue
        if not isinstance(node.func, ast_mod.Name): continue
        if not any(kw.arg is None for kw in node.keywords): continue
        name = node.func.id
        if   name in pos_param_names: candidates.append(('param', pos_param_names.index(name)))
        elif name in globals_dict:    candidates.append(('global', name))
        else:                         candidates.append(('unknown', name))
    param_cands = [c for c in candidates if c[0] == 'param']
    if len(param_cands) == 1:                                          return param_cands[0]
    if param_cands:                                                    return None  # multiple param forwards: ambiguous
    if len(candidates) == 1 and candidates[0][0] == 'global':          return candidates[0]
    return None


# ────── Consumers ──────

class _SwappedSig:
    """BaseSignature wrapper allowing params override and adding bracket_start (which BaseSignature lacks)."""
    def __init__(self, base, bracket_start, params=None):
        self._base = base
        self.params = list(params) if params is not None else list(base.params)
        self.bracket_start = bracket_start
        self.index = -1
    def __getattr__(self, name): return getattr(self._base, name)

def apply_signature_special_cases(interpreter, code, signatures):
    """
    [C] Query. For forwarded calls, swap in the target's sigs.
    The displayed param list is: target's own params, then an ellipsis (`...`) marking
    transparent kwargs passthrough, then any wrapper-private non-passthrough kwargs
    (e.g. partial's *args bindings, or wrapper-only meta-kwargs).
    """
    if not signatures: return signatures
    sig = signatures[0]
    targets = _resolve_forwarder_target(interpreter, code, sig)
    if not targets: return signatures
    extras = [p for i, p in enumerate(sig.params)
              if i > 0 and p is not None
              and not p.description.replace('param ', '', 1).startswith('*')]
    out = [_SwappedSig(ts, sig.bracket_start, list(ts.params) + [_EllipsisParam()] + extras)
           for t in targets for ts in t.get_signatures()]
    return out or signatures

class _EllipsisParam:
    """[C] jedi.Param-shaped stub rendering as `...` — visual passthrough marker in forwarded sigs."""
    __slots__ = ()
    description = 'param ...'

class _ParamCompletion:
    """Minimal jedi.Completion-shaped stub. Carries just name & type — enough for the completer."""
    __slots__ = ('name', 'type')
    def __init__(self, name): self.name, self.type = name, 'param'
    def get_signatures(self): return []

class _RuntimeParam:
    """jedi.Param-shaped stub built from an inspect.Parameter."""
    __slots__ = ('description',)
    def __init__(self, p):
        import inspect
        K = inspect.Parameter
        if   p.kind == K.VAR_POSITIONAL: self.description = 'param *' + p.name
        elif p.kind == K.VAR_KEYWORD:    self.description = 'param **' + p.name
        elif p.default is inspect.Parameter.empty: self.description = 'param ' + p.name
        else: self.description = 'param %s=%r' % (p.name, p.default)

class _RuntimeSignature:
    """jedi.BaseSignature-shaped stub built from inspect.signature()."""
    def __init__(self, func):
        import inspect
        self._func, self.full_name = func, '%s.%s' % (getattr(func, '__module__', '') or '', getattr(func, '__qualname__', func.__name__))
        try: self.params = [_RuntimeParam(p) for p in inspect.signature(func).parameters.values()]
        except (ValueError, TypeError): self.params = []
    def to_string(self): return '%s(%s)' % (self.full_name.rpartition('.')[-1], ', '.join(p.description.replace('param ', '') for p in self.params))

class _RuntimeName:
    """jedi.Name-shaped stub wrapping a runtime callable. Used by _ast_forwarder for global targets."""
    def __init__(self, func):
        self._func = func
        self.full_name = '%s.%s' % (getattr(func, '__module__', '') or '', getattr(func, '__qualname__', func.__name__))
        self.name = getattr(func, '__name__', '<callable>')
    def get_signatures(self): return [_RuntimeSignature(self._func)]

def synthesize_target_completions(interpreter, code, cursor_pos):
    """
    Query. If cursor is inside a forwarded call, return _ParamCompletion stubs for the target's
    accepted keyword args (one per param, with '=' suffix). Bypasses jedi.complete on synthetic
    code to avoid parso's shared parse-tree corruption.

    Note: jedi.complete() returns 0 results inside `**kwargs`-accepting calls (it punts on
    the ambiguity). The completer compensates by calling synthesize_scope_completions in
    that same context so users still see globals/locals/builtins/keywords as positional
    candidates.
    """
    line = code.count('\n', 0, cursor_pos) + 1
    column = cursor_pos - code.rfind('\n', 0, cursor_pos) - 1
    sigs = interpreter.get_signatures(line, column)
    if not sigs: return []
    targets = _resolve_forwarder_target(interpreter, code, sigs[0])
    if not targets: return []
    out = []
    for t in targets:
        for s in t.get_signatures():
            for p in s.params:
                if p is None: continue
                desc = p.description.replace('param ', '', 1)
                if desc.startswith('*'): continue
                name = desc.split(':', 1)[0].split('=', 1)[0].strip()
                if name: out.append(_ParamCompletion(name + '='))
    return out

def synthesize_scope_completions(interpreter, code, cursor_pos):
    """
    [C] Query. Enumerate in-scope names (interpreter namespaces + builtins + keywords)
    as completion stubs, filtered by the typed prefix at the cursor.

    Used to backfill when jedi.complete() returns nothing inside a `**kwargs`-accepting
    call — we still want users to see globals/locals/builtins so they can pass them
    as positional or kwarg values.

    Returns a list of _ScopeCompletion stubs (jedi.Completion-shaped).
    """
    import builtins, keyword
    line_start = code.rfind('\n', 0, cursor_pos) + 1
    line_text = code[line_start:cursor_pos]
    i = len(line_text)
    while i > 0 and (line_text[i-1].isalnum() or line_text[i-1] == '_'): i -= 1
    prefix = line_text[i:]
    seen, out = set(), []
    for ns in (getattr(interpreter, 'namespaces', ()) or ()):
        for name in ns:
            if not name.startswith(prefix): continue
            if name.startswith('__') and name.endswith('__'): continue
            if name in seen: continue
            seen.add(name)
            out.append(_ScopeCompletion(name, 'statement'))
    for name in dir(builtins):
        if not name.startswith(prefix): continue
        if name.startswith('_'): continue
        if name in seen: continue
        seen.add(name)
        out.append(_ScopeCompletion(name, 'statement'))
    for name in keyword.kwlist:
        if not name.startswith(prefix): continue
        if name in seen: continue
        seen.add(name)
        out.append(_ScopeCompletion(name, 'keyword'))
    return out

class _ScopeCompletion:
    """[C] jedi.Completion-shaped stub for namespace/builtin/keyword items in fallback completions."""
    __slots__ = ('name', 'type')
    def __init__(self, name, ctype): self.name, self.type = name, ctype
    def get_signatures(self): return []
    @property
    def full_name(self): return self.name
