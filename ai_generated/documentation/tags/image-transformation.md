# Image Transformation Functions

Functions for geometric and spatial transformations of images.

## Geometric Transformations
- `rotate_image()` - Rotate images by specified angles with automatic canvas expansion
- `rotate_images()` - Batch rotation of multiple images

## Related Operations  
- `crop_image()` - Crop images to specified regions
- `resize_image()` - Scale images to different dimensions
- `flip_image()` - Mirror images horizontally or vertically

## Usage Patterns
Transformation functions commonly used in:
- Image preprocessing for machine learning
- Creating animations and visual effects  
- Data augmentation pipelines
- Image composition and tiling operations

## Implementation Notes
- Automatic canvas expansion prevents cropping during rotation
- Alpha channel handling for transparency effects
- Multiple interpolation methods supported
- Optimized for batch processing workflows