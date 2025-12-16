"""
Simplified Python completer for rp's pseudo terminal.

Based on vanilla ptpython's approach with a few targeted optimizations:
- Fast namespace attribute access (np.array → dir(np) without Jedi)
- Fast import statement completions
- Trusts Jedi's calculations instead of reimplementing everything

Much simpler and more maintainable than the original 900-line version.
"""
from __future__ import unicode_literals

import os
import re
import sys
from cachetools import LRUCache
from rp.prompt_toolkit.completion import Completer, Completion
from rp.prompt_toolkit.document import Document
from rp.prompt_toolkit.buffer import Buffer
from rp.prompt_toolkit.contrib.completers import PathCompleter
from rp.prompt_toolkit.contrib.regular_languages.compiler import compile as compile_grammar
from rp.prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
from rp.rp_ptpython.completion_types import Candidate, CacheInfo
from rp.rp_ptpython.bash_completer import BashCompleter
from rp.rp_ptpython.completion_ranker import rank_jedi_completions, create_sorting_key
from rp.rp_ptpython.jedi_utils import JediInfo, get_jedi_interpreter, get_jedi_display_meta, format_jedi_value_description
import rp
import rp.rp_ptpython.r_iterm_comm as ric

__all__ = ('PythonCompleter', 'CacheInfo', 'Candidate')

# Keywords that shouldn't appear in completions
non_completable_keywords = {
    'class', 'finally', 'is', 'return', 'continue', 'for', 'lambda', 'try',
    'def', 'from', 'nonlocal', 'while', 'and', 'del', 'global', 'not', 'with',
    'as', 'elif', 'if', 'or', 'yield', 'assert', 'else', 'import', 'pass',
    'break', 'except', 'in', 'raise'
}

# Cache of all importable module names
_all_module_names = set(sys.builtin_module_names)


def get_all_importable_module_names():
    """Returns a set of all names that you can use 'import <name>' on."""
    import pkgutil
    
    if _all_module_names:
        def update_thread():
            # Update cache in background thread
            for _, name, _ in pkgutil.iter_modules():
                _all_module_names.add(name)
        
        from threading import Thread
        Thread(target=update_thread, daemon=True).start()
    
    return _all_module_names


def get_word_before_cursor_custom(document):
    """
    Custom word extraction that handles Python identifiers better.
    Returns the identifier before cursor, or empty string if cursor is after non-identifier char.
    """
    text = document.text_before_cursor
    
    # Work backwards from cursor
    i = len(text) - 1
    while i >= 0:
        char = text[i]
        if char.isalnum() or char in '._':
            i -= 1
        else:
            break
    
    output = text[i + 1:]
    return output


def get_last_name(s: str) -> str :
    """
    origin often has punctuation in it like origin=='np.this.that.this'

    Return the longest valid Python identifier suffix from `s`.

    A valid identifier:
      - starts with a letter or underscore
      - followed by letters, digits, or underscores
      - matches at the end of the string

    Returns None if no valid identifier is found.

    Examples:
        >>> get_last_name("foo.bar_baz9") # --> 'bar_baz9'
        >>> get_last_name("hello.123abc") # --> 'abc'
        >>> get_last_name("test.@var")    # --> 'var'
        >>> get_last_name("no_valid!")    # --> ''
        >>> get_last_name("lambda")       # --> 'lambda'
    """
    match = re.search(r'[A-Za-z_][A-Za-z0-9_]*$', s)
    return match.group(0) if match else ''


def create_backspaced_document(document, backspace_count):
    """Create a new document with n characters deleted before cursor."""
    buffer = Buffer(initial_document=document)
    buffer.delete_before_cursor(backspace_count)
    return buffer.document


class CompletionCache:
    """
    LRU cache for ALL completions (not just Jedi).

    Key is (code, cursor_position). Caches:
    - Raw candidate list (before fuzzy matching/ranking)
    - Jedi interpreter (for signatures to reuse)
    """

    def __init__(self):
        self._cache = LRUCache(maxsize=128)

    def has_cache(self, code: str, cursor_pos: int) -> bool:
        """Check if completions are cached for this position."""
        cache_key = (code, cursor_pos)
        return cache_key in self._cache

    def get_or_compute(self, code: str, cursor_pos: int, compute_func):
        """Get completions from cache or compute them."""
        cache_key = (code, cursor_pos)

        if cache_key not in self._cache:
            result = compute_func()
            self._cache[cache_key] = result

        return self._cache[cache_key]

    def get_cached_interpreter(self, code: str, cursor_pos: int):
        """Get cached Jedi interpreter if available (for signatures). Returns JediInfo or None."""
        cache_key = (code, cursor_pos)
        cached = self._cache.get(cache_key)
        if cached and isinstance(cached, dict) and 'interpreter' in cached:
            return JediInfo(interpreter=cached['interpreter'], line=cached['line'], column=cached['column'])
        return None

    def clear(self):
        """Clear the cache. Should be called after each command execution."""
        self._cache.clear()


