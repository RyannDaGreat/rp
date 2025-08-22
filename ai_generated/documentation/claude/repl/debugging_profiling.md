# RP Debugging and Profiling System

## Overview
RP provides comprehensive debugging and profiling capabilities built directly into the REPL, making performance analysis and debugging seamless.

## Profiling System

### 1. Basic Profiling (PROF)

#### Commands
- `PROF ON` - Enable profiling for all commands
- `PROF OFF` - Disable profiling
- `PROF` - Toggle profiling
- `PROF DEEP` - Enable deep profiling (includes external libraries)

#### How It Works
```python
# When profiling is enabled:
if _profiler:
    profiler = Profiler()
    profiler.start()
    # Execute user code
    profiler.stop()
    print(profiler.output_text(unicode=True, color=True, show_all=_PROF_DEEP))
```

#### Output Format
- Color-coded output showing function calls
- Time spent in each function
- Call counts
- Excludes functions taking <1ms by default

### 2. Line Profiling (LINEPROF)

#### Commands
- `LINEPROF ON` - Enable line-by-line profiling
- `LINEPROF OFF` - Disable line profiling
- `LINEPROF` - Toggle line profiling

#### Features
- Shows execution time per line
- Identifies bottlenecks within functions
- More granular than function profiling

### 3. Flamechart Visualization

#### Commands
- `PROF FLAME` - Generate and display flamechart HTML
- `PROF FLAME OPEN` - Open flamechart in browser
- `PROF FLAME COPY` - Copy compressed flamechart to clipboard
- `PROF FLAME PASTE` - Paste and open flamechart from clipboard

#### Implementation
```python
def _display_pterm_flamechart(local=False):
    if _prev_pterm_profiler is None:
        fansi_print("Nothing profiled yet", 'yellow bold')
        return
    
    html = _prev_pterm_profiler.output_html()
    if local:
        path = temporary_file_path('html')
        save_text_file(html, path)
        open_file_with_default_application(path)
    return html
```

### 4. Performance Timing (TICTOC)

#### Commands
- `TICTOC ON` - Show execution time for each command
- `TICTOC OFF` - Disable timing display
- `TICTOC` - Toggle timing

#### Display
Shows time in seconds after each command execution

## Debugging System

### 1. Debug Mode

#### Activation
- Add `debug()` at top of code
- Use `\de` microcompletion to toggle
- Ctrl+T to toggle debug() line

#### Debuggers Supported
- **pudb** - Visual debugger (preferred in terminal)
- **pdb** - Standard Python debugger
- **ipdb** - IPython debugger (in Jupyter)

### 2. Error Inspection

#### Commands
- `MORE` - Show last error traceback
- `MMORE` - Detailed stack trace with locals
- `HMORE` - Syntax-highlighted stack trace
- `RMORE` - Rich formatted stack trace
- `AMORE` - Set ans to the error object
- `DMORE` - Enter post-mortem debugger

#### Error Storage
```python
error_stack = UndoRedoStack(clear_redo_on_do=False)
# Maintains history of all errors
# Can navigate with undo/redo
```

### 3. Stack Trace Display

#### Functions
```python
print_stack_trace(error, verbose=False)
print_verbose_stack_trace(error)
print_highlighted_stack_trace(error)
print_rich_stack_trace(error)
```

#### Features
- Color-coded output
- Local variable inspection
- Source code context
- Frame navigation

### 4. Post-Mortem Debugging

#### DMORE Command
```python
if currently_in_a_tty():
    try:
        pip_import('pudb').post_mortem(tb)
    except:
        import pdb
        pdb.post_mortem(tb)
```

#### Features
- Inspect state at error point
- Navigate call stack
- Evaluate expressions in error context

## Memory Profiling

### 1. Garbage Collection Control

#### Commands
- `GC ON` - Force GC before each prompt
- `GC OFF` - Disable forced GC
- `GC` - Toggle GC mode

#### Use Case
Useful for PyTorch CUDA memory management:
```python
if do_garbage_collection_before_input:
    garbage_collector.collect()
```

### 2. Memory Monitoring

#### Commands
- `MONITOR` - System monitoring with glances
- `TOP` - Process viewer with bpytop
- `GPU` - GPU memory and usage

## Advanced Features

### 1. Module Reloading

#### Commands
- `RELOAD ON` - Auto-reload changed modules
- `RELOAD OFF` - Disable auto-reload

#### Implementation
```python
if _reload:
    _reload_modules()  # Reimports changed modules
```

### 2. IPython Integration

#### Activation
- `IPYTHON ON` - Use IPython evaluation
- `IPYTHON OFF` - Use standard evaluation

### 3. Profiler Persistence

#### Global Variables
```python
_prev_pterm_profiler = None  # Last profiler results
_prev_line_profiler = None   # Last line profiler results
```

Profiler results persist across commands for analysis

## Configuration

### RPRC Settings
```python
# In ~/.rp/.rprc

# Enable profiling by default
__import__('rp').r._profiler = True

# Enable deep profiling
__import__('rp').r._PROF_DEEP = True

# Enable timing by default
__import__('rp').r._tictoc = True

# Force garbage collection
__import__('rp').r.do_garbage_collection_before_input = True
```

### Performance Thresholds
- Functions <1ms excluded from basic profiling
- Snapshot warning if >250ms
- GC triggered based on memory pressure

## Integration with Other Systems

### 1. With Snapshot System
Profiling doesn't interfere with UNDO/REDO

### 2. With Variable Tracking
Profiler aware of user-created variables

### 3. With Error Handling
Errors during profiling are caught gracefully

## Tips & Best Practices

### 1. Profiling Workflow
```python
PROF ON          # Enable profiling
# Run slow code
PROF FLAME OPEN  # Visualize results
PROF OFF         # Disable when done
```

### 2. Line Profiling for Bottlenecks
```python
LINEPROF ON
# Run specific function
LINEPROF OFF
```

### 3. Memory Issues
```python
GC ON           # Force garbage collection
MONITOR         # Watch memory usage
```

### 4. Debugging Workflow
```python
debug()         # Add to top of code
# Run code - drops into debugger
DMORE          # Post-mortem on errors
```

## Performance Impact

### Overhead
- Basic profiling: ~5-10% overhead
- Deep profiling: ~20-30% overhead
- Line profiling: ~50-100% overhead
- TICTOC: Negligible overhead

### Memory Usage
- Profiler results stored in memory
- Flamechart generation can use significant memory
- Snapshot system separate from profiling

## Common Use Cases

### 1. Finding Slow Functions
```python
PROF ON
# Run slow operation
# See which functions take most time
```

### 2. Optimizing Loops
```python
LINEPROF ON
for i in range(1000):
    slow_operation()
# See which lines in loop are slow
```

### 3. Memory Leaks
```python
GC ON
MONITOR
# Watch memory grow over time
```

### 4. Interactive Debugging
```python
try:
    buggy_code()
except:
    DMORE  # Enter debugger at error
```

## Implementation Details

### Profiler Library
Uses `pyinstrument` for profiling:
- Statistical profiler
- Low overhead
- Beautiful output

### Line Profiler
Uses `line_profiler` when available:
- Deterministic profiling
- Per-line timing
- C extension for speed

### Debugger Selection
Priority order:
1. pudb (if in terminal)
2. ipdb (if in Jupyter)
3. pdb (fallback)

This comprehensive debugging and profiling system makes RP one of the most powerful REPLs for performance analysis and debugging.