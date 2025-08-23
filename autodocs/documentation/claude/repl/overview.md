# RP REPL System - Complete Deep Dive

## Architecture Overview

The RP REPL (called `pseudo_terminal`) is a revolutionary Python REPL that provides:
- **Real-time evaluation** as you type
- **Live variable tracking**
- **Automatic parenthesis balancing**
- **Advanced history with undo/redo**
- **Cell-based execution** (like Jupyter)
- **Multiple evaluation modes** (tictoc, profiling, IPython)

## Core Components

### 1. Main Entry Points
- `rp` (command) → `__main__.py` → `_pterm()` → `pseudo_terminal()`
- `pseudo_terminal()` is a 4000+ line function in r.py (find with `grep "def pseudo_terminal" r.py`)

### 2. Communication Layer: r_iterm_comm.py
Central state management between RP and the UI:
```python
globa = {}  # Global scope dictionary
rp_evaluator = lambda x: None  # Real-time evaluator function
current_input_text = ""  # What user is typing
python_input_buffers = {}  # Dynamic UI buffers
last_assignable_comm = None  # Last assigned variable
parenthesized_line = ""  # Auto-parenthesized version
ans = None  # Current answer value
```

### 3. Modified Libraries
- **rp_ptpython/** - Heavily modified Python REPL
- **prompt_toolkit/** - Custom terminal UI framework
- Both at top-level (not libs/) due to extensive modifications

## Key Features

### Real-Time Evaluation
As you type, RP evaluates your expression and shows the result:
- Updates via `rp_evaluator` function in r_iterm_comm
- Caches results to avoid re-evaluation (`rp_evaluator_mem`)
- Shows errors inline without interrupting typing

### Variable Tracking (VARS Display)
- Shows all variables in current scope
- Updates in real-time as you create/modify variables
- Tracks via `_user_created_var_names` set
- Displayed in 'vars' buffer

### Parenthesis Automator
- Visualizes parenthesis matching with box drawing characters
- Creates ASCII art showing nesting levels
- Example: `[[(hello)]]` shows matching brackets visually

### Smart Autocompletion
- Module name discovery (runs in background thread)
- APT package suggestions (on Linux)
- Callable detection (functions highlighted green)
- Iterable detection for smart completions

## Command System

### Special Keywords (detected in pseudo_terminal)
- `HELP` - Show help
- `MORE` / `MMORE` - Show error traceback
- `UNDO` / `REDO` - Navigate history snapshots
- `UNDO OFF` / `UNDO ALL` - Control snapshot system
- `VARS` - Show variables
- `HISTORY` - Show command history
- `CD` - Change directory with history
- `RETURN` - Exit REPL

### Keyboard Shortcuts
- **Ctrl+L** - Clear screen
- **Ctrl+D** - Duplicate line / Exit
- **Ctrl+W** - Run current cell
- **Ctrl+U** - Special command mode
- **Ctrl+P** - Previous in history
- **F2-F6** - Various UI toggles
- **Tab** - Smart completion
- **Alt+Enter** - Execute multiline

## Evaluation Modes

### Normal Mode
Standard Python evaluation with RP enhancements

### TicToc Mode (`_tictoc=True`)
Times execution of each command

### Profiler Mode (`_profiler=True`)
Full profiling of code execution

### Line Profiler Mode (`_line_profiler=True`)
Line-by-line execution timing

### IPython Mode (`_use_ipython_exeval=True`)
Use IPython's evaluation system

## History System

### Command History
- `successful_command_history` - Commands that worked
- `all_command_history` - Everything typed
- Green = single-line, Yellow = multi-line in display

### Answer History
- `ans_history` - All computed answers
- `ans_redo_history` - For redo functionality
- `use_ans_history` flag controls tracking

### Snapshot System
- `snapshot_history` - Full namespace snapshots
- Enables UNDO/REDO of entire session state
- Can be disabled with `snapshots_enabled=False`
- Warning if snapshot takes >0.25s (large namespace)

### Directory History
- `pwd_history` - Tracks directory changes
- `_cd_history` global list
- Special CD command with navigation

## The pseudo_terminal Function

### Key Variables
- `dicts` - Namespace hierarchy (globals, locals, custom)
- `ans` - Current answer value
- `error` - Last error for MORE command
- `should_print_ans` - Control answer display
- `use_modifier` - Enable command modifiers
- `allow_keyboard_interrupt_return` - Ctrl+C behavior

### Helper Functions
- `set_ans()` - Update answer with history
- `take_snapshot()` - Save namespace state
- `show_error()` - Display errors gracefully
- `print_history()` - Show command history
- `pterm_pretty_print()` - Smart output formatting

## Inspector System (rinsp)

Ryan's Inspector provides deep object introspection:
- Shows all attributes (methods green, modules blue)
- Filters with search
- Shows source code
- Displays documentation
- Smart truncation for large outputs

## Files to Explore

### Core REPL Logic
- Find with `grep "def pseudo_terminal" r.py` - pseudo_terminal function
- Find with `grep "def python_input" r.py` - python_input function
- Find with `grep "def rinsp" r.py` - rinsp inspector

### Communication
- `/rp/r_iterm_comm.py` - State management

### UI Components
- `/rp/rp_ptpython/layout.py` - UI layout with special windows
- `/rp/rp_ptpython/python_input.py` - Input handling
- `/rp/rp_ptpython/completer.py` - Autocompletion
- `/rp/rp_ptpython/key_bindings.py` - Keyboard shortcuts

### Filters & Display
- `/rp/rp_ptpython/filters.py` - ShowVarSpace, ShowRealtimeInput, etc.

## Next Steps
See subdocuments for deep dives into:
- [Real-Time Evaluation](realtime_eval.md)
- [Parenthesis Automator](parenthesis.md)
- [Variable Tracking](vars_tracking.md)
- [Key Bindings](keybindings.md)
- [History System](history.md)