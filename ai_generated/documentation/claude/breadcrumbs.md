# RP Navigation Breadcrumbs - For Future Claudes

## Quick Start
When you first encounter RP, know that:
1. **Everything is in r.py** - 53,000+ lines, 1625+ functions
2. **Import with**: `from rp.r import *` or `import rp`
3. **Accept anything philosophy** - Functions convert inputs automatically
4. **Check documentation/claude/** - Previous Claudes left guides here

## Finding Functions

### Strategy 1: Guess the Name
RP uses semantic verb-noun naming:
- Want to load an image? → `load_image()`
- Want to save multiple images? → `save_images()`
- Want to blur something? → `gauss_blur()`
- Want clipboard access? → `string_to_clipboard()`, `string_from_clipboard()`

### Strategy 2: Search by Pattern
Common prefixes:
- `load_*` - Loading data from files/URLs/clipboard
- `save_*` - Saving data to files
- `display_*` - Showing things on screen
- `get_*` - Retrieving values
- `set_*` - Setting values
- `is_*` - Boolean checks (is_image, is_url, is_float_image)
- `as_*` - Type conversions (as_numpy_image, as_float_image)
- `random_*` - Random generation (random_rgb_color, random_batch)
- `with_*` - Adding effects (with_corner_radius, with_drop_shadow)

### Strategy 3: Check Plurals
Most functions have singular/plural versions:
- `resize_image()` / `resize_images()`
- `load_image()` / `load_images()`
- `random_color()` / `random_colors()`

### Strategy 4: Look for Backend Variants
If a function could have multiple implementations:
- Base: `text_to_speech()`
- Variants: `text_to_speech_via_apple()`, `text_to_speech_via_google()`

## Common Operations Quick Reference

### Images
```python
# Load/Save
img = load_image("file.jpg")  # or URL
save_image(img, "output.png")

# Display
display_image(img)  # Opens preview
display_alpha_image(img)  # With checkerboard

# Transform
img = resize_image(img, 0.5)  # Scale by 50%
img = rotate_image(img, 45)  # Rotate 45 degrees
img = gauss_blur(img, sigma=2.0)

# Type conversion
img = as_float_image(img)  # Convert to 0-1 range
img = as_byte_image(img)  # Convert to 0-255
img = as_rgb_image(img)  # Ensure RGB
```

### Files & Paths
```python
# Current directory
set_current_directory("path/to/dir")  # Change directory
get_current_directory()  # Get current directory
get_all_files(".")  # List files

# File operations
files = get_all_files("*.py")  # Get files by pattern
text = load_text_file("file.txt")
save_text_file(text, "output.txt")
```

### Clipboard
```python
string_to_clipboard("text")
text = string_from_clipboard()
copy_image_to_clipboard(img)
img = load_image_from_clipboard()
```

### Random Generation
```python
random_choice("a", "b", "c")  # Pick one
random_batch([1,2,3,4,5], 3)  # Random sample
random_rgb_byte_color()  # Random color
random_float()  # 0-1 float
random_chance(0.7)  # 70% chance of True
```

## Platform Detection
```python
if currently_running_mac():
    # Mac-specific code
elif currently_running_linux():
    # Linux-specific code
elif currently_running_windows():
    # Windows-specific code
```

## Error Handling Patterns

### Strict Parameter
Many functions accept `strict`:
- `strict=True` - Raise exceptions (default)
- `strict=False` - Skip failures in batch operations
- `strict=None` - Return None for failures

```python
images = load_images("*.jpg", strict=False)  # Skip bad files
images = load_images("*.jpg", strict=None)  # Include None for bad files
```

### Squelching
```python
result = squelch_call(risky_function, arg1, arg2)  # Returns None on error
with TemporarilySuppressConsoleOutput():
    noisy_function()  # Output suppressed
```

## State Management

### Temporary Seeds
```python
with temporary_random_seed(42):
    # Reproducible randomness
    value = random_float()
# Original seed restored
```

### Timing
```python
toc = tic()  # Start timer
# ... do work ...
elapsed = toc()  # Get elapsed time
```

## Type Checking & Conversion

### The is_*/as_* Pattern
```python
if is_image(data):
    data = as_numpy_image(data)  # Ensure numpy format
    if is_float_image(data):
        data = as_byte_image(data)  # Convert to uint8
```

