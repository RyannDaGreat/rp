import rp
rp.pip_import('textual')
rp.pip_import('textual','textual[syntax]')
rp.pip_import('rich')
rp.pip_import('numpy')

from asyncio import Queue, Lock
from dataclasses import dataclass, field
from typing import Dict, Optional, Any, List, Tuple
from textual import work
from textual.await_complete import AwaitComplete
from textual.message import Message
from textual.widgets._tree import Tree, TreeNode
from textual.worker import Worker, WorkerCancelled, WorkerFailed, get_current_worker

# torch_hooks module and pytorch_module_explorer are kept separate
# but pytorch_module_explorer can display forward_stats if present

# No time formatting needed

def format_shape(shape):
    """Format a shape tuple consistently with proper multiplication symbols"""
    return "×".join(str(dim) for dim in shape) if shape else ""


def format_param_count(count):
    """Format parameter count as human-readable (e.g., 1.7M, 5.4B)
    
    Args:
        count: Number of parameters
        
    Returns:
        str: Formatted parameter count with K, M, or B suffix
    """
    if count < 1000:
        return f"{count}"
    elif count < 1_000_000:
        return f"{count/1000:.1f}K"
    elif count < 1_000_000_000:
        return f"{count/1_000_000:.1f}M"
    else:
        return f"{count/1_000_000_000:.1f}B"


def format_time(seconds):
    """Format time duration in a human-readable format
    
    Args:
        seconds: Time in seconds
        
    Returns:
        str: Formatted time with appropriate units (ns, μs, ms, s, min)
    """
    if seconds < 1e-6:  # Less than 1 microsecond
        # Show nanoseconds for very small times
        ns = seconds * 1e9
        return f"{ns:.1f}ns"
    elif seconds < 1e-3:  # Less than 1 millisecond
        # Show microseconds
        us = seconds * 1e6
        return f"{us:.2f}μs"
    elif seconds < 1.0:  # Less than 1 second
        # Show milliseconds
        ms = seconds * 1e3
        return f"{ms:.2f}ms"
    elif seconds < 60.0:  # Less than 1 minute
        # Show seconds with higher precision for smaller values
        if seconds < 10.0:
            return f"{seconds:.4f}s"
        else:
            return f"{seconds:.2f}s"
    else:  # Minutes or more
        minutes = seconds / 60.0
        if minutes < 60.0:  # Less than 1 hour
            return f"{minutes:.1f}min"
        else:
            hours = minutes / 60.0
            return f"{hours:.1f}h"


def format_percentage(percent, fixed_width=True):
    """Format a percentage value with fixed width
    
    Args:
        percent: Percentage value (0-100)
        fixed_width: Whether to use fixed width format (3 characters)
        
    Returns:
        str: Formatted percentage with fixed width
    """
    # Handle zero or very small values
    if percent <= 0:
        return " 0%" if fixed_width else "0%"
    
    # Also treat very small percentages as 0%
    if percent < 1:
        return " 0%" if fixed_width else "0%"
    
    # Format based on value range, ensuring consistent width
    if percent < 10:
        # Single digit with leading space
        return f" {int(percent)}%" if fixed_width else f"{int(percent)}%"
    elif percent < 100:
        # Double digit
        return f"{int(percent)}%" if fixed_width else f"{int(percent)}%"
    else:
        # 100% or higher
        return "100%" if fixed_width else "100%"
        
        
def make_transparent_if_equal(text, color, self_value, total_value, opacity=80):
    """Apply visual indicator if self_value equals total_value
    
    Args:
        text: The text to potentially modify
        color: The color to use (in hex format like "#ff0000")
        self_value: The self value to compare
        total_value: The total value to compare against
        opacity: The opacity level (0-100) to use if values are equal (not currently used)
        
    Returns:
        str: Text with visual indicator if values are equal, original text otherwise
    """
    if self_value == total_value and total_value > 0:
        # Since transparency might not be visible, use a dim style for leaf modules
        return f"[dim][{color}]{text}[/{color}][/dim]"
    else:
        return f"[{color}]{text}[/{color}]"


def get_torch_dtype_size(dtype):
    """Get the size in bytes of a torch dtype.
    
    Args:
        dtype: PyTorch data type
        
    Returns:
        int: Size in bytes of each element with the given dtype
    """
    if dtype == torch.float32:
        return 4
    elif dtype == torch.float16 or dtype == torch.bfloat16:
        return 2
    elif dtype == torch.int64 or dtype == torch.double:
        return 8
    elif dtype == torch.int32 or dtype == torch.float:
        return 4
    elif dtype == torch.int16:
        return 2
    elif dtype == torch.int8 or dtype == torch.uint8 or dtype == torch.bool:
        return 1
    else:
        # Default fallback, most common case is float32 (4 bytes)
        return 4


def format_torch_dtype(dtype):
    """Format torch dtype to a clean string without the torch. prefix
    
    Args:
        dtype: PyTorch data type
        
    Returns:
        str: Clean string representation of the dtype
    """
    # Convert to string and remove torch. prefix if present
    dtype_str = str(dtype)
    if "torch." in dtype_str:
        return dtype_str.split("torch.")[-1]
    return dtype_str


def get_module_param_attr(module, attr):
    """General function to get a parameter attribute from a module
    
    Args:
        module: PyTorch module to check
        attr: Name of the attribute to extract from parameters
        
    Returns:
        str: Formatted attribute value, or empty string if not available
    """
    if not module:
        return ""
        
    try:
        # First check if module has the attribute directly
        if hasattr(module, attr):
            attr_value = getattr(module, attr)
            # For device attribute, return as string
            if attr == 'device':
                return str(attr_value)
            # For dtype and other attributes, format as needed
            return format_torch_dtype(attr_value)
        
        # If no direct attribute, check parameters
        attr_values = set()
        
        # Check all parameters
        for param in module.parameters():
            if hasattr(param, attr):
                # For device, just get the string representation
                if attr == 'device':
                    attr_values.add(str(getattr(param, attr)))
                else: 
                    attr_values.add(str(getattr(param, attr)))

        # If we found values, format them appropriately
        if len(attr_values) == 1:
            value = attr_values.pop()
            # For device, return directly
            if attr == 'device':
                return value
            # For other attributes, format as torch dtype
            return format_torch_dtype(value)
        elif len(attr_values) > 1:
            # For device, use the format_devices helper
            if attr == 'device':
                return format_devices(attr_values)
            # For other attributes, show as mixed
            return f"(mixed {attr}s)"
        
    except Exception as e:
        # If any error occurs, don't show anything
        return f"(error getting {attr})"

def get_module_dtype(module):
    """Determine the dtype of a PyTorch module
    
    Args:
        module: PyTorch module to check
        
    Returns:
        str: Formatted dtype string, "(mixed dtypes)", or empty string if no params
    """
    return get_module_param_attr(module, 'dtype')


def basic_syntax_highlighting(text, default_style=""):
    """Apply basic Python syntax highlighting to text using rich markup
    
    Args:
        text: Text to highlight
        default_style: Base style to apply to non-highlighted parts (optional)
        
    Returns:
        str: Text with rich markup for syntax highlighting
    """
    import re
    
    # Save the passed text
    original_text = text
    
    # Skip highlighting if empty
    if not text:
        return text
    
    try:
        # Add base style if provided
        if default_style:
            base_open = f"[{default_style}]"
            base_close = f"[/{default_style}]"
            text = f"{base_open}{text}{base_close}"
        
        # Highlight numbers in green (including scientific notation like 1e-05)
        text = re.sub(r'(\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?)', r'[#66cc66]\1[/#66cc66]', text)
        
        # Highlight True, False, and None in blue
        text = re.sub(r'\b(True|False|None)\b', r'[#6699ff]\1[/#6699ff]', text)
        
        # Highlight strings in orange
        text = re.sub(r'(\'[^\']*\')', r'[#ff9966]\1[/#ff9966]', text)
        text = re.sub(r'(\"[^\"]*\")', r'[#ff9966]\1[/#ff9966]', text)
        
        return text
    except Exception:
        # If any error occurs during highlighting, return the original text
        # with the default style if provided
        if default_style:
            return f"[{default_style}]{original_text}[/{default_style}]"
        return original_text


def has_forward_stats(module_node):
    """Check if a module node has valid forward stats
    
    Args:
        module_node: The module node to check
        
    Returns:
        bool: True if the node has forward stats, False otherwise
    """
    # Extra check to debug why some modules might not show forward stats
    if module_node.module and hasattr(module_node.module, "forward_stats"):
        # If we have a module and forward_stats attribute, but it evaluates to False,
        # it could be an empty list or None
        stats = module_node.module.forward_stats
        return bool(stats)  # Convert to bool to handle empty lists, None, etc.
    
    return False


def get_latest_forward_stats(module_node):
    """Get the most recent forward stats for a module if they exist
    
    Args:
        module_node: The module node to check
        
    Returns:
        object: The most recent forward stats or None if unavailable
    """
    if has_forward_stats(module_node):
        return module_node.module.forward_stats[-1]
    return None

def get_total_runtime(module_node):
    """Get the sum of all runtimes across all forward passes
    
    Args:
        module_node: The module node to check
        
    Returns:
        float: Total runtime in seconds across all recorded passes
    """
    if has_forward_stats(module_node):
        total = 0.0
        # Sum up runtime from all recorded stats
        for stats in module_node.module.forward_stats:
            if hasattr(stats, "runtime"):
                total += stats.runtime
        return total
    return 0.0


def calculate_tensor_memory_size(tensor):
    """Calculate memory size of a tensor in bytes
    
    Args:
        tensor: PyTorch tensor
        
    Returns:
        int: Memory size in bytes
    """
    return tensor.numel() * get_torch_dtype_size(tensor.dtype)


def calculate_memory_from_shape(shape, dtype):
    """Calculate memory size in bytes from shape and dtype
    
    Args:
        shape: Tuple of dimensions
        dtype: PyTorch data type
        
    Returns:
        int: Memory size in bytes
    """
    # Calculate number of elements from shape
    if not shape:
        return 0
        
    num_elements = 1
    for dim in shape:
        num_elements *= dim
        
    # Get bytes per element based on dtype
    bytes_per_element = get_torch_dtype_size(dtype)
    
    # Return total size
    return num_elements * bytes_per_element


def extract_tensor_dtype(tensor_or_container, prefix="dtype"):
    """Extract dtype from a tensor or the first tensor in a container
    
    Args:
        tensor_or_container: PyTorch tensor or container of tensors
        prefix: Prefix to use in the formatted output (default: "dtype")
        
    Returns:
        str: Formatted dtype string or empty string if no tensor found
    """
    try:
        if isinstance(tensor_or_container, torch.Tensor):
            return f"{prefix}={format_torch_dtype(tensor_or_container.dtype)}"
        elif isinstance(tensor_or_container, (list, tuple)) and len(tensor_or_container) > 0:
            for item in tensor_or_container:
                if isinstance(item, torch.Tensor):
                    return f"{prefix}={format_torch_dtype(item.dtype)}"
    except:
        pass
    return ""


class NodeLabelComponent:
    """Base class for node label components"""
    # Default component metadata - to be overridden by subclasses
    display_name = "Base Component"
    description = "Base component description"
    example = "example"  # Example text to show in the label manager
    shortcut_key = None  # Keyboard shortcut (if any)
    style = ""  # Default style (empty)
    prefix = ""  # Text before styled content
    suffix = " "  # Text after styled content (default: space)
    
    def __init__(self, active=True):
        self.active = active
        # Initialize a storage for component-specific data
        self._cached_data = {}
        
    def toggle_active(self):
        """Toggle the active state of this component"""
        self.active = not self.active
        return self.active
        
    def get_label(self, module_node):
        """Get this component's contribution to the node label, if active"""
        if not self.active:
            return ""
        text = self._get_text(module_node)
        if not text:
            return ""
        if not self.style:
            return f"{self.prefix}{text}{self.suffix}"
        return f"{self.prefix}[{self.style}]{text}[/{self.style}]{self.suffix}"
    
    def get_width(self, module_node):
        """Get the display width of this component's contribution"""
        if not self.active:
            return 0
        text = self._get_text(module_node)
        if not text:
            return 0
        # Return the length of the plain text (without style markup) plus prefix and suffix
        return len(self.prefix) + len(text) + len(self.suffix)
        
    def _get_text(self, module_node):
        """Get the plain text content (to be overridden)"""
        raise NotImplementedError("Subclasses must implement _get_text")


class DeviceLabelComponent(NodeLabelComponent):
    """Component for displaying device information"""
    display_name = "Device Information"
    description = "Shows which device (CPU/GPU) the module is on"
    example = "cuda:0"
    shortcut_key = "d"
    style = "bold #9966ff"  # Purple
    
    def _get_text(self, module_node):
        """Get the device information using our helper function"""
        if not module_node.module:
            return ""
        
        # Use the new helper function that properly handles device attributes
        return get_module_device(module_node.module)


class SizeLabelComponent(NodeLabelComponent):
    """Component for displaying module size"""
    display_name = "Parameters Memory"
    description = "Shows the total memory size of the module's parameters"
    example = "1.2MB"
    shortcut_key = "m"  # Changed from 'b' to 'm'
    style = "#44cc88"  # Green-teal (not bold)
    
    def _get_text(self, module_node):
        if module_node.size_bytes > 0:
            # Format the memory size
            return rp.human_readable_file_size(module_node.size_bytes)
        return ""


class MemoryPercentComponent(NodeLabelComponent):
    """Component for displaying memory percentage relative to parent"""
    display_name = "Memory Percentage"
    description = "Shows what percentage of the parent module's memory this module uses"
    example = "45%"
    shortcut_key = "m"  # Same as SizeLabelComponent
    style = "#33aa66"  # Slightly darker green
    suffix = " "
    
    def _get_text(self, module_node):
        # Only calculate if we have a module with memory usage
        if not module_node.module or not hasattr(module_node, 'size_bytes') or module_node.size_bytes <= 0:
            return ""
            
        # Get the parent module using ModelTreeViewer.parent_map
        parent_module = ModelTreeViewer.parent_map.get(module_node.module)
        if not parent_module:
            return ""
            
        # Calculate parent's memory size
        parent_size_bytes = 0
        try:
            for param in parent_module.parameters():
                parent_size_bytes += calculate_tensor_memory_size(param)
        except Exception:
            return ""
        
        # Only show percentage if parent has memory usage
        if parent_size_bytes > 0:
            percent = (module_node.size_bytes / parent_size_bytes) * 100
            return format_percentage(percent)
        return ""
        
        
class SelfMemoryComponent(NodeLabelComponent):
    """Component for displaying self memory usage (excluding children)"""
    display_name = "Self Memory"
    description = "Shows the memory used by this module's parameters only (excluding children) - toggle with 'm' key"
    example = "self=1.2MB 45%"
    shortcut_key = "m"  # Same as SizeLabelComponent
    style = "#33bb77"  # Slightly darker green (not bold)
    
    def get_label(self, module_node):
        """Override get_label to use custom styling"""
        if not self.active:
            return ""
        text = self._get_text(module_node)
        if not text:
            return ""
        
        # Calculate own memory usage (excluding children)
        self_memory_bytes = 0
        try:
            # Get parameters directly owned by this module
            for param in module_node.module._parameters.values():
                if param is not None:
                    # Calculate memory for this parameter
                    self_memory_bytes += calculate_tensor_memory_size(param)
        except Exception:
            # If there's an error, return empty
            return ""
            
        # Compare with total memory
        total_memory_bytes = module_node.size_bytes if hasattr(module_node, 'size_bytes') else 0
        
        # Use our helper for styling
        return self.prefix + make_transparent_if_equal(text, self.style, self_memory_bytes, total_memory_bytes) + self.suffix
    
    def _get_text(self, module_node):
        if not module_node.module:
            return ""
            
        # Calculate own memory usage (excluding children)
        self_memory_bytes = 0
        try:
            # Get parameters directly owned by this module
            for param in module_node.module._parameters.values():
                if param is not None:
                    # Calculate memory for this parameter
                    self_memory_bytes += calculate_tensor_memory_size(param)
        except Exception:
            # If there's an error, return empty
            return ""
            
        # Only show if we have memory usage
        if self_memory_bytes > 0:
            # Calculate percentage of total memory
            total_memory_bytes = module_node.size_bytes if hasattr(module_node, 'size_bytes') else 0
            
            # Add percentage if total memory is available
            if total_memory_bytes > 0:
                percent = (self_memory_bytes / total_memory_bytes) * 100
                return f"self={rp.human_readable_file_size(self_memory_bytes)} {format_percentage(percent)}"
            else:
                return f"self={rp.human_readable_file_size(self_memory_bytes)}"
                
        return ""


class ForwardStatsComponent(NodeLabelComponent):
    """Base class for all forward stats components"""
    display_name = "Forward Statistics"
    description = "Base class for components showing forward pass statistics"
    example = "Stats"
    shortcut_key = "f"
    style = "bold #ffcc00"  # Golden yellow


class ForwardInputShapeComponent(ForwardStatsComponent):
    """Component for displaying forward pass input shape"""
    display_name = "Input Shape"
    description = "Shows the shape of input tensors passing through this module"
    example = "in=2×320×64×64"
    shortcut_key = "f"
    style = "italic #eecc00"  # Slightly darker yellow for input (italic)
    
    def _get_text(self, module_node):
        stats = get_latest_forward_stats(module_node)
        if not stats:
            return ""
            
        # Add input shape if available
        if hasattr(stats, "in_shape"):
            input_shape_str = format_shape(stats.in_shape)
            return f"in={input_shape_str}"
        return ""


class ForwardInputMemorySizeComponent(ForwardStatsComponent):
    """Component for displaying input tensor memory size"""
    display_name = "Input Memory Size"
    description = "Shows the memory size of input tensors passing through this module"
    example = "in_mem=1.2MB"
    shortcut_key = "m"  # Use 'm' for all memory components
    style = "italic #ccaa33"  # Darker yellow for input memory (italic)
    
    def _get_text(self, module_node):
        try:
            stats = get_latest_forward_stats(module_node)
            if not stats:
                return ""
                
            total_size = 0
            dtype = None
                
            # Method 1: Calculate from actual tensor if available
            if hasattr(stats, "in_tensor") and stats.in_tensor is not None:
                if isinstance(stats.in_tensor, torch.Tensor):
                    total_size = calculate_tensor_memory_size(stats.in_tensor)
                    dtype = stats.in_tensor.dtype
                elif isinstance(stats.in_tensor, (list, tuple)) and len(stats.in_tensor) > 0:
                    # Handle case where input is a list/tuple of tensors
                    for item in stats.in_tensor:
                        if isinstance(item, torch.Tensor):
                            total_size += calculate_tensor_memory_size(item)
                            if dtype is None:
                                dtype = item.dtype
            
            # Method 2: Calculate from shape and dtype if available
            if total_size == 0 and hasattr(stats, "in_shape") and stats.in_shape:
                # Try to find dtype - default to float32 if not found
                if not dtype:
                    if hasattr(stats, "in_dtype"):
                        dtype = stats.in_dtype
                    else:
                        # Default to float32 if no dtype info available
                        import torch
                        dtype = torch.float32
                        
                # Calculate from shape
                total_size = calculate_memory_from_shape(stats.in_shape, dtype)
                
            # Return formatted size if we calculated something
            if total_size > 0:
                return f"in_mem={rp.human_readable_file_size(total_size)}"
                
            return ""
        except Exception as e:
            # If any error occurs, display it
            return f"in_mem_err: {str(e)}"


