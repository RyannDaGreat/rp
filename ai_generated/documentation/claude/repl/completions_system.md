# RP Completions System Deep Dive

## Overview
The RP completions system (`rp_ptpython/completer.py`) is a sophisticated, multi-layered autocompletion engine that goes far beyond standard Python completions.

## Architecture

### Core Components

1. **PythonCompleter Class** (`completer.py`)
   - Main completion engine
   - Integrates multiple completion sources
   - Smart caching system

2. **Completion Cache** (`completion_cache_pre_origin_doc`)
   - Caches completions by document prefix
   - 7x speedup over uncached
   - Dynamic programming optimization

3. **Ryan's Matching Algorithm** (`ryan_completion_matches`)
   - Custom fuzzy matching for Python namespaces
   - Prioritizes user-created variables
   - Case-insensitive with case preference

## Completion Sources

### 1. Command-Specific Completions

#### CD Command Family
```python
if starts_with_any(before_line,'CD '):
    yield from yield_from_candidates(
        *pathsmod(x for x in scandir_path_before_cursor() if x.is_dir())
    )
```
- Only shows directories
- Smart path scanning
- Handles spaces in paths

#### TAKE Command
```python
if starts_with_any(before_line,'TAKE '):
    # Similar to CD but for creating directories
```

#### CDH (History) Commands
```python
if starts_with_any(before_line,'CDH '):
    # Shows directory history
    # Special handling for 'CDH GIT' to find git repos
```

### 2. File Path Completions

#### LS Commands
```python
if starts_with_any(before_line,'LS '):
    # Shows all files and directories
    # Prioritizes directories
```

#### RUN Command
```python
if before_line.startswith('RUN '):
    # Only shows .py and .rpy files
```

### 3. Shell Command Completions

#### Bang Commands (!)
```python
if before_line.startswith('!'):
    if before_line.startswith('!sudo apt install'):
        yield from yield_from_candidates(get_apt_completions())
    else:
        # Shows system commands from PATH
```

### 4. APT Package Completions
- Caches list of ~60,000 Ubuntu packages
- Smart filtering for `!sudo apt install`
- Background thread updates

### 5. Module Name Discovery
```python
def search_all_installed_module_names_from_scratch():
    # Searches site-packages
    # Finds all importable modules
    # ~7000 modules typically
```

### 6. Jedi Integration
- Full Python semantic completion
- Handles complex expressions
- Fallback for when Jedi fails

### 7. Special Completions

#### Backquote Completion (`)
Shows Python files for execution

#### Up Arrow Emulation (uuuu)
```python
if set(before_line)==set('u'):
    # Shows parent directory path
    # 'uuu' → 'CD ../../..'
```

## Smart Features

### 1. Priority System

```python
def sorting_key(x):
    # Priority order:
    # 1. User-created variables (highest)
    # 2. Non-private names
    # 3. Single underscore
    # 4. Double underscore (lowest)
```

### 2. Context Awareness

#### String Detection
```python
if self._path_completer_grammar.match(document.text_before_cursor):
    rp.r_iterm_comm.writing_in_string = True
    # Don't do Jedi completion in strings
```

#### Global vs Local
```python
in_global_or_nonlocal_declaration = (
    before_line.startswith('global ') or 
    before_line.startswith('nonlocal ')
)
```

### 3. Performance Optimizations

#### Fast Mode
```python
if ric.completion_style and ric.completion_style[0]=='fast':
    # Simple token matching, no Jedi
    # Much faster but less accurate
```

#### Regex Filtering
```python
compiled = re.compile('.*'+'.*'.join(
    re.escape(x) for x in origin.lower()
)+'.*')
# Filters 4000 candidates efficiently
```

### 4. Successful Command Tracking
```python
temp = (''.join(ric.successful_commands)).count(temp)
if temp:
    out /= temp  # Prioritize previously used completions
```

## Microcompletions

### Space-Based Transformations
Located in `key_bindings.py`, triggered on space:

