"""
Shared path completion utilities for rp's pseudo-terminal.

This module provides a clean, DRY implementation of path completion based on
best practices from vanilla ptpython's PathCompleter.

BUGS FIXED from the old system (completer_git_original.py):
==============================================================

1. INCONSISTENT PATH EXTRACTION (lines 299-324)
   OLD BUG: get_path_before_cursor() used split()[0] which broke on:
            - Paths with spaces (even quoted)
            - Multiple arguments after command
            - Edge cases with trailing/leading whitespace
   FIX: Use basename/dirname splitting like prompt_toolkit does

2. PATH MODIFICATION CONFUSION (lines 274-288)
   OLD BUG: pathmod() recursively calls itself on strings AND DirEntry objects
            with confusing logic about when to strip './' prefix
   FIX: Separate concerns - one function extracts paths from DirEntry,
        another formats completion text

3. NO TILDE EXPANSION
   OLD BUG: Commands like "CD ~/Doc" wouldn't complete properly
   FIX: Add expanduser() support like prompt_toolkit PathCompleter

4. HIDDEN FILE HANDLING INCONSISTENT (lines 828-835, 853-855)
   OLD BUG: Complex, brittle logic with multiple edge cases for ./paths
            Tried to strip ./ prefix but only in certain conditions
            Hidden files (.git, .bashrc) had hacky special handling
   FIX: Clean prefix-based matching - if user types ".", show hidden files
        If user types "./", handle it properly

5. SLASH HANDLING BUGS (lines 838-852)
   OLD BUG: Added/removed slashes inconsistently:
            - Stripped trailing slash from text completion
            - But only if '/' in origin (line 849-851)
            - Different behavior for before_line.endswith('/')
   FIX: Consistent slash handling - display shows /, completion doesn't add it

6. POOR ERROR HANDLING (lines 328-334)
   OLD BUG: Silent fallback to '.' on any path error
            Catches broad exception types but returns empty list
   FIX: Explicit exception handling with clear fallback behavior

7. MIXED CONCERNS
   OLD BUG: Path completion logic mixed with:
            - Sorting/priority logic
            - Display formatting
            - Origin/candidate matching
   FIX: Clean separation - this module ONLY handles path extraction/listing

8. NO FILTERING SUPPORT
   OLD BUG: File vs directory filtering scattered across different commands
            Repeated logic like "x.is_dir()" and "is_a_file(x)"
   FIX: files_only/dirs_only parameters like prompt_toolkit

ARCHITECTURE:
=============
This module provides low-level path utilities. The completer classes use these
to build Completion objects. We follow prompt_toolkit's design:

1. extract_path_components() - Parse user input into (directory, prefix)
2. list_path_candidates() - List matching files/dirs from filesystem
3. format_completion_text() - Format candidate for insertion
4. format_display_text() - Format candidate for display

Usage Example:
==============
    >>> from path_completion_utils import extract_path_components, list_path_candidates
    >>> directory, prefix = extract_path_components("CD ~/Doc", "CD ")
    >>> directory
    '/Users/ryan'
    >>> prefix
    'Doc'
    >>> candidates = list_path_candidates(directory, prefix, dirs_only=True)
    >>> [(c.name, c.is_dir) for c in candidates]
    [('Documents', True), ('Downloads', True)]
"""

from __future__ import unicode_literals
import os
from collections import namedtuple

__all__ = [
    'PathCandidate',
    'extract_path_components',
    'list_path_candidates',
    'format_completion_text',
    'format_display_text',
    'is_text_file_fast',
]

# Runtime caches for discovered extensions
_cached_text_extensions = {'.py', '.txt', '.md', '.js', '.ts', '.jsx', '.tsx', '.html', '.css',
                           '.scss', '.json', '.yaml', '.yml', '.xml', '.sh', '.bash', '.zsh',
                           '.c', '.cpp', '.h', '.hpp', '.java', '.rs', '.go', '.rb', '.php',
                           '.sql', '.r', '.R', '.vim', '.lua', '.pl', '.swift', '.kt', '.scala',
                           '.tex', '.rst', '.toml', '.ini', '.cfg', '.conf', '.log', '.rpy',
                           '.sass', '.less', '.coffee', '.dart', '.m', '.mm', '.cs', '.vb',
                           '.pas', '.f90', '.f95', '.hs', '.ml', '.ex', '.exs', '.clj', '.erl'}
