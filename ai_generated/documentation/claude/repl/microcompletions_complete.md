# Complete RP Microcompletions Reference

## Overview
RP's microcompletions are intelligent, context-aware text transformations that trigger on specific keystrokes. They dramatically speed up Python coding by automating common patterns.

## Categories of Microcompletions

### 1. Space-Based Microcompletions

#### Import Transformations
When you type a module name followed by space:
- `numpy ` → `import numpy as np`
- `pandas ` → `import pandas as pd`
- `matplotlib ` → `import matplotlib.pyplot as plt`
- `torch ` → `import torch`
- `requests ` → `import requests`
- `BeautifulSoup ` → `from bs4 import BeautifulSoup`

#### Operator Completions
After identifier + letter + space:
- `x a ` → `x and `
- `x o ` → `x or `
- `x i ` → `x in ` or `x is ` (context-dependent)
- `x n ` → `x not `
- `x t ` → `x to ` (in comments)

#### Loop Completions
- `for i ` → `for i in `
- `for _ ` → `for _ in `
- `for x ` → `for x in `

#### Conditional Completions  
- `if n ` → `if not `
- `elif n ` → `elif not `
- `while n ` → `while not `

### 2. Backslash Microcompletions (\\)

RP has **60+ backslash microcompletions** that transform into complex operations:

#### Editor Integration
- `\vi` → Opens buffer in vim
- `\mi` → Opens buffer in micro
- `\na` → Opens buffer in nano

#### Code Alignment
- `\al` → Align lines
- `\ac` → Align at character
- `\rcl` → Reverse columns

#### Code Cleanup
- `\sw` → Strip whitespace
- `\sc` → Strip comments
- `\sdo` → Strip docstrings
- `\stp` → Strip (general)
- `\d0l` to `\d9l` → Delete 0-9 empty lines
- `\dtt` → Delete to top
- `\dtb` → Delete to bottom

#### Code Transformation
- `\de` → Toggle `debug()` at top
- `\db` → Insert debug statement
- `\pu` → Insert pudb debugger
- `\fo` → Insert for loop
- `\wh` → Insert while loop
- `\fi` → Import from swap
- `\mla` → Multi-line arguments
- `\23p` → Python 2 to 3 conversion
- `\ya` → YAPF autoformat
- `\tts` → Tabs to spaces

#### Navigation
- `\gg` → Go to top
- `\GG` → Go to bottom
- `\vO` → Vim open line above
- `\vo` → Vim open line below

#### String Operations
- `\an` → Insert `ans`
- `\san` → Insert `str(ans)`
- `\spa` → String paste
- `\spl` → Splitlines
- `\lj` → Line join

#### Line Operations
- `\sl` → Sort lines
- `\rl` → Reverse lines
- `\und` → Unindent
- `\ind` → Indent

#### Special Operations
- `\lss` → LSS (file selector)
- `\lsr` → Relative LSS
- `\tbp` → Toggle big parenthesis
- `\wi` → Working index
- `\en` → Enumerate
- `\fn` → Function name
- `\inm` → If name main block
- `\irp` → Inline RP imports
- `\qrp` → Qualify RP imports

#### Diff Operations
- `\dipa` → Diff with paste
- `\ditp` → Diff with tmux paste
- `\divp` → Diff with vim paste
- `\diwp` → Diff with web paste
- `\dian` → Diff with ans
- `\dilp` → Diff with local paste
- `\diph` → Diff with PT history
- `\qph` → Query PT history

#### Deletion
- `\da` → Delete all

### 3. Prefix Completions (Lowercase → Uppercase)

When no variable exists with the lowercase name, RP converts common commands:

#### Directory Commands
- `cd ` → `CD ` (change directory)
- `pwd` → `PWD` (print working directory)
- `ls` → `LS` (list files)
- `mkdir` → `MKDIR` (make directory)

#### File Commands
- `cat ` → `CAT ` (display file)
- `rm ` → `RM ` (remove file)
- `mv ` → `MV ` (move file)
- `cp ` → `CP ` (copy file)

#### Python Commands
- `run ` → `RUN ` (run Python file)
- `exec` → `EXEC` (execute code)
- `import` → `IMPORT` (import module)

#### Git Commands
- `git` → `GIT` (git status)
- `commit` → `COMMIT` (git commit)
- `push` → `PUSH` (git push)
- `pull` → `PULL` (git pull)

#### Custom Prefix Shortcuts (RPRC)
You can add custom prefix shortcuts in your RPRC:
```python
# In ~/.rp/.rprc
__import__('rp').r._add_pterm_prefix_shortcut("fu", "!!fileutil")
__import__('rp').r._add_pterm_prefix_shortcut("fp", ["fansi_print('", "','green bold')"])
__import__('rp').r._add_pterm_prefix_shortcut("rcl", ["!rclone copy --progress --transfers 128 --metadata --checksum ", " ."])
```

Usage:
- `fu ` → `!!fileutil `
- `fp ` → `fansi_print('|','green bold')` (cursor at |)
- `rcl ` → `!rclone copy --progress --transfers 128 --metadata --checksum | .` (cursor at |)

### 4. Operator-Based Microcompletions

#### Plus (+) Key
- `x+` → `x+=1` (increment)
- String concatenation awareness

