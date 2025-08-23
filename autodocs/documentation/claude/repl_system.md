# RP's Custom REPL System

## Overview
When you run `rp` without arguments, you're not getting standard ptpython - you're getting a **heavily modified REPL** with revolutionary features built specifically for RP.

## Architecture

### Communication Bridge: r_iterm_comm.py
Central communication module that connects:
- RP's evaluation system (`rp.r`)
- Modified prompt_toolkit (UI layer)
- Modified rp_ptpython (REPL logic)

Key shared state:
- `rp_evaluator` - Real-time evaluation function
- `python_input_buffers` - Dynamic UI buffers
- `current_input_text` - What user is typing
- `last_assignable_comm` - Last assigned variable
- `parenthesized_line` - Auto-parenthesized version

### Modified prompt_toolkit
Located at top-level `/rp/prompt_toolkit/` (not in libs/)
- Custom UI components for RP features
- Modified event loop for real-time updates
- Integration points with r_iterm_comm

### Modified rp_ptpython
Located at top-level `/rp/rp_ptpython/` (not in libs/)
- Every file imports `rp.r_iterm_comm`
- Custom completers with RP-aware suggestions
- Special UI filters and layouts

## Revolutionary Features

### 1. Realtime Evaluator
- **Live evaluation as you type**
- Shows result of expressions before you hit enter
- Buffer: `realtime_display`
- Filter: `ShowRealtimeInput`

### 2. Parenthesis Automator
- **Automatic parenthesis balancing**
- Shows properly parenthesized version of your code
- Buffer: `parenthesizer_buffer`
- Filter: `ShowParenthesisAutomator`

### 3. VARS Display
- **Live variable tracking**
- Shows current scope variables
- Updates in real-time as you create/modify variables
- Buffer: `vars`
- Filter: `ShowVarSpace`

### 4. Custom Autocompletion
- Module name completion (via threading)
- APT package suggestions
- RP function awareness
- Smart caching in `completion_cache_pre_origin_doc`

### 5. RP-Emacs Mode
- Not standard Emacs mode - custom "RP-Emacs"
- Special key bindings for RP features
- Vi mode also heavily customized

## Why Top-Level, Not libs/

These aren't vendored libraries - they're **core RP subsystems**:
1. Too heavily modified to merge upstream changes
2. Integral to RP's user experience
3. Deep bidirectional integration with RP core
4. Custom features that don't exist in standard versions

## Data Flow

```
User types in REPL
    ↓
rp_ptpython captures input
    ↓
Updates r_iterm_comm.current_input_text
    ↓
RP evaluator processes in real-time
    ↓
Updates UI buffers via r_iterm_comm
    ↓
prompt_toolkit renders live updates
    ↓
User sees real-time evaluation/completion
```

## Key Files

### /rp/r_iterm_comm.py
- Communication bridge
- Shared state management
- ~30 global variables for REPL state

### /rp/rp_ptpython/python_input.py
- Main REPL input handler
- PythonInput class with RP customizations
- Integration with history, completion, evaluation

### /rp/rp_ptpython/layout.py
- Custom UI layout
- Special windows for realtime features
- ~800+ lines of UI code

### /rp/rp_ptpython/completer.py
- RP-aware autocompletion
- Module name discovery
- APT package suggestions
- Smart caching

### /rp/rp_ptpython/key_bindings.py
- Custom keyboard shortcuts
- RP-specific commands
- Integration with r_iterm_comm

## Usage

```bash
# Start RP REPL with all features
rp

# In REPL, you get:
# - Live evaluation as you type
# - Variable display
# - Smart autocompletion
# - Parenthesis automation
```

## Technical Achievement

This represents a **complete reimagining** of the Python REPL:
- Not just a ptpython fork - a ground-up rebuild
- Real-time features that don't exist elsewhere
- Deep integration impossible with standard libraries
- Performance optimized (no GC during input)

The modifications are so extensive that these are essentially new libraries that happen to share some DNA with prompt_toolkit/ptpython.

## Comprehensive Documentation

For deep dives into specific features, see the `/documentation/claude/repl/` directory:
- **[overview.md](repl/overview.md)** - Complete architecture overview
- **[realtime_eval.md](repl/realtime_eval.md)** - Real-time evaluation system
- **[parenthesis.md](repl/parenthesis.md)** - Parenthesis automator details
- **[vars_tracking.md](repl/vars_tracking.md)** - Variable tracking system
- **[commands.md](repl/commands.md)** - 200+ command shortcuts
- **[microcompletions.md](repl/microcompletions.md)** - Intelligent auto-transformations
- **[history.md](repl/history.md)** - History and persistence features