_cached_binary_extensions = {'.pyc', '.pyo', '.so', '.dylib', '.dll', '.exe', '.bin', '.o',
                             '.a', '.lib', '.obj', '.class', '.jar', '.war', '.ear',
                             '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp',
                             '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm',
                             '.mp3', '.wav', '.ogg', '.flac', '.m4a', '.wma',
                             '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar',
                             '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                             '.db', '.sqlite', '.sqlite3', '.pkl', '.pickle', '.npy', '.npz',
                             '.ttf', '.otf', '.woff', '.woff2', '.eot', '.tiff', '.tif'}

def is_text_file_fast(path):
    """
    Fast text file detection with runtime caching of discovered extensions.
    Once we check a .tiff file and find it's binary, we never check .tiff again.

    Returns True for text files, False for binary files.
    """
    import rp
    name = os.path.basename(path)
    name_lower = name.lower()
    ext = rp.get_file_extension(name)

    # Check cached extensions first
    if ext and ext in _cached_text_extensions:
        return True
    if ext and ext in _cached_binary_extensions:
        return False

    # Name whitelist - extensionless text files
    text_names = {'makefile', 'dockerfile', 'rakefile', 'readme', 'license',
                  'changelog', 'authors', 'contributors', 'gemfile', 'vagrantfile',
                  'procfile', 'brewfile', 'cmakelists.txt'}
    if name_lower in text_names:
        return True

    # Dotfiles are usually text (config files)
    if name.startswith('.') and not name.startswith('..'):
        return True

    # Name blacklist - known binary files without extensions
    binary_names = {'a.out'}
    if name_lower in binary_names:
        return False

    # Unknown extension - use actual file content check and cache result
    try:
        is_text = rp.is_utf8_file(path)
        if ext:  # Cache the result for this extension
            if is_text:
                _cached_text_extensions.add(ext)
            else:
                _cached_binary_extensions.add(ext)
        return is_text
    except:
        if ext:  # Cache as binary if we can't read it
            _cached_binary_extensions.add(ext)
        return False


# Use namedtuple instead of typing.NamedTuple to avoid typing module conflicts
PathCandidate = namedtuple('PathCandidate', ['name', 'full_path', 'is_dir', 'is_text_file'])
PathCandidate.__doc__ = """
A path completion candidate.

Attributes:
    name: Just the filename/dirname (no path components)
    full_path: Absolute path to the entry
    is_dir: Whether this is a directory
    is_text_file: Whether this is a text file (None if not checked)
"""
# Set default for is_text_file to None
PathCandidate.__new__.__defaults__ = (None,)


def extract_path_components(text, command_prefix='', expanduser=True):
    """
    Extract directory and prefix from user input text.

    This is the core path parsing function, based on prompt_toolkit's approach.

    Args:
        text: The text before cursor (e.g., "CD ~/Doc" or "/usr/local/b")
        command_prefix: Optional command to strip (e.g., "CD ", "CAT ")
        expanduser: Whether to expand ~ to home directory

    Returns:
        (directory, prefix) tuple where:
        - directory: The directory to search in (defaults to '.')
        - prefix: The text to match against filenames

    Examples:
        >>> extract_path_components("CD ~/Documents/proj")
        ('/Users/ryan/Documents', 'proj')

        >>> extract_path_components("CAT /usr/local/b")
        ('/usr/local', 'b')

        >>> extract_path_components("VIM ./file")
        ('.', 'file')

        >>> extract_path_components("CD ")
        ('.', '')
    """
    # Strip command prefix if provided
    if command_prefix and text.startswith(command_prefix):
        text = text[len(command_prefix):]

    # Strip leading/trailing whitespace from path part
    text = text.lstrip()

    # Do tilde expansion FIRST (like prompt_toolkit does)
    if expanduser:
        text = os.path.expanduser(text)

    # Now split into directory and prefix using os.path functions
    # This is the KEY insight from prompt_toolkit - let os.path do the work!
    dirname = os.path.dirname(text)
    prefix = os.path.basename(text)

    # If no directory specified, use current directory
    if not dirname:
        directory = '.'
    else:
        directory = dirname

    return directory, prefix


