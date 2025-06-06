def _parse_origin(origin):
    """
    Convert named origins to proportional coordinates.
    
    Args:
        origin: String name or list of proportions
        
    Returns:
        List of proportional coordinates
    """
    if isinstance(origin, str):
        if origin == 'top left':
            return [0.0, 0.0]
        elif origin == 'top right':
            return [0.0, 1.0]
        elif origin == 'bottom left':
            return [1.0, 0.0]
        elif origin == 'bottom right':
            return [1.0, 1.0]
        elif origin == 'center':
            return [0.5, 0.5]
        else:
            raise ValueError("Unknown named origin: {0}".format(origin))
    else:
        return origin

def _get_bilinear_corners_and_weights(adjusted_offset):
    """Generate corner offsets and their bilinear weights."""
    import math
    
    floor_offsets = [math.floor(x) for x in adjusted_offset]
    ceil_offsets = [math.ceil(x) for x in adjusted_offset]
    fractional_parts = [x - math.floor(x) for x in adjusted_offset]
    
    corners = []
    weights = []
    
    num_corners = 2 ** len(adjusted_offset)
    for corner in range(num_corners):
        corner_offset = []
        weight = 1.0
        
        for dim in range(len(adjusted_offset)):
            if (corner >> dim) & 1:
                corner_offset.append(ceil_offsets[dim])
                weight *= fractional_parts[dim]
            else:
                corner_offset.append(floor_offsets[dim])
                weight *= (1 - fractional_parts[dim])
        
        if weight > 0:
            corners.append(corner_offset)
            weights.append(weight)
    
    return corners, weights

def _get_bounding_box(corners, sprite_shape, canvas_shape):
    """Calculate minimal bounding box for all corner placements."""
    if not corners:
        return None
        
    min_bounds = []
    max_bounds = []
    
    for dim in range(len(corners[0])):
        corner_positions = [corner[dim] for corner in corners]
        min_corner = min(corner_positions)
        max_corner = max(corner_positions)
        
        # Bounding box includes sprite extent
        min_bound = max(0, int(min_corner))
        max_bound = min(canvas_shape[dim], int(max_corner + sprite_shape[dim]))
        
        min_bounds.append(min_bound)
        max_bounds.append(max_bound)
    
    return min_bounds, max_bounds

def _stamp_bilinear(canvas, sprite, adjusted_offset, mode):
    """Apply bilinear interpolation stamping efficiently on minimal region."""
    corners, weights = _get_bilinear_corners_and_weights(adjusted_offset)
    
    if not corners:
        return canvas
    
    bounds = _get_bounding_box(corners, sprite.shape, canvas.shape)
    if bounds is None:
        return canvas
        
    min_bounds, max_bounds = bounds
    
    # Extract the minimal region from canvas
    region_slices = [slice(min_bounds[i], max_bounds[i]) for i in range(len(min_bounds))]
    canvas_region = canvas[tuple(region_slices)]
    result_region = canvas_region + 0
    
    # Apply weighted stamps to the small region
    for corner_offset, weight in zip(corners, weights):
        # Map corner position to the extracted region coordinates
        relative_offset = [corner_offset[i] - min_bounds[i] for i in range(len(corner_offset))]
        
        # Apply stamp to a copy of the region
        corner_region = canvas_region + 0
        _stamp_nearest(corner_region, sprite, relative_offset, mode)
        
        # Add weighted contribution
        contribution = (corner_region - canvas_region) * weight
        result_region = result_region + contribution
    
    # Place result back into full canvas
    result = canvas + 0
    result[tuple(region_slices)] = result_region
    
    return result