### Common Type Checks
```python
is_valid_url(string)  # Valid URL?
is_image_file(path)  # Image file extension?
is_video_file(path)  # Video file extension?
is_numpy_array(obj)  # NumPy array?
is_torch_tensor(obj)  # PyTorch tensor?
```

## Batch Processing

### Using Plurals
```python
# Process multiple items
images = load_images("img1.jpg", "img2.jpg", "img3.jpg")
resized = resize_images(images, 0.5)
save_images(resized, ["out1.jpg", "out2.jpg", "out3.jpg"])
```

### Parallel Processing
```python
results = load_images(paths, num_threads=8)  # Parallel loading
```

## Hidden Gems

### Data Structure Manipulation
```python
detuple((x,))  # Unwrap single-item tuple → x
enlist(x)  # Ensure list: x → [x]
```

### Progress Bars
```python
load_images(many_paths, show_progress=True)  # Shows progress
load_images(many_paths, show_progress='tqdm')  # Specific style
```

### Context Managers
```python
with TemporarilySetAttr(obj, 'attr', new_value):
    # obj.attr temporarily has new_value
# Original value restored

with TemporarilyDownloadUrl(url) as local_path:
    # URL downloaded to temp file
# Temp file cleaned up
```

## Common Gotchas

1. **Images can be numpy, PIL, or torch** - Use `as_numpy_image()` to standardize
2. **Private functions are often exported** - Don't assume `_function` is private
3. **Functions may have aliases** - `invert_image` = `inverted_image`
4. **Check for _via_ variants** - Might be faster/better implementation
5. **Many functions lazy-import** - First call may be slower

## Debugging RP Functions

### Find Source
```python
import inspect
print(inspect.getsource(function_name))
```

### Check Aliases
Look for assignments like:
```python
inverted_image = invert_image  # Alias
```

### Find Related Functions
```python
# In Python
[f for f in dir(rp) if 'image' in f]  # All image functions
```

## Performance Tips

1. **Use cv_ or torch_ variants** - Often faster than default
2. **Batch operations** - Use plural functions, not loops
3. **Enable caching** - `use_cache=True` for repeated operations
4. **Check for compiled versions** - Some functions have Numba variants

## Why RP Imports So Fast

Despite being 513K+ lines with vendored libraries, RP imports in ~22ms because:
1. **Lazy imports everywhere** - Heavy deps only loaded when needed
2. **Minimal top-level imports** - Just 22 essentials at startup
3. **458+ function-level imports** - Deferred until function is called
4. **pip_import pattern** - External deps only installed when actually used

The Magic: `pip_import()`
```python
def some_function():
    pip_import('opencv-python')  # Only installs if you call this function!
    import cv2
    # ... use cv2 ...
```

With 436+ pip_import calls, RP doesn't force you to install everything - just what you need!

Example of lazy import pattern:
```python
def torch_resize_image(img):
    import torch  # Only imported if this function is called
    # ... torch operations ...
```

This is 10x faster than NumPy (207ms) and 35x faster than Pandas (771ms)!

## When Contributing

### Adding New Functions
1. Follow verb-noun naming
2. Create singular and plural versions
3. Accept multiple input types via `is_*/as_*`
4. Add standard parameters (strict, use_cache, show_progress)
5. Use `detuple()` for flexible arguments
6. Consider adding `_via_` variants

### Moving to Graveyard
1. Mark with `#GRAVEYARD START` and `#GRAVEYARD END`
2. Run `move_to_graveyard.py`
3. Functions remain accessible via imports

## Key Files for Contributors

If you plan on contributing to or analyzing `rp`, these files are important:
- **r.py**: The main module where most functions reside.
- **documentation/claude/**: Guides for developers and AI assistants.
- **`move_to_graveyard.py` & `libs/graveyard.py`**: These are part of an internal, automated refactoring system. End-users do not need to interact with them, but contributors may.
- **qualify_imports.py**: A utility for AST-based import refactoring.

## Final Tips

1. **When in doubt, search r.py** - Everything is there
2. **Try the obvious name first** - It probably exists
3. **Check for plural version** - Batch operations are common
4. **Look for _via_ variants** - Different implementations available
5. **Read the docstrings** - Many functions have helpful docs
6. **Use the accept-anything philosophy** - Pass any reasonable input

---

*Left by Claude on 2025-08-07 for future Claudes exploring RP*