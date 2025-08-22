# Real-Time Evaluation System

## Overview
RP's real-time evaluation is one of its most revolutionary features - it evaluates your Python expressions AS YOU TYPE, showing results before you hit enter.

## How It Works

### 1. Text Capture
Every keystroke updates `r_iterm_comm.current_input_text` via the modified prompt_toolkit event loop.

### 2. Evaluation Function
Located in `pseudo_terminal()` function (find with `grep "def try_eval" r.py`):

```python
def try_eval(text, return_value_as_boolean=False):
    if text != rp.r_iterm_comm.try_eval_mem_text:
        # Text changed, evaluate it
        rp.r_iterm_comm.try_eval_mem_text = text
        try:
            out = str(eval(text, scope()))
            if len(out) > 2000:
                out = out[:2000] + "..."
            rp.r_iterm_comm.rp_evaluator_mem = out
        except Exception as E:
            return str(rp.r_iterm_comm.rp_evaluator_mem) + "\nERROR: " + str(E)
    else:
        # Text unchanged, return cached result
        return rp.r_iterm_comm.rp_evaluator_mem
```

### 3. Display Buffer
Results shown in `realtime_display` buffer:
- Located in layout.py (find with `grep "buffer_name='realtime_display'" layout.py`)
- Uses lexer for syntax highlighting
- Wraps lines for readability

### 4. Caching System
- `try_eval_mem_text` - Last evaluated text
- `rp_evaluator_mem` - Cached result
- Avoids re-evaluation of unchanged text

## Features

### Safe Evaluation
- Only evaluates expressions, not statements
- Catches all exceptions
- Shows "ERROR: " prefix for failures
- Truncates long outputs (>2000 chars)

### Performance Optimizations
- Caching prevents redundant evaluation
- Runs in main thread (no async complexity)
- Disabled during multiline editing

### Smart Display
- Syntax highlighting via lexer
- Line wrapping for long results
- Shows in dedicated window region
- Hidden when not applicable

## Configuration

### Enabling/Disabling
Controlled by `ShowRealtimeInput` filter in filters.py:
```python
class ShowRealtimeInput(PythonInputFilter):
    def __call__(self, cli):
        return self.python_input.show_realtime_input
```

### Buffer Management
The display buffer is managed via `r_iterm_comm.python_input_buffers`:
```python
# In layout.py
BufferControl(
    buffer_name='realtime_display',
    lexer=lexer,  # Python syntax highlighting
)
```

## Examples

### Simple Expression
Type: `2 + 2`
Shows: `4` (immediately, before pressing enter)

### Variable Reference
```python
x = 10
# Type: x * 5
# Shows: 50
```

### Error Display
Type: `undefined_var`
Shows: `ERROR: name 'undefined_var' is not defined`

### Long Output Truncation
Type: `list(range(10000))`
Shows: `[0, 1, 2, 3, ... (truncated at 2000 chars)]`

## Integration Points

### With Variable Tracking
Real-time eval uses current scope from VARS display

### With Parenthesis Automator
Both features run simultaneously without conflict

### With Autocompletion
Completion suggestions based on evaluated types

## Limitations

1. **Expressions Only** - Can't evaluate statements like `x = 5`
2. **No Side Effects** - Evaluation is read-only
3. **Performance** - Complex expressions may lag
4. **Truncation** - Long outputs cut at 2000 chars

## Code Locations

- **Evaluator**: Find with `grep "def try_eval" r.py` - try_eval function
- **Display**: Find with `grep "buffer_name='realtime_display'" layout.py` - realtime_display buffer
- **Filter**: Find with `grep "class ShowRealtimeInput" filters.py` - ShowRealtimeInput
- **State**: `/rp/r_iterm_comm.py` - rp_evaluator, rp_evaluator_mem

## Future Enhancements

Potential improvements identified in code:
- Async evaluation for heavy computations
- Configurable truncation length
- Statement evaluation preview
- Type information display