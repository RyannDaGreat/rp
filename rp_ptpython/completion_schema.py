"""
Program-specific bash completion schema system.

This module provides an extensible framework for defining command-specific completions
in shell mode. It uses the bash lexer to understand command structure and provides
caching for expensive operations.

Example usage:
    >>> # Define a completion for 'conda activate'
    >>> @register_completion_schema('conda')
    >>> def conda_completions(tokens, cursor_token_idx):
    ...     if len(tokens) >= 2 and tokens[1].text == 'activate':
    ...         return get_conda_environments()
    ...     return None
"""
from __future__ import unicode_literals
import os
import subprocess
import time
import re
from threading import Lock

__all__ = (
    'get_completions_for_command',
    'register_completion_schema',
    'clear_cache',
    'PROGRAM_DESCRIPTIONS',
    'get_bash_origin',
)


# ==============================================================================
# COMPLETION SCHEMA DOCUMENTATION
# ==============================================================================
"""
This module defines completion schemas for shell commands. Each schema function
returns completions in a specific format that completer.py uses to provide
context-aware suggestions.

## Return Format

Completion functions should return dictionaries with descriptions:

1. **Dictionary (with descriptions)** - REQUIRED:
   - Format: {item: description, ...}
   - ALL flags and subcommands MUST use this format
   - completer.py detects this via isinstance(result, dict)
   - Example: {'--verbose': 'print detailed output', '-a': '-a/--all: show all files'}

2. **Lists are deprecated** - DO NOT USE:
   - Lists without descriptions provide poor user experience
   - ALL new completions must use dictionaries
   - Exception: Dynamic values like environment names can still use lists if descriptions don't add value

## Path Completions

The `_complete_paths()` helper function provides filesystem path completions with proper
shell escaping. It can be used as a fallback when no flag completions are appropriate.

**Usage Pattern**:
```python
@register_completion_schema('command')
def command_completions(tokens, cursor_token_idx, is_after):
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {...}  # Return flag completions
    return _complete_paths(tokens, cursor_token_idx, is_after)  # Fallback to path completions
```

**Features**:
- Returns dict with {quoted_path: 'File'} or {quoted_path: 'Folder'}
- Automatically quotes paths using shlex.quote() for shell safety
- Appends '/' to directory paths
- Supports ~ expansion and relative/absolute paths
- Returns None if no paths match

## Flag Description Format

**CRITICAL**: When flags have aliases (like -a/--all), the dict KEY stays as the flag itself,
but the VALUE (description) mentions both forms in the description text.

### The Pattern:
```python
{
    '-a': '-a/--all: show hidden and . files',
    '--all': '--all/-a: show hidden and . files'
}
```

### Key Points:
- **Dictionary KEY**: The actual flag being completed (e.g., '-a' or '--all')
- **Dictionary VALUE**: Description that mentions BOTH forms of the flag
- **Short flag description**: Start with short form first: '-a/--all: description'
- **Long flag description**: Start with long form first: '--all/-a: description'
- **Single form flags**: Just use the flag once: '--verbose: print detailed output'

### Why This Matters:
- The completion TEXT shown to the user is the KEY (e.g., '-a')
- The description VALUE tells the user about the alias (e.g., '-a/--all: description')
- This means when completing '-a', the user sees: "-a" with description "-a/--all: description"
- When completing '--all', the user sees: "--all" with description "--all/-a: description"

### Complete Example:
```python
@register_completion_schema('ls')
def ls_completions(tokens, cursor_token_idx, is_after=False):
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            # Both forms get entries, with descriptions mentioning both
            '-a': '-a/--all: show hidden and . files',
            '--all': '--all/-a: show hidden and . files',
            '-l': '-l: long format with details',  # No alias
            '-h': '-h/--human-readable: sizes in K, M, G',
            '--human-readable': '--human-readable/-h: sizes in K, M, G',
        }
    # Fallback to path completions (returns dict with descriptions)
    return _complete_paths(tokens, cursor_token_idx, is_after)
```

## Program Name Descriptions

When returning program/command completions (top-level), use short descriptions
that indicate where to find help:

### Format Guidelines:
- Format: 'git': 'distributed version control (git --help)'
- Format: 'ls': 'list directory contents (man ls)'
- Format: 'docker': 'container management (docker --help)'
- Keep descriptions under 50 characters when possible for clean display
- Always mention where to get help: (command --help) or (man command)

### Example:
```python
@register_completion_schema('program_names')
def program_completions(tokens, cursor_token_idx, is_after=False):
    return {
        'git': 'distributed version control (git --help)',
        'docker': 'container management (docker --help)',
        'ls': 'list directory contents (man ls)',
        'grep': 'search text patterns (man grep)',
    }
```

## Best Practices

1. **Prioritize cryptic flags**: Single-letter flags like -a, -l, -r need
   descriptions most because their meaning isn't obvious.

2. **Be concise but clear**: Describe what the flag DOES, not just what it
   stands for:
   - Good: '-r: recursively process directories'
   - Bad: '-r: recursive'
   - Bad: '-r: the recursive flag'

3. **Use consistent terminology**: Match the program's own help text when
   possible.

4. **Group related flags**: When defining multiple related flags, use similar
   phrasing:
   - '-v': '-v/--verbose: print detailed output'
   - '--verbose': '--verbose/-v: print detailed output'
   - '-q': '-q/--quiet: suppress output'
   - '--quiet': '--quiet/-q: suppress output'

5. **Indicate relationships**: When flags are aliases or similar:
   - '--silent: same as --quiet'
   - '-h: same as --help'

6. **ALWAYS include both forms**: If a flag has both short and long forms,
   BOTH must be in the dictionary as separate keys, each with their own
   description that mentions both forms.

## Detection in completer.py

The completer.py module checks the return type to determine if descriptions
are available:

```python
result = get_completions_for_command(tokens, cursor_idx)
if isinstance(result, dict):
    # Show completions with descriptions
    # The KEY is the completion text, VALUE is the description
    for item, description in result.items():
        display_completion_with_description(item, description)
else:
    # Show simple list
    for item in result:
        display_completion(item)
```

## Path Completion

Completion functions should call `_complete_paths()` as a fallback when not in
flag context. This provides filesystem-aware completions with automatic handling
of escaping and styling.

### Automatic Escaping

Paths returned by `_complete_paths()` are automatically quoted using `shlex.quote()`
for shell safety. This ensures paths with spaces, special characters, or other
shell metacharacters are properly escaped when inserted into the command line.

Examples:
- `/home/user/my file.txt` becomes `/home/user/my\ file.txt`
- `/path/with'quotes.txt` becomes `/path/with'quotes.txt`

### Folder vs File Distinction

The path completion system differentiates between folders and files:

- **Folders**: Get "Folder" description and display in bold automatically
- **Files**: Get "File" description with normal styling

The bold styling is implemented via a custom token system added to menus.py.
When completer.py sees description == 'Folder', it passes:
  display=[(Token.Menu.Completions.Completion.Folder, text)]
instead of just a plain string.

### Flag Context Detection

The `_is_flag_context()` helper function determines whether the current cursor
position is in a context where flag completions are appropriate.

**Important**: `_is_flag_context()` ONLY returns True when the current token
starts with '-'. It does NOT return True for positions after flags that expect
arguments.

Example behavior:
```python
# Returns True (cursor on a token starting with '-'):
'git commit -'
'ls --ver'

# Returns False (cursor not on a flag):
'git commit '
'ls --name '
'cd /home/user'
```

This ensures that path completions are shown when appropriate (e.g., after flags
that take file arguments) rather than defaulting to flag completions.

## How to Add a New Command Completion (Step-by-Step for Future Claude Instances)

### Step 1: Define the Completion Function

Create a function decorated with `@register_completion_schema('command_name')`:

```python
@register_completion_schema('mycommand')
def _mycommand_completions(tokens, cursor_token_idx, is_after):
    \"\"\"Completion schema for mycommand with helpful descriptions.\"\"\"
    # Your completion logic here
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-f': '-f/--flag: description of flag',
            '--flag': '--flag/-f: description of flag',
        }
    return _complete_paths(tokens, cursor_token_idx, is_after)
```

### Step 2: Add Program Description (if top-level command)

Add the command to `PROGRAM_DESCRIPTIONS` dictionary (around line 402):

```python
PROGRAM_DESCRIPTIONS = {
    # ... existing entries ...
    'mycommand': 'brief description (mycommand --help)',
}
```

### Step 3: Implement Flag Completions

Return a dictionary with ALL flags (both short and long forms):

```python
if _is_flag_context(tokens, cursor_token_idx, is_after):
    return {
        # Include BOTH forms with descriptions mentioning both
        '-a': '-a/--all: process all items',
        '--all': '--all/-a: process all items',

        # Flags without aliases
        '--verbose': 'print detailed output (man mycommand)',

        # Multi-way aliases (like -r/-R/--recursive)
        '-r': '-r/-R/--recursive: process directories recursively',
        '-R': '-r/-R/--recursive: process directories recursively',
        '--recursive': '--recursive/-r/-R: process directories recursively',
    }
```

### Step 4: Implement Subcommand Logic (if needed)

For commands with subcommands (like `git commit`, `docker run`):

```python
@register_completion_schema('mycommand')
def _mycommand_completions(tokens, cursor_token_idx, is_after):
    \"\"\"Completion schema for mycommand.\"\"\"

    # Get the subcommand (token at index 1)
    subcommand = tokens[1].text if len(tokens) > 1 else ''

    # Check for flags first
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        # Return subcommand-specific flags
        if subcommand == 'build':
            return {
                '--output': '--output/-o: specify output directory',
                '-o': '--output/-o: specify output directory',
            }
        elif subcommand == 'run':
            return {
                '--detach': '--detach/-d: run in background',
                '-d': '--detach/-d: run in background',
            }
        # Common flags for all subcommands
        return {
            '--help': 'show help message',
            '--version': 'show version',
        }

    # At position 0, complete subcommand names with descriptions
    if _complete_at_position_zero(tokens, cursor_token_idx):
        return {
            'build': 'build the project',
            'run': 'run the application',
            'test': 'run tests',
            'deploy': 'deploy to production',
        }

    # Otherwise, complete file paths
    return _complete_paths(tokens, cursor_token_idx, is_after)
```

### Step 5: Test Your Completion

Run the test suite to ensure your completion doesn't break existing functionality:

```bash
/opt/homebrew/opt/python@3.10/bin/python3.10 -m pytest test_completion_schema.py -v
```

### Step 6: Add to Documentation

Add your command to the appropriate section in:
- COMPLETION_IMPLEMENTATION_SUMMARY.md (if it exists)
- The module docstring above

### Helper Functions Available

- `_is_flag_context(tokens, cursor_token_idx, is_after)` - Returns True if cursor is on a flag
- `_complete_at_position_zero(tokens, cursor_token_idx)` - Returns True if completing first argument
- `_complete_paths(tokens, cursor_token_idx, is_after)` - Returns path completions with descriptions
- `_get_current_token_text(tokens, cursor_token_idx)` - Gets the text being completed
- `get_cached_result(key, compute_fn, ttl)` - Caches expensive computations

### Common Patterns

**Pattern 1: Simple flag-only command**
```python
@register_completion_schema('simple')
def _simple_completions(tokens, cursor_token_idx, is_after):
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {'-v': '--verbose: detailed output', '--verbose': '--verbose/-v: detailed output'}
    return None
```

**Pattern 2: Command with file arguments**
```python
@register_completion_schema('filecommand')
def _filecommand_completions(tokens, cursor_token_idx, is_after):
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {'-f': 'force operation'}
    return _complete_paths(tokens, cursor_token_idx, is_after)
```

**Pattern 3: Command with dynamic completions**
```python
@register_completion_schema('dynamic')
def _dynamic_completions(tokens, cursor_token_idx, is_after):
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {'-e': 'specify environment'}

    # Complete environment names dynamically with descriptions
    def get_envs():
        return {
            'prod': 'production environment',
            'staging': 'staging environment',
            'dev': 'development environment',
        }

    return get_cached_result('dynamic_envs', get_envs, ttl=60)
```

### Checklist Before Committing

- [ ] Function decorated with `@register_completion_schema('command')`
- [ ] Function follows naming convention `_commandname_completions`
- [ ] ALL flags return dictionaries with descriptions (NO LISTS)
- [ ] ALL subcommands return dictionaries with descriptions (NO LISTS)
- [ ] ALL flags with aliases have BOTH entries in dict
- [ ] Descriptions mention both forms: `-a/--all: description`
- [ ] NO duplicate keys in any dictionary
- [ ] All common_flags are dictionaries (not lists)
- [ ] Falls back to `_complete_paths()` when appropriate
- [ ] Program added to `PROGRAM_DESCRIPTIONS` if top-level
- [ ] Tests pass: `pytest test_completion_schema.py -v`
- [ ] Docstring explains what the command does
- [ ] No syntax errors: `python3.10 -m py_compile completion_schema.py`

## CRITICAL REQUIREMENTS (DO NOT SKIP)

**When adding or updating ANY completion schema:**

1. ✅ **ALL command flags** must return dicts with descriptions
2. ✅ **ALL subcommands** must return dicts with descriptions
3. ✅ **ALL nested subcommands** must have descriptions
4. ✅ **ALL common_flags** must be dicts (not lists)
5. ✅ **ALL _combine_flags calls** must handle dicts correctly
6. ✅ **NO duplicate keys** anywhere
7. ✅ **Proper short/long flag cross-referencing** (e.g., `-a/--all: description`)

**If you see a list being returned for flags or subcommands - CONVERT IT TO A DICT!**
"""


# Dictionary of common programs with descriptions
PROGRAM_DESCRIPTIONS = {
    'git': 'version control (git --help)',
    'ls': 'list directory (man ls)',
    'vim': 'text editor (vim --help)',
    'grep': 'search text (man grep)',
    'find': 'search files (man find)',
    'tar': 'archive tool (tar --help)',
    'docker': 'containers (docker --help)',
    'npm': 'node packages (npm --help)',
    'python': 'interpreter (python --help)',
    'rp': 'ryan\'s python shell (rp --help)',
    'claude': 'Claude AI CLI (claude --help)',
    'gemini': 'Gemini AI CLI (gemini --help)',
    'cargo': 'rust packages (cargo --help)',
    'kubectl': 'kubernetes (kubectl --help)',
    'ssh': 'remote shell (man ssh)',
    'curl': 'transfer data (curl --help)',
    'wget': 'download files (wget --help)',
    'rsync': 'sync files (man rsync)',
    'cp': 'copy files (man cp)',
    'mv': 'move files (man mv)',
    'rm': 'remove files (man rm)',
    'cat': 'concatenate (man cat)',
    'ps': 'process status (man ps)',
    'top': 'process monitor (man top)',
    'htop': 'interactive process viewer (htop --help)',
    'btop': 'resource monitor (btop --help)',
    'iotop': 'I/O monitor (iotop --help)',
    'iostat': 'I/O statistics (man iostat)',
    'vmstat': 'virtual memory stats (man vmstat)',
    'df': 'disk free (man df)',
    'du': 'disk usage (man du)',
    'gdu': 'disk usage analyzer (gdu --help)',
    'ncdu': 'NCurses disk usage (ncdu --help)',
    'lsblk': 'list block devices (man lsblk)',
    'pv': 'pipe viewer (pv --help)',
    'chmod': 'change mode (man chmod)',
    'chown': 'change owner (man chown)',
    'kill': 'send signal (man kill)',
    'tmux': 'terminal mux (man tmux)',
    'make': 'build tool (man make)',
    'gcc': 'C compiler (gcc --help)',
    'clang': 'C compiler (clang --help)',
    'node': 'JS runtime (node --help)',
    'go': 'go toolchain (go help)',
    'rustc': 'rust compiler (rustc --help)',
    'pip': 'python packages (pip --help)',
    'brew': 'macOS packages (brew --help)',
    'apt': 'debian packages (man apt)',
    'yum': 'rpm packages (man yum)',
    'systemctl': 'system control (man systemctl)',
    'journalctl': 'view logs (man journalctl)',
    'sed': 'stream editor (man sed)',
    'awk': 'text processing (man awk)',
    'jq': 'JSON processor (jq --help)',
    'sqlite3': 'SQL database (sqlite3 --help)',
    'rg': 'ripgrep search (rg --help)',
    'fzf': 'fuzzy finder (fzf --help)',
    'delta': 'git diff pager (delta --help)',
    'bat': 'cat with highlighting (bat --help)',
    'exa': 'modern ls (exa --help)',
    'ag': 'silver searcher (ag --help)',
    'ffmpeg': 'media tool (ffmpeg --help)',
    'convert': 'image tool (man convert)',
    'netstat': 'network statistics (man netstat)',
    'ifconfig': 'configure network interface (man ifconfig)',
    'lsof': 'list open files (man lsof)',
    'nmap': 'network mapper (man nmap)',
    'traceroute': 'trace route to host (man traceroute)',
    'dig': 'DNS lookup (man dig)',
    'host': 'DNS lookup (man host)',
    'nslookup': 'DNS query (man nslookup)',
    'nc': 'netcat networking (man nc)',
    'uv': 'python packages (uv --help)',
    'asciinema': 'terminal recorder (asciinema --help)',
    'speedtest': 'network speed test (speedtest --help)',
    'ranger': 'file manager (ranger --help)',
    'telnet': 'remote connection (man telnet)',
    'ab': 'Apache benchmark (ab --help)',
    'yes': 'output string repeatedly (man yes)',
    'lolcat': 'rainbow coloring (lolcat --help)',
}


# Global registry of completion schemas
_COMPLETION_SCHEMAS = {}

# Cache for expensive completion operations
_COMPLETION_CACHE = {}
_CACHE_LOCKS = {}
_CACHE_LOCK = Lock()


class CachedResult(object):
    """Wrapper for cached completion results with expiry."""
    def __init__(self, result, ttl=300):
        self.result = result
        self.timestamp = time.time()
        self.ttl = ttl

    def is_expired(self):
        return time.time() - self.timestamp > self.ttl


def cached_completion(cache_key, ttl=300):
    """
    Decorator for caching completion results.

    Args:
        cache_key: Unique key for this completion type
        ttl: Time to live in seconds (default 5 minutes)

    Example:
        >>> @cached_completion('conda_envs', ttl=600)
        >>> def get_conda_environments():
        ...     # Expensive operation
        ...     return subprocess.check_output(['conda', 'env', 'list'])
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Get or create lock for this cache key
            with _CACHE_LOCK:
                if cache_key not in _CACHE_LOCKS:
                    _CACHE_LOCKS[cache_key] = Lock()
                lock = _CACHE_LOCKS[cache_key]

            with lock:
                # Check cache
                if cache_key in _COMPLETION_CACHE:
                    cached = _COMPLETION_CACHE[cache_key]
                    if not cached.is_expired():
                        return cached.result

                # Compute and cache
                result = func(*args, **kwargs)
                _COMPLETION_CACHE[cache_key] = CachedResult(result, ttl)
                return result
        return wrapper
    return decorator


def clear_cache(cache_key=None):
    """Clear completion cache. If cache_key is None, clears all caches."""
    with _CACHE_LOCK:
        if cache_key is None:
            _COMPLETION_CACHE.clear()
        elif cache_key in _COMPLETION_CACHE:
            del _COMPLETION_CACHE[cache_key]


class Token(object):
    """Represents a bash token from the lexer."""
    def __init__(self, text, token_type, position):
        self.text = text
        self.token_type = token_type
        self.position = position

    def __repr__(self):
        return 'Token({}, {}, {})'.format(repr(self.text), self.token_type, self.position)


def tokenize_bash_command(text):
    """
    Tokenize bash command text into meaningful tokens using simple splitting.

    Returns list of Token objects representing the command structure.
    This uses simple whitespace splitting to avoid interfering with syntax highlighting.
    """
    # Simple tokenization by whitespace - good enough for completion purposes
    # Avoids using BashLexer which can interfere with syntax highlighting
    tokens = []
    pos = 0

    # Split by whitespace while tracking positions
    for token_text in text.split():
        # Find actual position in original text
        pos = text.find(token_text, pos)
        tokens.append(Token(token_text, None, pos))
        pos += len(token_text)

    return tokens


def find_cursor_token(tokens, cursor_pos):
    """
    Find which token the cursor is in or after.

    Returns (token_index, is_after) where:
        - token_index: index of the token cursor is in/after
        - is_after: True if cursor is after the token (for completion)
    """
    if not tokens:
        return 0, False

    for idx, token in enumerate(tokens):
        token_start = token.position
        # Account for original whitespace by looking at the stripped text
        # The position is the start of the stripped text
        token_end = token_start + len(token.text)

        # Cursor is within this token
        if token_start <= cursor_pos < token_end:
            return idx, False

        # Cursor is after this token (including whitespace after)
        if cursor_pos >= token_end:
            # Check if there's a next token
            if idx + 1 < len(tokens):
                next_token_start = tokens[idx + 1].position
                # Cursor is in the whitespace between this token and the next
                if cursor_pos < next_token_start:
                    return idx, True
            else:
                # No more tokens, cursor is after this one
                return idx, True

    # Fallback: cursor is after last token
    return len(tokens) - 1, True


def register_completion_schema(command_name):
    """
    Decorator to register a completion schema for a command.

    The decorated function should accept (tokens, cursor_token_idx) and return
    a list of completion candidates or None.

    Example:
        >>> @register_completion_schema('git')
        >>> def git_completions(tokens, cursor_token_idx):
        ...     if cursor_token_idx == 1:  # After 'git'
        ...         return ['add', 'commit', 'push', 'pull', 'status']
        ...     return None
    """
    def decorator(func):
        _COMPLETION_SCHEMAS[command_name] = func
        return func
    return decorator


def get_completions_for_command(text, cursor_pos):
    """
    Get completions for a bash command at the given cursor position.

    Args:
        text: The bash command text (without the leading !)
        cursor_pos: Cursor position in the text

    Returns:
        List of completion candidates or None
    """
    # Tokenize the command
    tokens = tokenize_bash_command(text)
    if not tokens:
        return None

    # Find cursor position in token stream
    cursor_token_idx, is_after = find_cursor_token(tokens, cursor_pos)

    # Get the command name (first token)
    command_name = tokens[0].text

    # Look up completion schema
    if command_name in _COMPLETION_SCHEMAS:
        schema_func = _COMPLETION_SCHEMAS[command_name]
        try:
            return schema_func(tokens, cursor_token_idx, is_after)
        except Exception:
            # Silently fail - don't break completions
            return None

    # FALLBACK 1: Auto-parse subcommands if at position 0 (right after command name)
    # This helps commands like 'claude' get automatic subcommand completion
    if cursor_token_idx == 0 and is_after:
        try:
            subcommands = _parse_subcommands_from_help(command_name)
            if subcommands:
                return subcommands
        except Exception:
            # Silently fail - continue to flag parsing
            pass

    # FALLBACK 1.5: Auto-parse NESTED subcommands if at position 1+ (after first subcommand)
    # Examples: 'docker network ', 'gh pr ', 'kubectl get '
    # Try calling help on the subcommand: 'docker network --help', 'gh pr --help'
    if cursor_token_idx >= 1 and is_after and not _is_flag_context(tokens, cursor_token_idx, is_after):
        try:
            # Build the compound command (e.g., 'docker network', 'gh pr')
            compound_cmd = ' '.join([t.text for t in tokens[:cursor_token_idx + 1]])
            nested_subcommands = _parse_subcommands_from_help(compound_cmd)
            if nested_subcommands:
                return nested_subcommands
        except Exception:
            # Silently fail - continue to flag parsing
            pass

    # FALLBACK 2: Try to parse flags for specific subcommand context
    # Examples: 'docker run --', 'cargo build --', 'gh label --'
    # Call help on the subcommand to get its specific flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        try:
            # If we have a subcommand, try parsing its specific help
            # Build compound command from all non-flag tokens before current position
            # E.g., 'gh label --' -> 'gh label', 'docker run --detach --' -> 'docker run'
            non_flag_tokens = [t.text for t in tokens[:cursor_token_idx+1] if not t.text.startswith('-')]
            if len(non_flag_tokens) >= 2:
                compound_cmd = ' '.join(non_flag_tokens)
                subcommand_flags = _parse_manpage_flags(compound_cmd)
                if subcommand_flags:
                    return subcommand_flags

            # Fallback to main command flags
            manpage_flags = _parse_manpage_flags(command_name)
            if manpage_flags:
                return manpage_flags
        except Exception:
            # Silently fail - don't break completions
            pass

    return None


def get_bash_origin(document_text, cursor_position):
    """
    Extract the word before cursor for bash completions, handling flags properly.

    For flags like '--verbose' or '-a', returns the full flag including dashes.
    For other words, returns the word before cursor.

    Args:
        document_text: Full text of the document
        cursor_position: Current cursor position

    Returns:
        The origin string for completion matching

    Example:
        >>> get_bash_origin('!git commit -', 14)
        '-'
        >>> get_bash_origin('!git commit --mes', 17)
        '--mes'
    """
    # Look backwards from cursor to find start of current token
    pos = cursor_position - 1
    while pos >= 0 and document_text[pos] in '-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        pos -= 1

    # Extract the token from start to cursor
    token = document_text[pos + 1:cursor_position]
    return token




# ============================================================================
# Built-in completion schemas
# ============================================================================

@cached_completion('conda_envs', ttl=600)
def _get_conda_environments():
    """Get list of conda environments (cached for 10 minutes)."""
    try:
        output = subprocess.check_output(
            ['conda', 'env', 'list'],
            stderr=subprocess.PIPE,
            timeout=5
        )
        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='ignore')

        envs = []
        for line in output.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract environment name (first word)
                parts = line.split()
                if parts:
                    envs.append(parts[0])
        return envs
    except Exception:
        return []


@cached_completion('git_remotes', ttl=60)
def _get_git_remotes():
    """Get list of git remotes (cached for 1 minute)."""
    try:
        output = subprocess.check_output(
            ['git', 'remote'],
            stderr=subprocess.PIPE,
            timeout=2
        )
        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='ignore')
        return [r.strip() for r in output.split('\n') if r.strip()]
    except Exception:
        return []


@cached_completion('git_branches', ttl=60)
def _get_git_branches():
    """Get list of git branches (cached for 1 minute)."""
    try:
        output = subprocess.check_output(
            ['git', 'branch', '-a'],
            stderr=subprocess.PIPE,
            timeout=2
        )
        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='ignore')

        branches = []
        for line in output.split('\n'):
            line = line.strip()
            if line:
                # Remove * from current branch
                if line.startswith('* '):
                    line = line[2:]
                # Remove remotes/ prefix for remote branches
                if line.startswith('remotes/'):
                    line = line[8:]
                branches.append(line)
        return branches
    except Exception:
        return []


@register_completion_schema('conda')
def _conda_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for conda commands with comprehensive flag support."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''
        common_flags = {
            '--help': 'show help message',
            '--version': '--version/-V: show version',
            '-V': '-V/--version: show version',
        }

        flag_mapping = {
            'install': {
                '--yes': '--yes/-y: automatically answer yes to prompts',
                '-y': '-y/--yes: automatically answer yes to prompts',
                '--channel': '--channel/-c: specify channel to search for packages',
                '-c': '-c/--channel: specify channel to search for packages',
                '--file': '--file/-f: read package list from file',
                '-f': '-f/--file: read package list from file',
                '--name': '--name/-n: name of environment to install into',
                '-n': '-n/--name: name of environment to install into',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--no-deps': 'do not install dependencies',
                '--only-deps': 'only install dependencies',
                '--force-reinstall': 'reinstall package even if up-to-date',
                '--update-deps': 'update dependencies',
                '--no-update-deps': 'do not update dependencies',
                '--revision': 'revert to specified revision number',
                '--use-local': 'use locally built packages',
                '--override-channels': 'do not search default channels',
                '--repodata-fn': 'specify repodata file name',
                '--strict-channel-priority': 'packages in lower priority channels not considered',
                '--no-channel-priority': 'ignore channel priority',
                '--no-pin': 'ignore pinned packages',
                '--copy': 'copy packages instead of hard-linking',
                '--no-shortcuts': 'do not create shortcuts (Windows)',
                '--shortcuts': 'create shortcuts (Windows)',
                '--clobber': 'allow clobbering of overlapping files',
                '--no-clobber': 'prevent clobbering of overlapping files',
                '--dry-run': '--dry-run/-d: perform dry run (no actual changes)',
                '-d': '-d/--dry-run: perform dry run (no actual changes)',
                '--json': 'output in JSON format',
                '--offline': 'work offline (do not connect to internet)',
                '--download-only': 'download packages without installing',
                '--show-channel-urls': 'show channel URLs',
                '--update-all': 'update all packages in environment',
                '--update-specs': 'update specs in environment',
                '--freeze-installed': 'do not update installed packages',
                '--update-all-deps': 'update all dependencies',
                '--satisfied-skip-solve': 'skip solving if dependencies satisfied',
                '--insecure': 'allow insecure SSL connections'
            },
            'create': {
                '--yes': '--yes/-y: automatically answer yes to prompts',
                '-y': '-y/--yes: automatically answer yes to prompts',
                '--name': '--name/-n: name for new environment',
                '-n': '-n/--name: name for new environment',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--file': '--file/-f: read package list from file',
                '-f': '-f/--file: read package list from file',
                '--channel': '--channel/-c: specify channel to search for packages',
                '-c': '-c/--channel: specify channel to search for packages',
                '--clone': 'clone existing environment',
                '--use-local': 'use locally built packages',
                '--override-channels': 'do not search default channels',
                '--repodata-fn': 'specify repodata file name',
                '--strict-channel-priority': 'packages in lower priority channels not considered',
                '--no-channel-priority': 'ignore channel priority',
                '--no-deps': 'do not install dependencies',
                '--only-deps': 'only install dependencies',
                '--no-pin': 'ignore pinned packages',
                '--copy': 'copy packages instead of hard-linking',
                '--no-shortcuts': 'do not create shortcuts (Windows)',
                '--shortcuts': 'create shortcuts (Windows)',
                '--clobber': 'allow clobbering of overlapping files',
                '--no-clobber': 'prevent clobbering of overlapping files',
                '--dry-run': '--dry-run/-d: perform dry run (no actual changes)',
                '-d': '-d/--dry-run: perform dry run (no actual changes)',
                '--json': 'output in JSON format',
                '--offline': 'work offline (do not connect to internet)',
                '--download-only': 'download packages without installing',
                '--show-channel-urls': 'show channel URLs',
                '--insecure': 'allow insecure SSL connections'
            },
            'remove': {
                '--yes': '--yes/-y: automatically answer yes to prompts',
                '-y': '-y/--yes: automatically answer yes to prompts',
                '--name': '--name/-n: name of environment to remove from',
                '-n': '-n/--name: name of environment to remove from',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--all': 'remove all packages (entire environment)',
                '--features': 'remove features',
                '--force-remove': 'force removal of package',
                '--no-pin': 'ignore pinned packages',
                '--dry-run': '--dry-run/-d: perform dry run (no actual changes)',
                '-d': '-d/--dry-run: perform dry run (no actual changes)',
                '--json': 'output in JSON format',
                '--offline': 'work offline (do not connect to internet)'
            },
            'update': {
                '--yes': '--yes/-y: automatically answer yes to prompts',
                '-y': '-y/--yes: automatically answer yes to prompts',
                '--all': 'update all packages in environment',
                '--name': '--name/-n: name of environment to update',
                '-n': '-n/--name: name of environment to update',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--channel': '--channel/-c: specify channel to search for packages',
                '-c': '-c/--channel: specify channel to search for packages',
                '--file': '--file/-f: read package list from file',
                '-f': '-f/--file: read package list from file',
                '--no-deps': 'do not install dependencies',
                '--force-reinstall': 'reinstall package even if up-to-date',
                '--update-deps': 'update dependencies',
                '--no-update-deps': 'do not update dependencies',
                '--use-local': 'use locally built packages',
                '--override-channels': 'do not search default channels',
                '--repodata-fn': 'specify repodata file name',
                '--strict-channel-priority': 'packages in lower priority channels not considered',
                '--no-channel-priority': 'ignore channel priority',
                '--no-pin': 'ignore pinned packages',
                '--copy': 'copy packages instead of hard-linking',
                '--clobber': 'allow clobbering of overlapping files',
                '--no-clobber': 'prevent clobbering of overlapping files',
                '--dry-run': '--dry-run/-d: perform dry run (no actual changes)',
                '-d': '-d/--dry-run: perform dry run (no actual changes)',
                '--json': 'output in JSON format',
                '--offline': 'work offline (do not connect to internet)',
                '--download-only': 'download packages without installing',
                '--show-channel-urls': 'show channel URLs',
                '--update-all': 'update all packages in environment',
                '--insecure': 'allow insecure SSL connections'
            },
            'search': {
                '--channel': '--channel/-c: specify channel to search',
                '-c': '-c/--channel: specify channel to search',
                '--use-local': 'use locally built packages',
                '--override-channels': 'do not search default channels',
                '--repodata-fn': 'specify repodata file name',
                '--platform': 'search for specific platform',
                '--info': 'show detailed package information',
                '--json': 'output in JSON format'
            },
            'list': {
                '--name': '--name/-n: name of environment to list',
                '-n': '-n/--name: name of environment to list',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--show-channel-urls': 'show channel URLs',
                '--canonical': 'output canonical names of packages',
                '--full-name': 'only search for full names',
                '--explicit': 'show explicit URLs for packages',
                '--md5': 'show MD5 checksums',
                '--json': 'output in JSON format',
                '--verbose': '--verbose/-v: use verbose output',
                '-v': '-v/--verbose: use verbose output',
                '--revisions': 'list revision history',
                '--no-pip': 'do not include pip packages'
            },
            'config': {
                '--system': 'write to system .condarc file',
                '--env': 'write to active environment .condarc file',
                '--file': 'write to specified file',
                '--show': 'display configuration values',
                '--show-sources': 'display configuration sources',
                '--validate': 'validate configuration',
                '--describe': 'describe configuration parameters',
                '--write-default': 'write default configuration',
                '--get': 'get a configuration value',
                '--append': 'append to configuration list',
                '--prepend': 'prepend to configuration list',
                '--set': 'set a configuration value',
                '--remove': 'remove a configuration value',
                '--remove-key': 'remove a configuration key',
                '--stdin': 'read configuration from stdin'
            },
            'clean': {
                '--all': '--all/-a: remove all unused packages and caches',
                '-a': '-a/--all: remove all unused packages and caches',
                '--index-cache': '--index-cache/-i: remove index cache',
                '-i': '-i/--index-cache: remove index cache',
                '--packages': '--packages/-p: remove unused packages',
                '-p': '-p/--packages: remove unused packages',
                '--tarballs': '--tarballs/-t: remove cached tarballs',
                '-t': '-t/--tarballs: remove cached tarballs',
                '--force-pkgs-dirs': 'remove all writable package caches'
            },
            'info': {
                '--envs': '--envs/-e: list all known conda environments',
                '-e': '-e/--envs: list all known conda environments',
                '--system': '--system/-s: display system information',
                '-s': '-s/--system: display system information',
                '--base': 'display base environment path',
                '--unsafe-channels': 'display channels with unsafe certificates',
                '--all': '--all/-a: display all information',
                '-a': '-a/--all: display all information',
                '--json': 'output in JSON format'
            },
        }

        return _get_subcommand_flags(subcommand, flag_mapping, common_flags)

    result = _complete_at_position_zero(cursor_token_idx, is_after,
                                        {
                                            'activate': 'activate a conda environment',
                                            'deactivate': 'deactivate the current conda environment',
                                            'env': 'manage conda environments',
                                            'install': 'install packages into an environment',
                                            'list': 'list installed packages in an environment',
                                            'remove': 'remove packages from an environment',
                                            'create': 'create a new conda environment',
                                            'update': 'update packages in an environment',
                                            'search': 'search for packages in repositories',
                                            'config': 'modify conda configuration',
                                            'clean': 'remove unused packages and caches',
                                            'compare': 'compare packages between environments',
                                            'doctor': 'diagnose and fix common conda issues',
                                            'info': 'display information about conda installation',
                                            'init': 'initialize conda for shell interaction',
                                            'notices': 'show conda notices and announcements',
                                            'package': 'create and manage conda packages',
                                            'rename': 'rename an existing environment',
                                            'run': 'run a command in a conda environment'
                                        })
    if result:
        return result

    if cursor_token_idx >= 1:
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        if subcommand == 'activate':
            result = _complete_subcommand_at_position(cursor_token_idx, is_after, 1, _get_conda_environments())
            if result:
                return result
            if cursor_token_idx == 2:
                return _get_conda_environments()

        elif subcommand == 'env':
            if cursor_token_idx == 1:
                return {
                    'list': 'list conda environments',
                    'create': 'create a new environment',
                    'remove': 'remove an environment',
                    'export': 'export environment to a file',
                    'update': 'update an environment',
                    'config': 'configure environment settings'
                }

    return None


@cached_completion('mamba_envs', ttl=600)
def _get_mamba_environments():
    """Get list of mamba environments (cached for 10 minutes)."""
    try:
        output = subprocess.check_output(
            ['mamba', 'env', 'list'],
            stderr=subprocess.PIPE,
            timeout=5
        )
        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='ignore')

        envs = []
        for line in output.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract environment name (first word)
                parts = line.split()
                if parts:
                    envs.append(parts[0])
        return envs
    except Exception:
        return []


@register_completion_schema('mamba')
def _mamba_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for mamba/micromamba commands with comprehensive flag support."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''
        common_flags = {
            '--help': '--help/-h: show help message',
            '-h': '-h/--help: show help message',
            '--version': 'show version information',
            '--verbose': '--verbose/-v: enable verbose output',
            '-v': '-v/--verbose: enable verbose output',
            '--quiet': '--quiet/-q: quiet mode (minimal output)',
            '-q': '-q/--quiet: quiet mode (minimal output)',
            '--yes': '--yes/-y: automatically answer yes to prompts',
            '-y': '-y/--yes: automatically answer yes to prompts',
            '--json': 'output in JSON format',
            '--offline': 'work offline (do not connect to internet)',
            '--dry-run': 'perform dry run (no actual changes)',
            '--download-only': 'download packages without installing',
        }

        flag_mapping = {
            'install': {
                '--channel': '--channel/-c: specify channel to search for packages',
                '-c': '-c/--channel: specify channel to search for packages',
                '--file': '--file/-f: read package list from file',
                '-f': '-f/--file: read package list from file',
                '--name': '--name/-n: name of environment to install into',
                '-n': '-n/--name: name of environment to install into',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--override-channels': 'do not search default channels',
                '--channel-priority': 'enable channel priority',
                '--strict-channel-priority': 'packages in lower priority channels not considered',
                '--no-channel-priority': 'ignore channel priority',
                '--no-pin': 'ignore pinned packages',
                '--no-py-pin': 'ignore python version pinning',
                '--pyc': 'compile python files to pyc',
                '--no-pyc': 'do not compile python files to pyc',
                '--allow-uninstall': 'allow uninstalling packages',
                '--no-allow-uninstall': 'do not allow uninstalling packages',
                '--allow-downgrade': 'allow downgrading packages',
                '--no-allow-downgrade': 'do not allow downgrading packages',
                '--allow-softlinks': 'allow using softlinks',
                '--no-allow-softlinks': 'do not allow using softlinks',
                '--always-softlink': 'always use softlinks instead of hardlinks',
                '--always-copy': 'always copy packages instead of linking',
                '--copy': 'copy packages instead of hard-linking',
                '--lock-timeout': 'timeout for file locks',
                '--shortcuts': 'create shortcuts (Windows)',
                '--no-shortcuts': 'do not create shortcuts (Windows)',
                '--safety-checks': 'enable safety checks',
                '--extra-safety-checks': 'enable extra safety checks',
                '--no-extra-safety-checks': 'disable extra safety checks',
                '--verify-artifacts': 'verify package artifacts',
                '--trusted-channels': 'specify trusted channels',
                '--exp-repodata-parsing': 'use experimental repodata parsing',
                '--no-exp-repodata-parsing': 'do not use experimental repodata parsing',
                '--platform': 'specify platform for packages',
                '--no-deps': 'do not install dependencies',
                '--only-deps': 'only install dependencies',
                '--category': 'specify package category',
                '--freeze-installed': 'do not update installed packages',
                '--force-reinstall': 'reinstall package even if up-to-date',
                '--root-prefix': '--root-prefix/-r: specify root prefix',
                '-r': '-r/--root-prefix: specify root prefix',
                '--relocate-prefix': 'relocate package prefix path',
            },
            'create': {
                '--channel': '--channel/-c: specify channel to search for packages',
                '-c': '-c/--channel: specify channel to search for packages',
                '--file': '--file/-f: read package list from file',
                '-f': '-f/--file: read package list from file',
                '--name': '--name/-n: name for new environment',
                '-n': '-n/--name: name for new environment',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--override-channels': 'do not search default channels',
                '--channel-priority': 'enable channel priority',
                '--strict-channel-priority': 'packages in lower priority channels not considered',
                '--no-channel-priority': 'ignore channel priority',
                '--no-pin': 'ignore pinned packages',
                '--no-py-pin': 'ignore python version pinning',
                '--pyc': 'compile python files to pyc',
                '--no-pyc': 'do not compile python files to pyc',
                '--allow-uninstall': 'allow uninstalling packages',
                '--no-allow-uninstall': 'do not allow uninstalling packages',
                '--allow-downgrade': 'allow downgrading packages',
                '--no-allow-downgrade': 'do not allow downgrading packages',
                '--allow-softlinks': 'allow using softlinks',
                '--no-allow-softlinks': 'do not allow using softlinks',
                '--always-softlink': 'always use softlinks instead of hardlinks',
                '--always-copy': 'always copy packages instead of linking',
                '--copy': 'copy packages instead of hard-linking',
                '--lock-timeout': 'timeout for file locks',
                '--shortcuts': 'create shortcuts (Windows)',
                '--no-shortcuts': 'do not create shortcuts (Windows)',
                '--safety-checks': 'enable safety checks',
                '--extra-safety-checks': 'enable extra safety checks',
                '--no-extra-safety-checks': 'disable extra safety checks',
                '--verify-artifacts': 'verify package artifacts',
                '--trusted-channels': 'specify trusted channels',
                '--exp-repodata-parsing': 'use experimental repodata parsing',
                '--no-exp-repodata-parsing': 'do not use experimental repodata parsing',
                '--platform': 'specify platform for packages',
                '--no-deps': 'do not install dependencies',
                '--only-deps': 'only install dependencies',
                '--category': 'specify package category',
                '--root-prefix': '--root-prefix/-r: specify root prefix',
                '-r': '-r/--root-prefix: specify root prefix',
                '--relocate-prefix': 'relocate package prefix path',
            },
            'remove': {
                '--name': '--name/-n: name of environment to remove from',
                '-n': '-n/--name: name of environment to remove from',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--all': 'remove all packages (entire environment)',
                '--force': 'force removal of package',
                '--root-prefix': '--root-prefix/-r: specify root prefix',
                '-r': '-r/--root-prefix: specify root prefix',
            },
            'uninstall': {
                '--name': '--name/-n: name of environment to uninstall from',
                '-n': '-n/--name: name of environment to uninstall from',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--all': 'uninstall all packages (entire environment)',
                '--force': 'force uninstallation of package',
                '--root-prefix': '--root-prefix/-r: specify root prefix',
                '-r': '-r/--root-prefix: specify root prefix',
            },
            'update': {
                '--name': '--name/-n: name of environment to update',
                '-n': '-n/--name: name of environment to update',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--all': 'update all packages in environment',
                '--channel': '--channel/-c: specify channel to search for packages',
                '-c': '-c/--channel: specify channel to search for packages',
                '--file': '--file/-f: read package list from file',
                '-f': '-f/--file: read package list from file',
                '--freeze-installed': 'do not update installed packages',
                '--force-reinstall': 'reinstall package even if up-to-date',
                '--root-prefix': '--root-prefix/-r: specify root prefix',
                '-r': '-r/--root-prefix: specify root prefix',
            },
            'search': {
                '--channel': '--channel/-c: specify channel to search',
                '-c': '-c/--channel: specify channel to search',
                '--override-channels': 'do not search default channels',
                '--platform': 'search for specific platform',
            },
            'list': {
                '--name': '--name/-n: name of environment to list',
                '-n': '-n/--name: name of environment to list',
                '--prefix': '--prefix/-p: full path to environment prefix',
                '-p': '-p/--prefix: full path to environment prefix',
                '--full-name': 'only search for full names',
                '--explicit': 'show explicit URLs for packages',
                '--root-prefix': '--root-prefix/-r: specify root prefix',
                '-r': '-r/--root-prefix: specify root prefix',
            },
            'config': {
                '--system': 'write to system .mambarc file',
                '--env': 'write to active environment .mambarc file',
                '--file': 'write to specified file',
                '--show': 'display configuration values',
                '--get': 'get a configuration value',
                '--append': 'append to configuration list',
                '--prepend': 'prepend to configuration list',
                '--set': 'set a configuration value',
                '--remove': 'remove a configuration value',
                '--remove-key': 'remove a configuration key',
            },
            'clean': {
                '--all': '--all/-a: remove all unused packages and caches',
                '-a': '-a/--all: remove all unused packages and caches',
                '--index-cache': '--index-cache/-i: remove index cache',
                '-i': '-i/--index-cache: remove index cache',
                '--packages': '--packages/-p: remove unused packages',
                '-p': '-p/--packages: remove unused packages',
                '--tarballs': '--tarballs/-t: remove cached tarballs',
                '-t': '-t/--tarballs: remove cached tarballs',
            },
            'info': {
                '--envs': '--envs/-e: list all known mamba environments',
                '-e': '-e/--envs: list all known mamba environments',
                '--system': '--system/-s: display system information',
                '-s': '-s/--system: display system information',
                '--all': '--all/-a: display all information',
                '-a': '-a/--all: display all information',
            },
        }

        return _get_subcommand_flags(subcommand, flag_mapping, common_flags)

    result = _complete_at_position_zero(cursor_token_idx, is_after,
                                        {
                                            'shell': 'shell-specific mamba configuration',
                                            'create': 'create a new mamba environment',
                                            'install': 'install packages into an environment',
                                            'update': 'update packages in an environment',
                                            'repoquery': 'query package repositories',
                                            'remove': 'remove packages from an environment',
                                            'uninstall': 'uninstall packages (alias for remove)',
                                            'list': 'list installed packages',
                                            'package': 'create and manage packages',
                                            'clean': 'remove unused packages and caches',
                                            'config': 'modify mamba configuration',
                                            'info': 'display mamba installation information',
                                            'constructor': 'create custom installers',
                                            'env': 'manage mamba environments',
                                            'activate': 'activate a mamba environment',
                                            'run': 'run a command in an environment',
                                            'ps': 'show running mamba processes',
                                            'auth': 'manage authentication for channels',
                                            'search': 'search for packages in repositories'
                                        })
    if result:
        return result

    if cursor_token_idx >= 1:
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        if subcommand == 'activate':
            result = _complete_subcommand_at_position(cursor_token_idx, is_after, 1, _get_mamba_environments())
            if result:
                return result
            if cursor_token_idx == 2:
                return _get_mamba_environments()

        elif subcommand == 'env':
            if cursor_token_idx == 1:
                return {
                    'list': 'list mamba environments',
                    'create': 'create a new environment',
                    'remove': 'remove an environment',
                    'export': 'export environment to a file',
                    'update': 'update an environment'
                }

    return None


@register_completion_schema('git')
def _git_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for git commands."""
    # Check for flags first
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        # Common flags for all git commands
        common_flags = {
            '--help': 'show help message',
            '--verbose': 'verbose output',
        }

        if subcommand == 'commit':
            commit_flags = {
                '-a': '-a/--all: automatically stage modified and deleted files',
                '--all': '--all/-a: automatically stage modified and deleted files',
                '-p': '-p/--patch: interactively select changes to commit',
                '--patch': '--patch/-p: interactively select changes to commit',
                '-C': '-C/--reuse-message: reuse commit message from specified commit',
                '--reuse-message': '--reuse-message/-C: reuse commit message from specified commit',
                '-c': '-c/--reedit-message: reuse and edit commit message from commit',
                '--reedit-message': '--reedit-message/-c: reuse and edit commit message from commit',
                '-m': '-m/--message: commit message (can use multiple times)',
                '--message': '--message/-m: commit message (can use multiple times)',
                '-F': '-F/--file: read commit message from file',
                '--file': '--file/-F: read commit message from file',
                '-s': '-s/--signoff: add Signed-off-by line to commit message',
                '--signoff': '--signoff/-s: add Signed-off-by line to commit message',
                '-e': '-e/--edit: edit commit message in editor',
                '--edit': '--edit/-e: edit commit message in editor',
                '--no-edit': 'use selected commit message without launching editor',
                '--amend': 'amend the previous commit',
                '-i': '-i/--include: only stage files listed on command line',
                '--include': '--include/-i: only stage files listed on command line',
                '-o': '-o/--only: bypass staged content and commit only specified files',
                '--only': '--only/-o: bypass staged content and commit only specified files',
                '-v': '-v/--verbose: show diff of changes being committed',
                '--verbose': '--verbose/-v: show diff of changes being committed',
                '-q': '-q/--quiet: suppress commit summary message',
                '--quiet': '--quiet/-q: suppress commit summary message',
                '-n': '-n/--no-verify: bypass pre-commit and commit-msg hooks',
                '--no-verify': '--no-verify/-n: bypass pre-commit and commit-msg hooks',
                '--dry-run': 'show what would be committed without committing',
                '-S': '-S/--gpg-sign: GPG-sign the commit',
                '--gpg-sign': '--gpg-sign/-S: GPG-sign the commit',
                '--no-gpg-sign': "don't GPG-sign the commit",
                '-u': '-u/--untracked-files: show untracked files in commit status',
                '--untracked-files': '--untracked-files/-u: show untracked files in commit status',
                '-z': '-z/--null: terminate entries with NUL instead of newline',
                '--null': '--null/-z: terminate entries with NUL instead of newline',
                '-t': '-t/--template: use file as commit message template',
                '--template': '--template/-t: use file as commit message template',
                '--fixup': 'create fixup commit for later squashing',
                '--squash': 'create squash commit for later squashing',
                '--reset-author': 'reset author to committer when amending',
                '--short': 'output in short format',
                '--branch': 'show branch information in status',
                '--porcelain': 'machine-readable output format',
                '--long': 'output in long format (default)',
                '--author': 'override author for commit',
                '--date': 'override date for commit',
                '--verify': 'run pre-commit and commit-msg hooks',
                '--allow-empty': 'allow empty commit',
                '--allow-empty-message': 'allow commit with empty message',
                '--cleanup': 'how to clean up commit message',
                '--no-post-rewrite': 'bypass post-rewrite hook',
                '--post-rewrite': 'run post-rewrite hook',
                '--status': 'include git status in commit message template',
                '--no-status': "don't include git status in template",
                '--trailer': 'add trailer to commit message',
                '--pathspec-from-file': 'read pathspecs from file',
                '--pathspec-file-nul': 'pathspec file is NUL-separated',
                '--ahead-behind': 'compute ahead/behind counts',
                '--interactive': 'interactively edit commit',
            }
            return {**{k: '' for k in common_flags}, **commit_flags}
        elif subcommand == 'push':
            push_flags = {
                '-u': '-u/--set-upstream: set upstream for tracking',
                '--set-upstream': '--set-upstream/-u: set upstream for tracking',
                '--all': '--all: push all branches',
                '--branches': '--branches: alias for --all',
                '--prune': '--prune: remove remote branches that do not have local counterpart',
                '--mirror': '--mirror: mirror all refs (dangerous)',
                '--dry-run': '--dry-run/-n: perform dry run without actually pushing',
                '-n': '-n/--dry-run: perform dry run without actually pushing',
                '--porcelain': '--porcelain: machine-readable output',
                '--delete': '--delete/-d: delete refs from remote',
                '-d': '-d/--delete: delete refs from remote',
                '--tags': '--tags: push all tags',
                '--follow-tags': '--follow-tags: push tags reachable from pushed commits',
                '--signed': '--signed: GPG sign the push',
                '--atomic': '--atomic: request atomic transaction on remote',
                '--no-atomic': '--no-atomic: do not request atomic transaction',
                '--receive-pack': '--receive-pack/--exec: path to git-receive-pack on remote',
                '--exec': '--exec/--receive-pack: path to git-receive-pack on remote',
                '--force-with-lease': '--force-with-lease: force push with safety check',
                '--force-if-includes': '--force-if-includes: force only if tip is reachable',
                '--force': '--force/-f: force push (dangerous)',
                '-f': '-f/--force: force push (dangerous)',
                '--repo': '--repo: repository to push to',
                '--thin': '--thin: use thin pack',
                '--no-thin': '--no-thin: do not use thin pack',
                '--quiet': '--quiet/-q: suppress all output',
                '-q': '-q/--quiet: suppress all output',
                '--verbose': '--verbose/-v: be more verbose',
                '-v': '-v/--verbose: be more verbose',
                '--progress': '--progress: force progress reporting',
                '--no-recurse-submodules': '--no-recurse-submodules: do not recurse into submodules',
                '--recurse-submodules': '--recurse-submodules: recurse into submodules',
                '--verify': '--verify: verify remote-tracking branches',
                '--no-verify': '--no-verify: bypass pre-push hook',
                '--push-option': '--push-option/-o: transmit string to server',
                '-o': '-o/--push-option: transmit string to server',
                '--ipv4': '--ipv4/-4: use IPv4 addresses only',
                '-4': '-4/--ipv4: use IPv4 addresses only',
                '--ipv6': '--ipv6/-6: use IPv6 addresses only',
                '-6': '-6/--ipv6: use IPv6 addresses only',
            }
            return {**{k: k for k in common_flags}, **push_flags}
        elif subcommand == 'pull':
            pull_flags = {
                '--all': '--all: fetch from all remotes',
                '--allow-unrelated-histories': '--allow-unrelated-histories: allow merging unrelated histories',
                '--append': '--append/-a: append to .git/FETCH_HEAD',
                '--autostash': '--autostash: automatically stash/unstash working directory',
                '--cleanup': '--cleanup: how to strip whitespace from message',
                '--commit': '--commit: perform merge and commit result',
                '--deepen': '--deepen: deepen history of shallow repository',
                '--depth': '--depth: create shallow clone with history truncated',
                '--dry-run': '--dry-run: perform dry run without making changes',
                '--edit': '--edit/-e: edit merge commit message',
                '--ff': '--ff: fast-forward if possible',
                '--ff-only': '--ff-only: refuse to merge unless fast-forward',
                '--force': '--force/-f: force overwrite of local branches',
                '--gpg-sign': '--gpg-sign/-S: GPG-sign the resulting merge commit',
                '--ipv4': '--ipv4/-4: use IPv4 addresses only',
                '--ipv6': '--ipv6/-6: use IPv6 addresses only',
                '--jobs': '--jobs/-j: number of parallel fetch operations',
                '--keep': '--keep/-k: keep downloaded pack',
                '--log': '--log: add commit messages to merge commit',
                '--negotiation-tip': '--negotiation-tip: report commits for negotiation',
                '--no-autostash': '--no-autostash: do not automatically stash',
                '--no-commit': '--no-commit: perform merge but do not commit',
                '--no-edit': '--no-edit: do not edit merge commit message',
                '--no-ff': '--no-ff: create merge commit even if fast-forward',
                '--no-gpg-sign': '--no-gpg-sign: do not GPG-sign merge commit',
                '--no-log': '--no-log: do not add commit messages',
                '--no-rebase': '--no-rebase: merge instead of rebasing',
                '--no-recurse-submodules': '--no-recurse-submodules: do not recurse into submodules',
                '--no-show-forced-updates': '--no-show-forced-updates: do not check for force-updates',
                '--no-signoff': '--no-signoff: do not add Signed-off-by line',
                '--no-squash': '--no-squash: do not squash commits',
                '--no-stat': '--no-stat/-n: do not show diffstat',
                '--no-tags': '--no-tags: do not fetch tags',
                '--no-verify': '--no-verify: bypass pre-merge hooks',
                '--no-verify-signatures': '--no-verify-signatures: do not verify GPG signatures',
                '--prefetch': '--prefetch: modify refspec to place refs in refs/prefetch/',
                '--progress': '--progress: force progress reporting',
                '--prune': '--prune/-p: remove remote-tracking branches that no longer exist',
                '--quiet': '--quiet/-q: suppress progress reporting',
                '--rebase': '--rebase/-r: rebase current branch on top of upstream',
                '--recurse-submodules': '--recurse-submodules: recurse into submodules',
                '--refmap': '--refmap: specify refmap',
                '--server-option': '--server-option/-o: transmit string to server',
                '--set-upstream': '--set-upstream: set upstream for git pull/status',
                '--shallow-exclude': '--shallow-exclude: shallow clone excluding revision',
                '--shallow-since': '--shallow-since: shallow clone from a date',
                '--show-forced-updates': '--show-forced-updates: check if branches were force-updated',
                '--signoff': '--signoff: add Signed-off-by line',
                '--squash': '--squash: create single commit from merge',
                '--stat': '--stat: show diffstat at end',
                '--strategy': '--strategy/-s: merge strategy to use',
                '--strategy-option': '--strategy-option/-X: option for merge strategy',
                '--tags': '--tags/-t: fetch all tags',
                '--unshallow': '--unshallow: convert shallow repository to complete one',
                '--update-shallow': '--update-shallow: accept refs that update .git/shallow',
                '--upload-pack': '--upload-pack: path to git-upload-pack on remote',
                '--verbose': '--verbose/-v: be more verbose',
                '--verify': '--verify: run pre-merge hooks',
                '--verify-signatures': '--verify-signatures: verify GPG signatures',
                '-4': '-4/--ipv4: use IPv4 addresses only',
                '-6': '-6/--ipv6: use IPv6 addresses only',
                '-S': '-S/--gpg-sign: GPG-sign the resulting merge commit',
                '-X': '-X/--strategy-option: option for merge strategy',
                '-a': '-a/--append: append to .git/FETCH_HEAD',
                '-e': '-e/--edit: edit merge commit message',
                '-f': '-f/--force: force overwrite of local branches',
                '-j': '-j/--jobs: number of parallel fetch operations',
                '-k': '-k/--keep: keep downloaded pack',
                '-n': '-n/--no-stat: do not show diffstat',
                '-o': '-o/--server-option: transmit string to server',
                '-p': '-p/--prune: remove remote-tracking branches that no longer exist',
                '-q': '-q/--quiet: suppress progress reporting',
                '-r': '-r/--rebase: rebase current branch on top of upstream',
                '-s': '-s/--strategy: merge strategy to use',
                '-t': '-t/--tags: fetch all tags',
                '-v': '-v/--verbose: be more verbose',
            }
            return {**{k: k for k in common_flags}, **pull_flags}
        elif subcommand == 'checkout':
            checkout_flags = {
                '--branch': '--branch/-b: create and checkout new branch',
                '--conflict': '--conflict: conflict resolution style',
                '--detach': '--detach/-d: detach HEAD at commit',
                '--force': '--force/-f: force checkout (discard local changes)',
                '--guess': '--guess: try to find remote branch with same name',
                '--ignore-other-worktrees': '--ignore-other-worktrees: do not check if branch is checked out elsewhere',
                '--ignore-skip-worktree-bits': '--ignore-skip-worktree-bits: ignore skip-worktree bit',
                '--merge': '--merge/-m: perform three-way merge with local changes',
                '--no-guess': '--no-guess: do not try to guess remote branch',
                '--no-overlay': '--no-overlay: remove files not in tree',
                '--no-overwrite-ignore': '--no-overwrite-ignore: do not update ignored files',
                '--no-progress': '--no-progress: do not force progress reporting',
                '--no-recurse-submodules': '--no-recurse-submodules: do not update submodules',
                '--no-track': '--no-track: do not set up upstream tracking',
                '--orphan': '--orphan: create new orphan branch',
                '--ours': '--ours: checkout our version for unmerged files',
                '--overlay': '--overlay: use overlay mode (default)',
                '--overwrite-ignore': '--overwrite-ignore: update ignored files (default)',
                '--patch': '--patch/-p: interactively select hunks',
                '--pathspec-file-nul': '--pathspec-file-nul: pathspec file is NUL-separated',
                '--pathspec-from-file': '--pathspec-from-file: read pathspec from file',
                '--progress': '--progress: force progress reporting',
                '--quiet': '--quiet/-q: suppress progress reporting',
                '--recurse-submodules': '--recurse-submodules: update submodules',
                '--theirs': '--theirs: checkout their version for unmerged files',
                '--track': '--track/-t: set upstream tracking',
                '-B': '-B: create/reset and checkout branch',
                '-b': '-b/--branch: create and checkout new branch',
                '-d': '-d/--detach: detach HEAD at commit',
                '-f': '-f/--force: force checkout (discard local changes)',
                '-l': '-l: create reflog for new branch',
                '-m': '-m/--merge: perform three-way merge with local changes',
                '-p': '-p/--patch: interactively select hunks',
                '-q': '-q/--quiet: suppress progress reporting',
                '-t': '-t/--track: set upstream tracking',
            }
            return {**{k: k for k in common_flags}, **checkout_flags}
        elif subcommand == 'add':
            add_flags = {
                '--all': '--all/-A: add changes from all tracked and untracked files',
                '--chmod': '--chmod: override executable bit of added files',
                '--dry-run': '--dry-run/-n: do not actually add files',
                '--edit': '--edit/-e: edit diff before adding',
                '--force': '--force/-f: allow adding ignored files',
                '--ignore-errors': '--ignore-errors: continue on errors',
                '--ignore-missing': '--ignore-missing: ignore missing files',
                '--ignore-removal': '--ignore-removal: ignore removed files',
                '--intent-to-add': '--intent-to-add/-N: record only the fact that path will be added later',
                '--interactive': '--interactive/-i: interactive adding',
                '--no-ignore-removal': '--no-ignore-removal: also add removed files (default)',
                '--no-refresh': '--no-refresh: do not refresh stat information',
                '--no-sparse': '--no-sparse: do not allow updating sparse entries',
                '--patch': '--patch/-p: interactively choose hunks to add',
                '--pathspec-file-nul': '--pathspec-file-nul: pathspec file is NUL-separated',
                '--pathspec-from-file': '--pathspec-from-file: read pathspec from file',
                '--refresh': '--refresh: refresh stat information',
                '--renormalize': '--renormalize: renormalize EOL of tracked files',
                '--sparse': '--sparse: allow updating sparse checkout entries',
                '--update': '--update/-u: update tracked files',
                '--verbose': '--verbose/-v: be verbose',
                '-A': '-A/--all: add changes from all tracked and untracked files',
                '-N': '-N/--intent-to-add: record only the fact that path will be added later',
                '-e': '-e/--edit: edit diff before adding',
                '-f': '-f/--force: allow adding ignored files',
                '-i': '-i/--interactive: interactive adding',
                '-n': '-n/--dry-run: do not actually add files',
                '-p': '-p/--patch: interactively choose hunks to add',
                '-u': '-u/--update: update tracked files',
                '-v': '-v/--verbose: be verbose',
            }
            return {**{k: k for k in common_flags}, **add_flags}
        elif subcommand == 'log':
            log_flags = {
                '--abbrev-commit': '--abbrev-commit: show abbreviated commit object names',
                '--after': '--after/--since: show commits more recent than date',
                '--all': '--all: pretend as if all refs in refs/ are listed',
                '--all-match': '--all-match: require all grep patterns to match',
                '--author': '--author: limit commits to author matching pattern',
                '--before': '--before/--until: show commits older than date',
                '--clear-decorations': '--clear-decorations: clear all previous decoration filters',
                '--committer': '--committer: limit commits to committer matching pattern',
                '--decorate': '--decorate: print out ref names',
                '--decorate-refs': '--decorate-refs: only decorate refs matching pattern',
                '--decorate-refs-exclude': '--decorate-refs-exclude: do not decorate refs matching pattern',
                '--diff-filter': '--diff-filter: select files by diff type',
                '--find-copies': '--find-copies/-C: detect copies',
                '--find-copies-harder': '--find-copies-harder: inspect unmodified files for copies',
                '--find-renames': '--find-renames/-M: detect renames',
                '--first-parent': '--first-parent: follow only first parent on merge commits',
                '--follow': '--follow: follow file history across renames',
                '--format': '--format: alias for --pretty',
                '--graph': '--graph: draw text-based graph of commit history',
                '--grep': '--grep: limit commits to those with message matching pattern',
                '--invert-grep': '--invert-grep: show commits not matching grep pattern',
                '--mailmap': '--mailmap/--use-mailmap: use mailmap file',
                '--max-age': '--max-age: maximum age of commits',
                '--max-count': '--max-count/-n: limit number of commits',
                '--merge': '--merge: show only commits related to merge conflicts',
                '--merges': '--merges: show only merge commits',
                '--min-age': '--min-age: minimum age of commits',
                '--name-only': '--name-only: show only names of changed files',
                '--name-status': '--name-status: show names and status of changed files',
                '--no-abbrev-commit': '--no-abbrev-commit: show full commit object names',
                '--no-merges': '--no-merges: do not show merge commits',
                '--no-patch': '--no-patch: suppress diff output',
                '--numstat': '--numstat: show numeric diffstat',
                '--oneline': '--oneline: shorthand for --pretty=oneline --abbrev-commit',
                '--patch': '--patch/-p: generate patch',
                '--pickaxe-all': '--pickaxe-all: show all changes in changeset with -S',
                '--pretty': '--pretty: format commit log messages',
                '--quiet': '--quiet/-q: suppress diff output',
                '--relative': '--relative: show only changes in subdirectory',
                '--reverse': '--reverse: output commits in reverse order',
                '--shortstat': '--shortstat: show only changed/insertions/deletions line',
                '--since': '--since/--after: show commits more recent than date',
                '--skip': '--skip: skip number of commits before output',
                '--source': '--source: show source of each commit',
                '--stat': '--stat: show diffstat',
                '--until': '--until/--before: show commits older than date',
                '--use-mailmap': '--use-mailmap/--mailmap: use mailmap file',
                '--walk-reflogs': '--walk-reflogs: walk reflog entries',
                '-C': '-C/--find-copies: detect copies',
                '-G': '-G: look for differences whose patch text contains pattern',
                '-L': '-L: trace line range evolution',
                '-M': '-M/--find-renames: detect renames',
                '-S': '-S: look for differences that change number of occurrences',
                '-n': '-n/--max-count: limit number of commits',
                '-p': '-p/--patch: generate patch',
                '-q': '-q/--quiet: suppress diff output',
            }
            return {**{k: k for k in common_flags}, **log_flags}
        elif subcommand == 'diff':
            diff_flags = {
                '--abbrev': '--abbrev: show abbreviated object names',
                '--cached': '--cached/--staged: show staged changes',
                '--check': '--check: warn if changes introduce whitespace errors',
                '--color-words': '--color-words: show word diff with colors',
                '--diff-algorithm': '--diff-algorithm: choose diff algorithm',
                '--diff-filter': '--diff-filter: select files by diff type',
                '--exit-code': '--exit-code: exit with 1 if differences exist',
                '--find-copies-harder': '--find-copies-harder: inspect unmodified files for copies',
                '--full-index': '--full-index: show full blob object names',
                '--function-context': '--function-context/-W: show whole function as context',
                '--histogram': '--histogram: use histogram diff algorithm',
                '--ignore-all-space': '--ignore-all-space/-w: ignore all whitespace',
                '--ignore-blank-lines': '--ignore-blank-lines: ignore blank line changes',
                '--ignore-space-at-eol': '--ignore-space-at-eol: ignore whitespace at line end',
                '--ignore-space-change': '--ignore-space-change/-b: ignore changes in whitespace',
                '--inter-hunk-context': '--inter-hunk-context: show context between diff hunks',
                '--merge-base': '--merge-base: use merge base for three-way diff',
                '--minimal': '--minimal: spend extra time to find minimal diff',
                '--name-only': '--name-only: show only names of changed files',
                '--name-status': '--name-status: show names and status of changed files',
                '--no-index': '--no-index: compare files outside repository',
                '--no-patch': '--no-patch: suppress diff output',
                '--no-renames': '--no-renames: turn off rename detection',
                '--numstat': '--numstat: generate numeric diffstat',
                '--output': '--output/-o: output to file',
                '--patch': '--patch/-p/-u: generate patch',
                '--patch-with-raw': '--patch-with-raw: synonym for -p --raw',
                '--patch-with-stat': '--patch-with-stat: synonym for -p --stat',
                '--patience': '--patience: use patience diff algorithm',
                '--pickaxe-all': '--pickaxe-all: show all changes in changeset with -S',
                '--quiet': '--quiet: disable all output',
                '--relative': '--relative: show only changes in subdirectory',
                '--shortstat': '--shortstat: output only last line of diffstat',
                '--staged': '--staged/--cached: show staged changes',
                '--stat': '--stat: generate diffstat',
                '--text': '--text/-a: treat all files as text',
                '--unified': '--unified/-U: lines of context',
                '--word-diff': '--word-diff: show word diff',
                '--word-diff-regex': '--word-diff-regex: word diff regex',
                '-B': '-B: detect complete rewrites',
                '-C': '-C: detect copies',
                '-G': '-G: look for differences whose patch text contains pattern',
                '-M': '-M: detect renames',
                '-O': '-O: output patch in order specified by file',
                '-R': '-R: swap inputs (reverse diff)',
                '-S': '-S: look for differences that change number of occurrences',
                '-U': '-U/--unified: lines of context',
                '-W': '-W/--function-context: show whole function as context',
                '-a': '-a/--text: treat all files as text',
                '-b': '-b/--ignore-space-change: ignore changes in whitespace',
                '-l': '-l: limit rename/copy detection',
                '-o': '-o/--output: output to file',
                '-p': '-p/--patch/-u: generate patch',
                '-u': '-u/--patch/-p: generate patch',
                '-w': '-w/--ignore-all-space: ignore all whitespace',
                '-z': '-z: output file names with NUL termination',
            }
            return {**{k: k for k in common_flags}, **diff_flags}
        elif subcommand == 'branch':
            branch_flags = {
                '--abbrev': '--abbrev: set minimum abbreviation length',
                '--all': '--all/-a: list both remote and local branches',
                '--color': '--color: use colors in output',
                '--column': '--column: display branches in columns',
                '--contains': '--contains: list branches containing commit',
                '--copy': '--copy/-c/-C: copy branch',
                '--create-reflog': '--create-reflog: create reflog for branch',
                '--delete': '--delete/-d/-D: delete branch',
                '--edit-description': '--edit-description: edit branch description',
                '--force': '--force/-f: reset branch to startpoint',
                '--format': '--format: format string for output',
                '--ignore-case': '--ignore-case/-i: ignore case when matching',
                '--list': '--list/-l: list branches',
                '--merged': '--merged: list branches merged into HEAD',
                '--move': '--move/-m/-M: move/rename branch',
                '--no-color': '--no-color: do not use colors',
                '--no-column': '--no-column: do not display in columns',
                '--no-contains': '--no-contains: list branches not containing commit',
                '--no-merged': '--no-merged: list branches not merged into HEAD',
                '--no-track': '--no-track: do not set up tracking',
                '--omit-empty': '--omit-empty: do not print newline after formatted refs',
                '--points-at': '--points-at: list branches pointing at object',
                '--quiet': '--quiet/-q: suppress informational messages',
                '--recurse-submodules': '--recurse-submodules: update submodules',
                '--remotes': '--remotes/-r: list or delete remote-tracking branches',
                '--set-upstream-to': '--set-upstream-to/-u: set upstream tracking',
                '--show-current': '--show-current: print name of current branch',
                '--sort': '--sort: field to sort on',
                '--track': '--track/-t: set up tracking mode',
                '--unset-upstream': '--unset-upstream: remove upstream information',
                '--verbose': '--verbose/-v: show hash and commit subject',
                '-C': '-C/--copy/-c: force copy branch',
                '-D': '-D/--delete/-d: force delete branch',
                '-M': '-M/--move/-m: force move/rename',
                '-a': '-a/--all: list both remote and local branches',
                '-c': '-c/--copy/-C: copy branch',
                '-d': '-d/--delete/-D: delete branch',
                '-f': '-f/--force: reset branch to startpoint',
                '-i': '-i/--ignore-case: ignore case when matching',
                '-l': '-l/--list: list branches',
                '-m': '-m/--move/-M: move/rename branch',
                '-q': '-q/--quiet: suppress informational messages',
                '-r': '-r/--remotes: list or delete remote-tracking branches',
                '-t': '-t/--track: set up tracking mode',
                '-u': '-u/--set-upstream-to: set upstream tracking',
                '-v': '-v/--verbose: show hash and commit subject',
            }
            return {**{k: k for k in common_flags}, **branch_flags}
        elif subcommand == 'merge':
            merge_flags = {
                '--abort': '--abort: abort current merge',
                '--allow-unrelated-histories': '--allow-unrelated-histories: allow merging unrelated histories',
                '--autostash': '--autostash: automatically stash/unstash',
                '--cleanup': '--cleanup: how to strip whitespace from message',
                '--commit': '--commit: perform merge and commit',
                '--continue': '--continue: continue current merge',
                '--edit': '--edit/-e: edit merge message before committing',
                '--ff': '--ff: fast-forward if possible (default)',
                '--ff-only': '--ff-only: refuse to merge unless fast-forward',
                '--file': '--file/-F: read message from file',
                '--gpg-sign': '--gpg-sign/-S: GPG-sign merge commit',
                '--into-name': '--into-name: use name instead of real ref name',
                '--log': '--log: add commit messages to merge message',
                '--message': '--message/-m: merge commit message',
                '--no-autostash': '--no-autostash: do not automatically stash',
                '--no-commit': '--no-commit: perform merge but do not commit',
                '--no-edit': '--no-edit: accept auto-generated merge message',
                '--no-ff': '--no-ff: always create merge commit',
                '--no-gpg-sign': '--no-gpg-sign: do not GPG-sign',
                '--no-log': '--no-log: do not add commit messages',
                '--no-overwrite-ignore': '--no-overwrite-ignore: do not update ignored files',
                '--no-progress': '--no-progress: do not force progress reporting',
                '--no-rerere-autoupdate': '--no-rerere-autoupdate: do not update index automatically',
                '--no-signoff': '--no-signoff: do not add Signed-off-by line',
                '--no-squash': '--no-squash: create merge commit (default)',
                '--no-stat': '--no-stat/-n: do not show diffstat',
                '--no-summary': '--no-summary: do not show summary',
                '--no-verify': '--no-verify: bypass pre-merge hook',
                '--no-verify-signatures': '--no-verify-signatures: do not verify signatures',
                '--overwrite-ignore': '--overwrite-ignore: update ignored files (default)',
                '--progress': '--progress: force progress reporting',
                '--quiet': '--quiet/-q: be more quiet',
                '--quit': '--quit: forget about current merge',
                '--rerere-autoupdate': '--rerere-autoupdate: update index with reused resolution',
                '--signoff': '--signoff: add Signed-off-by line',
                '--squash': '--squash: create single commit without merge commit',
                '--stat': '--stat: show diffstat at end',
                '--strategy': '--strategy/-s: merge strategy to use',
                '--strategy-option': '--strategy-option/-X: option for merge strategy',
                '--summary': '--summary: show summary of created/deleted files',
                '--verbose': '--verbose/-v: be more verbose',
                '--verify': '--verify: run pre-merge hook',
                '--verify-signatures': '--verify-signatures: verify commits are signed',
                '-F': '-F/--file: read message from file',
                '-S': '-S/--gpg-sign: GPG-sign merge commit',
                '-X': '-X/--strategy-option: option for merge strategy',
                '-e': '-e/--edit: edit merge message before committing',
                '-m': '-m/--message: merge commit message',
                '-n': '-n/--no-stat: do not show diffstat',
                '-q': '-q/--quiet: be more quiet',
                '-s': '-s/--strategy: merge strategy to use',
                '-v': '-v/--verbose: be more verbose',
            }
            return {**{k: k for k in common_flags}, **merge_flags}
        elif subcommand == 'rebase':
            rebase_flags = {
                '--abort': '--abort: abort rebase and return to original',
                '--apply': '--apply: use apply-based rebase',
                '--autosquash': '--autosquash: automatically squash/fixup commits',
                '--autostash': '--autostash: automatically stash/unstash',
                '--committer-date-is-author-date': '--committer-date-is-author-date: use author date as committer date',
                '--continue': '--continue: continue after resolving conflicts',
                '--edit-todo': '--edit-todo: edit todo list during interactive rebase',
                '--empty': '--empty: how to handle empty commits',
                '--exec': '--exec/-x: execute command after each commit',
                '--ff': '--ff: fast-forward if possible',
                '--force-rebase': '--force-rebase/-f: force rebase even if branch up-to-date',
                '--fork-point': '--fork-point: use reflog to find better common ancestor',
                '--gpg-sign': '--gpg-sign/-S: GPG-sign commits',
                '--ignore-whitespace': '--ignore-whitespace: ignore whitespace in context',
                '--interactive': '--interactive/-i: interactive rebase',
                '--keep-base': '--keep-base: use merge-base of upstream and branch',
                '--merge': '--merge/-m: use merge-based rebase',
                '--no-autosquash': '--no-autosquash: do not automatically squash',
                '--no-autostash': '--no-autostash: do not automatically stash',
                '--no-ff': '--no-ff: force creation of new commits',
                '--no-fork-point': '--no-fork-point: do not use reflog',
                '--no-gpg-sign': '--no-gpg-sign: do not GPG-sign',
                '--no-reapply-cherry-picks': '--no-reapply-cherry-picks: skip commits with upstream equivalent',
                '--no-rerere-autoupdate': '--no-rerere-autoupdate: do not update index automatically',
                '--no-reschedule-failed-exec': '--no-reschedule-failed-exec: do not reschedule failed exec',
                '--no-signoff': '--no-signoff: do not add Signed-off-by line',
                '--no-stat': '--no-stat/-n: do not show diffstat',
                '--no-update-refs': '--no-update-refs: do not update branches',
                '--no-verify': '--no-verify: bypass pre-rebase hook',
                '--onto': '--onto: rebase onto this branch',
                '--quiet': '--quiet/-q: be quiet',
                '--quit': '--quit: abort but keep HEAD where it is',
                '--reapply-cherry-picks': '--reapply-cherry-picks: reapply commits even if upstream has equivalent',
                '--rebase-merges': '--rebase-merges/-r: try to rebase merges',
                '--rerere-autoupdate': '--rerere-autoupdate: update index with reused resolution',
                '--reschedule-failed-exec': '--reschedule-failed-exec: reschedule failed exec commands',
                '--reset-author-date': '--reset-author-date: reset author date to committer date',
                '--root': '--root: rebase all commits reachable from branch',
                '--show-current-patch': '--show-current-patch: show patch in progress',
                '--signoff': '--signoff: add Signed-off-by line',
                '--skip': '--skip: skip current patch and continue',
                '--stat': '--stat: show diffstat',
                '--strategy': '--strategy/-s: merge strategy to use',
                '--strategy-option': '--strategy-option/-X: option for merge strategy',
                '--update-refs': '--update-refs: update branches pointing to rebased commits',
                '--verbose': '--verbose/-v: be verbose',
                '--verify': '--verify: run pre-rebase hook',
                '--whitespace': '--whitespace: pass to git-apply',
                '-C': '-C: pass -C option to git-apply',
                '-S': '-S/--gpg-sign: GPG-sign commits',
                '-X': '-X/--strategy-option: option for merge strategy',
                '-f': '-f/--force-rebase: force rebase even if branch up-to-date',
                '-i': '-i/--interactive: interactive rebase',
                '-m': '-m/--merge: use merge-based rebase',
                '-n': '-n/--no-stat: do not show diffstat',
                '-q': '-q/--quiet: be quiet',
                '-r': '-r/--rebase-merges: try to rebase merges',
                '-s': '-s/--strategy: merge strategy to use',
                '-v': '-v/--verbose: be verbose',
                '-x': '-x/--exec: execute command after each commit',
            }
            return {**{k: k for k in common_flags}, **rebase_flags}
        elif subcommand == 'reset':
            reset_flags = {
                '--hard': '--hard: reset index and working tree',
                '--intent-to-add': '--intent-to-add/-N: record only intent to add',
                '--keep': '--keep: reset index entries and update files different between commit and HEAD',
                '--merge': '--merge: reset index and update files different between commit and HEAD',
                '--mixed': '--mixed: reset index but not working tree (default)',
                '--no-recurse-submodules': '--no-recurse-submodules: do not recursively reset',
                '--no-refresh': '--no-refresh: do not refresh index',
                '--patch': '--patch/-p: interactively select hunks to reset',
                '--pathspec-file-nul': '--pathspec-file-nul: pathspec file is NUL-separated',
                '--pathspec-from-file': '--pathspec-from-file: read pathspec from file',
                '--quiet': '--quiet/-q: be quiet',
                '--recurse-submodules': '--recurse-submodules: recursively reset submodules',
                '--refresh': '--refresh: refresh index after reset',
                '--soft': '--soft: do not touch index or working tree',
                '-N': '-N/--intent-to-add: record only intent to add',
                '-p': '-p/--patch: interactively select hunks to reset',
                '-q': '-q/--quiet: be quiet',
            }
            return {**{k: k for k in common_flags}, **reset_flags}
        elif subcommand == 'stash':
            stash_flags = {
                '--all': '--all/-a: include all untracked and ignored files',
                '--include-untracked': '--include-untracked/-u: include untracked files',
                '--index': '--index: try to reinstate index changes',
                '--keep-index': '--keep-index/-k: keep changes already added to index',
                '--message': '--message/-m: stash message',
                '--no-keep-index': '--no-keep-index: do not keep index changes',
                '--only-untracked': '--only-untracked: stash only untracked files',
                '--patch': '--patch/-p: interactively select hunks',
                '--pathspec-file-nul': '--pathspec-file-nul: pathspec file is NUL-separated',
                '--pathspec-from-file': '--pathspec-from-file: read pathspec from file',
                '--quiet': '--quiet/-q: be quiet',
                '--staged': '--staged/-S: stash only staged changes',
                '-S': '-S/--staged: stash only staged changes',
                '-a': '-a/--all: include all untracked and ignored files',
                '-k': '-k/--keep-index: keep changes already added to index',
                '-m': '-m/--message: stash message',
                '-p': '-p/--patch: interactively select hunks',
                '-q': '-q/--quiet: be quiet',
                '-u': '-u/--include-untracked: include untracked files',
            }
            return {**{k: k for k in common_flags}, **stash_flags}
        elif subcommand == 'fetch':
            fetch_flags = {
                '--all': '--all: fetch from all remotes',
                '--append': '--append/-a: append to .git/FETCH_HEAD',
                '--atomic': '--atomic: use atomic transaction',
                '--auto-gc': '--auto-gc: run git gc --auto after fetch',
                '--auto-maintenance': '--auto-maintenance: run maintenance after fetch',
                '--deepen': '--deepen: deepen history of shallow repository',
                '--depth': '--depth: limit fetching to depth',
                '--dry-run': '--dry-run: show what would be done',
                '--filter': '--filter: object filtering',
                '--force': '--force/-f: force update of local branches',
                '--ipv4': '--ipv4/-4: use IPv4 addresses only',
                '--ipv6': '--ipv6/-6: use IPv6 addresses only',
                '--jobs': '--jobs/-j: number of parallel fetch operations',
                '--keep': '--keep/-k: keep downloaded pack',
                '--multiple': '--multiple/-m: fetch from multiple remotes',
                '--negotiate-only': '--negotiate-only: only print common ancestors',
                '--negotiation-tip': '--negotiation-tip: report commits for negotiation',
                '--no-auto-gc': '--no-auto-gc: do not run git gc --auto',
                '--no-auto-maintenance': '--no-auto-maintenance: do not run maintenance',
                '--no-progress': '--no-progress: do not force progress reporting',
                '--no-recurse-submodules': '--no-recurse-submodules: do not fetch submodules',
                '--no-show-forced-updates': '--no-show-forced-updates: do not check for forced updates',
                '--no-tags': '--no-tags/-n: do not fetch tags',
                '--no-write-fetch-head': '--no-write-fetch-head: do not write to .git/FETCH_HEAD',
                '--porcelain': '--porcelain: machine-readable output',
                '--prefetch': '--prefetch: modify refspec to place refs in refs/prefetch/',
                '--progress': '--progress: force progress reporting',
                '--prune': '--prune/-p: remove remote-tracking branches that no longer exist',
                '--prune-tags': '--prune-tags/-P: remove local tags that no longer exist',
                '--quiet': '--quiet/-q: be more quiet',
                '--recurse-submodules': '--recurse-submodules: fetch submodules',
                '--refetch': '--refetch: re-fetch without negotiating common commits',
                '--refmap': '--refmap: specify refmap',
                '--server-option': '--server-option/-o: transmit string to server',
                '--set-upstream': '--set-upstream: set upstream for git pull/status',
                '--shallow-exclude': '--shallow-exclude: shallow fetch excluding revision',
                '--shallow-since': '--shallow-since: shallow fetch from date',
                '--show-forced-updates': '--show-forced-updates: check for forced updates',
                '--stdin': '--stdin: read refspecs from stdin',
                '--tags': '--tags/-t: fetch all tags',
                '--unshallow': '--unshallow: convert shallow repository to complete',
                '--update-head-ok': '--update-head-ok/-u: allow updating HEAD ref',
                '--update-shallow': '--update-shallow: accept refs that update .git/shallow',
                '--upload-pack': '--upload-pack: path to git-upload-pack on remote',
                '--verbose': '--verbose/-v: be more verbose',
                '--write-commit-graph': '--write-commit-graph: write commit-graph after fetch',
                '--write-fetch-head': '--write-fetch-head: write to .git/FETCH_HEAD',
                '-4': '-4/--ipv4: use IPv4 addresses only',
                '-6': '-6/--ipv6: use IPv6 addresses only',
                '-P': '-P/--prune-tags: remove local tags that no longer exist',
                '-a': '-a/--append: append to .git/FETCH_HEAD',
                '-f': '-f/--force: force update of local branches',
                '-j': '-j/--jobs: number of parallel fetch operations',
                '-k': '-k/--keep: keep downloaded pack',
                '-m': '-m/--multiple: fetch from multiple remotes',
                '-n': '-n/--no-tags: do not fetch tags',
                '-o': '-o/--server-option: transmit string to server',
                '-p': '-p/--prune: remove remote-tracking branches that no longer exist',
                '-q': '-q/--quiet: be more quiet',
                '-t': '-t/--tags: fetch all tags',
                '-u': '-u/--update-head-ok: allow updating HEAD ref',
                '-v': '-v/--verbose: be more verbose',
            }
            return {**{k: k for k in common_flags}, **fetch_flags}
        elif subcommand == 'clone':
            clone_flags = {
                '--also-filter-submodules': '--also-filter-submodules: apply filter to submodules',
                '--bare': '--bare: make bare Git repository',
                '--branch': '--branch/-b: checkout specific branch',
                '--bundle-uri': '--bundle-uri: location of bundle file',
                '--checkout': '--checkout: checkout HEAD after clone (default)',
                '--config': '--config/-c: set config in new repository',
                '--depth': '--depth: create shallow clone with depth',
                '--dissociate': '--dissociate: dissociate from reference repositories',
                '--filter': '--filter: object filtering',
                '--hardlinks': '--hardlinks: use hardlinks when possible',
                '--ipv4': '--ipv4/-4: use IPv4 addresses only',
                '--ipv6': '--ipv6/-6: use IPv6 addresses only',
                '--jobs': '--jobs/-j: number of parallel submodule fetches',
                '--local': '--local/-l: clone from local repository',
                '--mirror': '--mirror: clone as mirror (implies bare)',
                '--no-checkout': '--no-checkout/-n: do not checkout HEAD after clone',
                '--no-hardlinks': '--no-hardlinks: copy files instead of hardlinks',
                '--no-progress': '--no-progress: do not force progress reporting',
                '--no-recurse-submodules': '--no-recurse-submodules: do not initialize submodules',
                '--no-single-branch': '--no-single-branch: clone all branches',
                '--no-tags': '--no-tags: do not clone tags',
                '--origin': '--origin/-o: name for remote (default: origin)',
                '--progress': '--progress: force progress reporting',
                '--quiet': '--quiet/-q: be more quiet',
                '--recurse-submodules': '--recurse-submodules/--recursive: initialize submodules',
                '--recursive': '--recursive/--recurse-submodules: initialize submodules',
                '--ref-format': '--ref-format: ref storage format',
                '--reference': '--reference: reference repository',
                '--reference-if-able': '--reference-if-able: reference if possible',
                '--reject-shallow': '--reject-shallow: reject cloning shallow repository',
                '--remote-submodules': '--remote-submodules: use submodule remote-tracking branches',
                '--revision': '--revision: use specific revision',
                '--separate-git-dir': '--separate-git-dir: separate git directory',
                '--server-option': '--server-option: transmit string to server',
                '--shallow-exclude': '--shallow-exclude: shallow clone excluding revision',
                '--shallow-since': '--shallow-since: shallow clone from date',
                '--shallow-submodules': '--shallow-submodules: clone submodules shallowly',
                '--shared': '--shared/-s: share objects with source repository',
                '--single-branch': '--single-branch: clone only one branch',
                '--sparse': '--sparse: initialize sparse-checkout',
                '--tags': '--tags: clone all tags',
                '--template': '--template: directory for templates',
                '--upload-pack': '--upload-pack/-u: path to git-upload-pack',
                '--verbose': '--verbose/-v: be more verbose',
                '-4': '-4/--ipv4: use IPv4 addresses only',
                '-6': '-6/--ipv6: use IPv6 addresses only',
                '-b': '-b/--branch: checkout specific branch',
                '-c': '-c/--config: set config in new repository',
                '-j': '-j/--jobs: number of parallel submodule fetches',
                '-l': '-l/--local: clone from local repository',
                '-n': '-n/--no-checkout: do not checkout HEAD after clone',
                '-o': '-o/--origin: name for remote (default: origin)',
                '-q': '-q/--quiet: be more quiet',
                '-s': '-s/--shared: share objects with source repository',
                '-u': '-u/--upload-pack: path to git-upload-pack',
                '-v': '-v/--verbose: be more verbose',
            }
            return {**{k: k for k in common_flags}, **clone_flags}
        elif subcommand == 'remote':
            return common_flags
        elif subcommand == 'tag':
            tag_flags = {
                '--annotate': '--annotate/-a: create annotated tag',
                '--cleanup': '--cleanup: how to strip whitespace from message',
                '--color': '--color: use colors in output',
                '--column': '--column: display tags in columns',
                '--contains': '--contains: list tags containing commit',
                '--create-reflog': '--create-reflog: create reflog',
                '--delete': '--delete/-d: delete tags',
                '--edit': '--edit/-e: edit tag message',
                '--file': '--file/-F: read message from file',
                '--force': '--force/-f: replace existing tag',
                '--format': '--format: format string for output',
                '--ignore-case': '--ignore-case/-i: ignore case when matching',
                '--list': '--list/-l: list tags',
                '--local-user': '--local-user/-u: use another key to sign',
                '--merged': '--merged: list tags merged into HEAD',
                '--message': '--message/-m: tag message',
                '--no-color': '--no-color: do not use colors',
                '--no-column': '--no-column: do not display in columns',
                '--no-contains': '--no-contains: list tags not containing commit',
                '--no-merged': '--no-merged: list tags not merged into HEAD',
                '--omit-empty': '--omit-empty: do not print newline after formatted refs',
                '--points-at': '--points-at: list tags pointing at object',
                '--sign': '--sign/-s: GPG-sign tag',
                '--sort': '--sort: field to sort on',
                '--trailer': '--trailer: add trailer to tag message',
                '--verify': '--verify/-v: verify GPG signature of tags',
                '-F': '-F/--file: read message from file',
                '-a': '-a/--annotate: create annotated tag',
                '-d': '-d/--delete: delete tags',
                '-e': '-e/--edit: edit tag message',
                '-f': '-f/--force: replace existing tag',
                '-i': '-i/--ignore-case: ignore case when matching',
                '-l': '-l/--list: list tags',
                '-m': '-m/--message: tag message',
                '-n': '-n: print <n> lines of annotation',
                '-s': '-s/--sign: GPG-sign tag',
                '-u': '-u/--local-user: use another key to sign',
                '-v': '-v/--verify: verify GPG signature of tags',
            }
            return {**{k: k for k in common_flags}, **tag_flags}
        else:
            return common_flags

    # git [subcommand] ...
    if cursor_token_idx == 0:
        if is_after:
            return {
                'add': 'add file contents to the index',
                'am': 'apply patches from a mailbox',
                'annotate': 'annotate file lines with commit info',
                'apply': 'apply a patch to files or index',
                'archive': 'create archive of files from tree',
                'bisect': 'find commit that introduced a bug',
                'blame': 'show what revision last modified lines',
                'branch': 'list, create, or delete branches',
                'bundle': 'move objects and refs by archive',
                'checkout': 'switch branches or restore files',
                'cherry-pick': 'apply changes from existing commits',
                'clean': 'remove untracked files from working tree',
                'clone': 'clone a repository into a new directory',
                'commit': 'record changes to the repository',
                'config': 'get and set repository or global options',
                'describe': 'describe commit using most recent tag',
                'diff': 'show changes between commits or working tree',
                'fetch': 'download objects and refs from repository',
                'format-patch': 'prepare patches for email submission',
                'gc': 'cleanup unnecessary files and optimize repo',
                'grep': 'print lines matching a pattern',
                'init': 'create an empty git repository',
                'log': 'show commit logs',
                'merge': 'join two or more development histories',
                'mv': 'move or rename a file or directory',
                'notes': 'add or inspect object notes',
                'pull': 'fetch and integrate with another repository',
                'push': 'update remote refs along with objects',
                'range-diff': 'compare two commit ranges',
                'rebase': 'reapply commits on top of another base',
                'reflog': 'manage reflog information',
                'remote': 'manage set of tracked repositories',
                'reset': 'reset current HEAD to specified state',
                'restore': 'restore working tree files',
                'revert': 'revert existing commits',
                'rm': 'remove files from working tree and index',
                'shortlog': 'summarize git log output',
                'show': 'show various types of objects',
                'show-branch': 'show branches and their commits',
                'stash': 'stash changes in dirty working directory',
                'status': 'show working tree status',
                'submodule': 'initialize, update or inspect submodules',
                'switch': 'switch branches',
                'tag': 'create, list, delete or verify tags',
                'whatchanged': 'show logs with difference each commit',
                'worktree': 'manage multiple working trees'
            }

    elif cursor_token_idx == 1:
        # Complete subcommands when cursor is in or at the end of token 1
        # This handles both "git c|" and "git comm|" cases
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        # If the subcommand is incomplete or we're still typing it, show all subcommands
        # Check if it's not a recognized complete subcommand
        known_subcommands = {'add', 'am', 'annotate', 'apply', 'archive', 'bisect', 'blame',
                           'branch', 'bundle', 'checkout', 'cherry-pick', 'clean', 'clone',
                           'commit', 'config', 'describe', 'diff', 'fetch', 'format-patch',
                           'gc', 'grep', 'init', 'log', 'merge', 'mv', 'notes', 'pull',
                           'push', 'range-diff', 'rebase', 'reflog', 'remote', 'reset',
                           'restore', 'revert', 'rm', 'shortlog', 'show', 'show-branch',
                           'stash', 'status', 'submodule', 'switch', 'tag', 'whatchanged',
                           'worktree'}

        if subcommand not in known_subcommands or not is_after:
            # Still completing the subcommand
            return {
                'add': 'add file contents to the index',
                'am': 'apply patches from a mailbox',
                'annotate': 'annotate file lines with commit info',
                'apply': 'apply a patch to files or index',
                'archive': 'create archive of files from tree',
                'bisect': 'find commit that introduced a bug',
                'blame': 'show what revision last modified lines',
                'branch': 'list, create, or delete branches',
                'bundle': 'move objects and refs by archive',
                'checkout': 'switch branches or restore files',
                'cherry-pick': 'apply changes from existing commits',
                'clean': 'remove untracked files from working tree',
                'clone': 'clone a repository into a new directory',
                'commit': 'record changes to the repository',
                'config': 'get and set repository or global options',
                'describe': 'describe commit using most recent tag',
                'diff': 'show changes between commits or working tree',
                'fetch': 'download objects and refs from repository',
                'format-patch': 'prepare patches for email submission',
                'gc': 'cleanup unnecessary files and optimize repo',
                'grep': 'print lines matching a pattern',
                'init': 'create an empty git repository',
                'log': 'show commit logs',
                'merge': 'join two or more development histories',
                'mv': 'move or rename a file or directory',
                'notes': 'add or inspect object notes',
                'pull': 'fetch and integrate with another repository',
                'push': 'update remote refs along with objects',
                'range-diff': 'compare two commit ranges',
                'rebase': 'reapply commits on top of another base',
                'reflog': 'manage reflog information',
                'remote': 'manage set of tracked repositories',
                'reset': 'reset current HEAD to specified state',
                'restore': 'restore working tree files',
                'revert': 'revert existing commits',
                'rm': 'remove files from working tree and index',
                'shortlog': 'summarize git log output',
                'show': 'show various types of objects',
                'show-branch': 'show branches and their commits',
                'stash': 'stash changes in dirty working directory',
                'status': 'show working tree status',
                'submodule': 'initialize, update or inspect submodules',
                'switch': 'switch branches',
                'tag': 'create, list, delete or verify tags',
                'whatchanged': 'show logs with difference each commit',
                'worktree': 'manage multiple working trees'
            }

        if subcommand in ('push', 'pull', 'fetch'):
            return _get_git_remotes()
        elif subcommand in ('checkout', 'merge', 'rebase'):
            return _get_git_branches()
        elif subcommand == 'remote':
            return {
                'add': 'add a remote',
                'remove': 'remove a remote',
                'rename': 'rename a remote',
                'show': 'show information about a remote',
                'prune': 'delete stale remote-tracking branches',
                'update': 'fetch updates for remotes',
            }
        elif subcommand == 'stash':
            return {
                'push': 'save local modifications to stash',
                'pop': 'apply and remove a stash',
                'list': 'list all stashes',
                'show': 'show changes in a stash',
                'drop': 'remove a single stash',
                'clear': 'remove all stashes',
                'apply': 'apply a stash without removing it',
            }
        elif subcommand == 'branch':
            return _get_git_branches()

    elif cursor_token_idx >= 2:
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        if subcommand in ('push', 'pull', 'fetch'):
            # For push/pull, after remote we might want branch
            if cursor_token_idx == 2 and is_after:
                return _get_git_branches()
            return _get_git_remotes()
        elif subcommand in ('checkout', 'merge', 'rebase', 'branch'):
            return _get_git_branches()

    return None


@register_completion_schema('python')
def _python_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for python command."""
    # Look for flags starting with -
    current_token = tokens[cursor_token_idx] if cursor_token_idx < len(tokens) else None

    if current_token and current_token.text.startswith('-'):
        # Complete python flags
        return {
            '-c': '-c: execute Python code from command line',
            '-m': '-m: run module as script',
            '-h': '-h/--help: show help message',
            '--help': '--help/-h: show help message',
            '-V': '-V/--version: print version and exit',
            '--version': '--version/-V: print version and exit',
            '-u': '-u: unbuffered stdout and stderr',
            '-O': '-O: optimize bytecode',
            '-OO': '-OO: remove docstrings and optimize',
            '-B': '-B: don\'t write .pyc files',
            '-s': '-s: don\'t add user site directory',
            '-S': '-S: don\'t imply import site',
            '-E': '-E: ignore PYTHON* environment variables',
            '-I': '-I: isolated mode',
            '-W': '-W: warning control',
            '-X': '-X: set implementation-specific option',
        }

    return None


@register_completion_schema('python3')
def _python3_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for python3 command (same as python)."""
    return _python_completions(tokens, cursor_token_idx, is_after)


@register_completion_schema('rp')
def _rp_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for rp command."""
    # rp [subcommand] ...
    if cursor_token_idx == 0 and is_after:
        return {
            'help': 'show help message',
            'call': 'call a Python function with arguments',
            'exec': 'execute Python code with variable assignments',
        }

    # For flags, no specific flags for rp itself
    # The call/exec subcommands use dynamic Python evaluation
    return None



@register_completion_schema('gemini')
def _gemini_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for gemini command."""
    # Check for subcommands
    if cursor_token_idx == 0 and is_after:
        return {
            'mcp': 'manage MCP servers',
            'extensions': 'manage extensions',
        }

    current_token = tokens[cursor_token_idx] if cursor_token_idx < len(tokens) else None

    if current_token and current_token.text.startswith('-'):
        return {
            '--telemetry': 'enable telemetry',
            '-d': '-d/--debug: enable debug mode',
            '--debug': '--debug/-d: enable debug mode',
            '--proxy': 'HTTP proxy URL',
            '-m': '-m/--model: model to use',
            '--model': '--model/-m: model to use',
            '-p': '-p/--prompt: prompt text',
            '--prompt': '--prompt/-p: prompt text',
            '-i': '-i/--prompt-interactive: interactive prompt mode',
            '--prompt-interactive': '--prompt-interactive/-i: interactive prompt mode',
            '-s': '-s/--sandbox: enable sandbox mode',
            '--sandbox': '--sandbox/-s: enable sandbox mode',
            '--sandbox-image': 'Docker image for sandbox',
            '-a': '-a/--all-files: include all files in context',
            '--all-files': '--all-files/-a: include all files in context',
            '--show-memory-usage': 'show memory usage statistics',
            '-y': '-y/--yolo: skip confirmations (YOLO mode)',
            '--yolo': '--yolo/-y: skip confirmations (YOLO mode)',
            '--approval-mode': 'approval mode (auto, interactive, none)',
            '-c': '-c/--checkpointing: enable checkpointing',
            '--checkpointing': '--checkpointing/-c: enable checkpointing',
            '--experimental-acp': 'enable experimental ACP features',
            '--allowed-mcp-server-names': 'comma-separated list of allowed MCP servers',
            '--allowed-tools': 'comma-separated list of allowed tools',
            '-e': '-e/--extensions: comma-separated list of extensions',
            '--extensions': '--extensions/-e: comma-separated list of extensions',
            '-l': '-l/--list-extensions: list available extensions',
            '--list-extensions': '--list-extensions/-l: list available extensions',
            '--include-directories': 'directories to include in context',
            '--screen-reader': 'enable screen reader mode',
            '-o': '-o/--output-format: output format',
            '--output-format': '--output-format/-o: output format',
            '-v': '-v/--version: show version',
            '--version': '--version/-v: show version',
            '-h': '-h/--help: show help message',
            '--help': '--help/-h: show help message',
        }

    return None



# Helper functions for complex completions
# ============================================================================

def _get_current_token_text(tokens, cursor_token_idx):
    """Get text of current token or empty string."""
    if cursor_token_idx < len(tokens):
        return tokens[cursor_token_idx].text
    return ''


def _is_flag_context(tokens, cursor_token_idx, is_after):
    """Check if we're in a context where flag completion is appropriate."""
    if cursor_token_idx < len(tokens):
        current_token = tokens[cursor_token_idx].text
        # If current token starts with -, we're completing a flag
        if current_token.startswith('-'):
            return True
    # If we're after a space and nothing typed yet, don't force flag completion
    # Let it fall through to path completion
    return False


def _complete_paths(tokens, cursor_token_idx, is_after):
    """Return ALL path completions with shell-safe quoting"""
    import os
    import shlex

    # Determine directory - ignore prefix, return ALL items
    current = tokens[cursor_token_idx].text if cursor_token_idx < len(tokens) else ''
    dir_path = os.path.dirname(current) or '.' if '/' in current else '.'

    completions = {}
    try:
        for item in os.listdir(dir_path):
            full_path = os.path.join(dir_path, item) if dir_path != '.' else item
            desc = 'Folder' if os.path.isdir(full_path) else 'File'
            # Use shlex.quote for shell-safe names
            quoted_item = shlex.quote(item)
            completions[quoted_item] = desc
    except (OSError, PermissionError):
        pass

    return completions if completions else None


def _parse_manpage_flags(command):
    """
    Parse man page or --help output to extract flags automatically.

    This is a fallback for commands without explicit completion schemas.
    Returns dict of {flag: description} or None if parsing fails.

    Strategy:
    1. Try `man command` first (most detailed)
    2. Fall back to `command --help` or `command -h`
    3. Parse output with regex to find flags and descriptions
    4. Cache results for 1 hour to avoid repeated subprocess calls

    Examples of patterns we match:
    - "  -a, --all          show all files"
    - "  -v                 verbose output"
    - "  --recursive        process directories recursively"
    """
    # Check cache first
    cache_key = 'manpage_{0}'.format(command)
    ttl = 3600  # 1 hour

    with _CACHE_LOCK:
        if cache_key not in _CACHE_LOCKS:
            _CACHE_LOCKS[cache_key] = Lock()
        lock = _CACHE_LOCKS[cache_key]

    with lock:
        # Check cache
        if cache_key in _COMPLETION_CACHE:
            cached = _COMPLETION_CACHE[cache_key]
            if not cached.is_expired():
                return cached.result

        # Try man page first (use col -b to clean up formatting)
        help_text = None

        # Handle compound commands like "docker run" -> ["docker", "run"]
        cmd_parts = command.split()

        # Try man page for compound commands (e.g., "man docker-run")
        if len(cmd_parts) > 1:
            man_compound = '-'.join(cmd_parts)
            try:
                man_result = subprocess.run(
                    ['man', man_compound],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=2
                )
                if man_result.returncode == 0 and len(man_result.stdout) > 100:
                    help_text = man_result.stdout
            except:
                pass

        # Try regular man page
        if not help_text:
            try:
                man_result = subprocess.run(
                    ['man', cmd_parts[0]],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=2
                )
                if man_result.returncode == 0 and len(man_result.stdout) > 100:
                    # Clean man page formatting with col -b
                    try:
                        col_result = subprocess.run(
                            ['col', '-b'],
                            input=man_result.stdout,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            timeout=1
                        )
                        if col_result.returncode == 0:
                            help_text = col_result.stdout
                        else:
                            help_text = man_result.stdout
                    except:
                        help_text = man_result.stdout
            except:
                pass

        # Fall back to --help for compound commands (e.g., ["docker", "run", "--help"])
        if not help_text:
            for help_flag in ['--help', '-h', 'help']:
                try:
                    cmd_with_help = cmd_parts + [help_flag]
                    result = subprocess.run(
                        cmd_with_help,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        timeout=2
                    )
                    output = result.stdout + result.stderr
                    if len(output) > 50:
                        help_text = output
                        break
                except:
                    continue

        if not help_text:
            _COMPLETION_CACHE[cache_key] = CachedResult(None, ttl)
            return None

        flags = {}

        # Pattern for man pages: "     -a      description"
        # Man pages typically use 5+ spaces before the flag
        man_pattern = re.compile(
            r'^\s{5,}(-[a-zA-Z0-9@])\s+(.+?)$',
            re.MULTILINE
        )

        # Pattern for --help output: "  -a, --all   description" or "  -R, --repo [ARG]   description"
        # Handles optional argument placeholders like [HOST/]OWNER/REPO or FILE or KEY=VALUE
        help_pattern1 = re.compile(
            r'^\s{2,}((?:-[a-zA-Z0-9](?:,?\s+)?)?--?[a-zA-Z0-9][-a-zA-Z0-9]*)(?:\s+(?:\[[^\]]+\]|[A-Z_/=]+)+)?\s{2,}(.+?)$',
            re.MULTILINE
        )

        # Pattern for simple flags: "  --flag  description" or "-flag=ARG  description"
        # Also matches flags at start of line (0 or more spaces)
        help_pattern2 = re.compile(
            r'^\s*(--?[a-zA-Z0-9][-a-zA-Z0-9]*(?:=[A-Z_]+)?)\s{2,}(.+?)$',
            re.MULTILINE
        )

        # Usage line fallback: "[-a] [-v] [--verbose]" or "[-R] [--Repo]"
        usage_pattern = re.compile(r'\[(-[a-zA-Z0-9]|--[a-zA-Z0-9][-a-zA-Z0-9]*)\]')

        # Try all patterns
        for pattern in [man_pattern, help_pattern1, help_pattern2]:
            for match in pattern.finditer(help_text):
                flag_part = match.group(1).strip()
                desc = match.group(2).strip()

                # Clean up description (take first sentence, max 80 chars)
                desc = desc.split('.')[0].strip()
                if len(desc) > 80:
                    desc = desc[:77] + '...'

                # Parse out individual flags from "flag_part"
                # Could be "-a", "-a, --all", "--all", or "-flag=ARG"
                flag_matches = re.findall(r'--?[a-zA-Z0-9@][-a-zA-Z0-9]*(?:=[A-Z_]+)?', flag_part)

                if len(flag_matches) == 2:
                    # Both short and long form
                    short, long = flag_matches
                    flags[short] = "{0}/{1}: {2}".format(short, long, desc)
                    flags[long] = "{0}/{1}: {2}".format(long, short, desc)
                elif len(flag_matches) == 1:
                    # Single flag
                    flag = flag_matches[0]
                    flags[flag] = desc

        # If we got good results, cache and return them
        if flags:
            _COMPLETION_CACHE[cache_key] = CachedResult(flags, ttl)
            return flags

        # If man page had no parseable flags, try --help as fallback
        # (Some commands have man pages but --help is more structured)
        if not flags and help_text:
            # Check if we used man page (by checking if help_text came from man)
            # If so, try --help as well
            for help_flag in ['--help', '-h', 'help']:
                try:
                    result = subprocess.run(
                        [command, help_flag],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        timeout=2
                    )
                    output = result.stdout + result.stderr
                    if len(output) > 50:
                        # Try parsing --help output
                        for pattern in [man_pattern, help_pattern1, help_pattern2]:
                            for match in pattern.finditer(output):
                                try:
                                    flag_part = match.group(1).strip()
                                    desc = match.group(2).strip()
                                    desc = desc.split('.')[0].strip()
                                    if len(desc) > 80:
                                        desc = desc[:77] + '...'
                                    flag_matches = re.findall(r'--?[a-zA-Z0-9@][-a-zA-Z0-9]*(?:=[A-Z_]+)?', flag_part)
                                    if len(flag_matches) == 2:
                                        short, long = flag_matches
                                        flags[short] = "{0}/{1}: {2}".format(short, long, desc)
                                        flags[long] = "{0}/{1}: {2}".format(long, short, desc)
                                    elif len(flag_matches) == 1:
                                        flag = flag_matches[0]
                                        flags[flag] = desc
                                except Exception:
                                    continue
                        if flags:
                            break
                except Exception:
                    continue

        if flags:
            _COMPLETION_CACHE[cache_key] = CachedResult(flags, ttl)
            return flags

        # Fall back to usage pattern (just flag names from usage)
        # Only if we found nothing else
        usage_flags = set(usage_pattern.findall(help_text))
        if usage_flags:
            result = {flag: 'see man {0}'.format(command) for flag in usage_flags}
            _COMPLETION_CACHE[cache_key] = CachedResult(result, ttl)
            return result

        # Cache negative result too (avoid repeated parsing)
        _COMPLETION_CACHE[cache_key] = CachedResult(None, ttl)
        return None


def _parse_subcommands_from_help(command, help_text=None):
    """
    Parse subcommands from --help output automatically.

    This is a fallback for commands without explicit subcommand schemas.
    Returns dict of {subcommand: description} or None if parsing fails.

    Matches common formats:
    - "Commands:" followed by "  subcommand    description"
    - "CORE COMMANDS" followed by "  auth:    Authenticate..."
    - "Management Commands:" followed by "  builder    Manage builds"

    Args:
        command: Command name (e.g., 'claude')
        help_text: Pre-fetched help text (optional, will fetch if None)

    Returns:
        dict of {subcommand: description} or None
    """
    # Check cache first
    cache_key = 'subcommands_{0}'.format(command)
    ttl = 3600  # 1 hour

    with _CACHE_LOCK:
        if cache_key not in _CACHE_LOCKS:
            _CACHE_LOCKS[cache_key] = Lock()
        lock = _CACHE_LOCKS[cache_key]

    with lock:
        # Check cache
        if cache_key in _COMPLETION_CACHE:
            cached = _COMPLETION_CACHE[cache_key]
            if not cached.is_expired():
                return cached.result

        # Get help text if not provided
        if not help_text:
            try:
                # Handle compound commands like "docker network" -> ["docker", "network", "--help"]
                cmd_parts = command.split()
                cmd_parts.append('--help')
                result = subprocess.run(
                    cmd_parts,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=2
                )
                help_text = result.stdout + result.stderr
                if len(help_text) < 50:
                    _COMPLETION_CACHE[cache_key] = CachedResult(None, ttl)
                    return None
            except Exception:
                _COMPLETION_CACHE[cache_key] = CachedResult(None, ttl)
                return None

        subcommands = {}

        # Pattern 1: Standard "Commands:" section
        # Matches:  "  subcommand    description"
        #          "  auth:        Authenticate gh"
        #          "  buildx*      Docker Buildx"
        #          "  install [options] [target]    Install stuff"
        #          "  cryptdecode Cryptdecode..."  (only 1 space for long command names)
        # Captures command name, skips optional parameters in brackets/parens/angles, then captures description
        # Changed from \s{2,} to \s+ to handle commands with only 1 space before description
        standard_pattern = re.compile(
            r'^\s+([a-z][-a-z0-9]*[*:]?)(?:\s+\[[^\]]+\]|\s+\([^\)]+\)|\s+<[^>]+>)*\s+(.+?)$',
            re.MULTILINE
        )

        # Find "Commands:" or similar section headers (case-insensitive)
        section_markers = [
            'Commands:',
            'COMMANDS',
            'CORE COMMANDS',
            'Management Commands:',
            'Available Commands:',
            'Common Commands:',
        ]

        # Look for commands section
        for marker in section_markers:
            # Find section header (case-insensitive)
            marker_lower = marker.lower()
            text_lower = help_text.lower()

            marker_pos = text_lower.find(marker_lower)
            if marker_pos == -1:
                continue

            # Extract text after this section (until next section or 5000 chars)
            # Increased from 1000 to 5000 to handle commands like rclone with many subcommands
            section_start = marker_pos + len(marker)
            section_text = help_text[section_start:section_start + 5000]

            # Find where this section ends (next all-caps header or empty line pattern)
            next_section = re.search(r'\n[A-Z][A-Z\s]+:\s*\n', section_text)
            if next_section:
                section_text = section_text[:next_section.start()]

            # Parse subcommands from this section
            for match in standard_pattern.finditer(section_text):
                try:
                    subcommand = match.group(1).strip()
                    desc = match.group(2).strip()

                    # Clean up subcommand name (remove trailing : or *)
                    subcommand = subcommand.rstrip(':*')

                    # Skip if it looks like a flag (starts with -)
                    if subcommand.startswith('-'):
                        continue

                    # Skip if subcommand is the same as the program name
                    # This avoids false matches like "brew commands" being parsed as "brew" subcommand
                    if subcommand.lower() == command.lower():
                        continue

                    # Clean up description
                    desc = desc.split('\n')[0].strip()  # Take first line only
                    if len(desc) > 80:
                        desc = desc[:77] + '...'

                    subcommands[subcommand] = desc
                except Exception:
                    continue

            # If we found subcommands in this section, stop looking
            # But require at least 2 subcommands to avoid false positives
            # (e.g., "brew commands" and "man brew" shouldn't count as valid subcommands)
            if len(subcommands) >= 2:
                break

        # If Pattern 1 found fewer than 2 subcommands, it's likely a false positive
        # Clear it so other patterns can try
        if len(subcommands) < 2:
            subcommands = {}

        # Pattern 2: Comma-separated format (npm, yarn, etc.)
        # Example: "All commands:\n\n    access, adduser, audit, bugs, cache, ci, completion,\n    config, dedupe..."
        if not subcommands:
            comma_markers = ['All commands:', 'Available commands:', 'Commands:']
            for marker in comma_markers:
                marker_lower = marker.lower()
                text_lower = help_text.lower()
                marker_pos = text_lower.find(marker_lower)
                if marker_pos == -1:
                    continue

                # Extract text after marker (until next section or 500 chars)
                section_start = marker_pos + len(marker)
                section_text = help_text[section_start:section_start + 500]

                # Stop at next section header (all caps line or double newline)
                next_section = re.search(r'\n\n[A-Z]', section_text)
                if next_section:
                    section_text = section_text[:next_section.start()]

                # Extract comma-separated command names
                # Remove leading/trailing whitespace and split by comma
                commands_text = re.sub(r'\s+', ' ', section_text).strip()
                if ',' in commands_text:
                    for cmd in commands_text.split(','):
                        cmd = cmd.strip()
                        # Only keep valid command names (letters, hyphens, underscores)
                        if re.match(r'^[a-z][a-z0-9_-]*$', cmd):
                            subcommands[cmd] = ''  # No descriptions in comma format

                if subcommands:
                    break

        # Pattern 3: "program command" format (brew, git, etc.)
        # Example: "brew search TEXT\n  brew info [FORMULA]...\n  brew install FORMULA..."
        # Looks for lines starting with the program name followed by a command
        if not subcommands:
            # Only use this pattern if we see multiple "program subcommand" lines
            # This avoids false positives from "man program" or "program --help"
            program_pattern = re.compile(
                r'^\s*{}\s+([a-z][a-z0-9_-]+)'.format(re.escape(command)),
                re.MULTILINE | re.IGNORECASE
            )

            candidates = {}
            for match in program_pattern.finditer(help_text):
                try:
                    subcommand = match.group(1).strip().lower()

                    # Skip if it looks like a flag
                    if subcommand.startswith('-'):
                        continue

                    # Skip common non-subcommands (but keep "help" as it's a valid subcommand for many programs)
                    if subcommand in {'option', 'options', 'command', 'usage', 'version'}:
                        continue

                    # Skip if the subcommand is the same as the program name (avoids "man brew" matching "brew")
                    if subcommand == command.lower():
                        continue

                    candidates[subcommand] = ''  # No descriptions available in this format
                except Exception:
                    continue

            # Only use this pattern if we found at least 3 subcommands
            # This reduces false positives
            if len(candidates) >= 3:
                subcommands = candidates

        # Cache and return
        if subcommands:
            _COMPLETION_CACHE[cache_key] = CachedResult(subcommands, ttl)
            return subcommands

        # Cache negative result
        _COMPLETION_CACHE[cache_key] = CachedResult(None, ttl)
        return None


def _parse_json_file(filepath, keys_path):
    """Parse JSON file and extract nested keys. Returns list or empty list on error."""
    try:
        import json
        with open(filepath, 'r') as f:
            data = json.load(f)
        for key in keys_path:
            data = data.get(key, {})
        return list(data.keys()) if isinstance(data, dict) else []
    except Exception:
        return []


def _parse_makefile_targets():
    """Extract target names from Makefile in current directory."""
    try:
        import re
        with open('Makefile', 'r') as f:
            targets = []
            for line in f:
                # Match target definitions: 'target:' at start of line
                match = re.match(r'^([a-zA-Z0-9_-]+):', line)
                if match and not match.group(1).startswith('.'):
                    targets.append(match.group(1))
            return targets
    except Exception:
        return []


def _parse_ssh_config_hosts():
    """Extract host names from ~/.ssh/config."""
    try:
        import re
        config_path = os.path.expanduser('~/.ssh/config')
        hosts = []
        with open(config_path, 'r') as f:
            for line in f:
                # Match 'Host hostname' lines
                match = re.match(r'^\s*Host\s+([^\s*]+)', line, re.IGNORECASE)
                if match and '*' not in match.group(1):
                    hosts.append(match.group(1))
        return hosts
    except Exception:
        return []


@cached_completion('systemctl_services', ttl=300)
def _get_systemctl_services():
    """Get list of systemd services (cached for 5 minutes)."""
    try:
        output = subprocess.check_output(
            ['systemctl', 'list-units', '--type=service', '--all', '--no-pager', '--no-legend'],
            stderr=subprocess.PIPE,
            timeout=3
        )
        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='ignore')

        services = []
        for line in output.split('\n'):
            parts = line.strip().split()
            if parts:
                # Service name is first column, may have .service suffix
                service = parts[0]
                if service.endswith('.service'):
                    service = service[:-8]
                services.append(service)
        return services
    except Exception:
        return []


@cached_completion('brew_formulae', ttl=3600)
def _get_brew_formulae():
    """Get list of brew formulae (cached for 1 hour)."""
    try:
        output = subprocess.check_output(
            ['brew', 'formulae'],
            stderr=subprocess.PIPE,
            timeout=5
        )
        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='ignore')
        return [f.strip() for f in output.split('\n') if f.strip()]
    except Exception:
        return []


@cached_completion('kubectl_resources', ttl=60)
def _get_kubectl_resources():
    """Get list of kubernetes resource types (cached for 1 minute)."""
    return ['pods', 'services', 'deployments', 'replicasets', 'statefulsets',
            'daemonsets', 'jobs', 'cronjobs', 'configmaps', 'secrets',
            'nodes', 'namespaces', 'ingresses', 'persistentvolumes',
            'persistentvolumeclaims', 'serviceaccounts']


# ============================================================================
# Helper functions for refactoring completion patterns
# ============================================================================

def _combine_flags(common, specific):
    """
    Combine common flags with subcommand-specific flags.

    Args:
        common: List or dict of common flags available for all subcommands
        specific: List or dict of flags specific to a subcommand

    Returns:
        Combined list or dict of flags

    Example:
        >>> common = ['--help', '--version']
        >>> specific = ['--force', '--verbose']
        >>> _combine_flags(common, specific)
        ['--help', '--version', '--force', '--verbose']
        >>> common = {'--help': 'show help', '--version': 'show version'}
        >>> specific = {'--force': 'force operation', '--verbose': 'verbose output'}
        >>> _combine_flags(common, specific)
        {'--help': 'show help', '--version': 'show version', '--force': 'force operation', '--verbose': 'verbose output'}
    """
    if isinstance(common, dict) and isinstance(specific, dict):
        return {**common, **specific}
    return common + specific


def _get_subcommand_flags(subcommand, flag_mapping, common_flags=None):
    """
    Get flags for a subcommand from a mapping dictionary.

    Args:
        subcommand: The subcommand name
        flag_mapping: Dict mapping subcommand names to their specific flags
        common_flags: Optional list of common flags to prepend (default: ['--help'])

    Returns:
        List of flags for the subcommand, or common flags if not in mapping

    Example:
        >>> mapping = {'install': ['--force', '--yes'], 'remove': ['--force']}
        >>> _get_subcommand_flags('install', mapping, ['--help'])
        ['--help', '--force', '--yes']
        >>> _get_subcommand_flags('unknown', mapping, ['--help'])
        ['--help']
    """
    if common_flags is None:
        common_flags = {
            '--help': 'show help message',
        }

    if subcommand in flag_mapping:
        return _combine_flags(common_flags, flag_mapping[subcommand])
    return common_flags


def _complete_at_position_zero(cursor_token_idx, is_after, items):
    """
    Standard position 0 completion for commands.

    Returns items if cursor is at position 0 and after the command,
    OR if cursor is at position 1 (in the subcommand being typed).

    Args:
        cursor_token_idx: Current cursor token index
        is_after: Whether cursor is after the token
        items: List of completion items to return

    Returns:
        items if at position 0 and after, or position 1 (not after), None otherwise

    Example:
        >>> _complete_at_position_zero(0, True, ['install', 'remove'])
        ['install', 'remove']
        >>> _complete_at_position_zero(1, False, ['install', 'remove'])
        ['install', 'remove']
        >>> _complete_at_position_zero(2, False, ['install', 'remove'])
        None
    """
    # Cursor after command name: "mamba |"
    if cursor_token_idx == 0 and is_after:
        return items
    # Cursor in the middle of typing subcommand: "mamba a|"
    if cursor_token_idx == 1 and not is_after:
        return items
    return None


def _complete_subcommand_at_position(cursor_token_idx, is_after, position, items):
    """
    Complete subcommands at a specific position.

    Args:
        cursor_token_idx: Current cursor token index
        is_after: Whether cursor is after the token
        position: The position to complete at (typically 1 for subcommands)
        items: List of completion items to return

    Returns:
        items if at specified position and after, None otherwise

    Example:
        >>> _complete_subcommand_at_position(1, True, 1, ['create', 'delete'])
        ['create', 'delete']
        >>> _complete_subcommand_at_position(1, False, 1, ['create', 'delete'])

        >>> _complete_subcommand_at_position(2, True, 1, ['create', 'delete'])

    """
    if cursor_token_idx == position and is_after:
        return items
    return None


# ============================================================================
# Additional completion schemas
# ============================================================================

@register_completion_schema('npm')
def _npm_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for npm commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        if subcommand == 'install':
            return {
                '--save-prod': '--save-prod/-P: save to dependencies (default)',
                '-P': '-P/--save-prod: save to dependencies (default)',
                '--save-dev': '--save-dev/-D: save to devDependencies',
                '-D': '-D/--save-dev: save to devDependencies',
                '--save-optional': '--save-optional/-O: save to optionalDependencies',
                '-O': '-O/--save-optional: save to optionalDependencies',
                '--save-exact': '--save-exact/-E: save exact version',
                '-E': '-E/--save-exact: save exact version',
                '--save': '--save/-S: save to dependencies (deprecated)',
                '-S': '-S/--save: save to dependencies (deprecated)',
                '--no-save': 'do not save to package.json',
                '--save-bundle': '--save-bundle/-B: save to bundleDependencies',
                '-B': '-B/--save-bundle: save to bundleDependencies',
                '--global': '--global/-g: install globally',
                '-g': '-g/--global: install globally',
                '--global-style': 'use global install layout',
                '--force': '--force/-f: force fetch remote resources',
                '-f': '-f/--force: force fetch remote resources',
                '--legacy-bundling': 'use legacy bundling algorithm',
                '--ignore-scripts': 'do not run package scripts',
                '--no-audit': 'skip security audit',
                '--no-bin-links': 'prevent symlinking bin files',
                '--no-optional': 'do not install optional dependencies',
                '--no-shrinkwrap': 'ignore npm-shrinkwrap.json',
                '--production': 'do not install devDependencies',
                '--dry-run': 'simulate install without changes',
                '--prefer-offline': 'prefer offline cache',
                '--prefer-online': 'prefer online registry',
                '--registry': 'specify registry URL',
                '--tag': 'install by tag (latest, next, etc.)',
                '--help': 'show help information'
            }
        elif subcommand == 'run':
            return {
                '--silent': '--silent/-s: suppress output',
                '-s': '-s/--silent: suppress output',
                '--help': 'show help information'
            }
        elif subcommand in ('test', 'start', 'build'):
            return {
                '--silent': '--silent/-s: suppress output',
                '-s': '-s/--silent: suppress output',
                '--production': 'run in production mode',
                '--help': 'show help information'
            }
        elif subcommand == 'audit':
            return {
                '--audit-level': 'minimum severity level (info, low, moderate, high, critical)',
                '--dry-run': 'simulate audit without changes',
                '--json': 'output in JSON format',
                '--production': 'only audit production dependencies',
                '--help': 'show help information'
            }
        elif subcommand == 'publish':
            return {
                '--access': 'package access level (public, restricted)',
                '--tag': 'tag to publish under (default: latest)',
                '--dry-run': 'simulate publish without changes',
                '--otp': 'one-time password for 2FA',
                '--help': 'show help information'
            }
        else:
            return ['--help', '--version']

    if cursor_token_idx == 0 and is_after:
        return {
            'install': 'Install a package and dependencies',
            'ci': 'Install dependencies from package-lock.json (clean install)',
            'run': 'Run a script defined in package.json',
            'test': 'Run tests defined in package.json',
            'start': 'Start the application',
            'build': 'Build the project',
            'init': 'Initialize a new package.json',
            'uninstall': 'Remove a package',
            'update': 'Update packages to latest versions',
            'upgrade': 'Alias for npm update',
            'publish': 'Publish a package to the registry',
            'link': 'Symlink a package folder',
            'unlink': 'Unlink a symlinked package',
            'audit': 'Run security audit on dependencies',
            'outdated': 'Check for outdated packages',
            'ls': 'List installed packages',
            'list': 'Alias for npm ls',
            'exec': 'Execute a command from a local or remote package',
            'access': 'Set access level on published packages',
            'adduser': 'Add a registry user account',
            'bin': 'Display npm bin folder',
            'bugs': 'Open package bugs tracker in browser',
            'cache': 'Manage npm cache',
            'completion': 'Tab completion for npm',
            'config': 'Manage npm configuration',
            'dedupe': 'Reduce duplication in dependency tree',
            'deprecate': 'Deprecate a version of a package',
            'diff': 'Show diff between package versions',
            'dist-tag': 'Modify package distribution tags',
            'docs': 'Open package documentation in browser',
            'doctor': 'Check npm environment for issues',
            'edit': 'Edit an installed package',
            'explore': 'Browse an installed package',
            'fund': 'Retrieve funding information',
            'get': 'Get a configuration value',
            'help': 'Get help on npm',
            'help-search': 'Search npm help documentation',
            'hook': 'Manage registry hooks',
            'install-ci-test': 'Install with ci and run tests',
            'install-test': 'Install and run tests',
            'logout': 'Log out of the registry',
            'owner': 'Manage package owners',
            'pack': 'Create a tarball from a package',
            'ping': 'Ping npm registry',
            'prefix': 'Display npm prefix',
            'profile': 'Manage registry profile',
            'prune': 'Remove extraneous packages',
            'query': 'Retrieve packages matching a query',
            'rebuild': 'Rebuild a package',
            'repo': 'Open package repository in browser',
            'restart': 'Restart a package',
            'root': 'Display npm root',
            'search': 'Search for packages',
            'set': 'Set a configuration value',
            'set-script': 'Set a script in package.json',
            'shrinkwrap': 'Lock down dependency versions',
            'star': 'Mark a package as a favorite',
            'stars': 'View packages marked as favorites',
            'stop': 'Stop a package',
            'team': 'Manage organization teams',
            'token': 'Manage authentication tokens',
            'unstar': 'Remove a package from favorites',
            'version': 'Bump package version',
            'view': 'View registry info about a package',
            'whoami': 'Display npm username'
        }

    elif cursor_token_idx == 1:
        subcommand = tokens[1].text if len(tokens) > 1 else ''
        if subcommand == 'run':
            return _parse_json_file('package.json', ['scripts'])
        elif subcommand == 'cache':
            return {
                'clean': 'Delete all data from cache folder',
                'verify': 'Verify cache contents',
                'ls': 'List cache contents'
            }

    return None


@register_completion_schema('yarn')
def _yarn_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for yarn commands (Yarn 1.x/Classic and Yarn 2+/Berry)."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        if subcommand == 'add':
            return {
                '--dev': '--dev/-D: add package to devDependencies',
                '-D': '-D/--dev: add package to devDependencies',
                '--peer': '--peer/-P: add package to peerDependencies',
                '-P': '-P/--peer: add package to peerDependencies',
                '--optional': '--optional/-O: add package to optionalDependencies',
                '-O': '-O/--optional: add package to optionalDependencies',
                '--exact': '--exact/-E: install exact version',
                '-E': '-E/--exact: install exact version',
                '--tilde': '--tilde: use tilde range (~) for version',
                '--ignore-workspace-root-check': '--ignore-workspace-root-check: bypass workspace root check',
                '--help': '--help: show help information',
            }
        elif subcommand in ('install', 'upgrade'):
            return {
                '--frozen-lockfile': '--frozen-lockfile: do not generate lockfile and fail if update is needed',
                '--production': '--production: install only production dependencies',
                '--pure-lockfile': '--pure-lockfile: do not generate lockfile',
                '--check-files': '--check-files: verify file tree of packages',
                '--force': '--force: refetch all packages',
                '--ignore-scripts': '--ignore-scripts: do not run lifecycle scripts',
                '--offline': '--offline: use offline mirror instead of network',
                '--help': '--help: show help information',
            }
        elif subcommand == 'run':
            return {
                '--silent': '--silent: skip output from script',
                '--help': '--help: show help information',
            }
        elif subcommand == 'up':
            return {
                '--interactive': '--interactive/-i: update dependencies interactively',
                '-i': '-i/--interactive: update dependencies interactively',
                '--exact': '--exact/-E: use exact version',
                '-E': '-E/--exact: use exact version',
                '--tilde': '--tilde/-T: use tilde range (~)',
                '-T': '-T/--tilde: use tilde range (~)',
                '--caret': '--caret/-C: use caret range (^)',
                '-C': '-C/--caret: use caret range (^)',
                '--help': '--help: show help information',
            }
        else:
            return {
                '--help': '--help: show help information',
                '--version': '--version: show version number',
            }

    if cursor_token_idx == 0 and is_after:
        return {
            'add': 'Add package to dependencies',
            'remove': 'Remove package from dependencies',
            'install': 'Install all dependencies',
            'run': 'Run script defined in package.json',
            'test': 'Run test script',
            'build': 'Run build script',
            'init': 'Initialize new package',
            'upgrade': 'Upgrade packages to latest versions',
            'up': 'Update dependencies interactively',
            'link': 'Link local package',
            'unlink': 'Unlink local package',
            'audit': 'Check for security vulnerabilities',
            'cache': 'Manage yarn cache',
            'why': 'Show why package is installed',
            'workspace': 'Run command in workspace',
            'workspaces': 'Manage multiple workspaces',
            'dlx': 'Execute package without installing',
            'exec': 'Execute shell command',
            'node': 'Run node with yarn environment',
            'plugin': 'Manage yarn plugins',
            'set': 'Change configuration',
            'config': 'Manage configuration',
            'info': 'Show package information',
            'list': 'List installed packages',
            'outdated': 'Show outdated packages',
            'owner': 'Manage package owners',
            'pack': 'Create tarball from package',
            'publish': 'Publish package to registry',
            'tag': 'Manage package tags',
            'team': 'Manage organization teams',
            'version': 'Bump package version',
            'versions': 'Show package version info',
            'bin': 'Show location of yarn bin folder',
            'check': 'Verify package integrity',
            'global': 'Manage global packages',
            'help': 'Show help information',
            'import': 'Import dependencies from package-lock.json',
            'licenses': 'List licenses of installed packages',
            'login': 'Store registry credentials',
            'logout': 'Clear registry credentials',
            'policies': 'Define project policies'
        }

    elif cursor_token_idx == 1:
        subcommand = tokens[1].text if len(tokens) > 1 else ''
        if subcommand == 'run':
            return _parse_json_file('package.json', ['scripts'])
        elif subcommand == 'cache':
            return {
                'clean': 'Clear cache files',
                'dir': 'Show cache directory path',
                'list': 'List cached packages'
            }
        elif subcommand == 'workspaces':
            return {
                'info': 'Show workspace information',
                'run': 'Run script in all workspaces',
                'list': 'List all workspaces',
                'foreach': 'Run command in each workspace'
            }
        elif subcommand == 'plugin':
            return {
                'import': 'Import plugin',
                'remove': 'Remove plugin',
                'runtime': 'List runtime plugins',
                'list': 'List installed plugins'
            }

    return None


@register_completion_schema('make')
def _make_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for make commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-j': '-j/--jobs: specify number of jobs to run simultaneously',
            '--jobs': '--jobs/-j: specify number of jobs to run simultaneously',
            '-B': '-B/--always-make: unconditionally make all targets',
            '--always-make': '--always-make/-B: unconditionally make all targets',
            '-n': '-n/--dry-run: print commands without executing them',
            '--dry-run': '--dry-run/-n: print commands without executing them',
            '-s': '-s/--silent: do not echo commands',
            '--silent': '--silent/-s: do not echo commands',
            '-k': '-k/--keep-going: continue after errors',
            '--keep-going': '--keep-going/-k: continue after errors',
            '-C': '-C/--directory: change to directory before reading makefiles',
            '--directory': '--directory/-C: change to directory before reading makefiles',
        }

    result = _complete_at_position_zero(cursor_token_idx, is_after, _parse_makefile_targets())
    if result:
        return result
    return None




@register_completion_schema('ssh')
def _ssh_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ssh commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-p': '-p: specify port number',
            '-i': '-i: identity file (private key)',
            '-L': '-L: local port forwarding',
            '-R': '-R: remote port forwarding',
            '-D': '-D: dynamic port forwarding (SOCKS proxy)',
            '-A': '-A: enable agent forwarding',
            '-X': '-X: enable X11 forwarding',
            '-Y': '-Y: enable trusted X11 forwarding',
            '-v': '-v: verbose mode',
            '-o': '-o: specify option',
            '-F': '-F: specify config file',
            '-l': '-l: login name',
            '-N': '-N: don\'t execute remote command',
            '-f': '-f: go to background',
            '-q': '-q: quiet mode',
            '-C': '-C: enable compression',
            '-4': '-4: force IPv4',
            '-6': '-6: force IPv6',
        }

    if cursor_token_idx == 0 and is_after:
        return _parse_ssh_config_hosts()
    return None



@register_completion_schema('docker-compose')
def _docker_compose_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for docker-compose commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''
        common_flags = {
            '--help': 'show help message',
            '--file': 'compose file path',
            '-f': '-f/--file: compose file path',
            '--project-name': 'project name',
            '-p': '-p/--project-name: project name',
        }

        flag_mapping = {
            'up': ['--detach', '-d', '--build', '--force-recreate', '--no-deps',
                   '--remove-orphans', '--abort-on-container-exit', '--scale'],
            'down': ['--volumes', '-v', '--remove-orphans', '--rmi', '--timeout', '-t'],
            'logs': ['--follow', '-f', '--tail', '--timestamps', '-t', '--no-color'],
            'exec': ['--detach', '-d', '--user', '-u', '--workdir', '-w', '--env', '-e'],
            'build': ['--no-cache', '--pull', '--parallel', '--compress'],
        }

        return _get_subcommand_flags(subcommand, flag_mapping, common_flags)

    result = _complete_at_position_zero(cursor_token_idx, is_after, {
        'up': 'create and start containers',
        'down': 'stop and remove containers',
        'start': 'start existing containers',
        'stop': 'stop running containers',
        'restart': 'restart containers',
        'build': 'build or rebuild services',
        'pull': 'pull service images',
        'push': 'push service images',
        'ps': 'list containers',
        'logs': 'view output from containers',
        'exec': 'execute command in running container',
        'run': 'run a one-off command',
        'config': 'validate and view compose file',
        'kill': 'kill containers',
        'rm': 'remove stopped containers',
        'create': 'create containers without starting',
        'pause': 'pause services',
        'unpause': 'unpause services',
        'top': 'display running processes',
        'events': 'receive real time events',
        'port': 'print public port for port binding',
    })
    if result:
        return result
    return None


@register_completion_schema('systemctl')
def _systemctl_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for systemctl commands with comprehensive flag/subcommand support."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--all': '--all/-a: show all units/properties',
            '-a': '-a/--all: show all units/properties',
            '--user': '--user: connect to user service manager',
            '--system': '--system: connect to system service manager',
            '--failed': '--failed: show only failed units',
            '--no-pager': '--no-pager: do not pipe output into pager',
            '--no-legend': '--no-legend: do not print legend',
            '--full': '--full: do not ellipsize output',
            '--quiet': '--quiet/-q: suppress output',
            '-q': '-q/--quiet: suppress output',
            '--no-reload': '--no-reload: do not reload unit after enabling',
            '--type': '--type/-t: list units of particular type',
            '-t': '-t/--type: list units of particular type',
            '--state': '--state: list units in particular state',
            '--property': '--property/-p: show only specified property',
            '-p': '-p/--property: show only specified property',
            '--value': '--value: show only values when showing properties',
            '--preset-mode': '--preset-mode: apply preset mode (full/enable-only/disable-only)',
            '--root': '--root: operate on alternative root path',
            '--runtime': '--runtime: make changes only temporarily',
            '--machine': '--machine/-M: operate on local container',
            '-M': '-M/--machine: operate on local container',
            '--lines': '--lines/-n: number of journal lines to show',
            '-n': '-n/--lines: number of journal lines to show',
            '--output': '--output/-o: change journal output mode',
            '-o': '-o/--output: change journal output mode',
            '--firmware-setup': '--firmware-setup: reboot into firmware setup',
            '--boot-loader-menu': '--boot-loader-menu: reboot into boot loader menu',
            '--boot-loader-entry': '--boot-loader-entry: reboot into specific boot loader entry',
            '--plain': '--plain: use plain output format',
            '--timestamp': '--timestamp: change timestamp display',
            '--mkdir': '--mkdir: create parent directories',
            '--marked': '--marked: show marked units',
            '--read-only': '--read-only: create read-only bind mount',
            '--now': '--now: start/stop unit after enabling/disabling',
            '--what': '--what: select mount points to operate on',
            '--show-types': '--show-types: show socket types',
            '--job-mode': '--job-mode: specify job mode (fail/replace/isolate)',
            '--kill-who': '--kill-who: select process to send signal to',
            '--signal': '--signal/-s: signal to send',
            '-s': '-s/--signal: signal to send',
            '-H': '-H/--host: operate on remote host',
            '--host': '--host/-H: operate on remote host',
            '--reverse': '--reverse/-r: show reverse dependencies',
            '-r': '-r/--reverse: show reverse dependencies',
            '--after': '--after: show units ordered after',
            '--before': '--before: show units ordered before',
            '--help': '--help/-h: print help information',
            '-h': '-h/--help: print help information',
            '--version': '--version: print version information',
            '--no-wall': '--no-wall: do not send wall message',
            '--no-block': '--no-block: do not wait until operation finishes',
            '--no-ask-password': '--no-ask-password: do not ask for passwords',
            '--force': '--force/-f: override safety checks',
            '-f': '-f/--force: override safety checks',
            '--ignore-inhibitors': '--ignore-inhibitors/-i: ignore inhibitor locks',
            '-i': '-i/--ignore-inhibitors: ignore inhibitor locks',
            '--dry-run': '--dry-run: only print what would be done',
            '--verbose': '--verbose/-v: print verbose output',
            '-v': '-v/--verbose: print verbose output',
            '-l': '-l: do not ellipsize output (deprecated, use --full)',
        }

    result = _complete_at_position_zero(cursor_token_idx, is_after,
                                        {
                                            'start': 'Start unit',
                                            'stop': 'Stop unit',
                                            'restart': 'Restart unit',
                                            'reload': 'Reload unit configuration',
                                            'status': 'Show unit status',
                                            'enable': 'Enable unit at boot',
                                            'disable': 'Disable unit at boot',
                                            'is-active': 'Check if unit is active',
                                            'is-enabled': 'Check if unit is enabled',
                                            'list-units': 'List loaded units',
                                            'daemon-reload': 'Reload systemd configuration',
                                            'reset-failed': 'Reset failed state for units',
                                            'mask': 'Mask unit',
                                            'unmask': 'Unmask unit',
                                            'cat': 'Show unit file contents',
                                            'edit': 'Edit unit file',
                                            'show': 'Show unit properties',
                                            'list-dependencies': 'Show unit dependencies',
                                            'list-jobs': 'List active jobs',
                                            'list-timers': 'List timers',
                                            'list-sockets': 'List sockets',
                                            'get-default': 'Get default target',
                                            'set-default': 'Set default target',
                                            'isolate': 'Start unit and stop all others',
                                            'switch-root': 'Switch to different root filesystem',
                                            'add-wants': 'Add Wants dependency',
                                            'add-requires': 'Add Requires dependency',
                                            'preset': 'Enable/disable unit per preset',
                                            'preset-all': 'Enable/disable all units per preset',
                                            'revert': 'Revert unit file to vendor version',
                                            'link': 'Link unit file',
                                            'is-system-running': 'Check system state',
                                            'default': 'Enter default mode',
                                            'rescue': 'Enter rescue mode',
                                            'emergency': 'Enter emergency mode',
                                            'halt': 'Halt the system',
                                            'poweroff': 'Power off the system',
                                            'reboot': 'Reboot the system',
                                            'kexec': 'Reboot via kexec',
                                            'exit': 'Exit user service manager',
                                            'suspend': 'Suspend the system',
                                            'hibernate': 'Hibernate the system',
                                            'hybrid-sleep': 'Hybrid sleep the system',
                                            'suspend-then-hibernate': 'Suspend then hibernate',
                                            'list-unit-files': 'List unit files',
                                            'is-failed': 'Check if unit failed',
                                            'kill': 'Send signal to processes',
                                            'try-restart': 'Restart if active',
                                            'reload-or-restart': 'Reload or restart unit',
                                            'try-reload-or-restart': 'Try reload or restart',
                                            'condrestart': 'Conditionally restart unit',
                                            'force-reload': 'Force reload unit',
                                            'list-machines': 'List running VMs/containers',
                                            'cancel': 'Cancel pending job',
                                            'snapshot': 'Create snapshot',
                                            'delete': 'Delete snapshot',
                                            'show-environment': 'Show environment variables',
                                            'set-environment': 'Set environment variable',
                                            'unset-environment': 'Unset environment variable',
                                            'import-environment': 'Import environment variables',
                                            'daemon-reexec': 'Reexecute systemd',
                                            'set-property': 'Set unit property'
                                        })
    if result:
        return result

    if cursor_token_idx >= 1:
        subcommand = tokens[1].text if len(tokens) > 1 else ''
        if subcommand in ('start', 'stop', 'restart', 'reload', 'status', 'enable',
                         'disable', 'mask', 'unmask', 'cat', 'edit', 'show',
                         'is-active', 'is-enabled', 'is-failed', 'kill', 'try-restart',
                         'reload-or-restart', 'try-reload-or-restart', 'set-property',
                         'list-dependencies'):
            result = _complete_subcommand_at_position(cursor_token_idx, is_after, 1, _get_systemctl_services())
            if result:
                return result

    return None




@register_completion_schema('journalctl')
def _journalctl_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for journalctl commands with comprehensive flag support."""
    # Check if we're completing a flag value (cursor is after a flag that takes an argument)
    # When is_after is True, the cursor is after the token at cursor_token_idx
    # When is_after is False, the cursor is within the token at cursor_token_idx
    if is_after and cursor_token_idx < len(tokens):
        prev_token = tokens[cursor_token_idx].text

        # Output format values
        if prev_token in ('-o', '--output'):
            return ['short', 'short-full', 'short-iso', 'short-iso-precise',
                    'short-precise', 'short-monotonic', 'short-unix', 'verbose',
                    'export', 'json', 'json-pretty', 'json-sse', 'json-seq',
                    'cat', 'with-unit']

        # Priority values
        if prev_token in ('-p', '--priority'):
            return ['emerg', 'alert', 'crit', 'err', 'warning', 'notice',
                    'info', 'debug', '0', '1', '2', '3', '4', '5', '6', '7']

    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--unit': '--unit/-u: show logs for specified systemd unit',
            '-u': '-u/--unit: show logs for specified systemd unit',
            '--boot': '--boot/-b: show logs from specific boot',
            '-b': '-b/--boot: show logs from specific boot',
            '--follow': '--follow/-f: follow journal in real-time',
            '-f': '-f/--follow: follow journal in real-time',
            '--lines': '--lines/-n: number of journal entries to show',
            '-n': '-n/--lines: number of journal entries to show',
            '--reverse': '--reverse/-r: show newest entries first',
            '-r': '-r/--reverse: show newest entries first',
            '--output': '--output/-o: change journal output mode',
            '-o': '-o/--output: change journal output mode',
            '--priority': '--priority/-p: filter output by message priorities',
            '-p': '-p/--priority: filter output by message priorities',
            '--grep': '--grep/-g: filter output to entries with MESSAGE matching regex',
            '-g': '-g/--grep: filter output to entries with MESSAGE matching regex',
            '--since': '--since/-S: show entries since specified date',
            '-S': '-S/--since: show entries since specified date',
            '--until': '--until/-U: show entries until specified date',
            '-U': '-U/--until: show entries until specified date',
            '--identifier': '--identifier/-t: show entries with specified syslog identifier',
            '-t': '-t/--identifier: show entries with specified syslog identifier',
            '--dmesg': '--dmesg/-k: show kernel messages only',
            '-k': '-k/--dmesg: show kernel messages only',
            '--system': '--system: show system service logs',
            '--user': '--user: show user service logs',
            '--list-boots': '--list-boots: show list of boot sessions',
            '--disk-usage': '--disk-usage: show disk usage of all journal files',
            '--vacuum-size': '--vacuum-size: reduce journal size below specified size',
            '--vacuum-time': '--vacuum-time: remove journal files older than specified time',
            '--vacuum-files': '--vacuum-files: leave only specified number of journal files',
            '--flush': '--flush: flush all journal data to disk',
            '--rotate': '--rotate: rotate journal files',
            '--verify': '--verify: verify journal file consistency',
            '--sync': '--sync: synchronize unwritten journal messages to disk',
            '--directory': '--directory/-D: specify journal directory',
            '-D': '-D/--directory: specify journal directory',
            '--file': '--file: show entries from specified journal file',
            '--root': '--root: operate on catalog hierarchy under specified directory',
            '--namespace': '--namespace: show journal from specified namespace',
            '--no-tail': '--no-tail: show all lines',
            '--no-pager': '--no-pager: do not pipe output into a pager',
            '--pager-end': '--pager-end/-e: jump to end in pager',
            '-e': '-e/--pager-end: jump to end in pager',
            '--catalog': '--catalog/-x: augment log lines with explanation texts',
            '-x': '-x/--catalog: augment log lines with explanation texts',
            '--quiet': '--quiet/-q: suppress info messages',
            '-q': '-q/--quiet: suppress info messages',
            '--merge': '--merge/-m: show entries from all available journals',
            '-m': '-m/--merge: show entries from all available journals',
            '--cursor': '--cursor: show entries starting at specified cursor',
            '--after-cursor': '--after-cursor: show entries after specified cursor',
            '--show-cursor': '--show-cursor: print cursor after last entry',
            '--cursor-file': '--cursor-file: show entries after cursor stored in file',
            '--no-full': '--no-full: ellipsize fields',
            '--all': '--all/-a: show all fields in full',
            '-a': '-a/--all: show all fields in full',
            '--field': '--field/-F: print all possible data values',
            '-F': '-F/--field: print all possible data values',
            '--case-sensitive': '--case-sensitive: use case sensitive pattern matching',
            '--utc': '--utc: express time in UTC',
            '--no-hostname': '--no-hostname: suppress output of hostname field',
            '--machine': '--machine/-M: show entries from specified machine',
            '-M': '-M/--machine: show entries from specified machine',
            '--help': '--help/-h: show help message',
            '-h': '-h/--help: show help message',
            '--version': '--version: show version information',
            '--facility': '--facility: filter by syslog facility',
        }

    # journalctl doesn't have subcommands at position 0
    return None


@register_completion_schema('ffmpeg')
def _ffmpeg_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ffmpeg commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        current_token = _get_current_token_text(tokens, cursor_token_idx)

        # Check if previous token is a flag that expects specific values
        if cursor_token_idx > 0:
            prev_token = tokens[cursor_token_idx - 1].text

            # Preset options for -preset flag
            if prev_token == '-preset':
                return ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast',
                        'medium', 'slow', 'slower', 'veryslow']

            # Video codec options for -c:v or -vcodec
            if prev_token in ('-c:v', '-vcodec'):
                return ['libx264', 'libx265', 'libvpx-vp9', 'h264', 'hevc',
                        'vp9', 'av1', 'mpeg4', 'copy']

            # Audio codec options for -c:a or -acodec
            if prev_token in ('-c:a', '-acodec'):
                return ['aac', 'libmp3lame', 'libopus', 'libvorbis', 'flac',
                        'pcm_s16le', 'ac3', 'copy']

            # Pixel format options for -pix_fmt
            if prev_token == '-pix_fmt':
                return ['yuv420p', 'yuv422p', 'yuv444p', 'rgb24', 'rgba',
                        'gray', 'nv12', 'nv21']

        # Return all available flags when in flag context
        return {
            '-i': 'input file',
            '-f': 'force format',
            '-ss': 'start time offset',
            '-t': 'duration to process',
            '-to': 'stop time',
            '-c:v': 'video codec',
            '-vcodec': 'video codec (alias)',
            '-b:v': 'video bitrate',
            '-r': 'frame rate',
            '-s': 'frame size (WxH)',
            '-aspect': 'aspect ratio',
            '-vf': 'video filter',
            '-pix_fmt': 'pixel format',
            '-preset': 'encoding preset',
            '-crf': 'constant rate factor (quality)',
            '-qscale:v': 'video quality scale',
            '-c:a': 'audio codec',
            '-acodec': 'audio codec (alias)',
            '-b:a': 'audio bitrate',
            '-ar': 'audio sample rate',
            '-ac': 'audio channels',
            '-af': 'audio filter',
            '-an': 'disable audio',
            '-vol': 'audio volume',
            '-aq': 'audio quality',
            '-y': 'overwrite output files',
            '-n': 'never overwrite output files',
            '-map': 'stream mapping',
            '-metadata': 'metadata string',
            '-movflags': 'MOV/MP4 muxer flags',
            '-shortest': 'finish encoding at shortest stream',
            '-codec': 'codec (all streams)',
            '-c': 'codec (alias)',
        }

    return None


@register_completion_schema('rsync')
def _rsync_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for rsync commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': '-a/--archive: archive mode (recursive + preserve permissions, times, etc)',
            '--archive': '--archive/-a: archive mode (recursive + preserve permissions, times, etc)',
            '-v': '-v/--verbose: increase verbosity',
            '--verbose': '--verbose/-v: increase verbosity',
            '-z': '-z/--compress: compress file data during transfer',
            '--compress': '--compress/-z: compress file data during transfer',
            '-r': '-r/--recursive: recurse into directories',
            '--recursive': '--recursive/-r: recurse into directories',
            '-h': '-h/--human-readable: output numbers in human-readable format',
            '--human-readable': '--human-readable/-h: output numbers in human-readable format',
            '-P': '-P: equivalent to --partial --progress',
            '--progress': 'show progress during transfer',
            '-n': '-n/--dry-run: perform trial run with no changes made',
            '--dry-run': '--dry-run/-n: perform trial run with no changes made',
            '--delete': 'delete extraneous files from destination',
            '--exclude': 'exclude files matching pattern',
            '-e': '-e/--rsh: specify remote shell to use',
            '--rsh': '--rsh/-e: specify remote shell to use',
            '--stats': 'show file transfer statistics',
            '--backup': 'make backups of existing destination files',
            '--update': 'skip files that are newer on receiver',
        }
    return None


@register_completion_schema('curl')
def _curl_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for curl commands."""
    # Check if we're after -X flag to show HTTP methods
    # Must check the current token when is_after=True
    current_token = _get_current_token_text(tokens, cursor_token_idx)
    if is_after and current_token in ('-X', '--request'):
        return ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']

    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-X': '-X/--request: specify HTTP request method',
            '--request': '--request/-X: specify HTTP request method',
            '-H': '-H/--header: add custom header',
            '--header': '--header/-H: add custom header',
            '-d': '-d/--data: send data in POST request',
            '--data': '--data/-d: send data in POST request',
            '-F': '-F/--form: submit form data',
            '--form': '--form/-F: submit form data',
            '-o': '-o/--output: write output to file',
            '--output': '--output/-o: write output to file',
            '-O': '-O/--remote-name: save with remote filename',
            '--remote-name': '--remote-name/-O: save with remote filename',
            '-L': '-L/--location: follow redirects',
            '--location': '--location/-L: follow redirects',
            '-i': '-i/--include: include response headers',
            '--include': '--include/-i: include response headers',
            '-I': '-I/--head: fetch headers only',
            '--head': '--head/-I: fetch headers only',
            '-s': '-s/--silent: silent mode',
            '--silent': '--silent/-s: silent mode',
            '-v': '-v/--verbose: verbose output',
            '--verbose': '--verbose/-v: verbose output',
            '-u': '-u/--user: server authentication',
            '--user': '--user/-u: server authentication',
            '-A': '-A/--user-agent: set user agent string',
            '--user-agent': '--user-agent/-A: set user agent string',
            '-b': '-b/--cookie: send cookies',
            '--cookie': '--cookie/-b: send cookies',
            '-c': '-c/--cookie-jar: save cookies to file',
            '--cookie-jar': '--cookie-jar/-c: save cookies to file',
            '-k': '-k/--insecure: skip SSL certificate verification',
            '--insecure': '--insecure/-k: skip SSL certificate verification',
            '-x': '-x/--proxy: use proxy server',
            '--proxy': '--proxy/-x: use proxy server',
        }

    return None


@cached_completion('tmux_sessions', ttl=10)
def _get_tmux_sessions():
    """Get list of tmux sessions (cached for 10 seconds)."""
    try:
        output = subprocess.check_output(
            ['tmux', 'list-sessions', '-F', '#{session_name}'],
            stderr=subprocess.PIPE,
            timeout=2
        )
        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='ignore')
        return [s.strip() for s in output.split('\n') if s.strip()]
    except Exception:
        return []


@register_completion_schema('tmux')
def _tmux_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for tmux commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        if subcommand in ('new-session', 'new'):
            return {
                '-A': 'attach if session exists',
                '-d': 'detach other clients',
                '-D': 'detach other clients on attach',
                '-E': 'do not update environment',
                '-P': 'print session info',
                '-X': 'send signal to group',
                '-s': 'session name',
                '-n': 'window name',
                '-c': 'start directory',
                '-x': 'width',
                '-y': 'height',
                '-e': 'environment variable',
                '-F': 'format string',
                '-f': 'flags',
                '-t': 'target session',
            }
        elif subcommand in ('attach-session', 'attach', 'a'):
            return {
                '-t': 'target session',
                '-d': 'detach other clients',
                '-E': 'do not update environment',
                '-r': 'read-only mode',
                '-x': 'width',
                '-c': 'working directory',
                '-f': 'flags',
            }
        elif subcommand in ('kill-session', 'kill-ses'):
            return {
                '-t': 'target session',
                '-a': 'kill all except target',
                '-C': 'clear terminal',
                '--help': 'show help',
            }
        elif subcommand in ('split-window', 'splitw'):
            return {
                '-h': 'split horizontally',
                '-v': 'split vertically',
                '-p': 'percentage of pane size',
                '-t': 'target pane',
                '-c': 'start directory',
                '-d': 'do not make new pane active',
                '-b': 'create pane before target',
                '-f': 'full width/height',
                '--help': 'show help',
            }
        elif subcommand in ('new-window', 'neww'):
            return {
                '-n': 'window name',
                '-t': 'target window',
                '-c': 'start directory',
                '-d': 'do not make new window active',
                '-a': 'insert after target',
                '-b': 'insert before target',
                '--help': 'show help',
            }
        elif subcommand in ('select-window', 'selectw'):
            return {
                '-t': 'target window',
                '-l': 'last window',
                '-n': 'next window',
                '-p': 'previous window',
                '--help': 'show help',
            }
        elif subcommand in ('select-pane', 'selectp'):
            return {
                '-t': 'target pane',
                '-U': 'select pane up',
                '-D': 'select pane down',
                '-L': 'select pane left',
                '-R': 'select pane right',
                '-l': 'last pane',
                '--help': 'show help',
            }
        elif subcommand in ('detach-client', 'detach'):
            return {
                '-s': 'target session',
                '-t': 'target client',
                '-a': 'detach all except target',
                '-P': 'send SIGHUP',
                '--help': 'show help',
            }
        elif subcommand in ('send-keys', 'send'):
            return {
                '-t': 'target pane',
                '-l': 'send keys literally',
                '-R': 'reset terminal state',
                '-M': 'mouse event',
                '-X': 'copy mode command',
                '--help': 'show help',
            }
        elif subcommand in ('capture-pane', 'capturep'):
            return {
                '-t': 'target pane',
                '-p': 'print to stdout',
                '-e': 'include escape sequences',
                '-a': 'use alternate screen',
                '-S': 'start line',
                '-E': 'end line',
                '--help': 'show help',
            }
        elif subcommand in ('save-buffer', 'saveb'):
            return {
                '-a': 'append to file',
                '-b': 'buffer name',
                '--help': 'show help',
            }
        elif subcommand in ('load-buffer', 'loadb'):
            return {
                '-b': 'buffer name',
                '--help': 'show help',
            }
        elif subcommand in ('list-sessions', 'ls'):
            return {
                '-F': 'format string',
                '--help': 'show help',
            }
        elif subcommand in ('list-windows', 'lsw'):
            return {
                '-t': 'target session',
                '-F': 'format string',
                '-a': 'all sessions',
                '--help': 'show help',
            }
        elif subcommand in ('list-panes', 'lsp'):
            return {
                '-t': 'target window',
                '-s': 'session-wide',
                '-a': 'all panes',
                '-F': 'format string',
                '--help': 'show help',
            }
        elif subcommand in ('bind-key', 'bind'):
            return {
                '-n': 'no prefix key',
                '-r': 'repeatable',
                '-T': 'key table',
                '-N': 'note',
            }
        elif subcommand in ('unbind-key', 'unbind'):
            return {
                '-a': 'remove all bindings',
                '-n': 'no prefix key',
                '-q': 'quiet',
                '-T': 'key table',
            }
        elif subcommand in ('source-file', 'source'):
            return {
                '-F': 'expand formats',
                '-n': 'do not execute',
                '-q': 'quiet',
                '-v': 'verbose',
                '-t': 'target pane',
            }
        elif subcommand in ('display-message', 'display'):
            return {
                '-a': 'list all clients',
                '-I': 'forward stdin',
                '-l': 'print to log',
                '-N': 'no escapes',
                '-p': 'print to stdout',
                '-v': 'verbose',
                '-c': 'target client',
                '-d': 'delay',
                '-F': 'format string',
                '-t': 'target pane',
            }
        elif subcommand in ('display-panes', 'displayp'):
            return {
                '-b': 'do not block',
                '-N': 'no activity',
                '-d': 'duration',
                '-t': 'target client',
            }
        elif subcommand in ('choose-tree',):
            return {
                '-G': 'include all sessions',
                '-N': 'start without preview',
                '-r': 'reverse order',
                '-s': 'sessions only',
                '-w': 'windows only',
                '-Z': 'zoom',
                '-F': 'format string',
                '-f': 'filter',
                '-K': 'key format',
                '-O': 'sort order',
                '-t': 'target pane',
            }
        elif subcommand in ('choose-client',):
            return {
                '-N': 'start without preview',
                '-r': 'reverse order',
                '-Z': 'zoom',
                '-F': 'format string',
                '-f': 'filter',
                '-K': 'key format',
                '-O': 'sort order',
                '-t': 'target pane',
            }
        elif subcommand in ('clock-mode',):
            return {
                '-t': 'target pane',
            }
        elif subcommand in ('command-prompt',):
            return {
                '-1': 'accept one key',
                '-b': 'before cursor',
                '-F': 'expand formats',
                '-k': 'key mode',
                '-i': 'initial text',
                '-I': 'comma-separated list',
                '-N': 'number prompts',
                '-p': 'prompts',
                '-t': 'target client',
                '-T': 'prompt type',
            }
        elif subcommand in ('confirm-before', 'confirm'):
            return {
                '-b': 'default to no',
                '-y': 'default to yes',
                '-c': 'target client',
                '-p': 'prompt',
                '-t': 'target client',
            }
        elif subcommand in ('copy-mode',):
            return {
                '-e': 'exit if at bottom',
                '-H': 'hide position',
                '-M': 'mouse drag',
                '-u': 'scroll up',
                '-q': 'cancel existing',
                '-s': 'source pane',
                '-t': 'target pane',
            }
        elif subcommand in ('find-window', 'findw'):
            return {
                '-C': 'content search',
                '-i': 'case insensitive',
                '-N': 'name search',
                '-r': 'regex search',
                '-T': 'title search',
                '-Z': 'zoom',
                '-t': 'target window',
            }
        elif subcommand in ('join-pane', 'joinp'):
            return {
                '-b': 'join before',
                '-d': 'do not make active',
                '-f': 'full size',
                '-h': 'horizontal split',
                '-v': 'vertical split',
                '-l': 'size',
                '-s': 'source pane',
                '-t': 'target pane',
            }
        elif subcommand in ('break-pane', 'breakp'):
            return {
                '-a': 'insert after',
                '-b': 'insert before',
                '-d': 'do not make active',
                '-P': 'print info',
                '-F': 'format string',
                '-n': 'window name',
                '-s': 'source pane',
                '-t': 'target window',
            }
        elif subcommand in ('last-pane', 'lastp'):
            return {
                '-d': 'disable',
                '-e': 'enable',
                '-Z': 'keep zoomed',
                '-t': 'target window',
            }
        elif subcommand in ('next-layout', 'nextl'):
            return {
                '-t': 'target window',
            }
        elif subcommand in ('prev-layout', 'prevl'):
            return {
                '-t': 'target window',
            }
        elif subcommand in ('pipe-pane', 'pipep'):
            return {
                '-I': 'stdin',
                '-O': 'stdout',
                '-o': 'open/toggle',
                '-t': 'target pane',
            }
        elif subcommand in ('refresh-client', 'refresh'):
            return {
                '-c': 'target client',
                '-D': 'set visible pane',
                '-l': 'request clipboard',
                '-L': 'move client left',
                '-R': 'move client right',
                '-S': 'set pane size',
                '-U': 'move client up',
                '-A': 'adjust size',
                '-B': 'refresh border',
                '-C': 'set cursor',
                '-f': 'flags',
                '-t': 'target client',
            }
        elif subcommand in ('run-shell', 'run'):
            return {
                '-b': 'background',
                '-C': 'invoke command',
                '-c': 'current directory',
                '-d': 'delay',
                '-t': 'target pane',
            }
        elif subcommand in ('suspend-client', 'suspendc'):
            return {
                '-t': 'target client',
            }
        elif subcommand in ('switch-client', 'switchc'):
            return {
                '-E': 'update environment',
                '-l': 'last session',
                '-n': 'next session',
                '-p': 'previous session',
                '-r': 'read-only',
                '-Z': 'keep zoomed',
                '-c': 'target client',
                '-t': 'target session',
                '-T': 'key table',
            }
        elif subcommand in ('wait-for', 'wait'):
            return {
                '-L': 'lock',
                '-S': 'signal',
                '-U': 'unlock',
            }
        else:
            return {
                '--help': 'show help message',
                '-V': 'show version',
            }

    # Main subcommands
    if cursor_token_idx == 0 and is_after:
        return {
            'new-session': 'create new session',
            'new': 'alias for new-session',
            'attach-session': 'attach to existing session',
            'attach': 'alias for attach-session',
            'a': 'alias for attach-session',
            'kill-session': 'kill session',
            'kill-ses': 'alias for kill-session',
            'list-sessions': 'list all sessions',
            'ls': 'alias for list-sessions',
            'list-windows': 'list windows in session',
            'lsw': 'alias for list-windows',
            'list-panes': 'list panes in window',
            'lsp': 'alias for list-panes',
            'split-window': 'split pane into two',
            'splitw': 'alias for split-window',
            'new-window': 'create new window',
            'neww': 'alias for new-window',
            'select-window': 'select window by index',
            'selectw': 'alias for select-window',
            'select-pane': 'select pane within window',
            'selectp': 'alias for select-pane',
            'detach-client': 'detach from session',
            'detach': 'alias for detach-client',
            'send-keys': 'send keys to pane',
            'send': 'alias for send-keys',
            'capture-pane': 'capture pane contents',
            'capturep': 'alias for capture-pane',
            'save-buffer': 'save buffer to file',
            'saveb': 'alias for save-buffer',
            'load-buffer': 'load buffer from file',
            'loadb': 'alias for load-buffer',
            'rename-session': 'rename session',
            'rename-window': 'rename window',
            'swap-pane': 'swap two panes',
            'swap-window': 'swap two windows',
            'move-pane': 'move pane to another window',
            'move-window': 'move window to another session',
            'resize-pane': 'resize pane',
            'respawnp': 'alias for respawn-pane',
            'respawn-pane': 'respawn pane with command',
            'respawn-window': 'respawn window with command',
            'rotate-window': 'rotate panes in window',
            'set-option': 'set session/window option',
            'set': 'alias for set-option',
            'show-options': 'show option values',
            'show': 'alias for show-options',
            'bind-key': 'bind key to command',
            'bind': 'alias for bind-key',
            'unbind-key': 'unbind key',
            'unbind': 'alias for unbind-key',
            'source-file': 'source config file',
            'source': 'alias for source-file',
            'display-message': 'display message in status line',
            'display': 'alias for display-message',
            'display-panes': 'display pane indicators',
            'displayp': 'alias for display-panes',
            'choose-tree': 'choose session/window from tree',
            'choose-client': 'choose client from list',
            'clock-mode': 'display clock',
            'command-prompt': 'open command prompt',
            'confirm-before': 'prompt for confirmation',
            'confirm': 'alias for confirm-before',
            'copy-mode': 'enter copy mode',
            'find-window': 'find window by name',
            'findw': 'alias for find-window',
            'join-pane': 'join pane to window',
            'joinp': 'alias for join-pane',
            'break-pane': 'break pane into window',
            'breakp': 'alias for break-pane',
            'last-pane': 'switch to last pane',
            'lastp': 'alias for last-pane',
            'next-layout': 'cycle to next layout',
            'nextl': 'alias for next-layout',
            'prev-layout': 'cycle to previous layout',
            'prevl': 'alias for prev-layout',
            'pipe-pane': 'pipe pane output to command',
            'pipep': 'alias for pipe-pane',
            'refresh-client': 'refresh client display',
            'refresh': 'alias for refresh-client',
            'run-shell': 'run shell command',
            'run': 'alias for run-shell',
            'suspend-client': 'suspend client',
            'suspendc': 'alias for suspend-client',
            'switch-client': 'switch client to session',
            'switchc': 'alias for switch-client',
            'wait-for': 'wait for event',
            'wait': 'alias for wait-for',
        }

    # Session name completions for -t flag
    elif cursor_token_idx >= 2:
        # Check if previous token is -t flag
        if cursor_token_idx >= 1 and tokens[cursor_token_idx - 1].text == '-t':
            return _get_tmux_sessions()

    return None


@register_completion_schema('pytest')
def _pytest_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for pytest commands."""
    # Check if cursor is after a flag that expects values
    if is_after and cursor_token_idx < len(tokens):
        current_token = tokens[cursor_token_idx].text
        if current_token == '--tb':
            return ['auto', 'long', 'short', 'line', 'native', 'no']
        elif current_token == '--cov-report':
            return ['term', 'html', 'xml', 'annotate']

    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-v': '-v/--verbose: increase verbosity',
            '--verbose': '--verbose/-v: increase verbosity',
            '-s': '-s/--capture=no: disable output capturing',
            '--capture=no': '--capture=no/-s: disable output capturing',
            '-k': '-k/--keyword: run tests matching keyword expression',
            '--keyword': '--keyword/-k: run tests matching keyword expression',
            '-m': '-m/--markers: run tests matching mark expression',
            '--markers': '--markers/-m: run tests matching mark expression',
            '-x': '-x/--exitfirst: exit on first test failure',
            '--exitfirst': '--exitfirst/-x: exit on first test failure',
            '--maxfail': 'exit after N failures or errors',
            '--tb': 'traceback print mode (auto/long/short/line/native/no)',
            '--pdb': 'start debugger on errors',
            '--lf': '--lf/--last-failed: rerun only failed tests',
            '--last-failed': '--last-failed/--lf: rerun only failed tests',
            '--ff': '--ff/--failed-first: run failed tests first',
            '--failed-first': '--failed-first/--ff: run failed tests first',
            '-n': '-n/--numprocesses: number of processes for parallel execution',
            '--numprocesses': '--numprocesses/-n: number of processes for parallel execution',
            '--cov': 'measure code coverage for packages',
            '--cov-report': 'coverage report type (term/html/xml/annotate)',
            '-q': '-q/--quiet: decrease verbosity',
            '--quiet': '--quiet/-q: decrease verbosity',
            '--collect-only': 'collect tests but don\'t execute them',
            '--fixtures': 'show available fixtures',
        }

    # Complete flags at position 0
    if cursor_token_idx == 0 and is_after:
        return {
            '-v': '-v/--verbose: increase verbosity',
            '--verbose': '--verbose/-v: increase verbosity',
            '-s': '-s/--capture=no: disable output capturing',
            '--capture=no': '--capture=no/-s: disable output capturing',
            '-k': '-k/--keyword: run tests matching keyword expression',
            '--keyword': '--keyword/-k: run tests matching keyword expression',
            '-m': '-m/--markers: run tests matching mark expression',
            '--markers': '--markers/-m: run tests matching mark expression',
            '-x': '-x/--exitfirst: exit on first test failure',
            '--exitfirst': '--exitfirst/-x: exit on first test failure',
            '--maxfail': 'exit after N failures or errors',
            '--tb': 'traceback print mode (auto/long/short/line/native/no)',
            '--pdb': 'start debugger on errors',
            '--lf': '--lf/--last-failed: rerun only failed tests',
            '--last-failed': '--last-failed/--lf: rerun only failed tests',
            '--ff': '--ff/--failed-first: run failed tests first',
            '--failed-first': '--failed-first/--ff: run failed tests first',
            '-n': '-n/--numprocesses: number of processes for parallel execution',
            '--numprocesses': '--numprocesses/-n: number of processes for parallel execution',
            '--cov': 'measure code coverage for packages',
            '--cov-report': 'coverage report type (term/html/xml/annotate)',
            '-q': '-q/--quiet: decrease verbosity',
            '--quiet': '--quiet/-q: decrease verbosity',
            '--collect-only': 'collect tests but don\'t execute them',
            '--fixtures': 'show available fixtures',
        }

    return None


@register_completion_schema('jupyter')
def _jupyter_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for jupyter commands."""
    # Check if cursor is after a flag that expects values  
    if is_after and cursor_token_idx < len(tokens):
        current_token = tokens[cursor_token_idx].text
        if current_token == '--to':
            return ['html', 'pdf', 'latex', 'markdown', 'python', 'rst', 'script']

    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        common_flags = {
            '--help': 'show help message',
            '--version': 'show version information',
        }

        if subcommand in ('notebook', 'lab'):
            notebook_flags = {
                '--port': 'specify port for server',
                '--ip': 'IP address server will listen on',
                '--no-browser': 'do not open browser automatically',
                '--notebook-dir': 'directory to use for notebooks',
                '--help': 'show help message',
            }
            return notebook_flags
        elif subcommand == 'nbconvert':
            nbconvert_flags = {
                '--to': 'convert notebook to specified format',
                '--output': 'output file name',
                '--help': 'show help message',
            }
            return nbconvert_flags
        else:
            return common_flags

    if cursor_token_idx == 0 and is_after:
        return {
            'notebook': 'start Jupyter notebook server',
            'lab': 'start JupyterLab server',
            'console': 'start Jupyter console',
            'kernelspec': 'manage Jupyter kernels',
            'nbconvert': 'convert notebooks to other formats',
            'trust': 'trust notebook execution',
            'troubleshoot': 'troubleshoot Jupyter issues',
            'server': 'manage Jupyter server',
        }

    elif cursor_token_idx == 1:
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        if subcommand == 'kernelspec':
            return {
                'list': 'list available kernels',
                'install': 'install kernel',
                'uninstall': 'uninstall kernel',
            }
        elif subcommand == 'nbconvert':
            # After nbconvert, user might want --to flag or a file
            nbconvert_flags = {
                '--to': 'convert notebook to specified format',
                '--output': 'output file name',
                '--help': 'show help message',
            }
            return nbconvert_flags

    return None


@register_completion_schema('ollama')
def _ollama_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ollama commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''
        common_flags = {
            '--help': 'show help message',
        }

        flag_mapping = {
            'run': {
                '--verbose': 'enable verbose output',
                '--insecure': 'use insecure connection',
                '--nowordwrap': 'disable word wrapping',
                '--format': 'response format (json)',
            },
            'pull': {
                '--insecure': 'use insecure connection',
            },
            'push': {
                '--insecure': 'use insecure connection',
            },
            'list': {
                '--format': 'output format (json)',
            },
            'show': {
                '--modelfile': 'show Modelfile for model',
                '--parameters': 'show parameters for model',
                '--template': 'show template for model',
                '--system': 'show system message for model',
            },
            'create': {
                '--file': 'path to Modelfile',
                '-f': 'path to Modelfile',
            },
            'rm': {
                # remove model, no specific flags beyond common
            },
            'cp': {
                # copy model, no specific flags beyond common
            },
            'serve': {
                '--address': 'bind address for server',
            },
            'ps': {
                '--format': 'output format (json)',
            },
        }

        return _get_subcommand_flags(subcommand, flag_mapping, common_flags)

    result = _complete_at_position_zero(cursor_token_idx, is_after, {
        'run': 'run model',
        'pull': 'pull model from registry',
        'push': 'push model to registry',
        'list': 'list local models',
        'show': 'show model info',
        'create': 'create model from Modelfile',
        'rm': 'remove model',
        'cp': 'copy model',
        'serve': 'start server',
        'ps': 'list running models',
    })
    if result:
        return result

    return None


@register_completion_schema('streamlit')
def _streamlit_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for streamlit commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        if subcommand == 'run':
            # Check if we're after --theme.base flag
            if cursor_token_idx >= 1:
                for i in range(cursor_token_idx, -1, -1):
                    if i < len(tokens) and tokens[i].text == '--theme.base':
                        # We're completing the value after --theme.base
                        if cursor_token_idx == i or (cursor_token_idx == i + 1):
                            return ['light', 'dark']

            run_flags = {
                '--server.port': 'port number for server',
                '--server.address': 'address to bind server to',
                '--server.headless': 'run server in headless mode',
                '--browser.serverAddress': 'browser server address',
                '--theme.base': 'base theme (light/dark)',
            }
            return run_flags
        else:
            common_flags = {
                '--help': 'show help message',
                '--version': 'show version information',
            }
            return common_flags

    if cursor_token_idx == 0 and is_after:
        return {
            'run': 'run Streamlit app',
            'hello': 'run hello world demo',
            'config': 'manage config settings',
            'cache': 'manage cache',
            'docs': 'open documentation',
            'version': 'show version',
        }

    elif cursor_token_idx == 1:
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        if subcommand == 'config':
            return {
                'show': 'show current config',
            }
        elif subcommand == 'cache':
            return {
                'clear': 'clear cache',
            }

    return None




@register_completion_schema('vim')
def _vim_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for vim commands."""
    # Only complete flags, otherwise return None to allow filename completion
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-R': 'read-only mode (view mode)',
            '-m': 'modifications not allowed (write disabled)',
            '-n': 'no swap file, use memory only',
            '-r': 'list swap files and exit, or recover crashed session',
            '-L': 'same as -r (recovery mode)',
            '-c': 'execute command after loading first file',
            '-S': 'source session file after loading first file',
            '-u': 'use alternative vimrc file',
            '-i': 'use alternative viminfo file',
            '-o': 'open N windows stacked horizontally',
            '-O': 'open N windows side by side vertically',
            '-p': 'open N tab pages',
            '-d': 'diff mode (like vimdiff)',
            '-b': 'binary mode',
            '+': 'start at end of file or execute command',
            '--help': 'show help message and exit',
            '--version': 'show version information and exit',
        }
    return None


@register_completion_schema('nvim')
def _nvim_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for nvim commands (same as vim)."""
    # Only complete flags, otherwise return None to allow filename completion
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-R': 'read-only mode (view mode)',
            '-m': 'modifications not allowed (write disabled)',
            '-n': 'no swap file, use memory only',
            '-r': 'list swap files and exit, or recover crashed session',
            '-L': 'same as -r (recovery mode)',
            '-c': 'execute command after loading first file',
            '-S': 'source session file after loading first file',
            '-u': 'use alternative vimrc file',
            '-i': 'use alternative viminfo file',
            '-o': 'open N windows stacked horizontally',
            '-O': 'open N windows side by side vertically',
            '-p': 'open N tab pages',
            '-d': 'diff mode (like vimdiff)',
            '-b': 'binary mode',
            '+': 'start at end of file or execute command',
            '--help': 'show help message and exit',
            '--version': 'show version information and exit',
        }
    return None


@register_completion_schema('grep')
def _grep_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for grep commands."""
    # Only complete flags, otherwise return None to allow filename completion
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-i': '-i/--ignore-case: case-insensitive search',
            '--ignore-case': '--ignore-case/-i: case-insensitive search',
            '-v': '-v/--invert-match: select non-matching lines',
            '--invert-match': '--invert-match/-v: select non-matching lines',
            '-r': '-r/--recursive: search directories recursively',
            '--recursive': '--recursive/-r: search directories recursively',
            '-R': '-R: search directories recursively (follow symlinks)',
            '-n': '-n/--line-number: show line numbers',
            '--line-number': '--line-number/-n: show line numbers',
            '-H': '-H/--with-filename: print filename for each match',
            '--with-filename': '--with-filename/-H: print filename for each match',
            '-h': '-h/--no-filename: suppress filename prefix',
            '--no-filename': '--no-filename/-h: suppress filename prefix',
            '-l': '-l/--files-with-matches: only print filenames with matches',
            '--files-with-matches': '--files-with-matches/-l: only print filenames with matches',
            '-L': '-L/--files-without-match: only print filenames without matches',
            '--files-without-match': '--files-without-match/-L: only print filenames without matches',
            '-c': '-c/--count: count matching lines',
            '--count': '--count/-c: count matching lines',
            '-o': '-o/--only-matching: print only matched parts',
            '--only-matching': '--only-matching/-o: print only matched parts',
            '-w': '-w/--word-regexp: match whole words only',
            '--word-regexp': '--word-regexp/-w: match whole words only',
            '-x': '-x/--line-regexp: match whole lines only',
            '--line-regexp': '--line-regexp/-x: match whole lines only',
            '-E': '-E/--extended-regexp: use extended regex (ERE)',
            '--extended-regexp': '--extended-regexp/-E: use extended regex (ERE)',
            '-F': '-F/--fixed-strings: treat pattern as literal string',
            '--fixed-strings': '--fixed-strings/-F: treat pattern as literal string',
            '-P': '-P/--perl-regexp: use Perl-compatible regex (PCRE)',
            '--perl-regexp': '--perl-regexp/-P: use Perl-compatible regex (PCRE)',
            '-A': '-A/--after-context: print NUM lines after match',
            '--after-context': '--after-context/-A: print NUM lines after match',
            '-B': '-B/--before-context: print NUM lines before match',
            '--before-context': '--before-context/-B: print NUM lines before match',
            '-C': '-C/--context: print NUM lines before and after match',
            '--context': '--context/-C: print NUM lines before and after match',
            '-m': '-m/--max-count: stop after NUM matches',
            '--max-count': '--max-count/-m: stop after NUM matches',
            '-q': '-q/--quiet: suppress all output, exit status only',
            '--quiet': '--quiet/-q: suppress all output, exit status only',
            '--silent': '--silent: suppress all output, exit status only',
            '-s': '-s/--no-messages: suppress error messages',
            '--no-messages': '--no-messages/-s: suppress error messages',
            '-b': '-b/--byte-offset: print byte offset with output',
            '--byte-offset': '--byte-offset/-b: print byte offset with output',
            '-a': '-a/--text: treat binary files as text',
            '--text': '--text/-a: treat binary files as text',
            '-I': '-I: ignore binary files',
            '-d': '-d/--directories: action for directories (read/skip/recurse)',
            '--directories': '--directories/-d: action for directories (read/skip/recurse)',
            '-D': '-D/--devices: action for devices (read/skip)',
            '--devices': '--devices/-D: action for devices (read/skip)',
            '-e': '-e/--regexp: use PATTERN for matching',
            '--regexp': '--regexp/-e: use PATTERN for matching',
            '-f': '-f/--file: read patterns from FILE',
            '--file': '--file/-f: read patterns from FILE',
            '-Z': '-Z/--null: print null byte after filename',
            '--null': '--null/-Z: print null byte after filename',
            '--color': '--color: colorize output',
            '--colour': '--colour: colorize output',
            '--include': '--include: search only files matching pattern',
            '--exclude': '--exclude: skip files matching pattern',
            '--exclude-dir': '--exclude-dir: skip directories matching pattern',
        }
    return None


@register_completion_schema('tar')
def _tar_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for tar commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        # Common flag combinations and individual flags with descriptions
        return {
            '-czf': 'create new gzip archive with file',
            '-xzf': 'extract gzip archive from file',
            '-cjf': 'create new bzip2 archive with file',
            '-xjf': 'extract bzip2 archive from file',
            '-cJf': 'create new xz archive with file',
            '-xJf': 'extract xz archive from file',
            '-tvf': 'list contents of archive verbosely with file',
            '-xvf': 'extract archive verbosely from file',
            '-cvf': 'create new archive verbosely with file',
            '-c': '-c/--create: create new archive',
            '--create': '--create/-c: create new archive',
            '-x': '-x/--extract: extract files from archive',
            '--extract': '--extract/-x: extract files from archive',
            '-t': '-t/--list: list contents of archive',
            '--list': '--list/-t: list contents of archive',
            '-v': '-v/--verbose: verbose output',
            '--verbose': '--verbose/-v: verbose output',
            '-f': '-f/--file: specify archive file',
            '--file': '--file/-f: specify archive file',
            '-z': '-z/--gzip: compress with gzip',
            '--gzip': '--gzip/-z: compress with gzip',
            '-j': '-j/--bzip2: compress with bzip2',
            '--bzip2': '--bzip2/-j: compress with bzip2',
            '-J': '-J/--xz: compress with xz',
            '--xz': '--xz/-J: compress with xz',
            '-C': '-C/--directory: change to directory before operation',
            '--directory': '--directory/-C: change to directory before operation',
            '-r': '-r/--append: append files to archive',
            '--append': '--append/-r: append files to archive',
            '-u': '-u/--update: only append newer files',
            '--update': '--update/-u: only append newer files',
            '-p': '-p/--preserve-permissions: preserve file permissions',
            '--preserve-permissions': '--preserve-permissions/-p: preserve file permissions',
            '-h': '-h/--dereference: follow symlinks',
            '--dereference': '--dereference/-h: follow symlinks',
            '-a': '-a/--auto-compress: auto-detect compression by extension',
            '--auto-compress': '--auto-compress/-a: auto-detect compression by extension',
            '-k': '-k/--keep-old-files: do not overwrite existing files',
            '--keep-old-files': '--keep-old-files/-k: do not overwrite existing files',
            '-m': '-m/--touch: do not extract modification time',
            '--touch': '--touch/-m: do not extract modification time',
            '-o': '-o/--no-same-owner: extract files as yourself',
            '--no-same-owner': '--no-same-owner/-o: extract files as yourself',
            '-P': '-P/--absolute-names: do not strip leading slashes',
            '--absolute-names': '--absolute-names/-P: do not strip leading slashes',
            '-w': '-w/--interactive: ask for confirmation',
            '--interactive': '--interactive/-w: ask for confirmation',
            '-W': '-W/--verify: verify archive after writing',
            '--verify': '--verify/-W: verify archive after writing',
            '--exclude': 'exclude files matching pattern',
            '--wildcards': 'use wildcards in patterns',
            '--no-wildcards': 'treat wildcards literally',
            '--anchored': 'patterns match start of path',
            '--no-anchored': 'patterns match anywhere',
            '--ignore-case': 'ignore case in patterns',
            '--no-ignore-case': 'case-sensitive patterns',
            '--strip-components': 'strip number of leading path components',
            '--transform': 'transform file names using sed expression',
            '--show-transformed-names': 'show transformed file names',
            '--same-owner': 'preserve original file ownership',
            '--no-same-permissions': 'apply user umask to permissions',
            '--numeric-owner': 'use numeric UIDs/GIDs',
            '--overwrite': 'overwrite existing files',
            '--remove-files': 'remove files after adding to archive',
            '--recursion': 'recurse into directories',
            '--no-recursion': 'do not recurse into directories',
            '--one-file-system': 'stay in local file system',
            '--totals': 'print total bytes after processing',
            '--checkpoint': 'display progress messages',
            '--checkpoint-action': 'execute action at each checkpoint',
            '--warning': 'control warning display',
            '--help': 'display help information',
            '--version': 'display version information',
            '--usage': 'display brief usage message',
        }
    return _complete_paths(tokens, cursor_token_idx, is_after)


@register_completion_schema('find')
def _find_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for find commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        # Check if previous token is -type to show type values
        if cursor_token_idx >= 1 and tokens[cursor_token_idx - 1].text == '-type':
            return {
                'f': 'regular file',
                'd': 'directory',
                'l': 'symbolic link',
                'b': 'block special',
                'c': 'character special',
                'p': 'FIFO (named pipe)',
                's': 'socket'
            }

        return {
            '-name': 'match basename pattern (case-sensitive)',
            '-iname': 'match basename pattern (case-insensitive)',
            '-type': 'match file type (f=file, d=directory, l=symlink, etc)',
            '-size': 'match file size (e.g., +100k, -1M)',
            '-mtime': 'match modification time in days (e.g., -7, +30)',
            '-atime': 'match access time in days',
            '-ctime': 'match status change time in days',
            '-user': 'match file owner by name or UID',
            '-group': 'match file group by name or GID',
            '-perm': 'match file permissions (e.g., 644, -755, /222)',
            '-exec': 'execute command on matched files',
            '-delete': 'delete matched files (use with caution)',
            '-print': 'print full file name on standard output',
            '-print0': 'print full file name, null-separated',
            '-maxdepth': 'descend at most N directory levels',
            '-mindepth': 'ignore files at levels less than N',
            '-path': 'match full path pattern (case-sensitive)',
            '-ipath': 'match full path pattern (case-insensitive)',
            '-regex': 'match full path against regex (case-sensitive)',
            '-iregex': 'match full path against regex (case-insensitive)',
            '-newer': 'match files modified more recently than reference file',
            '-empty': 'match empty files and directories',
            '-readable': 'match files readable by current user',
            '-writable': 'match files writable by current user',
            '-executable': 'match files executable by current user',
            '-prune': 'do not descend into matched directories',
            '-depth': 'process directory contents before directory itself',
            '-follow': 'follow symbolic links',
            '-lname': 'match symbolic link name pattern',
            '-ilname': 'match symbolic link name pattern (case-insensitive)',
            '-samefile': 'match files referring to same inode',
            '-inum': 'match files with specific inode number',
            '-links': 'match files with N hard links',
            '-nouser': 'match files with no valid user',
            '-nogroup': 'match files with no valid group',
            '-uid': 'match files with specific user ID',
            '-gid': 'match files with specific group ID',
            '-anewer': 'match files accessed more recently than reference',
            '-cnewer': 'match files changed more recently than reference',
            '-newer[acm][acmt]': 'compare file timestamps (e.g., -newermt, -neweram)',
            '-not': 'negate the following expression',
            '-or': 'logical OR between expressions',
            '-and': 'logical AND between expressions',
            '-true': 'always true',
            '-false': 'always false',
            '-ls': 'list matched files in ls -dils format',
            '-fls': 'list matched files to file in ls -dils format',
            '-ok': 'like -exec but ask for confirmation',
            '-okdir': 'like -execdir but ask for confirmation',
            '-execdir': 'execute command from subdirectory containing match',
            '-quit': 'exit immediately upon finding first match',
            '-printf': 'print formatted output',
            '-fprintf': 'print formatted output to file',
            '-mount': 'do not descend directories on other filesystems',
            '-xdev': 'do not descend directories on other filesystems',
            '-ignore_readdir_race': 'suppress errors from files disappearing during execution',
            '-noignore_readdir_race': 'report errors from files disappearing',
            '-daystart': 'measure times from beginning of today',
            '-regextype': 'specify regex type (e.g., posix-extended, emacs)',
            '-wholename': 'synonym for -path',
            '-iwholename': 'synonym for -ipath'
        }
    return None


@register_completion_schema('wget')
def _wget_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for wget commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-O': '-O/--output-document: write documents to file',
            '--output-document': '--output-document/-O: write documents to file',
            '-o': '-o/--output-file: log messages to file',
            '--output-file': '--output-file/-o: log messages to file',
            '-c': '-c/--continue: resume getting partially-downloaded file',
            '--continue': '--continue/-c: resume getting partially-downloaded file',
            '-b': '-b/--background: go to background after startup',
            '--background': '--background/-b: go to background after startup',
            '-q': '-q/--quiet: quiet mode',
            '--quiet': '--quiet/-q: quiet mode',
            '-v': '-v/--verbose: verbose output',
            '--verbose': '--verbose/-v: verbose output',
            '-r': '-r/--recursive: recursive download',
            '--recursive': '--recursive/-r: recursive download',
            '-l': '-l/--level: maximum recursion depth',
            '--level': '--level/-l: maximum recursion depth',
            '-k': '-k/--convert-links: convert links for local viewing',
            '--convert-links': '--convert-links/-k: convert links for local viewing',
            '-p': '-p/--page-requisites: download all files for page display',
            '--page-requisites': '--page-requisites/-p: download all files for page display',
            '-np': '-np/--no-parent: do not ascend to parent directory',
            '--no-parent': '--no-parent/-np: do not ascend to parent directory',
            '-N': '-N/--timestamping: only retrieve newer files',
            '--timestamping': '--timestamping/-N: only retrieve newer files',
            '-U': '-U/--user-agent: identify as agent-string',
            '--user-agent': '--user-agent/-U: identify as agent-string',
            '--header': 'insert string in headers',
            '--timeout': 'set all timeout values',
            '--tries': 'set number of retries',
            '--limit-rate': 'limit download rate',
            '--spider': 'do not download, just check if pages exist',
            '--no-check-certificate': 'do not validate SSL certificates',
        }
    return None


@register_completion_schema('chmod')
def _chmod_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for chmod commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-R': 'recursive: change files and directories recursively',
            '--recursive': 'recursive: change files and directories recursively',
            '-v': 'verbose: output a diagnostic for every file processed',
            '--verbose': 'verbose: output a diagnostic for every file processed',
            '-c': 'changes: like verbose but report only when a change is made',
            '--changes': 'changes: like verbose but report only when a change is made',
            '-f': 'silent/quiet: suppress most error messages',
            '--silent': 'silent/quiet: suppress most error messages',
            '--quiet': 'silent/quiet: suppress most error messages',
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }

    # Don't complete at position 0 - chmod takes mode+file, let files complete
    return None


@register_completion_schema('ps')
def _ps_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ps commands."""
    # Only complete when in flag context
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            'aux': 'BSD-style: all users, user-oriented, with no controlling terminal',
            '-e': '-e/-A: all processes',
            '-A': '-A/-e: all processes',
            '-f': 'full format listing (man ps)',
            '-a': 'all processes except session leaders and terminal-unrelated',
            '-u': 'user-oriented format',
            '-x': 'include processes without controlling terminal',
            '-l': 'long format',
            '-w': 'wide output (can be used multiple times)',
            '-o': 'custom output format (specify columns)',
            '--sort': 'sort by specified column',
            '--forest': 'ASCII art process tree',
            '--no-headers': 'suppress header line',
            '-p': '-p/--pid: select by process ID',
            '--pid': '--pid/-p: select by process ID',
            '-C': 'select by command name',
            '--help': 'display help message',
        }

    return None


@register_completion_schema('df')
def _df_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for df commands."""
    # Only complete when in flag context
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-h': 'human-readable: print sizes in powers of 1024 (e.g., 1023M)',
            '--human-readable': 'human-readable: print sizes in powers of 1024 (e.g., 1023M)',
            '-H': 'SI: print sizes in powers of 1000 (e.g., 1.1G)',
            '-k': 'use 1024-byte blocks (default)',
            '-m': 'use 1048576-byte (1M) blocks',
            '-B': 'block-size: scale sizes by SIZE before printing',
            '--block-size': 'scale sizes by SIZE before printing',
            '-T': 'print-type: print file system type',
            '--print-type': 'print file system type',
            '-t': 'type: limit listing to file systems of type TYPE',
            '--type': 'limit listing to file systems of type TYPE',
            '-x': 'exclude-type: limit listing to file systems not of type TYPE',
            '--exclude-type': 'limit listing to file systems not of type TYPE',
            '-a': 'all: include pseudo, duplicate, inaccessible file systems',
            '--all': 'all: include pseudo, duplicate, inaccessible file systems',
            '-i': 'inodes: list inode information instead of block usage',
            '--inodes': 'list inode information instead of block usage',
            '--total': 'produce a grand total',
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }

    return None


@register_completion_schema('scp')
def _scp_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for scp commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-r': '-r/--recursive: recursively copy entire directories',
            '--recursive': '--recursive/-r: recursively copy entire directories',
            '-P': '-P: specify port to connect to on remote host',
            '-p': '-p: preserve modification times, access times, and modes',
            '-q': '-q: quiet mode (disable progress meter)',
            '-v': '-v: verbose mode',
            '-C': '-C: enable compression',
            '-i': '-i: specify identity file (private key)',
            '-l': '-l: limit bandwidth in Kbit/s',
            '-o': '-o: pass options to ssh',
            '-c': '-c: select cipher for encryption',
            '-F': '-F: specify ssh config file',
            '-4': '-4: use IPv4 addresses only',
            '-6': '-6: use IPv6 addresses only',
            '--help': '--help: show help information',
        }
    return None


@register_completion_schema('ping')
def _ping_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ping commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-c': 'count: stop after sending count packets',
            '-i': 'interval: wait interval seconds between sending packets',
            '-t': 'ttl: set IP Time to Live (TTL)',
            '-W': 'timeout: time to wait for response in seconds',
            '-s': 'packetsize: specify number of data bytes to send',
            '-q': 'quiet: quiet output (only summary)',
            '-v': 'verbose: verbose output',
            '-n': 'numeric: numeric output only (no DNS)',
            '-a': 'audible: audible ping',
            '-f': 'flood: flood ping (send packets as fast as possible)',
            '-4': 'use IPv4 only',
            '-6': 'use IPv6 only',
            '--help': 'display help message and exit',
        }
    return None


@register_completion_schema('tree')
def _tree_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for tree commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': 'all files: include hidden files',
            '-d': 'directories only: list directories only',
            '-L': 'level: descend only level directories deep',
            '-f': 'full path: print the full path prefix for each file',
            '-i': 'no indentation: do not print indentation lines',
            '-s': 'size: print size of each file in bytes',
            '-h': 'human-readable: print sizes in human-readable format',
            '-D': 'print date of last modification',
            '-p': 'permissions: print file type and permissions',
            '-u': 'username: print file owner or UID',
            '-g': 'group: print file group owner or GID',
            '-C': 'colorize: turn colorization on always',
            '-n': 'no color: turn colorization off always',
            '-I': 'pattern: do not list files that match the given pattern',
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('code')
def _code_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for VS Code commands."""
    # Check for flags or after subcommand position
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-n': 'force new instance of code',
            '--new-window': 'force new instance of code',
            '-r': 'force open file/folder in last active window',
            '--reuse-window': 'force open file/folder in last active window',
            '-g': 'open file at specified line and column (file:line:column)',
            '--goto': 'open file at specified line and column (file:line:column)',
            '-d': 'compare two files with each other (diff mode)',
            '--diff': 'compare two files with each other (diff mode)',
            '-a': 'add folders to last active window',
            '--add': 'add folders to last active window',
            '-w': 'wait for files to be closed before returning',
            '--wait': 'wait for files to be closed before returning',
            '--locale': 'set display language (locale) for VS Code session',
            '--user-data-dir': 'specify directory for user data',
            '--extensions-dir': 'specify directory for extensions',
            '--list-extensions': 'list installed extensions',
            '--install-extension': 'install extension by ID or VSIX file',
            '--uninstall-extension': 'uninstall extension by ID',
            '--disable-extensions': 'disable all installed extensions',
            '--help': 'show help message and exit',
            '--version': 'show version information and exit',
        }

    # Don't complete at position 0 - code takes files first, let files complete
    return None


@register_completion_schema('aider')
def _aider_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for aider commands."""
    # Only complete flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--model': 'specify model to use (e.g., gpt-4, gpt-3.5-turbo)',
            '--opus': 'use Claude Opus model',
            '--sonnet': 'use Claude Sonnet model',
            '--4-turbo': 'use GPT-4 Turbo model',
            '--4o': 'use GPT-4o model',
            '--mini': 'use GPT-4o-mini model',
            '--deepseek': 'use DeepSeek model',
            '--message': 'specify message to send to aider',
            '-m': 'specify message to send to aider',
            '--yes': 'always say yes to confirmation prompts',
            '-y': 'always say yes to confirmation prompts',
            '--auto-commits': 'automatically commit changes',
            '--no-auto-commits': 'disable automatic commits',
            '--dirty-commits': 'allow commits with dirty repository',
            '--dry-run': 'perform dry run without making changes',
            '--map-tokens': 'specify tokens for repository map',
            '--edit-format': 'specify edit format (whole, diff, udiff)',
            '--architect': 'use architect mode for high-level design',
            '--help': 'show help message and exit',
            '--version': 'show version information and exit',
        }

    return None


def _get_signal_list():
    """Return list of common signals for kill/killall."""
    return ['SIGTERM', 'SIGKILL', 'SIGHUP', 'SIGINT', 'SIGQUIT', 'SIGSTOP',
            'SIGCONT', 'SIGUSR1', 'SIGUSR2', '1', '2', '3', '6', '9', '15']


@register_completion_schema('kill')
def _kill_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for kill commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-s': '-s/--signal: specify signal to send',
            '--signal': '--signal/-s: specify signal to send',
            '-l': '-l/--list: list signal names',
            '--list': '--list/-l: list signal names',
            '--help': 'display help message and exit',
        }

    # At position 1 (after 'kill'), if not a flag, show signals
    if cursor_token_idx == 1 and not _is_flag_context(tokens, cursor_token_idx, is_after):
        return _get_signal_list()

    return None


@register_completion_schema('killall')
def _killall_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for killall commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-s': '-s/--signal: specify signal to send',
            '--signal': '--signal/-s: specify signal to send',
            '-l': '-l/--list: list signal names',
            '--list': '--list/-l: list signal names',
            '--help': 'display help message and exit',
        }

    # At position 1 (after 'killall'), if not a flag, show signals
    if cursor_token_idx == 1 and not _is_flag_context(tokens, cursor_token_idx, is_after):
        return _get_signal_list()

    return None


# ============================================================================
# Group A: File Operation Commands
# ============================================================================

@register_completion_schema('fd')
def _fd_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for fd command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-t': '-t/--type: filter by type (f=file, d=directory, l=symlink, etc)',
            '--type': '--type/-t: filter by type (f=file, d=directory, l=symlink, etc)',
            '-e': '-e/--extension: filter by file extension',
            '--extension': '--extension/-e: filter by file extension',
            '-d': '-d/--max-depth: set maximum search depth',
            '--max-depth': '--max-depth/-d: set maximum search depth',
            '-H': '-H/--hidden: search hidden files and directories',
            '--hidden': '--hidden/-H: search hidden files and directories',
            '-I': '-I/--no-ignore: do not respect .(git|fd)ignore files',
            '--no-ignore': '--no-ignore/-I: do not respect .(git|fd)ignore files',
            '-L': '-L/--follow: follow symbolic links',
            '--follow': '--follow/-L: follow symbolic links',
            '-p': '-p/--absolute-path: show absolute instead of relative paths',
            '--absolute-path': '--absolute-path/-p: show absolute instead of relative paths',
            '-g': '-g/--glob: use glob-based search pattern',
            '--glob': '--glob/-g: use glob-based search pattern',
            '-x': '-x/--exec: execute command for each search result',
            '--exec': '--exec/-x: execute command for each search result',
            '-X': '-X/--exec-batch: execute command with all search results at once',
            '--exec-batch': '--exec-batch/-X: execute command with all search results at once',
            '-E': '-E/--exclude: exclude entries matching pattern',
            '--exclude': '--exclude/-E: exclude entries matching pattern',
            '-i': '-i/--ignore-case: case-insensitive search',
            '--ignore-case': '--ignore-case/-i: case-insensitive search',
            '-s': '-s/--case-sensitive: case-sensitive search',
            '--case-sensitive': '--case-sensitive/-s: case-sensitive search',
            '-F': '-F/--fixed-strings: treat pattern as literal string',
            '--fixed-strings': '--fixed-strings/-F: treat pattern as literal string',
            '--no-ignore-vcs': '--no-ignore-vcs: do not respect .gitignore files',
            '--no-ignore-parent': '--no-ignore-parent: do not respect ignore files in parent directories',
            '-u': '-u/--unrestricted: alias for --no-ignore --hidden',
            '--unrestricted': '--unrestricted/-u: alias for --no-ignore --hidden',
            '-c': '-c/--color: when to use colors (never, auto, always)',
            '--color': '--color/-c: when to use colors (never, auto, always)',
            '-j': '-j/--threads: set number of threads to use for searching',
            '--threads': '--threads/-j: set number of threads to use for searching',
            '--max-results': '--max-results: limit number of search results',
            '--changed-within': '--changed-within: filter by file modification time (newer than)',
            '--changed-before': '--changed-before: filter by file modification time (older than)',
            '--size': '--size: filter by file size',
            '--owner': '--owner: filter by owning user and/or group',
            '--base-directory': '--base-directory: change current working directory',
            '--path-separator': '--path-separator: set path separator when printing file paths',
            '--search-path': '--search-path: provide paths to search as alternative to positional path argument',
            '-0': '-0/--print0: separate results by null character',
            '--print0': '--print0/-0: separate results by null character',
            '--prune': '--prune: do not traverse into matching directories',
            '--strip-cwd-prefix': '--strip-cwd-prefix: strip ./ prefix when output is a terminal',
            '--one-file-system': '--one-file-system: do not cross file system boundaries',
            '--help': '--help: show help information',
            '--version': '--version: show version information',
        }
    return None


@register_completion_schema('ln')
def _ln_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ln command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-s': '-s/--symbolic: create symbolic links instead of hard links',
            '--symbolic': '--symbolic/-s: create symbolic links instead of hard links',
            '-f': '-f/--force: remove existing destination files',
            '--force': '--force/-f: remove existing destination files',
            '-n': '-n/--no-dereference: treat destination that is symlink to directory as normal file',
            '--no-dereference': '--no-dereference/-n: treat destination that is symlink to directory as normal file',
            '-v': '-v/--verbose: print name of each linked file',
            '--verbose': '--verbose/-v: print name of each linked file',
            '-i': '-i/--interactive: prompt whether to remove destinations',
            '--interactive': '--interactive/-i: prompt whether to remove destinations',
            '-b': '-b/--backup: make backup of each existing destination file',
            '--backup': '--backup/-b: make backup of each existing destination file',
            '-S': '-S/--suffix: override usual backup suffix',
            '--suffix': '--suffix/-S: override usual backup suffix',
            '-t': '-t/--target-directory: specify directory in which to create links',
            '--target-directory': '--target-directory/-t: specify directory in which to create links',
            '-T': '-T/--no-target-directory: treat destination as normal file',
            '--no-target-directory': '--no-target-directory/-T: treat destination as normal file',
            '-r': '-r/--relative: create symbolic links relative to link location',
            '--relative': '--relative/-r: create symbolic links relative to link location',
            '-L': '-L/--logical: dereference targets that are symbolic links',
            '--logical': '--logical/-L: dereference targets that are symbolic links',
            '-P': '-P/--physical: make hard links directly to symbolic links',
            '--physical': '--physical/-P: make hard links directly to symbolic links',
            '--help': '--help: show help information',
            '--version': '--version: show version information',
        }
    return None


@register_completion_schema('cat')
def _cat_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for cat command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-n': '-n/--number: number all output lines',
            '--number': '--number/-n: number all output lines',
            '-b': '-b/--number-nonblank: number non-empty output lines',
            '--number-nonblank': '--number-nonblank/-b: number non-empty output lines',
            '-s': '-s/--squeeze-blank: suppress repeated empty output lines',
            '--squeeze-blank': '--squeeze-blank/-s: suppress repeated empty output lines',
            '-v': '-v/--show-nonprinting: use ^ and M- notation, except for LFD and TAB',
            '--show-nonprinting': '--show-nonprinting/-v: use ^ and M- notation, except for LFD and TAB',
            '-E': '-E/--show-ends: display $ at end of each line',
            '--show-ends': '--show-ends/-E: display $ at end of each line',
            '-T': '-T/--show-tabs: display TAB characters as ^I',
            '--show-tabs': '--show-tabs/-T: display TAB characters as ^I',
            '-A': '-A/--show-all: equivalent to -vET',
            '--show-all': '--show-all/-A: equivalent to -vET',
            '-e': 'equivalent to -vE',
            '-t': 'equivalent to -vT',
            '-u': 'ignored (for POSIX compatibility)',
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('cp')
def _cp_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for cp command with helpful descriptions."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-r': '-r/-R/--recursive: copy directories recursively',
            '-R': '-R/-r/--recursive: copy directories recursively',
            '--recursive': '--recursive/-r/-R: copy directories recursively',
            '-a': '-a/--archive: archive mode: copy recursively and preserve all attributes',
            '--archive': '--archive/-a: archive mode: copy recursively and preserve all attributes',
            '-f': '-f/--force: force: overwrite without prompting',
            '--force': '--force/-f: force: overwrite without prompting',
            '-i': '-i/--interactive: prompt before overwriting files',
            '--interactive': '--interactive/-i: prompt before overwriting files',
            '-n': '-n/--no-clobber: never overwrite existing files',
            '--no-clobber': '--no-clobber/-n: never overwrite existing files',
            '-v': '-v/--verbose: verbose: show files being copied',
            '--verbose': '--verbose/-v: verbose: show files being copied',
            '-p': '-p/--preserve: preserve file attributes (mode, ownership, timestamps)',
            '--preserve': '--preserve/-p: preserve file attributes (mode, ownership, timestamps)',
            '-L': '-L/--dereference: follow symbolic links in source',
            '--dereference': '--dereference/-L: follow symbolic links in source',
            '-P': '-P/--no-dereference: never follow symbolic links',
            '--no-dereference': '--no-dereference/-P: never follow symbolic links',
            '-H': 'follow command-line symbolic links',
            '-d': 'copy symlinks as symlinks, not the files they point to',
            '--no-preserve': 'do not preserve specified attributes',
            '-u': '-u/--update: copy only when source is newer or destination is missing',
            '--update': '--update/-u: copy only when source is newer or destination is missing',
            '-x': '-x/--one-file-system: stay on this file system',
            '--one-file-system': '--one-file-system/-x: stay on this file system',
            '-b': '-b/--backup: make backup of each existing destination file',
            '--backup': '--backup/-b: make backup of each existing destination file',
            '-S': '-S/--suffix: override the usual backup suffix',
            '--suffix': '--suffix/-S: override the usual backup suffix',
            '-t': '-t/--target-directory: copy all source arguments into directory',
            '--target-directory': '--target-directory/-t: copy all source arguments into directory',
            '-T': '-T/--no-target-directory: treat destination as a normal file',
            '--no-target-directory': '--no-target-directory/-T: treat destination as a normal file',
            '-l': '-l/--link: hard link files instead of copying',
            '--link': '--link/-l: hard link files instead of copying',
            '-s': '-s/--symbolic-link: make symbolic links instead of copying',
            '--symbolic-link': '--symbolic-link/-s: make symbolic links instead of copying',
            '--attributes-only': 'copy only file attributes, not data',
            '--copy-contents': 'copy contents of special files when recursive',
            '--parents': 'use full source file name under directory',
            '--reflink': 'perform lightweight copy-on-write copy',
            '--sparse': 'control creation of sparse files',
            '--strip-trailing-slashes': 'remove trailing slashes from source arguments',
            '-Z': '-Z/--context: set SELinux security context of destination',
            '--context': '--context/-Z: set SELinux security context of destination',
            '--help': 'display help message',
            '--version': 'output version information',
        }
    return _complete_paths(tokens, cursor_token_idx, is_after)


@register_completion_schema('mv')
def _mv_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for mv command with helpful descriptions."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-f': '-f/--force: force: overwrite without prompting',
            '--force': '--force/-f: force: overwrite without prompting',
            '-i': '-i/--interactive: prompt before overwriting files',
            '--interactive': '--interactive/-i: prompt before overwriting files',
            '-n': '-n/--no-clobber: never overwrite existing files',
            '--no-clobber': '--no-clobber/-n: never overwrite existing files',
            '-v': '-v/--verbose: verbose: show files being moved',
            '--verbose': '--verbose/-v: verbose: show files being moved',
            '-u': '-u/--update: move only when source is newer or destination is missing',
            '--update': '--update/-u: move only when source is newer or destination is missing',
            '-b': '-b/--backup: make backup of each existing destination file',
            '--backup': '--backup/-b: make backup of each existing destination file',
            '-S': '-S/--suffix: override the usual backup suffix',
            '--suffix': '--suffix/-S: override the usual backup suffix',
            '-t': '-t/--target-directory: move all source arguments into directory',
            '--target-directory': '--target-directory/-t: move all source arguments into directory',
            '-T': '-T/--no-target-directory: treat destination as a normal file',
            '--no-target-directory': '--no-target-directory/-T: treat destination as a normal file',
            '--strip-trailing-slashes': 'remove trailing slashes from source arguments',
            '-Z': '-Z/--context: set SELinux security context of destination',
            '--context': '--context/-Z: set SELinux security context of destination',
            '--help': 'display help message',
            '--version': 'output version information',
        }
    return _complete_paths(tokens, cursor_token_idx, is_after)


@register_completion_schema('rm')
def _rm_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for rm command with helpful descriptions."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-r': '-r/-R/--recursive: remove directories and their contents recursively',
            '-R': '-R/-r/--recursive: remove directories and their contents recursively',
            '--recursive': '--recursive/-r/-R: remove directories and their contents recursively',
            '-f': '-f/--force: force: ignore nonexistent files, never prompt',
            '--force': '--force/-f: force: ignore nonexistent files, never prompt',
            '-i': '-i/--interactive: prompt before every removal',
            '--interactive': '--interactive/-i: prompt before every removal',
            '-I': 'prompt once before removing more than 3 files',
            '--interactive=once': 'prompt once before removing more than 3 files',
            '-v': '-v/--verbose: verbose: show files being removed',
            '--verbose': '--verbose/-v: verbose: show files being removed',
            '-d': '-d/--dir: remove empty directories',
            '--dir': '--dir/-d: remove empty directories',
            '--one-file-system': 'stay on the same file system when removing recursively',
            '--no-preserve-root': 'do not treat / specially (dangerous)',
            '--preserve-root': 'do not remove / (default)',
            '--help': 'display help message',
            '--version': 'output version information',
        }
    return _complete_paths(tokens, cursor_token_idx, is_after)


@register_completion_schema('touch')
def _touch_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for touch command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': 'change only the access time',
            '--time=atime': 'change only the access time',
            '--time=access': 'change only the access time',
            '--time=use': 'change only the access time',
            '-m': 'change only the modification time',
            '--time=mtime': 'change only the modification time',
            '--time=modify': 'change only the modification time',
            '-c': '-c/--no-create: do not create any files',
            '--no-create': '--no-create/-c: do not create any files',
            '-t': 'use [[CC]YY]MMDDhhmm[.ss] instead of current time',
            '-d': '-d/--date: parse STRING and use it instead of current time',
            '--date': '--date/-d: parse STRING and use it instead of current time',
            '--time': 'change the specified time: atime, access, use, mtime, modify',
            '-r': '-r/--reference: use this file\'s times instead of current time',
            '--reference': '--reference/-r: use this file\'s times instead of current time',
            '-h': '-h/--no-dereference: affect symbolic links instead of referenced file',
            '--no-dereference': '--no-dereference/-h: affect symbolic links instead of referenced file',
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('mkdir')
def _mkdir_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for mkdir command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-p': '-p/--parents: create parent directories as needed, no error if existing',
            '--parents': '--parents/-p: create parent directories as needed, no error if existing',
            '-m': '-m/--mode: set file mode (as in chmod), not a=rwx - umask',
            '--mode': '--mode/-m: set file mode (as in chmod), not a=rwx - umask',
            '-v': '-v/--verbose: print a message for each created directory',
            '--verbose': '--verbose/-v: print a message for each created directory',
            '-Z': '-Z/--context: set SELinux security context to default type',
            '--context': '--context/-Z: set SELinux security context to default type',
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('rmdir')
def _rmdir_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for rmdir command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-p': '-p/--parents: remove DIRECTORY and its ancestors (e.g., rmdir -p a/b/c)',
            '--parents': '--parents/-p: remove DIRECTORY and its ancestors (e.g., rmdir -p a/b/c)',
            '-v': '-v/--verbose: output a diagnostic for every directory processed',
            '--verbose': '--verbose/-v: output a diagnostic for every directory processed',
            '--ignore-fail-on-non-empty': 'ignore each failure from non-empty directory',
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('tail')
def _tail_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for tail command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-n': '-n/--lines: output the last NUM lines (default 10)',
            '--lines': '--lines/-n: output the last NUM lines (default 10)',
            '-f': '-f/--follow: output appended data as the file grows',
            '--follow': '--follow/-f: output appended data as the file grows',
            '-F': 'same as --follow=name --retry',
            '-c': '-c/--bytes: output the last NUM bytes',
            '--bytes': '--bytes/-c: output the last NUM bytes',
            '-q': '-q/--quiet/--silent: never output headers giving file names',
            '--quiet': '--quiet/-q/--silent: never output headers giving file names',
            '--silent': '--silent/-q/--quiet: never output headers giving file names',
            '-v': '-v/--verbose: always output headers giving file names',
            '--verbose': '--verbose/-v: always output headers giving file names',
            '-s': '-s/--sleep-interval: sleep for approximately NUM seconds between iterations',
            '--sleep-interval': '--sleep-interval/-s: sleep for approximately NUM seconds between iterations',
            '--max-unchanged-stats': 'reopen file which has not changed after NUM iterations',
            '--pid': 'with -f, terminate after process ID, PID dies',
            '--retry': 'keep trying to open a file even if it is inaccessible',
            '-z': '-z/--zero-terminated: line delimiter is NUL, not newline',
            '--zero-terminated': '--zero-terminated/-z: line delimiter is NUL, not newline',
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('ls')
def _ls_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ls command with helpful descriptions."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': '-a/--all: show all files including hidden (. and ..)',
            '--all': '--all/-a: show all files including hidden (. and ..)',
            '-A': '-A/--almost-all: show almost all (exclude . and ..)',
            '--almost-all': '--almost-all/-A: show almost all (exclude . and ..)',
            '-l': 'long format with details',
            '-h': '-h/--human-readable: human-readable sizes (1K, 234M, 2G)',
            '--human-readable': '--human-readable/-h: human-readable sizes (1K, 234M, 2G)',
            '-r': '-r/--reverse: reverse order while sorting',
            '--reverse': '--reverse/-r: reverse order while sorting',
            '-t': 'sort by modification time, newest first',
            '--sort=time': 'sort by modification time',
            '-S': 'sort by file size, largest first',
            '--sort=size': 'sort by file size',
            '-R': '-R/--recursive: list subdirectories recursively',
            '--recursive': '--recursive/-R: list subdirectories recursively',
            '-1': 'list one file per line',
            '-d': '-d/--directory: list directories themselves, not contents',
            '--directory': '--directory/-d: list directories themselves, not contents',
            '-G': '-G/--no-group: do not print group names',
            '--no-group': '--no-group/-G: do not print group names',
            '-F': '-F/--classify: append indicator (*/=>@|) to entries',
            '--classify': '--classify/-F: append indicator (*/=>@|) to entries',
            '-i': '-i/--inode: print inode number of each file',
            '--inode': '--inode/-i: print inode number of each file',
            '-s': '-s/--size: print allocated size of each file',
            '--size': '--size/-s: print allocated size of each file',
            '-L': '-L/--dereference: follow symbolic links',
            '--dereference': '--dereference/-L: follow symbolic links',
            '-H': '-H/--dereference-command-line: follow symlinks on command line',
            '--dereference-command-line': '--dereference-command-line/-H: follow symlinks on command line',
            '-p': 'append / indicator to directories',
            '-n': '-n/--numeric-uid-gid: numeric user and group IDs',
            '--numeric-uid-gid': '--numeric-uid-gid/-n: numeric user and group IDs',
            '-o': 'long format without group info',
            '-g': 'long format without owner info',
            '--author': 'print author of each file',
            '-c': 'sort by ctime (status change time)',
            '-u': 'sort by atime (access time)',
            '--color': 'colorize the output',
            '--hide': 'do not list implied entries matching pattern',
            '--ignore': 'do not list implied entries matching pattern',
            '-I': 'do not list implied entries matching pattern',
            '-k': '-k/--kibibytes: use 1024-byte blocks',
            '--kibibytes': '--kibibytes/-k: use 1024-byte blocks',
            '-m': 'comma-separated list',
            '-x': 'list entries by lines instead of columns',
            '-X': 'sort alphabetically by extension',
            '--sort': 'sort by WORD: none, size, time, version, extension',
            '-T': 'set tab stops to COLS instead of 8',
            '--tabsize': 'set tab size in columns',
            '-w': 'set output width to COLS',
            '--width': 'set output width in columns',
            '--full-time': 'show full date and time',
            '--time': 'select time: atime, access, use, ctime, status',
            '--time-style': 'time/date format: full-iso, long-iso, iso, locale',
            '--format': 'output format: across, commas, horizontal, long, single-column, verbose, vertical',
            '--quoting-style': 'quoting style: literal, locale, shell, shell-always, shell-escape, c, escape',
            '--indicator-style': 'indicator style: none, slash, file-type, classify',
            '--hyperlink': 'hyperlink file names',
            '--block-size': 'scale sizes by SIZE before printing',
            '--context': '--context/-Z: print security context of each file',
            '-Z': '-Z/--context: print security context of each file',
            '--help': 'display this help and exit',
            '--version': 'output version information and exit'
        }
    return _complete_paths(tokens, cursor_token_idx, is_after)


@register_completion_schema('echo')
def _echo_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for echo command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-n': 'do not output trailing newline',
            '-e': 'enable interpretation of backslash escapes',
            '-E': 'disable interpretation of backslash escapes (default)',
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('diff')
def _diff_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for diff command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-u': '-u/--unified: unified diff format (default 3 lines context)',
            '--unified': '--unified/-u: unified diff format (default 3 lines context)',
            '-c': '-c/--context: context diff format (default 3 lines)',
            '--context': '--context/-c: context diff format (default 3 lines)',
            '-r': '-r/--recursive: recursively compare subdirectories',
            '--recursive': '--recursive/-r: recursively compare subdirectories',
            '-N': '-N/--new-file: treat absent files as empty',
            '--new-file': '--new-file/-N: treat absent files as empty',
            '-q': '-q/--brief: report only whether files differ',
            '--brief': '--brief/-q: report only whether files differ',
            '-s': '-s/--report-identical-files: report when files are identical',
            '--report-identical-files': '--report-identical-files/-s: report when files are identical',
            '-i': '-i/--ignore-case: ignore case differences',
            '--ignore-case': '--ignore-case/-i: ignore case differences',
            '-w': '-w/--ignore-all-space: ignore all whitespace',
            '--ignore-all-space': '--ignore-all-space/-w: ignore all whitespace',
            '-b': '-b/--ignore-space-change: ignore changes in whitespace amount',
            '--ignore-space-change': '--ignore-space-change/-b: ignore changes in whitespace amount',
            '-B': '-B/--ignore-blank-lines: ignore blank line changes',
            '--ignore-blank-lines': '--ignore-blank-lines/-B: ignore blank line changes',
            '-E': '-E/--ignore-tab-expansion: ignore tab expansion changes',
            '--ignore-tab-expansion': '--ignore-tab-expansion/-E: ignore tab expansion changes',
            '-Z': '-Z/--ignore-trailing-space: ignore trailing whitespace',
            '--ignore-trailing-space': '--ignore-trailing-space/-Z: ignore trailing whitespace',
            '-a': '-a/--text: treat all files as text',
            '--text': '--text/-a: treat all files as text',
            '-y': '-y/--side-by-side: output in two columns',
            '--side-by-side': '--side-by-side/-y: output in two columns',
            '-W': '-W/--width: set output width for side-by-side',
            '--width': '--width/-W: set output width for side-by-side',
            '-p': '-p/--show-c-function: show which C function each change is in',
            '--show-c-function': '--show-c-function/-p: show which C function each change is in',
            '-F': '-F/--show-function-line: show most recent matching line',
            '--show-function-line': '--show-function-line/-F: show most recent matching line',
            '-l': '-l/--paginate: pass output through pr for pagination',
            '--paginate': '--paginate/-l: pass output through pr for pagination',
            '-t': '-t/--expand-tabs: expand tabs to spaces in output',
            '--expand-tabs': '--expand-tabs/-t: expand tabs to spaces in output',
            '-T': '-T/--initial-tab: prepend tab to align tabs properly',
            '--initial-tab': '--initial-tab/-T: prepend tab to align tabs properly',
            '--suppress-common-lines': 'do not output common lines in side-by-side',
            '--suppress-blank-empty': 'suppress space/tab before empty output lines',
            '-d': '-d/--minimal: try hard to find smaller set of changes',
            '--minimal': '--minimal/-d: try hard to find smaller set of changes',
            '--speed-large-files': 'assume large files with scattered small changes',
            '-e': '-e/--ed: output ed script',
            '--ed': '--ed/-e: output ed script',
            '-n': '-n/--rcs: output RCS format diff',
            '--rcs': '--rcs/-n: output RCS format diff',
            '--normal': 'output normal diff (default)',
            '--from-file': 'compare FILE to all operands (FILE can be directory)',
            '--to-file': 'compare all operands to FILE (FILE can be directory)',
            '-x': '-x/--exclude: exclude files matching pattern',
            '--exclude': '--exclude/-x: exclude files matching pattern',
            '-X': '-X/--exclude-from: exclude files matching patterns in file',
            '--exclude-from': '--exclude-from/-X: exclude files matching patterns in file',
            '-S': '-S/--starting-file: start with FILE when comparing directories',
            '--starting-file': '--starting-file/-S: start with FILE when comparing directories',
            '--horizon-lines': 'keep NUM lines of common prefix/suffix',
            '--line-format': 'format all input lines with LFMT',
            '--GTYPE-group-format': 'format GTYPE input groups with GFMT',
            '--LTYPE-line-format': 'format LTYPE input lines with LFMT',
            '--unchanged-line-format': 'format unchanged lines',
            '--old-line-format': 'format old (deleted) lines',
            '--new-line-format': 'format new (added) lines',
            '--unchanged-group-format': 'format unchanged groups',
            '--old-group-format': 'format old (deleted) groups',
            '--new-group-format': 'format new (added) groups',
            '--changed-group-format': 'format changed groups',
            '--color': 'colorize output (auto/never/always)',
            '--palette': 'colors to use when --color is active',
            '--label': 'use LABEL instead of filename in output',
            '--help': 'display help message',
            '--version': 'output version information',
        }
    return None


# ============================================================================
# Group D: System Utility Commands
# ============================================================================

@register_completion_schema('clear')
def _clear_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for clear command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('dd')
def _dd_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for dd command."""
    current = _get_current_token_text(tokens, cursor_token_idx)

    # If current token contains '=', we're completing a value
    if '=' in current:
        prefix = current.split('=')[0] + '='
        if prefix == 'status=':
            return ['status=none', 'status=noxfer', 'status=progress']
        elif prefix == 'conv=':
            return ['conv=notrunc', 'conv=noerror', 'conv=sync', 'conv=fsync']
        return None

    # Offer flags/operands
    return {
        'if=': 'if=FILE: read from FILE instead of stdin',
        'of=': 'of=FILE: write to FILE instead of stdout',
        'bs=': 'bs=BYTES: read and write BYTES bytes at a time',
        'count=': 'count=N: copy only N input blocks',
        'seek=': 'seek=N: skip N obs-sized blocks at start of output',
        'skip=': 'skip=N: skip N ibs-sized blocks at start of input',
        'status=': 'status=LEVEL: level of information to print to stderr',
        'conv=': 'conv=CONVS: convert the file as per comma-separated symbol list',
        'iflag=': 'iflag=FLAGS: read as per comma-separated symbol list',
        'oflag=': 'oflag=FLAGS: write as per comma-separated symbol list',
    }


@register_completion_schema('du')
def _du_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for du command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': 'all: write counts for all files, not just directories',
            '--all': 'all: write counts for all files, not just directories',
            '-h': 'human-readable: print sizes in human-readable format (e.g., 1K, 234M)',
            '--human-readable': 'human-readable: print sizes in human-readable format (e.g., 1K, 234M)',
            '-s': 'summarize: display only a total for each argument',
            '--summarize': 'summarize: display only a total for each argument',
            '-c': 'total: produce a grand total',
            '--total': 'total: produce a grand total',
            '-d': 'max-depth: print total for directory only if it is N or fewer levels',
            '--max-depth': 'max-depth: print total for directory only if it is N or fewer levels',
            '-x': 'one-file-system: skip directories on different file systems',
            '--one-file-system': 'one-file-system: skip directories on different file systems',
            '--exclude': 'exclude files that match PATTERN',
            '--time': 'show time of the last modification of any file or directory',
            '-L': 'dereference: dereference all symbolic links',
            '--dereference': 'dereference: dereference all symbolic links',
            '-P': "no-dereference: don't follow any symbolic links (default)",
            '--no-dereference': "no-dereference: don't follow any symbolic links (default)",
        }
    return None


@register_completion_schema('whoami')
def _whoami_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for whoami command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('pwd')
def _pwd_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for pwd command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-L': '-L/--logical: use PWD from environment, even if it contains symlinks',
            '--logical': '--logical/-L: use PWD from environment, even if it contains symlinks',
            '-P': '-P/--physical: avoid all symlinks (default)',
            '--physical': '--physical/-P: avoid all symlinks (default)',
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('top')
def _top_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for top command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': 'calculate and display all processes (not just top ones)',
            '-c': 'set event counting mode',
            '-d': 'calculate memory delta processes',
            '-e': 'generate events (for performance monitoring)',
            '-F': 'do not calculate statistics on shared libraries',
            '-h': 'print command line usage',
            '-i': 'set interval between samples (seconds)',
            '-l': 'set logging mode (samples)',
            '-n': 'set number of samples',
            '-o': 'specify sort order (pid, command, cpu, csw, etc.)',
            '-O': 'specify secondary sort order',
            '-p': 'accumulate per-process statistics',
            '-s': 'set delay between updates (seconds)',
            '-S': 'display global statistics',
            '-U': 'monitor processes owned by specified user',
            '-u': 'report CPU usage',
            '-stats': 'specify statistics to display',
        }
    return None


# ============================================================================
# Group B: Additional Development Tool Commands
# ============================================================================

@register_completion_schema('black')
def _black_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for black (Python formatter) commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--check': 'check if files would be reformatted without writing back',
            '--diff': 'show diffs for changes without writing back',
            '--color': 'show colored output (auto/always/never)',
            '--fast': 'skip AST safety checks (may result in incorrect code)',
            '--safe': 'ensure code is valid after formatting (default)',
            '--quiet': '--quiet/-q: suppress output',
            '-q': '-q/--quiet: suppress output',
            '--verbose': '--verbose/-v: show detailed output',
            '-v': '-v/--verbose: show detailed output',
            '--line-length': '--line-length/-l: max line length',
            '-l': '-l/--line-length: max line length',
            '--target-version': '--target-version/-t: Python version to target',
            '-t': '-t/--target-version: Python version to target',
            '--skip-string-normalization': '--skip-string-normalization/-S: do not normalize string quotes',
            '-S': '-S/--skip-string-normalization: do not normalize string quotes',
            '--exclude': 'files/directories to exclude',
            '--include': 'files/directories to include',
            '--force-exclude': 'forcefully exclude files matching pattern',
            '--help': 'show help message and exit',
            '--version': 'show version and exit',
            '--config': 'path to configuration file',
            '--code': 'format code passed as string',
            '--python-cell-magics': 'enable Python cell magic support',
            '--skip-magic-trailing-comma': 'skip adding trailing commas to magic methods',
            '--experimental-string-processing': 'enable experimental string processing',
            '--preview': 'enable preview style',
            '--pyi': 'treat file as stub file',
            '--ipynb': 'treat file as Jupyter notebook',
            '--required-version': 'require black version to match',
            '--workers': '--workers/-W: number of parallel workers',
            '-W': '-W/--workers: number of parallel workers',
        }
    return None


@register_completion_schema('cmake')
def _cmake_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for cmake commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-S': 'specify source directory',
            '-B': 'specify build directory',
            '-G': 'specify generator',
            '-D': 'create or update cache entry',
            '-U': 'remove matching entries from cache',
            '-C': 'pre-load cache script',
            '--build': 'build project',
            '--install': 'install project',
            '--open': 'open generated project',
            '--fresh': 'delete cache and rebuild',
            '--toolchain': 'specify toolchain file',
            '--preset': 'specify configure preset',
            '--list-presets': 'list available presets',
            '-N': 'view mode only',
            '-L': 'list non-advanced cache variables',
            '-LA': 'list all cache variables',
            '-LAH': 'list all cache variables with help',
            '--trace': 'trace cmake execution',
            '--trace-expand': 'trace with variable expansion',
            '--trace-format': 'set trace output format',
            '--trace-source': 'trace only specific files',
            '--trace-redirect': 'redirect trace output',
            '--warn-uninitialized': 'warn about uninitialized variables',
            '--warn-unused-vars': 'warn about unused variables',
            '--no-warn-unused-cli': 'do not warn about unused command line options',
            '--check-system-vars': 'check system variables',
            '--profiling-format': 'set profiling format',
            '--profiling-output': 'set profiling output file',
            '--help': 'show help message',
            '--version': 'show version',
            '--help-full': 'show full help',
            '--help-manual': 'show manual for topic',
            '--help-command': 'show command help',
            '--help-variable': 'show variable help',
            '--help-policy': 'show policy help',
            '--help-property': 'show property help',
            '--help-module': 'show module help',
        }
    return None




@register_completion_schema('bash')
def _bash_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for bash commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-c': 'execute commands from string',
            '-i': 'interactive shell',
            '-l': 'act as login shell',
            '-s': 'read commands from standard input',
            '-r': 'restricted shell',
            '-D': 'dump translatable strings',
            '-v': 'print shell input lines as they are read',
            '-x': 'print commands and arguments as they are executed',
            '-n': 'read commands but do not execute them',
            '-e': 'exit immediately if command exits with non-zero status',
            '-u': 'treat unset variables as error',
            '-f': 'disable filename expansion (globbing)',
            '-m': 'enable job control',
            '-p': 'privileged mode',
            '-t': 'exit after reading and executing one command',
            '-a': 'mark variables for export',
            '-b': 'notify of job termination immediately',
            '-B': 'perform brace expansion',
            '-C': 'prevent output redirection from overwriting files',
            '-E': 'inherit ERR trap in shell functions',
            '-H': 'enable ! style history substitution',
            '-P': 'do not follow symbolic links',
            '-T': 'inherit DEBUG and RETURN traps',
            '--noprofile': 'do not load profile files',
            '--norc': 'do not load .bashrc',
            '--rcfile': '--rcfile/--init-file: specify alternative rc file',
            '--login': '--login/-l: act as login shell',
            '--restricted': '--restricted/-r: restricted shell',
            '--verbose': '--verbose/-v: print shell input lines',
            '--xtrace': '--xtrace/-x: print commands as executed',
            '--noediting': 'disable readline editing',
            '--posix': 'conform to POSIX standard',
            '--debugger': 'enable debugger support',
            '--dump-strings': 'dump translatable strings in $"..." format',
            '--dump-po-strings': 'dump translatable strings in PO format',
            '--help': 'display help and exit',
            '--version': 'display version and exit',
            '--init-file': '--init-file/--rcfile: specify alternative rc file',
            '--pretty-print': 'pretty-print shell functions',
        }
    return None


@register_completion_schema('nano')
def _nano_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for nano (text editor) commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-h': '-h/--help: show help message and exit',
            '--help': '--help/-h: show help message and exit',
            '-v': '-v/--version: show version information',
            '--version': '--version/-v: show version information',
            '-B': '-B/--backup: save backups of existing files',
            '--backup': '--backup/-B: save backups of existing files',
            '-C': '-C/--backupdir: directory for saving backup files',
            '--backupdir': '--backupdir/-C: directory for saving backup files',
            '-D': '-D/--boldtext: use bold text instead of reverse video',
            '--boldtext': '--boldtext/-D: use bold text instead of reverse video',
            '-E': '-E/--tabstospaces: convert typed tabs to spaces',
            '--tabstospaces': '--tabstospaces/-E: convert typed tabs to spaces',
            '-F': '-F/--multibuffer: enable multiple file buffers',
            '--multibuffer': '--multibuffer/-F: enable multiple file buffers',
            '-G': '-G/--locking: use vim-style file locking',
            '--locking': '--locking/-G: use vim-style file locking',
            '-H': '-H/--historylog: save and reload search/replace history',
            '--historylog': '--historylog/-H: save and reload search/replace history',
            '-I': '-I/--ignorercfiles: ignore nanorc files',
            '--ignorercfiles': '--ignorercfiles/-I: ignore nanorc files',
            '-J': '-J/--guidestripe: show vertical guide stripe at column',
            '--guidestripe': '--guidestripe/-J: show vertical guide stripe at column',
            '-K': '-K/--rawsequences: fix numeric keypad key confusion',
            '--rawsequences': '--rawsequences/-K: fix numeric keypad key confusion',
            '-L': '-L/--nonewlines: do not add newlines to file ends',
            '--nonewlines': '--nonewlines/-L: do not add newlines to file ends',
            '-M': '-M/--trimblanks: trim trailing whitespace when hard-wrapping',
            '--trimblanks': '--trimblanks/-M: trim trailing whitespace when hard-wrapping',
            '-N': '-N/--noconvert: do not convert files from DOS/Mac format',
            '--noconvert': '--noconvert/-N: do not convert files from DOS/Mac format',
            '-O': '-O/--bookstyle: leading whitespace means new paragraph',
            '--bookstyle': '--bookstyle/-O: leading whitespace means new paragraph',
            '-P': '-P/--positionlog: save and restore cursor position',
            '--positionlog': '--positionlog/-P: save and restore cursor position',
            '-Q': '-Q/--quotestr: regular expression to match quoting',
            '--quotestr': '--quotestr/-Q: regular expression to match quoting',
            '-R': '-R/--restricted: restricted mode',
            '--restricted': '--restricted/-R: restricted mode',
            '-S': '-S/--softwrap: enable soft wrapping of overlong lines',
            '--softwrap': '--softwrap/-S: enable soft wrapping of overlong lines',
            '-T': '-T/--tabsize: set tab width in columns',
            '--tabsize': '--tabsize/-T: set tab width in columns',
            '-U': '-U/--quickblank: do one-line status bar blanking',
            '--quickblank': '--quickblank/-U: do one-line status bar blanking',
            '-V': '-V/--stateflags: show state flags in title bar',
            '--stateflags': '--stateflags/-V: show state flags in title bar',
            '-W': '-W/--wordbounds: detect word boundaries more accurately',
            '--wordbounds': '--wordbounds/-W: detect word boundaries more accurately',
            '-X': '-X/--wordchars: which characters are word parts',
            '--wordchars': '--wordchars/-X: which characters are word parts',
            '-Y': '-Y/--syntax: syntax highlighting definition to use',
            '--syntax': '--syntax/-Y: syntax highlighting definition to use',
            '-Z': '-Z/--zap: let Backspace and Delete erase marked region',
            '--zap': '--zap/-Z: let Backspace and Delete erase marked region',
            '-a': '-a/--atblanks: wrap lines at whitespace',
            '--atblanks': '--atblanks/-a: wrap lines at whitespace',
            '-b': '-b/--breaklonglines: automatically hard-wrap overlong lines',
            '--breaklonglines': '--breaklonglines/-b: automatically hard-wrap overlong lines',
            '-c': '-c/--constantshow: constantly show cursor position',
            '--constantshow': '--constantshow/-c: constantly show cursor position',
            '-d': '-d/--rebinddelete: fix Backspace/Delete key confusion',
            '--rebinddelete': '--rebinddelete/-d: fix Backspace/Delete key confusion',
            '-e': '-e/--emptyline: keep line below title bar empty',
            '--emptyline': '--emptyline/-e: keep line below title bar empty',
            '-f': '-f/--rcfile: use only this file for configuration',
            '--rcfile': '--rcfile/-f: use only this file for configuration',
            '-g': '-g/--showcursor: show cursor in file browser and help',
            '--showcursor': '--showcursor/-g: show cursor in file browser and help',
            '-i': '-i/--autoindent: automatically indent new lines',
            '--autoindent': '--autoindent/-i: automatically indent new lines',
            '-j': '-j/--jumpyscrolling: scroll per half-screen instead of per line',
            '--jumpyscrolling': '--jumpyscrolling/-j: scroll per half-screen instead of per line',
            '-k': '-k/--cutfromcursor: cut from cursor to end of line',
            '--cutfromcursor': '--cutfromcursor/-k: cut from cursor to end of line',
            '-l': '-l/--linenumbers: show line numbers in front of text',
            '--linenumbers': '--linenumbers/-l: show line numbers in front of text',
            '-m': '-m/--mouse: enable mouse support',
            '--mouse': '--mouse/-m: enable mouse support',
            '-n': '-n/--noread: do not read file (only write)',
            '--noread': '--noread/-n: do not read file (only write)',
            '-o': '-o/--operatingdir: set operating directory',
            '--operatingdir': '--operatingdir/-o: set operating directory',
            '-p': '-p/--preserve: preserve XON/XOFF keys',
            '--preserve': '--preserve/-p: preserve XON/XOFF keys',
            '-q': '-q/--indicator: show position+portion indicator',
            '--indicator': '--indicator/-q: show position+portion indicator',
            '-r': '-r/--restricted: restricted mode (duplicate of -R)',
            '-s': '-s/--speller: use alternative spell checker',
            '--speller': '--speller/-s: use alternative spell checker',
            '-t': '-t/--saveonexit: save changes on exit, do not prompt',
            '--saveonexit': '--saveonexit/-t: save changes on exit, do not prompt',
            '-u': '-u/--unix: save file in Unix format',
            '--unix': '--unix/-u: save file in Unix format',
            '-w': '-w/--nowrap: do not hard-wrap long lines',
            '--nowrap': '--nowrap/-w: do not hard-wrap long lines',
            '-x': '-x/--nohelp: do not show help lines',
            '--nohelp': '--nohelp/-x: do not show help lines',
            '-y': '-y/--afterends: make Ctrl+Right stop at word ends',
            '--afterends': '--afterends/-y: make Ctrl+Right stop at word ends',
            '-z': '-z/--suspend: enable suspension',
            '--suspend': '--suspend/-z: enable suspension',
            '-$': 'same as -S/--softwrap',
            '-%': 'same as -V/--stateflags',
            '-_': '-_/--minibar: show minibar at bottom instead of title bar',
            '--minibar': '--minibar/-_: show minibar at bottom instead of title bar',
            '-0': '-0/--zero: hide all bars and use whole terminal',
            '--zero': '--zero/-0: hide all bars and use whole terminal',
        }
    return None


@register_completion_schema('micro')
def _micro_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for micro (text editor) commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-version': 'show version information',
            '-config-dir': 'show configuration directory and exit',
            '-options': 'show all option values and exit',
            '-debug': 'enable debug mode (creates log file)',
            '-plugin': 'plugin command (install, remove, update, available, list)',
            '-clean': 'clean configuration directory',
            '-help': 'show help message and exit',
            '-startpos': 'start at specified line and column (LINE:COL or LINE)',
            '-filetype': 'set filetype for syntax highlighting',
            '-readonly': 'open file in read-only mode',
        }
    return None


@register_completion_schema('which')
def _which_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for which commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': '-a/--all: print all matching executables',
            '--all': '--all/-a: print all matching executables',
            '-s': '-s/--silent: silent mode, no output',
            '--silent': '--silent/-s: silent mode, no output',
            '--help': 'show help message',
            '--version': 'show version information',
        }
    return None


# ============================================================================
# Group E: Advanced Tool Commands
# ============================================================================

# @register_completion_schema('rclone')
# def _rclone_completions(tokens, cursor_token_idx, is_after):
#     """Completion schema for rclone commands."""
#     # Check for flags
#     if _is_flag_context(tokens, cursor_token_idx, is_after):
#         return {
#             '--help': '--help/-h: show help',
#             '-h': '-h/--help: show help',
#             '--version': '--version/-V: show version',
#             '-V': '-V/--version: show version',
#             '--config': 'path to config file',
#             '--dry-run': '--dry-run/-n: perform trial run without making changes',
#             '-n': '-n/--dry-run: perform trial run without making changes',
#             '--verbose': '--verbose/-v: verbose output',
#             '-v': '-v/--verbose: verbose output',
#             '--quiet': '--quiet/-q: quiet mode',
#             '-q': '-q/--quiet: quiet mode',
#             '--progress': '--progress/-P: show progress',
#             '-P': '-P/--progress: show progress',
#             '--transfers': 'number of file transfers to run in parallel',
#             '--checkers': 'number of checkers to run in parallel',
#             '--bwlimit': 'bandwidth limit in KBytes/s',
#             '--exclude': 'exclude files matching pattern',
#             '--include': 'include files matching pattern',
#         }
#
#     # Subcommands at position 0
#     result = _complete_at_position_zero(cursor_token_idx, is_after, {
#         'copy': 'copy files from source to dest',
#         'sync': 'make source and dest identical',
#         'move': 'move files from source to dest',
#         'delete': 'remove files in path',
#         'purge': 'remove path and all contents',
#         'mkdir': 'make directory',
#         'rmdir': 'remove directory',
#         'ls': 'list objects in path',
#         'lsl': 'list objects with size and modification time',
#         'lsd': 'list all directories in path',
#         'lsf': 'list objects with formatting',
#         'mount': 'mount remote as file system',
#         'cat': 'concatenate files and send to stdout',
#         'size': 'print total size of objects in path',
#         'check': 'check files for corruption',
#         'md5sum': 'produce md5sum file',
#         'sha1sum': 'produce sha1sum file',
#         'copyto': 'copy files from source to dest without creating directory',
#         'moveto': 'move file or directory from source to dest',
#         'copyurl': 'copy url content to dest',
#         'serve': 'serve remote over protocol',
#         'config': 'enter interactive configuration',
#         'genautocomplete': 'generate shell autocomplete script',
#         'about': 'get quota information',
#         'authorize': 'remote authorization',
#         'cleanup': 'clean up remote',
#         'dedupe': 'interactively find duplicate files',
#         'link': 'generate public link to file/folder',
#         'listremotes': 'list configured remotes',
#         'tree': 'list contents in tree format',
#         'ncdu': 'explore remote with text UI',
#         'rcat': 'copy stdin to file on remote',
#         'rcd': 'run rclone daemon',
#         'selfupdate': 'update rclone binary',
#         'test': 'run test subcommand',
#         'touch': 'create new file or update timestamp',
#         'version': 'show version',
#     })
#     if result:
#         return result
#     return None
#
#
@register_completion_schema('qpdf')
def _qpdf_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for qpdf commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': 'show help message',
            '--version': 'show version information',
            '--linearize': 'linearize (web-optimize) PDF',
            '--encrypt': 'encrypt PDF with password',
            '--decrypt': 'decrypt PDF',
            '--password': 'specify password for encrypted PDF',
            '--pages': 'select pages from one or more input files',
            '--rotate': 'rotate pages',
            '--split-pages': 'split PDF into separate files',
            '--overlay': 'overlay pages from another file',
            '--underlay': 'underlay pages from another file',
            '--collate': 'collate rather than concatenate pages',
            '--flatten-annotations': 'flatten annotations',
            '--generate-appearances': 'generate appearance streams',
            '--optimize-images': 'optimize images',
            '--compress-streams': 'compress streams',
            '--recompress-flate': 'recompress flate streams',
            '--compression-level': 'set compression level',
            '--object-streams': 'control object streams',
            '--preserve-unreferenced': 'preserve unreferenced objects',
            '--remove-unreferenced-resources': 'remove unreferenced resources',
            '--keep-files-open': 'keep files open during processing',
            '--keep-files-open-threshold': 'threshold for keeping files open',
        }
    return None


@register_completion_schema('open')
def _open_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for macOS open commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': 'specify application to use for opening file',
            '-e': 'open file with TextEdit',
            '-t': 'open file with default text editor',
            '-f': 'read input from standard input and open with default text editor',
            '-F': 'open application in fresh state (do not restore windows)',
            '-W': 'wait for application to exit before returning',
            '-R': 'reveal file in Finder instead of opening',
            '-n': 'open new instance of application even if one is already running',
            '-g': 'do not bring application to foreground',
            '-j': 'launch application hidden',
            '-h': 'search for file using header information',
            '--args': 'pass remaining arguments to application',
            '--env': 'set environment variable for application',
            '--stdin': 'pass stdin to application',
            '--stdout': 'redirect stdout from application',
            '--stderr': 'redirect stderr from application',
            '--fresh': 'launch application in fresh state',
            '--new': 'open new instance of application',
            '--reveal': 'reveal file in Finder',
            '--background': 'do not bring application to foreground',
            '--hide': 'launch application hidden',
            '--wait-apps': 'wait for applications to exit',
            '--help': 'show help message and exit',
        }
    return None


@register_completion_schema('man')
def _man_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for man commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': 'display all matching manual pages',
            '-d': 'print debugging information',
            '-D': 'display and print debugging information',
            '-f': 'equivalent to whatis',
            '-F': 'show only the manual page file location',
            '-k': 'equivalent to apropos',
            '-K': 'search for text in all pages',
            '-l': 'treat argument as local filename',
            '-t': 'format page for printing using groff',
            '-w': 'print location of manual page',
            '-W': 'print location of cat page or source file',
            '-P': 'specify pager program',
            '-S': '-S/-s: colon-separated list of sections',
            '-s': '-s/-S: colon-separated list of sections',
            '-M': 'specify search path for manual pages',
            '--help': 'show help message',
            '--usage': 'show usage information',
            '--version': 'show version information',
        }
    return None


@register_completion_schema('stow')
def _stow_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for stow commands."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-d': '-d/--dir: stow directory (default is parent of current)',
            '--dir': '--dir/-d: stow directory (default is parent of current)',
            '-t': '-t/--target: target directory (default is current directory)',
            '--target': '--target/-t: target directory (default is current directory)',
            '-S': '-S/--stow: stow packages',
            '--stow': '--stow/-S: stow packages',
            '-D': '-D/--delete: unstow packages',
            '--delete': '--delete/-D: unstow packages',
            '-R': '-R/--restow: restow packages (unstow then stow)',
            '--restow': '--restow/-R: restow packages (unstow then stow)',
            '--adopt': 'adopt files from target into stow directory',
            '--no-folding': 'disable folding of newly stowed directories',
            '-v': '-v/--verbose: increase verbosity',
            '--verbose': '--verbose/-v: increase verbosity',
            '-n': '-n/--no/--simulate: simulate actions without modifying filesystem',
            '--no': '--no/-n/--simulate: simulate actions without modifying filesystem',
            '--simulate': '--simulate/-n/--no: simulate actions without modifying filesystem',
            '--override': 'force overriding of conflicts',
            '--defer': 'defer conflicting files',
            '--ignore': 'ignore files matching regex',
        }
    return None


@register_completion_schema('manim')
def _manim_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for manim commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': '--help/-h: show help message',
            '-h': '-h/--help: show help message',
            '--version': '--version/-v: show version information',
            '-v': '-v/--version: show version information',
            '-p': '-p/--preview: preview animation when done',
            '--preview': '--preview/-p: preview animation when done',
            '-f': '-f/--format: output format (mp4, gif, png, etc.)',
            '--format': '--format/-f: output format (mp4, gif, png, etc.)',
            '-s': '-s/--save_last_frame: save last frame as image',
            '--save_last_frame': '--save_last_frame/-s: save last frame as image',
            '-q': '-q/--quality: render quality (l/m/h/p/k)',
            '--quality': '--quality/-q: render quality (l/m/h/p/k)',
            '-r': '-r/--resolution: resolution (WIDTHxHEIGHT)',
            '--resolution': '--resolution/-r: resolution (WIDTHxHEIGHT)',
            '--fps': 'frames per second',
            '-n': '-n/--from_animation_number: start from animation number',
            '--from_animation_number': '--from_animation_number/-n: start from animation number',
            '-a': '-a/--write_all: render all animations',
            '--write_all': '--write_all/-a: render all animations',
            '--dry_run': 'run without rendering',
            '--tex_template': 'specify LaTeX template',
            '--plugins': 'specify plugins',
            '--flush_cache': 'flush cache before rendering',
        }

    # Subcommands at position 0
    result = _complete_at_position_zero(cursor_token_idx, is_after,
                                        ['render', 'cfg', 'plugins', 'init'])
    if result:
        return result
    return None


@register_completion_schema('micromamba')
def _micromamba_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for micromamba commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return ['--help', '-h', '--version', '-v', '-y', '--yes', '-n', '--name',
                '-p', '--prefix', '-c', '--channel', '--override-channels',
                '--repodata-fn', '--no-deps', '--only-deps', '-f', '--file',
                '--freeze-installed']

    # Subcommands at position 0
    result = _complete_at_position_zero(cursor_token_idx, is_after,
                                        ['create', 'install', 'update', 'remove', 'list',
                                         'search', 'clean', 'info', 'config', 'activate',
                                         'deactivate', 'run', 'shell', 'env'])
    if result:
        return result
    return None


# ============================================================================
# Group C: Terminal/Editor Commands
# ============================================================================

@register_completion_schema('zellij')
def _zellij_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for zellij commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''
        common_flags = {
            '--help': 'show help message',
            '-h': '-h/--help: show help',
            '--version': 'show version',
            '-V': '-V/--version: show version',
        }

        flag_mapping = {
            'action': {**common_flags, **{'--max-panes': 'maximum number of panes', '--data-dir': 'data directory', '--server': 'server socket', '--session': '--session/-s: session name', '-s': '-s/--session: session name', '--layout': '--layout/-l: layout file', '-l': '-l/--layout: layout file', '--config': '--config/-c: config file', '-c': '-c/--config: config file', '--config-dir': 'config directory', '--debug': 'enable debug mode'}},
            'attach': {**common_flags, **{'--session': '--session/-s: session to attach to', '-s': '-s/--session: session to attach to', '--create': 'create session if it does not exist', '--index': 'attach to session by index', '--options': 'session options'}},
            'edit': {**common_flags, **{'--session': '--session/-s: target session', '-s': '-s/--session: target session', '--floating': 'open in floating pane', '--in-place': 'open in current pane', '--direction': 'split direction'}},
            'kill-session': {**common_flags, **{'--session': '--session/-s: session to kill', '-s': '-s/--session: session to kill'}},
            'list-sessions': common_flags,
            'run': {**common_flags, **{'--session': '--session/-s: target session', '-s': '-s/--session: target session', '--floating': 'run in floating pane', '--in-place': 'run in current pane', '--direction': 'split direction', '--name': '--name/-n: pane name', '-n': '-n/--name: pane name', '--close-on-exit': 'close pane when command exits'}},
            'setup': {**common_flags, **{'--dump-config': 'dump default config', '--clean': 'clean config', '--check': 'check config'}},
        }

        return _get_subcommand_flags(subcommand, flag_mapping, common_flags)

    result = _complete_at_position_zero(cursor_token_idx, is_after, {
        'action': 'send action to session',
        'attach': 'attach to session',
        'convert-config': 'convert configuration format',
        'edit': 'edit file in session',
        'kill-all-sessions': 'kill all sessions',
        'kill-session': 'kill specific session',
        'list-sessions': 'list active sessions',
        'options': 'change session options',
        'plugin': 'manage plugins',
        'run': 'run command in new pane',
        'setup': 'setup zellij configuration',
    })
    if result:
        return result

    return None


@register_completion_schema('fnm')
def _fnm_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for fnm (Fast Node Manager) commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''
        common_flags = {
            '--help': 'show help message',
            '-h': '-h/--help: show help',
            '--version': 'show version',
            '-V': '-V/--version: show version',
            '--log-level': 'set log level',
            '--node-dist-mirror': 'node distribution mirror',
            '--fnm-dir': 'fnm directory',
            '--multishell-path': 'multishell path',
            '--arch': 'architecture',
            '--version-file-strategy': 'version file strategy',
        }

        flag_mapping = {
            'install': {**common_flags, **{'--lts': 'install LTS version', '--latest': 'install latest version'}},
            'use': {**common_flags, **{'--install-if-missing': 'install version if not present', '--silent-if-unchanged': 'suppress output if version unchanged'}},
            'env': {**common_flags, **{'--shell': 'target shell', '--multi': 'allow multiple versions', '--use-on-cd': 'automatically switch version on directory change'}},
            'list': common_flags,
            'list-remote': common_flags,
            'uninstall': common_flags,
            'alias': common_flags,
            'default': common_flags,
            'current': common_flags,
            'exec': common_flags + ['--using'],
            'completions': common_flags + ['--shell'],
        }

        return _get_subcommand_flags(subcommand, flag_mapping, common_flags)

    result = _complete_at_position_zero(cursor_token_idx, is_after, {
        'install': 'install Node.js version',
        'use': 'change Node.js version',
        'env': 'print shell configuration',
        'list': 'list installed versions',
        'list-remote': 'list remote Node.js versions',
        'uninstall': 'uninstall Node.js version',
        'alias': 'alias version to common name',
        'default': 'set default Node.js version',
        'current': 'print current Node.js version',
        'exec': 'run command with fnm configured',
        'completions': 'print shell completions',
    })
    if result:
        return result

    return None


@register_completion_schema('npx')
def _npx_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for npx commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': '--help/-h: show help message',
            '-h': '-h/--help: show help message',
            '-p': '-p/--package: package to install and execute',
            '--package': '--package/-p: package to install and execute',
            '-c': '-c/--call: command string to execute',
            '--call': '--call/-c: command string to execute',
            '--shell': '--shell/-s: shell to use for command',
            '-s': '-s/--shell: shell to use for command',
            '--shell-auto-fallback': 'auto-fallback to shell',
            '--no-install': 'skip installation if package is not found',
            '-y': '-y/--yes: skip confirmation prompt',
            '--yes': '--yes/-y: skip confirmation prompt',
            '-q': '-q/--quiet: suppress output',
            '--quiet': '--quiet/-q: suppress output',
            '-v': '-v/--version: show version information',
            '--version': '--version/-v: show version information',
        }

    return None


@register_completion_schema('marimo')
def _marimo_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for marimo commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        subcommand = tokens[1].text if len(tokens) > 1 else ''

        # Common flags as dictionary with descriptions
        common_flags = {
            '--help': 'show help message',
            '-h': '-h/--help: show help message',
            '--version': 'show version',
            '-v': '-v/--version: show version',
        }

        # Subcommand-specific flags
        flag_mapping = {
            'edit': {
                **common_flags,
                '--port': '--port/-p: specify server port',
                '-p': '--port/-p: specify server port',
                '--host': 'specify server host',
                '--headless': 'run without browser',
                '--no-token': 'disable authentication token',
                '--token-password': 'set token password',
            },
            'run': {
                **common_flags,
                '--port': '--port/-p: specify server port',
                '-p': '--port/-p: specify server port',
                '--host': 'specify server host',
                '--headless': 'run without browser',
                '--no-token': 'disable authentication token',
                '--token-password': 'set token password',
                '--include-code': 'include code in output',
            },
            'new': common_flags,
            'convert': {
                **common_flags,
                '--output': '--output/-o: specify output file',
                '-o': '--output/-o: specify output file',
            },
            'export': {
                **common_flags,
                '--output': '--output/-o: specify output directory',
                '-o': '--output/-o: specify output directory',
                '--format': 'export format (html, pdf, etc)',
                '--watch': 'watch for changes and re-export',
            },
            'tutorial': common_flags,
            'config': {
                **common_flags,
                '--show': 'show current configuration',
            },
        }

        # Return flags for the specific subcommand, or common flags if unknown
        if subcommand in flag_mapping:
            return flag_mapping[subcommand]
        return common_flags

    # Subcommands as dictionary with descriptions
    subcommands = {
        'edit': 'edit a marimo notebook',
        'run': 'run a marimo notebook',
        'new': 'create a new notebook',
        'convert': 'convert notebook to/from other formats',
        'export': 'export notebook to static format',
        'tutorial': 'run interactive tutorial',
        'config': 'manage marimo configuration',
    }

    result = _complete_at_position_zero(cursor_token_idx, is_after, subcommands)
    if result:
        return result

    return None


@register_completion_schema('vimdiff')
def _vimdiff_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for vimdiff commands."""
    # Check for flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return ['-R', '-d', '-c', '-S', '-u', '-n', '-b', '-o', '-O', '-p', '-q',
                '--help', '--version', '--noplugin', '--startuptime']

    return None


# ============================================================================
# Group F: Shell Integration Commands
# ============================================================================

@register_completion_schema('sudo')
def _sudo_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for sudo commands with passthrough to actual command."""
    # First, try to find if there's a command to passthrough to
    # Find the first non-flag token after sudo
    command_idx = None
    for i in range(1, len(tokens)):
        if not tokens[i].text.startswith('-'):
            command_idx = i
            break

    # If we found a command and cursor is at or after it, forward to that command
    if command_idx is not None and cursor_token_idx >= command_idx:
        command_name = tokens[command_idx].text

        # Check if this command has a completion schema
        if command_name in _COMPLETION_SCHEMAS:
            # Adjust token indices: pretend the actual command is at position 0
            adjusted_cursor_idx = cursor_token_idx - command_idx
            adjusted_tokens = tokens[command_idx:]

            try:
                schema_func = _COMPLETION_SCHEMAS[command_name]
                return schema_func(adjusted_tokens, adjusted_cursor_idx, is_after)
            except Exception:
                return None

    # If no passthrough, check for sudo flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-u': '-u/--user: run command as specified user',
            '--user': '--user/-u: run command as specified user',
            '-g': '-g/--group: run command with specified group',
            '--group': '--group/-g: run command with specified group',
            '-H': 'set HOME environment variable to target user',
            '-k': 'invalidate timestamp file',
            '-K': 'remove timestamp file',
            '-l': 'list user privileges',
            '-v': 'update timestamp without running command',
            '-V': 'display version information',
            '-h': '-h/--help: display help',
            '--help': '--help/-h: display help',
            '-b': 'run command in background',
            '-E': 'preserve environment',
            '-e': 'edit files instead of running command',
            '-i': 'simulate initial login',
            '-s': 'run shell',
            '-S': 'read password from stdin',
            '-n': 'non-interactive mode (fail if password required)',
            '-P': 'preserve group vector',
        }

    return None


@register_completion_schema('cd')
def _cd_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for cd commands (directory navigation)."""
    # Check for cd flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return ['-L', '-P', '-e', '-@']

    # Path completion is handled elsewhere in the system
    return None


@register_completion_schema('time')
def _time_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for time commands with passthrough to actual command."""
    # First, try to find if there's a command to passthrough to
    # Find the first non-flag token after time
    command_idx = None
    for i in range(1, len(tokens)):
        if not tokens[i].text.startswith('-'):
            command_idx = i
            break

    # If we found a command and cursor is at or after it, forward to that command
    if command_idx is not None and cursor_token_idx >= command_idx:
        command_name = tokens[command_idx].text

        # Check if this command has a completion schema
        if command_name in _COMPLETION_SCHEMAS:
            # Adjust token indices: pretend the actual command is at position 0
            adjusted_cursor_idx = cursor_token_idx - command_idx
            adjusted_tokens = tokens[command_idx:]

            try:
                schema_func = _COMPLETION_SCHEMAS[command_name]
                return schema_func(adjusted_tokens, adjusted_cursor_idx, is_after)
            except Exception:
                return None

    # If no passthrough, check for time flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        # BSD and GNU time flags
        return {
            '-p': 'use POSIX format output',
            '-l': 'show detailed resource usage (BSD)',
            '--verbose': 'verbose output showing all statistics (GNU)',
            '--portability': 'use POSIX format output (GNU)',
        }

    return None


@register_completion_schema('osascript')
def _osascript_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for osascript commands (macOS AppleScript execution)."""
    # Check for osascript flags
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-e': 'execute the given AppleScript command',
            '-l': 'specify language (e.g., AppleScript, JavaScript)',
            '-i': 'run script in interactive mode',
            '-s': 'set script flags',
            '-ss': 'set script flags with strict mode',
        }

    return None


@register_completion_schema('netstat')
def _netstat_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for netstat (network statistics) command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-A': 'show addresses of protocol control blocks',
            '-a': 'show state of all sockets',
            '-L': 'show size of listen queues',
            '-l': 'print full IPv6 address',
            '-n': 'show network addresses as numbers',
            '-W': 'show wide output',
            '-f': 'limit statistics to address family',
            '-p': 'show statistics for protocol',
            '-g': 'show multicast routing tables',
            '-i': 'show interface statistics',
            '-I': 'show statistics for specific interface',
            '-s': 'show per-protocol statistics',
            '-w': 'wait time between displays',
            '-b': 'show buffer sizes',
            '-d': 'show dropped packets',
            '-R': 'show routing table contents',
            '-t': 'show current connections in time wait',
            '-S': 'show source address',
            '-m': 'show mbuf statistics',
            '-r': 'show routing tables',
        }
    return None


@register_completion_schema('ifconfig')
def _ifconfig_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ifconfig (network interface configuration) command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': 'display all interfaces',
            '-l': 'list interface names only',
            '-X': 'disable extended link-level reachability information',
            'alias': 'establish an additional network address',
            '-alias': 'remove network address',
            'arp': 'enable use of ARP',
            '-arp': 'disable use of ARP',
            'broadcast': 'set broadcast address',
            'debug': 'enable driver debugging',
            '-debug': 'disable driver debugging',
            'delete': 'remove network address',
            'down': 'mark interface as down',
            'up': 'mark interface as up',
            'inet': 'set IPv4 address',
            'inet6': 'set IPv6 address',
            'media': 'set media type',
            'mediaopt': 'set media options',
            'metric': 'set routing metric',
            'mtu': 'set maximum transmission unit',
            'netmask': 'set network mask',
            'prefixlen': 'set prefix length for IPv6',
            'promisc': 'enable promiscuous mode',
            '-promisc': 'disable promiscuous mode',
        }
    return None


@register_completion_schema('lsof')
def _lsof_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for lsof (list open files) command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-i': 'list files opened by network connections',
            '-p': 'list files opened by specific process ID',
            '-u': 'list files opened by specific user',
            '-c': 'list files opened by processes with command name',
            '-n': 'do not resolve hostnames (faster)',
            '-P': 'do not resolve port numbers (faster)',
            '-t': 'terse output (PIDs only)',
            '-s': 'show file size',
            '-r': 'repeat mode (continuous listing)',
            '-a': 'AND the selections (instead of OR)',
            '-l': 'inhibit conversion of user IDs to login names',
            '-h': 'print help message',
            '-v': 'print version information',
            '-V': 'verbose search information',
            '-w': 'suppress warning messages',
            '-d': 'select by file descriptor',
            '-D': 'direct device cache file processing',
            '-F': 'produce output for post-processing',
            '-g': 'select by process group ID',
            '-k': 'specify kernel name list file',
            '-m': 'specify kernel memory file',
            '-R': 'list parent PID',
            '-T': 'report TCP/TPI information',
            '-X': 'skip TCP and UDP port name lookup',
            '+r': 'repeat mode with delay',
            '+D': 'search directory recursively',
            '+L': 'list link counts',
            '+|-f': 'enable/disable kernel file structure',
        }
    return None


@register_completion_schema('nmap')
def _nmap_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for nmap (network mapper) command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            # TARGET SPECIFICATION
            '-iL': 'input from list of hosts/networks',
            '-iR': 'choose random targets',
            '--exclude': 'exclude hosts/networks',
            '--excludefile': 'exclude list from file',
            # HOST DISCOVERY
            '-sL': 'list scan - simply list targets to scan',
            '-sn': 'ping scan - disable port scan',
            '-Pn': 'treat all hosts as online -- skip host discovery',
            '-PS': 'TCP SYN discovery to given ports',
            '-PA': 'TCP ACK discovery to given ports',
            '-PU': 'UDP discovery to given ports',
            '-PY': 'SCTP discovery to given ports',
            '-PE': 'ICMP echo request discovery probes',
            '-PP': 'ICMP timestamp request discovery probes',
            '-PM': 'ICMP netmask request discovery probes',
            '-PO': 'IP protocol ping',
            '-n': 'never do DNS resolution',
            '-R': 'always resolve [default: sometimes]',
            '--dns-servers': 'specify custom DNS servers',
            '--system-dns': 'use OS\'s DNS resolver',
            '--traceroute': 'trace hop path to each host',
            # SCAN TECHNIQUES
            '-sS': 'TCP SYN scan',
            '-sT': 'TCP connect() scan',
            '-sA': 'TCP ACK scan',
            '-sW': 'TCP window scan',
            '-sM': 'TCP maimon scan',
            '-sU': 'UDP scan',
            '-sN': 'TCP null scan',
            '-sF': 'TCP FIN scan',
            '-sX': 'TCP xmas scan',
            '--scanflags': 'customize TCP scan flags',
            '-sI': 'idle scan',
            '-sY': 'SCTP INIT scan',
            '-sZ': 'SCTP COOKIE-ECHO scan',
            '-sO': 'IP protocol scan',
            '-b': 'FTP bounce scan',
            # PORT SPECIFICATION
            '-p': 'only scan specified ports',
            '--exclude-ports': 'exclude the specified ports from scanning',
            '-F': 'fast mode - scan fewer ports than the default scan',
            '-r': 'scan ports sequentially - don\'t randomize',
            '--top-ports': 'scan <number> most common ports',
            '--port-ratio': 'scan ports more common than <ratio>',
            # SERVICE/VERSION DETECTION
            '-sV': 'probe open ports to determine service/version info',
            '--version-intensity': 'set from 0 (light) to 9 (try all probes)',
            '--version-light': 'limit to most likely probes (intensity 2)',
            '--version-all': 'try every single probe (intensity 9)',
            '--version-trace': 'show detailed version scan activity (for debugging)',
            # SCRIPT SCAN
            '-sC': 'equivalent to --script=default',
            '--script': 'comma separated list of directories, script-files or script-categories',
            '--script-args': 'provide arguments to scripts',
            '--script-args-file': 'provide NSE script args in a file',
            '--script-trace': 'show all data sent and received',
            '--script-updatedb': 'update the script database',
            '--script-help': 'show help about scripts',
            # OS DETECTION
            '-O': 'enable OS detection',
            '--osscan-limit': 'limit OS detection to promising targets',
            '--osscan-guess': 'guess OS more aggressively',
            # TIMING AND PERFORMANCE
            '-T': 'set timing template (0-5: higher is faster)',
            '--min-hostgroup': 'parallel host scan group sizes',
            '--max-hostgroup': 'parallel host scan group sizes',
            '--min-parallelism': 'probe parallelization',
            '--max-parallelism': 'probe parallelization',
            '--min-rtt-timeout': 'specifies probe round trip time',
            '--max-rtt-timeout': 'specifies probe round trip time',
            '--initial-rtt-timeout': 'specifies probe round trip time',
            '--max-retries': 'caps number of port scan probe retransmissions',
            '--host-timeout': 'give up on target after this long',
            '--scan-delay': 'adjust delay between probes',
            '--max-scan-delay': 'adjust delay between probes',
            '--min-rate': 'send packets no slower than <number> per second',
            '--max-rate': 'send packets no faster than <number> per second',
            # FIREWALL/IDS EVASION AND SPOOFING
            '-f': 'fragment packets (optionally w/given MTU)',
            '--mtu': 'fragment packets (optionally w/given MTU)',
            '-D': 'cloak a scan with decoys',
            '-S': 'spoof source address',
            '-e': 'use specified interface',
            '-g': 'use given port number',
            '--source-port': 'use given port number',
            '--proxies': 'relay connections through HTTP/SOCKS4 proxies',
            '--data': 'append a custom payload to sent packets',
            '--data-string': 'append a custom ASCII string to sent packets',
            '--data-length': 'append random data to sent packets',
            '--ip-options': 'send packets with specified ip options',
            '--ttl': 'set IP time-to-live field',
            '--spoof-mac': 'spoof your MAC address',
            '--badsum': 'send packets with a bogus TCP/UDP/SCTP checksum',
            # OUTPUT
            '-oN': 'output scan in normal format to the given filename',
            '-oX': 'output scan in XML format to the given filename',
            '-oS': 'output scan in s|<rIpt kIddi3 format to the given filename',
            '-oG': 'output scan in grepable format to the given filename',
            '-oA': 'output in the three major formats at once',
            '-v': 'increase verbosity level (use -vv or more for greater effect)',
            '-d': 'increase debugging level (use -dd or more for greater effect)',
            '--reason': 'display the reason a port is in a particular state',
            '--open': 'only show open (or possibly open) ports',
            '--packet-trace': 'show all packets sent and received',
            '--iflist': 'print host interfaces and routes (for debugging)',
            '--append-output': 'append to rather than clobber specified output files',
            '--resume': 'resume an aborted scan',
            '--noninteractive': 'disable runtime interactions via keyboard',
            '--stylesheet': 'XSL stylesheet to transform XML output to HTML',
            '--webxml': 'reference stylesheet from Nmap.Org for more portable XML',
        }
    return None


@register_completion_schema('traceroute')
def _traceroute_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for traceroute command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': 'turn on AS# lookups for each hop encountered',
            '-A': 'turn on AS# lookups and use the given server instead of the default',
            '-d': 'enable socket level debugging',
            '-D': 'print differences between transmitted and quoted packet',
            '-e': 'firewall evasion mode - use fixed destination ports',
            '-E': 'detect ECN bleaching',
            '-f': 'set the initial time-to-live used in the first outgoing probe packet',
            '-F': 'set the "don\'t fragment" bit',
            '-g': 'specify a loose source route gateway (8 maximum)',
            '-i': 'specify a network interface to obtain the source IP address',
            '-I': 'use ICMP ECHO instead of UDP datagrams',
            '-M': 'set the initial time-to-live value used in outgoing probe packets',
            '-m': 'set the max time-to-live (max number of hops) used in outgoing probe packets',
            '-n': 'print hop addresses numerically rather than symbolically',
            '-P': 'send packets of specified IP protocol (UDP, TCP, GRE, ICMP)',
            '-p': 'set the base port number used in probes (default is 33434)',
            '-q': 'set the number of probes per ttl (default is three probes)',
            '-r': 'bypass the normal routing tables and send directly to a host',
            '-s': 'use the following IP address as the source address in outgoing probe packets',
            '-S': 'print a summary of how many probes were not answered for each hop',
            '-t': 'set the type-of-service in probe packets (default zero)',
            '-v': 'verbose output - received ICMP packets other than TIME_EXCEEDED and UNREACHABLEs',
            '-w': 'set the time (in seconds) to wait for a response to a probe (default 5 sec)',
            '-x': 'toggle IP checksums',
            '-z': 'set the time (in milliseconds) to pause between probes (default 0)',
        }
    return None


@register_completion_schema('dig')
def _dig_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for dig (DNS lookup) command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '+short': 'display terse output',
            '+trace': 'trace delegation from root servers',
            '+nocmd': 'do not print initial command line',
            '+nocomments': 'do not print comment lines',
            '+noquestion': 'do not print question section',
            '+noanswer': 'do not print answer section',
            '+noauthority': 'do not print authority section',
            '+noadditional': 'do not print additional section',
            '+nostats': 'do not print statistics',
            '+noall': 'clear all display flags',
            '+all': 'set all display flags',
            '+answer': 'display answer section',
            '+stats': 'display statistics',
            '+tcp': 'use TCP instead of UDP',
            '+notcp': 'use UDP (default)',
            '+recurse': 'enable recursion (default)',
            '+norecurse': 'disable recursion',
            '+dnssec': 'request DNSSEC records',
            '+multiline': 'verbose multiline format for records',
            '+retry': 'set number of UDP retries',
            '+time': 'set query timeout (seconds)',
            '+tries': 'set number of UDP attempts',
            '+bufsize': 'set EDNS0 UDP packet size',
            '+ndots': 'set number of dots for absolute names',
            '+domain': 'set search domain',
            '+search': 'use search list (default)',
            '+nosearch': 'do not use search list',
            '+defname': 'use default domain (default)',
            '+nodefname': 'do not use default domain',
            '+aaonly': 'set AA flag in query',
            '+adflag': 'set AD flag in query',
            '+cdflag': 'set CD flag in query',
            '+cl': 'display class in records',
            '+ttlid': 'display TTL in records',
            '+identify': 'identify server that provided answer',
            '+split': 'split hex/base64 fields into chunks',
            '@': 'specify DNS server (e.g., @8.8.8.8)',
            '-p': 'specify port number',
            '-b': 'specify bind address',
            '-4': 'use IPv4 only',
            '-6': 'use IPv6 only',
            '-t': 'specify query type (A, AAAA, MX, NS, etc.)',
            '-x': 'reverse lookup',
            '-f': 'read queries from file',
            '-v': 'print version',
            '-h': 'print help',
        }
    return None


@register_completion_schema('host')
def _host_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for host (DNS lookup) command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': 'equivalent to -v -t ANY',
            '-c': 'specify query class (IN, CH, HS)',
            '-C': 'check SOA records for zone',
            '-d': '-d/-v: verbose output',
            '-v': '-d/-v: verbose output',
            '-l': 'list all hosts in domain (zone transfer)',
            '-i': 'use IP6.INT for reverse lookups',
            '-n': 'non-recursive query',
            '-r': 'disable recursive processing',
            '-R': 'set number of retries',
            '-s': 'set number of UDP retries for SERVFAIL',
            '-t': 'specify query type (A, AAAA, MX, NS, SOA, TXT, etc.)',
            '-T': 'use TCP',
            '-U': 'use UDP (default)',
            '-w': 'wait forever for response',
            '-W': 'set wait time (seconds)',
            '-4': 'use IPv4 only',
            '-6': 'use IPv6 only',
            '-m': 'set memory debugging flags',
            '-N': 'set number of dots for absolute names',
            '-V': 'print version',
        }
    return None


@register_completion_schema('nslookup')
def _nslookup_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for nslookup (DNS query) command."""
    # nslookup is interactive and has no command-line flags for query options
    return None


@register_completion_schema('nc')
def _nc_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for nc/netcat (networking utility) command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-4': 'use IPv4 only',
            '-6': 'use IPv6 only',
            '-A': 'set SO_RECV_ANYIF on socket',
            '-a': 'use alternate APN',
            '-b': 'allow broadcast',
            '-C': 'send CRLF as line ending',
            '-c': 'cellular interface',
            '-D': 'enable debugging on socket',
            '-d': 'disable reading from stdin',
            '-E': 'no TCP extended options',
            '-F': 'pass socket fd',
            '-G': 'connection timeout',
            '-H': 'traffic class',
            '-h': 'help message',
            '-I': 'TCP receive buffer length',
            '-i': 'delay interval for lines sent',
            '-J': 'source address for connection',
            '-K': 'traffic class',
            '-k': 'keep listening after client disconnect',
            '-L': 'tcp connection timeout for retransmissions',
            '-l': 'listen mode (server)',
            '-m': 'minimum throughput in kbits/sec',
            '-N': 'shutdown network socket after EOF',
            '-n': 'do not resolve hostnames',
            '-O': 'TCP send buffer length',
            '-o': 'hex dump traffic',
            '-p': 'specify source port',
            '-r': 'random local and remote ports',
            '-s': 'specify source address',
            '-t': 'telnet negotiation',
            '-U': 'use Unix domain socket',
            '-u': 'UDP mode (default is TCP)',
            '-v': 'verbose output',
            '-w': 'timeout for connections and reads',
            '-X': 'specify proxy protocol version',
            '-x': 'specify proxy address and port',
            '-z': 'zero-I/O mode (scanning)',
        }
    return None


@register_completion_schema('uv')
def _uv_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for uv (Python package installer)."""
    # Show subcommands after 'uv '
    if cursor_token_idx == 0 and is_after:
        return {
            'install': 'install packages',
            'sync': 'sync environment with lockfile',
            'add': 'add a dependency to the project',
            'remove': 'remove a dependency from the project',
            'lock': 'update the project lockfile',
            'pip': 'pip-compatible interface',
            'run': 'run a command in the environment',
            'init': 'initialize a new project',
            'venv': 'create a virtual environment',
            'tool': 'manage tools',
            'python': 'manage Python installations',
            'cache': 'manage the cache',
            'version': 'display version',
            'help': 'display help',
        }
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': 'display help message',
            '--version': 'display version information',
            '--quiet': '--quiet/-q: suppress output',
            '-q': '-q/--quiet: suppress output',
            '--verbose': '--verbose/-v: verbose output',
            '-v': '-v/--verbose: verbose output',
            '--no-cache': 'disable cache',
            '--cache-dir': 'path to cache directory',
            '--python': 'specify Python version',
            '--system': 'use system Python',
        }
    return None


@register_completion_schema('asciinema')
def _asciinema_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for asciinema (terminal recorder)."""
    # Show subcommands after 'asciinema '
    if cursor_token_idx == 0 and is_after:
        return {
            'rec': 'record terminal session',
            'play': 'play recorded session',
            'cat': 'print full output of recorded session',
            'upload': 'upload recorded session to asciinema.org',
            'auth': 'manage authentication with asciinema.org',
        }
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': 'display help message',
            '--version': 'display version information',
            '--stdin': 'enable stdin recording',
            '--append': 'append to existing recording',
            '--raw': 'save raw stdout output',
            '--overwrite': 'overwrite existing recording',
            '-c': 'specify command to record',
            '--command': 'specify command to record',
            '-e': 'comma-separated list of env vars to capture',
            '--env': 'comma-separated list of env vars to capture',
            '-t': 'set recording title',
            '--title': 'set recording title',
            '-i': 'limit idle time (for rec)',
            '--idle-time-limit': 'limit idle time (for rec)',
            '-s': 'set playback speed (for play)',
            '--speed': 'set playback speed (for play)',
            '-l': 'loop playback (for play)',
            '--loop': 'loop playback (for play)',
        }
    return None


@register_completion_schema('speedtest')
def _speedtest_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for speedtest (network speed test)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': 'display help message',
            '--version': 'display version information',
            '--secure': 'use HTTPS instead of HTTP',
            '--no-download': 'skip download test',
            '--no-upload': 'skip upload test',
            '--json': 'output results in JSON format',
            '--csv': 'output results in CSV format',
            '--csv-delimiter': 'delimiter for CSV output',
            '--csv-header': 'include header in CSV output',
            '--simple': 'simple output format',
            '--list': 'list available test servers',
            '--server': 'specify server ID for test',
            '--servers': 'comma-separated list of server IDs',
            '--exclude': 'exclude servers by ID',
            '--source': 'source IP address to bind to',
            '--timeout': 'timeout for HTTP requests',
            '--share': 'generate and provide URL to speedtest.net share result',
            '--bytes': 'display values in bytes instead of bits',
        }
    return None


@register_completion_schema('ranger')
def _ranger_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ranger (file manager)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': 'display help message',
            '--version': 'display version information',
            '--debug': 'activate debug mode',
            '--clean': 'clean configuration, do not load user files',
            '--confdir': 'path to configuration directory',
            '--datadir': 'path to data directory',
            '--copy-config': 'copy default configuration to user directory',
            '--choosefile': 'make ranger act like file chooser',
            '--choosedir': 'make ranger act like directory chooser',
            '--selectfile': 'open with selected file',
            '--list-unused-keys': 'list all keys not bound to any action',
            '--list-tagged-files': 'list all tagged files',
            '--profile': 'print statistics after exit',
            '--cmd': 'execute command after startup',
            '-r': '-r/--confdir: path to configuration directory',
            '-d': '-d/--debug: activate debug mode',
        }
    return None


@register_completion_schema('convert')
def _convert_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for convert (ImageMagick image processor)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': 'display help message',
            '--version': 'display version information',
            '-resize': 'resize image (e.g., 800x600, 50%)',
            '-quality': 'JPEG/PNG compression quality (1-100)',
            '-rotate': 'rotate image by degrees',
            '-format': 'output format (jpg, png, gif, etc.)',
            '-crop': 'crop image (e.g., 100x100+10+10)',
            '-scale': 'scale image to size',
            '-thumbnail': 'create thumbnail',
            '-flip': 'flip image vertically',
            '-flop': 'flop image horizontally',
            '-background': 'set background color',
            '-fill': 'set fill color',
            '-gravity': 'set gravity (NorthWest, Center, etc.)',
            '-blur': 'blur image',
            '-sharpen': 'sharpen image',
            '-contrast': 'enhance contrast',
            '-normalize': 'normalize image',
            '-negate': 'negate colors',
            '-colors': 'reduce number of colors',
            '-colorspace': 'set colorspace (RGB, CMYK, Gray)',
            '-strip': 'strip image metadata',
            '-density': 'set image resolution (DPI)',
            '-page': 'set page size and offset',
            '-compress': 'compression type',
            '-define': 'define coder/decoder specific options',
        }
    return None


@register_completion_schema('telnet')
def _telnet_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for telnet command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-4': 'force IPv4 address resolution',
            '-6': 'force IPv6 address resolution',
            '-8': 'use 8-bit data path',
            '-E': 'stop escape character',
            '-K': 'do not send automatic login',
            '-L': 'use 8-bit data path on output',
            '-N': 'disable TCP keep-alives',
            '-S': 'TOS value',
            '-X': 'authentication type',
            '-c': 'disable .telnetrc reading',
            '-d': 'enable debugging',
            '-e': 'escape character',
            '-f': 'forward credentials (Kerberos)',
            '-F': 'forward credentials (Kerberos)',
            '-k': 'Kerberos realm',
            '-l': 'specify user name',
            '-n': 'trace file',
            '-r': 'rlogin-like interface',
            '-s': 'source address',
            '-u': 'force unencrypted communication',
            '-P': 'IPsec policy',
        }
    return None


@register_completion_schema('ab')
def _ab_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ab (Apache Bench)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-n': 'number of requests to perform',
            '-c': 'number of concurrent requests',
            '-t': 'time limit for testing (seconds)',
            '-s': 'timeout per request (seconds)',
            '-k': 'enable HTTP KeepAlive feature',
            '-p': 'file containing POST data',
            '-u': 'file containing PUT data',
            '-T': 'content-type header for POST/PUT',
            '-v': 'verbosity level',
            '-w': 'print results in HTML table',
            '-i': 'use HEAD instead of GET',
            '-x': 'use <table> attributes',
            '-X': 'use proxy server',
            '-y': 'use <tr> attributes',
            '-z': 'use <td> attributes',
            '-C': 'add cookie (e.g., name=value)',
            '-H': 'add arbitrary header',
            '-A': 'add Basic WWW Authentication',
            '-P': 'add Basic Proxy Authentication',
            '-g': 'write gnuplot file',
            '-e': 'write CSV file',
            '-r': 'do not exit on socket receive errors',
            '-m': 'HTTP method',
            '-h': 'display help message',
            '-V': 'display version information',
        }
    return None


@register_completion_schema('yes')
def _yes_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for yes command."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': 'display help message and exit',
            '--version': 'output version information and exit',
        }
    return None


@register_completion_schema('lolcat')
def _lolcat_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for lolcat (rainbow coloring)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--help': 'display help message',
            '--version': 'display version information',
            '-a': '-a/--animate: enable animation',
            '--animate': '--animate/-a: enable animation',
            '-d': '-d/--duration: animation duration (seconds)',
            '--duration': '--duration/-d: animation duration (seconds)',
            '-s': '-s/--speed: animation speed',
            '--speed': '--speed/-s: animation speed',
            '-p': '-p/--spread: rainbow spread',
            '--spread': '--spread/-p: rainbow spread',
            '-F': '-F/--freq: rainbow frequency',
            '--freq': '--freq/-F: rainbow frequency',
            '-f': '-f/--force: force color even when not in tty',
            '--force': '--force/-f: force color even when not in tty',
            '-S': '-S/--seed: rainbow seed (0 for random)',
            '--seed': '--seed/-S: rainbow seed (0 for random)',
            '-i': '-i/--invert: invert foreground and background',
            '--invert': '--invert/-i: invert foreground and background',
            '-t': '-t/--truecolor: enable truecolor (24-bit)',
            '--truecolor': '--truecolor/-t: enable truecolor (24-bit)',
        }
    return None


@register_completion_schema('htop')
def _htop_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for htop command (interactive process viewer)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-d': '-d/--delay: set update delay in tenths of seconds',
            '--delay': '--delay/-d: set update delay in tenths of seconds',
            '-C': '-C/--no-color: start htop in monochrome mode',
            '--no-color': '--no-color/-C: start htop in monochrome mode',
            '-F': '-F/--filter: filter process list by command name',
            '--filter': '--filter/-F: filter process list by command name',
            '-h': '-h/--help: print help and exit',
            '--help': '--help/-h: print help and exit',
            '-p': '-p/--pid: show only given PIDs',
            '--pid': '--pid/-p: show only given PIDs',
            '-s': '-s/--sort-key: sort by this column',
            '--sort-key': '--sort-key/-s: sort by this column',
            '-u': '-u/--user: show only processes of a given user',
            '--user': '--user/-u: show only processes of a given user',
            '-U': '-U/--no-unicode: disable unicode characters',
            '--no-unicode': '--no-unicode/-U: disable unicode characters',
            '-M': '-M/--no-mouse: disable mouse support',
            '--no-mouse': '--no-mouse/-M: disable mouse support',
            '-t': '-t/--tree: show tree view by default',
            '--tree': '--tree/-t: show tree view by default',
            '-H': '-H/--highlight-changes: highlight new and old processes',
            '--highlight-changes': '--highlight-changes/-H: highlight new and old processes',
            '--readonly': 'disable all system and process changing features',
            '-V': '-V/--version: print version information',
            '--version': '--version/-V: print version information',
        }
    return None


@register_completion_schema('btop')
def _btop_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for btop command (resource monitor)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-h': '-h/--help: show help message',
            '--help': '--help/-h: show help message',
            '-v': '-v/--version: show version info',
            '--version': '--version/-v: show version info',
            '-lc': '-lc/--low-color: disable truecolor mode',
            '--low-color': '--low-color/-lc: disable truecolor mode',
            '-t': '-t/--tty_on: force start with tty mode',
            '--tty_on': '--tty_on/-t: force start with tty mode',
            '+t': '+t/--tty_off: force start without tty mode',
            '--tty_off': '--tty_off/+t: force start without tty mode',
            '-p': '-p/--preset: start with preset (0-9)',
            '--preset': '--preset/-p: start with preset (0-9)',
            '--utf-force': 'force use of UTF-8 encoding',
            '--debug': 'start in debug mode with extra logging',
        }
    return None


@register_completion_schema('iotop')
def _iotop_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for iotop command (I/O monitor)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-C': 'do not clear screen',
            '-D': 'print delta times',
            '-j': 'print project ID',
            '-o': 'print disk delta times',
            '-P': 'print %I/O',
            '-Z': 'print zone ID',
            '-d': 'specify device',
            '-f': 'specify filename',
            '-m': 'specify mount_point',
            '-t': 'specify top processes to show',
        }
    return None


@register_completion_schema('iostat')
def _iostat_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for iostat command (I/O statistics)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-C': 'display CPU statistics',
            '-I': 'display total statistics for a given device',
            '-K': 'display block count in kilobytes',
            '-c': 'repeat display count times',
            '-d': 'display only device statistics',
            '-n': 'limit number of disks displayed',
            '-o': 'display old-style iostat device statistics',
            '-T': 'display TTY statistics',
            '-U': 'display system load averages',
            '-w': 'wait time between samples in seconds',
        }
    return None


@register_completion_schema('vmstat')
def _vmstat_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for vmstat command (virtual memory statistics)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': '-a/--active: show active/inactive memory',
            '--active': '--active/-a: show active/inactive memory',
            '-f': '-f/--forks: show number of forks since boot',
            '--forks': '--forks/-f: show number of forks since boot',
            '-m': '-m/--slabs: show slabinfo',
            '--slabs': '--slabs/-m: show slabinfo',
            '-n': '-n/--one-header: display header only once',
            '--one-header': '--one-header/-n: display header only once',
            '-s': '-s/--stats: show event counter statistics',
            '--stats': '--stats/-s: show event counter statistics',
            '-d': '-d/--disk: show disk statistics',
            '--disk': '--disk/-d: show disk statistics',
            '-D': '-D/--disk-sum: show disk summary statistics',
            '--disk-sum': '--disk-sum/-D: show disk summary statistics',
            '-p': '-p/--partition: show partition specific statistics',
            '--partition': '--partition/-p: show partition specific statistics',
            '-S': '-S/--unit: define display unit (k/K/m/M)',
            '--unit': '--unit/-S: define display unit (k/K/m/M)',
            '-t': '-t/--timestamp: show timestamp',
            '--timestamp': '--timestamp/-t: show timestamp',
            '-w': '-w/--wide: wide output mode',
            '--wide': '--wide/-w: wide output mode',
            '-V': '-V/--version: show version',
            '--version': '--version/-V: show version',
            '-h': '-h/--help: show help',
            '--help': '--help/-h: show help',
        }
    return None


@register_completion_schema('lsblk')
def _lsblk_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for lsblk command (list block devices)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': '-a/--all: print all devices',
            '--all': '--all/-a: print all devices',
            '-b': '-b/--bytes: print size in bytes',
            '--bytes': '--bytes/-b: print size in bytes',
            '-d': '-d/--nodeps: do not print slaves or holders',
            '--nodeps': '--nodeps/-d: do not print slaves or holders',
            '-D': '-D/--discard: print discard capabilities',
            '--discard': '--discard/-D: print discard capabilities',
            '-e': '-e/--exclude: exclude devices by major number',
            '--exclude': '--exclude/-e: exclude devices by major number',
            '-f': '-f/--fs: output info about filesystems',
            '--fs': '--fs/-f: output info about filesystems',
            '-i': '-i/--ascii: use ASCII characters only',
            '--ascii': '--ascii/-i: use ASCII characters only',
            '-I': '-I/--include: show only devices with specified major numbers',
            '--include': '--include/-I: show only devices with specified major numbers',
            '-l': '-l/--list: use list format output',
            '--list': '--list/-l: use list format output',
            '-m': '-m/--perms: output info about permissions',
            '--perms': '--perms/-m: output info about permissions',
            '-n': '-n/--noheadings: do not print headings',
            '--noheadings': '--noheadings/-n: do not print headings',
            '-o': '-o/--output: specify output columns',
            '--output': '--output/-o: specify output columns',
            '-O': '-O/--output-all: output all available columns',
            '--output-all': '--output-all/-O: output all available columns',
            '-p': '-p/--paths: print complete device path',
            '--paths': '--paths/-p: print complete device path',
            '-P': '-P/--pairs: use key="value" output format',
            '--pairs': '--pairs/-P: use key="value" output format',
            '-r': '-r/--raw: use raw output format',
            '--raw': '--raw/-r: use raw output format',
            '-s': '-s/--inverse: inverse dependencies',
            '--inverse': '--inverse/-s: inverse dependencies',
            '-t': '-t/--topology: output info about topology',
            '--topology': '--topology/-t: output info about topology',
            '-S': '-S/--scsi: output SCSI device info',
            '--scsi': '--scsi/-S: output SCSI device info',
            '-x': '-x/--sort: sort output by column',
            '--sort': '--sort/-x: sort output by column',
            '-h': '-h/--help: display help',
            '--help': '--help/-h: display help',
            '-V': '-V/--version: display version',
            '--version': '--version/-V: display version',
        }
    return None


@register_completion_schema('pv')
def _pv_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for pv command (pipe viewer / progress monitor)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-p': '-p/--progress: show progress bar',
            '--progress': '--progress/-p: show progress bar',
            '-t': '-t/--timer: show elapsed time',
            '--timer': '--timer/-t: show elapsed time',
            '-e': '-e/--eta: show estimated time of arrival',
            '--eta': '--eta/-e: show estimated time of arrival',
            '-I': '-I/--fineta: show absolute estimated time of arrival',
            '--fineta': '--fineta/-I: show absolute estimated time of arrival',
            '-r': '-r/--rate: show data transfer rate',
            '--rate': '--rate/-r: show data transfer rate',
            '-a': '-a/--average-rate: show average data transfer rate',
            '--average-rate': '--average-rate/-a: show average data transfer rate',
            '-b': '-b/--bytes: show total bytes transferred',
            '--bytes': '--bytes/-b: show total bytes transferred',
            '-T': '-T/--buffer-percent: show percentage of transfer buffer in use',
            '--buffer-percent': '--buffer-percent/-T: show percentage of transfer buffer in use',
            '-A': '-A/--last-written: show last bytes written (continuous update)',
            '--last-written': '--last-written/-A: show last bytes written (continuous update)',
            '-n': '-n/--numeric: numeric output only (for parsing)',
            '--numeric': '--numeric/-n: numeric output only (for parsing)',
            '-q': '-q/--quiet: do not output any information',
            '--quiet': '--quiet/-q: do not output any information',
            '-W': '-W/--wait: wait until first byte transferred',
            '--wait': '--wait/-W: wait until first byte transferred',
            '-D': '-D/--delay-start: delay showing progress for N seconds',
            '--delay-start': '--delay-start/-D: delay showing progress for N seconds',
            '-s': '-s/--size: set size to SIZE bytes',
            '--size': '--size/-s: set size to SIZE bytes',
            '-l': '-l/--line-mode: count lines instead of bytes',
            '--line-mode': '--line-mode/-l: count lines instead of bytes',
            '-0': '-0/--null: count null-terminated lines',
            '--null': '--null/-0: count null-terminated lines',
            '-i': '-i/--interval: update interval in seconds',
            '--interval': '--interval/-i: update interval in seconds',
            '-w': '-w/--width: assume terminal width of N characters',
            '--width': '--width/-w: assume terminal width of N characters',
            '-H': '-H/--height: assume terminal height of N rows',
            '--height': '--height/-H: assume terminal height of N rows',
            '-N': '-N/--name: prefix output with given name',
            '--name': '--name/-N: prefix output with given name',
            '-f': '-f/--force: force output (to non-terminal)',
            '--force': '--force/-f: force output (to non-terminal)',
            '-c': '-c/--cursor: use cursor positioning escape sequences',
            '--cursor': '--cursor/-c: use cursor positioning escape sequences',
            '-L': '-L/--rate-limit: limit transfer to RATE bytes/sec',
            '--rate-limit': '--rate-limit/-L: limit transfer to RATE bytes/sec',
            '-B': '-B/--buffer-size: use buffer size of N bytes',
            '--buffer-size': '--buffer-size/-B: use buffer size of N bytes',
            '-C': '-C/--no-splice: never use splice()',
            '--no-splice': '--no-splice/-C: never use splice()',
            '-E': '-E/--skip-errors: skip read errors in input',
            '--skip-errors': '--skip-errors/-E: skip read errors in input',
            '-S': '-S/--stop-at-size: stop after --size bytes',
            '--stop-at-size': '--stop-at-size/-S: stop after --size bytes',
            '-R': '-R/--remote: update settings of remote PV process',
            '--remote': '--remote/-R: update settings of remote PV process',
            '-P': '-P/--pidfile: save process ID in file',
            '--pidfile': '--pidfile/-P: save process ID in file',
            '-d': '-d/--watchfd: watch file descriptor N',
            '--watchfd': '--watchfd/-d: watch file descriptor N',
            '-h': '-h/--help: show help',
            '--help': '--help/-h: show help',
            '-V': '-V/--version: show version',
            '--version': '--version/-V: show version',
        }
    return None


@register_completion_schema('gdu')
def _gdu_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for gdu command (disk usage analyzer)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': '-a/--show-apparent-size: show apparent size',
            '--show-apparent-size': '--show-apparent-size/-a: show apparent size',
            '-c': '-c/--no-color: disable colors',
            '--no-color': '--no-color/-c: disable colors',
            '-i': '-i/--ignore-dirs: ignore directories matching pattern',
            '--ignore-dirs': '--ignore-dirs/-i: ignore directories matching pattern',
            '-I': '-I/--ignore-dirs-pattern: ignore dirs matching regex',
            '--ignore-dirs-pattern': '--ignore-dirs-pattern/-I: ignore dirs matching regex',
            '-X': '-X/--ignore-from: read ignore patterns from file',
            '--ignore-from': '--ignore-from/-X: read ignore patterns from file',
            '-H': '-H/--ignore-hidden: ignore hidden directories',
            '--ignore-hidden': '--ignore-hidden/-H: ignore hidden directories',
            '-l': '-l/--log-file: save errors to file',
            '--log-file': '--log-file/-l: save errors to file',
            '-m': '-m/--max-cores: set max cores to use',
            '--max-cores': '--max-cores/-m: set max cores to use',
            '-n': '-n/--non-interactive: non-interactive mode',
            '--non-interactive': '--non-interactive/-n: non-interactive mode',
            '-x': '-x/--exclude-from: exclude directories from file',
            '--exclude-from': '--exclude-from/-x: exclude directories from file',
            '-d': '-d/--delete-in-background: delete in background',
            '--delete-in-background': '--delete-in-background/-d: delete in background',
            '-p': '-p/--no-progress: disable progress bar',
            '--no-progress': '--no-progress/-p: disable progress bar',
            '-s': '-s/--summarize: show only total in non-interactive mode',
            '--summarize': '--summarize/-s: show only total in non-interactive mode',
            '-g': '-g/--no-cross: do not cross filesystem boundaries',
            '--no-cross': '--no-cross/-g: do not cross filesystem boundaries',
            '-C': '-C/--no-mouse: disable mouse support',
            '--no-mouse': '--no-mouse/-C: disable mouse support',
            '-r': '-r/--read-from-file: read analysis from JSON file',
            '--read-from-file': '--read-from-file/-r: read analysis from JSON file',
            '-f': '-f/--input-file: import analysis from JSON',
            '--input-file': '--input-file/-f: import analysis from JSON',
            '-o': '-o/--output-file: export analysis to JSON',
            '--output-file': '--output-file/-o: export analysis to JSON',
            '--write-config': 'write current config to file',
            '--read-config': 'read config from file',
            '--use-storage': 'use persistent key-value storage for analysis data',
            '--storage-path': 'path to persistent key-value storage directory',
            '-v': '-v/--version: print version',
            '--version': '--version/-v: print version',
            '-h': '-h/--help: print help',
            '--help': '--help/-h: print help',
        }
    return None


@register_completion_schema('ncdu')
def _ncdu_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ncdu command (NCurses disk usage)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-0': 'scan with full progress but no UI',
            '-1': 'single-line minimal UI',
            '-2': 'full UI with file counts',
            '-q': '-q/--slow-ui-updates: slower UI updates for remote connections',
            '--slow-ui-updates': '--slow-ui-updates/-q: slower UI updates for remote connections',
            '-r': '-r/--read-only: read-only mode',
            '--read-only': '--read-only/-r: read-only mode',
            '-o': '-o/--output: export scan to file',
            '--output': '--output/-o: export scan to file',
            '-f': '-f/--input: import scan from file',
            '--input': '--input/-f: import scan from file',
            '-x': 'same filesystem only',
            '-e': 'enable extended information',
            '--extended': 'enable extended information mode',
            '-X': '-X/--exclude: exclude files matching pattern',
            '--exclude': '--exclude/-X: exclude files matching pattern',
            '--exclude-from': 'exclude files matching patterns in file',
            '--exclude-caches': 'exclude directories containing CACHEDIR.TAG',
            '--exclude-kernfs': 'exclude Linux kernel filesystems',
            '--follow-symlinks': 'follow symbolic links',
            '--enable-shell': 'enable shell command execution',
            '--disable-shell': 'disable shell command execution',
            '--enable-delete': 'enable file deletion',
            '--disable-delete': 'disable file deletion',
            '--enable-refresh': 'enable refresh/recalculation',
            '--disable-refresh': 'disable refresh/recalculation',
            '--color': 'color scheme (off/dark/dark-bg)',
            '--confirm-quit': 'confirm before quitting',
            '--confirm-delete': 'confirm before deleting',
            '-L': '-L/--follow-symlinks: follow symlinks',
            '--si': 'use base 10 (SI) prefixes',
            '--disk-usage': 'show disk usage instead of apparent size',
            '--apparent-size': 'show apparent size instead of disk usage',
            '-h': '-h/--help: show help',
            '--help': '--help/-h: show help',
            '-v': '-v/--version: show version',
            '--version': '--version/-v: show version',
        }
    return None


@register_completion_schema('jq')
def _jq_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for jq (JSON processor)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-r': '-r/--raw-output: output raw strings, not JSON texts',
            '--raw-output': '--raw-output/-r: output raw strings, not JSON texts',
            '-c': '-c/--compact-output: compact instead of pretty-printed output',
            '--compact-output': '--compact-output/-c: compact instead of pretty-printed output',
            '-n': '-n/--null-input: use null as input value',
            '--null-input': '--null-input/-n: use null as input value',
            '-e': '-e/--exit-status: set exit status based on output',
            '--exit-status': '--exit-status/-e: set exit status based on output',
            '-s': '-s/--slurp: read entire input stream into array',
            '--slurp': '--slurp/-s: read entire input stream into array',
            '-S': '-S/--sort-keys: sort object keys in output',
            '--sort-keys': '--sort-keys/-S: sort object keys in output',
            '-C': '-C/--color-output: colorize JSON output (default)',
            '--color-output': '--color-output/-C: colorize JSON output (default)',
            '-M': '-M/--monochrome-output: disable colored output',
            '--monochrome-output': '--monochrome-output/-M: disable colored output',
            '-j': '-j/--join-output: no newlines after each output',
            '--join-output': '--join-output/-j: no newlines after each output',
            '-a': '-a/--ascii-output: force ASCII output',
            '--ascii-output': '--ascii-output/-a: force ASCII output',
            '--arg': 'pass a string value as a variable ($name)',
            '--argjson': 'pass a JSON value as a variable ($name)',
            '--slurpfile': 'read JSON objects from file into variable',
            '--rawfile': 'read raw text from file into variable',
            '--args': 'remaining arguments are positional string arguments',
            '--jsonargs': 'remaining arguments are positional JSON arguments',
            '-f': '-f/--from-file: read program from file',
            '--from-file': '--from-file/-f: read program from file',
            '-L': 'prepend directory to module search path',
            '--tab': 'use tabs for indentation',
            '--indent': 'use N spaces for indentation (default 2)',
            '--stream': 'parse input in streaming fashion',
            '--seq': 'use application/json-seq MIME type',
            '--help': 'show help message',
            '--version': 'show jq version',
        }
    return None


@register_completion_schema('sqlite3')
def _sqlite3_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for sqlite3 database tool."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '--': 'treat subsequent arguments as non-options',
            '-A': 'run ".archive" command',
            '-append': 'append database to file',
            '-ascii': 'set output mode to ascii',
            '-bail': 'stop after hitting an error',
            '-batch': 'force batch I/O',
            '-box': 'set output mode to box',
            '-column': 'set output mode to column',
            '-cmd': 'run command before reading stdin',
            '-csv': 'set output mode to csv',
            '-deserialize': 'open database using sqlite3_deserialize()',
            '-echo': 'print commands before execution',
            '-init': 'read/process named file for initialization',
            '-header': 'turn headers on',
            '-noheader': 'turn headers off',
            '-help': 'show help message',
            '-hexkey': 'specify hexadecimal encryption key',
            '-html': 'set output mode to html',
            '-interactive': 'force interactive I/O',
            '-key': 'specify encryption key',
            '-json': 'set output mode to json',
            '-line': 'set output mode to line',
            '-list': 'set output mode to list',
            '-lookaside': 'configure lookaside memory allocator',
            '-markdown': 'set output mode to markdown',
            '-maxsize': 'maximum size for --deserialize',
            '-memtrace': 'trace all memory allocations',
            '-newline': 'set output row separator',
            '-nofollow': 'refuse to open symbolic links to database files',
            '-nonce': 'set nonce for decryption',
            '-nullvalue': 'set text string for NULL values',
            '-pagecache': 'configure page cache memory',
            '-pcachetrace': 'trace page cache activity',
            '-quote': 'set output mode to quote',
            '-readonly': 'open database in read-only mode',
            '-safe': 'enable safe mode',
            '-separator': 'set output field separator',
            '-stats': 'print memory stats before exit',
            '-table': 'set output mode to table',
            '-tabs': 'set output mode to tabs',
            '-version': 'show SQLite version',
            '-vfs': 'specify VFS to use',
            '-vtrace': 'trace VFS calls',
            '-zip': 'open database as a ZIP archive',
        }
    return None


@register_completion_schema('rg')
def _rg_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for rg (ripgrep)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-i': '-i/--ignore-case: case insensitive search',
            '--ignore-case': '--ignore-case/-i: case insensitive search',
            '-s': '-s/--case-sensitive: case sensitive search',
            '--case-sensitive': '--case-sensitive/-s: case sensitive search',
            '-S': '-S/--smart-case: smart case (insensitive unless uppercase present)',
            '--smart-case': '--smart-case/-S: smart case (insensitive unless uppercase present)',
            '-v': '-v/--invert-match: invert matching (show non-matching lines)',
            '--invert-match': '--invert-match/-v: invert matching (show non-matching lines)',
            '-w': '-w/--word-regexp: only show matches surrounded by word boundaries',
            '--word-regexp': '--word-regexp/-w: only show matches surrounded by word boundaries',
            '-x': '-x/--line-regexp: only show matches of entire line',
            '--line-regexp': '--line-regexp/-x: only show matches of entire line',
            '-e': 'specify pattern to search for (can be repeated)',
            '-g': 'include/exclude files matching glob pattern',
            '--glob': 'include/exclude files matching glob pattern',
            '-t': 'only search files matching TYPE (e.g., -t py)',
            '--type': 'only search files matching TYPE',
            '-T': 'do not search files matching TYPE',
            '--type-not': 'do not search files matching TYPE',
            '-l': '-l/--files-with-matches: only print filenames with matches',
            '--files-with-matches': '--files-with-matches/-l: only print filenames with matches',
            '--files': 'print each file that would be searched',
            '-c': '-c/--count: only show count of matches per file',
            '--count': '--count/-c: only show count of matches per file',
            '-A': 'show NUM lines after each match',
            '--after-context': 'show NUM lines after each match',
            '-B': 'show NUM lines before each match',
            '--before-context': 'show NUM lines before each match',
            '-C': 'show NUM lines before and after each match',
            '--context': 'show NUM lines before and after each match',
            '-n': '-n/--line-number: show line numbers (default)',
            '--line-number': '--line-number/-n: show line numbers (default)',
            '-N': '-N/--no-line-number: suppress line numbers',
            '--no-line-number': '--no-line-number/-N: suppress line numbers',
            '-H': '-H/--with-filename: print filename with matches (default)',
            '--with-filename': '--with-filename/-H: print filename with matches (default)',
            '--no-filename': 'never print filename with matches',
            '-h': 'do not print filename with matches',
            '--hidden': 'search hidden files and directories',
            '--no-hidden': 'do not search hidden files (default)',
            '--follow': 'follow symbolic links',
            '-L': '-L/--follow: follow symbolic links',
            '-a': '-a/--text: search binary files as text',
            '--text': '--text/-a: search binary files as text',
            '--binary': 'search binary files (off by default)',
            '-z': '-z/--search-zip: search compressed files (gzip, bzip2, etc)',
            '--search-zip': '--search-zip/-z: search compressed files',
            '-u': 'reduce level of "smart" filtering (can be repeated: -uu, -uuu)',
            '-F': '-F/--fixed-strings: treat pattern as literal string, not regex',
            '--fixed-strings': '--fixed-strings/-F: treat pattern as literal string, not regex',
            '--no-ignore': 'do not respect .gitignore files',
            '--no-ignore-vcs': 'do not respect VCS ignore files',
            '-M': 'do not print lines longer than NUM bytes',
            '--max-columns': 'do not print lines longer than NUM bytes',
            '-m': 'limit matches per file to NUM',
            '--max-count': 'limit matches per file to NUM',
            '-r': '-r/--replace: replace matches with string',
            '--replace': '--replace/-r: replace matches with string',
            '-o': '-o/--only-matching: print only matched parts',
            '--only-matching': '--only-matching/-o: print only matched parts',
            '-q': '-q/--quiet: do not print matches',
            '--quiet': '--quiet/-q: do not print matches',
            '--color': 'control when to use colors (never, auto, always, ansi)',
            '--colors': 'configure color settings',
            '-p': '-p/--pretty: alias for --color=always -n -H',
            '--pretty': '--pretty/-p: alias for --color=always -n -H',
            '-j': 'use NUM threads (default: available CPUs)',
            '--threads': 'use NUM threads',
            '--sort': 'sort results by path, modified, accessed, or created',
            '--sortr': 'sort results in reverse',
            '--stats': 'print statistics about search',
            '--json': 'print results in JSON format',
            '--help': 'show help message',
            '--version': 'show ripgrep version',
        }
    return None


@register_completion_schema('fzf')
def _fzf_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for fzf (fuzzy finder)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-m': '-m/--multi: enable multi-select with tab/shift-tab',
            '--multi': '--multi/-m: enable multi-select with tab/shift-tab',
            '-x': '-x/--extended: extended search mode (default)',
            '--extended': '--extended/-x: extended search mode (default)',
            '-e': '-e/--exact: enable exact-match mode',
            '--exact': '--exact/-e: enable exact-match mode',
            '-i': 'case-insensitive match (default)',
            '+i': 'case-sensitive match',
            '--literal': 'do not normalize latin script letters',
            '-q': 'start with given query',
            '--query': 'start with given query',
            '-f': 'filter mode: print matching items and exit',
            '--filter': 'filter mode: print matching items and exit',
            '--height': 'display in given height (e.g., 40%)',
            '--min-height': 'minimum height when --height is given in percent',
            '--layout': 'layout: default, reverse, reverse-list',
            '--reverse': 'reverse layout (prompt at top)',
            '--border': 'draw border (rounded, sharp, horizontal, vertical, top, bottom, left, right, none)',
            '--margin': 'screen margin (TRBL format or all)',
            '--padding': 'padding inside border (TRBL format or all)',
            '--prompt': 'input prompt (default: "> ")',
            '--pointer': 'pointer to current line (default: ">")',
            '--marker': 'multi-select marker (default: ">")',
            '--header': 'header string',
            '--header-lines': 'first N lines as sticky header',
            '--preview': 'command to preview highlighted line',
            '--preview-window': 'preview window layout',
            '--ansi': 'enable processing of ANSI color codes',
            '--tabstop': 'number of spaces for tab character (default: 8)',
            '--color': 'color scheme (16, dark, light, or custom)',
            '--no-bold': 'do not use bold text',
            '--bind': 'custom key bindings (e.g., ctrl-j:accept)',
            '--cycle': 'enable cyclic scroll',
            '--keep-right': 'keep right end of line visible on overflow',
            '--no-hscroll': 'disable horizontal scroll',
            '--hscroll-off': 'number of columns to keep visible',
            '--filepath-word': 'make word-wise movements respect path separators',
            '--jump-labels': 'label characters for jump mode',
            '--tiebreak': 'comma-separated criteria (length, begin, end, index)',
            '--sync': 'synchronous search for multi-stage filtering',
            '--delimiter': 'field delimiter regex (default: AWK-style)',
            '-d': 'field delimiter regex',
            '--nth': 'comma-separated field indices for limiting search',
            '--with-nth': 'comma-separated field indices for display',
            '-n': 'comma-separated field indices for limiting search',
            '--algo': 'fuzzy matching algorithm (v1 or v2, default: v2)',
            '--expect': 'comma-separated keys that can be used to complete',
            '--read0': 'read input delimited with NULL character',
            '--print0': 'print output delimited with NULL character',
            '--print-query': 'print query as first line',
            '--no-mouse': 'disable mouse',
            '--help': 'show help message',
            '--version': 'show fzf version',
        }
    return None


@register_completion_schema('delta')
def _delta_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for delta (git diff pager)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-n': '-n/--line-numbers: show line numbers',
            '--line-numbers': '--line-numbers/-n: show line numbers',
            '-s': '-s/--side-by-side: display diffs side by side',
            '--side-by-side': '--side-by-side/-s: display diffs side by side',
            '--diff-highlight': 'emulate diff-highlight',
            '--diff-so-fancy': 'emulate diff-so-fancy',
            '--navigate': 'activate diff navigation (n/N keys)',
            '--show-syntax-themes': 'show available syntax highlighting themes',
            '--show-themes': 'show available delta themes',
            '--light': 'use default light theme',
            '--dark': 'use default dark theme',
            '--syntax-theme': 'syntax highlighting theme',
            '--line-numbers-left-format': 'format string for left line numbers',
            '--line-numbers-right-format': 'format string for right line numbers',
            '--line-numbers-left-style': 'style for left line numbers',
            '--line-numbers-right-style': 'style for right line numbers',
            '--line-numbers-minus-style': 'style for removed line numbers',
            '--line-numbers-plus-style': 'style for added line numbers',
            '--line-numbers-zero-style': 'style for unchanged line numbers',
            '--file-modified-label': 'text to display for modified files',
            '--file-added-label': 'text to display for added files',
            '--file-removed-label': 'text to display for removed files',
            '--file-renamed-label': 'text to display for renamed files',
            '--hunk-header-style': 'style for hunk headers',
            '--hunk-header-decoration-style': 'style for hunk header decorations',
            '--file-style': 'style for file headers',
            '--file-decoration-style': 'style for file header decorations',
            '--hyperlinks': 'render commit hashes as hyperlinks',
            '--hyperlinks-file-link-format': 'format for file hyperlinks',
            '--keep-plus-minus-markers': 'keep +/- markers in output',
            '--tabs': 'number of spaces to replace tabs with',
            '--width': 'width of output (default: terminal width)',
            '-w': '-w/--width: width of output',
            '--paging': 'paging mode (always, never, auto)',
            '--color-only': 'do not alter input structurally, only add colors',
            '--features': 'activate named features',
            '--inspect-raw-lines': 'display raw line bytes (debugging)',
            '--help': 'show help message',
            '--version': 'show delta version',
        }
    return None


@register_completion_schema('bat')
def _bat_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for bat (cat with syntax highlighting)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-l': '-l/--language: set syntax highlighting language',
            '--language': '--language/-l: set syntax highlighting language',
            '-n': '-n/--number: show line numbers',
            '--number': '--number/-n: show line numbers',
            '-p': '-p/--plain: disable paging and decorations (alias: --style=plain)',
            '--plain': '--plain/-p: disable paging and decorations',
            '-A': '-A/--show-all: show non-printable characters',
            '--show-all': '--show-all/-A: show non-printable characters',
            '--style': 'configure output style (auto, full, plain, changes, header, grid, rule, numbers, snip)',
            '--color': 'when to use colors (auto, never, always)',
            '--italic-text': 'use italics in output (always, never)',
            '--decorations': 'when to show decorations (auto, never, always)',
            '--paging': 'when to use pager (auto, never, always)',
            '-m': '-m/--map-syntax: map glob pattern to language',
            '--map-syntax': '--map-syntax/-m: map glob pattern to language',
            '--theme': 'set color theme for syntax highlighting',
            '--list-themes': 'list available themes',
            '--list-languages': 'list supported languages',
            '-r': 'only print lines NUM1:NUM2',
            '--line-range': 'only print lines NUM1:NUM2',
            '-H': 'highlight given line(s)',
            '--highlight-line': 'highlight given line(s)',
            '--file-name': 'specify file name to display (for stdin)',
            '-d': '-d/--diff: only show lines with git changes',
            '--diff': '--diff/-d: only show lines with git changes',
            '--diff-context': 'include N lines of context around diffs',
            '--tabs': 'set tab width to N spaces',
            '--wrap': 'text wrapping mode (auto, never, character)',
            '--terminal-width': 'explicitly set terminal width',
            '--no-config': 'do not use config file',
            '--config-file': 'use alternate config file',
            '--config-dir': 'use alternate config directory',
            '--cache-dir': 'use alternate cache directory',
            '--generate-config-file': 'generate default config file',
            '--acknowledgements': 'show acknowledgements',
            '-h': '-h/--help: show short help',
            '--help': '--help/-h: show detailed help message',
            '-V': '-V/--version: show version',
            '--version': '--version/-V: show version',
        }
    return None


@register_completion_schema('exa')
def _exa_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for exa (modern ls replacement)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-1': '-1/--oneline: display one entry per line',
            '--oneline': '--oneline/-1: display one entry per line',
            '-l': '-l/--long: display extended file metadata',
            '--long': '--long/-l: display extended file metadata',
            '-G': '-G/--grid: display entries as a grid (default)',
            '--grid': '--grid/-G: display entries as a grid (default)',
            '-x': '-x/--across: sort grid across, not downwards',
            '--across': '--across/-x: sort grid across, not downwards',
            '-R': '-R/--recurse: recurse into directories',
            '--recurse': '--recurse/-R: recurse into directories',
            '-T': '-T/--tree: recurse into directories as tree',
            '--tree': '--tree/-T: recurse into directories as tree',
            '-a': '-a/--all: show hidden and . files',
            '--all': '--all/-a: show hidden and . files',
            '-d': '-d/--list-dirs: list directories like regular files',
            '--list-dirs': '--list-dirs/-d: list directories like regular files',
            '-L': 'limit depth of recursion',
            '--level': 'limit depth of recursion',
            '-r': '-r/--reverse: reverse sort order',
            '--reverse': '--reverse/-r: reverse sort order',
            '-s': '-s/--sort: sort by field (name, size, extension, modified, etc)',
            '--sort': '--sort/-s: sort by field',
            '--group-directories-first': 'list directories before files',
            '--git-ignore': 'ignore files mentioned in .gitignore',
            '-I': 'ignore files matching glob pattern',
            '--ignore-glob': 'ignore files matching glob pattern',
            '-b': '-b/--binary: list file sizes with binary prefixes',
            '--binary': '--binary/-b: list file sizes with binary prefixes',
            '-B': '-B/--bytes: list file sizes in bytes',
            '--bytes': '--bytes/-B: list file sizes in bytes',
            '-h': '-h/--header: add header row',
            '--header': '--header/-h: add header row',
            '-H': '-H/--links: list file hard link count',
            '--links': '--links/-H: list file hard link count',
            '-i': '-i/--inode: list file inode number',
            '--inode': '--inode/-i: list file inode number',
            '--git': 'list file git status',
            '--no-git': 'suppress git status column',
            '-@': '-@/--extended: list file extended attributes',
            '--extended': '--extended/-@: list file extended attributes',
            '-t': 'sort by modified time',
            '--modified': 'sort by or display modified time',
            '-u': 'sort by accessed time',
            '--accessed': 'sort by or display accessed time',
            '-U': 'sort by created time',
            '--created': 'sort by or display created time',
            '--time': 'time field to show (modified, accessed, created)',
            '--time-style': 'time format style (default, iso, long-iso, full-iso)',
            '--color': 'when to use colors (always, auto, never)',
            '--color-scale': 'highlight file sizes by age',
            '--icons': 'display icons for file types',
            '--no-icons': 'do not display icons',
            '--help': 'show help message',
            '--version': 'show exa version',
        }
    return None


@register_completion_schema('ag')
def _ag_completions(tokens, cursor_token_idx, is_after):
    """Completion schema for ag (the silver searcher)."""
    if _is_flag_context(tokens, cursor_token_idx, is_after):
        return {
            '-a': '-a/--all-types: search all files (ignore .agignore)',
            '--all-types': '--all-types/-a: search all files (ignore .agignore)',
            '-A': 'print NUM lines after match',
            '--after': 'print NUM lines after match',
            '-B': 'print NUM lines before match',
            '--before': 'print NUM lines before match',
            '-C': 'print NUM lines before and after match',
            '--context': 'print NUM lines before and after match',
            '-c': '-c/--count: only print count of matches per file',
            '--count': '--count/-c: only print count of matches per file',
            '--color': 'print color codes in results (on by default)',
            '--nocolor': 'do not print color codes',
            '--color-line-number': 'color for line numbers (default 1;33)',
            '--color-match': 'color for match highlight (default 30;43)',
            '--color-path': 'color for file paths (default 1;32)',
            '-D': '-D/--debug: print debug messages',
            '--debug': '--debug/-D: print debug messages',
            '--depth': 'search up to NUM directories deep (default 25)',
            '-f': '-f/--follow: follow symlinks',
            '--follow': '--follow/-f: follow symlinks',
            '-F': '-F/--fixed-strings: alias for --literal',
            '--fixed-strings': '--fixed-strings/-F: alias for --literal',
            '-g': 'print filenames matching PATTERN',
            '-G': 'only search files matching PATTERN',
            '--file-search-regex': 'only search files matching PATTERN',
            '-H': '-H/--heading: print filename above matches (default)',
            '--heading': '--heading/-H: print filename above matches (default)',
            '--no-heading': 'print filename on each match line',
            '--hidden': 'search hidden files (disabled by default)',
            '-i': '-i/--ignore-case: match case insensitively',
            '--ignore-case': '--ignore-case/-i: match case insensitively',
            '-s': '-s/--case-sensitive: match case sensitively',
            '--case-sensitive': '--case-sensitive/-s: match case sensitively',
            '-S': '-S/--smart-case: match case sensitively if pattern has uppercase',
            '--smart-case': '--smart-case/-S: match case sensitively if pattern has uppercase',
            '--ignore': 'ignore files/directories matching pattern',
            '-l': '-l/--files-with-matches: only print filenames with matches',
            '--files-with-matches': '--files-with-matches/-l: only print filenames with matches',
            '-L': '-L/--files-without-matches: only print filenames without matches',
            '--files-without-matches': '--files-without-matches/-L: only print filenames without matches',
            '--literal': 'match PATTERN literally (no regex)',
            '-m': 'skip rest of file after NUM matches',
            '--max-count': 'skip rest of file after NUM matches',
            '--numbers': 'print line numbers (default)',
            '--no-numbers': 'do not print line numbers',
            '-o': '-o/--only-matching: print only matching part',
            '--only-matching': '--only-matching/-o: print only matching part',
            '--print-long-lines': 'print matches on long lines (>2k chars)',
            '-p': 'search path to FILE for ignore patterns',
            '--path-to-ignore': 'search path to FILE for ignore patterns',
            '-Q': '-Q/--literal: alias for --literal',
            '--literal': '--literal/-Q: match pattern literally',
            '-r': '-r/--recurse: recurse into directories (default)',
            '--recurse': '--recurse/-r: recurse into directories (default)',
            '-R': '-R/--no-recurse: do not recurse into directories',
            '--no-recurse': '--no-recurse/-R: do not recurse into directories',
            '--search-binary': 'search binary files for matches',
            '--stats': 'print stats (files scanned, time taken, etc)',
            '--stats-only': 'print stats and nothing else',
            '-t': 'search files with type TYPE',
            '--type': 'search files with type TYPE',
            '-u': '-u/--unrestricted: search all files (ignore .agignore, .gitignore)',
            '--unrestricted': '--unrestricted/-u: search all files',
            '-U': '-U/--skip-vcs-ignores: ignore VCS ignore files (.gitignore)',
            '--skip-vcs-ignores': '--skip-vcs-ignores/-U: ignore VCS ignore files',
            '-v': '-v/--invert-match: invert match',
            '--invert-match': '--invert-match/-v: invert match',
            '-w': '-w/--word-regexp: only match whole words',
            '--word-regexp': '--word-regexp/-w: only match whole words',
            '-W': 'show NUM characters of context around match',
            '--width': 'show NUM characters of context around match',
            '-z': '-z/--search-zip: search contents of compressed files',
            '--search-zip': '--search-zip/-z: search contents of compressed files',
            '--parallel': 'parse and search in parallel',
            '--no-parallel': 'do not parse and search in parallel',
            '--help': 'show help message',
            '--version': 'show ag version',
        }
    return None
