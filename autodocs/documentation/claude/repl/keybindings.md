# RP Keybindings Complete Reference

## Overview
RP's keybinding system (`rp_ptpython/key_bindings.py`) contains **105+ custom keyboard shortcuts** that transform the Python REPL into an intelligent code editor.

### Understanding Key Notation
- **Ctrl+X** = Hold Control and press X
- **Meta+X** = Either Alt+X OR press Escape then X (try both!)
- **Shift+X** = Hold Shift and press X
- **F1-F6** = Function keys
- **Context-aware** = Behavior changes based on what you're doing

### Quick Start - Most Important Shortcuts
1. **Ctrl+E** - Run code without clearing
2. **Escape then E** - AI-powered code fix (Claude)
3. **F3** - Browse/search history
4. **Ctrl+V** - Paste (or Alt+V for Vim edit)
5. **Ctrl+Space** - Comment/uncomment
6. **Ctrl+D** - Duplicate line (or exit if empty)
7. **Ctrl+T** - Toggle debug() line
8. **Space** - Smart completions (after module names)

## Key Categories

### 1. Execution Controls

#### Ctrl+E - Smart Execute
- **Normal (Ctrl+E)**: Run code without clearing buffer, cursor stays in place
- **With Meta (Escape then E or Alt+E)**: AI-powered code editing! Sends your buffer to Claude for improvement/fixes
- Find in code: `grep '@handle.*ControlE' key_bindings.py`
- Meta check: `grep 'if not meta_pressed.*ControlE' key_bindings.py`

#### Ctrl+W - Cell Execution  
- Runs code between `##` cell boundaries (Jupyter-style)
- If buffer starts with `!`, runs as shell command
- Cursor position preserved
- Find in code: `grep '@handle.*ControlW' key_bindings.py`
- Example:
  ```python
  ## Cell 1
  x = 5
  ## Cell 2  
  print(x)  # Ctrl+W here only runs Cell 2
  ```

