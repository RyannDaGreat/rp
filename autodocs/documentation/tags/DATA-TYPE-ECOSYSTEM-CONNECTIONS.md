# RP Data Type Ecosystem Connections

## Executive Summary

RP maintains **type consistency across 2000+ functions** through a sophisticated **universal conversion network** built on fundamental data structures. The system enables seamless function composition by providing automatic conversions between formats while preserving semantic meaning across domains.

## Universal Data Types Hierarchy

### Core Foundation Layer

**`as_numpy_array(x)`** - The Universal Converter
- **Role**: Central hub for all data type conversions
- **Accepts**: Python lists, numpy arrays, PyTorch tensors (CPU/GPU), PIL images, any `np.asarray()` compatible object
- **Guarantees**: Always returns a copy, handles GPU tensors automatically, preserves precision
- **Usage**: Used by 70+ functions as the backbone for "accept anything" design

**`is_number(x)`** - Primitive Type Validator  
- **Scope**: Python numbers, numpy scalars, torch scalars, built-in numeric types
- **Pattern**: Foundation for all numeric validation across domains
- **Cross-domain**: Enables color values, matrix operations, audio processing

**`is_iterable(x)`** - Container Type Validator
- **Pattern**: Base validator for collections across all domains
- **Usage**: Colors, paths, coordinate arrays, batch operations

### Domain-Specific Universal Types

## 1. Image Ecosystem - The Model Domain

**Image Representations (Interchangeable)**
```python
# All equivalent representations of the same image:
numpy_img    # HWC numpy array (primary format)
pil_img      # PIL.Image object  
torch_img    # CHW torch tensor (separate validation)

# Automatic conversion network:
is_image() → as_numpy_image() → as_pil_image() → as_torch_image()
```

**Format Conversion Network**
```
Channel Formats:    Grayscale (HW) ←→ RGB (HW3) ←→ RGBA (HW4)
Data Type Network:  Bool ←→ UInt8 (0-255) ←→ Float32 (0.0-1.0)
Backend Formats:    NumPy ←→ PIL ←→ PyTorch
```

**Batch Operations Pattern**
- Singular: `resize_image()` → Plural: `resize_images()`  
- Input: Any mix of formats → Output: Consistent format
- Efficiency: Tensor operations when possible, fallback to per-image processing

## 2. Color Ecosystem - Cross-Domain Connector

**Universal Color Representation**
```python
# All accepted formats for colors:
[0.5, 0.8, 0.2]           # Float RGB (0.0-1.0)
[128, 200, 50]            # Byte RGB (0-255)  
[128, 200, 50, 255]       # Byte RGBA with alpha
'#80C832'                 # Hex color string
np.array([0.5, 0.8, 0.2]) # Numpy color array

# Validation hierarchy:
is_color() → is_float_color() | is_byte_color() | is_binary_color()
```

**Color Conversion Network**
```
String Colors:  Hex ←→ Named Colors ←→ RGB tuples
Numeric Types:  Float (0-1) ←→ Byte (0-255) ←→ Binary (T/F)
Format Bridge:  Colors ←→ Images (uniform_color_image())
```

**Cross-Domain Usage**
- **Images**: Background colors, blend operations, alpha channels
- **Graphics**: Plot colors, annotation colors, UI elements  
- **Data**: Color mapping for visualizations, categorical encoding

## 3. Mathematical Objects - Computational Core

**Matrix/Tensor Abstraction**
```python
is_a_matrix()        # 2D numerical arrays
is_a_square_matrix() # NxN matrices for transformations
_tensorify()         # Universal tensor converter (internal)
```

**Coordinate System Network** 
```python
# All convertible coordinate formats:
is_points_array()    # [[x1,y1], [x2,y2], ...] format
is_cv_contour()      # OpenCV contour format
is_complex_vector()  # Complex number coordinates

# Converters:
as_points_array() | as_cv_contour() | as_complex_vector()
```

**Usage Bridges**
- **Images**: Transformation matrices, coordinate mapping, geometric operations
- **Audio**: Signal processing matrices, frequency domain transforms
- **Graphics**: 3D transformations, projection matrices

## 4. File & Network Types - I/O Abstraction

**Universal Resource Identifiers**
```python
is_valid_url()       # Network resource validation
is_image_file()      # Image file type detection  
is_video_file()      # Video file type detection
is_sound_file()      # Audio file type detection
```

**I/O Abstraction Pattern**
```python
# Same function, different sources:
load_image('path/to/file.jpg')           # Local file
load_image('https://example.com/img.png') # Network URL  
load_image_from_clipboard()              # System clipboard
```

**Cross-Domain I/O Pattern**
- **Detection**: File type → Domain router → Specialized loader
- **Caching**: Unified caching across local/network sources
- **Fallback**: URL download → temp file → standard file loading

## 5. Audio/Video Temporal Data

**Temporal Container Pattern**
```python
# Video = Sequence of Images
THWC_numpy    # Time, Height, Width, Channels
TCHW_torch    # Time, Channels, Height, Width

# Audio = 1D/2D Numerical Sequences  
audio_array   # Numpy arrays with sampling rate metadata
```