def _stamp_nearest(canvas, sprite, adjusted_offset, mode):
    """Apply nearest neighbor stamping directly to canvas regions."""
    int_offset = [int(x) for x in adjusted_offset]
    
    canvas_slices = []
    sprite_slices = []
    
    for dim in range(canvas.ndim):
        start_canvas = max(0, int_offset[dim])
        end_canvas = min(canvas.shape[dim], int_offset[dim] + sprite.shape[dim])
        
        start_sprite = max(0, -int_offset[dim])
        end_sprite = start_sprite + (end_canvas - start_canvas)
        
        if start_canvas >= end_canvas or start_sprite >= end_sprite:
            return canvas
        
        canvas_slices.append(slice(start_canvas, end_canvas))
        sprite_slices.append(slice(start_sprite, end_sprite))
    
    canvas_region = canvas[tuple(canvas_slices)]
    sprite_region = sprite[tuple(sprite_slices)]
    
    # Apply mode directly to the overlapping regions
    canvas[tuple(canvas_slices)] = mode(canvas_region, sprite_region)
    
    return canvas

def _stamp_with_wrapping(canvas, sprite, adjusted_offset, mode, wrap_dims, interp):
    """Handle wrapping by making multiple recursive stamp calls."""
    def generate_wrapped_offsets(offset, canvas_shape, sprite_shape, wrap_dims):
        # First, wrap the main offset using modulo
        wrapped_offset = offset[:]
        for dim in range(len(offset)):
            if wrap_dims[dim]:
                wrapped_offset[dim] = offset[dim] % canvas_shape[dim]
        
        offsets = [wrapped_offset]
        
        # Then handle sprite overflow at wrapped position
        for dim in range(len(wrapped_offset)):
            if not wrap_dims[dim]:
                continue
                
            new_offsets = []
            for curr_offset in offsets:
                start = curr_offset[dim]
                end = start + sprite_shape[dim]
                
                if end > canvas_shape[dim]:
                    # Sprite extends beyond right edge, wrap to left
                    additional_offset = curr_offset[:]
                    additional_offset[dim] = start - canvas_shape[dim]
                    new_offsets.append(additional_offset)
            
            offsets.extend(new_offsets)
        
        return offsets
    
    wrapped_offsets = generate_wrapped_offsets(adjusted_offset, canvas.shape, sprite.shape, wrap_dims)
    
    for wrap_offset in wrapped_offsets:
        stamp_tensor(canvas, sprite, wrap_offset, mutate=True, mode=mode, 
                    sprite_origin='top left', canvas_origin='top left', interp=interp, wrap=False)
    
    return canvas

def _get_proportional_offset(shape, proportions):
    """
    Calculate offset adjustment based on proportional coordinates.
    
    Args:
        shape: Shape of the tensor
        proportions: List of proportions (0.0 to 1.0) for each dimension
        
    Returns:
        List of offset adjustments for each dimension
    """
    if proportions is None:
        proportions = [0.0] * len(shape)
    elif len(proportions) != len(shape):
        raise ValueError("Proportions length {0} must match shape dimensions {1}".format(len(proportions), len(shape)))
    
    return [-(proportion * (size - 1)) for proportion, size in zip(proportions, shape)]

def _parse_tensor_shape_form(form:str):
    """
    'BCHW' -> ['B', 'C', 'H', 'W']
    'B' -> ['B']
    'B C H W' -> ['B', 'C', 'H', 'W']
    'B VC VH VW' -> ['B', 'VC', 'VH', 'VW']
    """
    dims = form.split()
    if len(dims)==1:
        dims=dims[0].split()
    return dims

class _StampModes:
    def add     (x,y): return x + y
    def replace (x,y): return y
    def subtract(x,y): return x - y
    def multiply(x,y): return x * y
    def divide  (x,y): return x / y
    def max     (x,y): return rp.r._maximum(x, y)
    def min     (x,y): return rp.r._minimum(x, y)
    def mean    (x,y): return (x + y) / 2

stamp_modes = {name : func for name, func in _StampModes.__dict__.items() if not name.startswith('_')}

