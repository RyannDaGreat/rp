# Chainsaw Debugger

## Overview
**File**: `chainsaw.py`  
**Type**: Standalone debugging tool  
**Purpose**: Advanced Python execution tracer with conditional breakpoints

## Description
> *"This is the ultimate debugging tool when you know something weird is happening but you don't know where."*

Chainsaw is a sophisticated tracing debugger that monitors Python execution and automatically launches a debugger when specific conditions are met.

## Core Functionality

### `trap_namespace_tracer(**checks)`
Sets up a trace function that monitors local variables and triggers debugging when conditions match.

```python
def trap_namespace_tracer(**checks):
    def tracer(frame, event, args):
        flag = True
        for key, value in checks.items():
            namespace = frame.f_locals
            if key not in namespace or namespace[key] != value:
                flag = False
        if flag:
            print('CAUGHT!!!')
            set_pudb_trace_at_frame(frame, event, args)
        return tracer  # Must return tracer to maintain trace
    sys.settrace(tracer)
```

### `set_pudb_trace_at_frame(frame, event, args)`
Launches PuDB debugger at a specific execution frame.

```python
def set_pudb_trace_at_frame(frame, event, args):
    import pudb
    dbg = pudb._get_debugger()
    dbg.set_trace(frame)
    dbg.trace_dispatch(frame, event, args)
```

## Usage Examples

### Basic Variable Monitoring
```python
from rp.chainsaw import trap_namespace_tracer

def problematic_function():
    i = 0
    for _ in range(100):
        print('i=', i)
        i += 1
        i %= 30

# Set trap to trigger when i equals 19
trap_namespace_tracer(i=19)
problematic_function()
# Automatically opens debugger when i becomes 19
```

### Multiple Condition Monitoring
```python
# Monitor multiple variables simultaneously
trap_namespace_tracer(x=42, status='error', count=10)

# Will only trigger when ALL conditions are met:
# x == 42 AND status == 'error' AND count == 10
```

### Function Entry Monitoring
```python
# Using event parameter to detect function calls
def advanced_tracer(frame, event, args):
    if event == 'call' and frame.f_code.co_name == 'target_function':
        print(f"Entering function: {frame.f_code.co_name}")
        set_pudb_trace_at_frame(frame, event, args)
    return advanced_tracer

sys.settrace(advanced_tracer)
```

## How It Works

### 1. Trace Hook Installation
Uses Python's `sys.settrace()` to install a global trace function that monitors every line of execution.

### 2. Condition Evaluation
For each traced frame, checks local variables against specified conditions:
```python
namespace = frame.f_locals
if key not in namespace or namespace[key] != value:
    flag = False
```

### 3. Debugger Integration
When conditions match, automatically launches PuDB debugger at the exact execution point where conditions were met.

### 4. Execution Context
Preserves full execution context including:
- Local variables
- Global variables  
- Call stack
- Execution frame

## Advanced Features

### Event-Based Tracing
The `event` parameter provides different trace points:
- `'call'`: Function entry
- `'line'`: Line execution
- `'return'`: Function exit
- `'exception'`: Exception occurrence

### Frame Inspection
Full access to execution frame allows monitoring:
- `frame.f_locals`: Local variables
- `frame.f_globals`: Global variables
- `frame.f_code.co_name`: Function name
- `frame.f_code.co_filename`: Source file
- `frame.f_lineno`: Line number

## Performance Considerations

### Overhead
- **High overhead**: Traces every line of execution
- **Production unsuitable**: Only for debugging sessions
- **Memory impact**: Maintains trace function references

### Optimization Strategies
```python
# Limit tracing scope
def selective_tracer(frame, event, args):
    # Only trace specific modules
    if '/my_project/' not in frame.f_code.co_filename:
        return None
    
    # Your condition checking here
    return selective_tracer
```

## Comparison to Other Debug Tools

### vs. `pdb.set_trace()`
- **Chainsaw**: Conditional, automatic breakpoints
- **pdb**: Manual breakpoint placement

### vs. `hunter.py`
- **Chainsaw**: Focuses on namespace conditions
- **hunter**: More comprehensive tracing with complex predicates

### vs. IDE Debuggers
- **Chainsaw**: Programmatic, condition-based
- **IDE**: Interactive, visual debugging

## Limitations

### Current Implementation Issues
1. **Print statement bug**: `print('TRACE')` doesn't appear after debugger exit
2. **Limited condition types**: Only exact equality matching
3. **No subcommand support**: Cannot handle complex expressions

### Potential Improvements
```python
# Enhanced condition matching
def enhanced_tracer(**conditions):
    def tracer(frame, event, args):
        namespace = frame.f_locals
        for key, condition in conditions.items():
            if callable(condition):
                if not condition(namespace.get(key)):
                    return tracer
            else:
                if namespace.get(key) != condition:
                    return tracer
        # All conditions met
        set_pudb_trace_at_frame(frame, event, args)
        return tracer
    return tracer

# Usage with callable conditions
trap_enhanced_tracer(
    i=lambda x: x > 10 and x < 20,
    status=lambda x: x in ['error', 'warning']
)
```

## Integration with RP

### REPL Integration
Could be integrated into RP's debugging workflow:
```python
# Add to RP's debug commands
def debug_when(**conditions):
    from rp.chainsaw import trap_namespace_tracer
    trap_namespace_tracer(**conditions)
```

### Error Handling Enhancement
```python
# Combine with RP's error handling
def trap_on_error():
    def error_tracer(frame, event, args):
        if event == 'exception':
            set_pudb_trace_at_frame(frame, event, args)
        return error_tracer
    sys.settrace(error_tracer)
```

## Example Debugging Session

```python
# Problem: Loop variable behaving unexpectedly
def mystery_bug():
    items = [1, 2, 3, 4, 5]
    for i, item in enumerate(items):
        result = process_item(item)
        if i == 3:  # Something weird happens here
            do_something_complex()

# Solution: Use Chainsaw to catch the exact moment
from rp.chainsaw import trap_namespace_tracer

# Trap when we reach the problematic iteration
trap_namespace_tracer(i=3)
mystery_bug()

# Debugger automatically opens at i=3
# Can inspect: item, result, items, all local variables
# Can step through do_something_complex() interactively
```

This makes Chainsaw invaluable for those "impossible to reproduce" bugs where you know approximately when something goes wrong but need to see the exact execution state.