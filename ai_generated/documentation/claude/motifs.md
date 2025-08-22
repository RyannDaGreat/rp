# RP Design Motifs - Deep Dive

## Core Philosophy
RP embodies "Practicality beats purity" - every design decision prioritizes developer ergonomics and real-world usability over theoretical correctness.

## Discovered Motifs

### 1. Semantic Verb-Noun Naming
Functions read like natural language commands:
- `load_image()`, `save_image()`, `display_image()`
- `copy_image_to_clipboard()`, `load_image_from_clipboard()`
- `trim_videos_to_max_length()`, `crop_images_to_square()`

**Why**: Makes the API discoverable - you can often guess the function name.

### 2. Systematic Pluralization
Singular functions for single items, plural for collections:
```python
load_image(path) → single image
load_images(*paths) → list of images
with_drop_shadow(img) → single processed image  
with_drop_shadows(imgs) → list of processed images
```

Implementation typically: `return [singular_func(x) for x in items]`

### 3. Backend Selection via "_via_"
Multiple implementations with automatic selection:
```python
text_to_speech() → picks best available:
  ├── text_to_speech_via_apple()  # macOS
  ├── text_to_speech_via_google() # cross-platform
  └── text_to_speech_via_aws()    # cloud option
```

### 4. Consistent Control Parameters
Standard parameters across functions:
- `use_cache=False` - Enable caching
- `strict=True` - Error handling (True=fail, False=skip, None=return None)
- `copy=True` - Copy vs in-place modification
- `shutup=False` - Suppress output
- `show_progress=False` - Progress bars ('eta', 'tqdm', or bool)
- `num_threads=None` - Parallelization

### 5. Argument Flexibility Helpers
Helper functions enable multiple calling conventions:
```python
detuple(x) - Unwraps single-item tuples
enlist(x) - Ensures list format
entuple(x) - Ensures tuple format

# Allows both:
func(item1, item2)
func([item1, item2])
```

### 6. Graceful Error Squelching
Multiple error handling strategies:
```python
squelch_call(func, *args) - Silent failure
strict=False - Skip failures in batch operations
strict=None - Return None for failures
TemporarilySuppressConsoleOutput() - Hide warnings
```

### 7. Temporal State Management
Safe, scoped state changes:
```python
with temporary_random_seed(42):
    # Reproducible randomness here
# Original seed restored

toc = tic()  # Creates closure with timer state
elapsed = toc()  # Check elapsed time
```

### 8. Type Introspection Pipeline
Systematic type checking and conversion:
```python
is_image() → bool
as_numpy_image() → converts anything to numpy
is_float_image() → check dtype
as_float_image() → convert to float
```

### 9. Lazy Import Pattern
Heavy dependencies imported on first use:
```python
def torch_function():
    import torch  # Only imported when needed
    return torch.tensor(...)
```

### 10. Fallback Chains
Functions try multiple approaches:
```python
resize_image():
  1. Try cv_resize_image() - fast
  2. Fallback to skimage - robust
  3. Last resort: pure Python
```

### 11. Format-Driven Dispatch
File extensions determine behavior:
```python
save_video("out.mp4") → save_video_mp4()
save_video("out.gif") → save_video_gif()
load_image("file.exr") → load_openexr_image()
```

### 12. Symmetric Function Pairs
Operations come in pairs:
```python
encode_image_to_bytes() ↔ decode_image_from_bytes()
string_to_clipboard() ↔ string_from_clipboard()
text_file_to_string() ↔ string_to_text_file()
```

### 13. Varargs for Collections
Functions accept any number of arguments:
```python
get_max_image_dimensions(*images)
horizontally_concatenated_images(*images)
overlay_images(*images)
```

### 14. Smart Defaults
Defaults that "just work":
```python
gauss_blur(img, σ=None)  # σ calculated from image size
resize_image(img, scale)  # scale can be float or (w,h)
with_corner_radius(img, radius=None)  # radius from image size
```

### 15. Progressive Enhancement
Simple call → complex call:
```python
# Simple
save_image(img, "out.png")

# Enhanced
save_image(img, "out.png", quality=95, optimize=True, exif=metadata)
```

## Anti-Patterns RP Avoids

### The FFmpeg Problem
❌ Functions with dozens of conditional parameters
✅ Separate functions for separate concerns

### The NumPy Strictness
❌ Rejecting inputs that aren't the exact right type
✅ Accept anything reasonable, convert internally

### The Verbose Java
❌ ImageFileLoaderFactoryBuilder patterns
✅ Simple, direct function names

## Usage Patterns

### Batch Processing Pattern
```python
# Process multiple items maintaining order
results = [process(x) for x in items if condition(x)]
```

### Safe Exploration Pattern
```python
# Try it without consequences
with temporary_state():
    experimental_operation()
```

### Platform Independence Pattern
```python
if currently_running_mac():
    mac_specific_function()
else:
    cross_platform_fallback()
```

## For Future Claudes

### When Adding Functions
1. Follow verb-noun naming
2. Create singular and plural versions
3. Add standard control parameters
4. Provide symmetric pairs (encode/decode)
5. Use detuple() for argument flexibility

### When Debugging
1. Check for `_via_` variants
2. Look for strict parameter behavior
3. Verify fallback chains
4. Check if function uses lazy imports

### Finding Functions
1. Guess the verb-noun name
2. Try plural if working with collections
3. Look for `_via_` for specific backends
4. Check for format-specific variants (e.g., `_mp4`)

## Dependency Management Philosophy

### The pip_import Pattern (RP's Most Used Function!)
With 436+ uses throughout r.py, `pip_import()` is the cornerstone of RP's dependency strategy:

```python
def opencv_function():
    pip_import('cv2')  # Auto-installs opencv if needed
    import cv2
    # ... use cv2 ...
```

**How it works**:
1. Tries to import the module
2. If missing, checks PyPI
3. Asks user permission to install (auto-yes in Colab)
4. Installs and imports on demand

This means users only install dependencies for functions they actually use!

### Strategic Vendoring (Not Everything!)
RP only vendors libraries that have caused problems:
- **rp_ptpython, prompt_toolkit** - Vendored due to breaking API changes
- **Terminal image viewer** - Forked and modified with CFFI for C-speed
- **jedi, parso** - Lightly vendored for version stability

Stable libraries stay external:
- **pygments** - Never had breaking changes, stays external
- **PIL, cv2, torch** - Handled via pip_import

**Philosophy**: Vendor only when there's historical pain, otherwise use pip_import

### Ultra-Fast Import (22ms for 513K lines!)

Despite containing 513K+ lines of code, RP imports in ~22ms:
- **RP**: ~22ms
- **NumPy**: ~207ms (10x slower)
- **Pandas**: ~771ms (35x slower)

**How**:
- Only 22 top-level imports (lightweight core)
- 458+ lazy imports inside functions (load on demand)
- Vendored libs avoid pip resolution overhead
- Smart code organization despite 53,000+ line main file

**Pattern**:
```python
def torch_function():
    import torch  # Only imported when torch_function() is called
    return torch.tensor(...)
```

This "batteries AND factory included" philosophy means RP ships as a monolithic, self-sufficient module that's still blazing fast to import.

## Living Document
This document captures patterns discovered through deep analysis. Update when new patterns emerge or existing ones evolve.