class ForwardOutputShapeComponent(ForwardStatsComponent):
    """Component for displaying forward pass output shape"""
    display_name = "Output Shape"
    description = "Shows the shape of output tensors produced by this module"
    example = "out=2×320×64×64"
    shortcut_key = "f"
    style = "#ddbb00"  # Slightly darker yellow for output (not italic)
    
    def _get_text(self, module_node):
        stats = get_latest_forward_stats(module_node)
        if not stats:
            return ""
            
        # Add output shape if available
        if hasattr(stats, "out_shape"):
            output_shape_str = format_shape(stats.out_shape)
            return f"out={output_shape_str}"
        return ""


class ForwardOutputMemorySizeComponent(ForwardStatsComponent):
    """Component for displaying output tensor memory size"""
    display_name = "Output Memory Size"
    description = "Shows the memory size of output tensors produced by this module"
    example = "out_mem=1.2MB"
    shortcut_key = "m"  # Use 'm' for all memory components
    style = "#bbaa33"  # Darker yellow for output memory (not italic)
    
    def _get_text(self, module_node):
        try:
            stats = get_latest_forward_stats(module_node)
            if not stats:
                return ""
                
            total_size = 0
            dtype = None
                
            # Method 1: Calculate from actual tensor if available
            if hasattr(stats, "out_tensor") and stats.out_tensor is not None:
                if isinstance(stats.out_tensor, torch.Tensor):
                    total_size = calculate_tensor_memory_size(stats.out_tensor)
                    dtype = stats.out_tensor.dtype
                elif isinstance(stats.out_tensor, (list, tuple)) and len(stats.out_tensor) > 0:
                    # Handle case where output is a list/tuple of tensors
                    for item in stats.out_tensor:
                        if isinstance(item, torch.Tensor):
                            total_size += calculate_tensor_memory_size(item)
                            if dtype is None:
                                dtype = item.dtype
            
            # Method 2: Calculate from shape and dtype if available
            if total_size == 0 and hasattr(stats, "out_shape") and stats.out_shape:
                # Try to find dtype - default to float32 if not found
                if not dtype:
                    if hasattr(stats, "out_dtype"):
                        dtype = stats.out_dtype
                    else:
                        # Default to float32 if no dtype info available
                        import torch
                        dtype = torch.float32
                        
                # Calculate from shape
                total_size = calculate_memory_from_shape(stats.out_shape, dtype)
                
            # Return formatted size if we calculated something
            if total_size > 0:
                return f"out_mem={rp.human_readable_file_size(total_size)}"
                
            return ""
        except Exception as e:
            # If any error occurs, display it
            return f"out_mem_err: {str(e)}"


class ForwardCallCountComponent(ForwardStatsComponent):
    """Component for displaying forward pass call count"""
    display_name = "Call Count"
    description = "Shows how many times this module has been called"
    example = "(5 calls)"
    shortcut_key = "f"
    style = "italic #ffaa00"  # Amber yellow for call count (italic, not bold)
    
    def _get_text(self, module_node):
        if has_forward_stats(module_node):
            # Always include call count, even if just one call
            calls = len(module_node.module.forward_stats)
            suffix = "call" if calls == 1 else "calls"
            return f"({calls} {suffix})"
        return ""


class ForwardRuntimeComponent(ForwardStatsComponent):
    """Component for displaying self runtime of forward pass"""
    display_name = "Total Self Runtime"
    description = "Shows the cumulative runtime of this module alone, not including children, across all forward passes"
    example = "self=0.0123s 35%"
    shortcut_key = "r"  # Use 'r' for all runtime components
    style = "bold #ff9966"  # Orange for runtime
    
    def _get_text(self, module_node):
        # Get sum of all runtimes
        self_runtime = get_total_runtime(module_node)
        if self_runtime <= 0:
            return ""
            
        # Only show if significant (more than 1 microsecond)
        if self_runtime < 0.000001:
            return ""
            
        # Calculate percentage of total runtime
        if module_node.module:
            # Calculate total runtime (including children)
            module_total_runtime = get_module_total_runtime(module_node.module)
            
            # Add percentage if total runtime is available and significant
            if module_total_runtime > 0.000001:
                percent = (self_runtime / module_total_runtime) * 100
                return f"self={format_time(self_runtime)} {format_percentage(percent)}"
        
        # Default case without percentage
        return f"self={format_time(self_runtime)}"


class AvgSelfRuntimeComponent(ForwardStatsComponent):
    """Component for displaying average self runtime per call"""
    display_name = "Average Self Runtime"
    description = "Shows the average runtime of this module alone, not including children, per forward pass"
    example = "avg=1.5ms"
    shortcut_key = "r"  # Use 'r' for all runtime components
    style = "bold #ff8855"  # Lighter orange for avg runtime
    
    def _get_text(self, module_node):
        # Get total runtime
        total_runtime = get_total_runtime(module_node)
        if total_runtime <= 0:
            return ""
            
        # Get number of calls
        if not has_forward_stats(module_node):
            return ""
            
        call_count = len(module_node.module.forward_stats)
        if call_count <= 0:
            return ""
            
        # Calculate average runtime
        avg_runtime = total_runtime / call_count
        
        # Only show if significant (more than 1 microsecond)
        if avg_runtime < 0.000001:
            return ""
            
        # Format the result
        return f"avg={format_time(avg_runtime)}"


def get_module_total_runtime(module):
    """Helper function to calculate total runtime for a module and its children recursively
    
    Args:
        module: The PyTorch module to calculate runtime for
        
    Returns:
        float: Total runtime in seconds
    """
    if not module:
        return 0.0
        
    # Start with own runtime
    total = 0.0
    if hasattr(module, "forward_stats") and module.forward_stats:
        # Sum up runtime from all stats records
        for stats in module.forward_stats:
            if hasattr(stats, "runtime"):
                total += stats.runtime
    
    # Add runtime from all children recursively
    for child_name, child_module in module._modules.items():
        if child_module is not None:
            total += get_module_total_runtime(child_module)
            
    return total


class TotalRuntimeComponent(ForwardStatsComponent):
    """Component for displaying total runtime including children"""
    display_name = "Total Runtime"
    description = "Shows the total runtime spent in this module and all its children"
    example = "123ms"
    shortcut_key = "r"  # Use 'r' for all runtime components
    style = "bold #ff6633"  # Darker orange for total runtime
    
    def _get_text(self, module_node):
        if not module_node.module:
            return ""
            
        # Use cached value if available
        node_id = id(module_node.module)
        if node_id in self._cached_data:
            return self._cached_data[node_id]
            
        # Calculate runtime for this module and its children using the helper function
        this_runtime = get_module_total_runtime(module_node.module)
        
        # Skip if runtime is too small
        if this_runtime <= 0.000001:  # Skip if less than 1 microsecond
            return ""
            
        # Format time
        time_str = format_time(this_runtime)
        
        # Format and cache the result
        formatted = f"{time_str}"
        self._cached_data[node_id] = formatted
        return formatted


class RuntimePercentComponent(ForwardStatsComponent):
    """Component for displaying runtime percentage relative to parent"""
    display_name = "Runtime Percentage"
    description = "Shows what percentage of the parent module's runtime this module takes"
    example = "35%"
    shortcut_key = "r"  # Same as other runtime components
    style = "bold #dd5522"  # Similar orange as TotalRuntimeComponent but slightly different
    
    def _get_text(self, module_node):
        if not module_node.module:
            return ""
            
        # Use cached value if available
        node_id = id(module_node.module)
        if node_id in self._cached_data:
            return self._cached_data[node_id]
            
        # Calculate runtime for this module
        this_runtime = get_module_total_runtime(module_node.module)
        
        # Skip if runtime is too small
        if this_runtime <= 0.000001:  # Skip if less than 1 microsecond
            return ""
            
        # Get the parent module using ModelTreeViewer.parent_map
        parent_module = ModelTreeViewer.parent_map.get(module_node.module)
        if not parent_module:
            return ""
            
        # Calculate parent's total runtime
        parent_runtime = get_module_total_runtime(parent_module)
        
        # Only show percentage if parent has runtime
        if parent_runtime > 0.000001:  # More than 1 microsecond
            percent = (this_runtime / parent_runtime) * 100
            formatted = format_percentage(percent)
            self._cached_data[node_id] = formatted
            return formatted
            
        return ""


class AvgTotalRuntimeComponent(ForwardStatsComponent):
    """Component for displaying average total runtime per call"""
    display_name = "Average Total Runtime"
    description = "Shows the average total runtime of this module and all its children per forward pass"
    example = "avg=3.2ms"
    shortcut_key = "r"  # Use 'r' for all runtime components
    style = "bold #ff4422"  # Even darker orange for avg total runtime
    
    def _get_text(self, module_node):
        if not module_node.module or not has_forward_stats(module_node):
            return ""
            
        # Get number of calls
        call_count = len(module_node.module.forward_stats)
        if call_count <= 0:
            return ""
            
        # Use cached value if available
        node_id = id(module_node.module)
        if node_id in self._cached_data:
            return self._cached_data[node_id]
        
        # Use the shared helper function to calculate total runtime
        total_runtime = get_module_total_runtime(module_node.module)
            
        # Skip if runtime is too small
        if total_runtime < 0.000001:
            return ""
            
        # Calculate average
        avg_runtime = total_runtime / call_count
        
        # Format the result
        formatted = f"avg={format_time(avg_runtime)}"
        self._cached_data[node_id] = formatted
        return formatted
    
    def _find_tree_from_node(self, module_node):
        """Find the tree this node belongs to"""
        # Access app directly
        app = self._get_app()
        if not app:
            return None
            
        # Try to find the tree
        try:
            tree = app.query_one("#tree-pane > Tree")
            return tree
        except:
            return None
            
    def _get_app(self):
        """Get the Textual app instance"""
        # This is a bit of a hack but should work
        import textual.app
        try:
            return textual.app.App.get_running_app()
        except:
            return None
    
    def _get_total_runtime_recursively(self, module):
        """Calculate the total runtime of this module and all its children recursively"""
        if not module:
            return 0.0
            
        # Start with own runtime
        total = 0.0
        if hasattr(module, "forward_stats") and module.forward_stats:
            # Sum up runtime from all stats records
            for stats in module.forward_stats:
                if hasattr(stats, "runtime"):
                    total += stats.runtime
        
        # Add runtime from all children recursively
        for child_name, child_module in module._modules.items():
            if child_module is not None:
                total += self._get_total_runtime_recursively(child_module)
                
        return total


class ModuleNameComponent(NodeLabelComponent):
    """Component for displaying the module name"""
    display_name = "Module Name"
    description = "Shows the module's name"
    example = "(conv_in)"
    shortcut_key = None  # Always on, no toggle
    style = "bold #ff66aa"  # Pink
    suffix = ": "
    
    def __init__(self):
        # Module name is always active - it's the primary identifier
        super().__init__(active=True)
        
    def toggle_active(self):
        """Module name can't be toggled off"""
        return True
        
    def _get_text(self, module_node):
        if module_node.name:
            return f"({module_node.name})"
        return ""


class ModuleTypeBaseComponent(NodeLabelComponent):
    """Base class for module type components"""
    display_name = "Module Args"
    description = "Shows the module's class name and constructor args"
    example = "Conv2d(320, 4, kernel_size=3)"
    shortcut_key = None
    
    def __init__(self):
        # Module type components are always active
        super().__init__(active=True)
        
    def toggle_active(self):
        """Module type can't be toggled off"""
        return True


class ModuleTypeNameComponent(ModuleTypeBaseComponent):
    """Component for displaying the module class name"""
    style = "bold #00aaff"  # Bold bright blue
    suffix = ""  # No space between type name and args
    
    def _get_text(self, module_node):
        return module_node.module_type


class ModuleTypeArgsComponent(ModuleTypeBaseComponent):
    """Component for displaying the module arguments"""
    style = "italic #0088cc"  # Base style for non-highlighted parts
    
    def __init__(self):
        super().__init__()
        # Store the highlighted version of the last args string for display
        self._highlighted_args = {}  # Dictionary: module_node -> highlighted args
    
    def _get_text(self, module_node):
        if not module_node.extra_info:
            return ""
        
        # For width calculation, always return plain text
        # This ensures proper alignment even with markup
        plain_text = f"({module_node.extra_info})"
        
        # Calculate the highlighted version for display
        highlighted = self._highlight_args(module_node.extra_info)
        
        # Store the highlighted version for get_label to use
        self._highlighted_args[module_node] = f"({highlighted})"
        
        # For get_width calculations, return the plain text
        # This ensures proper width calculation for alignment
        return plain_text
        
    def get_label(self, module_node):
        """Override get_label to use highlighted version after width calc"""
        if not self.active:
            return ""
            
        # Get the plain text first (triggers _get_text)
        plain = self._get_text(module_node)
        if not plain:
            return ""
            
        # Get the highlighted version that was stored
        highlighted = self._highlighted_args.get(module_node, plain)
        
        # Use the highlighted version for display but original for width
        return f"{self.prefix}[{self.style}]{highlighted}[/{self.style}]{self.suffix}"
    
    def _highlight_args(self, args_text):
        """Highlight arguments with distinct colors"""
        import re
        
        # Process the string character by character
        pos = 0
        result = ""
        
        # Define patterns
        param_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)='  # Parameter names like in_features=
        number_pattern = r'(\d+\.?\d*(?:[eE][-+]?\d+)?)'  # Numbers like 1280 or 1e-5
        bool_pattern = r'\b(True|False|None)\b'  # Boolean values
        
        while pos < len(args_text):
            # Check for parameter names
            param_match = re.match(param_pattern, args_text[pos:])
            if param_match:
                # Parameter name in default blue
                result += param_match.group(1) + "="
                pos += len(param_match.group())
                continue
                
            # Check for numbers - use a blue-green like before
            number_match = re.match(number_pattern, args_text[pos:])
            if number_match:
                result += f"[#55aacc]{number_match.group(1)}[/#55aacc]"
                pos += len(number_match.group())
                continue
                
            # Check for booleans - use bright blue like before
            bool_match = re.match(bool_pattern, args_text[pos:])
            if bool_match:
                result += f"[#6699ff]{bool_match.group(1)}[/#6699ff]"
                pos += len(bool_match.group())
                continue
                
            # Default - add character as is
            result += args_text[pos]
            pos += 1
            
        return result


class ParamShapesComponent(NodeLabelComponent):
    """Component for displaying parameter shapes"""
    display_name = "Parameter Shapes"
    description = "Shows the shapes of module parameters like weight and bias tensors"
    example = "weight: 4×320×3×3, bias: 4"
    shortcut_key = "t"
    style = "italic #66dd33"  # Light green (italic instead of bold)
    prefix = " | "
    suffix = ""
    
    def _get_text(self, module_node):
        return module_node.state_dict_info if module_node.state_dict_info else ""


class ParamCountComponent(NodeLabelComponent):
    """Component for displaying parameter count"""
    display_name = "Parameter Count"
    description = "Shows the number of parameters in the module including all children"
    example = "1.7M"
    shortcut_key = "p"
    style = "#ff8c00"  # Dark orange (not bold)
    suffix = " "
    
    def _get_text(self, module_node):
        # Get parameter count from module_node's param_count property
        if hasattr(module_node, 'param_count') and module_node.param_count > 0:
            # Format the parameter count in a human-readable way
            return format_param_count(module_node.param_count)
        return ""


class ParamPercentComponent(NodeLabelComponent):
    """Component for displaying parameter percentage relative to parent"""
    display_name = "Parameter Percentage"
    description = "Shows what percentage of the parent module's parameters this module contains"
    example = "50%"
    shortcut_key = "p"  # Same as ParamCountComponent
    style = "#cc7000"  # Slightly darker orange
    suffix = " "
    
    def _get_text(self, module_node):
        # Only calculate if we have a module with parameters
        if not module_node.module or not hasattr(module_node, 'param_count') or module_node.param_count <= 0:
            return ""
            
        # Get the parent module using ModelTreeViewer.parent_map
        parent_module = ModelTreeViewer.parent_map.get(module_node.module)
        if not parent_module:
            return ""
            
        # Calculate parent's parameter count
        parent_param_count = 0
        try:
            for param in parent_module.parameters():
                parent_param_count += param.numel()
        except Exception:
            return ""
        
        # Only show percentage if parent has parameters
        if parent_param_count > 0:
            percent = (module_node.param_count / parent_param_count) * 100
            return format_percentage(percent)
        return ""
        
        
class SelfParamCountComponent(NodeLabelComponent):
    """Component for displaying self parameter count (excluding children)"""
    display_name = "Self Parameter Count"
    description = "Shows the number of parameters in this module only (excluding children) - toggle with 'p' key"
    example = "self=1.7M 50%"
    shortcut_key = "p"  # Same as ParamCountComponent
    style = "#ee7700"  # Slightly darker orange (not bold)
    
    def get_label(self, module_node):
        """Override get_label to use custom styling"""
        if not self.active:
            return ""
        text = self._get_text(module_node)
        if not text:
            return ""
        
        # Get total parameter count for comparison
        self_params = 0
        try:
            # Get parameters directly owned by this module
            for param in module_node.module._parameters.values():
                if param is not None:
                    self_params += param.numel()
        except Exception:
            # If there's an error, return empty
            return ""
            
        # Compare with total params
        total_params = module_node.param_count if hasattr(module_node, 'param_count') else 0
        
        # Use our helper for styling
        return self.prefix + make_transparent_if_equal(text, self.style, self_params, total_params) + self.suffix
    
    def _get_text(self, module_node):
        if not module_node.module:
            return ""
            
        # Calculate own parameters (excluding children)
        self_params = 0
        try:
            # Get parameters directly owned by this module
            for param in module_node.module._parameters.values():
                if param is not None:
                    self_params += param.numel()
        except Exception:
            # If there's an error, return empty
            return ""
            
        # Only show if we have parameters
        if self_params > 0:
            # Calculate percentage of total parameters
            total_params = module_node.param_count if hasattr(module_node, 'param_count') else 0
            
            # Add percentage if total params is available
            if total_params > 0:
                percent = (self_params / total_params) * 100
                return f"self={format_param_count(self_params)} {format_percentage(percent)}"
            else:
                return f"self={format_param_count(self_params)}"
                
        return ""


class OwnParamsComponent(NodeLabelComponent):
    """Component for displaying own parameter count (excluding children)"""
    display_name = "Own Params"
    description = "Shows the number of parameters in this module only (excluding children) - only displayed when different from total Parameter Count (which means the module has children with parameters)"
    example = "1.7M"
    shortcut_key = None  # No keyboard shortcut
    style = "bold yellow"
    suffix = " "
    
    def _get_text(self, module_node):
        if not module_node.module:
            return ""
            
        # Get total parameter count from module_node
        total_params = module_node.param_count if hasattr(module_node, 'param_count') else 0
        
        # Calculate own parameters (excluding children)
        own_params = 0
        try:
            # Get parameters directly owned by this module
            for param in module_node.module._parameters.values():
                if param is not None:
                    own_params += param.numel()
        except Exception:
            # If there's an error, return empty
            return ""
            
        # Only show if we have parameters AND it's different from total count
        # (which means this module has child modules with parameters)
        if own_params > 0 and own_params != total_params:
            return format_param_count(own_params)
        return ""


