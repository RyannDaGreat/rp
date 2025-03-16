import rp

def resize_conv2d_channels(conv2d, in_channels=None, out_channels=None):
    """
    Create a new Conv2d layer with resized input/output channels while preserving weights.
    
    Args:
        conv2d: Original Conv2d layer
        in_channels: New number of input channels (if None, keeps original)
        out_channels: New number of output channels (if None, keeps original)
        
    Returns:
        New Conv2d layer with requested channel dimensions and preserved weights
        
    EXAMPLE:
        >>> import torch.nn as nn
        >>> # Original conv2d with 3 input channels, 64 output channels
        >>> conv = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        
        >>> conv
        Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        >>> conv.weight.shape
        torch.Size([64, 3, 3, 3])
        
        >>> # Resize to 5 input channels, 32 output channels
        >>> new_conv = resize_conv2d_channels(conv, in_channels=5, out_channels=32)
        
        >>> new_conv
        Conv2d(5, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
        >>> new_conv.weight.shape
        torch.Size([32, 5, 3, 3])
        
    """
    from torch.nn import Conv2d
    
    # ------------------------
    # Input Validation Section
    # ------------------------
    if not isinstance(conv2d, Conv2d):
        raise TypeError("Expected Conv2d layer, got " + type(conv2d).__name__)

    # Set new channels or keep original
    new_in_channels = in_channels if in_channels is not None else conv2d.in_channels
    new_out_channels = out_channels if out_channels is not None else conv2d.out_channels
    
    # Validate channel dimensions
    if new_in_channels <= 0:
        raise ValueError("in_channels must be positive, got " + str(new_in_channels))
    if new_out_channels <= 0:
        raise ValueError("out_channels must be positive, got " + str(new_out_channels))
        
    # Check if groups is compatible with new in_channels
    if new_in_channels % conv2d.groups != 0:
        raise ValueError(
            "in_channels ("
            + str(new_in_channels)
            + ") must be divisible by groups ("
            + str(conv2d.groups)
            + ")"
        )
    
    # ------------------------
    # Main Implementation
    # ------------------------
    # Create new Conv2d with same parameters except for channels
    new_conv = Conv2d(
        in_channels=new_in_channels,
        out_channels=new_out_channels,
        kernel_size=conv2d.kernel_size,
        stride=conv2d.stride,
        padding=conv2d.padding,
        dilation=conv2d.dilation,
        groups=conv2d.groups,
        bias=conv2d.bias is not None,
        padding_mode=conv2d.padding_mode,
        device=conv2d.weight.device,
        dtype=conv2d.weight.dtype
    )
    
    # Copy weights where dimensions overlap using rp.crop_tensor
    new_weight_shape = (new_out_channels, new_in_channels // conv2d.groups) + conv2d.kernel_size
    new_conv.weight.data = rp.crop_tensor(conv2d.weight.data, new_weight_shape)
    
    # Copy bias where dimensions overlap
    if conv2d.bias is not None:
        new_conv.bias.data = rp.crop_tensor(conv2d.bias.data, (new_out_channels,))
    
    return new_conv