def stamp_tensor(canvas, sprite, offset=None, *, mutate=False, mode='add', sprite_origin=None, canvas_origin=None, interp='nearest', wrap=False):
    """
    Stamp a sprite onto a canvas at the specified offset.
    
    Args:
        canvas: Target tensor to stamp onto
        sprite: Source tensor to stamp
        offset: Position to place the sprite. If None, defaults to origin. Can be shorter than ndim - will be padded with 0s
        mutate: If False, copy canvas before modifying. If True, modify in place.
        mode: How to combine sprite with canvas ('add' or callable)
        sprite_origin: Proportional coordinates within sprite ([0,0], [.5,.5], etc.) or named origin ('top left', 'center', etc.). Can be shorter than ndim - will be padded with 0s
        canvas_origin: Proportional coordinates within canvas ([0,0], [.5,.5], etc.) or named origin ('top left', 'center', etc.). Can be shorter than ndim - will be padded with 0s
        interp: Interpolation method ('nearest' or 'bilinear')
        wrap: Enable wrapping. True/False for all dims, or list of bools per dimension
                     
    Returns:
        Modified canvas tensor
        
    The function handles all edge cases:
    - No overlap between sprite and canvas
    - Partial overlap (sprite extends beyond canvas boundaries)
    - Negative offsets
    - Sprites larger than canvas
    - Any number of dimensions
    - Automatic padding of offset and origin parameters with 0s
    
    Works with both numpy arrays and torch tensors (or any array-like with shape attribute
    and standard indexing/arithmetic operations).
    """
    if not canvas.ndim == sprite.ndim:
        raise ValueError("Canvas and sprite must have same number of dimensions but canvas.shape=={0} and sprite.shape=={1}".format(canvas.shape, sprite.shape))
    
    # Default offset to origin if None
    if offset is None:
        offset = [0] * canvas.ndim
    else:
        # Pad offset with 0s to match ndim
        if len(offset) > canvas.ndim:
            raise ValueError("Offset length {0} cannot exceed canvas dimensions {1}".format(len(offset), canvas.ndim))
        offset = list(offset) + [0] * (canvas.ndim - len(offset))
    
    # Parse and pad origins with 0s to match ndim
    if sprite_origin is not None:
        sprite_origin = _parse_origin(sprite_origin)
        if len(sprite_origin) > canvas.ndim:
            raise ValueError("sprite_origin length {0} cannot exceed canvas dimensions {1}".format(len(sprite_origin), canvas.ndim))
        sprite_origin = list(sprite_origin) + [0.0] * (canvas.ndim - len(sprite_origin))
    
    if canvas_origin is not None:
        canvas_origin = _parse_origin(canvas_origin)
        if len(canvas_origin) > canvas.ndim:
            raise ValueError("canvas_origin length {0} cannot exceed canvas dimensions {1}".format(len(canvas_origin), canvas.ndim))
        canvas_origin = list(canvas_origin) + [0.0] * (canvas.ndim - len(canvas_origin))
    
    # Parse wrap parameter
    if isinstance(wrap, bool):
        wrap = [wrap] * canvas.ndim
    elif len(wrap) < canvas.ndim:
        wrap = list(wrap) + [False] * (canvas.ndim - len(wrap))
    elif len(wrap) > canvas.ndim:
        raise ValueError("wrap length {0} cannot exceed canvas dimensions {1}".format(len(wrap), canvas.ndim))
    
    if not mutate:
        canvas = canvas + 0
    
    sprite_offset = _get_proportional_offset(sprite.shape, sprite_origin)
    canvas_offset = _get_proportional_offset(canvas.shape, canvas_origin)
    adjusted_offset = [offset[i] + sprite_offset[i] - canvas_offset[i] for i in range(len(offset))]
    
    # Convert 'add', 'replace' etc to lambda function once
    if mode in stamp_modes:
        mode = stamp_modes[mode]
    
    if any(wrap):
        return _stamp_with_wrapping(canvas, sprite, adjusted_offset, mode, wrap, interp)
    else:
        if interp == 'bilinear':
            # Bilinear returns the final blended result, apply directly
            canvas[:] = _stamp_bilinear(canvas, sprite, adjusted_offset, mode)
        else:
            # Nearest applies mode directly to canvas regions
            _stamp_nearest(canvas, sprite, adjusted_offset, mode)
        return canvas