class OwnVRAMComponent(NodeLabelComponent):
    """Component for displaying own VRAM usage (excluding children)"""
    display_name = "Own VRAM"
    description = "Shows the memory used by this module's parameters only (excluding children) - only displayed when different from total memory usage (which means the module has children with parameters)"
    example = "1.2MB"
    shortcut_key = None  # No keyboard shortcut
    style = "bold green"
    suffix = " "
    
    def _get_text(self, module_node):
        if not module_node.module:
            return ""
            
        # Get total memory usage
        total_size_bytes = module_node.size_bytes if hasattr(module_node, 'size_bytes') else 0
            
        # Calculate own memory usage (excluding children)
        own_size_bytes = 0
        try:
            # Get parameters directly owned by this module
            for param in module_node.module._parameters.values():
                if param is not None:
                    # Use calculate_memory_from_shape for consistent behavior
                    own_size_bytes += calculate_memory_from_shape(param.shape, param.dtype)
        except Exception:
            # If there's an error, return empty
            return ""
            
        # Only show if we have memory usage AND it's different from total memory
        # (which means this module has child modules with parameters)
        if own_size_bytes > 0 and own_size_bytes != total_size_bytes:
            return rp.human_readable_file_size(own_size_bytes)
        return ""


class InputDTypeComponent(ForwardStatsComponent):
    """Component for displaying input tensor dtype"""
    display_name = "Input DType"
    description = "Shows the data type of input tensors passing through this module"
    example = "in_dtype=float32"
    shortcut_key = None  # No keyboard shortcut
    style = "cyan"
    
    def _get_text(self, module_node):
        stats = get_latest_forward_stats(module_node)
        if not stats:
            return ""
            
        # Add input dtype if available
        if hasattr(stats, "in_tensor") and stats.in_tensor is not None:
            return extract_tensor_dtype(stats.in_tensor, "in_dtype")
        return ""


class OutputDTypeComponent(ForwardStatsComponent):
    """Component for displaying output tensor dtype"""
    display_name = "Output DType"
    description = "Shows the data type of output tensors produced by this module"
    example = "out_dtype=float32"
    shortcut_key = None  # No keyboard shortcut
    style = "cyan"
    
    def _get_text(self, module_node):
        stats = get_latest_forward_stats(module_node)
        if not stats:
            return ""
            
        # Add output dtype if available
        if hasattr(stats, "out_tensor") and stats.out_tensor is not None:
            return extract_tensor_dtype(stats.out_tensor, "out_dtype")
        return ""


class ModuleDTypeComponent(NodeLabelComponent):
    """Component for displaying module dtype"""
    display_name = "DType"
    description = "Shows the dtype of the module's parameters (omitted if no parameters)"
    example = "float32"
    shortcut_key = "d"  # Share shortcut with DeviceLabelComponent
    style = "italic #33bbee"  # Bright blue-cyan in italic (not bold)
    
    def _get_text(self, module_node):
        if not module_node.module:
            return ""
            
        # Use the helper function to get the dtype
        return get_module_dtype(module_node.module)


class AlignmentComponent(NodeLabelComponent):
    """Component for aligning sibling nodes vertically"""
    display_name = "Alignment"
    description = "Aligns sibling nodes vertically by adding whitespace"
    example = ""
    shortcut_key = "A"
    prefix = ""
    suffix = ""
    
    def _get_text(self, module_node):
        """Alignment component is special - it returns padding to align with siblings"""
        # Actual alignment calculation is done in ModuleNode.get_label()
        # This just returns an empty string as the text itself
        return ""

from textual.app import App, ComposeResult
from textual.widgets import Tree, Footer, Static, Button, Switch, ListView, Label, ListItem, MarkdownViewer
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, Container, ScrollableContainer
from textual.widgets._text_area import TextArea
from textual.reactive import reactive
from textual._text_area_theme import TextAreaTheme
from textual.screen import ModalScreen
from typing import Dict, Optional, Any, List, Tuple
import torch
from rich.text import Text
from rich.pretty import Pretty
from rich.console import Console
from rich.style import Style
from io import StringIO
import inspect
import numpy as np
import os
import pathlib
import tempfile


class HJKLTree(Tree):
    """A Tree subclass that adds hjkl vim-style navigation"""
    
    BINDINGS = [
        # Add vim-style navigation
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("h", "cursor_left", "Left", show=False),
        Binding("l", "cursor_right", "Right", show=False),
    ]
            
    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """Handle node expansion"""
        # Store this node's path in global expanded state
        if event.node.data is not None:
            path = self.app.get_node_path(event.node)
            # Track this path as expanded
            if not hasattr(self.app, 'global_expanded_paths'):
                self.app.global_expanded_paths = set()
            self.app.global_expanded_paths.add(path)
            
        # When a node is expanded, post an event that the parent app can handle
        self.app.on_node_expanded(event.node)
    
    def on_tree_node_collapsed(self, event: Tree.NodeCollapsed) -> None:
        """Handle node collapse
        
        When a node is collapsed, we:
        1. Save the expansion state of all its children (which ones were expanded)
        2. Remove all children nodes to save memory
        3. Mark the node as not loaded so children will be recreated on expansion
        
        This approach optimizes memory usage while preserving the folding history,
        allowing us to restore the exact same expanded/collapsed state when a user
        expands this node again.
        """
        # Only process non-root nodes
        if event.node != self.root:
            # Remove this node from global expanded paths
            if event.node.data is not None:
                path = self.app.get_node_path(event.node)
                if hasattr(self.app, 'global_expanded_paths'):
                    if path in self.app.global_expanded_paths:
                        self.app.global_expanded_paths.remove(path)
                
            # Recursively track all expanded descendants before removing them
            if event.node.data is not None:
                # Define a function to collect all expanded nodes recursively
                def collect_expanded_paths(node):
                    expanded_children = set()
                    for child in node.children:
                        if child.data is not None:
                            child_path = self.app.get_node_path(child)
                            # If child is expanded, add its path and process its children
                            if child.is_expanded:
                                expanded_children.add(child_path)
                                # Store in app's global state
                                if not hasattr(self.app, 'global_expanded_paths'):
                                    self.app.global_expanded_paths = set()
                                self.app.global_expanded_paths.add(child_path)
                                # Recursively process expanded children
                                expanded_children.update(collect_expanded_paths(child))
                    return expanded_children
                
                # Save all expanded descendants in this node
                event.node.data.expanded_children = collect_expanded_paths(event.node)
                
            # Remove all children
            event.node.remove_children()
            
            # Mark as not loaded so it will be reloaded when expanded again
            if event.node.data is not None:
                event.node.data.loaded = False
    
    def walk_tree(self, node=None):
        """Walk through the tree recursively starting from node (or root if not specified).
        
        Args:
            node: The starting node (defaults to root)
            
        Yields:
            TreeNode: Each node in the tree
        """
        if node is None:
            node = self.root
            
        # Yield the node itself
        yield node
        
        # Recursively yield all children
        for child in node.children:
            yield from self.walk_tree(child)
        
    def action_cursor_right(self) -> None:
        """Handle right cursor movement (expand node or notify)."""
        node = self.cursor_node
        if node and not node.is_expanded and node.allow_expand:
            # Load and expand the node directly
            if node.data is not None and not node.data.loaded:
                module_entry = node.data
                children = self.app._get_module_children(module_entry.module)
                if children:
                    # Mark as loaded and populate
                    module_entry.loaded = True
                    self.app._populate_node_with_children(node, children, module_entry.module)
            # Expand the node
            node.expand()
        elif self.cursor_node:
            # Use default Tree behavior when appropriate
            if self.cursor_node.is_expanded:
                # Move to the first child if expanded
                if self.cursor_node.children:
                    self.select_node(self.cursor_node.children[0])
            elif self.cursor_node.allow_expand:
                # Expand if allowed
                self.cursor_node.expand()
            
    def action_cursor_left(self) -> None:
        """Handle left cursor movement (collapse node)."""
        node = self.cursor_node
        if node and node.is_expanded:
            # Collapse the node - this will trigger the on_tree_node_collapsed handler
            node.collapse()
        elif node and node.parent:
            # If not expanded but has a parent, move to parent
            self.select_node(node.parent)


class HJKLListView(ListView):
    """A ListView subclass that adds hjkl vim-style navigation"""
    
    BINDINGS = [
        # Add vim-style navigation
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        # Add toggle with space/enter
        Binding("space", "toggle_selected", "Toggle", show=False),
        Binding("enter", "toggle_selected", "Toggle", show=False),
        # Pass through panel keys
        Binding("a", "pass_through_a", "", show=False),
        Binding("i", "pass_through_i", "", show=False),
        # Add reordering with Shift+J and Shift+K
        Binding("J", "move_down", "Move Down", show=False),  # Shift+J
        Binding("K", "move_up", "Move Up", show=False),      # Shift+K
        # Add move to top/bottom with Shift+T and Shift+B
        Binding("T", "move_to_top", "Move to Top", show=False),  # Shift+T
        Binding("B", "move_to_bottom", "Move to Bottom", show=False),  # Shift+B
    ]
    
    CSS = """
    #move-up-button, #move-down-button {
        width: 3;
        height: 3;
        margin: 0;
        padding: 0;
        content-align: center middle;
    }
    """
    
    def action_toggle_selected(self) -> None:
        """Toggle the currently highlighted component"""
        # Get the currently highlighted item
        if self.highlighted_child is not None and isinstance(self.highlighted_child, ComponentListItem):
            # Activate the item's toggle method
            self.highlighted_child.toggle_switch()
            
    def action_pass_through_a(self) -> None:
        """Pass through 'a' key to toggle attributes panel"""
        # Get parent app and call its toggle_attrs_panel action
        self.app.action_toggle_attrs_panel()
        
    def action_pass_through_i(self) -> None:
        """Pass through 'i' key to toggle code panel"""
        # Get parent app and call its toggle_code_panel action
        self.app.action_toggle_code_panel()
        
    def action_move_up(self) -> None:
        """Move the currently highlighted component up in the list (Shift+K)"""
        if self.highlighted_child is not None and isinstance(self.highlighted_child, ComponentListItem):
            # Call the app's method to move the component up
            self.app.move_component_up(self.highlighted_child)
            
    def action_move_down(self) -> None:
        """Move the currently highlighted component down in the list (Shift+J)"""
        if self.highlighted_child is not None and isinstance(self.highlighted_child, ComponentListItem):
            # Call the app's method to move the component down
            self.app.move_component_down(self.highlighted_child)
            
    def action_move_to_top(self) -> None:
        """Move the currently highlighted component to the top of the list (Shift+T)"""
        if self.highlighted_child is not None and isinstance(self.highlighted_child, ComponentListItem):
            # Call the app's method to move the component to the top
            self.app.move_component_to_top(self.highlighted_child)
            
    def action_move_to_bottom(self) -> None:
        """Move the currently highlighted component to the bottom of the list (Shift+B)"""
        if self.highlighted_child is not None and isinstance(self.highlighted_child, ComponentListItem):
            # Call the app's method to move the component to the bottom
            self.app.move_component_to_bottom(self.highlighted_child)


class HelpScreen(ModalScreen):
    """Help screen with scrollable markdown documentation"""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Close", show=True),
        Binding("q", "app.pop_screen", "Close", show=False),
        Binding("enter", "app.pop_screen", "Close", show=False),
    ]
    
    CSS = """
    HelpScreen {
        align: center middle;
    }
    
    #help-container {
        width: 90%;
        height: 90%;
        background: #1a1a1a;
        border: solid #444444;
        padding: 0;
        margin: 2 4;
    }
    
    #help-title-bar {
        height: auto;
        background: #333333;
        color: #ffffff;
        border-bottom: solid #444444;
        layout: horizontal;
    }
    
    #help-title {
        width: 1fr;
        text-align: center;
        padding: 1;
        text-style: bold;
    }
    
    Button {
        margin: 1 2;
    }
    
    /* MarkdownViewer specifics */
    MarkdownViewer {
        background: #1a1a1a;
        color: #ffffff;
    }
    
    Horizontal > VerticalScroll {
        width: 24;
    }
    
    .markdown-body {
        color: #ffffff;
    }
    
    .header {
        margin: 1 0 0 2;
        text-style: bold;
    }
    
    #close-button {
        background: #992222;
        color: #ffffff;
        min-width: 9;
        width: 9;
        height: 3;
        content-align: center middle;
        text-style: bold;
    }
    
    #close-button:hover {
        background: #cc3333;
    }
    
    /* Ensure table of contents is visible */
    .markdown-navigation {
        background: #222222;
        color: #dddddd;
        padding: 1;
        border-right: solid #444444;
    }
    
    /* TOC links are styled separately */
    .toc-link {
        color: #dddddd;
    }
    
    .toc-link:hover {
        color: #ffffff;
        text-style: underline;
    }
    """
    
    # Define a fallback help text as a class attribute for guaranteed availability
    FALLBACK_HELP = """
# PyTorch Module Explorer

An interactive TUI for exploring PyTorch models

## Key Controls

### Navigation
- Arrow keys or hjkl: Navigate tree
- Space: Toggle node fold/unfold
- Enter: Expand selected node

### Display Options
- f: Toggle forward statistics (runtime tensor shapes, requires forward pass)
- t: Toggle parameter shapes 
- m: Toggle memory usage (both total and self-only memory)
- p: Toggle parameter counts (both total and self-only counts)
- d: Toggle device information
- r: Toggle runtime components
- A: Toggle node alignment

### Panels
- c: Toggle code panel
- a: Toggle attributes panel
- L: Toggle label customization
- <: Expand the rightmost sidepanel width
- >: Contract the rightmost sidepanel width

### Label Customization
- Space/Enter: Toggle the selected label component on/off
- Shift+J: Move the selected component down in the list
- Shift+K: Move the selected component up in the list
- Shift+T: Move the selected component to the top of the list
- Shift+B: Move the selected component to the bottom of the list

### Folding
- z: Fold/unfold the selected node and all its descendants
- Z: Fold/unfold all nodes in the entire tree
- s: Fold/unfold immediate sibling nodes (same level only)
- S: Fold/unfold all sibling nodes and their descendants
- o: Fold/unfold all nodes of the same class type globally
- O: Fold/unfold all nodes of the same class type and their descendants

Press ESC or Enter to close this help window.
"""

    def compose(self) -> ComposeResult:
        with Container(id="help-container"):
            with Horizontal(id="help-title-bar"):
                yield Static("RP: Explore Torch Module Documentation", id="help-title")
                yield Button("CLOSE", id="close-button")
            
            # Get the markdown content
            content = self._get_help_markdown()
            
            # Use MarkdownViewer with direct markdown content - no error handling,
            # if it fails then let it crash properly
            from textual.widgets import MarkdownViewer
            yield MarkdownViewer(markdown=content, show_table_of_contents=True)
    
    def on_button_pressed(self, event) -> None:
        """Handle button presses"""
        if event.button.id == "close-button":
            self.app.pop_screen()
            
    # Let Textual handle all the scrolling and clicking behavior natively
            
    # No on_mount needed - we're using a direct content approach in compose
            
    # Removed old method (replaced by _create_and_load_doc)
    
    # Use class variable to cache the help markdown content
    _help_markdown_content = None
    
    def _get_help_markdown(self):
        """Get the markdown help content (memoized)"""
        # Return cached content if we already loaded it
        if HelpScreen._help_markdown_content is not None:
            return HelpScreen._help_markdown_content
        
        # Simple approach: the file is in the same directory as this file
        module_dir = os.path.dirname(os.path.abspath(__file__))
        doc_path = os.path.join(module_dir, "pytorch_module_explorer_doc.md")
        
        # Read the file - let it crash if there's a problem
        with open(doc_path, 'r', encoding='utf-8') as f:
            HelpScreen._help_markdown_content = f.read()
            
        return HelpScreen._help_markdown_content




class AttributeTree:
    """Helper class to build and manage attribute trees"""
    
    def __init__(self, tree_widget: HJKLTree):
        """Initialize with a tree widget
        
        Args:
            tree_widget: The HJKLTree widget to populate
        """
        self.tree = tree_widget
    
    def clear(self):
        """Clear the tree"""
        self.tree.clear()
    
    def set_title(self, title: str):
        """Set the title of the tree
        
        Args:
            title: Title to display
        """
        self.tree.root.label = title
    
    def expand_root(self):
        """Expand the root node"""
        self.tree.root.expand()
    
    def is_simple_type(self, value):
        """Check if a value is a simple type (should be a leaf node)
        
        Args:
            value: The value to check
            
        Returns:
            bool: True if value is a simple type
        """
        return (value is None or 
                isinstance(value, (bool, int, float, str)) or
                (isinstance(value, (list, tuple)) and len(value) == 0) or
                (isinstance(value, dict) and len(value) == 0))
    
    def format_value(self, value):
        """Format a value for display in the attributes tree with Python syntax highlighting
        
        Args:
            value: The value to format
            
        Returns:
            str: Formatted value with rich markup for Python syntax highlighting
        """
        MAX_STR_LENGTH = 100  # Maximum length for string display
        
        try:
            if value is None:
                return "[blue bold]None[/blue bold]"  # Python None is typically blue
            elif isinstance(value, bool):
                return f"[blue bold]{value}[/blue bold]"  # Python booleans are typically blue like keywords
            elif isinstance(value, int):
                return f"[#b5cea8]{value}[/#b5cea8]"  # VS Code number color
            elif isinstance(value, float):
                return f"[#b5cea8]{value}[/#b5cea8]"  # VS Code number color
            elif isinstance(value, str):
                try:
                    if len(value) > MAX_STR_LENGTH:
                        truncated = value[:MAX_STR_LENGTH] + "..."
                        return f"[#ce9178]\"{truncated}\"[/#ce9178]"  # VS Code string color
                    else:
                        return f"[#ce9178]\"{value}\"[/#ce9178]"  # VS Code string color
                except Exception as e:
                    return f"[red]<Error accessing string: {str(e)}>[/red]"
            elif isinstance(value, (list, tuple)):
                try:
                    type_name = type(value).__name__
                    if len(value) > 5:
                        return f"[#4ec9b0]{type_name}[/#4ec9b0] [#dddddd]with {len(value)} items[/#dddddd]"
                    else:
                        # Format collection with proper Python syntax highlighting
                        if isinstance(value, list):
                            items = []
                            for item in value:
                                items.append(self.format_value(item))
                            return f"[#dddddd][[/#dddddd]{', '.join(items)}[#dddddd]][/#dddddd]"
                        elif isinstance(value, tuple):
                            items = []
                            for item in value:
                                items.append(self.format_value(item))
                            return f"[#dddddd]([/#dddddd]{', '.join(items)}[#dddddd])[/#dddddd]"
                except Exception as e:
                    return f"[#4ec9b0]{type(value).__name__}[/#4ec9b0] [red]<Error: {str(e)}>[/red]"
            elif isinstance(value, dict):
                try:
                    if len(value) == 0:
                        return "[#dddddd]{}[/#dddddd]"
                    return f"[#4ec9b0]dict[/#4ec9b0] [#dddddd]with {len(value)} keys[/#dddddd]"
                except Exception as e:
                    return f"[#4ec9b0]dict[/#4ec9b0] [red]<Error: {str(e)}>[/red]"
            elif isinstance(value, torch.Tensor):
                try:
                    shape_str = format_shape(value.shape)
                    return f"[#4ec9b0]Tensor[/#4ec9b0] [#dddddd]shape={shape_str}, dtype={value.dtype}[/#dddddd]"
                except Exception as e:
                    return f"[#4ec9b0]Tensor[/#4ec9b0] [red]<Error accessing properties: {str(e)}>[/red]"
            else:
                # For other types, use type color for class name
                return f"[#4ec9b0]{type(value).__name__}[/#4ec9b0]"
        except Exception as e:
            return f"[red]<Error formatting value: {str(e)}>[/red]"
    
    def add_attributes_recursively(self, parent_node, obj, max_depth=3, current_depth=0):
        """Recursively add attributes to a node
        
        Args:
            parent_node: The tree node to add attributes to
            obj: The object to extract attributes from
            max_depth: Maximum recursion depth to prevent infinite loops
            current_depth: Current recursion depth
        """
        if current_depth >= max_depth:
            parent_node.add("[dim][italic]... (max depth reached)[/dim][/italic]")
            return
            
        # Get all attributes that don't start with underscore
        attrs = {}
        try:
            if hasattr(obj, "__dict__") and obj.__dict__:
                # Add from __dict__ first (instance attributes)
                for name, value in obj.__dict__.items():
                    if not name.startswith('_') and not callable(value):
                        attrs[name] = value
            
            # Then add from dir() (includes properties, etc.)
            for name in dir(obj):
                if name not in attrs and not name.startswith('_'):
                    try:
                        value = getattr(obj, name)
                        # Skip methods and built-in functions
                        if not callable(value):
                            attrs[name] = value
                    except Exception as e:
                        attrs[name] = f"Error: {str(e)}"
        except Exception as e:
            parent_node.add(f"[red]<Error accessing attributes: {str(e)}>[/red]")
            return
        
        # Sort attributes by name
        for name in sorted(attrs.keys()):
            value = attrs[name]
            # Format attribute name in bold cyan (VS Code style for property names)
            node_label = f"[bold #569cd6]{name}[/bold #569cd6]: {self.format_value(value)}"
            
            # Check if this is a simple type (leaf node) or complex type (expandable)
            is_leaf = self.is_simple_type(value)
            
            # Add node to the parent
            attr_node = parent_node.add(node_label)
            
            # Set expandability based on type
            attr_node._allow_expand = not is_leaf
            
            # Only add children for complex types
            if not is_leaf:
                if isinstance(value, dict) and len(value) > 0:
                    for k, v in sorted(value.items()):
                        # Format dictionary keys also in bold cyan
                        key_str = str(k) if not isinstance(k, str) else k
                        child_label = f"[bold #569cd6]{key_str}[/bold #569cd6]: {self.format_value(v)}"
                        child_node = attr_node.add(child_label)
                        child_node._allow_expand = not self.is_simple_type(v)
                        
                        # Recursively add attributes if it's a complex type
                        if not self.is_simple_type(v):
                            self.add_attributes_recursively(child_node, v, max_depth, current_depth + 1)
                        
                elif isinstance(value, (list, tuple)) and len(value) > 0 and len(value) <= 20:
                    for i, item in enumerate(value):
                        # Format indices in bold number color
                        child_label = f"[bold #b5cea8]{i}[/bold #b5cea8]: {self.format_value(item)}"
                        child_node = attr_node.add(child_label)
                        child_node._allow_expand = not self.is_simple_type(item)
                        
                        # Recursively add attributes if it's a complex type
                        if not self.is_simple_type(item):
                            self.add_attributes_recursively(child_node, item, max_depth, current_depth + 1)
                
                elif hasattr(value, "__dict__") or len(dir(value)) > 0:
                    try:
                        # Recursively add attributes
                        self.add_attributes_recursively(attr_node, value, max_depth, current_depth + 1)
                    except Exception as e:
                        attr_node.add(f"[red]<Error accessing attributes: {str(e)}>[/red]")
    
    def build_for_object(self, obj):
        """Build the attribute tree for an object
        
        Args:
            obj: The object to build the tree for
        """
        self.clear()
        self.set_title(f"Attributes of {obj.__class__.__name__}")
        self.add_attributes_recursively(self.tree.root, obj)
        self.expand_root()


