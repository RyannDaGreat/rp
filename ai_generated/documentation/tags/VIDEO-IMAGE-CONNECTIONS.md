# VIDEO-IMAGE CONNECTIONS: How RP Bridges Video and Image Processing

*Mapping the concrete relationships between video and image functions in RP*

---

## Core Philosophy: Videos as Sequences of Images

RP treats videos fundamentally as **temporal sequences of images**. This creates a natural bridge where:
- Image operations can be applied to individual video frames
- Batch image operations power video processing 
- Video functions internally delegate to image functions
- Format conversions work seamlessly between domains

---

## 1. DIRECT VIDEO → IMAGE DELEGATION PATTERNS

### Resize Operations
```python
# Video functions call image functions internally
def resize_videos(*videos, size, interp="auto", ...):
    # Core pattern: video function calls resize_images for each video
    output = (
        resize_images(          # ← Image batch function
            video,
            size=size,
            interp=interp,
            ...
        )
        for video in videos
    )
```

**Key Discovery**: `resize_videos()` directly calls `resize_images()` for each video, which in turn applies `resize_image()` to each frame.

### Crop Operations  
```python
def crop_videos(videos, height=None, width=None, origin='top left', ...):
    # Delegates to crop_images for each video
    output = (crop_images(video, height=height, width=width, origin=origin, lazy=lazy_frames) 
              for video in videos)
```

**Pattern**: Video processing functions are thin wrappers that apply batch image operations.

---

## 2. HIERARCHICAL OPERATION STRUCTURE

### The Delegation Chain
```
resize_videos()    # Video plural (multiple videos)
    ↓
resize_images()    # Image plural (frames within each video) 
    ↓
resize_image()     # Image singular (individual frame)
    ↓
cv_resize_image() or _resize_image_via_skimage()  # Implementation backends
```

### Crop Chain Example
```
crop_videos_to_max_size()          # Video batch with size calculation
    ↓
crop_videos()                      # Video batch processing
    ↓  
crop_images()                      # Image batch (frames)
    ↓
crop_image()                       # Single frame processing
```

---

## 3. FORMAT CONVERSION PATTERNS

### Universal Conversion Functions
RP provides format converters that work on both images and videos:

```python
# These work on both single images and video frame sequences
as_numpy_images(images)     # Converts list of images OR video frames
as_rgb_images(images)       # Color space conversion for images/frames
as_byte_images(images)      # Data type conversion
as_pil_images(images)       # Format conversion

# Video-specific conversions that leverage image converters
as_numpy_videos(videos)     # BTCHW → BTHWC for batched videos
as_torch_videos(videos)     # Video tensors with proper dimensions
```

### Key Pattern: `_images_conversion()` Helper
```python
def _images_conversion(func, images, *, copy_check, copy=True):
    """
    Private helper that powers all plural image converters.
    Used by video functions to convert frame sequences efficiently.
    
    Optimizations:
    - Avoids unnecessary copying for numpy arrays
    - Batch type checking with copy_check predicates
    - Works on video frame sequences seamlessly
    """
```

---

## 4. LOAD/SAVE MULTIPLEXING

### Loading Architecture
```python
# Images: Single format, multiple sources  
load_image(location)           # File or URL auto-detection
load_images(*locations)        # Batch loading with threading

# Videos: Temporal dimension adds complexity
load_video_stream(path)        # Generator - memory efficient
load_video(path)              # Full load - returns numpy array
load_videos(*paths)           # Batch video loading
```

**Key Difference**: Video loading has stream vs. full variants due to memory considerations.

### Saving Multiplexing by Extension
```python
def save_video(images, path, *, framerate=60):
    """
    Extension-based multiplexing to format-specific functions.
    Note: 'images' parameter name shows video-as-image-sequence philosophy.
    """
    if path.endswith('.mp4') : return save_video_mp4(images, path, framerate=framerate)
    if path.endswith('.avi') : return save_video_avi(images, path, framerate=framerate)  
    if path.endswith('.gif') : return save_video_gif(images, path, framerate=framerate)
    if path.endswith('.png') : return save_video_png(images, path, framerate=framerate)  # Animated PNG
    if path.endswith('.webp'): return save_video_webp(images, path, framerate=framerate)
```

### Format Bridges
```python
# Some video formats are actually animated image formats
save_video_gif = save_animated_gif_via_pil    # GIF is animated image format
save_video_png = save_animated_png            # APNG (animated PNG)  
save_video_webp = save_animated_webp          # Animated WebP
```