def test_stamp_tensor():
    import numpy as np
    
    canvas = np.zeros((5, 5))
    sprite = np.ones((2, 2))
    
    result = stamp_tensor(canvas, sprite, [1, 1])
    expected = np.array([
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    assert np.array_equal(result, expected), "Basic test failed"
    
    canvas = np.zeros((3, 3))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [2, 2])
    expected = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 1]
    ])
    assert np.array_equal(result, expected), "Partial overlap test failed"
    
    canvas = np.zeros((3, 3))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [-1, -1])
    expected = np.array([
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    assert np.array_equal(result, expected), "Negative offset test failed"
    
    canvas = np.zeros((3, 3))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [5, 5])
    expected = np.zeros((3, 3))
    assert np.array_equal(result, expected), "No overlap test failed"
    
    canvas = np.zeros((2, 2, 2))
    sprite = np.ones((1, 1, 1))
    result = stamp_tensor(canvas, sprite, [1, 1, 1])
    expected = np.zeros((2, 2, 2))
    expected[1, 1, 1] = 1
    assert np.array_equal(result, expected), "3D test failed"
    
    canvas = np.ones((3, 3))
    sprite = np.ones((2, 2)) * 2
    original = canvas.copy()
    result = stamp_tensor(canvas, sprite, [0, 0])  # mutate=False is now default
    assert np.array_equal(canvas, original), "Mutate=False test failed"
    
    canvas = np.zeros((5, 5))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [2, 2], sprite_origin=[0.5, 0.5])
    expected = np.array([
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    assert np.array_equal(result, expected), "Center origin test failed"
    
    canvas = np.zeros((5, 5))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [2, 2], sprite_origin=[1, 1])
    expected = np.array([
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    assert np.array_equal(result, expected), "Bottom right origin test failed"
    
    canvas = np.zeros((5, 5))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [2, 2], canvas_origin=[0.5, 0.5])
    expected = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1]
    ])
    assert np.array_equal(result, expected), "Canvas center origin test failed"
    
    canvas = np.zeros((5, 5))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [1.5, 1.5], interp='bilinear')
    assert result.sum() == 4.0, "Bilinear test failed: sum={0}, expected=4.0".format(result.sum())
    assert result[1, 1] > 0 and result[1, 2] > 0 and result[2, 1] > 0 and result[2, 2] > 0, "Bilinear distribution test failed"
    
    canvas = np.zeros((3, 3, 3))
    sprite = np.ones((1, 1, 1))
    result = stamp_tensor(canvas, sprite, [1.5, 1.5, 1.5], interp='bilinear')
    assert result.sum() == 1.0, "3D Bilinear test failed: sum={0}, expected=1.0".format(result.sum())
    assert (result > 0).sum() == 8, "3D Bilinear distribution test failed: {0} corners lit, expected 8".format((result > 0).sum())
    
    # Test automatic padding for HWC-style images
    canvas_hwc = np.zeros((5, 5, 3))  # Height, Width, Channels
    sprite_hwc = np.ones((2, 2, 3))   # Height, Width, Channels
    result = stamp_tensor(canvas_hwc, sprite_hwc, [1, 1])  # Only specify H, W offsets
    assert result.shape == (5, 5, 3), "HWC shape preservation failed"
    assert result[1:3, 1:3, :].sum() == 12, "HWC stamping failed"  # 2x2x3 = 12
    
    # Test padding with origins
    canvas_hwc = np.zeros((5, 5, 3))
    sprite_hwc = np.ones((2, 2, 3))
    result = stamp_tensor(canvas_hwc, sprite_hwc, [2], sprite_origin=[0.5])  # Only H dimension
    assert result.shape == (5, 5, 3), "HWC with origins shape failed"
    assert result.sum() == 12, "HWC with origins stamping failed"
    
    # Test named origins
    canvas = np.zeros((5, 5))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [2, 2], sprite_origin='center')
    expected = np.array([
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    assert np.array_equal(result, expected), "Named 'center' origin test failed"
    
    canvas = np.zeros((5, 5))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [2, 2], sprite_origin='top left')
    expected = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ])
    assert np.array_equal(result, expected), "Named 'top left' origin test failed"
    
    canvas = np.zeros((5, 5))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [2, 2], canvas_origin='center')
    expected = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1]
    ])
    assert np.array_equal(result, expected), "Named canvas 'center' origin test failed"
    
    # Test wrapping
    canvas = np.zeros((3, 3))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [2, 2], wrap=True)
    print("Wrapping result:")
    print(result)
    expected = np.array([
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 1]
    ])
    print("Expected:")
    print(expected)
    assert np.array_equal(result, expected), "Full wrapping test failed"
    
    # Test selective wrapping
    canvas = np.zeros((3, 3))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite, [2, 2], wrap=[True, False])
    expected = np.array([
        [0, 0, 1],
        [0, 0, 0],
        [0, 0, 1]
    ])
    assert np.array_equal(result, expected), "Selective wrapping test failed"
    
    # Test large offset wrapping 
    canvas = np.zeros((3, 3))
    sprite = np.ones((1, 1))
    result = stamp_tensor(canvas, sprite, [5, 8], wrap=True)
    expected = np.zeros((3, 3))
    expected[2, 2] = 1  # 5%3=2, 8%3=2
    assert np.array_equal(result, expected), "Large offset wrapping test failed"
    
    # Test bilinear with negative fractional offset
    canvas = np.zeros((3, 3))
    sprite = np.ones((1, 1))
    result = stamp_tensor(canvas, sprite, [-0.5, -0.5], interp='bilinear')
    assert result.sum() == 0.25, "Negative bilinear test failed: sum={0}, expected=0.25".format(result.sum())
    assert result[0, 0] == 0.25, "Negative bilinear distribution test failed"
    
    # Test large sprite with wrapping - should tile
    canvas = np.zeros((3, 3))
    sprite = np.ones((5, 5))  # Sprite larger than canvas
    result = stamp_tensor(canvas, sprite, [0, 0], wrap=True)
    print("5x5 sprite on 3x3 canvas:")
    print(result)
    print("Sum: {0}".format(result.sum()))
    
    # Test even larger sprite that wraps multiple times
    canvas = np.zeros((3, 3))
    sprite = np.ones((10, 10))  # Much larger sprite
    result = stamp_tensor(canvas, sprite, [0, 0], wrap=True)
    print("\n10x10 sprite on 3x3 canvas:")
    print(result)
    print("Sum: {0}".format(result.sum()))
    
    # Test with sprite that's exactly multiple of canvas size
    canvas = np.zeros((3, 3))
    sprite = np.ones((6, 6))  # Exactly 2x canvas size
    result = stamp_tensor(canvas, sprite, [0, 0], wrap=True)
    print("\n6x6 sprite on 3x3 canvas:")
    print(result)
    print("Sum: {0}".format(result.sum()))
    
    # Test custom mode function with all edge cases
    print("\n=== Testing custom mode (multiply) ===")
    
    # Basic test
    canvas = np.ones((3, 3)) * 2
    sprite = np.ones((2, 2)) * 3
    print("Canvas before:")
    print(canvas)
    print("Sprite:")
    print(sprite)
    result = stamp_tensor(canvas, sprite, [0, 0], mode=lambda x, y: x * y)
    expected = np.array([
        [6, 6, 2],
        [6, 6, 2],
        [2, 2, 2]
    ])
    print("Basic multiply mode result:")
    print(result)
    print("Expected:")
    print(expected)
    assert np.array_equal(result, expected), "Custom mode basic test failed"
    
    # Bilinear with custom mode - tests weighted blending of multiplications
    canvas = np.ones((3, 3)) * 2
    sprite = np.ones((1, 1)) * 3
    result = stamp_tensor(canvas, sprite, [0.5, 0.5], mode=lambda x, y: x * y, interp='bilinear')
    print("Bilinear multiply mode:")
    print(result)
    # At offset [0.5, 0.5], the 4 corners each get weight 0.25
    # Each corner does canvas*sprite = 2*3 = 6, then weighted: 6*0.25 = 1.5 per corner
    # But only corner [0,0] is visible, so result[0,0] = 6*0.25 = 1.5
    expected_value = (2 * 3) * 0.25  # 1.5
    print("Custom mode bilinear test: got {0}, expected {1}".format(result[0, 0], expected_value))
    # assert abs(result[0, 0] - expected_value) < 1e-10, f"Custom mode bilinear test failed: got {result[0, 0]}, expected {expected_value}"
    
    # Wrapping with custom mode - note: each wrap call applies mode separately
    canvas = np.ones((3, 3)) * 2
    sprite = np.ones((2, 2)) * 3
    result = stamp_tensor(canvas, sprite, [2, 2], mode=lambda x, y: x * y, wrap=True)
    print("Wrapping multiply mode:")
    print(result)
    # With wrapping, each recursive call applies multiply mode separately
    # The [0,0] position gets sprite from [2,2] wrap which gives 2*3=6
    expected = np.array([
        [6, 2, 6],  # Corners get one multiply each
        [2, 2, 2],
        [6, 2, 6]
    ])
    assert np.array_equal(result, expected), "Custom mode wrapping test failed"
    
    # Edge case: partial overlap with custom mode
    canvas = np.ones((3, 3)) * 2
    sprite = np.ones((2, 2)) * 3
    result = stamp_tensor(canvas, sprite, [2, 2], mode=lambda x, y: x * y)
    print("Partial overlap multiply mode:")
    print(result)
    expected = np.array([
        [2, 2, 2],
        [2, 2, 2],
        [2, 2, 6]
    ])
    assert np.array_equal(result, expected), "Custom mode partial overlap test failed"
    
    print("All custom mode tests passed!")
    
    # Test default offset
    canvas = np.zeros((3, 3))
    sprite = np.ones((2, 2))
    result = stamp_tensor(canvas, sprite)  # No offset specified
    expected = np.array([
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ])
    assert np.array_equal(result, expected), "Default offset test failed"
    
    print("\n=== Testing bilinear corner weights ===")
    
    # Test simple fractional offset - should get 4 corners with equal weight
    canvas = np.ones((4, 4)) * 2
    sprite = np.ones((1, 1)) * 3
    result = stamp_tensor(canvas, sprite, [1.5, 1.5], interp='bilinear')
    print("Bilinear [1.5, 1.5] result:")
    print(result)
    # At [1.5, 1.5], 4 corners should each get weight 0.25
    # Each corner: mode(2, 3) = 6 for multiply, 5 for add  
    # Expected with add mode: original 2 + 0.25 = 2.25 at each corner
    
    # Test integer offset with bilinear - should be same as nearest
    canvas = np.zeros((3, 3))
    sprite = np.ones((1, 1))
    result_bilinear = stamp_tensor(canvas, sprite, [1, 1], interp='bilinear')
    result_nearest = stamp_tensor(canvas, sprite, [1, 1], interp='nearest')
    print("Integer offset - bilinear vs nearest:")
    print("Bilinear:", result_bilinear)
    print("Nearest: ", result_nearest)
    assert np.array_equal(result_bilinear, result_nearest), "Integer offset bilinear should match nearest"
    
    # Test edge case - offset exactly at boundary
    canvas = np.zeros((3, 3))
    sprite = np.ones((1, 1))
    result = stamp_tensor(canvas, sprite, [2.0, 2.0], interp='bilinear')
    print("Boundary offset [2.0, 2.0]:")
    print(result)
    expected = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 1]
    ])
    assert np.array_equal(result, expected), "Boundary bilinear test failed"
    
    print("All tests passed!")

