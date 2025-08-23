# RP Graveyard System - Complete Documentation

> **Note for Users:** This document describes an internal developer tool. The "graveyard" is a mechanism for automated refactoring and is not a feature you need to interact with. All functions, whether in `r.py` or `graveyard.py`, are equally available to you when you `import rp`.

## Overview
The RP Graveyard System is an automated code refactoring tool that safely moves unused, deprecated, or experimental functions from the main `r.py` module to a separate `libs/graveyard.py` file while preserving their functionality and accessibility. It was created primarily to allow AI assistants to refactor the codebase safely.

## Key Benefits
- **Safe refactoring**: All moved functions remain accessible via imports
- **Automated dependency resolution**: No manual fixes needed for function calls
- **Private function support**: Exports private functions starting with `_` 
- **Zero downtime**: Functions work exactly the same after moving
- **Clean main module**: Reduces clutter in `r.py` without breaking anything

## System Components

### 1. Marker System
Functions are marked for graveyard using comment markers:
```python
#GRAVEYARD START
def unused_function():
    return "This will be moved"
#GRAVEYARD END
```

### 2. Automated Processing Script
**Location**: `/opt/homebrew/lib/python3.10/site-packages/rp/move_to_graveyard.py`

**Key features**:
- Finds all `#GRAVEYARD START/END` pairs
- Extracts code blocks between markers
- Applies dependency qualification using AST manipulation
- Removes blocks from `r.py`
- Appends processed blocks to `libs/graveyard.py`
- Automatically generates `__all__` lists including private functions

### 3. Dependency Qualification System
The system uses `rp.qualify_imports()` to automatically convert dependencies:

**Input code**:
```python
from rp.r import *

def my_function():
    result = get_default_shell()  # Uses function from r.py
    return display_image("test.png")
```

**Output code**:
```python
import rp.r

def my_function():
    result = rp.r.get_default_shell()  # Qualified call
    return rp.r.display_image("test.png")
```

## Usage Instructions

### Step 1: Mark Functions for Graveyard
Add markers around the code you want to move:
```python
#GRAVEYARD START
def old_function():
    """This function is no longer needed"""
    return deprecated_behavior()

def related_helper():
    """Helper that's only used by old_function"""  
    return "helper"
#GRAVEYARD END
```

### Step 2: Run the Graveyard Script
```bash
cd /opt/homebrew/lib/python3.10/site-packages/rp
/opt/homebrew/opt/python@3.10/bin/python3.10 move_to_graveyard.py
```

### Step 3: Verify Results
The script will:
- Report number of blocks found and processed
- Show successful qualification of dependencies
- Update the `__all__` list in graveyard.py
- Confirm all functions remain accessible

## Technical Details

### AST-Based Processing
The system uses Python's `ast` module to:
1. **Parse code blocks**: Convert to Abstract Syntax Tree
2. **Extract exports**: Find all function, class, and variable definitions
3. **Generate `__all__`**: Create export lists including private names
4. **Preserve structure**: Maintain original code organization

### Import Strategy
Each moved code block follows this pattern:
1. **Add star import**: `from rp.r import *` at the top
2. **Apply qualification**: Convert to `import rp.r` + qualified calls
3. **Result**: Self-contained block with explicit dependencies

### Private Function Export
The system automatically includes private functions in `__all__` lists:
```python
__all__ = [
    'public_function',
    'another_function', 
    '_private_function',    # Private functions included
    '_internal_variable',   # Private variables included
]
```

### Error Handling
The system includes comprehensive error handling:
- **Syntax errors**: Graceful fallback for unparseable code
- **Missing markers**: Reports unmatched START/END pairs
- **Import failures**: Detailed error reporting with code snippets

## File Structure

### Before Moving
```
rp/
├── r.py                     # Contains unused_function()
└── libs/
    └── graveyard.py        # Empty or existing moved functions
```

### After Moving  
```
rp/
├── r.py                     # unused_function() removed
└── libs/
    └── graveyard.py        # Contains moved function with qualified deps
```

## Advanced Features

### Batch Processing
Multiple code blocks can be marked and moved in a single run:
```python
#GRAVEYARD START
def function_group_1():
    pass
#GRAVEYARD END

# Other code...

#GRAVEYARD START  
def function_group_2():
    pass
#GRAVEYARD END
```

### Automatic `__all__` Management
The system automatically:
- Scans all moved code for exportable names
- Generates sorted `__all__` lists (public names first, private last)  
- Updates the list every time the script runs
- Ensures consistent export behavior