def get_module_device(module):
    """Determine the device of a PyTorch module
    
    Args:
        module: PyTorch module to check
        
    Returns:
        str: Device string, or empty string if no params
    """
    return get_module_param_attr(module, 'device')


def format_devices(devices):
    """Format a set of device strings in a clean, concise way
    
    Args:
        devices: Set of device strings
        
    Returns:
        str: Formatted device string
    """
    if not devices:
        return ""
        
    # Convert all to strings
    devices = set(map(str, devices))
    
    # Condense down any combination of cuda:1, cuda:2, cuda:3 to cuda:1,2,3
    cuda_labels = set()
    cuda_devices = set(x for x in devices if x.startswith('cuda:'))
    if cuda_devices:
        cuda_numbers = ','.join(sorted(x.strip('cuda:') for x in cuda_devices))
        cuda_labels |= {f'cuda:{cuda_numbers}'}

    other_devices = devices - cuda_devices
    other_labels = set(map(str, other_devices))

    return '/'.join(sorted(other_labels | cuda_labels))


def get_module_device_label(module):
    """Get the device label for a module
    
    Args:
        module: PyTorch module to check
        
    Returns:
        str: Formatted device label (e.g., 'cuda:0' or 'cpu')
    """
    if module is None:
        return ''

    if hasattr(module, 'device'):
        return str(module.device)
        
    try:
        # Get devices from all parameters
        devices = set(x.device for x in module.parameters())
        return format_devices(devices)
    except Exception:
        # Fallback to get_module_device for any errors
        return get_module_device(module)
        


    









@dataclass
class ModuleEntry:
    """Attaches module information to a tree node."""
    
    module: Any  # The PyTorch module
    name: str = ""  # Module name
    loaded: bool = False  # Has this been loaded?
    path: str = ""  # Full attribute path to this module (e.g., "model.encoder.layers[0]")
    expanded_children: set = field(default_factory=set)  # Set of full paths of expanded children
    
    # Note: expanded_children is used to preserve folding state even when nodes are deleted.
    # When a node is collapsed, we record which children were expanded in this set using their full paths.
    # Later, when the node is expanded again, we automatically re-expand those same children.
    # This provides a memory-efficient way to maintain folding history across the entire module hierarchy.


class ModuleNode:
    """Node representing a PyTorch module"""
    # Define component classes with their default active states
    # Ordered by how they appear in the label
    component_classes = [
        (AlignmentComponent, False),  # Alignment first in the list
        (DeviceLabelComponent, False),
        (ModuleDTypeComponent, False), # DType next to Device
        (ParamCountComponent, False),  # Parameter count hidden by default
        (ParamPercentComponent, False),  # Parameter percentage hidden by default
        (SelfParamCountComponent, False),  # Self parameter count hidden by default
        (SizeLabelComponent, True),    # Parameters memory 
        (MemoryPercentComponent, False),  # Memory percentage hidden by default
        (SelfMemoryComponent, False),  # Self memory hidden by default
        (ForwardInputMemorySizeComponent, False),  # Memory components grouped together
        (ForwardOutputMemorySizeComponent, False),
        (ForwardInputShapeComponent, False),
        (ForwardOutputShapeComponent, False),
        (ForwardCallCountComponent, False),
        (ForwardRuntimeComponent, False),   # Runtime components grouped together
        (RuntimePercentComponent, False),  # Runtime percentage hidden by default
        (AvgSelfRuntimeComponent, False),
        (TotalRuntimeComponent, True),      # Total runtime component enabled by default
        (AvgTotalRuntimeComponent, False),
        (ModuleNameComponent, None),  # None means use default constructor
        (ModuleTypeNameComponent, None),  # None means use default constructor
        (ModuleTypeArgsComponent, None),  # None means use default constructor
        (ParamShapesComponent, True)
    ]
    
    def __init__(self, name: str, module_type: str, extra_info: str = "", state_dict_info: str = "", 
                 module=None, size_bytes: int = 0, param_count: int = 0):
        self.name = name
        self.module_type = module_type
        self.extra_info = extra_info
        self.state_dict_info = state_dict_info
        self.module = module
        self.size_bytes = size_bytes
        self.param_count = param_count
        # Use the new function directly - no need to cache it
        # Device info will be retrieved dynamically through the device component
        self.device_label = ""
        
        # Initialize label components in the order they'll be displayed
        self.label_components = []
        for component_class, default_active in self.component_classes:
            # Special case for components with custom constructors
            if default_active is None:
                component = component_class()  # Use default constructor 
            else:
                component = component_class(active=default_active)
            self.label_components.append(component)
    
    # Component look-up helper methods
    def get_component(self, component_class):
        """Get a component of a specific class"""
        for component in self.label_components:
            if isinstance(component, component_class):
                return component
        return None

    def is_alignment_active(self):
        """Check if alignment is active"""
        alignment_component = self.get_component(AlignmentComponent)
        return alignment_component and alignment_component.active

    def get_label(self, alignment_data=None) -> str:
        """Get the display label for this node with optional alignment"""
        # Check if alignment is active
        alignment_active = self.is_alignment_active()
        
        # Handle recursive call when alignment is active but no data is provided yet
        if alignment_active and alignment_data is None:
            alignment_component = self.get_component(AlignmentComponent)
            alignment_component.active = False  # Temporarily disable
            label = self.get_label()  # Get unaligned label
            alignment_component.active = True   # Re-enable
            return label
        
        # Initialize label parts list
        label_parts = []
        
        # Handle standard (non-aligned) case
        if not alignment_active or not alignment_data:
            # Just concatenate active non-alignment components
            for component in self.label_components:
                if not isinstance(component, AlignmentComponent):
                    label_parts.append(component.get_label(self))
            return "".join(label_parts)
            
        # Handle alignment case - extract alignment data
        component_widths = alignment_data.get("component_widths", {})
        alignment_positions = alignment_data.get("positions", [])
        has_expandable_children = alignment_data.get("has_expandable_children", {})
        current_node = alignment_data.get("current_node")
        
        # Add alignment prefix (┆) ONLY for leaves (nodes without children)
        # NEVER add this symbol to nodes that have children (which get ▶/▼ from Textual)
        if current_node:
            # Most reliable way to check if a node should show ┆ is to verify:
            # 1. It doesn't have allow_expand=True (which would show ▶/▼)
            # 2. It's not in the has_expandable_children dict as True
            node_has_children = (
                getattr(current_node, 'allow_expand', False) or
                has_expandable_children.get(current_node, False)
            )
            
            if not node_has_children:
                label_parts.append("[#5F5F5F]┆ [/#5F5F5F]")
        
        # Process all components in order by position
        for i in alignment_positions:
            # Skip invalid positions
            if i >= len(self.label_components):
                continue
            
            component = self.label_components[i]
            
            # Skip alignment component itself
            if isinstance(component, AlignmentComponent):
                continue
            
            # Get maximum width for this component position
            max_width = component_widths.get(i, 0)
            
            # Handle inactive or empty components
            if not component.active or not component._get_text(self):
                if max_width > 0:
                    label_parts.append(" " * max_width)
                continue
            
            # Get component text and add padding
            component_text = component.get_label(self)
            width = component.get_width(self)
            padding = max_width - width
            
            if padding > 0:
                component_text += " " * padding
                
            label_parts.append(component_text)
            
        return "".join(label_parts)

class ComponentState:
    """Class to manage state for a component type with callbacks for UI updates"""
    
    def __init__(self, component_class, default_active=False):
        self.component_class = component_class
        self.active = default_active
        self.display_name = component_class.display_name
        self.example = component_class.example
        self.style = component_class.style
        self.shortcut_key = component_class.shortcut_key
        # Callbacks to update UI when state changes
        self.ui_callbacks = []
        
    def add_callback(self, callback):
        """Add a callback to be called when state changes
        
        Args:
            callback: Function that takes a boolean for the new state
        """
        self.ui_callbacks.append(callback)
        
    def toggle(self):
        """Toggle the active state and notify callbacks"""
        self.active = not self.active
        self._notify_callbacks()
        return self.active
        
    def set_active(self, active):
        """Set the active state directly and notify callbacks"""
        self.active = active
        self._notify_callbacks()
        return self.active
        
    def _notify_callbacks(self):
        """Notify all callbacks about state change"""
        for callback in self.ui_callbacks:
            callback(self.active)
        
    @property
    def status_text(self):
        """Get the formatted status text"""
        return "ON" if self.active else "OFF"
        
    @property 
    def status_style(self):
        """Get the style for status text"""
        return "green" if self.active else "red"
        
    @property
    def formatted_example(self):
        """Get the formatted example text"""
        if self.style:
            return f"[{self.style}]{self.example}[/{self.style}]"
        return self.example
        
    @property
    def shortcut_text(self):
        """Get the formatted shortcut text"""
        if self.shortcut_key:
            return f"(Key: {self.shortcut_key})"
        return ""
        
    @property
    def button_text(self):
        """Get the complete formatted button text"""
        return f"[{self.status_style}]{self.status_text}[/{self.status_style}] {self.display_name}: {self.formatted_example} {self.shortcut_text}"
        

from textual.widgets import ListItem

