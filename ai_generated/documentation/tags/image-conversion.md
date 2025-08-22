# Image Conversion Functions

Functions for converting between different image formats and color spaces.

## Color Space Conversion
- `rgb_to_hsv()` - Convert RGB images to HSV color space
- `hsv_to_rgb()` - Convert HSV images back to RGB color space  
- `as_rgb_image()` - Convert any image format to RGB (grayscale, RGBA → RGB)

## Format Conversion  
- `_rgba_image_to_rgb_image()` - Internal: Remove alpha channel from RGBA
- `_grayscale_image_to_rgb_image()` - Internal: Convert grayscale to RGB by channel duplication
- `_rgb_image_to_rgb_image()` - Internal: Copy RGB image (for copy=True operations)

## Related Functions
- `as_rgba_image()` - Convert to RGBA format
- `as_grayscale_image()` - Convert to grayscale format
- `as_float_image()` - Convert to floating-point format
- `as_byte_image()` - Convert to byte format

## Usage Patterns
Image conversion functions are fundamental to RP's image processing pipeline, ensuring consistent formats across different operations while preserving image quality and handling edge cases.