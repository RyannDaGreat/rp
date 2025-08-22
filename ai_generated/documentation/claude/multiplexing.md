# RP Multiplexing Pattern Documentation

## Overview
RP uses a multiplexing pattern where base functions with minimal arguments dispatch to implementation variants (`_via_` functions) that have extended, backend-specific arguments. This avoids the "ffmpeg problem" where functions have dozens of conditional parameters.

## Core Principle: No Useless Args
Every argument in a function signature must be usable. Base functions only include arguments that work across ALL implementations. Backend-specific arguments belong in the specific implementation functions.

## Multiplexing Patterns

### 1. File Extension-Based Multiplexing

**Example: `save_video()`**
```python
save_video(images, path, framerate=60)
  ├── path.endswith('.mp4')  → save_video_mp4(images, path, framerate, video_bitrate='high', height, width, show_progress, backend)
  ├── path.endswith('.avi')  → save_video_avi(images, path, framerate)
  ├── path.endswith('.gif')  → save_video_gif(images, path, framerate)
  └── path.endswith('.webp') → save_video_webp(images, path, framerate)
```

The base function has ONLY common args (framerate). Format-specific args like `video_bitrate` only exist in `save_video_mp4`.

### 2. Backend-Based Multiplexing

**Example: `copy_image_to_clipboard()`**
```python
copy_image_to_clipboard(image, backend=None)
  ├── backend='copykitten'     → _copy_image_to_clipboard_via_copykitten(image)  # Supports RGBA
  └── backend='pyjpgclipboard' → _copy_image_to_clipboard_via_pyjpgclipboard(image)  # RGB only
```

**Example: `resize_image()`**
```python
resize_image(image, scale, interp='bilinear')
  ├── Try: cv_resize_image(image, scale, interp)  # Fast OpenCV
  ├── Fallback: _resize_image_via_skimage(image, scale, interp)  # Slower but more robust
  └── Last resort: grid2d(...)  # Pure Python
```

### 3. Input-Type Multiplexing

**Example: `load_image()`**
```python
load_image(location, use_cache=False)
  ├── is_valid_url(location) → load_image_from_url(location)
  └── else                    → load_image_from_file(location)
```

**Example: `load_image_from_file()`**
```python
load_image_from_file(file_name)
  ├── .exr  → load_openexr_image(file_name)
  ├── .HEIC → _load_image_from_file_via_PIL(file_name)
  ├── Try: _load_image_from_file_via_imageio(file_name)
  ├── Try: _load_image_from_file_via_scipy(file_name)
  ├── Try: _load_image_from_file_via_opencv(file_name)
  └── Try: _load_image_from_file_via_PIL(file_name)
```

## Key Design Principles

1. **Base function = Simple API**: Minimal args that work everywhere
2. **Specific function = Advanced API**: Extended args for power users
3. **Graceful fallbacks**: Try multiple implementations in order
4. **File extensions determine path**: `.mp4` → `save_video_mp4()`
5. **No conditional parameters**: Unlike ffmpeg's dozens of maybe-used args

## Usage Examples

### Simple Usage (Base Function)
```python
# User doesn't care about backend details
save_video(frames, "output.mp4")  # Uses defaults
resize_image(img, 0.5)  # Uses fastest available
```

### Advanced Usage (Specific Function)
```python
# User needs specific features
save_video_mp4(frames, "output.mp4", video_bitrate='10M', backend='moviepy')
cv_resize_image(img, 0.5, interp='lanczos')  # Force OpenCV with specific interpolation
```

## Benefits

- **Clean API**: Simple functions for simple cases
- **Power when needed**: Advanced functions for advanced cases  
- **No parameter bloat**: Functions don't carry unused baggage
- **Clear expectations**: Args in signature are always usable
- **Performance optimization**: Can try fast path first, fall back if needed

## Implementation Variants Naming

- `_via_[backend]`: Private implementation variant (e.g., `_resize_image_via_skimage`)
- `[backend]_[function]`: Public backend-specific function (e.g., `cv_resize_image`, `torch_resize_image`)
- `[function]_[format]`: Format-specific function (e.g., `save_video_mp4`, `load_openexr_image`)

## Anti-Pattern: The FFmpeg Problem

What RP avoids:
```python
# BAD: Dozens of parameters, most unused depending on format
save_video(images, path, framerate=60, video_bitrate=None, audio_bitrate=None, 
           codec=None, pixel_format=None, crf=None, preset=None, tune=None,
           x264_params=None, aac_params=None, ...)  # 50+ more conditional params
```

What RP does instead:
```python
# GOOD: Base has universal params
save_video(images, path, framerate=60)

# GOOD: Specific functions have specific params  
save_video_mp4(images, path, framerate=60, video_bitrate='high', backend='moviepy')
save_video_webm(images, path, framerate=60, quality=0.8, lossless=False)
```

## Finding Multiplexing Functions

Look for:
- Functions ending with `_via_*`
- Format-specific functions (`save_*_mp4`, `load_*_from_url`)
- Functions with backend parameters
- Try/except chains attempting multiple implementations