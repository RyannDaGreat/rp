# Parenthesis Automator System

## Overview
The Parenthesis Automator creates ASCII art visualizations of parenthesis nesting, making complex expressions easier to understand at a glance.

## The Algorithm

The `parenthesizer_automator` function can be found with `grep "def parenthesizer_automator" r.py`:

### Core Logic
```python
def parenthesizer_automator(string: str):
    # Handles ANSI colored strings specially
    if has_ansi_colors(string):
        plain = strip_ansi_escapes(string)
        result = parenthesizer_automator(plain)
        # Preserve original colored line in middle
        
    # Main algorithm
    def _parenthesizer_automator(x: str):
        # Convert to parenthesis-only representation
        l = lambda q: ''.join(
            '(' if x in '([{' else 
            ')' if x in ')]}' else 
            ' ' for x in q
        )
        
        # Recursive matching algorithm
        # Marks matched pairs with < and >
        # Converts to box drawing characters
```

### Visual Output

Input: `[[(hello)]]`
Output:
```
┌─────────┐
│ ┌─────┐ │
│ │ ┌─┐ │ │
[ [ ( ) ] ]
│ │ └─┘ │ │
│ └─────┘ │
└─────────┘
```

## Box Drawing Characters

The system uses Unicode box drawing:
- `┌` `┐` - Top corners
- `└` `┘` - Bottom corners  
- `│` - Vertical lines
- `─` - Horizontal lines (implied)

## Features

### Multi-Type Support
Handles all bracket types:
- Parentheses: `()`
- Square brackets: `[]`
- Curly braces: `{}`

### ANSI Color Preservation
- Detects colored terminal strings
- Processes plain text version
- Restores colors in middle line

### Recursive Matching
- Pairs innermost brackets first
- Works outward to outer brackets
- Handles nested structures

### Line-by-Line Processing
Processes each line independently:
```python
return '\n'.join(
    _parenthesizer_automator(line) 
    for line in string.splitlines()
)
```

## Display Integration

### Buffer Management
In layout.py (find with `grep "buffer_name='parenthesizer_buffer'" layout.py`):
```python
Window(
    BufferControl(
        buffer_name='parenthesizer_buffer',
        lexer=lexer
    ),
    wrap_lines=False
)
```

### Filter Control
`ShowParenthesisAutomator` filter controls visibility

### Real-Time Updates
Updates via `r_iterm_comm.parenthesized_line`

## Algorithm Details

### Step 1: Extract Brackets
```python
# Convert string to bracket-only representation
'foo(bar[baz])' → '   (   [   ])'
```

### Step 2: Match Pairs
```python
# Find matching pairs, mark with < >
'((()))' → '<<>>><'
```

### Step 3: Build Layers
```python
# Recursive layers for nested brackets
# Each level gets its own visual layer
```

### Step 4: Convert to Box Art
```python
# Replace markers with box characters
'<' → '┌'
'>' → '┐'
'(' → '│'
```

## Edge Cases

### Unbalanced Parentheses
```python
'(((' → Shows unclosed brackets
')))' → Shows unmatched closers
```

### Empty Input
Returns original string unchanged

### Mixed Content
Non-bracket characters shown as spaces in visualization

## Performance Considerations

### Recursion Depth
- Limited by Python's recursion limit
- Very deep nesting may fail
- Author notes: "I wonder what the time complexity is?"

### Optimization Attempts
Code includes commented attempt at non-recursive version:
```python
# I tried and failed to do this without recursion
# My failure is below
```

## Usage in REPL

### Automatic Display
Shows when typing expressions with brackets

### Visual Debugging
Helps identify mismatched parentheses

### Learning Tool
Makes nested structures clear for beginners

## Code Locations

- **Main Function**: Find with `grep "def parenthesizer_automator" r.py`
- **Display Buffer**: Find with `grep "buffer_name='parenthesizer_buffer'" layout.py`
- **Filter**: Find with `grep "class ShowParenthesisAutomator" filters.py`
- **State Variable**: Find with `grep "parenthesized_line" r_iterm_comm.py` - parenthesized_line

## Known Limitations

1. **Single Line Optimized** - Works best with single lines
2. **Recursion Based** - May hit limits with deep nesting
3. **ASCII Art** - Fixed character width required
4. **Performance** - Complex expressions may lag

## Future Improvements

Potential enhancements:
- Non-recursive implementation for better performance
- Colorized brackets for easier matching
- Horizontal layout option
- Error highlighting for mismatches