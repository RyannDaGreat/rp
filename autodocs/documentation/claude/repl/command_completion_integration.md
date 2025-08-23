# RP Command and Completion Integration Guide

## Overview
RP's commands, microcompletions, and completion system are deeply integrated. This guide shows how they work together to create an intelligent, context-aware coding environment.

## 1. Directory Navigation Integration

### CD Command Family

#### Command Shortcuts (r.py)
- `CD` - Change directory
- `CDU` / `U` - Go up one directory  
- `CDB` / `B` - Go back in history
- `CDH` - Interactive history browser
- `TAKE` - Make directory and CD into it

#### Completion Support (completer.py)
```python
# Find with: grep "starts_with_any.*before_line.*'CD '" completer.py
if starts_with_any(before_line,'CD '):
    yield from yield_from_candidates(
        *pathsmod(x for x in scandir_path_before_cursor() if x.is_dir())
    )
```
**Only shows directories, not files!**

#### Microcompletions (key_bindings.py)
- `cd ` → `CD ` (prefix conversion when no variable named 'cd')
- `u` → `../` (one directory up)
- `uu` → `../../` (two directories up)
- `uuu` → `../../../` (three directories up)
- `uuuu` → `CD ../../../` (full command)

#### How They Work Together
1. Type `cd ` → converts to `CD ` via prefix completion
2. After `CD `, completer only shows directories
3. Type `u` repeatedly for parent directory navigation
4. `CDH` gets special completions:
   ```python
   if starts_with_any(before_line,'CDH '):
       # Shows directory history
       # Special handling for 'CDH GIT' to find git repos
   ```

### TAKE Command Integration

#### Command (r.py)
```python
TAKE directory_name  # Creates and enters directory
```

#### Completion (completer.py)
```python
if starts_with_any(before_line,'TAKE '):
    # Similar to CD but for creating directories
    # Shows existing directories as hints
```

## 2. File Operations Integration

### CAT/NCAT/CCAT Commands

#### Command Shortcuts (r.py)
- `CAT` - Display file contents
- `NCAT` - Display with line numbers
- `CCAT` - Copy file contents to clipboard
- `ACAT` - Advanced cat with options

#### Completion Support (completer.py)
```python
# These commands get file path completions
if starts_with_any(before_line,'CAT ','NCAT ','CCAT ','ACAT '):
    # Shows all files and directories
    # Prioritizes files over directories
```

#### Microcompletions
- `cat ` → `CAT ` (prefix conversion)

#### Autocomplete Enhancement (r.py)
```python
# Find with: grep "_autocomplete_lss_name.*CAT" r.py
if user_message.startswith('CAT '):
    user_message = 'CAT ' + _autocomplete_lss_name(user_message, command_name='CAT')
```
**Auto-completes partial file names!**

### LS Command Family

#### Commands (r.py)
- `LS` / `L` - List files
- `LSS` - Interactive file selector
- `LSA` - List all (including hidden)
- `LST` - List sorted by time
- `LSD` - List sorted by disk size
- `LSN` - List sorted by name/number

#### Completion Support (completer.py)
```python
if starts_with_any(before_line,'LS '):
    # Shows all files and directories
    # Different from CD which only shows directories
```

#### Microcompletions
- `ls` → `LS` (prefix conversion)
- `\lss` → Opens LSS selector (backslash command)
- `\lsr` → Relative LSS

### File Writing Commands

#### Commands (r.py)
- `WANS` - Write ans to file
- `SAVE` - Save with safety checks
- `WRITE` - Direct write

#### Path Completion
All get standard file/directory completions for path specification

## 3. Python Execution Integration

### RUN Command

#### Command (r.py)
```python
RUN script.py  # Executes Python file
```

#### Specialized Completion (completer.py)
```python
if before_line.startswith('RUN '):
    # Only shows .py and .rpy files!
    # Filters out all other file types
```

#### Microcompletions
- `run ` → `RUN ` (prefix conversion)

### EXEC/IMPORT Commands

#### Commands
- `EXEC` - Execute code
- `IMPORT` - Import module
- `RELOAD` - Reload modules

#### Module Completion
Gets module name completions from discovered modules

## 4. Shell Command Integration

### Bang Commands (!)

#### Completion System (completer.py)
```python
if before_line.startswith('!'):
    if before_line.startswith('!sudo apt install'):
        # Special case: APT package completions
        yield from yield_from_candidates(get_apt_completions())
    else:
        # Shows system commands from PATH
```

#### APT Package Completions
- **60,000+ Ubuntu packages** cached
- Downloads package list on first use
- Stored in `/tmp/` for fast access

#### Microcompletions
- `!` at start maintains shell context
- `!!` for persistent shell commands

## 5. Git Integration

### Git Commands

#### Commands (r.py)
- `GIT` / `G` - Git status
- `GITD` / `GD` - Git diff
- `GITA` / `GA` - Git add
- `GITC` / `GC` - Git commit

#### Microcompletions
- `git` → `GIT` (prefix conversion)
- Works with all git subcommands

## 6. Image/Media Commands

### Image Display Commands

#### Commands (r.py)
- `I` / `IMG` - Display image
- `II` - Interactive image viewer
- `IIS` - Select and display images

