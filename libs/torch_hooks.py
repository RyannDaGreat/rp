# 2025-03-07 07:29:36.931516
#pip install rp textual textual[syntax]

import rp
import torch
from contextlib import contextmanager
import time
import inspect
from typing import Dict, Any, Union, List, Optional

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


def is_torch_module(obj: Any) -> bool:
    """Check if an object is a PyTorch module
    
    Args:
        obj: The object to check
        
    Returns:
        bool: True if obj is a PyTorch module, False otherwise
    """
    try:
        return isinstance(obj, torch.nn.Module)
    except (ImportError, AttributeError):
        return False


def find_modules_in_object(obj: Any) -> Dict[str, torch.nn.Module]:
    """Find all PyTorch modules within an object's attributes
    
    Args:
        obj: Any object that might contain PyTorch modules as attributes
        
    Returns:
        Dict mapping attribute names to module instances
    """
    modules = {}
    
    # If the object itself is a module, return it with an empty key
    if is_torch_module(obj):
        modules[""] = obj
        return modules
    
    # For non-module objects, search their attributes
    if hasattr(obj, "__dict__"):
        for name, value in obj.__dict__.items():
            if is_torch_module(value):
                modules[name] = value
    
    return modules


@contextmanager
def stats_collection(obj: Any):
    """Context manager to collect stats during forward pass
    
    This function works with both:
    1. PyTorch modules directly
    2. Objects that contain PyTorch modules as attributes (like diffusers pipelines)
    
    It uses pre- and post-hooks to measure the actual execution time of each module
    and collect input/output tensor statistics.
    
    Args:
        obj: A PyTorch module or an object containing PyTorch modules
        
    Returns:
        The module(s) with added statistics
        
    Examples:
        # Direct module usage
        model = torch.nn.Sequential(...)
        with stats_collection(model):
            output = model(input_tensor)
            
        # With diffusers pipeline
        pipe = StableDiffusionPipeline.from_pretrained(...)
        with stats_collection(pipe):
            output = pipe("prompt", num_inference_steps=10)
            
        # After collection, view the results with the module explorer
        from rp.libs.pytorch_module_explorer import explore_module
        explore_module(model)  # or explore_module(pipe)
    """
    # Find all modules in the object
    modules = find_modules_in_object(obj)
    
    # If no modules found, warn and proceed
    if not modules:
        print(f"Warning: No PyTorch modules found in {type(obj).__name__} object")
        try:
            yield
            return
        finally:
            pass
    
    # Add hooks to all found modules
    all_hooks = []
    
    for name, module in modules.items():
        hooks = add_forward_hooks(module)
        all_hooks.extend(hooks)
        
        # Print info about which modules are being monitored
        if name:
            print(f"Collecting stats for {name} ({module.__class__.__name__})")
        else:
            print(f"Collecting stats for {module.__class__.__name__}")
    
    try:
        yield
    finally:
        # Remove all hooks when done
        for hook in all_hooks:
            hook.remove()


# Legacy function for backward compatibility
@contextmanager
def record_module_forward_stats(module):
    """Legacy context manager - kept for backwards compatibility
    
    Please use stats_collection() instead for new code.
    
    This uses pre- and post-hooks to measure the actual execution time of each module.
    
    Returns:
        The module with added statistics
    """
    # Simply call our new function
    with stats_collection(module):
        yield


# Example usage:
# 
# from diffusers import StableDiffusionPipeline
# import torch
# import rp
# from rp.libs.torch_hooks import stats_collection
# from rp.libs.pytorch_module_explorer import explore_module
#
# # Load a pipeline
# pipe = StableDiffusionPipeline.from_pretrained(
#     "runwayml/stable-diffusion-v1-5", 
#     torch_dtype=torch.float16
# )
# pipe = pipe.to("cuda")
#
# # Use the context manager to collect stats on the entire pipeline
# with stats_collection(pipe):
#     pipe("a photo of an astronaut riding a horse", num_inference_steps=5)
#
# # Explore the pipeline with collected stats
# explore_module(pipe)
#
# # Or just monitor a specific module:
# with stats_collection(pipe.unet):
#     pipe("a photo of an astronaut riding a horse", num_inference_steps=5)
#
# # Explore just the UNET
# explore_module(pipe.unet)
