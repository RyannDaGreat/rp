# RP Encoding/Decoding Theme Connections

## Overview
This document maps all encoding/decoding related functions in the RP module and their interconnected workflows. RP provides comprehensive data transformation capabilities across multiple formats and representations.

## Core Encoding/Decoding Function Categories

### 1. Base64 Encoding/Decoding Functions

**Core Base64 Functions:**
- `bytes_to_base64(bytestring: bytes) -> str` - Convert bytes to base64 string
- `base64_to_bytes(base64_string: str) -> bytes` - Convert base64 string back to bytes
- `object_to_base64(x)` - Serialize object to base64 (uses `object_to_bytes` + `bytes_to_base64`)
- `base64_to_object(x)` - Deserialize base64 to object (uses `base64_to_bytes` + `bytes_to_object`)

**Image-Specific Base64 Functions:**
- `encode_image_to_base64(image, filetype=None, quality=100)` - Encode single image to base64
- `encode_images_to_base64(images, filetype=None, quality=100)` - Batch encode images to base64
- `decode_image_from_base64(base64_string)` - Decode base64 string back to image
- `decode_images_from_base64(base64_strings)` - Batch decode base64 strings to images

**File Base64 Functions:**
- `file_to_base64(path: str, use_cache=False)` - Convert file directly to base64

### 2. Byte Operations and Binary Data Handling

**Core Byte Functions:**
- `object_to_bytes(x: object) -> bytes` - Serialize any object to bytes using dill + compression
- `bytes_to_object(x: bytes) -> object` - Deserialize bytes back to object
- `can_convert_object_to_bytes(x: object) -> bool` - Check if object can be serialized
- `file_to_bytes(path: str, use_cache=False)` - Read file as bytes
- `bytes_to_file(data: bytes, path: str = None)` - Write bytes to file

**Image-Byte Functions:**
- `encode_image_to_bytes(image, filetype=None, quality=100)` - Encode image to bytes
- `encode_images_to_bytes(images, filetype=None, quality=100)` - Batch encode images to bytes
- `decode_bytes_to_image(encoded_image: bytes)` - Decode bytes to image
- `decode_images_from_bytes(encoded_images)` - Batch decode bytes to images

**Video-Byte Functions:**
- `encode_video_to_bytes(video, filetype: str='.avi', framerate=30)` - Encode video to bytes
- `decode_video_from_bytes(encoded_video: bytes, filetype: str='.avi')` - Decode bytes to video

**Base16 (Hex) Functions:**
- `bytes_to_base16(bytestring: bytes) -> str` - Convert bytes to hex string
- `base16_to_bytes(base16_string: str) -> bytes` - Convert hex string to bytes

### 3. Steganography Functions (Data Hiding in Images)

**Core Steganography Functions:**
- `encode_bytes_to_image(data: bytes)` - Hide binary data inside an RGB image
- `decode_image_to_bytes(image) -> bytes` - Extract binary data from an image

**Workflow:**
1. `encode_bytes_to_image()` packs data length as 8-byte little-endian integer
2. Pads data to fit in RGB pixels (3 bytes per pixel)
3. Creates square image with side_len = ceil(sqrt(pixels_needed))
4. `decode_image_to_bytes()` extracts length from first 8 bytes, then returns exact data

**REPL Integration:**
- `ICO`, `IMCO`, `IFC`, `IFCA`, `IFCH` - Copy objects/files as visual images in terminal
- `IPA`, `IMPA`, `IMP`, `IFP`, `IFPA` - Paste objects/files from images

### 4. URL Encoding/Decoding Functions

**URL Handling Functions:**
- Uses standard `urllib.parse` module for URL operations
- `is_valid_url(url)` - Validate URL format using urllib.parse
- Various functions use `urllib.parse.urlencode()` for parameter encoding
- `urllib.parse.quote()` and `urllib.parse.quote_plus()` for URL component encoding

**Notable URL Usage:**
- Google search URL construction with `urllib.parse.quote(query)`
- TinyURL API integration with `urlencode({'url': url})`
- Web request parameter encoding

### 5. Compression/Decompression Functions

**Core Compression Functions:**
- `compress_bytes(data: bytes) -> bytes` - Compress bytes using zlib
- `decompress_bytes(compressed_data: bytes) -> bytes` - Decompress zlib-compressed bytes

**Archive Functions:**
- `make_zip_file_from_folder(src_folder, dst_zip_file) -> str` - Create ZIP archive
- `extract_zip_file(zip_file_path, folder_path, *, treat_as=None, show_progress=False)` - Extract ZIP/TAR
- `unzip_to_folder` - Alias for `extract_zip_file`
- `zip_folder_to_bytes(folder_path: str)` - Create ZIP archive in memory as bytes

**Integration:**
- `object_to_bytes()` automatically compresses serialized data using `compress_bytes()`
- `bytes_to_object()` automatically decompresses using `decompress_bytes()`

### 6. Serialization Functions (Pickle, JSON, etc.)

**Object Serialization:**
- `_dill_dumps(x)` - Internal dill serialization
- `object_to_bytes(x)` - High-level object serialization (dill + compression)
- `bytes_to_object(x)` - High-level object deserialization

**JSON Functions:**
- `load_json(path, *, use_cache=False)` - Load JSON from file
- `load_jsons(*paths, use_cache=False, strict=True, ...)` - Batch load JSON files
- `save_json(data, path, *, pretty=False, default=None)` - Save data as JSON
- `autoformat_json(data, indent=4)` - Format JSON with proper indentation

