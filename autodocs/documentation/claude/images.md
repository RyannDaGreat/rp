# RP Image System Documentation

## Overview
RP's image system provides ~285+ functions for image processing with a flexible philosophy: **"Accept anything, return what makes sense"**. Functions automatically handle conversions between formats, letting users focus on operations rather than type management.

## Image Representations

### 1. NumPy Arrays (Primary Format)
- **Grayscale**: 2D array, shape (H, W)
- **RGB**: 3D array, shape (H, W, 3)
- **RGBA**: 3D array, shape (H, W, 4)
- **Data types**: 
  - `float32/64`: Values 0.0-1.0
  - `uint8`: Values 0-255
  - `bool`: Binary images

### 2. PIL Images
- Fixed modes: 'L', 'RGB', 'RGBA', '1', 'F', etc.
- Limited dtype support (no true bool)
- Automatically converted to NumPy for processing
- Accepted by `is_image()` but not equivalent to NumPy

### 3. Torch Tensors
- CHW format (Channels, Height, Width)
- Separate validation: `is_torch_image()`
- Parallel functions: `torch_resize_image`, etc.
- NOT accepted by `is_image()`

### 4. Videos
- Just sequences of images with time dimension
- NumPy: THWC format
- Torch: TCHW format

## Core Functions

### Type Checking
```python
is_image(x)          # NumPy/PIL only
is_torch_image(x)    # Torch tensors only
is_grayscale_image(x)  # 2D arrays
is_rgb_image(x)      # HW3 arrays
is_rgba_image(x)     # HW4 arrays
is_float_image(x)    # float dtype
is_byte_image(x)     # uint8 dtype
is_binary_image(x)   # bool dtype
```

### Type Conversion
```python
as_numpy_image(x)    # Convert to NumPy
as_pil_image(x)      # Convert to PIL
as_torch_image(x)    # Convert to Torch
as_grayscale_image(x)  # Convert to grayscale
as_rgb_image(x)      # Convert to RGB
as_rgba_image(x)     # Convert to RGBA
as_float_image(x)    # Convert to float (0-1)
as_byte_image(x)     # Convert to uint8 (0-255)
as_binary_image(x)   # Convert to bool
```

### Loading & Saving
```python
load_image(path)     # Load from file/URL
save_image(img, path)  # Save to file
load_images(*paths)  # Batch load
save_images(imgs)    # Batch save
load_image_from_clipboard()
copy_image_to_clipboard(img)
```

### Display
```python
display_image(img)   # Show image
display_alpha_image(img)  # With checkerboard
display_image_in_terminal(img)
display_image_in_notebook(img)
```

### Transformations
```python
resize_image(img, scale)
rotate_image(img, angle)
crop_image(img, height, width)
shift_image(img, dx, dy)
horizontally_flipped_image(img)
vertically_flipped_image(img)
```

### Effects & Filters
```python
gauss_blur(img, σ)
with_corner_radius(img, radius)
with_image_glow(img, blur, strength)
with_alpha_outline(img, radius, color)
inverted_image(img)
```

### Blending & Composition
```python
blend_images(bottom, top, alpha, mode)
overlay_images(*images)
horizontally_concatenated_images(*imgs)
vertically_concatenated_images(*imgs)
grid_concatenated_images(imgs, cols)
```

### Encoding & Decoding
```python
# Images ↔ Bytes
encode_image_to_bytes(img) ↔ decode_bytes_to_image(bytes)
encode_images_to_bytes(imgs) ↔ decode_images_from_bytes(bytes)

# Images ↔ Base64
encode_image_to_base64(img) ↔ decode_image_from_base64(b64)
encode_images_to_base64(imgs) ↔ decode_images_from_base64(b64s)

# Videos ↔ Bytes
encode_video_to_bytes(vid) ↔ decode_video_from_bytes(bytes)
```

## Conversion Philosophy

### Input Flexibility
- Functions accept ANY reasonable image type
- Automatic conversion via `is_*` and `as_*` functions
- Example: `gauss_blur(pil_image)` works fine

### Output Variability
- Functions return whatever type makes sense
- Input type doesn't determine output type
- Example: `resize_image(bool_array)` might return float

### User Responsibility
- Functions give you what they give you
- Use `as_*` functions to convert to desired type
- Example: `as_byte_image(gauss_blur(img))`

## Batch Operations
Most functions have plural versions for batch processing:
- `resize_image` → `resize_images`
- `crop_image` → `crop_images`
- `rotate_image` → `rotate_images`
- `inverted_image` → `inverted_images`

## Special Features

### Multiple Backends
- OpenCV: `cv_resize_image`
- PyTorch: `torch_resize_image`
- Skia: `skia_resize_image`
- PIL: Default for many operations

### Image Sources
Functions that load images from various sources (all return NumPy):
- `load_image_from_url()`
- `load_image_from_webcam()`
- `load_image_from_screenshot()`
- `load_pdf_as_images()`
- `load_image_from_matplotlib()`

### Exotic Formats
- OpenEXR: `load_openexr_image`, `save_openexr_image`
- WebP: `save_image_webp`
- AVIF: `save_image_avif`
- JXL: `save_image_jxl`

## Common Patterns

### Load, Process, Save
```python
img = load_image('input.jpg')
img = resize_image(img, 0.5)
img = gauss_blur(img, 2.0)
save_image(img, 'output.png')
```

### Type Conversion Chain
```python
img = load_image('photo.png')     # Returns NumPy
img = as_float_image(img)         # Convert to float
img = inverted_image(img)         # Process
img = as_byte_image(img)          # Convert back
```

### Batch Processing
```python
images = load_images('*.jpg')
images = resize_images(images, (128, 128))
save_images(images, paths)
```

## Function Aliases
Many functions have multiple names for convenience:
- `inverted_image` = `invert_image`
- `decode_bytes_to_image` = `decode_image_from_bytes`
- `decode_bytes_to_video` = `decode_video_from_bytes`

## Key Insights

1. **NumPy is the lingua franca** - Everything converts to/from NumPy
2. **Automatic type handling** - Functions handle conversions internally
3. **Flexible I/O** - Accept anything, return what's practical
4. **Batch-first design** - Most operations have batch versions
5. **Multiple backends** - Choose performance vs. features

## Quick Reference

### Check image type
```python
is_image(x)         # Is it a valid image?
is_grayscale_image(x)  # Is it grayscale?
is_float_image(x)   # Is it float dtype?
```

### Convert image type
```python
as_rgb_image(x)     # Make it RGB
as_float_image(x)   # Make it float
as_numpy_image(x)   # Make it NumPy
```

### Basic operations
```python
load_image(path)
save_image(img, path)
display_image(img)
resize_image(img, scale)
```