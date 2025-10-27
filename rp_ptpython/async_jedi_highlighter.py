"""
Async semantic highlighting using Jedi with difflib-based position syncing.

Runs Jedi analysis in background thread (min 0.3s interval) and uses difflib to translate
cached positions when code changes slightly.
"""
from __future__ import unicode_literals
import threading
import time
from difflib import SequenceMatcher

__all__ = ['AsyncJediHighlighter']


class AsyncJediHighlighter:
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
        self.redraw_callback = redraw_callback

        # Cache: (code_text, callable_pos, module_pos, unused_pos)
        self.cached_code = ""
        self.cached_results = (set(), set(), set())

        # Background thread state
        self.lock = threading.Lock()
        self.pending_request = None  # (code, globals_dict, locals_dict, timestamp)
        self.last_jedi_run = 0  # timestamp of last Jedi run
        self.worker_thread = None
        self.worker_running = False

    def get_highlights(self, code, globals_dict, locals_dict):
        """
        Get semantic highlights for code.

        Returns cached results translated via difflib, and schedules
        background Jedi run if needed.

        Args:
            code: Python code string
            globals_dict: Global namespace
            locals_dict: Local namespace

        Returns:
            Tuple of (callable_positions, module_positions, unused_var_positions)
            Each is a set of (line, column, length) tuples.
        """
        # If code unchanged, return cached results immediately
        if code == self.cached_code:
            return self.cached_results

        # Use difflib to translate cached positions to new code
        translated_results = self._translate_positions(self.cached_code, code, self.cached_results)

        # Update cached_results with translated positions immediately
        # This ensures get_line_with_highlights uses translated positions
        # until background Jedi completes
        with self.lock:
            self.cached_results = translated_results
            self.cached_code = code

        # Schedule background Jedi run (debounced to 0.3s)
        self._schedule_background_jedi(code, globals_dict, locals_dict)

        return translated_results

    def _translate_positions(self, old_code, new_code, old_results):
        """
        Translate positions from old code to new code using difflib.

        Args:
            old_code: Previous code string
            new_code: Current code string
            old_results: Tuple of (callable_pos, module_pos, unused_pos) sets

        Returns:
            Translated tuple of position sets
        """
        if not old_code or not old_results or not any(old_results):
            return (set(), set(), set())

        # Split into lines
        old_lines = old_code.splitlines(keepends=True)
        new_lines = new_code.splitlines(keepends=True)

        # Edge case: if no lines, return empty
        if not old_lines:
            return (set(), set(), set())

        # Compute line-by-line diff
        matcher = SequenceMatcher(None, old_lines, new_lines)

        # Build mapping: old_line_num (1-indexed) -> (new_line_num, column_offset)
        # Strategy: Process opcodes and track cumulative line shift
        line_map = {}

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                # Lines unchanged - direct mapping with any accumulated shift
                for offset in range(i2 - i1):
                    old_line_idx = i1 + offset  # 0-indexed array position
                    new_line_idx = j1 + offset  # 0-indexed array position
                    # Jedi uses 1-indexed line numbers
                    line_map[old_line_idx + 1] = (new_line_idx + 1, 0)

            elif tag == 'replace':
                # Lines changed - try to map what we can with column offset
                # Map line-by-line up to the shorter range
                num_mapped = min(i2 - i1, j2 - j1)
                for offset in range(num_mapped):
                    old_line_idx = i1 + offset
                    new_line_idx = j1 + offset
                    old_line = old_lines[old_line_idx]
                    new_line = new_lines[new_line_idx]
                    col_offset = self._compute_column_offset(old_line, new_line)
                    line_map[old_line_idx + 1] = (new_line_idx + 1, col_offset)

            elif tag == 'insert':
                # New lines inserted - old lines don't exist here, but this shifts
                # subsequent lines. The shift is handled by the 'equal' blocks that follow.
                pass

            elif tag == 'delete':
                # Old lines deleted - these old lines have no mapping
                # The shift is handled by subsequent 'equal' blocks
                pass

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

    def _compute_column_offset(self, old_line, new_line):
        """
        Compute column offset between old and new line.

        Returns offset to add to old column positions.
        Uses common prefix to determine how much content shifted.
        """
        # Find length of common prefix
        common_prefix_len = 0
        for i, (old_char, new_char) in enumerate(zip(old_line, new_line)):
            if old_char == new_char:
                common_prefix_len = i + 1
            else:
                break

        # If prefix is very short (< 3 chars), don't trust it
        # This handles cases where lines are completely different
        if common_prefix_len < 3:
            # Try to find any common substring using difflib
            matcher = SequenceMatcher(None, old_line, new_line)
            match = matcher.find_longest_match(0, len(old_line), 0, len(new_line))
            if match.size >= 3:
                # Offset is difference in starting positions
                return match.b - match.a
            # Lines too different - return 0 (no offset)
            return 0

        # Lines share a good prefix - no column offset needed
        return 0

    def _schedule_background_jedi(self, code, globals_dict, locals_dict):
        """
        Schedule background Jedi run (debounced to 0.3s min interval).
        """
        now = time.time()

        with self.lock:
            # Store pending request
            self.pending_request = (code, globals_dict, locals_dict, now)

            # Start worker thread if not running
            if not self.worker_running:
                self.worker_running = True
                self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
                self.worker_thread.start()

    def _worker_loop(self):
        """Background worker that processes Jedi requests."""
        while True:
            # Check for pending request
            with self.lock:
                if self.pending_request is None:
                    self.worker_running = False
                    break

                code, globals_dict, locals_dict, timestamp = self.pending_request
                self.pending_request = None

            # Debounce: wait until 0.3 seconds since last run
            # (reduced from 1.0s to make highlighting more responsive)
            now = time.time()
            time_since_last = now - self.last_jedi_run
            if time_since_last < 0.3:
                time.sleep(0.3 - time_since_last)

            # Run Jedi analysis
            results = self._run_jedi(code, globals_dict, locals_dict)

            # Update cache ONLY if this is still the current code
            # If code changed while we were running Jedi, discard stale results
            with self.lock:
                # Check if there's a pending request (newer code came in)
                if self.pending_request is None:
                    # No pending request, this is the latest - update cache
                    self.cached_code = code
                    self.cached_results = results
                    self.last_jedi_run = time.time()
                    should_redraw = True
                else:
                    # Newer request pending, discard these stale results
                    should_redraw = False

            # Trigger redraw only if we updated cache
            if should_redraw and self.redraw_callback:
                try:
                    self.redraw_callback()
                except:
                    pass  # Don't crash worker if redraw fails

    def _run_jedi(self, code, globals_dict, locals_dict):
        """
        Run Jedi analysis (in background thread).

        Returns tuple of (callable_pos, module_pos, unused_pos) sets.
        """
        import jedi
        import re

        if not code.strip():
            return (set(), set(), set())

        try:
            # Use Interpreter with runtime namespaces
            interpreter = jedi.Interpreter(code, namespaces=[globals_dict, locals_dict])

            callable_positions = set()
            module_positions = set()

            # Tokenize code to find ALL identifiers (including attribute access)
            # get_names() misses attribute access like obj.method or obj.__call__
            lines = code.splitlines()

            for line_idx, line_text in enumerate(lines):
                line_num = line_idx + 1  # Jedi uses 1-indexed lines

                # Find all word tokens (identifiers) on this line
                for match in re.finditer(r'\b(\w+)\b', line_text):
                    token_text = match.group(1)
                    col_start = match.start()  # Start column for position storage
                    # Infer at the END of the token so Jedi has full context
                    # e.g., for 'load_image', infer at the 'e' not the 'l'
                    col_infer = match.end() - 1  # Column to infer at

                    try:
                        # Infer type at END of token (Jedi uses 0-indexed columns)
                        inferred = interpreter.infer(line=line_num, column=col_infer)

                        if inferred:
                            name_type = inferred[0].type
                            # Store position at START of token (matches Pygments)
                            pos = (line_num, col_start, len(token_text))

                            # Check if callable
                            if name_type in ('function', 'class'):
                                callable_positions.add(pos)
                            elif name_type == 'instance':
                                # instance can be callable (methods, __call__, etc.)
                                # Check full_name for known callable patterns
                                full_name = getattr(inferred[0], 'full_name', '')
                                if ('__call__' in full_name or
                                    'method' in str(inferred[0]).lower() or
                                    'function' in full_name):
                                    callable_positions.add(pos)
                            elif name_type == 'module':
                                module_positions.add(pos)
                    except:
                        pass

            # TODO: unused variable detection
            unused_var_positions = set()

            return (callable_positions, module_positions, unused_var_positions)

        except Exception:
            return (set(), set(), set())
