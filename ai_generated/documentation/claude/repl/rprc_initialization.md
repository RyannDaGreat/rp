# RPRC Initialization System

## Overview
The RPRC (RP Run Commands) file is RP's initialization system, similar to `.bashrc` or `.vimrc`, that runs custom Python code every time RP starts.

## File Location
```python
rprc_file_path = os.path.join(_rp_folder, ".rprc")
# Typically: ~/.rp/.rprc
```

## Default RPRC Content

The default RPRC file created on first run contains:

```python
## Add the current directory to the path
__import__("sys").path.append(__import__("os").getcwd())

## Auto-download pip imports
#__import__("rp").r._pip_import_autoyes=True
#__import__("rp").r._pip_install_needs_sudo=False

## Set terminal cursor to bar instead of block
#__import__('rp').set_cursor_to_bar()

## Custom command prefix shortcuts
#__import__('rp').r._add_pterm_prefix_shortcut("fu","!!fileutil")
#__import__('rp').r._add_pterm_prefix_shortcut("fp",["fansi_print('","','green bold')"])

## Custom pterm commands
#__import__('rp').r._add_pterm_command_shortcuts('''
#     CLC $r._pterm_cd("~/CleanCode")
#     RZG $os.system(f"cd {$get_path_parent($get_module_path(rp)} ; lazygit")
#''')

## Protected folders for CDH/CDC
__import__("rp").cdc_protected_prefixes+=[
   # '/Users/ryan/sshfs/' 
]

## Import RP namespace (optional)
#from rp import *
```

## Execution Process

### 1. When RPRC Runs
```python
# Find with: grep "_pterm_exeval.*rprc" r.py
_pterm_exeval("None", *dicts)  # Initialize
_, error = _pterm_exeval(rprc, *dicts)  # Execute RPRC
if error:
    fansi_print("ERROR in RPRC:", 'red', 'bold')
    show_error(error)
```

### 2. Execution Context
- Runs in the main REPL namespace
- Has access to all RP functions
- Errors are caught and displayed
- Doesn't stop REPL from starting

## RPRC Commands

### Accessing RPRC
- `RPRC` - Open RPRC in vim
- `RPRC EDIT` - Edit RPRC file
- `RPRC PATH` - Show RPRC path
- `RPRC ADD <code>` - Append code to RPRC

### Managing RPRC
```python
def _get_ryan_rprc_path():
    if not file_exists(rprc_file_path):
        string_to_text_file(rprc_file_path, _default_rprc)
    return text_file_to_string(rprc_file_path)
```

## Common Customizations

### 1. Auto-Import Modules
```python
# Always import common libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
```

### 2. Custom Shortcuts
```python
# Add command shortcuts
__import__('rp').r._add_pterm_command_shortcuts('''
    PROJ $r._pterm_cd("~/projects")
    GS git status
    GL git log --oneline -10
''')

# Add prefix shortcuts
__import__('rp').r._add_pterm_prefix_shortcut("!", "!!")
```

### 3. Environment Settings
```python
# Enable features
__import__("rp").r._pip_import_autoyes = True
__import__("rp").r._profiler = False
__import__("rp").r._tictoc = True
__import__("rp").r.use_ans_history = True

# Display settings
__import__('rp').set_cursor_to_bar()
__import__('rp').r.enable_fansi_print = True
```

### 4. Path Management
```python
import sys
import os

# Add custom paths
sys.path.append("/path/to/my/modules")
sys.path.append(os.path.expanduser("~/mylib"))

# Set environment variables
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
```

### 5. Protected Directories
```python
# Protect mounted drives from CDH CLEAN
__import__("rp").cdc_protected_prefixes += [
    '/mnt/network/',
    '/Volumes/External/',
    '~/sshfs/'
]
```

## Advanced Features

### 1. Conditional Initialization
```python
import platform

if platform.system() == "Darwin":
    # Mac-specific settings
    __import__('rp').r.enable_mac_features = True
elif platform.system() == "Linux":
    # Linux-specific settings
    pass
```

### 2. Project-Specific Settings
```python
import os
cwd = os.getcwd()

if "ml_project" in cwd:
    import torch
    torch.set_default_dtype(torch.float32)
    print("ML Project mode activated")
```