class ComponentListItem(ListItem):
    """Component list item with state sync"""
    
    def __init__(self, component_state):
        super().__init__()
        self.component_state = component_state
        # Register a callback to update our UI when state changes
        self.component_state.add_callback(self.update_switch)
    
    def compose(self) -> ComposeResult:
        """Create a toggle with colored text and description"""
        # Container for the whole item with switch and text content
        with Horizontal(classes="top-row"):
            # Switch on left
            yield Switch(
                value=self.component_state.active, 
                id=f"switch-{self.component_state.component_class.__name__}",
                disabled=True,  # This prevents tab focus
                classes="component-switch"
            )
            with Vertical(classes="item-container"):
                # Top row with switch and labels
                    
                    # Shortcut in dimmed color
                    shortcut = self.component_state.shortcut_key
                    shortcut_text = f"[#888888]({shortcut})[/#888888] " if shortcut else ""
                    
                    # Name in bold white
                    name = f"[bold white]{self.component_state.display_name}[/bold white] "
                    
                    # Example in original styling
                    example = self.component_state.formatted_example
                    
                    # Combined label with tight height
                    yield Label(f"{shortcut_text}{name}{example}", classes="component-label")
                
                    # Description in italic gray on the second row
                    desc = self.component_state.component_class.description
                    yield Label(f"[italic #888888]{desc}[/italic #888888]", classes="component-description")
                    
            # # Add up/down buttons on the right side in a column
            # with Horizontal(classes="move-buttons-container"):
            #     yield Button("▲", id="move-up-button", classes="move-button")
            #     yield Button("▼", id="move-down-button", classes="move-button")
    
    def on_click(self) -> None:
        """Handle clicks on the component"""
        # Just toggle the switch when the component is clicked
        self.toggle_switch()
    
    def toggle_switch(self) -> None:
        """Toggle the component state - this updates both the model and UI"""
        # Use the app's toggle_component method to ensure consistency
        app = self.app
        component_name = self.component_state.component_class.__name__
        app.toggle_component(component_name)
        
    def update_switch(self, is_active) -> None:
        """Update switch UI to match state - called from callback"""
        # Direct UI update without changing state
        try:
            switch = self.query_one(Switch)
            if switch.value != is_active:
                switch.value = is_active
        except Exception:
            # Switch might not be available yet, try again later
            pass
            
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses for up/down movement"""
        # This event correctly identifies which button was pressed
        if event.button.id == "move-up-button":
            self.app.move_component_up(self)
        elif event.button.id == "move-down-button":
            self.app.move_component_down(self)
            
        # Stop event propagation to prevent it from also triggering on_click
        event.stop()



def build_parent_map(model):
    """Build a mapping from modules to their parent modules
    
    Instead of modifying modules directly (which can cause issues with PyTorch's
    custom __setattr__), this builds a dictionary mapping each module to its parent.
    
    Args:
        model: The PyTorch model to process
        
    Returns:
        dict: A mapping from modules to their parent modules
    """
    # Dictionary to store parent relationships
    parent_map = {}
    
    # Process modules recursively
    def process_children(module, parent=None):
        # Store parent relationship in the dictionary
        parent_map[module] = parent
        
        # Process all children
        for name, child in module.named_children():
            process_children(child, module)
    
    # Start from the root with no parent
    process_children(model, None)
    
    # Store the parent map as a class variable on ModelTreeViewer
    ModelTreeViewer.parent_map = parent_map
    
    return parent_map


class ModelTreeViewer(App):
    """Textual app to display a PyTorch model structure as a tree with folding"""
    # Store the model for direct access by components
    model = None
    # Store parent mapping
    parent_map = {}
    
    # Queue for loading module children
    load_queue: Queue = None
    
    CSS = """
    #main-container {
        layout: horizontal;
        height: 100%;
    }
    
    #label-manager {
        width: 25%;
        min-width: 30;
        height: 100%;
        border-right: solid gray;
        display: none;
    }

    #label-manager-title {
        height: auto;
        padding: 1;
        background: #333333;
        color: #ffffff;
        text-align: center;
        text-style: bold;
    }
    
    HJKLListView {
        width: 100%;
        height: 1fr;
        border: none;
        overflow-y: auto; /* Show scrollbar only when needed */
    }
    
    /* Component list styling */
    .component-item {
        padding: 0;
        height: 5; /* Make each item exactly 5 rows tall */
    }
    
    /* Position switch on left, label on right */
    .component-switch {
        margin-right: 1;
        width: auto;
        # height: 1;
    }
    
    .component-label {
        width: 1fr; /* Take remaining space */
        height: 1;
        content-align: left middle;
    }
    
    .item-container {
        margin: 0;
        padding: 0;
        height: 5;
        width: 1fr;
    }
    
    .top-row {
        height: 5;
        margin: 1 0 1 0;
        padding: 0;
    }
    
    .component-description {
        height: 2;
        width: 100%;
        margin-left: 5; /* Align with the text above, not with the switch */
    }
    
    /* Make disabled switches appear fully opaque */
    Switch:disabled {
        opacity: 100%;
        text-opacity: 100%;
    }
    
    .move-buttons-container {
        width: 40;
        height: 5;
        padding: 0;
        margin: 0;
    }
    
    .move-button {
        width: 1;
        height: 5;
        background: #444444;
        color: #ffffff;
        margin: 0;
        padding: 0;
        content-align: center middle;
    }
    
    .move-button:hover {
        background: #666666;
    }
    
    #label-instructions {
        height: auto;
        padding: 1;
        background: #222222;
        color: #999999;
        text-align: center;
        text-style: italic;
    }
    
    #tree-pane {
        width: 40%;
        height: 100%;
        border-right: solid gray;
    }
    
    #editor-pane {
        width: 60%;
        height: 100%;
        layout: vertical;
    }
    
    #code-title {
        height: auto;
        padding: 1;
        border-bottom: solid gray;
        background: #333333;
        color: #ffffff;
        text-align: center;
        text-style: bold;
    }
    
    #code-editor {
        height: 2fr;
        width: 100%;
        border-bottom: solid gray;
    }
    
    #attrs-title {
        height: auto;
        padding: 1;
        border-bottom: solid gray;
        background: #333333;
        color: #ffffff;
        text-align: center;
        text-style: bold;
    }
    
    #attrs-pane {
        height: 1fr;
        width: 100%;
        overflow-y: auto;
    }
    
    Tree {
        width: 100%;
        height: 100%;
        overflow-x: auto;  /* Allow horizontal scrolling */
    }
    
    TextArea {
        width: 100%;
        height: 100%;
    }
    
    .param-shape {
        color: #5fd700;
        text-style: italic;
    }
    
    .device-info {
        color: #d787ff;
        text-style: bold;
    }
    
    .bright_yellow {
        color: #ffff00;
        text-style: italic;
    }
    
    Tree > .tree--cursor {
        background: #3a3a3a;
        color: #ffffff;
    }
    """
    
    BINDINGS = [
        
        # Panel options
        Binding("L", "toggle_label_manager", "Labels"),
        Binding("<", "expand_right_panel", " "),
        Binding("c", "toggle_code_panel", "Code"),
        Binding("a", "toggle_attrs_panel", "Attr "),
        Binding(">", "contract_right_panel", " "),

        # Tree operations
        Binding("z", "toggle_subtree", "Fold Subtree "),
        Binding("Z", "toggle_all_folds", "Fold All "),
        Binding("s", "toggle_siblings", " /"),
        Binding("S", "toggle_all_siblings", "Fold Siblings"),
        Binding("o", "toggle_same_class", " /"),
        Binding("O", "toggle_all_same_class", "Fold by Class"),
        
        # Display options - individual toggles
        Binding("A", "toggle_alignment", "Align"),  # Capital A for alignment
        Binding("t", "toggle_param_shapes", ""),
        Binding("m", "toggle_memory", ""),  # Toggle both all-memory and self-memory
        Binding("p", "toggle_params", ""),  # Toggle both all-params and self-params
        Binding("d", "toggle_device", ""),  # This will trigger both device and dtype
        Binding("r", "toggle_runtime", ""),  # New binding for runtime components
        Binding("f", "toggle_forward_stats", ""),
        
        # Help
        Binding("?", "show_help", "Help"),
    ]
    
    def __init__(self, model=None):
        super().__init__()
        # Store model at class level for easy access by components
        ModelTreeViewer.model = model
        # Also store at instance level
        self.model = model
        
        # Initialize the load queue
        self.load_queue = Queue()
        
        # Initialize the lock for async access
        self.lock = Lock()
        
        # Build parent mapping for all modules
        if model:
            build_parent_map(model)
        
        # Cache node_data for each tree node
        self.node_data: Dict[Any, ModuleNode] = {}
        
        # Flag to track if code panel is visible
        self.code_panel_visible = True
        
        # Flag to track if attributes panel is visible
        self.attrs_panel_visible = True
        
        # Flag to track if label manager is visible
        self.label_manager_visible = False
        
        # Right panel width tracking
        self.right_panel_width = 60  # Default percentage
        self.min_right_panel_width = 5   # Minimum percentage (reduced to 5%)
        self.max_right_panel_width = 80  # Maximum percentage
        self.right_panel_step = 5     # Percentage to increase/decrease by
        
        # Flag to prevent recursive updates between UI and components
        self._updating_from_selection = False
        
        # Use a built-in theme for the editor
        self.editor_theme = TextAreaTheme.get_builtin_theme("vscode_dark")
        
        # Extract component classes and their default states from ModuleNode
        # This ensures we're using exactly the same components that are used in the nodes
        self.component_classes = []
        component_defaults = {}
        
        for component_class, default_active in ModuleNode.component_classes:
            # For classes with no default specified, use their constructor default
            if default_active is None:
                component_obj = component_class()
                default_active = component_obj.active
            
            # Add to our lists
            self.component_classes.append(component_class)
            component_defaults[component_class] = default_active
        
        # Create a class map for faster lookup
        self.component_class_map = {cls.__name__: cls for cls in self.component_classes}
        
        # Initialize component states with default values
        self.component_states = {}
        
        # Create ComponentState objects for each component type
        for component_class, default_active in component_defaults.items():
            # Enable TotalRuntimeComponent by default for better visibility
            if component_class.__name__ == "TotalRuntimeComponent":
                default_active = True
                
            self.component_states[component_class.__name__] = ComponentState(
                component_class, default_active
            )
    
    def compose(self) -> ComposeResult:
        """Compose the UI with label manager, tree view, and editor panes"""
        with Horizontal(id="main-container"):
            # Label manager panel (initially hidden)
            with Container(id="label-manager"):
                yield Static("Labels Customization", id="label-manager-title")
                yield Static("Choose what you want to see!\nClick below or use keyboard shortcuts\nUse ⇧J and ⇧K to reorder labels", id="label-instructions")
                # Buttons will be added in init_label_manager
            
            # Tree view pane
            with Static(id="tree-pane"):
                yield HJKLTree("Model Structure")
            
            # Right pane with code editor and attributes
            with Static(id="editor-pane"):
                # Create a static widget to display the file path
                yield Static("", id="code-title")
                # Code editor in a container to control height
                with Static(id="code-editor"):
                    editor = TextArea(
                        language="python", 
                        read_only=True, 
                        show_line_numbers=True
                    )
                    # We'll register the theme after the widget is mounted
                    yield editor
                
                # Attributes section
                yield Static("Attributes: No Object Selected", id="attrs-title")
                with Static(id="attrs-pane"):
                    yield HJKLTree("No Object Selected")
                
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up the UI when app is mounted"""
        # Set up the model tree
        tree = self.query_one("#tree-pane > HJKLTree")
        
        # Register theme with editor
        editor = self.query_one("#code-editor > TextArea")
        if self.editor_theme:
            editor.register_theme(self.editor_theme)
            editor.theme = "vscode_dark"
        
        # Initialize attributes tree
        attrs_tree = self.query_one("#attrs-pane > HJKLTree")
        attrs_tree.root.expand()
        
        # Initialize label manager
        self.init_label_manager()
        
        # Initialize panel layout
        self.update_panel_layout()
        
        # Start the module loader worker
        self._module_loader()
        
        # Populate the tree if we have a model
        if self.model:
            # Initialize with the root only
            self.populate_tree(self.model, tree.root)
            
            # Show code and attributes for root model upon startup
            self.update_editor_with_module(self.model)
            
            # Manually load the root node's children since we're expanding it programmatically
            if tree.root.data is not None:
                # Add root to load queue
                self._add_to_load_queue(tree.root, tree.root.data)
                # Now expand the root - this won't trigger the event handler
                tree.root.expand()
            
        # Focus on the tree by default
        tree.focus()
        
    def _add_to_load_queue(self, node, module_entry):
        """Add the given node to the load queue.
        
        Args:
            node: The tree node
            module_entry: The ModuleEntry for this node
            
        Returns:
            AwaitComplete: An optionally awaitable object
        """
        if not module_entry.loaded:
            module_entry.loaded = True
            self.load_queue.put_nowait(node)
        
        return AwaitComplete(self.load_queue.join())
        
    @work(exclusive=True)
    async def _module_loader(self) -> None:
        """Background worker to load module children on demand."""
        worker = get_current_worker()
        while not worker.is_cancelled:
            try:
                # Get the next node that needs loading (blocks if queue is empty)
                node = await self.load_queue.get()
                
                try:
                    async with self.lock:
                        # Get module information
                        module_entry = node.data
                        if module_entry is None:
                            continue
                        
                        # Load children for this module
                        children = self._get_module_children(module_entry.module)
                        
                        # Update the node with children
                        if children:
                            self._populate_node_with_children(node, children, module_entry.module)
                except WorkerCancelled:
                    # The worker was cancelled, exit
                    break
                except Exception as e:
                    # Log any errors but continue processing
                    import traceback
                    print(f"Error loading module children: {e}")
                    traceback.print_exc()
                finally:
                    # Mark this task as done - ensure this happens even if there's an error
                    self.load_queue.task_done()
            except WorkerCancelled:
                # The worker was cancelled, exit
                break
            except Exception:
                # Catch any unexpected errors at the top level to keep the worker running
                import traceback
                traceback.print_exc()
        
    def init_label_manager(self):
        """Initialize the label manager with HJKLListView and component items"""
        # Get label manager container
        label_container = self.query_one("#label-manager")
        
        # Try to get the existing component list
        try:
            list_view = self.query_one("#component-list")
            # If found, clear its contents
            list_view.clear()
        except Exception:
            # If not found or error occurred, remove any potential children first
            children_to_remove = [child for child in label_container.children 
                                if isinstance(child, (ListView, HJKLListView, Container)) or 
                                (hasattr(child, "id") and child.id == "component-list")]
            for child in children_to_remove:
                # Remove using proper method (no arguments)
                child.remove()
                
            # Create a new ListView with hjkl support
            list_view = HJKLListView(id="component-list")
            label_container.mount(list_view)
        
        # Add component list items
        for component_class in self.component_classes:
            # Get the component state for this class
            component_state = self.component_states[component_class.__name__]
            
            # Create a list item for this component
            list_item = ComponentListItem(component_state)
            list_item.add_class("component-item")
            
            # Add to list view
            list_view.append(list_item)
    
    def calculate_module_stats(self, module):
        """Calculate the size and parameter count of a module based on its state_dict tensors
        
        Returns:
            tuple: (size_in_bytes, param_count)
        """
        total_size = 0
        param_count = 0
        try:
            state_dict = module.state_dict()
            for param_name, tensor in state_dict.items():
                if isinstance(tensor, torch.Tensor):
                    # Count parameters (elements in the tensor)
                    num_elements = tensor.numel()
                    param_count += num_elements
                    
                    # Calculate tensor size using the helper function
                    # We use calculate_memory_from_shape which is more general
                    total_size += calculate_memory_from_shape(tensor.shape, tensor.dtype)
        except Exception as e:
            # If there's an error calculating stats, return zeros
            return 0, 0
            
        return total_size, int(param_count)
        
    def _get_module_children(self, module):
        """Get children for a PyTorch module
        
        Args:
            module: PyTorch module to get children for
            
        Returns:
            dict: Dictionary of {name: child_module} pairs
        """
        if not is_torch_module(module):
            # For non-module objects, look for modules in __dict__
            module_dict = {}
            if hasattr(module, "__dict__"):
                for key, value in module.__dict__.items():
                    if is_torch_module(value):
                        module_dict[key] = value
            return module_dict
        else:
            # For actual module objects, return the named_children
            return {name: child for name, child in module.named_children()}
    
    def _populate_node_with_children(self, node, children, parent_module):
        """Populate a node with its children
        
        Args:
            node: Tree node to populate
            children: Dictionary of {name: child_module} pairs
            parent_module: The parent module
        """
        node.remove_children()
        for key, child_module in children.items():
            # Apply consistent formatting with yellow module name and syntax-colored code
            module_part = f"[bold yellow]({key})[/bold yellow]: "
            # Use cyan for the class name (typical Python syntax highlighting)
            code_part = f"[cyan]{child_module._get_name()}[/cyan]"
            formatted_label = module_part + code_part
            
            # Create module entry with name
            module_entry = ModuleEntry(module=child_module, name=key)
            
            # Create child node with lazy-loaded data
            child_node = node.add(
                formatted_label,
                data=module_entry,
                allow_expand=bool(self._get_module_children(child_module))
            )
            
            # Create module node for display formatting
            module_name = key
            module_type = child_module._get_name()
            extra_info = child_module.extra_repr()
            
            # For leaf modules, get parameter shapes
            state_dict_info = ""
            if not child_module._modules:  # This is a leaf module
                try:
                    # Get state dict and format tensor shapes
                    params = list(child_module.state_dict().items())
                    if params:
                        shapes = []
                        for param_name, tensor in params:
                            if isinstance(tensor, torch.Tensor):
                                shape_str = f"{param_name}: {format_shape(tensor.shape)}"
                                shapes.append(shape_str)
                        state_dict_info = ", ".join(shapes)
                except Exception as e:
                    state_dict_info = f"Error: {str(e)}"
            
            # Calculate module stats
            module_size, param_count = self.calculate_module_stats(child_module)
            
            # Create display node data
            node_data = ModuleNode(
                name=module_name,
                module_type=module_type,
                extra_info=extra_info,
                state_dict_info=state_dict_info,
                module=child_module,
                size_bytes=module_size,
                param_count=param_count
            )
            
            # Apply the current component state to this new node before adding it to node_data
            self._apply_current_component_states_to_node(node_data)
            
            # Store the node data
            self.node_data[child_node] = node_data
            
            # Check if alignment is active to properly align the new nodes
            any_aligned = any(
                node_data.is_alignment_active() 
                for node_data in self.node_data.values()
            )
            
            # Update the label with alignment if needed
            if any_aligned:
                # Calculate alignment for this parent's children
                alignment_data = self.calculate_aligned_labels(node)
                if alignment_data:
                    # Set the current node in alignment data
                    alignment_data["current_node"] = child_node
                    child_node.label = node_data.get_label(alignment_data)
                else:
                    child_node.label = node_data.get_label()
            else:
                child_node.label = node_data.get_label()
            
        node.expand()
    
    def populate_tree(self, obj, tree_node):
        """
        Initialize tree with root node, children will be loaded on demand

        Args:
            obj: Either a PyTorch module or an object containing modules in __dict__
            tree_node: The current tree node to populate
        """
        # Check if the object is a PyTorch module
        if is_torch_module(obj):
            # Handle PyTorch module case
            module = obj
            module_name = module._get_name()
            extra_info = module.extra_repr()
            
            # Calculate the module size and parameter count
            module_size, param_count = self.calculate_module_stats(module)
            
            # Get state dict info for leaf modules (no children)
            state_dict_info = ""
            if not module._modules:  # This is a leaf module
                try:
                    # Get state dict and format tensor shapes
                    params = list(module.state_dict().items())
                    if params:
                        shapes = []
                        for param_name, tensor in params:
                            if isinstance(tensor, torch.Tensor):
                                shape_str = f"{param_name}: {format_shape(tensor.shape)}"
                                shapes.append(shape_str)
                        state_dict_info = ", ".join(shapes)
                except Exception as e:
                    state_dict_info = f"Error: {str(e)}"
            
            # Create or get the parent node data
            if tree_node == self.query_one(Tree).root:
                node_name = ""
            else:
                node_label = str(tree_node.label)
                if ":" in node_label:
                    node_name = node_label.split(":")[0].strip("() ")
                else:
                    node_name = node_label
            
            # Create display node data (for formatting)
            node_data = ModuleNode(
                name=node_name, 
                module_type=module_name, 
                extra_info=extra_info, 
                state_dict_info=state_dict_info, 
                module=module, 
                size_bytes=module_size, 
                param_count=param_count
            )
            
            # Apply current component states to the new node
            self._apply_current_component_states_to_node(node_data)
            
            self.node_data[tree_node] = node_data
            
            # Create module entry (for lazy loading)
            module_entry = ModuleEntry(module=module, name=node_name)
            
            # Check if it has children
            has_children = bool(self._get_module_children(module))
            
            # Set node data and options
            tree_node.data = module_entry
            tree_node.allow_expand = has_children
            
            # Set node display text
            tree_node.label = node_data.get_label()
            
        else:
            # Handle non-module objects by exploring their __dict__ for modules
            # This is for the root node that contains modules but isn't itself a module
            
            if tree_node == self.query_one(Tree).root:
                # For the root node, create a special node data
                root_class_name = obj.__class__.__name__
                node_data = ModuleNode(
                    name="", 
                    module_type=root_class_name, 
                    extra_info="", 
                    state_dict_info="", 
                    module=obj, 
                    size_bytes=0, 
                    param_count=0
                )
                
                # Apply current component states to the root node
                self._apply_current_component_states_to_node(node_data)
                
                self.node_data[tree_node] = node_data
                
                # Create module entry for lazy loading
                module_entry = ModuleEntry(module=obj, name="")
                tree_node.data = module_entry
                
                # Set root node label
                tree_node.label = f"[cyan]{root_class_name}[/cyan]"
                
                # Check if it has children
                has_children = bool(self._get_module_children(obj))
                tree_node.allow_expand = has_children
                
            else:
                # Non-root node that's not a module - just display its type
                class_name = obj.__class__.__name__
                tree_node.label = f"[cyan]{class_name}[/cyan] (not a PyTorch module)"
                tree_node.allow_expand = False
    
    def on_node_expanded(self, node) -> None:
        """Handle node expansion to load children directly
        
        This is called when a node is expanded by clicking or pressing right arrow.
        It ensures that the node's children are loaded and displayed properly.
        
        Key features:
        1. Loads children on demand when a node is expanded
        2. Restores the previous expansion state of children
        3. Automatically re-expands any children that were expanded before the collapse
        
        This approach provides a consistent user experience by preserving the folding
        history while still allowing memory optimization through node removal.
        """
        if node.data is not None and not node.data.loaded:
            # Load the children directly instead of using the queue
            module_entry = node.data
            children = self._get_module_children(module_entry.module)
            if children:
                # Remember which children were previously expanded - both from local and global state
                previously_expanded = module_entry.expanded_children
                
                # Initialize the global expanded paths if not already
                if not hasattr(self, 'global_expanded_paths'):
                    self.global_expanded_paths = set()
                    
                # Mark as loaded and populate the node
                module_entry.loaded = True
                self._populate_node_with_children(node, children, module_entry.module)
                
                # Re-expand all children that should be expanded
                for child in node.children:
                    if child.data is not None:
                        # Get the full path of this child
                        child_path = self.get_node_path(child)
                        
                        # Check if this path should be expanded based on:
                        # 1. Previously stored expansion in this node's data
                        # 2. Global tree expansion tracking
                        should_expand = (
                            child_path in previously_expanded or 
                            (hasattr(self, 'global_expanded_paths') and child_path in self.global_expanded_paths)
                        )
                        
                        if should_expand:
                            child.expand()
                
                # After handling expansions, check if we need to apply alignment
                any_aligned = any(
                    data.is_alignment_active() 
                    for data in self.node_data.values()
                )
                
                if any_aligned:
                    # Recalculate and update all labels with proper alignment
                    self.update_aligned_node_labels()
    
    def on_tree_node_selected(self, event) -> None:
        """Handle tree node selection to update the editor and attributes tree"""
        # Check if the selected node is from the main model tree by checking if it's in our node_data
        node = event.node
        if node in self.node_data:
            module = self.node_data[node].module
            if module is not None:
                self.update_editor_with_module(module)
    
    # Removed format_value - now part of AttributeTree class
    
    # Remove the moved methods - now they're in AttributeTree class
    
    def format_python_attribute_path(self, path_parts):
        """Format a list of path parts into a valid Python attribute path
        
        Converts sequences like ["transformer_blocks", "8", "attn1"] into
        proper Python syntax: "transformer_blocks[8].attn1"
        
        Args:
            path_parts: List of path components
            
        Returns:
            str: Properly formatted Python attribute path
        """
        processed_parts = []
        i = 0
        while i < len(path_parts):
            part = path_parts[i]
            
            # Check if this part is followed by a numeric index
            if i + 1 < len(path_parts) and path_parts[i + 1].isdigit():
                # This part should have an index
                index_part = path_parts[i + 1]
                processed_parts.append(f"{part}[{index_part}]")
                i += 2  # Skip the next part since we've incorporated it
            else:
                # Regular part (may be a digit or a name)
                processed_parts.append(part)
                i += 1
        
        # Join processed parts with dots
        return ".".join(processed_parts)
    
    def get_module_path(self, module):
        """Get a properly formatted Python path to a module in the model structure
        
        Args:
            module: The module to get a path for
            
        Returns:
            str: Python-style path to the module (e.g., "model.layers[0].attention")
        """
        # Try to find the node for this module
        for node, node_data in self.node_data.items():
            if node_data.module is module:
                # Get the node path
                return self.get_node_path(node)
        
        # If we can't find a path, return the class name
        return module.__class__.__name__
        
    def get_node_path(self, node):
        """Get the full attribute path for a tree node by traversing its parent hierarchy
        
        Args:
            node: Tree node to get path for
            
        Returns:
            String with the full Python attribute path (e.g., "model.encoder.layers[0]")
        """
        if node is None or node.data is None:
            return ""
            
        # If the node already has a path set, return it
        if node.data.path:
            return node.data.path
            
        # Build path by traversing up the tree
        path_parts = []
        current = node
        
        # Traverse up the tree collecting names
        while current is not None and current.data is not None and current != self.query_one("#tree-pane > Tree").root:
            if current.data.name:  # Skip nodes without names
                path_parts.insert(0, current.data.name)
            current = current.parent
            
        # Format the path parts into a proper attribute path
        if path_parts:
            formatted_path = self.format_python_attribute_path(path_parts)
            
            # Store the path in the node data for future use
            if node.data is not None:
                node.data.path = formatted_path
                
            return formatted_path
        
        # Default for root node
        if node.data is not None:
            node.data.path = "model"
        return "model"
    
    def build_attributes_tree(self, obj):
        """Build a tree of attributes for the given object"""
        attrs_tree = self.query_one("#attrs-pane > Tree")
        attrs_title = self.query_one("#attrs-title")
        
        # Get the full path to the object
        path = self.get_module_path(obj)
        
        # Update the attributes title directly
        attrs_title.update(f"Attributes: {path}".replace('[',r'\[').replace(']',r']'))
        
        # Create and use the AttributeTree helper class
        attribute_tree = AttributeTree(attrs_tree)
        attribute_tree.build_for_object(obj)
                
    def update_editor_with_module(self, module) -> None:
        """Update the editor with module source code and attributes"""
        editor = self.query_one("#code-editor > TextArea")
        code_title = self.query_one("#code-title")
        
        try:
            # Get source code for the module class
            source = inspect.getsource(module.__class__)
            line_number = inspect.getsourcelines(module.__class__)[1]
            
            # Get file path information if available
            try:
                file_path = inspect.getfile(module.__class__)
            except (TypeError, OSError):
                file_path = "Unknown file path"
            
            # Update the title with the file path
            code_title.update(f"{file_path}")
            
            # Set the content in the editor
            editor.text = source
            
            # Move cursor to the class definition line
            editor.move_cursor((line_number-1, 0))
            
        except (TypeError, OSError) as e:
            # Handle case where source isn't available (built-in modules, etc.)
            code_title.update(f"{module.__class__.__name__}")
            editor.text = f"# Source code not available for {module.__class__.__name__}\n# {str(e)}"
        
        # Build the attributes tree
        self.build_attributes_tree(module)
    
    def action_focused_panel_down(self) -> None:
        """Move down in the currently focused panel"""
        # If the focused widget is a component list item
        if isinstance(self.focused, ComponentListItem):
            # Get all component items
            component_items = list(self.query(ComponentListItem))
            if not component_items:
                return
                
            # Find the currently focused item
            focused_index = component_items.index(self.focused)
            
            # Move focus to the next item
            if focused_index < len(component_items) - 1:
                # Focus the next item
                component_items[focused_index + 1].focus()
        
        # If the tree has focus, use its cursor movement
        elif self.focused and "#tree-pane" in str(self.focused.css_id_selector):
            tree = self.query_one(Tree)
            tree.action_cursor_down()
        
        # If the attribute tree has focus
        elif self.focused and "#attrs-pane" in str(self.focused.css_id_selector):
            # Handle attribute tree navigation if needed
            attrs_tree = self.query_one("#attrs-pane > Tree")
            attrs_tree.action_cursor_down()
            
    def action_focused_panel_up(self) -> None:
        """Move up in the currently focused panel"""
        # If the focused widget is a component list item
        if isinstance(self.focused, ComponentListItem):
            # Get all component items
            component_items = list(self.query(ComponentListItem))
            if not component_items:
                return
                
            # Find the currently focused item
            focused_index = component_items.index(self.focused)
            
            # Move focus to the previous item
            if focused_index > 0:
                # Focus the previous item
                component_items[focused_index - 1].focus()
        
        # If the tree has focus, use its cursor movement
        elif self.focused and "#tree-pane" in str(self.focused.css_id_selector):
            tree = self.query_one(Tree)
            tree.action_cursor_up()
            
        # If the attribute tree has focus
        elif self.focused and "#attrs-pane" in str(self.focused.css_id_selector):
            # Handle attribute tree navigation if needed
            attrs_tree = self.query_one("#attrs-pane > Tree")
            attrs_tree.action_cursor_up()
            
    def action_focused_panel_left(self) -> None:
        """Handle left movement in the focused panel"""
        # If the tree has focus, use tree's left action (collapse)
        if self.focused and "#tree-pane" in str(self.focused.css_id_selector):
            tree = self.query_one(Tree)
            node = tree.cursor_node
            if node and node.is_expanded:
                node.collapse()  # Use node.collapse() directly
            elif node and node.parent:
                tree.select_node(node.parent)
                tree.scroll_to_node(node.parent)
        
        # If the attribute tree has focus
        elif self.focused and "#attrs-pane" in str(self.focused.css_id_selector):
            attrs_tree = self.query_one("#attrs-pane > Tree")
            node = attrs_tree.cursor_node
            if node and node.is_expanded:
                node.collapse()
            elif node and node.parent:
                attrs_tree.select_node(node.parent)
                attrs_tree.scroll_to_node(node.parent)
                
    def action_focused_panel_right(self) -> None:
        """Handle right movement in the focused panel"""
        # If the tree has focus, use tree's right action (expand)
        if self.focused and "#tree-pane" in str(self.focused.css_id_selector):
            tree = self.query_one(Tree)
            node = tree.cursor_node
            if node and not node.is_expanded and node.allow_expand:
                node.expand()  # Use node.expand() directly
            elif node:
                # When pressing right on a selected node, update the editor
                if node in self.node_data and self.node_data[node].module:
                    self.update_editor_with_module(self.node_data[node].module)
        
        # If the attribute tree has focus
        elif self.focused and "#attrs-pane" in str(self.focused.css_id_selector):
            attrs_tree = self.query_one("#attrs-pane > Tree")
            node = attrs_tree.cursor_node
            if node and not node.is_expanded and node.allow_expand:
                node.expand()
    
    def action_toggle_focused(self) -> None:
        """Toggle the currently focused component or tree node"""
        # If a component item is focused, toggle its switch
        if self.focused and isinstance(self.focused, ComponentListItem):
            self.focused.toggle_switch()
            return
            
        # Otherwise, toggle the tree node
        self.action_toggle_node()
    
    def action_focus_next_pane(self) -> None:
        """Focus the next major pane in the application"""
        # Define the order of panes to cycle through
        panes = []
        
        # Only include visible panes
        if self.label_manager_visible:
            panes.append("label-manager")
        
        panes.append("tree-pane")
        
        if self.code_panel_visible:
            panes.append("code-editor")
            
        if self.attrs_panel_visible:
            panes.append("attrs-pane")
            
        # Find the currently focused pane
        current_index = -1
        current_id = None
        
        if self.focused:
            # Check if we're in a component list item (label manager)
            if isinstance(self.focused, ComponentListItem):
                current_id = "label-manager"
            else:
                # Check based on ID
                for pane_id in panes:
                    if pane_id in str(self.focused.css_id_selector):
                        current_id = pane_id
                        break
        
        # Find the index of the current pane
        if current_id:
            try:
                current_index = panes.index(current_id)
            except ValueError:
                current_index = -1
        
        # Focus the next pane
        if current_index >= 0 and len(panes) > 0:
            next_index = (current_index + 1) % len(panes)
            next_id = panes[next_index]
            
            # Focus the appropriate widget in the next pane
            if next_id == "label-manager":
                items = list(self.query(ComponentListItem))
                if items:
                    items[0].focus()
            elif next_id == "tree-pane":
                tree = self.query_one(Tree)
                tree.focus()
            elif next_id == "code-editor":
                editor = self.query_one("#code-editor > TextArea")
                editor.focus()
            elif next_id == "attrs-pane":
                attrs_tree = self.query_one("#attrs-pane > Tree")
                attrs_tree.focus()
        else:
            # Default to first pane if nothing was focused
            if panes:
                first_id = panes[0]
                if first_id == "label-manager":
                    items = list(self.query(ComponentListItem))
                    if items:
                        items[0].focus()
                elif first_id == "tree-pane":
                    tree = self.query_one(Tree)
                    tree.focus()
    
    def action_focus_prev_pane(self) -> None:
        """Focus the previous major pane in the application"""
        # Define the order of panes to cycle through
        panes = []
        
        # Only include visible panes
        if self.label_manager_visible:
            panes.append("label-manager")
        
        panes.append("tree-pane")
        
        if self.code_panel_visible:
            panes.append("code-editor")
            
        if self.attrs_panel_visible:
            panes.append("attrs-pane")
            
        # Find the currently focused pane
        current_index = -1
        current_id = None
        
        if self.focused:
            # Check if we're in a component list item (label manager)
            if isinstance(self.focused, ComponentListItem):
                current_id = "label-manager"
            else:
                # Check based on ID
                for pane_id in panes:
                    if pane_id in str(self.focused.css_id_selector):
                        current_id = pane_id
                        break
        
        # Find the index of the current pane
        if current_id:
            try:
                current_index = panes.index(current_id)
            except ValueError:
                current_index = -1
        
        # Focus the previous pane
        if current_index >= 0 and len(panes) > 0:
            prev_index = (current_index - 1) % len(panes)
            prev_id = panes[prev_index]
            
            # Focus the appropriate widget in the previous pane
            if prev_id == "label-manager":
                items = list(self.query(ComponentListItem))
                if items:
                    items[0].focus()
            elif prev_id == "tree-pane":
                tree = self.query_one(Tree)
                tree.focus()
            elif prev_id == "code-editor":
                editor = self.query_one("#code-editor > TextArea")
                editor.focus()
            elif prev_id == "attrs-pane":
                attrs_tree = self.query_one("#attrs-pane > Tree")
                attrs_tree.focus()
        else:
            # Default to last pane if nothing was focused
            if panes:
                last_id = panes[-1]
                if last_id == "label-manager":
                    items = list(self.query(ComponentListItem))
                    if items:
                        items[0].focus()
                elif last_id == "tree-pane":
                    tree = self.query_one(Tree)
                    tree.focus()
    
    def action_page_up(self) -> None:
        """Handle Page Up key to scroll the code editor up"""
        # Check if code panel is visible
        if self.code_panel_visible:
            editor = self.query_one("#code-editor > TextArea")
            # Scroll up a page
            editor.scroll_page_up()
    
    def action_page_down(self) -> None:
        """Handle Page Down key to scroll the code editor down"""
        # Check if code panel is visible
        if self.code_panel_visible:
            editor = self.query_one("#code-editor > TextArea")
            # Scroll down a page
            editor.scroll_page_down()
    
    def get_node_path(self, node):
        """Get a clean path representation for a node
        
        Args:
            node: The tree node
            
        Returns:
            str: A formatted module path (e.g., "down_blocks[3].attention")
        """
        if node not in self.node_data:
            return str(node.label)
            
        module_node = self.node_data[node]
            
        # Find the hierarchy of node names from root to this node
        path_parts = []
        current = node
        
        while current and current.parent and current != self.query_one(Tree).root:
            if current in self.node_data:
                data = self.node_data[current]
                if data.name:
                    path_parts.insert(0, data.name)
            current = current.parent
            
        # Join the path parts with dots
        if path_parts:
            return ".".join(path_parts)
        else:
            # Fallback to module type if no path available
            return module_node.module_type
    
    def toggle_node_state(self, node, expand: Optional[bool] = None) -> bool:
        """Toggle or set a node's expand/collapse state
        
        Args:
            node: The tree node to toggle
            expand: If True, expand; if False, collapse; if None, toggle current state
            
        Returns:
            True if action was performed, False otherwise
        """
        if not node:
            return False
            
        # For nodes that don't allow expansion (leaf nodes), we still want to
        # count them as processed for sibling operations
        if not node.allow_expand:
            return True
            
        if expand is None:
            # Toggle current state
            if node.is_expanded:
                node.collapse()
                return True
            elif node.allow_expand:
                node.expand()
                return True
        elif expand and not node.is_expanded and node.allow_expand:
            node.expand()
            return True
        elif not expand and node.is_expanded:
            node.collapse()
            return True
            
        return False
    
    def action_toggle_node(self) -> None:
        """Toggle expand/collapse of selected node"""
        tree = self.query_one(Tree)
        node = tree.cursor_node
        if node and not node.is_expanded and node.allow_expand:
            # When expanding, load the children directly
            if node.data is not None and not node.data.loaded:
                module_entry = node.data
                children = self._get_module_children(module_entry.module)
                if children:
                    # Mark as loaded and populate
                    module_entry.loaded = True
                    self._populate_node_with_children(node, children, module_entry.module)
                    
        # Toggle the node state
        self.toggle_node_state(node)
    
    def toggle_nodes_by_criteria(self, start_node, expand: Optional[bool], 
                            filter_func=None, is_recursive=True, scope_name=None):
        """Generic helper to toggle nodes based on criteria
        
        Args:
            start_node: The node to start processing from
            expand: If True, expand nodes; if False, collapse nodes
            filter_func: Optional function that takes a node and returns True if it should be processed
            is_recursive: If True, process node's descendants; if False, only immediate children
            scope_name: Name of the scope for notification (e.g., "subtree", "siblings", "global")
                        If None, no notification is shown but count is still returned
            
        Returns:
            int: Number of nodes processed
        """
        if not start_node:
            return 0
            
        count = 0
        action = "Expanded" if expand else "Collapsed"
        node_path = self.get_node_path(start_node) if scope_name else ""
        
        def process_node(node, depth=0):
            nonlocal count
            
            # Apply filter if provided
            should_process = filter_func(node) if filter_func else True
            
            # Process the node if it passes the filter
            if should_process and self.toggle_node_state(node, expand):
                count += 1
                
            # Process children if recursive
            if is_recursive:
                for child in node.children:
                    process_node(child, depth + 1)
            elif depth == 0:  # Only process immediate children in non-recursive mode
                for child in node.children:
                    if should_process and self.toggle_node_state(child, expand):
                        count += 1
        
        # Start processing
        process_node(start_node)
        
        # Only show notification if scope_name is provided and count > 0
        if scope_name and count > 0:
            if node_path:
                self.notify(f"{action} {count} nodes in {scope_name} of {node_path}")
            else:
                self.notify(f"{action} {count} nodes in {scope_name}")
                
        # Always return the count
        return count
        
    def process_nodes_recursively(self, start_node, expand: Optional[bool], subtree_only: bool = False) -> int:
        """Process nodes recursively to expand or collapse them
        
        Args:
            start_node: The node to start processing from
            expand: If True, expand nodes; if False, collapse nodes
            subtree_only: If True, only process the subtree under start_node
            
        Returns:
            Number of nodes processed
        """
        # Use the generic helper with recursive mode
        return self.toggle_nodes_by_criteria(
            start_node, 
            expand, 
            is_recursive=True, 
            scope_name=None  # Don't show notification since caller will handle it
        )
    
    def action_toggle_subtree(self) -> None:
        """Toggle fold/unfold the entire subtree under the selected node

        This is triggered by the 'z' key - it should recursively expand or collapse
        the current node and all of its descendants.
        """
        tree = self.query_one(Tree)
        
        # Get the currently selected node
        selected_node = tree.cursor_node
        if not selected_node:
            return
            
        # Special case for root node - always keep it expanded
        is_root = (selected_node == tree.root)
            
        # Check if the selected node is expanded
        expand = not selected_node.is_expanded
        
        # Get the node path for notification
        node_path = self.get_node_path(selected_node)
        
        if expand:
            # EXPANDING: Use our helper function for recursive expansion
            notification = f"Expanded subtree of {node_path}"
            self.recursive_expand_nodes(tree, [selected_node], notification)
        else:
            # COLLAPSING: Use our helper function for recursive collapse
            if is_root:
                # Special case for root - collapse all children but keep root expanded
                # First get all nodes in the tree
                all_nodes = list(tree.walk_tree())
                
                # Collapse all nodes except root using our helper function
                skip_nodes = {tree.root}
                notification = f"Collapsed all nodes except root"
                self.recursive_collapse_nodes(tree, all_nodes, notification, skip_nodes)
                
                # Make sure root stays expanded
                selected_node.expand()
            else:
                # Use our helper function for standard recursive collapse
                notification = f"Collapsed subtree of {node_path}"
                self.recursive_collapse_nodes(tree, [selected_node], notification)
    
    def recursive_expand_nodes(self, tree, start_nodes, notification=None):
        """Recursively expand a list of nodes and all their descendants
        
        Args:
            tree: The tree widget
            start_nodes: A list of nodes to expand recursively 
            notification: Optional notification message to show when complete
            
        Returns:
            int: Number of nodes expanded
        """
        if not start_nodes:
            return 0
            
        # To keep track of how many nodes we expanded
        expanded_count = 0
        
        # Process each start node separately to expand its entire subtree
        for start_node in start_nodes:
            # Skip if the node doesn't allow expansion
            if not start_node.allow_expand:
                continue
                
            # First make sure this node itself is expanded
            if not start_node.is_expanded:
                # Load the node's children if needed
                if start_node.data is not None and not start_node.data.loaded:
                    module_entry = start_node.data
                    children = self._get_module_children(module_entry.module)
                    if children:
                        # Remember which children were previously expanded
                        previously_expanded = module_entry.expanded_children
                        
                        # Load and populate
                        module_entry.loaded = True
                        self._populate_node_with_children(start_node, children, module_entry.module)
                        
                        # Re-expand previously expanded children (will be processed in the queue later)
                        if previously_expanded:
                            for child in start_node.children:
                                if child.data is not None:
                                    # Get the full path of the child
                                    child_path = self.get_node_path(child)
                                    if child_path in previously_expanded:
                                        # Mark for future expansion in the queue
                                        pass  # No action needed here, they will be processed in the queue
                
                # Now expand this node
                start_node.expand()
                expanded_count += 1
            
            # Now do a breadth-first expansion of all descendants
            # Use a FIFO queue to process nodes level by level
            queue = list(start_node.children)  # Start with immediate children
            
            # Process all nodes in the queue
            while queue:
                # Get the next node from the queue
                node = queue.pop(0)
                
                # Only process expandable nodes
                if not node.allow_expand:
                    continue
                
                # If node isn't expanded yet, load its children and expand it
                if not node.is_expanded:
                    # Load children if needed
                    if node.data is not None and not node.data.loaded:
                        module_entry = node.data
                        children = self._get_module_children(module_entry.module)
                        if children:
                            # Remember which children were previously expanded
                            previously_expanded = module_entry.expanded_children
                            
                            # Load and populate
                            module_entry.loaded = True
                            self._populate_node_with_children(node, children, module_entry.module)
                            
                            # Re-expand previously expanded children
                            if previously_expanded:
                                for child in node.children:
                                    if child.data is not None:
                                        # Get the full path of the child
                                        child_path = self.get_node_path(child)
                                        if child_path in previously_expanded:
                                            # Mark these child nodes to be processed by our algorithm
                                            queue.append(child)
                    
                    # Now expand the node
                    node.expand()
                    expanded_count += 1
                
                # Add all this node's children to end of queue for processing
                queue.extend(node.children)
        
        # Show notification if provided
        if notification and expanded_count > 0:
            self.notify(notification)
            
        return expanded_count
    
    def recursive_collapse_nodes(self, tree, start_nodes, notification=None, skip_nodes=None):
        """Recursively collapse a list of nodes and all their descendants
        
        Args:
            tree: The tree widget
            start_nodes: A list of nodes to collapse recursively
            notification: Optional notification message to show when complete
            skip_nodes: Optional set of nodes to skip (won't be collapsed)
            
        Returns:
            int: Number of nodes collapsed
        """
        if not start_nodes:
            return 0
            
        collapsed_count = 0
        
        # Create a set of nodes to skip if provided
        nodes_to_skip = set() if skip_nodes is None else set(skip_nodes)
        
        # Process each start node independently
        for start_node in start_nodes:
            # Skip nodes that shouldn't be processed
            if start_node in nodes_to_skip:
                continue
                
            # Skip nodes that aren't expanded (no point collapsing them)
            if not start_node.is_expanded:
                continue
            
            # First, find all expanded nodes in this subtree that need to be collapsed
            # Starting from deepest nodes, so we don't lose access to nodes when parents collapse
            to_collapse = []
            
            # Helper function to collect all expanded nodes in the subtree
            def collect_expanded(node):
                # Skip nodes that should be excluded
                if node in nodes_to_skip:
                    return
                
                # If node is expanded, add it and check its children
                if node.is_expanded:
                    to_collapse.append(node)
                    # Process all children
                    for child in node.children:
                        collect_expanded(child)
            
            # Collect all expanded nodes in this subtree
            collect_expanded(start_node)
            
            # Collapse nodes from deepest to shallowest to avoid losing access to nodes
            # when a parent collapses (which would remove children from the tree)
            for node in reversed(to_collapse):
                # Before collapsing, save expanded children state for parent nodes
                # that have children which are also expanded
                if node.children and node.data is not None:
                    expanded_children = set()
                    for child in node.children:
                        if child.is_expanded and child.data is not None:
                            # Get the full path of the child
                            child_path = self.get_node_path(child)
                            expanded_children.add(child_path)
                    node.data.expanded_children = expanded_children
                
                node.collapse()
                collapsed_count += 1
        
        # Show notification if provided
        if notification and collapsed_count > 0:
            self.notify(notification)
            
        return collapsed_count
    
    # This function has been removed and replaced by recursive_expand_nodes
    
    def process_pending_loads(self):
        """Force process any pending module loads synchronously.
        
        This ensures that when we're doing recursive operations, all
        nodes get loaded before proceeding with further expansions.
        """
        # This is a simplified synchronous version for immediate load processing
        while not self.load_queue.empty():
            try:
                # Get the next node
                node = self.load_queue.get_nowait()
                
                # Get module information
                module_entry = node.data
                if module_entry is None:
                    continue
                    
                # Skip if already processed
                if module_entry.loaded:
                    continue
                    
                module_entry.loaded = True
                
                # Load children for this module
                children = self._get_module_children(module_entry.module)
                
                # Update the node with children
                if children:
                    self._populate_node_with_children(node, children, module_entry.module)
            except Exception as e:
                # Log any errors but continue processing
                print(f"Error processing module load: {e}")
            finally:
                # Mark as done
                self.load_queue.task_done()

    def action_toggle_all_folds(self) -> None:
        """Toggle all nodes - collapse all if any are expanded, otherwise expand all"""
        tree = self.query_one(Tree)
        
        # Get all nodes in the tree
        all_nodes = list(tree.walk_tree())
        
        # Check if any nodes are expanded (excluding the root node)
        any_expanded = False
        for node in all_nodes:
            if node != tree.root and node.is_expanded:
                any_expanded = True
                break
        
        # If any nodes are expanded, collapse all, otherwise expand all
        expand = not any_expanded
        
        # Create the notification message
        action = "Expanded" if expand else "Collapsed"
        notification = f"{action} all nodes globally"
        
        if expand:
            # Use our helper function to expand all nodes
            self.recursive_expand_nodes(tree, [tree.root], notification)
        else:
            # Collapse all nodes except the root
            skip_nodes = {tree.root}
            self.recursive_collapse_nodes(tree, all_nodes, notification, skip_nodes)
            
            # Make sure root stays expanded
            tree.root.expand()
    
    def action_toggle_siblings(self) -> None:
        """Toggle immediate sibling nodes at the same level as the cursor node"""
        tree = self.query_one(Tree)
        if not tree.cursor_node or not tree.cursor_node.parent:
            return
            
        parent = tree.cursor_node.parent
        current_node = tree.cursor_node
        
        # Determine toggle direction based on node type
        if current_node.allow_expand:
            # For expandable nodes, use their current state
            expand = not current_node.is_expanded
        else:
            # For leaf nodes (not expandable), check siblings to determine direction
            # Default to expanding if there's no expandable sibling
            expand = True
            for sibling in parent.children:
                if sibling.allow_expand:
                    expand = not sibling.is_expanded
                    break
        
        # Toggle all siblings directly - simpler and more reliable
        count = 0
        for sibling in parent.children:
            if self.toggle_node_state(sibling, expand):
                count += 1
                
        # Show notification
        action = "Expanded" if expand else "Collapsed"
        parent_path = self.get_node_path(parent)
        self.notify(f"{action} {count} siblings under {parent_path}")
        
    def action_toggle_all_siblings(self) -> None:
        """Toggle all sibling nodes recursively (including their descendants)"""
        tree = self.query_one(Tree)
        if not tree.cursor_node or not tree.cursor_node.parent:
            return
            
        parent = tree.cursor_node.parent
        current_node = tree.cursor_node
        
        # Determine toggle direction based on node type
        if current_node.allow_expand:
            # For expandable nodes, use their current state
            expand = not current_node.is_expanded
        else:
            # For leaf nodes (not expandable), check siblings to determine direction
            # Default to expanding if there's no expandable sibling
            expand = True
            for sibling in parent.children:
                if sibling.allow_expand:
                    expand = not sibling.is_expanded
                    break
        
        # Create siblings list to expand/collapse recursively
        siblings = list(parent.children)
        
        # Create appropriate notification message
        parent_path = self.get_node_path(parent)
        
        if expand:
            # Use helper function to expand siblings recursively
            notification = f"Expanded all siblings and their descendants under {parent_path}"
            self.recursive_expand_nodes(tree, siblings, notification)
        else:
            # Use helper function to collapse siblings recursively
            notification = f"Collapsed all siblings under {parent_path}"
            self.recursive_collapse_nodes(tree, siblings, notification)
        
    
    def action_toggle_same_class(self) -> None:
        """Toggle all nodes of the same class type globally (non-recursive)"""
        tree = self.query_one(Tree)
        if not tree.cursor_node or tree.cursor_node not in self.node_data:
            return
            
        current_node = tree.cursor_node
        target_module_type = self.node_data[current_node].module_type
        
        # Toggle based on current node's state
        expand = not current_node.is_expanded
        
        # Find all nodes of the target type (just the nodes, not their descendants)
        matching_nodes = []
        
        # Use our walk_tree method to find all nodes
        for node in list(tree.walk_tree()):
            # Check if this node matches the target type
            if node in self.node_data and self.node_data[node].module_type == target_module_type:
                matching_nodes.append(node)
        
        # Create appropriate notification messages
        if expand:
            notification = f"Expanded {len(matching_nodes)} nodes of class {target_module_type} globally"
            # Use our helper function to expand matching nodes (without descendants)
            for node in matching_nodes:
                # Expand just this node (not its children)
                if node.allow_expand and not node.is_expanded:
                    # Load children if needed
                    if node.data is not None and not node.data.loaded:
                        module_entry = node.data
                        children = self._get_module_children(module_entry.module)
                        if children:
                            module_entry.loaded = True
                            self._populate_node_with_children(node, children, module_entry.module)
                    # Expand the node
                    node.expand()
            # Show notification
            self.notify(notification)
        else:
            notification = f"Collapsed {len(matching_nodes)} nodes of class {target_module_type} globally"
            # Collapse just the matching nodes (not their descendants)
            for node in matching_nodes:
                if node.is_expanded:
                    node.collapse()
            # Show notification
            self.notify(notification)
        
    def action_toggle_all_same_class(self) -> None:
        """Toggle all nodes of the same class type and their descendants"""
        tree = self.query_one(Tree)
        if not tree.cursor_node or tree.cursor_node not in self.node_data:
            return
            
        current_node = tree.cursor_node
        target_module_type = self.node_data[current_node].module_type
        
        # Toggle based on current node's state
        expand = not current_node.is_expanded
        
        # Find all nodes of the target type
        matching_nodes = []
        
        # Use our walk_tree method to find all nodes
        for node in list(tree.walk_tree()):
            # Check if this node matches the target type
            if node in self.node_data and self.node_data[node].module_type == target_module_type:
                matching_nodes.append(node)
        
        # Create appropriate notification messages
        if expand:
            notification = f"Expanded all {len(matching_nodes)} {target_module_type} modules and their subtrees"
            # Use our helper function to recursively expand
            self.recursive_expand_nodes(tree, matching_nodes, notification)
        else:
            notification = f"Collapsed all {len(matching_nodes)} {target_module_type} modules"
            # Use our helper function to recursively collapse
            self.recursive_collapse_nodes(tree, matching_nodes, notification)
    
    def update_all_node_labels(self) -> None:
        """Update all node labels in the tree"""
        tree = self.query_one(Tree)
        
        # Check if alignment is active
        any_aligned = any(
            node_data.is_alignment_active() 
            for node_data in self.node_data.values()
        )
        
        if any_aligned:
            # Use the alignment-aware update
            self.update_aligned_node_labels()
        else:
            # Regular update without alignment
            def update_node_label(node):
                if node in self.node_data:
                    node.label = self.node_data[node].get_label()
                for child in node.children:
                    update_node_label(child)
            
            update_node_label(tree.root)
    
    def calculate_aligned_labels(self, parent_node):
        """Calculate alignment for a group of sibling nodes
        
        Args:
            parent_node: The parent node whose children will be aligned
            
        Returns:
            dict: Alignment data for the siblings
        """
        # Skip if parent has no children
        if not parent_node.children:
            return None
            
        # Get all children that are in our node_data
        children = [child for child in parent_node.children if child in self.node_data]
        if not children:
            return None
            
        # Initialize data structures
        component_widths = {}
        active_component_positions = set()
        has_expandable_children = {}
        
        # First pass: track active components and expandable status
        for child in children:
            # Mark nodes with children OR with allow_expand=True
            has_expandable_children[child] = (
                len(child.children) > 0 or 
                getattr(child, 'allow_expand', False)
            )
            
            # Find active components
            node_data = self.node_data[child]
            for i, component in enumerate(node_data.label_components):
                if (isinstance(component, AlignmentComponent) or 
                    not component.active or 
                    not component._get_text(node_data)):
                    continue
                
                # Remember this position
                active_component_positions.add(i)
        
        # Second pass: calculate max widths
        alignment_positions = sorted(active_component_positions)
        
        for child in children:
            node_data = self.node_data[child]
            for i in alignment_positions:
                if i >= len(node_data.label_components):
                    continue
                
                component = node_data.label_components[i]
                if not component.active:
                    continue
                
                # Calculate width and update max
                width = component.get_width(node_data)
                if width > 0:
                    component_widths[i] = max(component_widths.get(i, 0), width)
        
        return {
            "component_widths": component_widths,
            "positions": alignment_positions,
            "has_expandable_children": has_expandable_children
        }
    
    def update_aligned_node_labels(self):
        """Update node labels with alignment between siblings"""
        tree = self.query_one(Tree)
        
        def update_node_group(parent_node):
            # Calculate alignment data for this parent's children
            alignment_data = self.calculate_aligned_labels(parent_node)
            
            # Update each child with alignment data
            for child in parent_node.children:
                if child in self.node_data:
                    # Add the current node to the alignment_data for identifying in get_label
                    if alignment_data:
                        alignment_data["current_node"] = child
                    child.label = self.node_data[child].get_label(alignment_data)
                    
                # Recursively process child's children
                update_node_group(child)
        
        # Start from root (but don't align root itself)
        update_node_group(tree.root)
    
    def _apply_current_component_states_to_node(self, node_data):
        """Apply all current component states to a new node
        
        Args:
            node_data: The ModuleNode to update with current component states
        """
        # Loop through all component states and apply them to this node
        for component_name, component_state in self.component_states.items():
            # Get the component class
            component_class = self._get_component_class_by_name(component_name)
            if not component_class:
                continue
                
            # Apply this component's state to all matching components in the node
            for component in node_data.label_components:
                if isinstance(component, component_class):
                    component.active = component_state.active

    def apply_component_state(self, component_name):
        """Apply the component state to all component instances
        
        Args:
            component_name: The name of the component class to update
        """
        if component_name not in self.component_states:
            return
            
        component_state = self.component_states[component_name]
        is_active = component_state.active
        
        # Get the component class from the class map
        component_class = self._get_component_class_by_name(component_name)  
        if not component_class:
            return
            
        # Apply to all matching components in the tree
        for node, node_data in self.node_data.items():
            for component in node_data.label_components:
                if isinstance(component, component_class):
                    component.active = is_active
    
    def _toggle_component_class(self, component_class):
        """Internal helper to toggle a component class and its subclasses
        
        Args:
            component_class: The component class to toggle
        """
        # Get the component state
        component_name = component_class.__name__
        if component_name not in self.component_states:
            self.notify(f"No components of this type found")
            return
            
        # Toggle the state
        component_state = self.component_states[component_name]
        component_state.toggle()
        
        # Apply the new state to all components in the tree
        self.apply_component_state(component_name)
        
        # Update UI and notify user
        self.update_all_node_labels()
        
        # Update the switch in the corresponding component list item
        if self.label_manager_visible:
            try:
                # Find the component list item for this component
                item = self.query_one(f"#item-{component_name}")
                if item:
                    # Focus the item (which will also update its appearance)
                    item.focus()
                    
                    # Update the switch value
                    switch = item.query_one(Switch)
                    if switch:
                        switch.value = component_state.active
            except Exception:
                # Just continue if there's an error - no need to bind the exception
                pass
            
        status = "Showing" if component_state.active else "Hiding"
        self.notify(f"{status} {component_state.display_name}")
    
    def action_toggle_param_shapes(self) -> None:
        """Toggle parameter shapes display"""
        self.toggle_component("ParamShapesComponent")
        
    def action_toggle_memory(self) -> None:
        """Toggle all memory-related components (total, percentage, and self)"""
        # Toggle all memory components at once
        memory_components = [
            "SizeLabelComponent",        # Total memory
            "MemoryPercentComponent",    # Memory percentage
            "SelfMemoryComponent"        # Self memory
        ]
        
        # Check if any memory component is already active
        any_active = False
        for name in memory_components:
            if name in self.component_states and self.component_states[name].active:
                any_active = True
                break
                
        # Set the new state to the opposite of the current state
        new_state = not any_active
        
        # Toggle each component
        for name in memory_components:
            if name in self.component_states:
                self.component_states[name].set_active(new_state)
                self.apply_component_state(name)
                
        # Update tree display
        self.update_all_node_labels()
        
        # Show notification
        status = "Showing" if new_state else "Hiding"
        self.notify(f"{status} memory information")
    
    def action_toggle_params(self) -> None:
        """Toggle parameter count display (total, percentage, and self)"""
        # Toggle all parameter-related components
        param_components = [
            "ParamCountComponent",      # Total parameters
            "ParamPercentComponent",    # Parameter percentage
            "SelfParamCountComponent"   # Self parameters
        ]
        
        # Check if any parameter component is already active
        any_active = False
        for name in param_components:
            if name in self.component_states and self.component_states[name].active:
                any_active = True
                break
                
        # Set the new state to the opposite of the current state
        new_state = not any_active
        
        # Toggle each component
        for name in param_components:
            if name in self.component_states:
                self.component_states[name].set_active(new_state)
                self.apply_component_state(name)
                
        # Update tree display
        self.update_all_node_labels()
        
        # Show notification
        status = "Showing" if new_state else "Hiding"
        self.notify(f"{status} parameter information")
        
    def action_toggle_device(self) -> None:
        """Toggle device and dtype display"""
        # Toggle both device and dtype components
        device_state = self.component_states.get("DeviceLabelComponent")
        dtype_state = self.component_states.get("ModuleDTypeComponent")
        
        # Determine new state based on device component
        new_state = not device_state.active if device_state else True
        
        # Update both components
        if device_state:
            device_state.set_active(new_state)
            self.apply_component_state("DeviceLabelComponent")
            
        if dtype_state:
            dtype_state.set_active(new_state)
            self.apply_component_state("ModuleDTypeComponent")
        
        # Update tree display
        self.update_all_node_labels()
        
        # Show notification
        status = "Showing" if new_state else "Hiding"
        self.notify(f"{status} device and dtype information")
        
    def action_toggle_input_shape(self) -> None:
        """Toggle input shape display"""
        self.toggle_component("ForwardInputShapeComponent")
        
    def action_toggle_output_shape(self) -> None:
        """Toggle output shape display"""
        self.toggle_component("ForwardOutputShapeComponent")
        
    def action_toggle_call_count(self) -> None:
        """Toggle call count display"""
        self.toggle_component("ForwardCallCountComponent")
    
    def _get_component_class_by_name(self, class_name):
        """Get component class by name from the class map
        
        Args:
            class_name: Name of the component class
            
        Returns:
            The component class or None if not found
        """
        return self.component_class_map.get(class_name)

    def action_toggle_runtime(self) -> None:
        """Toggle all runtime components at once"""
        # Get all runtime component states
        runtime_components = [
            "ForwardRuntimeComponent",
            "AvgSelfRuntimeComponent",
            "TotalRuntimeComponent",
            "RuntimePercentComponent",
            "AvgTotalRuntimeComponent"
        ]
        
        # Find any active component to determine direction
        any_active = False
        for name in runtime_components:
            if name in self.component_states and self.component_states[name].active:
                any_active = True
                break
                
        # Set all components to the opposite state
        new_state = not any_active
        
        # Toggle each component - callbacks will handle UI updates
        for name in runtime_components:
            if name in self.component_states:
                # Set the state directly without toggling
                self.component_states[name].set_active(new_state)
                # Apply to actual components in the tree nodes
                self.apply_component_state(name)
        
        # Update tree display
        self.update_all_node_labels()
        
        # Show notification
        status = "Showing" if new_state else "Hiding"
        self.notify(f"{status} all runtime components")
        
    def action_toggle_forward_stats(self) -> None:
        """Toggle all forward stats components at once"""
        # Get all forward stats component states
        forward_components = [
            "ForwardInputShapeComponent",
            "ForwardOutputShapeComponent", 
            "ForwardCallCountComponent"
        ]
        
        # Find any active component to determine direction
        any_active = False
        for name in forward_components:
            if name in self.component_states and self.component_states[name].active:
                any_active = True
                break
                
        # Set all components to the opposite state
        new_state = not any_active
        
        # Toggle each component - callbacks will handle UI updates
        for name in forward_components:
            if name in self.component_states:
                # Set the state directly without toggling
                self.component_states[name].set_active(new_state)
                # Apply to actual components in the tree nodes
                self.apply_component_state(name)
        
        # Update tree display
        self.update_all_node_labels()
        
        # Show notification
        status = "Showing" if new_state else "Hiding"
        self.notify(f"{status} all forward stats")
    
    def action_toggle_alignment(self) -> None:
        """Toggle node label alignment for siblings"""
        self.toggle_component("AlignmentComponent")
        
        # Update UI with alignment
        self.update_all_node_labels()
        
    def action_toggle_attrs_panel(self) -> None:
        """Toggle visibility of the attributes panel"""
        # Get attributes pane and code editor
        attrs_pane = self.query_one("#attrs-pane")
        attrs_title = self.query_one("#attrs-title")
        code_editor = self.query_one("#code-editor")
        
        # Toggle attributes panel visibility flag
        self.attrs_panel_visible = not self.attrs_panel_visible
        
        # If label manager is open, ensure the editor pane is visible when enabling attrs panel
        if self.label_manager_visible and self.attrs_panel_visible:
            editor_pane = self.query_one("#editor-pane")
            editor_pane.display = True
        
        # Update layout based on which panels are visible
        self.update_panel_layout()
    
    def action_toggle_code_panel(self) -> None:
        """Toggle visibility of the code panel"""
        # Toggle code panel visibility flag
        self.code_panel_visible = not self.code_panel_visible
        
        # If label manager is open, ensure the editor pane is visible when enabling code panel
        if self.label_manager_visible and self.code_panel_visible:
            editor_pane = self.query_one("#editor-pane")
            editor_pane.display = True
        
        # Update layout based on which panels are visible
        self.update_panel_layout()
        
    
    
    def move_component_up(self, component_item):
        """Move a component up in the list
        
        Args:
            component_item: The ComponentListItem to move up
        """
        try:
            # Try to get component name from the item directly
            if hasattr(component_item, 'component_state') and hasattr(component_item.component_state, 'component_class'):
                component_name = component_item.component_state.component_class.__name__
            else:
                # If we got a highlighted widget instead, get the index and determine component from there
                list_view = self.query_one("#component-list")
                if list_view and list_view.highlighted_child:
                    index = list_view.children.index(list_view.highlighted_child)
                    if 0 <= index < len(self.component_classes):
                        component_name = self.component_classes[index].__name__
                    else:
                        self.notify("Cannot determine which component to move")
                        return
                else:
                    self.notify("No component selected")
                    return
            
            # Find the index of this component in our component_classes list
            component_class = self._get_component_class_by_name(component_name)
            if not component_class:
                self.notify(f"Component {component_name} not found")
                return
                
            current_index = self.component_classes.index(component_class)
            
            # Don't move if already at the top
            if current_index <= 0:
                self.notify(f"Component already at the top")
                return
                
            # Swap positions in the component_classes list
            self.component_classes[current_index], self.component_classes[current_index-1] = \
                self.component_classes[current_index-1], self.component_classes[current_index]
                
            # Update ModuleNode.component_classes to match
            ModuleNode.component_classes[current_index], ModuleNode.component_classes[current_index-1] = \
                ModuleNode.component_classes[current_index-1], ModuleNode.component_classes[current_index]
                
            # Rebuild the label manager UI
            self.init_label_manager()
            
            # Rebuild all node labels with the new order
            self._rebuild_node_components()
            
            # Update the tree display
            self.update_all_node_labels()
            
            # Update the selection in the list - now points to the new position (current_index-1)
            self.call_after_refresh(lambda: self._focus_component_item(current_index-1))
            
            # Show notification
            self.notify(f"Moved {component_name} up")
        except Exception as e:
            # Log any errors
            print(f"Error moving component up: {e}")
            self.notify(f"Error moving component: {str(e)}")
    
    def move_component_down(self, component_item):
        """Move a component down in the list
        
        Args:
            component_item: The ComponentListItem to move down
        """
        try:
            # Try to get component name from the item directly
            if hasattr(component_item, 'component_state') and hasattr(component_item.component_state, 'component_class'):
                component_name = component_item.component_state.component_class.__name__
            else:
                # If we got a highlighted widget instead, get the index and determine component from there
                list_view = self.query_one("#component-list")
                if list_view and list_view.highlighted_child:
                    index = list_view.children.index(list_view.highlighted_child)
                    if 0 <= index < len(self.component_classes):
                        component_name = self.component_classes[index].__name__
                    else:
                        self.notify("Cannot determine which component to move")
                        return
                else:
                    self.notify("No component selected")
                    return
            
            # Find the index of this component in our component_classes list
            component_class = self._get_component_class_by_name(component_name)
            if not component_class:
                self.notify(f"Component {component_name} not found")
                return
                
            current_index = self.component_classes.index(component_class)
            
            # Don't move if already at the bottom
            if current_index >= len(self.component_classes) - 1:
                self.notify(f"Component already at the bottom")
                return
                
            # Swap positions in the component_classes list
            self.component_classes[current_index], self.component_classes[current_index+1] = \
                self.component_classes[current_index+1], self.component_classes[current_index]
                
            # Update ModuleNode.component_classes to match
            ModuleNode.component_classes[current_index], ModuleNode.component_classes[current_index+1] = \
                ModuleNode.component_classes[current_index+1], ModuleNode.component_classes[current_index]
                
            # Rebuild the label manager UI
            self.init_label_manager()
            
            # Rebuild all node labels with the new order
            self._rebuild_node_components()
            
            # Update the tree display
            self.update_all_node_labels()
            
            # Update the selection in the list - now points to the new position (current_index+1)
            self.call_after_refresh(lambda: self._focus_component_item(current_index+1))
            
            # Show notification
            self.notify(f"Moved {component_name} down")
        except Exception as e:
            # Log any errors
            print(f"Error moving component down: {e}")
            self.notify(f"Error moving component: {str(e)}")
            
    def move_component_to_top(self, component_item):
        """Move a component to the top of the list
        
        Args:
            component_item: The ComponentListItem to move to the top
        """
        try:
            # Try to get component name from the item directly
            if hasattr(component_item, 'component_state') and hasattr(component_item.component_state, 'component_class'):
                component_name = component_item.component_state.component_class.__name__
            else:
                # If we got a highlighted widget instead, get the index and determine component from there
                list_view = self.query_one("#component-list")
                if list_view and list_view.highlighted_child:
                    index = list_view.children.index(list_view.highlighted_child)
                    if 0 <= index < len(self.component_classes):
                        component_name = self.component_classes[index].__name__
                    else:
                        self.notify("Cannot determine which component to move")
                        return
                else:
                    self.notify("No component selected")
                    return
            
            # Find the index of this component in our component_classes list
            component_class = self._get_component_class_by_name(component_name)
            if not component_class:
                self.notify(f"Component {component_name} not found")
                return
                
            current_index = self.component_classes.index(component_class)
            
            # Don't move if already at the top
            if current_index <= 0:
                self.notify(f"Component already at the top")
                return
                
            # Remove from current position and insert at the top
            component_item = self.component_classes.pop(current_index)
            self.component_classes.insert(0, component_item)
            
            # Do the same with ModuleNode.component_classes
            module_node_item = ModuleNode.component_classes.pop(current_index)
            ModuleNode.component_classes.insert(0, module_node_item)
                
            # Rebuild the label manager UI
            self.init_label_manager()
            
            # Rebuild all node labels with the new order
            self._rebuild_node_components()
            
            # Update the tree display
            self.update_all_node_labels()
            
            # Update the selection in the list - now points to the top
            self.call_after_refresh(lambda: self._focus_component_item(0))
            
            # Show notification
            self.notify(f"Moved {component_name} to top")
        except Exception as e:
            # Log any errors
            print(f"Error moving component to top: {e}")
            self.notify(f"Error moving component: {str(e)}")
            
    def move_component_to_bottom(self, component_item):
        """Move a component to the bottom of the list
        
        Args:
            component_item: The ComponentListItem to move to the bottom
        """
        try:
            # Try to get component name from the item directly
            if hasattr(component_item, 'component_state') and hasattr(component_item.component_state, 'component_class'):
                component_name = component_item.component_state.component_class.__name__
            else:
                # If we got a highlighted widget instead, get the index and determine component from there
                list_view = self.query_one("#component-list")
                if list_view and list_view.highlighted_child:
                    index = list_view.children.index(list_view.highlighted_child)
                    if 0 <= index < len(self.component_classes):
                        component_name = self.component_classes[index].__name__
                    else:
                        self.notify("Cannot determine which component to move")
                        return
                else:
                    self.notify("No component selected")
                    return
            
            # Find the index of this component in our component_classes list
            component_class = self._get_component_class_by_name(component_name)
            if not component_class:
                self.notify(f"Component {component_name} not found")
                return
                
            current_index = self.component_classes.index(component_class)
            
            # Don't move if already at the bottom
            if current_index >= len(self.component_classes) - 1:
                self.notify(f"Component already at the bottom")
                return
                
            # Remove from current position and append to the end
            component_item = self.component_classes.pop(current_index)
            self.component_classes.append(component_item)
            
            # Do the same with ModuleNode.component_classes
            module_node_item = ModuleNode.component_classes.pop(current_index)
            ModuleNode.component_classes.append(module_node_item)
                
            # Rebuild the label manager UI
            self.init_label_manager()
            
            # Rebuild all node labels with the new order
            self._rebuild_node_components()
            
            # Update the tree display
            self.update_all_node_labels()
            
            # Update the selection in the list - now points to the bottom
            bottom_index = len(self.component_classes) - 1
            self.call_after_refresh(lambda: self._focus_component_item(bottom_index))
            
            # Show notification
            self.notify(f"Moved {component_name} to bottom")
        except Exception as e:
            # Log any errors
            print(f"Error moving component to bottom: {e}")
            self.notify(f"Error moving component: {str(e)}")
    
    def _rebuild_node_components(self):
        """Rebuild all node components to reflect the new order"""
        for node, node_data in self.node_data.items():
            # Create new label components in the new order
            new_components = []
            component_states = {}
            
            # Save the active state of existing components
            for component in node_data.label_components:
                component_name = component.__class__.__name__
                component_states[component_name] = component.active
            
            # Create new components in the updated order
            for component_class in self.component_classes:
                component_name = component_class.__name__
                # Initialize with saved state (default to current class default if not found)
                is_active = component_states.get(component_name, None)
                
                # Check if this component class accepts the 'active' parameter
                # ModuleNameComponent, ModuleTypeNameComponent, and ModuleTypeArgsComponent don't accept it
                if component_name in ('ModuleNameComponent', 'ModuleTypeNameComponent', 'ModuleTypeArgsComponent'):
                    # These components don't take an active parameter in constructor
                    component = component_class()
                    # But we can set the active state after creation if we have it
                    if is_active is not None:
                        component.active = is_active
                else:
                    # For other components that accept the active parameter
                    if is_active is None:
                        # Get default from class definition
                        component = component_class()
                    else:
                        # Use saved active state
                        component = component_class(active=is_active)
                    
                new_components.append(component)
            
            # Update the node's components
            node_data.label_components = new_components
    
    def _focus_component_item(self, index):
        """Focus a specific component item by index and ensure it's highlighted
        
        Args:
            index: Index of the component item to focus
        """
        try:
            # Get the list view first
            list_view = self.query_one("#component-list")
            if not list_view:
                return

            list_view.index = index

                
            # Get all component items
            items = list(list_view.children)
            if 0 <= index < len(items):
                # Set the highlighted item directly on the list view
                list_view.index = index
                
                # Focus the list view itself
                list_view.focus()
                
                # # Ensure the item is visible by scrolling to it
                # list_view.scroll_to_child(index)
        except Exception as e:
            # Log the error but continue
            self.notify(f"Error focusing component item: {e}")
            pass
            
    def toggle_component(self, component_name):
        """Toggle a component by name - central method for all component toggling
        
        Args:
            component_name: Name of the component class
        """
        if component_name not in self.component_states:
            return
            
        # Toggle the state - this will trigger UI callbacks automatically
        component_state = self.component_states[component_name]
        component_state.toggle()
        
        # Update component in tree nodes
        self.apply_component_state(component_name)
        
        # Update tree display
        self.update_all_node_labels()
        
        # Show notification
        status = "Showing" if component_state.active else "Hiding"
        self.notify(f"{status} {component_state.display_name}")
    
    def action_toggle_label_manager(self) -> None:
        """Toggle the label manager panel"""
        # Toggle visibility state
        previous_state = self.label_manager_visible
        self.label_manager_visible = not previous_state
        
        # Update the UI
        self.update_panel_layout()
        
        # Set focus based on the action
        if self.label_manager_visible:
            # If we just turned on the label manager, update the instructions
            try:
                instructions = self.query_one("#label-instructions")
                instructions.update("Choose what you want to see!\nClick labels or use keyboard shortcuts\nUse ⇧J/⇧K to move up/down, ⇧T/⇧B for top/bottom")
            except Exception:
                # If instructions not found, it's fine to continue
                pass
            
            # Focus the list view
            list_view = self.query_one("#component-list")
            if list_view:
                list_view.focus()
                
                # Then try to focus the first item specifically
                self.call_after_refresh(self._focus_first_component_item)
        elif previous_state:
            # If we just turned off the label manager, focus the tree
            tree = self.query_one("#tree-pane > HJKLTree")
            tree.focus()
            
    def action_show_help(self) -> None:
        """Show the help documentation modal dialog"""
        self.push_screen(HelpScreen())
            
    def _focus_first_component_item(self):
        """Helper method to focus the first component item after UI refresh"""
        try:
            items = list(self.query(ComponentListItem))
            if items and len(items) > 0:
                items[0].focus()
        except Exception:
            # Silently fail if there's an issue focusing
            pass
    
    def action_expand_right_panel(self) -> None:
        """Expand the right panel (editor pane) by increasing its width"""
        if not self.code_panel_visible and not self.attrs_panel_visible:
            # Right panel is not even visible
            return
            
        # Increase width by step size
        self.right_panel_width = min(self.right_panel_width + self.right_panel_step, self.max_right_panel_width)
        
        # Update layout
        self.update_panel_layout()
        
    def action_contract_right_panel(self) -> None:
        """Contract the right panel (editor pane) by decreasing its width"""
        if not self.code_panel_visible and not self.attrs_panel_visible:
            # Right panel is not even visible
            return
            
        # Decrease width by step size
        self.right_panel_width = max(self.right_panel_width - self.right_panel_step, self.min_right_panel_width)
        
        # Update layout
        self.update_panel_layout()
        
    def update_panel_layout(self) -> None:
        """Update the layout based on which panels are visible"""
        # Get all the relevant panes
        label_manager = self.query_one("#label-manager")
        editor_pane = self.query_one("#editor-pane")
        tree_pane = self.query_one("#tree-pane")
        code_editor = self.query_one("#code-editor")
        attrs_pane = self.query_one("#attrs-pane")
        attrs_title = self.query_one("#attrs-title")
        
        # Handle label manager visibility
        if self.label_manager_visible:
            label_manager.display = True
            tree_pane.styles.width = "40%"
            
            # Check if either right panel should be visible
            if self.code_panel_visible or self.attrs_panel_visible:
                editor_pane.display = True
                editor_pane.styles.width = "45%"
            else:
                editor_pane.display = False
                tree_pane.styles.width = "75%"
        else:
            label_manager.display = False
            
            # Handle visibility of the right panel
            if not self.code_panel_visible and not self.attrs_panel_visible:
                # Hide the entire right panel
                editor_pane.display = False
                tree_pane.styles.width = "100%"
                return
            
            # Show the right panel with the current width
            editor_pane.display = True
            editor_pane.styles.width = f"{self.right_panel_width}%"
            tree_pane.styles.width = f"{100 - self.right_panel_width}%"
        
        # Handle code editor visibility
        if self.code_panel_visible:
            code_editor.display = True
            if self.attrs_panel_visible:
                # Both panels visible
                code_editor.styles.height = "2fr"
            else:
                # Only code panel visible
                code_editor.styles.height = "1fr"
        else:
            code_editor.display = False
        
        # Handle attributes panel visibility
        if self.attrs_panel_visible:
            attrs_pane.display = True
            attrs_title.display = True
            attrs_pane.styles.height = "1fr"
        else:
            attrs_pane.display = False
            attrs_title.display = False