def list_path_candidates(
    directory,
    prefix='',
    files_only=False,
    dirs_only=False,
    show_hidden=None,
    check_text_files=False
):
    """
    List filesystem entries matching the given prefix.

    Args:
        directory: Directory to search in
        prefix: Filename prefix to match (case-sensitive)
        files_only: Only return files (not directories)
        dirs_only: Only return directories (not files)
        show_hidden: Whether to show hidden files (starting with .)
                    If None, auto-detect from prefix (show if prefix starts with .)
        check_text_files: Whether to check if files are text files (for VIM prioritization)
                         Default False to avoid unnecessary I/O

    Returns:
        List of PathCandidate objects, sorted by name

    Examples:
        >>> list_path_candidates('/usr', 'loc')
        [PathCandidate(name='local', full_path='/usr/local', is_dir=True, is_text_file=None)]

        >>> list_path_candidates('.', '', dirs_only=True)
        [PathCandidate(name='src', ...), PathCandidate(name='tests', ...)]
    """
    # Auto-detect hidden file preference from prefix
    if show_hidden is None:
        show_hidden = prefix.startswith('.')

    candidates = []

    try:
        # Use os.scandir for efficiency (like the old code did)
        with os.scandir(directory) as entries:
            for entry in entries:
                name = entry.name

                # Skip hidden files unless explicitly requested
                if not show_hidden and name.startswith('.'):
                    continue

                # Check prefix match (case-sensitive, like bash)
                if not name.startswith(prefix):
                    continue

                # Check file/dir filtering
                try:
                    is_dir = entry.is_dir()
                except OSError:
                    # Broken symlink or permission issue
                    continue

                if files_only and is_dir:
                    continue
                if dirs_only and not is_dir:
                    continue

                # Build full path for the candidate
                full_path = os.path.join(directory, name)

                # Optionally check if it's a text file
                is_text = None
                if check_text_files and not is_dir:
                    is_text = is_text_file_fast(full_path)

                candidates.append(PathCandidate(
                    name=name,
                    full_path=full_path,
                    is_dir=is_dir,
                    is_text_file=is_text
                ))

    except (OSError, PermissionError, FileNotFoundError, NotADirectoryError, ValueError):
        # Directory doesn't exist, no permission, or invalid path
        # Return empty list (don't crash completion)
        return []

    # Sort by name (case-sensitive, like bash)
    candidates.sort(key=lambda c: c.name)

    return candidates


def format_completion_text(candidate, prefix, include_slash=False):
    """
    Format the completion text to insert.

    Args:
        candidate: The PathCandidate to format
        prefix: The prefix that was matched (to compute what to insert)
        include_slash: Whether to include trailing slash for directories

    Returns:
        Text to insert after the cursor

    Examples:
        >>> c = PathCandidate('Documents', '/Users/ryan/Documents', True)
        >>> format_completion_text(c, 'Doc')
        'uments'

        >>> format_completion_text(c, 'Doc', include_slash=True)
        'uments/'
    """
    # The completion is everything AFTER the prefix
    # prompt_toolkit does: completion = filename[len(prefix):]
    completion = candidate.name[len(prefix):]

    # Optionally add slash for directories (for display, not insertion)
    if include_slash and candidate.is_dir:
        completion += '/'

    return completion


def format_display_text(candidate, show_slash=True):
    """
    Format the display text shown in completion menu.

    Args:
        candidate: The PathCandidate to format
        show_slash: Whether to show trailing slash for directories

    Returns:
        Text to display in completion menu

    Examples:
        >>> c = PathCandidate('Documents', '/Users/ryan/Documents', True)
        >>> format_display_text(c)
        'Documents/'

        >>> format_display_text(c, show_slash=False)
        'Documents'
    """
    display = candidate.name

    # Add slash for visual indication (like prompt_toolkit does)
    if show_slash and candidate.is_dir:
        display += '/'

    return display


def get_path_before_cursor_simple(before_line, command_prefix=''):
    """
    DEPRECATED: Use extract_path_components() instead.

    Simple helper that extracts just the directory from before_line.
    Kept for backward compatibility but prefer the new API.
    """
    directory, _ = extract_path_components(before_line, command_prefix)
    return directory
