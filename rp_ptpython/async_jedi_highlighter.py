"""
Async semantic highlighting using Jedi with difflib-based position syncing.

Runs Jedi analysis in background thread (min 0.3s interval) and uses difflib to translate
cached positions when code changes slightly.
"""
from __future__ import unicode_literals
from rp.rp_ptpython.async_analyzer_base import AsyncAnalyzerBase, build_line_map_difflib
import builtins

__all__ = ['AsyncJediHighlighter']


class AsyncJediHighlighter(AsyncAnalyzerBase):
    """
    Background Jedi analyzer with difflib-based position translation.

    Instead of running Jedi synchronously on every keystroke, this:
    1. Caches last Jedi results + code they were computed for
    2. Uses difflib to translate cached positions to new code
    3. Runs Jedi in background thread (debounced to 0.3s min interval)
    4. Triggers redraw when new results arrive
    """

    def __init__(self, redraw_callback=None):
        """
        Initialize async highlighter.

        Args:
            redraw_callback: Optional function to call when new results arrive
        """
        super().__init__(debounce_interval=0.3, redraw_callback=redraw_callback)
        self.enable_treesitter = True  # Current state of tree-sitter highlighting
        self.enable_jedi = True  # Current state of Jedi highlighting

    def _empty_results(self):
        """Return empty Jedi results: (callables, modules, unused, parameters, unreachable, kwargs, globals, locals, nonlocals)."""
        return (set(), set(), set(), set(), set(), set(), set(), set(), set())

    def get_highlights(self, code, globals_dict, locals_dict, enable_treesitter=True, enable_jedi=True):
        """
        Get semantic highlights for code.

        Tree-sitter results (parameters, kwargs) are computed immediately and cached.
        Jedi results (callables, modules, etc) come from cache and update in background.

        Args:
            code: Python code string
            globals_dict: Global namespace
            locals_dict: Local namespace
            enable_treesitter: If True, compute tree-sitter highlights (params, kwargs)
            enable_jedi: If True, compute Jedi highlights (callables, modules, etc)
        """
        # Store flags for background thread to use
        self.enable_treesitter = enable_treesitter
        self.enable_jedi = enable_jedi

        # Fast: compute tree-sitter results immediately (~1ms)
        parameter_positions = set()
        kwarg_positions = set()
        global_positions = set()
        local_positions = set()
        nonlocal_positions = set()

        if enable_treesitter:
            from rp.rp_ptpython.treesitter_semantic import (
                parse_code, extract_parameter_positions, extract_kwarg_positions, extract_scope_positions
            )
            try:
                ts_tree = parse_code(code)
                parameter_positions = extract_parameter_positions(ts_tree, code)
                kwarg_positions = extract_kwarg_positions(ts_tree, code)
                global_positions, local_positions, nonlocal_positions = extract_scope_positions(ts_tree, code)
            except:
                pass

        # Get cached Jedi results (will be empty/stale on first call)
        if enable_jedi:
            jedi_results = self.get_results(code, globals_dict, locals_dict)
            # Jedi provides: callables, modules, unused_vars, (old params), unreachable, (old kwargs), (old globals), (old locals), (old nonlocals)
            # We ignore old params/kwargs/globals/locals/nonlocals from Jedi - tree-sitter handles those now
            (callable_positions, module_positions, unused_var_positions, _,
             unreachable_positions, _, _, _, _) = jedi_results
        else:
            # Jedi disabled - use empty sets
            callable_positions = set()
            module_positions = set()
            unused_var_positions = set()
            unreachable_positions = set()

        # Merge: tree-sitter (params, kwargs, scopes) + Jedi (callables, modules, unused)
        merged_results = (callable_positions, module_positions, unused_var_positions,
                         parameter_positions, unreachable_positions, kwarg_positions,
                         global_positions, local_positions, nonlocal_positions)

        # CRITICAL: Update cached_results immediately so lexer sees tree-sitter results now
        with self.lock:
            self.cached_results = merged_results
            self.cached_code = code

        # Trigger immediate redraw to show tree-sitter highlighting
        if self.redraw_callback:
            self.redraw_callback()

        # Background thread will update cached_results again when Jedi completes (if enabled),
        # triggering another redraw with full results
        return merged_results

    def _translate_results(self, old_code, new_code, old_results):
        """Translate Jedi position sets using difflib line mapping."""
        if not old_code or not old_results or not any(old_results):
            return (set(), set(), set(), set(), set(), set(), set(), set(), set())

        # Build line mapping
        line_map = build_line_map_difflib(old_code, new_code)

        # Translate all position sets
        def translate_set(pos_set):
            result = set()
            for line, col, length in pos_set:
                if line in line_map:
                    new_line, col_offset = line_map[line]
                    new_col = max(0, col + col_offset)
                    result.add((new_line, new_col, length))
            return result

        return tuple(translate_set(s) for s in old_results)

    def _analyze(self, code, globals_dict, locals_dict):
        """
        Run Jedi analysis (in background thread).

        Also re-computes tree-sitter results to ensure they're in sync with Jedi results.

        Returns tuple of (callable_pos, module_pos, unused_pos, parameter_pos, unreachable_pos,
                         kwarg_pos, global_pos, local_pos, nonlocal_pos) sets.
        """
        import jedi
        import re
        from rp.rp_ptpython.unreachable_detector import get_unreachable_positions
        from rp.rp_ptpython.treesitter_semantic import parse_code, extract_parameter_positions, extract_kwarg_positions

        if not code.strip():
            return (set(), set(), set(), set(), set(), set(), set(), set(), set())

        try:
            # Compute tree-sitter results (if enabled)
            parameter_positions = set()
            kwarg_positions = set()
            global_positions = set()
            local_positions = set()
            nonlocal_positions = set()

            if self.enable_treesitter:
                from rp.rp_ptpython.treesitter_semantic import (
                    parse_code, extract_parameter_positions, extract_kwarg_positions, extract_scope_positions
                )
                try:
                    ts_tree = parse_code(code)
                    parameter_positions = extract_parameter_positions(ts_tree, code)
                    kwarg_positions = extract_kwarg_positions(ts_tree, code)
                    global_positions, local_positions, nonlocal_positions = extract_scope_positions(ts_tree, code)
                except:
                    pass

            # Use Interpreter for other semantic analysis (if Jedi enabled)
            if not self.enable_jedi:
                # Jedi disabled - return tree-sitter results only
                return (set(), set(), set(), parameter_positions, set(), kwarg_positions,
                        global_positions, local_positions, nonlocal_positions)

            interpreter = jedi.Interpreter(code, namespaces=[globals_dict, locals_dict])

            # OPTIMIZATION: Use get_names() once instead of many infer() calls
            callable_positions = set()
            module_positions = set()
            unused_var_positions = set()

            try:
                # Get ALL names at once (much faster than individual calls)
                all_names = interpreter.get_names(all_scopes=True, definitions=True, references=True)

                # Build position lookups
                name_positions = {}  # {(line, col): (name_obj, type)}
                param_definitions = {}  # {param_name: [(line, col)]}

                for name in all_names:
                    pos_key = (name.line, name.column)
                    name_positions[pos_key] = (name, name.type)

                    # Track parameter definitions for unused detection
                    if name.type == 'param' and name.is_definition():
                        if name.name not in param_definitions:
                            param_definitions[name.name] = []
                        param_definitions[name.name].append((name.line, name.column))

                # Detect unused parameters
                for param_name, def_positions in param_definitions.items():
                    # Count references to this parameter
                    ref_count = sum(1 for name in all_names
                                  if name.name == param_name and name.type in ('param', 'statement'))

                    # If only 1 reference (the definition), it's unused
                    if ref_count <= len(def_positions):
                        for line, col in def_positions:
                            unused_var_positions.add((line, col, len(param_name)))
            except:
                pass

            # Still need to scan for callables/modules with infer() for accuracy
            # But we can be smarter about it - only check likely candidates
            lines = code.splitlines()
            for line_idx, line_text in enumerate(lines):
                line_num = line_idx + 1

                # Only check tokens that look like they might be callables/modules
                for match in re.finditer(r'\b([A-Za-z_]\w*)\b', line_text):
                    token_text = match.group(1)
                    col_start = match.start()

                    # Skip if already identified as parameter
                    if (line_num, col_start, len(token_text)) in parameter_positions:
                        continue

                    # Skip common keywords
                    if token_text in ('def', 'class', 'return', 'if', 'else', 'elif',
                                     'for', 'while', 'import', 'from', 'as', 'in',
                                     'and', 'or', 'not', 'is', 'True', 'False', 'None'):
                        continue

                    try:
                        col_infer = match.end() - 1
                        inferred = interpreter.infer(line=line_num, column=col_infer)

                        if inferred:
                            name_type = inferred[0].type
                            full_name = getattr(inferred[0], 'full_name', '')

                            # #EXAMPLES OF full_name:
                            #     builtins.list
                            #     __main__.get_jedi_tokens
                            #     builtins.list
                            #     builtins.int

                            pos = (line_num, col_start, len(token_text))

                            if not full_name.startswith('builtins.'): 
                                # print(full_name)
                                #Leave builtins's highlighting the same...if its a builtin
                                if name_type in ('function', 'class'):
                                    callable_positions.add(pos)
                                elif name_type == 'module':
                                    module_positions.add(pos)
                                elif name_type == 'instance':
                                    # Check if it's a callable instance
                                    if ('__call__' in full_name or
                                        'method' in str(inferred[0]).lower() or
                                        'function' in full_name):
                                        callable_positions.add(pos)
                    except:
                        pass

            # Detect unreachable code
            unreachable_positions = get_unreachable_positions(code)

            # Tree-sitter already computed globals/locals/nonlocals above
            # Return all results: Jedi (callables, modules, unused) + tree-sitter (params, kwargs, scopes, unreachable)
            return (callable_positions, module_positions, unused_var_positions,
                    parameter_positions, unreachable_positions, kwarg_positions,
                    global_positions, local_positions, nonlocal_positions)

        except Exception:
            return (set(), set(), set(), set(), set(), set(), set(), set(), set())