---

## 5. CONCRETE FUNCTION RELATIONSHIPS

### Resize Family
| Function | Domain | Calls | Purpose |
|----------|--------|-------|---------|
| `resize_image()` | Single image | `cv_resize_image()` or `_resize_image_via_skimage()` | Base operation |
| `resize_images()` | Image batch | `resize_image()` on each | Frame-by-frame processing |
| `resize_videos()` | Video batch | `resize_images()` on each video | Video-level batch |
| `resize_videos_to_fit()` | Video batch + sizing | `resize_videos()` | Adds dimension calculation |

### Crop Family  
| Function | Domain | Calls | Purpose |
|----------|--------|-------|---------|
| `crop_image()` | Single image | Direct implementation | Base cropping |
| `crop_images()` | Image batch | `crop_image()` on each | Frame batch |  
| `crop_videos()` | Video batch | `crop_images()` on each video | Video batch |
| `crop_videos_to_max_size()` | Video batch + sizing | `crop_videos()` | Adds size calculation |

### Format Conversion Chain
| Function | Domain | Calls | Purpose |
|----------|--------|-------|---------|
| `as_rgb_image()` | Single image | Direct conversion | Base conversion |
| `as_rgb_images()` | Image batch | `_images_conversion(as_rgb_image, ...)` | Optimized batch |
| Video processing | Video frames | `as_rgb_images()` on frame sequence | Inherits batch optimization |

---

## 6. BRIDGING FUNCTIONS: VIDEO ↔ IMAGE

### Video Thumbnail Generation
```python
def get_youtube_video_thumbnail(url_or_id, *, use_cache=False, output='image'):
    """
    Bridge function: Video metadata → Image loading
    
    1. Extract thumbnail URL from video metadata
    2. Use load_image() to fetch thumbnail  
    3. Return as image for image processing pipeline
    """
    thumbnail_url = _get_youtube_video_data_via_embeddify(video_url)['thumbnail_url']
    thumbnail_image = load_image(thumbnail_url, use_cache=use_cache)  # ← Image function
    return thumbnail_image
```

### Frame Extraction Pattern
Videos are treated as frame sequences that can be processed like image batches:

```python
# Common pattern in RP functions
for frame in load_video_stream(path):
    processed_frame = some_image_function(frame)  # Any image operation works
    
# Or using batch operations  
video_frames = load_video(path)                   # Shape: (T, H, W, C) 
processed_frames = some_images_function(video_frames)  # Batch image operation
```

---

## 7. PERFORMANCE PATTERNS

### Lazy Evaluation for Videos
```python
def resize_videos(*videos, lazy=False, lazy_frames=False, ...):
    """
    Two-tier lazy evaluation:
    - lazy=True: Don't process videos until accessed
    - lazy_frames=True: Don't process frames within each video until accessed
    """
    output = (
        resize_images(video, ..., lazy=lazy_frames)  # Frame-level laziness
        for video in videos
    )
    if not lazy:
        output = list(output)  # Force video-level evaluation
    return output
```

### Memory Optimization
```python
# Stream processing for large videos
for frame in load_video_stream(path):  # Generator - low memory
    processed = resize_image(frame, scale)
    # Process one frame at a time instead of loading entire video

# vs. batch processing for smaller videos  
video = load_video(path)               # Full load - higher memory
processed_video = resize_images(video, scale)  # Batch operation - faster
```

---

## 8. CODEC/FORMAT RELATIONSHIPS

### Image Formats → Video Codecs
| Image Format | Video Equivalent | Function Bridge |
|-------------|------------------|-----------------|
| PNG | Animated PNG (APNG) | `save_video_png = save_animated_png` |
| WebP | Animated WebP | `save_video_webp = save_animated_webp` |
| GIF | GIF Animation | `save_video_gif = save_animated_gif_via_pil` |
| JPEG | MP4 (H.264) | `save_video_mp4()` with frame compression |
| Generic | AVI | `save_video_avi()` with OpenCV backend |

### Format Detection Pattern
```python
def save_video(images, path, **kwargs):
    """
    File extension determines codec, similar to save_image() pattern:
    - .mp4 → H.264 video encoding  
    - .avi → OpenCV video encoding
    - .gif → PIL animated GIF
    - .png → Animated PNG sequence
    - .webp → Animated WebP
    """
```