**Temporal Conversion Network**
```
Video Formats:  List[Images] ←→ THWC Array ←→ TCHW Tensor
Audio Formats:  MP3/WAV ←→ Numpy Arrays ←→ Frequency Domain
```

## Cross-Domain Compatibility Patterns

### 1. The `pip_import` Ecosystem

**Lazy Dependency Loading (436+ uses)**
```python
pip_import('cv2')        # Auto-installs opencv-python if needed
pip_import('torch')      # Handles PyTorch ecosystem
pip_import('PIL')        # Pillow/PIL ecosystem bridge
```

**Pattern Benefits**
- **Minimal imports**: Only load what you use (22ms startup vs NumPy's 207ms)
- **Auto-resolution**: Package name mismatches handled automatically
- **Failure isolation**: Missing dependencies don't break unrelated functionality

### 2. Implementation Multiplexing Pattern

**Base Function → Specialized Variants**
```python
# Base function with common arguments only:
resize_image(img, scale)

# Backend-specific variants with format-specific args:
_resize_image_via_cv2(img, interpolation=cv2.INTER_CUBIC)
_resize_image_via_skimage(img, anti_aliasing=True)
```

**Multiplexing Strategy**
- **File extension routing**: `save_video()` → `save_video_mp4()` with bitrate args
- **Backend fallbacks**: Try optimal backend first, fallback to alternatives
- **No useless args**: Base functions stay clean, variants handle complexity

### 3. Type Consistency Guarantees

**Input Acceptance Rules**
1. **Accept anything reasonable**: Functions try multiple conversion paths
2. **Consistent output format**: Return type matches function domain expectations  
3. **Copy semantics**: `copy=True` default ensures mutation safety
4. **Validation boundaries**: Clear error messages when conversion impossible

**Composition Enablement**
```python
# This works because of universal conversion network:
result = blend_images(
    load_image('path/img1.jpg'),           # File → numpy array
    uniform_color_image(100, 100, 'red'),  # String → color → image  
    alpha=load_image_from_clipboard()       # Clipboard → grayscale → alpha
)
```

## Function Composition Architecture

### Data Flow Patterns

**1. Pipeline Composition**
```python
# Each function accepts output of previous:
image → resize_image() → as_grayscale_image() → inverted_image() → save_image()
```

**2. Mixed-Type Operations** 
```python
# Different input types, unified processing:
blend_images(
    numpy_image,     # Already correct format
    pil_image,       # Converted via as_numpy_image()  
    torch_tensor,    # Converted via as_numpy_array()
    alpha=0.5        # Number → alpha mask
)
```

**3. Batch Processing Consistency**
```python
# Singular and plural functions maintain compatibility:
single_result = process_image(img)
batch_results = process_images([img1, img2, img3])  # Same semantics
```

### Error Handling & Validation Hierarchy

**Validation Cascade**
1. **Type validation**: `is_image()`, `is_color()`, `is_number()`
2. **Format detection**: Channel count, data type, dimensions
3. **Automatic conversion**: Try reasonable conversion paths  
4. **Clear failures**: Meaningful error messages when impossible

**Cross-Domain Error Consistency**
```python
assert is_image(input), 'Error: input is not an image as defined by rp.is_image()'
assert is_color(color), 'Color should be RGB/RGBA float color or string'
assert is_number(value), 'Expected numeric value, got: ' + type(value)
```

## Performance & Memory Considerations

### Conversion Efficiency

**Smart Copying Strategy**
- `copy=False`: Performance optimization, might not copy, might mutate original
- `copy=True`: Always creates new object, safe for mutation
- **Efficiency shortcuts**: Skip expensive ops when format already correct

**Tensor Operation Batching**
- **Numpy vectorization**: Process entire arrays when possible
- **Torch GPU acceleration**: Keep computations on GPU when available
- **Fallback gracefully**: Per-element processing when vectorization impossible

### Caching & Memory Management  

**Strategic Caching**
- **File loading**: Cache by absolute path for consistency
- **Network resources**: Download once, cache locally
- **Expensive conversions**: Cache format conversions where appropriate

## Conclusion: The "Accept Anything" Philosophy

RP's data type ecosystem succeeds because it provides:

1. **Universal Converters**: `as_numpy_array()` as the central conversion hub
2. **Domain Bridges**: Colors, coordinates, and I/O abstractions work across domains  
3. **Lazy Loading**: Only import what you need, when you need it
4. **Consistent Patterns**: Same validation/conversion patterns across all domains
5. **Composition Support**: Any function output can feed into compatible function input
6. **Performance Optimization**: Smart copying, vectorization, and backend selection

This creates a **cohesive ecosystem** where users focus on **what** they want to accomplish, not **how** to wrangle data types between operations.

---

*This documentation maps the data type connections that enable RP's 2000+ functions to work seamlessly together across images, audio, video, mathematical objects, colors, files, and network resources.*