class PythonCompleter(Completer):
    """
    Simplified completer for Python code.
    
    Uses vanilla ptpython's approach: trust Jedi's calculations.
    Adds a few fast-paths for common patterns.
    """
    
    def __init__(self, get_globals, get_locals, enable_dictionary_completion=lambda: True, allow_jedi_dynamic_imports=lambda: False):
        super().__init__()
        self.get_globals = get_globals
        self.get_locals = get_locals
        self.enable_dictionary_completion = enable_dictionary_completion
        self.allow_jedi_dynamic_imports = allow_jedi_dynamic_imports

        self._bash_completer = BashCompleter()
        self._completion_cache = CompletionCache()

    def _complete_python_while_typing(self, document):
        """Should we complete Python code while typing (not just on Tab)?"""
        char_before = document.char_before_cursor
        return document.text and (char_before.isalnum() or char_before in '_.')
    
    def _complete_path_while_typing(self, document):
        """Should we complete paths while typing?"""
        char_before = document.char_before_cursor
        return document.text and (char_before.isalnum() or char_before in '/.~')

    def clear_cache(self):
        """Clear completion cache. Should be called after each command execution.

        Note: rp.pseudo_terminal calls this at the start of each input.
        Search for: pyin._completer.clear_cache()
        """
        self._completion_cache.clear()

    def has_cached_completions(self, document) -> bool:
        """
        Check if completions are cached for this document position.
        Used to decide whether to compute synchronously (cache hit, fast)
        or asynchronously (cache miss, slow Jedi computation).
        """
        cache_info = self.get_cache_key_for_document(document)
        return self._completion_cache.has_cache(cache_info.cache_text, cache_info.cache_pos)

    def get_cache_key_for_document(self, document) -> CacheInfo:
        """
        Get the cache key (backspaced text, cursor_pos) for a document.
        Used by both completions and signatures to hit the same cache.

        Returns:
            CacheInfo with cache_text, cache_pos, origin, name_origin
        """
        origin = get_word_before_cursor_custom(document)
        name_origin = get_last_name(origin)
        if not name_origin:
            # After dot with no chars yet (e.g., 'numpy.') - don't backspace, keep the dot
            name_origin = ''
        backspace_num = len(name_origin)
        backspaced_doc = create_backspaced_document(document, backspace_num)
        return CacheInfo(cache_text=backspaced_doc.text, cache_pos=backspaced_doc.cursor_position, origin=origin, name_origin=name_origin)

    def _path_completions(self, before_line, dirs_only=False, files_only=False, check_text_files=False, priority_func=None):
        """
        Helper for path-based completions (CD, VIM, CAT, etc).

        Args:
            before_line: Text before cursor
            dirs_only: Only show directories
            files_only: Only show files
            check_text_files: Check if files are text (for VIM)
            priority_func: Function taking PathCandidate, returns priority int (or None for no priority)

        Returns:
            List of Candidate objects
        """
        from rp.rp_ptpython.path_completer_utils import extract_path_components, list_path_candidates
        cmd_prefix = before_line.split()[0] + ' '
        directory, prefix = extract_path_components(before_line, cmd_prefix)
        path_objs = list_path_candidates(directory, prefix, dirs_only=dirs_only, files_only=files_only, check_text_files=check_text_files)

        def make_candidate(c):
            priority = priority_func(c) if priority_func else 0
            return Candidate(name=c.name, priority=priority, is_dir=c.is_dir, is_text_file=c.is_text_file, display_style='path')

        return [make_candidate(c) for c in path_objs]

    def _get_raw_candidates(self, document):
        """
        Get raw completion candidates from various sources.

        Returns:
            dict with:
            - 'candidates': list of candidate strings
            - 'priorities': dict mapping candidate -> priority (optional)
        """
        
        #Common Variables
        before_line = document.current_line_before_cursor
        after_line = document.current_line_after_cursor
        text = document.text
        after = document.text_after_cursor
        before = document.text_before_cursor
        single_line = not '\n' in document.text_before_cursor and not after_line
        shell_mode = document.text.startswith('!')
        scope = rp.merged_dicts(self.get_globals(), self.get_locals(), precedence='last')

        shell_extensions = '.sh', '.bash', '.zsh'
        python_extensions = '.py', '.rpy'
        if shell_mode: script_extensions = shell_extensions
        elif text:     script_extensions = python_extensions
        else:          script_extensions = shell_extensions + python_extensions

        #Priority Functions
        def script_priority(c):
            if c.is_dir:
                return 2  # Folders third
            name_lower = c.name.lower()
            if rp.ends_with_any(name_lower, script_extensions):
                return 0  # Script files first
            if c.is_text_file:
                return 1  # Text files second
            return 3  # Other files last

        # Shell mode - delegate to bash completer
        if shell_mode:
            return self._bash_completer.get_raw_candidates(document)

        #RP Commands
        if single_line:
            if rp.starts_with_any(before, 'PYM ', 'APYM ', 'CDM ')                                                           : return [Candidate(name=name) for name in get_all_importable_module_names()]
            if rp.starts_with_any(before, 'CD ')                                                                             : return self._path_completions(before, dirs_only=True)
            if rp.starts_with_any(before, 'TAKE ', 'MKDIR ')                                                                 : return self._path_completions(before, priority_func=lambda c: 0 if c.is_dir else 1)
            if rp.starts_with_any(before, 'VIM ', 'NVIM ')                                                                   : return self._path_completions(before, check_text_files=True, priority_func=lambda c: 0 if (c.is_dir or c.is_text_file) else 1)
            if rp.starts_with_any(before, 'OPEN ', 'RM ', 'RN ', 'MV ', 'FD ', 'WANS ', 'PIP ')                              : return self._path_completions(before)
            if rp.starts_with_any(before, 'RUN ')                                                                            : return self._path_completions(before, check_text_files=True, priority_func=script_priority)
            if rp.starts_with_any(before, 'CAT ', 'NCAT ', 'CCAT ', 'ACAT ', 'TAB ', 'PY ', 'APY ', 'LSS ', 'LSR ', 'FCOPY '): return self._path_completions(before, priority_func=lambda c: 0 if not c.is_dir else 1)
            if rp.starts_with_any(before, 'CDH '):
                # Show full paths in hints
                history = rp.r._get_cd_history()
                names = rp.r._get_cdh_back_names()
                # Match names to paths
                name_to_path = {}
                for path in reversed(history):
                    folder_name = rp.get_folder_name(path)
                    if folder_name and folder_name not in name_to_path:
                        name_to_path[folder_name] = path
                return [Candidate(name=name, display_meta='Path: ' + name_to_path.get(name, name)) for name in names]
            if rp.starts_with_any(before, 'CDU '):
                pwd = rp.get_current_directory()
                cwd = pwd
                updirs = []
                for _ in range(len(rp.path_split(pwd))):
                    cwd = rp.get_parent_directory(cwd)
                    if rp.get_folder_name(cwd):
                        updirs.append(rp.get_folder_name(cwd))
                return [Candidate(name=name) for name in updirs]

        if '`' in before_line:
            micro_command_arg = before_line.split('`')[-1]
            if not rp.contains_any(micro_command_arg, '"', "'"): #Making sure we're not in a string. Ideally we'd have a better way to know this, like looking at syntax highlighting...
                return self._path_completions(before, check_text_files=True, priority_func=script_priority)

        # Import statements
        if re.fullmatch(r'\s*(from|import)\s+\w*', before_line):
            return [Candidate(name=name) for name in get_all_importable_module_names()]

        # First Word Completions - should be super fast, much faster than Jedi
        if not text:
            python_candidates = [
                Candidate(
                    name=name,
                    priority=0,
                    display=(
                        name + "()"
                        if callable(value)
                        else name + "." if rp.is_a_module(value) else name
                    ),
                )
                for name, value in scope.items()
            ]
            bash_candidates = [
                Candidate(name="!" + name, match_text=name, priority=1)
                for name in rp.r._get_sys_commands_cache #Will not do this eagerly, so that python completions are first and fast...
            ]
            path_candidates = [
                Candidate(name=repr(name), match_text=name, display='./'+name, priority=2)
                for name in os.listdir() #Will not do this eagerly, so that python completions are first and fast...
            ]
            return bash_candidates + python_candidates + path_candidates

        # Jedi completions
        try:
            jedi_info = get_jedi_interpreter(
                document.text,
                document.cursor_position,
                self.get_globals(),
                self.get_locals(),
                allow_dynamic_imports=self.allow_jedi_dynamic_imports()
            )
            jedi_completions = jedi_info.interpreter.complete(jedi_info.line, jedi_info.column)
            def make_display(jc):
                if jc.type in ('function', 'class'):
                    return jc.name + '()'
                elif jc.type == 'module':
                    return jc.name + '.'
                else:
                    return jc.name
            candidates = [Candidate(name=jc.name, display=make_display(jc), display_meta=get_jedi_display_meta(jc, self.get_globals(), self.get_locals())) for jc in jedi_completions]
            # Return both candidates AND interpreter for signature reuse
            return {'candidates': candidates, 'interpreter': jedi_info.interpreter, 'line': jedi_info.line, 'column': jedi_info.column}
        except Exception:
            return []

    def get_completions(self, document, complete_event):
        """
        Get completions with unified caching and ranking.

        Flow:
        1. Special: 'uuuuu' - CD to parent
        2. Get raw candidates (cached) - includes shell, Python, and RP commands
        3. Apply fuzzy matching and ranking
        4. Yield Completion objects
        """

        before_line = document.current_line_before_cursor
        after_line = document.current_line_after_cursor

        # Special: 'uuuuu' → CD to parent directories
        if not after_line and set(before_line) == set('u'):
            cwd = rp.get_current_directory()
            for _ in range(len(before_line)):
                cwd = rp.get_parent_directory(cwd)
            updir = 'CD ' + cwd
            yield Completion(
                text=updir,
                start_position=-10000,
                display='^' + rp.get_folder_name(cwd)
            )
            return

        # Don't complete on empty lines
        if not before_line.strip():
            return

        # Get raw candidates (cached)
        # Extract final identifier for fuzzy matching and backspace document for Jedi
        # (e.g., 'np.arr' -> name_origin='arr', cache at 'np.')
        cache_info = self.get_cache_key_for_document(document)

        result = self._completion_cache.get_or_compute(
            cache_info.cache_text,
            cache_info.cache_pos,
            lambda: self._get_raw_candidates(create_backspaced_document(document, len(cache_info.name_origin)))
        )

        # Extract candidates (handle Jedi format with interpreter vs regular list)
        if isinstance(result, dict) and 'candidates' in result:
            candidate_objs = result['candidates']  # Jedi format
        else:
            candidate_objs = result  # Regular list format

        # Apply fuzzy matching + ranking
        from rp.rp_ptpython.completion_ranker import rank_completions
        user_created_vars = set(ric.rp_pt_user_created_var_names)

        # Use match_text for fuzzy matching (Candidate property handles default to name)
        match_texts = [c.match_text for c in candidate_objs]
        priorities = {match_text: c.priority for match_text, c in zip(match_texts, candidate_objs)}
        ranked_match_texts = rank_completions(match_texts, cache_info.name_origin, user_created_vars, priorities)

        # Create lookup from match_text back to candidate
        match_to_cand = {match_text: c for match_text, c in zip(match_texts, candidate_objs)}

        # Store candidate names (for insertion) for r.py's _autocomplete_lss_name function
        ric.current_candidates = [match_to_cand[mt].name for mt in ranked_match_texts]

        # Yield Completion objects
        for match_text in ranked_match_texts:
            cand = match_to_cand[match_text]
            name = cand.name
            display = cand.display  # Property handles default to name
            display_meta = cand.display_meta

            # Add / suffix and metadata for path completions
            if cand.display_style == 'path':
                if cand.is_dir:
                    display = name + '/'
                    display_meta = 'Directory'
                elif cand.is_text_file is not None:
                    # VIM completions with text file info
                    display_meta = 'Text file' if cand.is_text_file else 'Binary file'

            yield Completion(
                text=name,
                start_position=-len(cache_info.name_origin),
                display=display,
                display_meta=display_meta
            )