**Pickle Functions:**
- `load_pickled_value(file_name: str)` - Load pickled data from file
- `save_pickled_value(file_name: str, *variables)` - Save variables as pickled data

### 7. Hash Functions and Checksums

**Core Hash Functions:**
- `_get_hash(source, hash_func_name, func_display_name, *, show_progress, format)` - Generic hash helper
- `get_md5_hash(source, format='hex', *, show_progress=False)` - MD5 hashing
- `get_sha256_hash(source, format='hex', *, show_progress=False)` - SHA256 hashing

**Hash Output Formats:**
- `'hex'`/`'base16'` - Hexadecimal string (default)
- `'int'` - Integer representation
- `'bytes'` - Raw bytes
- `'base64'` - Base64 encoded string

**Utility Hash Functions:**
- `handy_hash(value)` - General-purpose hashing for objects
- `args_hash(function, *args, **kwargs)` - Hash function arguments for memoization
- `_set_hash(x)`, `_dict_hash(x)`, `_list_hash(x)`, etc. - Type-specific hashers

### 8. Encryption/Decryption Functions

**Status:** No explicit encryption/decryption functions found in RP. The module focuses on encoding, compression, and data transformation rather than cryptographic security.

## Key Workflow Connections

### 1. Object → Base64 Workflow
```python
object → object_to_bytes() → compress_bytes() → bytes_to_base64() → base64_string
base64_string → base64_to_bytes() → decompress_bytes() → bytes_to_object() → object
```

### 2. Image → Base64 Workflow  
```python
image → encode_image_to_bytes() → bytes_to_base64() → base64_string
base64_string → base64_to_bytes() → decode_bytes_to_image() → image
```

### 3. Steganography Workflow
```python
data → encode_bytes_to_image() → rgb_image
rgb_image → decode_image_to_bytes() → data
```

### 4. File Archive Workflow
```python
folder → make_zip_file_from_folder() → zip_file
zip_file → extract_zip_file() → folder
folder → zip_folder_to_bytes() → bytes
```

### 5. Comprehensive Data Pipeline
```python
# Forward: Any Object → Visual Steganography
object → object_to_bytes() → compress_bytes() → encode_bytes_to_image() → rgb_image

# Reverse: Visual Steganography → Any Object  
rgb_image → decode_image_to_bytes() → decompress_bytes() → bytes_to_object() → object
```

## Function Pairs and Symmetric Operations

### Core Symmetric Pairs
- `bytes_to_base64` ↔ `base64_to_bytes`
- `bytes_to_base16` ↔ `base16_to_bytes`
- `object_to_bytes` ↔ `bytes_to_object` 
- `object_to_base64` ↔ `base64_to_object`
- `encode_image_to_bytes` ↔ `decode_bytes_to_image`
- `encode_image_to_base64` ↔ `decode_image_from_base64`
- `encode_bytes_to_image` ↔ `decode_image_to_bytes`
- `compress_bytes` ↔ `decompress_bytes`
- `file_to_bytes` ↔ `bytes_to_file`
- `make_zip_file_from_folder` ↔ `extract_zip_file`

### Batch Operation Pairs
- `encode_images_to_bytes` ↔ `decode_images_from_bytes`
- `encode_images_to_base64` ↔ `decode_images_from_base64`

## REPL Integration Shortcuts

### Base64 Object Transfer Commands
- `64P` - Paste object from base64 clipboard
- `64C` - Copy object to base64 clipboard  
- `64FC` - Copy file bundle to base64
- `64FCA` - Copy answer file bundle to base64
- `64FCH` - Copy current directory to base64
- `64FP` - Paste file bundle from base64
- `64FPA` - Paste answer file bundle from base64

### Image Steganography Commands
- `ICO`, `IMCO` - Copy object as visual image
- `IFC`, `IFCA`, `IFCH` - Copy file as visual image  
- `IPA`, `IMPA`, `IMP` - Paste object from image
- `IFP`, `IFPA` - Paste file from image
- `IFPAO`, `IFPO` - Paste and open file from image

## Performance and Design Notes

### Automatic Compression
- `object_to_bytes()` automatically applies zlib compression for efficiency
- All steganography operations work on compressed data by default

### Caching Support
- `file_to_bytes()` and `file_to_base64()` support `use_cache=False` parameter
- Hash functions support `show_progress=False` for large files

### Multi-Format Support  
- Hash functions support multiple output formats (hex, int, bytes, base64)
- Image encoding supports various filetypes and quality settings
- Archive extraction supports both ZIP and TAR formats with auto-detection

### Error Handling
- `bytes_to_object()` gracefully falls back to returning original bytes on decompression failure
- `can_convert_object_to_bytes()` pre-validates serializability using dill.pickles()

## Integration Patterns

### 1. Web Integration
- Base64 encoding for HTTP data transfer
- Image base64 encoding for HTML embedding in Jupyter notebooks
- URL encoding for web requests and API calls

### 2. File System Integration  
- Direct file-to-base64 conversion with caching
- ZIP archive creation and extraction
- Temporary file handling for complex workflows

### 3. Image Processing Integration
- Seamless conversion between image formats and bytes/base64
- Steganography for hiding arbitrary data in images
- Batch processing support for multiple images

### 4. Terminal/REPL Integration
- Visual data transfer using image steganography
- Clipboard integration for base64 data
- Command shortcuts for common encoding workflows

This encoding/decoding system provides a comprehensive foundation for data transformation, serialization, and steganographic operations across the entire RP ecosystem.