### Dependency Chain Handling
Complex dependency chains are automatically resolved:
```python
# Original in r.py
def helper():
    return get_data()

def main_func():  
    return helper() + process_result()

# After moving - automatically qualified
def helper():
    return rp.r.get_data()

def main_func():
    return helper() + rp.r.process_result()  # Mixed local/qualified calls
```

## Example Workflow

### 1. Identify Candidates
Look for functions that are:
- Deprecated or superseded
- Experimental or debug-only
- Rarely used utilities
- Legacy compatibility functions

### 2. Mark for Moving
```python
#GRAVEYARD START
def legacy_audio_format_converter():
    """Superseded by new_audio_converter()"""
    # Complex legacy implementation
    pass

def old_image_resizer():
    """Use resize_image() instead"""
    # Old implementation
    pass
#GRAVEYARD END
```

### 3. Execute Move
```bash
/opt/homebrew/opt/python@3.10/bin/python3.10 move_to_graveyard.py
```

### 4. Verify Accessibility
```python
import rp

# Functions still work exactly the same
result = rp.legacy_audio_format_converter()  # Imported from graveyard
image = rp.old_image_resizer()              # Still accessible
```

## Integration with RP Module

### Import Hierarchy
```python
# In r.py
from rp.libs.graveyard import *  # Imports all graveyard functions

# In user code  
import rp                        # Gets everything including graveyard
result = rp.graveyard_function() # Works seamlessly
```

### Circular Import Prevention
The graveyard system prevents circular imports by:
- Using qualified imports (`import rp.r` not `from rp.r import *`)
- Processing dependencies at move-time, not runtime
- Creating self-contained code blocks

## Best Practices

### 1. Group Related Functions
Move related functions together in single graveyard blocks:
```python
#GRAVEYARD START
# Audio format conversion utilities (all deprecated)
def convert_wav_to_mp3_old():
    pass

def get_audio_bitrate_legacy():  
    pass

def normalize_audio_old():
    pass
#GRAVEYARD END
```

### 2. Document Reasoning
Include comments explaining why functions are being moved:
```python
#GRAVEYARD START
# Moved to graveyard: Superseded by new TensorFlow-based implementation
def old_ml_classifier():
    """Legacy scikit-learn implementation - use new_classifier() instead"""
    pass
#GRAVEYARD END
```

### 3. Test Before Moving
Verify functions still work after marking but before moving:
```python
# Mark with graveyard tags
#GRAVEYARD START  
def test_function():
    return "works"
#GRAVEYARD END

# Test accessibility
assert test_function() == "works"  # Should still work

# Then run move script
```

### 4. Incremental Refactoring
Move functions in small, logical groups rather than massive blocks:
- Easier to debug if issues arise
- Cleaner git history
- Safer for production systems

## Troubleshooting

### Common Issues

**1. Syntax Errors in Moved Code**
- Check for incomplete functions or missing imports
- Ensure code blocks are syntactically complete

**2. Import Loops** 
- Verify moved functions don't import from graveyard
- Check for complex circular dependencies

**3. Missing Functions After Move**
- Confirm `from rp.libs.graveyard import *` exists in r.py
- Check that function names are in graveyard's `__all__` list

**4. Qualification Failures**
- Review error messages from `qualify_imports`
- Check for unsupported Python constructs

### Debug Commands
```bash
# Test graveyard import manually
python3.10 -c "from rp.libs.graveyard import *; print(dir())"

# Check __all__ list
python3.10 -c "import rp.libs.graveyard; print(graveyard.__all__)"

# Verify specific function
python3.10 -c "import rp; print(rp.moved_function)"
```

## Performance Impact
- **Minimal runtime overhead**: Functions are imported once at startup
- **Reduced memory footprint**: Unused code moved out of main module
- **Faster import times**: Smaller main module imports faster
- **Clean namespace**: Less clutter in main module

## Future Enhancements
- **Selective imports**: Import only needed graveyard functions
- **Usage analysis**: Track which graveyard functions are actually used
- **Automatic candidate detection**: AI-powered identification of move candidates
- **Rollback capability**: Easy restoration of moved functions

---

## Quick Reference

### Mark for graveyard:
```python
#GRAVEYARD START
def function_to_move():
    pass
#GRAVEYARD END
```

### Run graveyard script:
```bash
/opt/homebrew/opt/python@3.10/bin/python3.10 move_to_graveyard.py
```

### Functions remain accessible:
```python
import rp
rp.moved_function()  # Works exactly the same
```