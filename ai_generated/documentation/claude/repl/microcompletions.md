# Microcompletions System

## Overview
RP's microcompletions are intelligent, context-aware text transformations that happen as you type, making Python coding faster and more intuitive.

## Core Concept
Unlike traditional autocompletion that suggests options, microcompletions automatically transform your input based on context, following the principle: "Should be activated on the fringes of useless or invalid syntax"

## Key Features

### 1. Space Completions
When you press space after typing a function/variable name:
```python
# Type: "pri" + space
# Becomes: "print("
# Cursor positioned inside parentheses

# Type: "le" + space  
# Becomes: "len("
```

### 2. Operator Completions
Automatic operator insertion:
```python
# Type: "x i" 
# Becomes: "x in "

# Type: "x a"
# Becomes: "x and "

# Type: "x o"
# Becomes: "x or "
```

### 3. String Key Transformations
Smart dictionary key handling:
```python
# Type: "dict.ke" + trigger
# Becomes: "dict['key']"

# Handles nested access:
# Type: "a.b.c"
# Becomes: "a['b']['c']"
```

### 4. Parenthesis Completions
Automatic parenthesis for callables:
```python
# If 'func' is callable:
# Type: "func" + space
# Becomes: "func("
```

### 5. Import Completions
Smart import statement handling:
```python
# Type: "import num" + space
# Becomes: "import numpy"

# Type: "from pa" + space  
# Becomes: "from pandas"
```

## Implementation Details

### Location
Main logic in `/rp/rp_ptpython/key_bindings.py`

### Key Components

#### Microcompletion Enable Check
```python
microcompletions_enabled = Condition(
    lambda cli: getattr(python_input, 'enable_microcompletions', False)
)
```

#### Space Handler
```python
@handle(' ', filter=~vi_mode_enabled & microcompletions_enabled)
def _(event):
    # Complex logic for space completions
    # Checks if preceding text is callable
    # Adds parentheses if appropriate
```

#### Character Handlers
Individual handlers for each character that trigger transformations:
- Letters (a-z): Operator completions
- Period (.): Dictionary access
- Quotes: String handling
- Semicolon: Statement separation

### Context Detection

#### Callable Detection
```python
def is_callable_token(token_name):
    import rp.r_iterm_comm as r_iterm_comm
    try:
        return callable(eval(token_name, r_iterm_comm.globa))
    except:
        return False
```

#### Iterable Detection
```python
def is_iterable_token(token_name):
    from rp import is_iterable
    try:
        return is_iterable(eval(token_name, r_iterm_comm.globa))
    except:
        return False
```

## Special Cases

### Disabled Contexts
Microcompletions are disabled in:
- Shell commands (`!command`)
- Special REPL commands (`CD`, `RUN`, etc.)
- String literals
- Comments
- Import statements (partial)
- Lambda expressions

### String Handling
Special logic for string contexts:
```python
# Detects if cursor is inside string
# Prevents operator completions in strings
# Allows different behavior for string operations
```

### Multi-line Handling
Different behavior for multi-line input:
- More conservative completions
- Preserves indentation
- Handles line continuations

## Configuration

### Enabling/Disabling
Controlled by `python_input.enable_microcompletions`

### Per-Character Control
Each character can be individually configured:
```python
@handle('a', filter=~vi_mode_enabled & microcompletions_enabled)
# Can be disabled by removing handler
```

## Advanced Features

### 1. Smart Import Completion
Detects common module abbreviations:
```python
# "np" → "numpy"
# "pd" → "pandas"  
# "tf" → "tensorflow"
```

### 2. Operator Precedence
Handles operator precedence intelligently:
```python
# "x in y a" → "x in y and "
# Not "x iny a" (prevents merging)
```

### 3. Bracket Matching
Maintains bracket balance:
```python
# Won't complete if it breaks bracket matching
# Tracks parenthesis depth
```

### 4. History Integration
Uses command history for better predictions:
- Learns from previous completions
- Adapts to user patterns

## Performance Considerations

### Caching
- `ric.current_candidates` - Cached completion candidates
- Avoids re-evaluation on each keystroke

### Lazy Evaluation
- Only evaluates when necessary
- Checks cache first

### Thread Safety
- Runs in main UI thread
- No async complications

## Common Transformations

### Functions
- `pr` → `print(`
- `le` → `len(`
- `ra` → `range(`
- `su` → `sum(`

### Operators
- `i` → `in`
- `a` → `and`
- `o` → `or`
- `n` → `not`

### Common Patterns
- `for i` → `for i in`
- `if x` → `if x:`
- `def f` → `def f():`

## Debugging Microcompletions

### Disable Temporarily
Hold Alt while typing to bypass

### Check State
```python
print(python_input.enable_microcompletions)
```

### View Candidates
```python
import rp.r_iterm_comm as ric
print(ric.current_candidates)
```

## Known Issues

1. **Over-eager Completion**: Sometimes completes when not wanted
2. **String Detection**: May fail in complex string scenarios
3. **Performance**: Can lag with large namespaces
4. **Lambda Handling**: Disabled in lambda contexts (too complex)

## Future Improvements

From code comments:
- "TODO: 't' → 'not' should be space completion not char handler"
- "TODO: Fix backspace shouldn't erase everything"
- "TODO: Highlight callables different color"
- "TODO: Add way to add space without autocomplete"

## Tips for Users

1. **Hold Alt** for normal space
2. **Use Escape** to cancel completion
3. **Backspace** to undo transformation
4. **Tab** for traditional completion

## Code Locations

- **Main Logic**: Find with `grep "@handle.*' '.*microcompletions_enabled" key_bindings.py`
- **Space Handler**: Find with `grep "@handle.*' '.*filter=~vi_mode" key_bindings.py`
- **Character Handlers**: Find with `grep "@handle.*'[a-z]'.*microcompletions" key_bindings.py`
- **Enable Check**: Find with `grep "microcompletions_enabled = Condition" key_bindings.py`
- **Callable Detection**: Find with `grep "def is_callable_token" key_bindings.py`