1. **Import Transformations**
   - `numpy` → `import numpy as np`
   - `torch` → `import torch`
   - Module names → import statements

2. **Operator Completions**
   - `x a` → `x and`
   - `x o` → `x or`
   - `x i` → `x in` or `x is`

3. **Common Patterns**
   - `for i` → `for i in`
   - `if n` → `if not`

## Completion Display

### 1. Display Formatting
```python
display = x  # What user sees
text = x     # What gets inserted

# Remove trailing / from folders
if x.strip().endswith('/'):
    text = text.strip()[:-1]
```

### 2. Hidden File Handling
```python
if x.startswith('.'):
    if origin.startswith('.'):
        output = -1  # Show first if explicitly requested
    else:
        output = 1   # Hide by default
```

## Caching System

### 1. Completion Cache
```python
completion_cache_pre_origin_doc = {}
# Key: document prefix
# Value: tuple of completions
```

### 2. Ryan Match Cache
```python
_ryan_completion_matches_cache = {}
# Key: (hash(origin), hash(candidates))
# Value: sorted matches
```

### 3. Module Cache
```python
_cached_all_module_names = set()
_cached_all_module_names_done = threading.Event()
```

## Error Handling

### 1. Jedi Failures
```python
if script and not isinstance(script, Exception):
    try:
        completions = script.completions()
    except Exception:
        pass  # Silently fail, continue with other sources
```

### 2. Grammar Updates
```python
if isinstance(script, Exception):
    # Prompt to update Parso grammar files
    # Downloads from GitHub if needed
```

### 3. Global Error Suppression
```python
try:
    # All completion logic
except Exception as e:
    if not SHOWN_ERROR:
        # Show error once per session
        SHOWN_ERROR = e
```

## Special Completion Patterns

### 1. Dictionary Key Completion (commented out)
Would complete: `dict_var[` → `dict_var['key']`

### 2. Path Transformation
- `/System/` → `System/` (remove leading slash)
- `folder/` → `folder` (remove trailing slash)
- `../` → parent directory completion

### 3. Fuzzy Matching Algorithm
```python
def match(origin: str, candidate: str) -> int:
    # 'np' matches 'numpy'
    # 'rif' matches 'read_image_file'
    # Case-insensitive but case-preferring
```

## Performance Metrics

- **Module Discovery**: ~10 seconds for 7000 modules
- **APT Cache**: ~60,000 packages
- **Jedi Completions**: Variable (10ms - 1s)
- **Cached Completions**: <1ms
- **Fuzzy Matching**: ~5ms for 4000 candidates

## Configuration

### Settings
- `ric.completion_style`: Fast vs full mode
- `ric.enable_space_autocompletions`: Microcompletions
- `sorting_priorities`: Custom priority dict

### Customization Points
1. Add to `sorting_priorities` for custom ordering
2. Modify `ryan_completion_matches` for matching
3. Add command-specific completions in `_get_completions`

## Integration Points

### With r_iterm_comm
- `ric.globa`: Global namespace
- `ric.current_candidates`: Active completions
- `ric.successful_commands`: Command history
- `ric.writing_in_string`: String context flag

### With REPL
- Updates after every keystroke
- Shares namespace with evaluator
- Respects PT ON/OFF settings

## Advanced Features

### 1. APT Completion System
- Pre-downloads Ubuntu package list
- 60,000+ package names
- Smart caching in `/tmp/`

### 2. Module Discovery Thread
- Background thread on startup
- Searches all site-packages
- Non-blocking initialization

### 3. Multi-Level Matching
- Exact match (highest priority)
- Fuzzy match (medium)
- Substring match (lowest)

## Future Improvements (TODOs in code)

1. Dictionary key completion
2. Better string context detection
3. Improved performance for large namespaces
4. More command-specific completions
5. Better VI mode integration

This completion system represents years of refinement and optimization, creating one of the most intelligent Python REPL completion engines available.