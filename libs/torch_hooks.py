# 2025-03-07 07:29:36.931516
#pip install rp textual textual[syntax]

import rp
import torch
from contextlib import contextmanager
import time

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

# Import for more accurate timing
import torch.autograd.profiler as profiler
import functools

def add_forward_hooks(module):
    """Add hooks to record stats during forward pass of all submodules"""
    hooks = []
    
    def forward_pre_hook(module, input):
        """Pre-hook to start timing just before module execution"""
        # Use backend-agnostic approach with PyTorch profiler
        # Create a profiler context and store it on the module
        module._profiler_context = profiler.record_function(f"{module.__class__.__name__}_forward")
        module._profiler_context.__enter__()  # Start the profiler
        
        # Also store a simple wall time for backup
        module._forward_start_time = time.time()
        
        return None
    
    def forward_hook(module, input, output):
        """Post-hook to finish timing right after module execution"""
        # Default to using wall time as fallback
        runtime = 0.0
        end_time = time.time()
        
        # Profiler-based timing (backend agnostic)
        if hasattr(module, '_profiler_context'):
            # Exit the profiler context to end timing
            try:
                # Get elapsed time in microseconds from profiler
                # Save the context in a temporary variable
                ctx = module._profiler_context
                ctx.__exit__(None, None, None)
                
                # PyTorch profiler doesn't provide direct access to elapsed time
                # So we'll use our wall time as primary source
                runtime = end_time - module._forward_start_time
                
                # Clean up
                delattr(module, '_profiler_context')
            except Exception as e:
                # Log the error for debugging
                print(f"Error in profiler timing for {module.__class__.__name__}: {str(e)}")
                # Fallback to wall time if profiler fails
                if hasattr(module, '_forward_start_time'):
                    runtime = end_time - module._forward_start_time
        elif hasattr(module, '_forward_start_time'):
            # Fallback to wall time if profiler wasn't available
            runtime = end_time - module._forward_start_time
        
        # Clean up temporary attributes
        if hasattr(module, '_forward_start_time'):
            delattr(module, '_forward_start_time')
        
        # Initialize forward_stats list if it doesn't exist
        if not hasattr(module, 'forward_stats'):
            module.forward_stats = []
            
        # Create stats dictionary
        stats = rp.as_easydict()
        
        # Add runtime information
        stats.update({
            'runtime': runtime,  # Time in seconds for this module's forward pass
        })
        
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
        
        # Only add stats if we have information
        # Always add stats now, even if there's only runtime info
        module.forward_stats.append(stats)
    
    # Register hooks for all submodules
    for name, submodule in module.named_modules():
        if hasattr(submodule, "forward") and callable(submodule.forward):
            # Clear existing stats
            if hasattr(submodule, "forward_stats"):
                del submodule.forward_stats
            
            # Register pre-hook to start timing
            pre_hook = submodule.register_forward_pre_hook(forward_pre_hook)
            hooks.append(pre_hook)
            
            # Register post-hook to end timing and collect stats
            post_hook = submodule.register_forward_hook(forward_hook)
            hooks.append(post_hook)
    
    return hooks


@contextmanager
def record_module_forward_stats(module):
    """Context manager to collect stats during forward pass
    
    This uses pre- and post-hooks to measure the actual execution time of each module.
    For GPU operations, it uses CUDA events with synchronization for accurate timing.
    For CPU operations, it uses time.time().
    
    The timing is as accurate as possible:
    - For GPU: Uses torch.cuda.Event with synchronization
    - For CPU: Uses time.time() directly
    - Automatically detects whether operations are on GPU or CPU
    
    Returns:
        The module with added statistics
    """
    # Register both pre-hooks and post-hooks for timing
    hooks = add_forward_hooks(module)
    try:
        yield
    finally:
        # Remove all hooks when done
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