---

## 9. BATCH PATTERNS: IMAGES vs VIDEOS

### Singular → Plural → Video Pattern
```
operation_image()     # Single image
    ↓
operation_images()    # Multiple images (batch)  
    ↓
operation_videos()    # Multiple videos (each video is image batch)
```

### Example: Resize Ecosystem
```python
resize_image(img, scale)                    # Base operation
resize_images(imgs, scale)                  # Apply to image list
resize_videos(vids, size=new_size)          # Apply to video list (each video is image list)

# With sizing calculations
resize_image_to_fit(img, height, width)     # Single with aspect ratio
resize_images_to_fit(imgs, height, width)   # Batch with aspect ratio  
resize_videos_to_fit(vids, height, width)   # Video batch with aspect ratio
```

---

## 10. ERROR HANDLING AND FALLBACKS

### Implementation Multiplexing
```python
def resize_image(image, scale, interp='bilinear'):
    """
    Fallback chain for robustness:
    1. Try OpenCV (fastest)
    2. Fall back to skimage  
    3. Fall back to pure Python (slowest but works everywhere)
    """
    try:
        return cv_resize_image(image, scale, interp)
    except Exception:
        pass
    try:
        return _resize_image_via_skimage(image, scale, interp) 
    except Exception:
        pass
    # Pure Python fallback for extreme compatibility
    return grid2d(...)  # Slowest but most compatible
```

**Key Insight**: Video operations inherit this robustness because they delegate to image functions.

---

## 11. USAGE PATTERNS AND EXAMPLES

### Video Processing Pipeline
```python
# Load video as image sequence
video = load_video("input.mp4")

# Apply image operations to video frames  
video = resize_images(video, scale=0.5)    # Batch image resize
video = crop_images(video, height=256, width=256)  # Batch image crop
video = as_rgb_images(video)               # Batch color conversion

# Save processed frames as video
save_video(video, "output.mp4", framerate=30)
```

### Cross-Domain Operations
```python
# Extract thumbnail using video function, process with image functions
thumbnail = get_youtube_video_thumbnail(video_url)
thumbnail = resize_image(thumbnail, scale=0.5)
thumbnail = crop_image_to_square(thumbnail)  
display_image(thumbnail)

# Mix video frames with still images
video_frames = load_video("clip.mp4")
still_image = load_image("overlay.png")
blended_frames = [blend_images(frame, still_image) for frame in video_frames]
save_video(blended_frames, "blended_output.mp4")
```

---

## 12. ARCHITECTURAL INSIGHTS

### Why This Design Works

1. **Conceptual Simplicity**: Videos are just "images with time" - easy to understand
2. **Code Reuse**: Image functions automatically work for video frames  
3. **Batch Optimization**: `_images_conversion()` provides optimized batch processing
4. **Lazy Evaluation**: Memory-efficient processing for large videos
5. **Format Flexibility**: Same operations work across image/video formats

### Performance Trade-offs

**Advantages**:
- Massive code reuse (image functions power video processing)
- Consistent API patterns across domains
- Automatic batching optimizations
- Memory-efficient streaming options

**Considerations**:
- Video-specific optimizations (like temporal filters) require specialized functions
- Memory usage for large videos when using batch operations
- Frame-by-frame processing may be slower than specialized video algorithms

---

## 13. FUNCTION FAMILY SUMMARY

### Core Relationship Patterns

1. **Delegation**: `video_function()` → `images_function()` → `image_function()`
2. **Multiplexing**: `save_video()` → format-specific `save_video_FORMAT()`  
3. **Bridging**: `get_youtube_video_thumbnail()` uses `load_image()`
4. **Batch Processing**: Videos processed as image batches with lazy options
5. **Format Conversion**: Universal converters work on images and video frames
6. **Implementation Fallbacks**: Inherited from image functions for robustness

### Most Important Connections

- **resize_videos()** ← delegates to → **resize_images()**
- **crop_videos()** ← delegates to → **crop_images()**  
- **save_video()** ← multiplexes to → **save_video_FORMAT()**
- **as_*_images()** ← powers → **video frame conversion**
- **load_video()** ← returns → **image sequence for batch processing**

---

*This analysis reveals RP's elegant approach: rather than building separate video and image systems, it treats videos as temporal sequences of images, allowing maximum code reuse while maintaining performance through batch optimizations and lazy evaluation.*