def is_torch_module(obj):
    """Check if an object is a PyTorch module
    
    Args:
        obj: The object to check
        
    Returns:
        bool: True if obj is a PyTorch module, False otherwise
    """
    try:
        import torch.nn
        return isinstance(obj, torch.nn.Module)
    except (ImportError, AttributeError):
        return False


class ModuleWrapper(torch.nn.Module):
    """
    Wraps a non-module object to make it look like a PyTorch module.
    Only PyTorch modules in the object's __dict__ will be exposed as children.
    """
    def __init__(self, obj):
        """
        Initialize the wrapper with an object
        
        Args:
            obj: The object to wrap
        """
        super().__init__()
        self.wrapped_obj = obj
        
        # Extract all torch modules from the object's __dict__
        if hasattr(obj, "__dict__"):
            for name, value in obj.__dict__.items():
                if is_torch_module(value):
                    # Add each module as a child module of this wrapper
                    self.add_module(name, value)
    
    def _get_name(self):
        """Return the class name of the wrapped object"""
        return f"{self.wrapped_obj.__class__.__name__}Wrapper"
    
    def extra_repr(self):
        """Show what object is being wrapped"""
        return f"wrapped_type={self.wrapped_obj.__class__.__name__}"
    
    def forward(self, *args, **kwargs):
        """Forward method - not used but required for nn.Module"""
        raise NotImplementedError("ModuleWrapper is for visualization only")


