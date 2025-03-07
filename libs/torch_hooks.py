# 2025-03-07 07:29:36.931516
#pip install rp textual textual[syntax]

import rp
import torch
from contextlib import contextmanager
# No time import needed

def calculate_tensor_memory(tensor):
    """Calculate memory usage of a tensor including its gradient if it exists"""
    tensor_bytes = tensor.nelement() * tensor.element_size()
    grad_bytes = 0
    if tensor.grad is not None:
        grad_bytes = tensor.grad.nelement() * tensor.grad.element_size()
    return tensor_bytes + grad_bytes

def extract_tensor(obj):
    """
    Extract a tensor from an object that might be:
    1. A tensor itself
    2. A container object (like Transformer2DModelOutput) with a tensor attribute
    3. Something else (return None)
    """
    # If it's already a tensor, return it
    if isinstance(obj, torch.Tensor):
        return obj
        
    # If it has a 'sample' attribute that's a tensor (common in diffusers outputs)
    if hasattr(obj, 'sample') and isinstance(obj.sample, torch.Tensor):
        return obj.sample
    
    # Try common tensor attribute names
    for attr_name in ['tensor', 'hidden_states', 'last_hidden_state', 'logits', 'values', 'pred']:
        if hasattr(obj, attr_name) and isinstance(getattr(obj, attr_name), torch.Tensor):
            return getattr(obj, attr_name)
            
    # Try the first attribute that's a tensor
    if hasattr(obj, '__dict__'):
        for attr_name, attr_val in obj.__dict__.items():
            if isinstance(attr_val, torch.Tensor):
                return attr_val
    
    # No tensor found
    return None

def add_forward_hooks(module):
    """Add hooks to record stats during forward pass of all submodules"""
    
    hooks = []
    
    def forward_hook(module, input, output):
        """Record stats after the module has run"""
        # Initialize forward_stats list if it doesn't exist
        if not hasattr(module, 'forward_stats'):
            module.forward_stats = []
            
        # Create stats dictionary
        stats = rp.as_easydict()
        
        # Extract input tensor if available
        input_tensor = None
        if isinstance(input, tuple) and len(input) > 0:
            input_tensor = extract_tensor(input[0])
            
        # Add input tensor stats if we have a tensor
        if input_tensor is not None:
            stats.update({
                'in_shape': input_tensor.shape,
                'in_dtype': input_tensor.dtype,
                'in_device': input_tensor.device,
                'in_min': float(input_tensor.min()),
                'in_max': float(input_tensor.max()),
                'in_mean': float(input_tensor.float().mean()),
                'in_std': float(input_tensor.float().std()),
                'in_requires_grad': input_tensor.requires_grad,
                'in_has_grad': input_tensor.grad is not None,
                'in_memory_bytes': calculate_tensor_memory(input_tensor),
            })
        
        # Extract output tensor if available
        output_tensor = extract_tensor(output)
        
        # Add output tensor stats if we have a tensor
        if output_tensor is not None:
            stats.update({
                'out_shape': output_tensor.shape,
                'out_dtype': output_tensor.dtype,
                'out_device': output_tensor.device,
                'out_min': float(output_tensor.min()),
                'out_max': float(output_tensor.max()),
                'out_mean': float(output_tensor.float().mean()),
                'out_std': float(output_tensor.float().std()),
                'out_requires_grad': output_tensor.requires_grad,
                'out_has_grad': output_tensor.grad is not None,
                'out_memory_bytes': calculate_tensor_memory(output_tensor),
            })
        
        # Only add stats if we have output or input information
        if len(stats) > 0:    
            # Add to the module's stats
            module.forward_stats.append(stats)
    
    # Register hooks for all submodules
    for name, submodule in module.named_modules():
        if hasattr(submodule, "forward") and callable(submodule.forward):
            # Clear existing stats
            if hasattr(submodule, "forward_stats"):
                del submodule.forward_stats
            
            # Register forward hook
            hook = submodule.register_forward_hook(forward_hook)
            
            # Keep track of handle to remove later
            hooks.append(hook)
    
    return hooks


@contextmanager
def record_module_forward_stats(module):
    """Context manager to collect stats during forward pass"""
    hooks = add_forward_hooks(module)
    try:
        yield
    finally:
        # Remove hooks when done
        for hook in hooks:
            hook.remove()



# from diffusers import StableDiffusionPipeline
# import rp
#
# pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16", torch_dtype=torch.float16)
# pipe = pipe.to('mps')
#
# # Use the context manager for clean hook management
# with rp.record_module_forward_stats(pipe.unet):
#     pipe('Image of Doggy', num_inference_steps=3)
#
# # Explore the collected stats
# rp.explore_torch_module(pipe.unet)
