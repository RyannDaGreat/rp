# Manual Page Completer

## Overview
**File**: `experimental/manpage_completer.py`  
**Type**: Standalone utility  
**Purpose**: Generates command-line autocompletion suggestions from Unix manual pages

## Functionality
Extracts command-line options from `man` pages and provides them as completion suggestions for shell commands.

## Core Functions

### `get_manpage_completions(line)`
```python
completions = get_manpage_completions('git ')
# Returns: ['-h', '--help', '--version', '--git-dir', ...]
```

**Parameters:**
- `line` (str): Command line being completed

**Returns:**
- `list[str]`: Available command-line options for the command

### `generate_options_of(cmd)`
```python
options = list(generate_options_of('git'))
# Yields: [('Show help message', ('-h', '--help')), ...]
```

**Parameters:**
- `cmd` (str): Command name to analyze

**Returns:**
- Generator yielding `(description, options)` tuples

## How It Works

### 1. Manual Page Extraction
```python
def _get_man_page(cmd: str):
    # Runs: man cmd | col -b
    # Returns clean text without control characters
```

### 2. Option Pattern Matching
Uses regex to find option patterns:
- Short options: `-h`, `-v`, `-f`
- Long options: `--help`, `--version`, `--file`
- Combined patterns: `-h, --help`

### 3. Section Analysis
Searches for option documentation in man page sections:
- "OPTIONS"
- "COMMAND OPTIONS"  
- "DESCRIPTION"

### 4. Caching
Uses `@memoized` decorator to cache results for performance.

## Usage Examples

### Basic Usage
```python
from rp.experimental.manpage_completer import get_manpage_completions

# Get completions for git command
options = get_manpage_completions('git ')
print(options)  # ['-h', '--help', '--version', ...]

# Get completions for ls command
options = get_manpage_completions('ls ')  
print(options)  # ['-a', '--all', '-l', '--long', ...]
```

### Integration with Shell
```python
def complete_command(line):
    \"\"\"Shell completion integration\"\"\"
    if not line.strip():
        return []
    
    return get_manpage_completions(line)
```

## Implementation Details

### Text Processing Pipeline
1. **Raw manual page** → `man command`
2. **Clean formatting** → `col -b` (remove backspaces)
3. **Section extraction** → Find OPTIONS/DESCRIPTION sections
4. **Option parsing** → Regex matching for `-opt` and `--option`
5. **Description extraction** → Parse option descriptions
6. **Caching** → Store results for future use

### Regex Pattern
```python
r"(?:(,\s?)|^|(\sor\s))(?P<option>-[\w]|--[\w-]+)(?=\[?(\s|,|=\w+|$))"
```
Matches option patterns while handling various formatting styles found in man pages.

## Performance Characteristics

### Caching Strategy
- Uses `functools.lru_cache` for parsed results
- Avoids repeated `man` command execution
- Handles dynamic command discovery

### Error Handling
- Graceful fallback for commands without man pages
- Handles malformed man page formatting
- Returns empty list for unknown commands

## Limitations

### System Dependencies
- Requires `man` command availability
- Requires `col` command for formatting
- Unix-like systems only

### Coverage Limitations
- Only processes commands with man pages
- May miss some option formats
- Doesn't handle subcommand completion

## Integration Opportunities

### REPL Integration
Could be integrated into RP's command completion system:
```python
# In REPL completion logic
if line.startswith('!'):  # Shell command
    return get_manpage_completions(line[1:])
```

### Shell Plugin
Could be adapted for zsh/bash completion plugins:
```bash
# Example zsh integration
_rp_complete() {
    local completions
    completions=($(python -c "from rp.experimental.manpage_completer import get_manpage_completions; print(' '.join(get_manpage_completions('$words')))"))
    reply=($completions)
}
```

## Related Files
- **Original source**: Based on `xonsh/completers/man.py`
- **Dependencies**: Uses RP's `@memoized` decorator
- **Integration potential**: Could enhance RP's shell command execution