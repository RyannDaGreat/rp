# Image Processing Functions

Comprehensive image manipulation, conversion, and analysis tools.

## Image Loading & Saving
- **load_image** (r.py:11350) - Universal image loader (files, URLs, arrays)
- **save_image** (r.py:11458) - Multi-format image saving with auto-detection
- **save_image_jpg** (r.py:11502) - JPEG-specific saving with quality control
- **save_animated_png** (r.py:11892) - APNG creation from image sequences

## Image Type Detection & Validation
- **is_image** (r.py:10845) - Universal image format detection
- **is_torch_tensor** (r.py:10892) - PyTorch tensor detection
- **is_numpy_array** (r.py:10923) - NumPy array validation
- **is_binary_image** (r.py:10967) - Binary/boolean image detection
- **is_grayscale_image** (r.py:11012) - Grayscale format detection
- **is_rgb_image** (r.py:11045) - RGB format validation
- **is_rgba_image** (r.py:11078) - RGBA format validation with alpha channel
- **is_byte_image** (r.py:11134) - Integer pixel format validation
- **is_video_file** (r.py:11298) - Video file format detection via MIME types

## Image Format Conversion
- **as_numpy_image** (r.py:10556) - Convert any image to NumPy array
- **as_numpy_array** (r.py:10612) - General array conversion utility
- **as_byte_image** (r.py:10734) - Convert to uint8 pixel format
- **as_rgb_image** (r.py:10823) - Convert any image to RGB format
- **as_pil_image** (r.py:10891) - Convert to PIL Image format
- **_rgba_image_to_rgb_image** (r.py:10945) - RGBA→RGB conversion helper
- **_grayscale_image_to_rgb_image** (r.py:10967) - Grayscale→RGB conversion
- **_rgb_image_to_rgb_image** (r.py:10989) - RGB copying helper

## Batch Image Operations
- **inverted_images** (r.py:46084) - Batch color inversion with format preservation
- **resize_videos** (r.py:42134) - Batch video resizing operations
- **resize_video_to_fit** (r.py:42198) - Single video resize with aspect ratio
- **decode_images_from_bytes** (r.py:11201) - Deserialize compressed image data

## Color Space & Transformation
- **rgb_to_hsv** (r.py:15234) - RGB to HSV color space conversion
- **hsv_to_rgb** (r.py:15289) - HSV to RGB conversion with validation
- **rotate_image** (r.py:18143) - Image rotation with canvas expansion

## Display & Visualization
- **display_image** (r.py:19567) - Multi-backend image display
- **cv_imshow** (r.py:12156) - OpenCV-based interactive display
- **display_file_tree** (r.py:18755) - Visual file system explorer with image previews
- **_display_image_in_notebook_via_ipyplot** (r.py:19654) - Jupyter notebook display

## Advanced Computer Vision
- **get_optical_flow_via_pyflow** (r.py:16789) - Optical flow computation
- **cv_best_match_contour** (r.py:12834) - Single best contour matching
- **cv_best_match_contours** (r.py:12901) - Ranked contour matching
- **get_apriltag_images** (r.py:53732) - AprilTag detection and extraction

## Video Processing
- **get_video_width** (r.py:42001) - Extract video width dimension
- **get_video_height** (r.py:42023) - Extract video height dimension  
- **get_video_widths** (r.py:42067) - Batch video width extraction
- **get_video_heights** (r.py:42089) - Batch video height extraction
- **as_numpy_video** (r.py:41823) - Convert video to NumPy array
- **as_numpy_videos** (r.py:41867) - Batch video conversion
- **resize_videos** (r.py:42134) - Batch video resizing operations
- **resize_video_to_fit** (r.py:42198) - Single video resize with aspect ratio
- **crop_videos_to_max_size** (r.py:42312) - Crop to maximum dimensions
- **crop_videos_to_min_size** (r.py:42356) - Crop to minimum dimensions

## Computer Vision & Detection
- **get_apriltag_images** (r.py:53732) - AprilTag detection and extraction from images