### 3. Custom Functions
```python
# Define helper functions available in every session
def quick_plot(data):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.plot(data)
    plt.show()

def load_config():
    import json
    with open("config.json") as f:
        return json.load(f)
```

### 4. Startup Messages
```python
# Display welcome message
__import__('rp').fansi_print("""
╔══════════════════════════════════╗
║   Welcome to RP Development      ║
║   Project: Neural Networks       ║
╔══════════════════════════════════╝
""", 'cyan', 'bold')

# Show current directory
print(f"Working in: {os.getcwd()}")
```

## Settings Override System

### 1. RPRC Settings Override
```python
_rprc_pterm_settings_overrides = {}  # Modified in RPRC

def _load_pyin_settings_file():
    settings = eval(text_file_to_string(_pyin_settings_file_path))
    settings.update(_rprc_pterm_settings_overrides)
    return settings
```

### 2. Common Overrides
```python
# In RPRC:
__import__('rp').r._rprc_pterm_settings_overrides = {
    'complete_while_typing': False,
    'enable_history_search': True,
    'vi_mode': False,
}
```

## Error Handling

### 1. RPRC Errors Don't Stop REPL
```python
try:
    exec(rprc_content)
except Exception as e:
    fansi_print("ERROR in RPRC:", 'red', 'bold')
    print_stack_trace(e)
    # REPL continues normally
```

### 2. Debugging RPRC
```python
# Add to RPRC for debugging
try:
    # Your code here
    pass
except Exception as e:
    __import__('rp').print_verbose_stack_trace(e)
```

## Best Practices

### 1. Keep It Fast
- Avoid heavy imports that slow startup
- Use lazy imports when possible
- Profile with `time rp -c "exit()"`

### 2. Error Recovery
```python
# Wrap risky operations
try:
    import heavy_module
except ImportError:
    print("Warning: heavy_module not available")
```

### 3. Documentation
```python
# Document your customizations
"""
My RPRC Configuration
- Auto-imports: numpy, pandas
- Custom shortcuts: PROJ, GS
- Features: profiling disabled for speed
"""
```

### 4. Version Control
```bash
# Back up your RPRC
cp ~/.rp/.rprc ~/.rp/.rprc.backup

# Track in git
cd ~/.rp
git init
git add .rprc
git commit -m "My RP configuration"
```

## Integration with Other Systems

### 1. With Command Shortcuts
RPRC can add new shortcuts that become available immediately

### 2. With pip_import
Set auto-yes for seamless package installation

### 3. With Profiling
Enable/disable profiling by default

### 4. With History
Configure history settings and limits

## Tips & Tricks

### 1. Quick Testing
```bash
# Test RPRC without entering REPL
rp -c "print('RPRC loaded successfully')"
```

### 2. Multiple Configurations
```python
# In RPRC - load different configs
import os
if os.path.exists(".rp_local"):
    exec(open(".rp_local").read())
```

### 3. Performance Mode
```python
# Minimal RPRC for maximum speed
__import__("sys").path.append(__import__("os").getcwd())
# Nothing else - pure speed
```

### 4. Development Mode
```python
# Rich RPRC for development
from rp import *
__import__('rp').r._reload = True  # Auto-reload
__import__('rp').r._profiler = True  # Profiling
__import__('rp').r._tictoc = True  # Timing
```

## File Creation

### First Run
```python
def _get_ryan_rprc_path():
    if not file_exists(rprc_file_path):
        # Creates default RPRC on first run
        string_to_text_file(rprc_file_path, _default_rprc)
    return text_file_to_string(rprc_file_path)
```

### Manual Reset
```bash
# Reset to default RPRC
rm ~/.rp/.rprc
rp  # Will recreate default
```

## Security Considerations

### 1. Code Execution
- RPRC runs with full Python permissions
- Be careful with downloaded RPRC files
- Review before using others' configurations

### 2. Path Additions
- Adding paths can expose modules
- Verify path contents before adding

### 3. Environment Variables
- Can affect system behavior
- Document any changes made

This initialization system makes RP highly customizable while maintaining safety and performance.