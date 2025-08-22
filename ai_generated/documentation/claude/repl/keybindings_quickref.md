# RP Keyboard Shortcuts - Quick Reference

## Essential Shortcuts (Learn These First!)

| Shortcut | Action | Notes |
|----------|--------|-------|
| **Ctrl+E** | Run code (keep buffer) | Doesn't clear your input |
| **Escape, E** | AI code fix (Claude) | Let AI improve your code |
| **Ctrl+D** | Duplicate line OR exit | Exit only on empty buffer |
| **F3** | Search command history | Fuzzy finder for history |
| **Ctrl+V** | Paste from clipboard | Standard paste |
| **Escape, V** | Edit buffer in Vim | Full Vim editor |
| **Ctrl+Space** | Toggle comments | Works on selection |
| **Ctrl+T** | Toggle debug() line | Quick debugging |
| **Space** | Smart completions | After module names |
| **Backspace** | Smart delete | Deletes pairs like () |

## Execution & Testing

| Shortcut | Action | Example |
|----------|--------|---------|
| **Ctrl+E** | Run without clearing | Test code safely |
| **Ctrl+W** | Run current cell | Between ## markers |
| **Ctrl+Q** | Abandon buffer | Clear but save to history |
| **Escape, E** | AI assistance | Fix errors with Claude |

## Editing

| Shortcut | Action | Details |
|----------|--------|---------|
| **Ctrl+D** | Duplicate line | Copy line below |
| **Ctrl+Delete** | Delete entire line | Remove line instantly |
| **Ctrl+T** | Toggle debug() | Add/remove at top |
| **Ctrl+B** | Toggle bottom line | Add/remove at bottom |
| **Ctrl+Space** | Comment/uncomment | Python # comments |
| **F2** | Edit in nano | External editor |
| **F4** | Edit in micro | Modern editor |
| **Escape, V** | Edit in Vim | Power editing |

## Navigation

| Shortcut | Action | Context |
|----------|--------|---------|
| **↑/↓** | History or completions | Context-aware |
| **Escape+↑/↓** | Jump 10 lines | Fast movement |
| **Shift+←/→** | Swap arguments | In function calls |
| **F3** | Query history | Fuzzy search |
| **Ctrl+L** | Clear screen | Clean display |

## Clipboard & Answers

| Shortcut | Action | What it does |
|----------|--------|--------------|
| **Ctrl+V** | Paste | System clipboard |
| **Ctrl+C** | Copy | Selection or line |
| **Ctrl+A** | Paste ans as string | Insert str(ans) |
| **Escape, A** | Paste ans as repr | Insert repr(ans) |

## Smart Typing (Microcompletions)

| Pattern | Result | Example |
|---------|--------|---------|
| `numpy ` | `import numpy as np` | Module imports |
| `x a ` | `x and ` | Boolean operators |
| `for i ` | `for i in ` | Loop syntax |
| `if n ` | `if not ` | Conditionals |
| `x+` | `x+=1` | Increment |
| `def name-` | `def name_` | Underscore |
| `(` | `()` with cursor inside | Auto-pairs |

## Undo/Redo

| Shortcut | Action | Type |
|----------|--------|------|
| **Ctrl+Z** | Undo buffer change | Text undo |
| **Ctrl+Y** | Redo buffer change | Text redo |
| **Ctrl+U** | Insert "UNDO" | Namespace undo |
| **Ctrl+P** | Toggle PREV/NEXT | Answer history |

## Hidden Power Features

| Shortcut | Action | Description |
|----------|--------|-------------|
| **Escape, X** | Delete first char all lines | Bulk edit |
| **Escape, `** | Toggle shell mode (!prefix) | Shell commands |
| **Escape, S** | Insert "self" | Quick Python |
| **Escape, Space** | Literal space | Bypass completions |
| **Backspace** on `()` | Delete both parens | Smart pairs |

## Meta Key Guide

**Meta key = Escape OR Alt** (try both on your system)

- Press **Escape** then the key (two separate presses)
- OR hold **Alt** while pressing the key
- Mac users: Often Alt instead of Ctrl for some shortcuts

## Context Matters!

Many shortcuts change behavior based on:
- Whether you have text selected
- If you're in a string
- If buffer is empty
- If you're in VI mode
- Your cursor position (in function, at line start, etc.)

## Quick Examples

```python
# Type this:          # Get this:
numpy<space>          import numpy as np
for i<space>          for i in 
x a<space>            x and 
def helper-           def helper_

# Ctrl+T adds:        debug()
# Ctrl+E runs without clearing
# F3 searches history
# Escape,E sends to AI
```

## Pro Tips

1. **Space is magic** - Trust it after module names
2. **Escape then key** - Many hidden features
3. **Backspace is smart** - Deletes pairs and indents
4. **Context aware** - Same key, different actions
5. **F3 is powerful** - Better than arrow history

---
*Reference: key_bindings.py has 105+ total keybindings*