#### File Type Filtering
Commands that work with images can filter completions to show only image files

## 7. Clipboard Operations

### Copy/Paste Commands

#### Commands with Path Completion
- `FCOPY` - Copy file to web
- `FPASTE` - Paste file from web
- `LCOPY` - Local file copy
- `LPASTE` - Local file paste

#### Integration
All get appropriate file/directory completions

## 8. History Browsing

### History Commands

#### Commands (r.py)
- `HISTORY` / `HIST` - Command history
- `QVH` - Query visual history
- `QPH` - Query prompt-toolkit history

#### Special Completions
- `CDH` gets directory history completions
- `QVH` uses fuzzy finder for history search

## 9. Custom Command Integration

### RPRC Customization

#### Adding Commands with Completions
```python
# In ~/.rp/.rprc

# Add command that gets file completions
__import__('rp').r._add_pterm_command_shortcuts('''
    MYCAT $cat_with_colors
''')

# Add prefix shortcut with path completion
__import__('rp').r._add_pterm_prefix_shortcut("proj", "CD ~/projects/")
```

#### How Completions Apply
- Commands starting with `CD ` get directory completions
- Commands starting with `CAT ` get file completions
- Commands starting with `!` get shell completions

### Custom Prefix Shortcuts

#### Definition (RPRC)
```python
__import__('rp').r._add_pterm_prefix_shortcut("fu", "!!fileutil")
__import__('rp').r._add_pterm_prefix_shortcut("rcl", 
    ["!rclone copy --progress ", " ."])
```

#### Cursor Positioning
For complex replacements with lists:
- First element: text before cursor
- Second element: text after cursor
- Example: `["fansi_print('", "','green bold')"]`
  - Results in: `fansi_print('|','green bold')` where `|` is cursor

## 10. Microcompletion Context Awareness

### When Microcompletions are Disabled

#### In completer.py context
```python
# Find with: grep "Microcompletions OFF\|microcompletions off" key_bindings.py
# Or: grep "(!|!!|PY |PYM |CD |RUN" key_bindings.py
if re.fullmatch(r'((!|!!|PY |PYM |CD |RUN |MKDIR |CAT |ACAT |VIM |OPEN |RM |TAB |TAKE |MV |CCAT |NCAT |WANS |EDIT |([A-Z]+ )).*)', before_line):
    # Microcompletions OFF for these commands
```

This prevents interference between command completions and microcompletions.

### String Context Detection
```python
if self._path_completer_grammar.match(document.text_before_cursor):
    rp.r_iterm_comm.writing_in_string = True
    # Don't do Jedi completion in strings
```

## 11. Priority System in Completions

### Sorting Algorithm (completer.py)
```python
def sorting_key(x):
    # Priority order:
    # 1. User-created variables (highest)
    # 2. Non-private names
    # 3. Single underscore
    # 4. Double underscore (lowest)
```

### Command History Priority
```python
# Previously successful commands get higher priority
temp = (''.join(ric.successful_commands)).count(temp)
if temp:
    out /= temp  # Lower number = higher priority
```

## 12. Performance Optimizations

### Caching System
```python
completion_cache_pre_origin_doc = {}
# Caches completions by document prefix
# 7x speedup over uncached
```

### Fast Mode
```python
if ric.completion_style and ric.completion_style[0]=='fast':
    # Simple token matching, no Jedi
    # Much faster but less accurate
```

## Integration Architecture

### Data Flow
```
User Input → Microcompletions → Command Conversion → Completer → Display
     ↓             ↓                    ↓                ↓          ↓
   "cd "      →  "CD "         →  Directory filter  → Path list → User
   "cat "     →  "CAT "        →  File filter      → File list → User
   "run "     →  "RUN "        →  Python filter    → .py files → User
```

### Context Stack
1. **Microcompletion Layer**: Transforms input
2. **Command Layer**: Interprets commands
3. **Completion Layer**: Provides context-aware suggestions
4. **Display Layer**: Shows filtered results

## Best Practices

### 1. Command Design
- Commands that work with directories should start with `CD`
- File commands should include standard names (CAT, LS, etc.)
- This ensures proper completion filtering

### 2. Custom Commands
- Follow naming conventions for automatic completions
- Use prefix shortcuts for complex command templates
- Test with completion system active

### 3. Performance
- Leverage caching for repeated operations
- Use fast mode for large namespaces
- Disable completions temporarily with `PT OFF`

## Tips for Users

### 1. Let the System Work
- Type naturally - `cd ` becomes `CD ` automatically
- Trust `u` repetition for parent directories
- Use TAB after commands for completions

### 2. Command Shortcuts
- Many commands have single-letter aliases
- These get the same completions as full commands
- Example: `L` gets same completions as `LS`

### 3. Context Matters
- `CD ` only shows directories
- `RUN ` only shows Python files
- `!sudo apt install ` shows packages
- This filtering saves time and reduces errors

## Summary

The integration between commands, completions, and microcompletions creates a seamless experience where:
- **Commands** define the action
- **Completions** provide context-aware suggestions
- **Microcompletions** accelerate input
- **All three** work together without interference

This tight integration is what makes RP's command system so powerful - each layer enhances the others rather than conflicting.