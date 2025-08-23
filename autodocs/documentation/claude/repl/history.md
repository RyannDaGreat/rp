# History and Persistence System

## Overview
RP's REPL maintains multiple types of history with sophisticated persistence, snapshots, and undo/redo capabilities.

## History Types

### 1. Command History
Multiple tracking levels:
- `successful_command_history` - Commands that executed successfully
- `all_command_history` - Everything typed (including errors)
- File: `~/.rp/HISTORY`

### 2. Answer History
- `ans_history` - All computed answer values
- `ans_redo_history` - For redo functionality
- Controlled by `use_ans_history` flag

### 3. Directory History
- `pwd_history` - Directory navigation trail
- `_cd_history` - Global CD history
- File: `~/.rp/r.py.rp_cd_history.txt`

### 4. Snapshot History
- `snapshot_history` - Complete namespace snapshots
- Enables UNDO/REDO of entire session state
- Memory-only (not persisted)

## File Locations

### Primary History Files
```python
history_filename = "~/.rp/r.py.history.txt"  # ptpython history
pterm_history_filename = "~/.rp/HISTORY"  # Main REPL history
cd_history_path = "~/.rp/r.py.rp_cd_history.txt"
```

### History File Format
```
############################################################
########### BEGINNING OF PSEUDO TERMINAL SESSION ###########
###########         2024-01-15 10:30:45         ###########
############################################################

x = 5
print(x)
y = x * 2
```

## Command History System

### Recording
Every successful command is recorded:
```python
def _write_to_pterm_hist(entry):
    global _pterm_hist_file
    if _pterm_hist_file is None:
        _pterm_hist_file = open(pterm_history_filename, 'a+')
        # Write session header
    _pterm_hist_file.write('\n' + entry)
```

### Display
`HISTORY` command shows color-coded history:
- **Green**: Single-line commands
- **Yellow**: Multi-line commands
- **Bold yellow**: Alternating multi-line for readability

### Navigation
- `PREV` / `P` - Previous command
- `NEXT` / `N` - Next command
- Arrow keys in ptpython mode

## Answer History (ans)

### Automatic Tracking
Every computed value stored:
```python
def set_ans(val, save_history=True, snapshot=True):
    if save_history and use_ans_history:
        ans_history.append(val)
    dicts[0]['ans'] = val
```

### Display Options
- Green: Normal ans with history
- Yellow: Temporary ans (no history)
- Gray: History disabled

### Special Formatting
Multi-line arrays/dataframes aligned:
```python
ans = [[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]]
```

## Snapshot System (UNDO/REDO)

### How Snapshots Work
```python
def get_snapshot():
    # Captures entire namespace state
    return deepcopy(scope())

def take_snapshot():
    if snapshots_enabled:
        snapshot_history.append(get_snapshot())
```

### UNDO Operations
- `UNDO` - Revert to previous snapshot
- `REDO` - Move forward in snapshot history
- `UNDO ALL` - Clear all snapshots
- `UNDO OFF` - Disable snapshots (performance)

### Performance Warning
Large namespaces can make snapshots slow:
```python
if time.time() - start > 0.25:
    # Warning: snapshot took too long
    # Suggests using UNDO OFF
```

## Directory History

### Tracking
Every CD command recorded:
```python
def _pterm_cd(path):
    pwd_history.append(get_current_directory())
    _cd_history.append(path)
    set_current_directory(path)
```

### Navigation Commands
- `CDH` - Interactive history browser
- `CDB` / `B` - Go back in history
- `CDHF` - Fast history navigation
- `CDH GIT` - Find git repositories

### Persistence
CD history saved to file after each change

## History Browsers

### Interactive Selection
`QVH` - Query visual history with fuzzy finder:
```python
_input_select_multiple_history(pterm_history_filename)
```

### Multi-line History
Special handler for multi-line commands:
```python
_input_select_multiple_history_multiline(
    history_filename, 
    old_code=current_buffer
)
```

## PTython Integration

### History File
PTython maintains separate history:
```python
FileHistory(history_filename)  # ~/.rp/r.py.history.txt
```

### Buffer Persistence
Maintains buffer across sessions:
- Incomplete commands saved
- Restored on next launch

## Special Features

### 1. Session Headers
Each session marked with timestamp:
```
########### BEGINNING OF PSEUDO TERMINAL SESSION ###########
###########         2024-01-15 10:30:45         ###########
```

### 2. Fast History
Limited size for performance:
```python
_fast_pterm_history_size = 1024 * 1024  # 1MB limit
```

### 3. Permission Handling
Graceful handling of write failures:
```python
try:
    _write_to_pterm_hist(x)
except PermissionError:
    print("PERMISSION ERROR SAVING HISTORY")
```

### 4. History Cleaning
Commands to clean history:
- `HIST CLEAN` - Remove duplicates
- `HIST CLEAR` - Clear all history
- `CDC` / `CCL` - Clean CD history

## Configuration

### Enabling/Disabling

#### Answer History
```python
use_ans_history = True  # Toggle answer tracking
```

#### Snapshots
```python
snapshots_enabled = False  # Can break with large data
```

#### Command History
Always enabled (can't disable)

### Size Limits
- PTython history: Unlimited
- Fast history: 1MB
- Snapshots: Memory limited

## Tips & Tricks

### 1. Quick History Search
Use `QVH` for fuzzy search through history

### 2. Session Recovery
History files preserve work across crashes

### 3. Selective Undo
UNDO only reverts namespace, not file changes

### 4. History Export
```python
# Export history to file
history = print_history(return_as_string=True)
save_text_file(history, "session.py")
```

### 5. Clean Starts
```bash
rm ~/.rp/HISTORY  # Clear all history
```

## Performance Considerations

### Snapshot Performance
- Disabled by default for large data
- Deep copies entire namespace
- Can break with certain objects (e.g., FlannDict)

### History File I/O
- Buffered writes for performance
- File kept open during session
- Flushed on exit

### Memory Usage
- Snapshots can consume significant memory
- Answer history grows unbounded
- Consider periodic cleanup

## Code Locations

- **Main History**: Search `grep "successful_command_history\|all_command_history" r.py`
- **Snapshot System**: Search `grep "def get_snapshot\|def take_snapshot" r.py`
- **History Display**: Search `grep "def print_history" r.py`
- **File Writing**: Search `grep "def _write_to_pterm_hist" r.py`
- **CD History**: Search `grep "pwd_history\|_cd_history" r.py`
- **PTython History**: Search `grep "FileHistory" python_input.py`