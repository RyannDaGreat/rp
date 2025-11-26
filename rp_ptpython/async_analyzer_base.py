"""
Base class for async code analysis with background thread and difflib position translation.

This consolidates the common async pattern used by Jedi semantic highlighting
and Ruff syntax checking.
"""
from __future__ import unicode_literals
import threading
import time
from difflib import SequenceMatcher

__all__ = ['AsyncAnalyzerBase']


class AsyncAnalyzerBase:
    """
    Base class for async code analyzers.

    Handles:
    - Background thread management with debouncing
    - Cache management
    - difflib-based position translation for instant feedback
    - Redraw triggering

    Subclasses must implement:
    - _analyze(code, *args) -> results
    - _translate_results(old_code, new_code, old_results) -> new_results
    """

    def __init__(self, debounce_interval=0.3, redraw_callback=None):
        """
        Initialize async analyzer.

        Args:
            debounce_interval: Minimum seconds between analysis runs
            redraw_callback: Function to call when new results arrive
        """
        self.debounce_interval = debounce_interval
        self.redraw_callback = redraw_callback

        # Cache
        self.cached_code = ""
        self.cached_results = self._empty_results()

        # Background thread state
        self.lock = threading.Lock()
        self.pending_request = None  # (code, args, timestamp)
        self.last_run = 0
        self.worker_thread = None
        self.worker_running = False

    def _empty_results(self):
        """Return empty results. Override if needed."""
        return None

    def get_results(self, code, *args):
        """
        Get analysis results for code.

        Returns cached results translated via difflib, and ALWAYS schedules
        background analysis (debouncing handles throttling).

        Args:
            code: Code to analyze
            *args: Additional arguments for analysis

        Returns:
            Analysis results (type depends on subclass)
        """
        # Translate cached positions to new code (instant feedback)
        translated = self._translate_results(self.cached_code, code, self.cached_results)

        # Update cache with translated immediately
        with self.lock:
            self.cached_results = translated
            self.cached_code = code

        # ALWAYS schedule background analysis (debouncing prevents spam)
        self._schedule_background_analysis(code, args)

        return translated

    def _translate_results(self, old_code, new_code, old_results):
        """
        Translate results from old code to new code using difflib.

        Subclasses must implement this.

        Args:
            old_code: Previous code string
            new_code: Current code string
            old_results: Results from old code

        Returns:
            Translated results for new code
        """
        raise NotImplementedError("Subclass must implement _translate_results")

    def _analyze(self, code, *args):
        """
        Perform analysis on code.

        Subclasses must implement this. Runs in background thread.

        Args:
            code: Code to analyze
            *args: Additional arguments

        Returns:
            Analysis results
        """
        raise NotImplementedError("Subclass must implement _analyze")

    def _schedule_background_analysis(self, code, args):
        """Schedule background analysis run."""
        now = time.time()

        with self.lock:
            self.pending_request = (code, args, now)

            if not self.worker_running:
                self.worker_running = True
                self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
                self.worker_thread.start()

    def _worker_loop(self):
        """Background worker that processes analysis requests."""
        while True:
            # Check for pending request
            with self.lock:
                if self.pending_request is None:
                    self.worker_running = False
                    break

                code, args, timestamp = self.pending_request
                self.pending_request = None

            # Debounce: wait until debounce_interval since last run
            now = time.time()
            time_since_last = now - self.last_run
            if time_since_last < self.debounce_interval:
                time.sleep(self.debounce_interval - time_since_last)

            # Run analysis
            results = self._analyze(code, *args)

            # Update cache ONLY if still current code
            with self.lock:
                if self.pending_request is None:
                    # No pending request, this is latest - update cache
                    self.cached_code = code
                    self.cached_results = results
                    self.last_run = time.time()
                    should_redraw = True
                else:
                    # Newer request pending, discard stale results
                    should_redraw = False

            # Trigger redraw if we updated cache
            if should_redraw and self.redraw_callback:
                try:
                    self.redraw_callback()
                except:
                    pass  # Don't crash worker if redraw fails


def build_line_map_difflib(old_code, new_code):
    """
    Build line mapping from old code to new code using difflib.

    Returns dict mapping old_line_num (1-indexed) -> (new_line_num, col_offset).
    Useful for subclass implementations of _translate_results.

    Args:
        old_code: Old code string
        new_code: New code string

    Returns:
        Dictionary: {old_line: (new_line, col_offset)}
    """
    if not old_code:
        return {}

    old_lines = old_code.splitlines(keepends=True)
    new_lines = new_code.splitlines(keepends=True)

    if not old_lines:
        return {}

    matcher = SequenceMatcher(None, old_lines, new_lines)
    line_map = {}

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # Lines unchanged - direct mapping
            for offset in range(i2 - i1):
                old_line_idx = i1 + offset
                new_line_idx = j1 + offset
                line_map[old_line_idx + 1] = (new_line_idx + 1, 0)

        elif tag == 'replace':
            # Lines changed - map what we can with column offset
            num_mapped = min(i2 - i1, j2 - j1)
            for offset in range(num_mapped):
                old_line_idx = i1 + offset
                new_line_idx = j1 + offset
                old_line = old_lines[old_line_idx]
                new_line = new_lines[new_line_idx]
                col_offset = _compute_column_offset(old_line, new_line)
                line_map[old_line_idx + 1] = (new_line_idx + 1, col_offset)

    return line_map


def _compute_column_offset(old_line, new_line):
    """Compute column offset between old and new line."""
    # Find length of common prefix
    common_prefix_len = 0
    for i, (old_char, new_char) in enumerate(zip(old_line, new_line)):
        if old_char == new_char:
            common_prefix_len = i + 1
        else:
            break

    # If prefix very short, don't trust it
    if common_prefix_len < 3:
        # Try to find common substring
        matcher = SequenceMatcher(None, old_line, new_line)
        match = matcher.find_longest_match(0, len(old_line), 0, len(new_line))
        if match.size >= 3:
            return match.b - match.a
        return 0

    # Lines share good prefix - no column offset
    return 0