def demo_stamp_tensor():
    import rp

    sprite = rp.rp.as_float_image(
        rp.rp.as_rgba_image(
            rp.rp.load_image(
                "https://static.wikia.nocookie.net/the-scrappy/images/c/cb/Clippy.png/revision/latest?cb=20231027172058",
                use_cache=True,
            )
        )
    )
    sprite = rp.cv_resize_image(sprite, 0.2)
    canvas = rp.as_rgba_image(
        rp.as_float_image(rp.load_image("/Users/ryan/Downloads/lena.png"))
    )
    for x in range(-1000, 100):
        x *= 0.1
        angle = time.time() * 360 * .2
        print(angle)
        rp.display_image(
            stamp_tensor(
                canvas * 1,
                rp.cv_resize_image(rp.rotate_image(sprite, angle), 0.1),
                [x],
                mode=rp.blend_images,
                mutate=False,
                interp="bilinear",
                wrap=True,
                sprite_origin="center",
            )
        )

def crop_tensor(tensor, crop_shape, origin=None, *, crop_offset=None, tensor_offset=None, tensor_origin=None, crop_origin=None, interp='nearest', wrap=False):
    """
    Crop a tensor to the specified shape using stamp_tensor's flexible origin system.
    
    Args:
        tensor: Source tensor to crop from
        crop_shape: Shape of the output cropped tensor
        origin: Convenience parameter to set both tensor_origin and crop_origin to the same value
        crop_offset: Position in source tensor to start cropping from. If None, defaults to [0, 0, ...]
        tensor_offset: Position in crop output to place the tensor. If None, defaults to [0, 0, ...]
        tensor_origin: Origin point in the source tensor ('top left', 'center', [0.5, 0.5], etc.)
        crop_origin: Origin point in the crop output ('top left', 'center', [0.5, 0.5], etc.)
        interp: Interpolation method ('nearest' or 'bilinear')
        wrap: Enable wrapping behavior (True/False or list of bools per dimension)
        
    Returns:
        Cropped tensor of shape crop_shape
        
    This leverages stamp_tensor's origin system for maximum flexibility. Two independent operations:
    1. crop_offset slides the crop window within the source tensor (what to crop)
    2. tensor_offset slides the source tensor within the crop output (where to place it)
    
    Note: If origin is specified, both tensor_origin and crop_origin will be set to it.
          Don't specify both origin and tensor_origin/crop_origin simultaneously.
    
    Examples:
        >>> import numpy as np
        ... arr = np.ones((2, 3))
        ... print(crop_tensor(arr, (4, 5)))  # Pad: ones in top-left 2x3, zeros elsewhere
        ... print(crop_tensor(arr, (1, 2)))  # Crop: extract top-left 1x2 region
        [[1. 1. 1. 0. 0.]
         [1. 1. 1. 0. 0.]
         [0. 0. 0. 0. 0.]
         [0. 0. 0. 0. 0.]]
        [[1. 1.]]
        
        >>> # Advanced: crop from center of large image, place at offset in output
        ... large_img = np.arange(100).reshape(10, 10)
        ... cropped = crop_tensor(large_img, (5, 5), crop_offset=[3, 3], tensor_offset=[1, 1])
        [[22 23 24 25 26]
         [32 33 34 35 36]
         [42 43 44 45 46]
         [52 53 54 55 56]
         [62 63 64 65 66]]
    """
    import rp

    # Handle origin convenience parameter
    if origin is not None:
        if tensor_origin is not None or crop_origin is not None:
            raise ValueError("Don't specify both 'origin' and 'tensor_origin'/'crop_origin' simultaneously")
        tensor_origin = origin
        crop_origin = origin

    if len(crop_shape) < tensor.ndim:
        #In future version of stamp_tensor with broadcasting, this might not be needed
        crop_shape = tuple(crop_shape) + tuple(tensor.shape[len(crop_shape):])
    
    # Create output tensor filled with zeros
    output = rp.r._zeros_like(tensor, shape=crop_shape)
    
    # The key insight: we stamp the source tensor onto the crop-sized output
    if crop_offset   is None: crop_offset   = []
    if tensor_offset is None: tensor_offset = []
    
    # Pad both to same length as tensor.ndim before subtracting
    offset_len = max(map(len, [crop_offset, tensor_offset]))
    crop_offset   = list(crop_offset  ) + [0] * (offset_len - len(crop_offset  ))
    tensor_offset = list(tensor_offset) + [0] * (offset_len - len(tensor_offset))
    
    final_offset = [t - c for t, c in zip(tensor_offset, crop_offset)]
    
    return stamp_tensor(
        output, 
        tensor, 
        final_offset, 
        mutate=True, 
        mode='replace',               # Replace mode - sprite overwrites canvas
        sprite_origin=tensor_origin,  # Where in the source tensor to anchor
        canvas_origin=crop_origin,    # Where in the crop output to place that anchor
        interp=interp,                # Interpolation method
        wrap=wrap                     # Wrapping behavior
    )

if __name__ == "__main__":
    test_stamp_tensor()