#### Minus (-) Key  
- `x-` → `x-=1` (decrement)
- `def name-` → `def name_` (underscore conversion)
- `for -` → `for _ in :`

#### Equals (=) Key
- After operators for augmented assignment
- Smart spacing

#### Dot (.) Operator
- `.attribute` → `ans.attribute` (when starting line)
- Smart attribute completion

#### Question Mark (?)
- `?` at end → `rinsp(expression)`
- `??` at end → Detailed inspection
- `???` at end → Extra detailed inspection

#### Exclamation Mark (!)
- `!command` → Shell command execution
- `!!command` → Persistent shell command

#### Colon (:)
- Smart indentation after
- Function/class definition handling

### 5. Bracket/Parenthesis Microcompletions

#### Auto-Pairing
- `(` → `()`
- `[` → `[]`
- `{` → `{}`
- `"` → `""`
- `'` → `''`

#### Smart Deletion
Backspace deletes matching pairs:
- `(|)` + Backspace → `` (deletes both)
- `[|]` + Backspace → `` (deletes both)

### 6. Advanced Backslash Commands with Arguments

Some backslash commands accept arguments in backticks:

#### Replace Operations
- `` `old`new\r`` → Replace all 'old' with 'new'
- `` `var1`var2\rv`` → Replace variable names

#### Extract Variable
- `` `expression`varname\ev`` → Extract expression to variable

#### File Operations
- `` `path\l`` → Load file into buffer
- `` `path\w`` → Write buffer to file
- `` `path\s`` → Save buffer to file (with backup)

#### Navigation
- `` `123\g`` → Go to line 123
- `` `50\dtl`` → Delete to line 50

#### Python Evaluation
- `` `lambda x: x.upper()\p`` → Apply Python function to buffer

#### Cancel
- `` `anything\c`` → Cancel and delete the command

### 7. Special Slash Commands

#### Question Mark Shortcuts
When no variable exists with the name:
- `/v` → `?v` (vim ans)
- `/s` → `?s` (show string)
- `/p` → `?p` (print)
- `/e` → `?e` (execute)

### 8. Multi-Character Sequences

#### Up Arrows (uuuu)
- `u` → `../` (one directory up)
- `uu` → `../../` (two directories up)
- `uuu` → `../../../` (three directories up)
- `uuuu` → `CD ../../../` (CD three up)

### 9. Context-Aware Transformations

#### String Detection
Microcompletions disabled inside strings

#### Command Context
Disabled after certain commands:
- After `!`, `!!`, `PY`, `CD`, `RUN`, `MKDIR`, etc.

#### Import Context
- `from x i` → `from x import`
- Smart module recognition

### 10. VI Mode Compatibility

When VI mode is enabled, certain microcompletions are disabled to avoid conflicts:
- Ctrl+H
- Ctrl+U
- Ctrl+P
- Some character handlers

## Configuration

### Enabling/Disabling

#### Global Toggle
```python
python_input.enable_microcompletions = True/False
```

#### In RPRC
```python
__import__('rp').r.enable_space_autocompletions = True
```

### Adding Custom Microcompletions

#### Via RPRC
```python
# Add prefix shortcut
__import__('rp').r._add_pterm_prefix_shortcut("shortcut", "replacement")

# Add command shortcuts
__import__('rp').r._add_pterm_command_shortcuts('''
    MYCOMMAND $some_function()
    MC2 !shell_command
''')
```

#### Via additional_prefix_shortcuts
```python
__import__('rp').r.additional_prefix_shortcuts = {
    "my": "MY_REPLACEMENT",
    "test": ["complex", "replacement"]
}
```

## Performance Characteristics

### Speed
- Microcompletions execute instantly (<1ms)
- No blocking of input
- Cached pattern matching

### Memory
- Minimal overhead
- Patterns compiled once

## Tips & Tricks

### 1. Learning Curve
Start with common ones:
- Space after module names
- `\de` for debug toggle
- Backspace for pair deletion

### 2. Customization
Add your own patterns for repetitive code

### 3. Muscle Memory
- Trust the space bar
- Let `-` become `_` automatically
- Use `+` for incrementing

### 4. Efficiency Combos
- `numpy ` + `\al` → Import and align
- `\de` + `\pu` → Debug setup
- `\sc` + `\sw` → Clean code

## Complete List Summary

### Total Microcompletions: **150+**
- **Space-based**: 30+ patterns
- **Backslash commands**: 60+ commands
- **Prefix conversions**: 20+ commands
- **Operator-based**: 15+ patterns
- **Bracket handling**: 10+ patterns
- **Special sequences**: 15+ patterns

## Common Workflows

### 1. Quick Import and Use
```python
numpy   # → import numpy as np
np.array([1,2,3])
```

### 2. Debug Insertion
```python
\de     # Adds debug() at top
# Run code - drops into debugger
\de     # Removes debug()
```

### 3. Code Cleanup
```python
\sc     # Strip comments
\sw     # Strip whitespace
\ya     # YAPF format
```

### 4. Variable Extraction
```python
`complex_expression`result\ev
# Creates: result = complex_expression
```

### 5. Quick Alignment
```python
\ac     # Align at character
\al     # Align lines
```

This microcompletion system represents one of the most sophisticated code acceleration systems in any REPL, dramatically reducing keystrokes and accelerating Python development.