def explore_module(obj):
    """
    Start the interactive module explorer
    
    Args:
        obj: Either a PyTorch module or an object containing PyTorch modules
            in its __dict__ (like models with multiple components)
            
    Example:
        # Regular module usage
        import torch
        model = torch.nn.Sequential(
            torch.nn.Linear(10, 20), 
            torch.nn.ReLU()
        )
        explore_module(model)
        
        # Non-module object containing modules
        class ModelContainer:
            def __init__(self):
                self.encoder = torch.nn.Linear(10, 20)
                self.decoder = torch.nn.Linear(20, 10)
                self.other_attr = "not a module"
                
        container = ModelContainer()
        explore_module(container)  # Will show encoder and decoder modules
    """
    # If the object is not a module but has modules in its __dict__, wrap it
    if not is_torch_module(obj):
        # Check if it has any modules in its __dict__
        has_modules = False
        if hasattr(obj, "__dict__"):
            for value in obj.__dict__.values():
                if is_torch_module(value):
                    has_modules = True
                    break
        
        if has_modules:
            obj = ModuleWrapper(obj)
    
    # Run the explorer with the object (wrapped if needed)
    app = ModelTreeViewer(obj)
    app.run()


def explore_torch_module_with_stats(obj, *args, **kwargs):
    """
    Run a forward pass and then explore the module. If torch_hooks has been used
    to collect forward_stats, they will be displayed when pressing 'f'.
    
    Usage example:
        import torch
        import rp
        from rp.libs.torch_hooks import stats_collection
        from rp.libs.pytorch_module_explorer import explore_torch_module_with_stats
        
        # Create your model
        model = torch.nn.Sequential(
            torch.nn.Linear(10, 20),
            torch.nn.ReLU(),
            torch.nn.Linear(20, 1)
        )
        
        # Create sample input data
        x = torch.randn(32, 10)
        
        # Method 1: Use explore_torch_module_with_stats directly
        # This simply runs a forward pass and then explores the module
        explore_torch_module_with_stats(model, x)
        
        # Method 2: Collect stats with torch_hooks first
        # This attaches hooks to collect stats during the forward pass
        with rp.libs.torch_hooks.stats_collection(model):
            model(x)
        # Then explore the module with the collected stats
        explore_module(model)
        
        # Method 3: Non-module container with modules
        class ModelContainer:
            def __init__(self):
                self.model = torch.nn.Sequential(
                    torch.nn.Linear(10, 20),
                    torch.nn.ReLU()
                )
            def forward(self, x):
                return self.model(x)
                
        container = ModelContainer()
        # Run with stats collection on the inner model
        with rp.libs.torch_hooks.stats_collection(container.model):
            container.forward(x)
        # Then explore the container
        explore_module(container)
    """
    # For non-module objects with a callable/runnable module attribute
    if not is_torch_module(obj) and hasattr(obj, "__dict__"):
        # Try to identify a main module to run the forward pass on
        main_module = None
        for name, value in obj.__dict__.items():
            if is_torch_module(value):
                main_module = value
                break
                
        # If we found a module and have input data, run the forward pass on it
        if main_module is not None and len(args) > 0:
            main_module(*args, **kwargs)
    
    # For regular module objects, run the forward pass directly
    elif is_torch_module(obj) and len(args) > 0:
        # Run a forward pass (no stats collection on its own)
        obj(*args, **kwargs)
    
    # Now explore the module or wrapped object (will show forward_stats if they exist)
    explore_module(obj)


if __name__ == "__main__":
    # Load the model
    import diffusers
    model = diffusers.CogVideoXTransformer3DModel()
    
    # Run the interactive explorer
    explore_module(model)
