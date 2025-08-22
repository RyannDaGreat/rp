# Variable Tracking System (VARS)

## Overview
RP's VARS system tracks all user-created variables in the REPL session, displaying them in real-time and providing powerful variable management features.

## Core Components

### 1. Tracking Set
```python
_user_created_var_names = set()  # In r.py
rp_pt_user_created_var_names = []  # In r_iterm_comm.py
```

### 2. Display Buffer
- Buffer name: `'vars'`
- Updated via `rp_pt_VARS` in r_iterm_comm
- Shows sorted list of variable names

## How It Works

### Variable Detection
After each command execution:
```python
# Capture scope before execution
scope_before = set(scope())

# Execute user code
exec(code, scope)

# Detect new variables
new_vars = set(scope()) - scope_before
_user_created_var_names |= new_vars
```

### Cleanup
Removes deleted variables:
```python
# Remove variables that no longer exist
_user_created_var_names &= set(scope())
```

### Display Update
Updates display buffer:
```python
rp.r_iterm_comm.rp_VARS_display = str(
    ' '.join(sorted(list(_user_created_var_names)))
)
```

## VARS Commands

### Display Commands
- `VARS` - Show all tracked variables
- `VS` - Variables show (alias)
- `VSS` / `VSM` - Select variables with fuzzy finder
- `VSR` - Repr all variables (detailed view)

### Copy Commands
- `CVS` / `CVSR` - Copy vars repr to clipboard
- `COVSR` - Copy vars repr (alternative)

### Management
- `VARS OFF` - Disable variable tracking
- `VARS CLEAR` - Clear tracked variables
- `VARS RESET` - Reset tracking system

## Display Features

### Real-Time Updates
- Updates after every command
- Shows additions immediately
- Removes deleted vars automatically

### Sorting
Variables displayed in alphabetical order:
```python
sorted(list(_user_created_var_names))
```

### Filtering
Excludes system variables:
- No `__builtins__`
- No imported modules (unless assigned)
- No RP internal variables

## Integration Points

### With Autocompletion
Completer uses tracked variables:
```python
user_created_var_names = set(ric.rp_pt_user_created_var_names)
# Prioritizes user variables in suggestions
```

### With Real-Time Eval
Real-time evaluator can access all tracked variables

### With History
Variable state can be saved in snapshots

## Special Features

### Variable Inspection
Use `rinsp()` on any tracked variable:
```python
x = [1, 2, 3]
# 'x' now in VARS
rinsp(x)  # Detailed inspection
```

### Bulk Operations
Select multiple variables:
```python
VSS  # Opens fuzzy selector
# Select variables with Tab
# Operations apply to all selected
```

### Variable Repr
`VSR` command shows detailed representation:
```python
# For each variable shows:
# - Name
# - Type
# - Value (truncated if large)
# - Memory address
```

## Display Window

### Layout Configuration
In layout.py:
```python
ConditionalContainer(
    content=HSplit([
        Window(BufferControl(
            buffer_name='vars',
            lexer=SimpleLexer(default_token=Token.Docstring)
        ), wrap_lines=True)
    ]),
    filter=ShowVarSpace(python_input) & ~IsDone(),
)
```

### Visual Separation
Can display with separator from real-time eval:
```python
ConditionalContainer(
    content=Window(
        width=D.exact(1),
        content=FillControl('│', token=Token.Window.TIItleV2)
    ),
    filter=ShowVarSpaceAndShowRealtimeInput(python_input)
)
```

## Performance Considerations

### Set Operations
Uses Python sets for O(1) lookups:
```python
_user_created_var_names = set()  # Fast membership testing
```

### Incremental Updates
Only processes changes:
```python
new_vars = set(scope()) - scope_before  # Only new additions
```

### Display Throttling
Updates batched per command, not per keystroke

## Configuration

### Enabling/Disabling
Controlled by `ShowVarSpace` filter

### Display Options
- Show with real-time eval
- Show alone
- Hide completely

## Common Use Cases

### 1. Learning/Teaching
See all variables at a glance - great for education

### 2. Debugging
Track variable creation/deletion during execution

### 3. Data Analysis
Monitor dataframes and arrays as you work

### 4. Cleanup
Identify variables to delete:
```python
# See all vars in VARS display
del unwanted_var  # Automatically removed from display
```

## Implementation Details

### Scope Detection
Uses `scope()` function to get current namespace:
```python
def scope():
    return merged_dicts(*reversed(dicts))
```

### Assignment Detection
Tracks any name binding:
- Simple assignment: `x = 5`
- Multiple assignment: `a, b = 1, 2`
- Augmented assignment: `x += 1`
- Function definitions: `def func():`
- Class definitions: `class MyClass:`

### Exclusions
Doesn't track:
- Temporary variables in comprehensions
- Variables in functions (local scope)
- System variables
- Imported names (unless reassigned)

## Tips & Tricks

### 1. Quick Variable Check
Glance at VARS display instead of `dir()`

### 2. Bulk Deletion
```python
# Select variables to delete
for var in ['a', 'b', 'c']:
    del globals()[var]
```

### 3. Export Variables
```python
CVS  # Copy all variable definitions
# Paste in new session to recreate
```

### 4. Variable History
Variables tracked across UNDO/REDO operations

## Code Locations

- **Tracking Logic**: Search `grep "_user_created_var_names.*|=" r.py`
- **Display Update**: Search `grep "rp_VARS_display" r.py`
- **Cleanup**: Search `grep "_user_created_var_names.*&=" r.py`
- **Commands**: Search `grep "'VARS'\|'VS'" r.py` in command shortcuts
- **Display Buffer**: Search `grep "buffer_name='vars'" layout.py`
- **State Storage**: Search `grep "rp_pt_user_created_var_names" r_iterm_comm.py`