#### Ctrl+Q - Abandon Buffer
- Saves current buffer to history (so you don't lose it)
- Clears the input area completely
- Does NOT exit RP (use Ctrl+D on empty buffer to exit)
- Useful when you want to start fresh but keep your work

### 2. Editor Integration

#### Ctrl+V - Paste/Vim Integration
- **Normal (Ctrl+V)**: Paste from system clipboard
- **With Meta (Escape then V or Alt+V)**: Opens entire buffer in Vim for editing
- Vim opens at your current cursor position
- When you save and exit Vim, changes return to buffer
- Find in code: `grep '@handle.*ControlV' key_bindings.py`
- Vim check: `grep 'vim(' key_bindings.py`
- Note: On Mac, this might be Alt+Z due to key mapping

#### F2 - Nano Editor
- Opens entire buffer in nano editor
- Cursor position preserved
- Save and exit to return changes to buffer
- Alternative to Vim for those who prefer nano

#### F4 - Micro Editor
- Opens buffer in micro editor (modern terminal editor)
- Similar to nano but with more features
- Must have micro installed

### 3. History Navigation

#### Ctrl+P - Previous/Next Toggle
- Alternates between inserting "PREV" and "NEXT" commands
- PREV recalls previous answer, NEXT moves forward
- **Disabled in VI mode** (conflicts with VI paste)

#### Ctrl+U - Undo
- Inserts the text "UNDO" which triggers RP's snapshot undo
- **Disabled in VI mode** (conflicts with VI's line operations)
- Different from Ctrl+Z which is buffer undo

#### F3 - Query History  
- Opens fuzzy finder (fzf) with your command history
- Can select multiple entries with Tab
- Selected commands return to buffer
- Much more powerful than arrow key history

### 4. Clipboard Operations

#### Ctrl+C - Smart Copy
- **With selection**: Copy selection
- **Without selection**: Copy current line
- Adds newline prefix for line copies

#### Ctrl+V - Smart Paste
- Handles multi-line properly
- Strips leading newline when appropriate

#### Ctrl+A - Paste Answer
- **Normal (Ctrl+A)**: Inserts `str(ans)` at cursor
- **With Meta (Escape then A or Alt+A)**: Inserts `repr(ans)` at cursor
- Useful for quickly reusing the last result
- Note: On Mac, this might be Alt+Z

### 5. Text Manipulation

#### Ctrl+D - Duplicate Line / Exit
- **With text in buffer**: Duplicates current line below cursor
- **Empty buffer**: Exits RP (standard Unix EOF)
- Cursor position maintained when duplicating

#### Ctrl+Delete - Delete Line
- Removes entire current line instantly
- If line is indented, maintains proper indentation context
- Different from Ctrl+U which deletes TO start of line in some modes

#### Ctrl+T - Toggle Top Line (debug)
- Press once: Adds `debug()` at top of buffer
- Press again: Removes the `debug()` line
- **Eager binding**: Happens immediately
- Perfect for quickly adding/removing debug breakpoint

#### Ctrl+B - Toggle Bottom Line
- Adds/removes a line at bottom of buffer
- Content can be configured (default varies)
- **Eager binding**: Happens immediately
- Useful for temporary notes or markers

### 6. Navigation

#### Arrow Keys
- **Up/Down**: 
  - In completions menu: Navigate suggestions
  - Otherwise: Navigate command history
- **Meta+Up/Down** (Alt or Escape first): Jump 10 lines in buffer
- **Left/Right**: Move cursor one character
- **Meta+Left/Right**: Move by word
- **With selection**: Arrow keys cancel selection

#### Shift+Left/Right - Argument Swapping
- Inside function calls: Swaps arguments around commas
- Example: `func(a, |b, c)` + Shift+Right → `func(a, c, |b)`
- Smart: Handles nested parentheses correctly
- Only works when cursor is between commas

### 7. Smart Backspace (Context-Aware)

#### Regular Backspace
- **Matching pairs**: `(|)` + Backspace → `` (deletes both)
- **Empty indentation**: Deletes entire indent level at once
- **Self-assignment**: `self.x| = x` + Backspace → `|` (deletes both sides)
- **Import cleanup**: `import os as |` + Backspace → `import os`
- **Eager binding**: Processes immediately

#### Meta+Backspace  
- Delete entire word/token backwards
- Stops at punctuation boundaries
- Respects snake_case and camelCase

### 8. Microcompletions (Space Key)

The space key triggers intelligent transformations when specific patterns are detected:

#### Import Completions
**Type module name + space:**
- `numpy ` → `import numpy as np`
- `pandas ` → `import pandas as pd`
- `torch ` → `import torch`
- `matplotlib ` → `import matplotlib.pyplot as plt`
- `requests ` → `import requests`

#### Operator Completions  
**After variable + letter + space:**
- `x a ` → `x and ` (a for and)
- `x o ` → `x or ` (o for or)
- `x i ` → `x in ` or `x is ` (context-dependent)
- `x n ` → `x not ` (n for not)
- `x t ` → `x to ` (in comments)

#### Loop Completions
**In for loops:**
- `for i ` → `for i in ` (adds 'in' automatically)
- `for _ ` → `for _ in ` (underscore iterator)
- `for x ` → `for x in ` (any variable name)

#### Conditional Completions
**After if/elif/while + n:**
- `if n ` → `if not ` (n becomes not)
- `elif n ` → `elif not `
- `while n ` → `while not `

**Note:** Disabled after commands like CD, RUN, CAT, etc.

### 9. Increment/Decrement Operators

#### Plus (+) Key
- `x+` → `x+=1`
- String concatenation awareness
- Smart spacing

#### Minus (-) Key
- `x-` → `x-=1`
- `def name-` → `def name_` (underscore conversion)
- `for -` → `for _ in :`

### 10. Bracket Operations

#### Bracketed Paste (Terminal Feature)
- Handles multi-line paste
- Preserves formatting
- Indentation awareness

### 11. Special Characters

#### Less Than (<) / Greater Than (>) - Argument Movement
- **After comma in function**: Moves arguments
- `<` moves current argument left
- `>` moves current argument right
- Example: `func(a, |b, c)` + `>` → `func(a, c, |b)`
- Only active with microcompletions enabled

#### Parentheses/Brackets
- Auto-pairs: `(` → `()`
- Auto-deletion of pairs
- Nested handling

### 12. Comment Controls

#### Ctrl+Space - Toggle Comments
- **With selection**: Comments/uncomments selected lines
- **No selection**: Comments/uncomments current line
- Uses Python `#` comments
- Preserves indentation perfectly
- Multi-line aware

### 13. VI Mode Specific

When VI mode is enabled, these bindings are DISABLED to avoid conflicts:
- **Ctrl+H** - In normal mode would insert HISTORY, in VI mode is standard backspace
- **Ctrl+U** - In normal mode inserts UNDO, in VI mode deletes to line start
- **Ctrl+P** - In normal mode toggles PREV/NEXT, in VI mode is paste
- Most microcompletions are disabled in VI mode
- Find VI filters: `grep '~vi_mode_enabled' key_bindings.py`

### 14. Function Keys

#### F1 - Help
- Shows help documentation

#### F2 - Edit in Nano
- External editor integration

#### F3 - History Query
- Interactive history browser

#### F4 - Edit in Micro
- Alternative editor

#### F6 - Custom Function
- User-definable action
- Can be customized in RPRC or settings

### 15. Advanced Features

#### Cell-Based Execution
```python
## Cell 1
code_block_1()

## Cell 2
code_block_2()
```
- Ctrl+W runs current cell
- Supports shell mode with `!`

#### Smart Indentation
- Backspace removes entire indent
- Auto-indent after `:` 
- Dedent on `pass`, `return`, etc.

#### Self-Assignment Detection
```python
self.var| = var  # Backspace affects both sides
```

#### Import Cleanup
- `import os as |` + Backspace → `import os`
- `import os, |` + Backspace → `import os`

## Microcompletion Details

### How It Works
1. Analyzes text before cursor
2. Checks token context
3. Applies transformation
4. Maintains cursor position

### Transformation Rules

#### Import Rules
```python
# On space after module name:
'numpy' → 'import numpy as np'
'requests' → 'import requests'
'BeautifulSoup' → 'from bs4 import BeautifulSoup'
```

#### Operator Rules
```python
# After identifier + letter + space:
'x a ' → 'x and '
'y o ' → 'y or '
'z i ' → 'z in ' or 'z is '
```

#### Special Cases
```python
# Context-aware transformations:
'for i ' → 'for i in '
'lambda x' → 'lambda x:'
'def func' → 'def func():'
```

## Configuration

### Settings
- `enable_space_autocompletions`: Toggle microcompletions
- `vi_mode_enabled`: VI mode compatibility
- `microcompletions_enabled`: Master toggle

### Customization
Key bindings can be modified in:
- `~/.rp/settings.json`
- RPRC initialization file

## Buffer Management

### Undo/Redo System
- **Ctrl+Z**: Undo last buffer change (standard undo)
- **Ctrl+Y**: Redo buffer change
- **Different from UNDO command** which reverts namespace state
- Tracks complete document history including cursor position

### Selection Handling
- Copy/paste with selection
- Arrow keys exit selection
- Smart selection operations

## Integration Features

### Clipboard Integration
- System clipboard support
- tmux clipboard
- Vim clipboard
- Web clipboard

### External Editor Protocol
1. Save buffer to temp file
2. Launch editor with cursor position
3. Read back changes
4. Restore cursor from editor

## Performance Optimizations

### Eager Bindings
Some keys marked `eager=True` for immediate response:
- Backspace (`grep 'Backspace.*eager=True' key_bindings.py`)
- Ctrl+T (`grep 'ControlT.*eager=True' key_bindings.py`)
- Ctrl+B (`grep 'ControlB.*eager=True' key_bindings.py`)

### Lazy Evaluation
Completions only trigger when needed:
- After certain characters
- On explicit request
- Context-dependent

## Tips & Tricks

### 1. Quick Editing
- **Escape then V** (or Alt+V): Edit complex code in Vim
- **F3**: Search through history with fuzzy finder
- **Ctrl+D**: Quickly duplicate lines for testing

### 2. Efficient Navigation  
- **Escape+Arrow**: Jump 10 lines at once
- **Shift+Left/Right**: Reorder function arguments
- **Ctrl+L**: Clear screen when it gets cluttered

### 3. Smart Completions
- **Trust the space bar** after module names
- **Let `-` become `_`** in function names
- **Use `+`** for auto-increment (`x+` → `x+=1`)

### 4. Debugging
- **Ctrl+T**: Instant debug() toggle
- **Ctrl+E**: Test code without losing it
- **Escape then E**: Let AI fix your bugs!

### 5. Hidden Gems
- **Escape then X**: Delete first char of every line
- **Escape then `** (backtick): Toggle shell mode
- **Escape then S**: Insert "self" quickly

## Missing/Undocumented Shortcuts

These exist in the code but aren't fully documented above:
- **Ctrl+L** - Clear screen (`grep '@handle.*ControlL' key_bindings.py`)
- **Ctrl+H** - Backspace alternative (`grep '@handle.*ControlH' key_bindings.py`)
- **Ctrl+Z** - Buffer undo (`grep '@handle.*ControlZ' key_bindings.py`)
- **Ctrl+Y** - Buffer redo (`grep '@handle.*ControlY' key_bindings.py`)
- **Delete** key - Forward delete (`grep '@handle.*Delete' key_bindings.py`)
- **Escape** key alone - Sets meta flag (`grep '@handle.*Keys.Escape' key_bindings.py`)
- **BracketedPaste** - Terminal paste (`grep 'BracketedPaste' key_bindings.py`)
- **Meta+X** - Delete first char every line (`grep "char=='X'.*meta_pressed" key_bindings.py`)
- **Meta+S** - Insert "self" (`grep "char=='s'.*meta_pressed" key_bindings.py`)
- **Meta+`** - Toggle shell mode (`grep "char=='\`'.*meta_pressed" key_bindings.py`)
- **Meta+Space** - Literal space (`grep "' '.*meta_pressed" key_bindings.py`)

## Total Keybindings

- **105+ total handlers** in key_bindings.py
- **50+ Ctrl combinations**
- **20+ Meta combinations** (Escape then key)
- **60+ character handlers** (including all backslash commands)
- **Context-aware behaviors** via filters

This represents one of the most sophisticated REPL keybinding systems, with context-aware transformations that make Python coding dramatically more efficient.