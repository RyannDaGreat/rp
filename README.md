# RP (Ryan's Python) 🐍

[Written with AI]

**The comprehensive Python utility library that just works**

[![PyPI version](https://badge.fury.io/py/rp.svg)](https://badge.fury.io/py/rp)
[![Python Support](https://img.shields.io/badge/python-3.6+-blue.svg)](https://pypi.org/project/rp/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

RP is a massive, self-contained Python utility library with 1600+ functions covering everything from image processing to web scraping, audio manipulation to machine learning tools. It's designed with a "batteries AND factory included" philosophy - install once, use everything.

## ⚡ Quick Start

```bash
pip install rp
```

```python
# Import everything (recommended)
from rp.r import *

# Or import the module
import rp

# Load and process an image
img = load_image("photo.jpg")  # Works with files or URLs
img = resize_image(img, 0.5)   # Resize to 50%
img = gauss_blur(img, 2.0)     # Apply blur
save_image(img, "output.png")  # Save result
display_image(img)             # Show in preview
```

## ✨ Key Features

- **🚀 Ultra-fast import**: ~22ms for 500K+ lines (10x faster than NumPy)
- **📦 Self-contained**: All dependencies included - no version conflicts
- **🔄 Accept anything**: Functions automatically handle type conversions
- **⚙️ Smart defaults**: Sensible parameters that "just work"
- **🔀 Multiple backends**: Choose performance vs features (OpenCV, PIL, PyTorch, etc.)
- **📊 Batch operations**: Process multiple items efficiently
- **🧠 Zero configuration**: No setup required, works out of the box

## 🎯 What Can You Do?

### 🖼️ Image Processing (285+ functions)
```python
# Load from anywhere
img = load_image("https://example.com/photo.jpg")
img = load_image_from_clipboard()

# Transform and enhance
img = resize_image(img, (800, 600))
img = with_corner_radius(img, 20)
img = with_drop_shadow(img)

# Batch processing
images = load_images("*.jpg")
resized = resize_images(images, 0.5)
save_images(resized, "thumbnails/")
```

### 🗂️ File & System Operations
```python
# Smart file handling
files = get_all_files("*.py", recursive=True)
text = load_text_file("document.txt")
save_json(data, "output.json")

# Clipboard integration
string_to_clipboard("Hello World")
text = string_from_clipboard()
copy_image_to_clipboard(img)
```

### 🎵 Audio & Video Processing
```python
# Audio operations
audio = load_audio("song.mp3")
save_audio(audio, "converted.wav")
text_to_speech("Hello world", voice="Karen")

# Video creation
frames = load_images("frame_*.png")
save_video(frames, "animation.mp4", framerate=30)
```

### 🌐 Web & Network
```python
# Easy web requests
html = get_url("https://api.example.com")
data = get_json("https://api.example.com/data")
download_file("https://example.com/file.zip", "local.zip")

# Web scraping helpers
links = extract_links_from_html(html)
images = extract_images_from_html(html)
```

### 🎲 Random & Math Utilities
```python
# Smart random functions
color = random_rgb_color()
sample = random_batch([1,2,3,4,5], 3)
if random_chance(0.7):  # 70% probability
    print("Lucky!")

# Math helpers
result = clamp(value, 0, 100)
normalized = normalize_list([1, 2, 3, 4, 5])
```

### 💻 Terminal & System
```python
# Platform detection
if currently_running_mac():
    mac_specific_code()

# Terminal utilities
with TemporarilySuppressConsoleOutput():
    noisy_function()  # Output hidden

# Timing utilities
timer = tic()
# ... do work ...
elapsed = toc()  # Get elapsed time
```

## 🏗️ Core Design Principles

### Accept Anything Philosophy
Functions automatically handle different input types:
```python
# All of these work:
img = resize_image(numpy_array, 0.5)
img = resize_image(pil_image, 0.5) 
img = resize_image(torch_tensor, 0.5)

# Output is always what makes most sense
img = as_numpy_image(img)  # Ensure NumPy format
```

### Semantic Naming
Function names read like natural language:
```python
load_image(), save_image(), display_image()
copy_image_to_clipboard(), load_image_from_clipboard()
horizontally_concatenated_images()
vertically_flipped_image()
```

### Smart Pluralization
Batch operations are intuitive:
```python
# Single
img = load_image("photo.jpg")

# Multiple  
imgs = load_images("photo1.jpg", "photo2.jpg", "photo3.jpg")
imgs = load_images("*.jpg")  # Glob patterns work too
```

### Multiple Backends
Choose the best tool for the job:
```python
# Automatic selection
img = resize_image(img, 0.5)  # Uses fastest available

# Specific backend
img = cv_resize_image(img, 0.5)      # Force OpenCV
img = torch_resize_image(img, 0.5)   # Force PyTorch
img = skia_resize_image(img, 0.5)    # Force Skia
```

## 📊 By The Numbers

- **59,451 lines** in main module
- **1,600+ functions** covering every common task
- **285+ image functions** with flexible type handling
- **~22ms import time** despite massive functionality
- **500K+ total lines** including vendored dependencies
- **Zero breaking changes** - backward compatibility guaranteed

## 🚀 Why RP Imports So Fast

Despite being huge (500K+ lines), RP imports in just ~22ms through:

1. **Lazy imports**: Heavy dependencies only loaded when needed
2. **Smart vendoring**: Only problematic libraries are included
3. **On-demand installation**: `pip_import()` installs packages only when used
4. **Minimal startup**: Just 22 essential imports at startup

```python
# This function only imports OpenCV when called
def opencv_function():
    pip_import('opencv-python')  # Auto-installs if needed
    import cv2
    return cv2.some_operation()
```

## 📖 Function Categories

| Category | Examples | Count |
|----------|----------|-------|
| **Images** | `load_image`, `resize_image`, `gauss_blur` | 285+ |
| **Files** | `load_text_file`, `get_all_files`, `save_json` | 200+ |
| **Audio** | `load_audio`, `text_to_speech`, `save_audio` | 50+ |
| **Video** | `save_video`, `load_video`, `extract_frames` | 30+ |
| **Web** | `get_url`, `download_file`, `extract_links` | 100+ |
| **Random** | `random_choice`, `random_color`, `random_batch` | 40+ |
| **Math** | `clamp`, `normalize`, `interpolate` | 80+ |
| **System** | `platform detection`, `clipboard`, `terminal` | 60+ |
| **ML/AI** | Various machine learning utilities | 100+ |

## 🛠️ Advanced Usage

### Error Handling
```python
# Strict mode (default) - raises on error  
imgs = load_images("*.jpg", strict=True)

# Lenient mode - skips bad files
imgs = load_images("*.jpg", strict=False)

# None mode - includes None for failures
imgs = load_images("*.jpg", strict=None)
```

### Progress Bars
```python
# Built-in progress tracking
imgs = load_images(many_paths, show_progress=True)
results = process_batch(data, show_progress='tqdm')
```

### Caching
```python
# Enable caching for expensive operations
result = expensive_function(data, use_cache=True)
```

### Temporary State
```python
# Safe state management
with temporary_random_seed(42):
    # Reproducible randomness
    value = random_float()
# Original seed restored

with TemporarilySetAttr(obj, 'attr', new_value):
    # obj.attr temporarily changed
# Original value restored
```

## 🤝 Contributing

RP follows consistent patterns:

1. **Semantic naming**: `verb_noun()` format
2. **Type flexibility**: Accept multiple input types
3. **Pluralization**: Create batch versions of functions
4. **Standard parameters**: `strict`, `use_cache`, `show_progress`
5. **Backend variants**: Provide `_via_` implementations

## 📜 License

MIT License - Use it however you want!

## 🎉 Why Choose RP?

- **Everything in one place**: No hunting for the right library
- **Consistent API**: Learn once, use everywhere  
- **Battle-tested**: Used in production for years
- **Zero dependencies**: No pip hell or version conflicts
- **Lightning fast**: Optimized for real-world usage
- **Just works**: Sensible defaults for everything

Install RP once, never pip install again. Welcome to Python productivity nirvana! 🚀

---

*Made with ❤️ for Python developers who want to focus on building, not configuring.*
