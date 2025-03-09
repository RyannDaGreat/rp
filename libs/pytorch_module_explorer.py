import rp
rp.pip_import('textual')
rp.pip_import('textual','textual[syntax]')
rp.pip_import('rich')
rp.pip_import('numpy')

# torch_hooks module and pytorch_module_explorer are kept separate
# but pytorch_module_explorer can display forward_stats if present

# No time formatting needed

def format_shape(shape):
    """Format a shape tuple consistently with proper multiplication symbols"""
    return "×".join(str(dim) for dim in shape) if shape else ""


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
    style = "bold purple"
    
    def _get_text(self, module_node):
        return module_node.device_label if module_node.device_label else ""


class SizeLabelComponent(NodeLabelComponent):
    """Component for displaying module size"""
    display_name = "Size Information"
    description = "Shows the memory size of the module's parameters"
    example = "1.2MB"
    shortcut_key = "b"
    style = "bold green"
    
    def _get_text(self, module_node):
        if module_node.size_bytes > 0:
            return rp.human_readable_file_size(module_node.size_bytes)
        return ""


class ForwardStatsComponent(NodeLabelComponent):
    """Base class for all forward stats components"""
    display_name = "Forward Statistics"
    description = "Base class for components showing forward pass statistics"
    example = "Stats"
    shortcut_key = "f"
    style = "orange1"


class ForwardInputShapeComponent(ForwardStatsComponent):
    """Component for displaying forward pass input shape"""
    display_name = "Input Shape"
    description = "Shows the shape of input tensors passing through this module"
    example = "in=2×320×64×64"
    shortcut_key = "1"
    
    def _get_text(self, module_node):
        if not module_node.module:
            return ""
        
        if not hasattr(module_node.module, "forward_stats") or not module_node.module.forward_stats:
            return ""
            
        # Get the most recent forward stats
        stats = module_node.module.forward_stats[-1]
        
        # Add input shape if available
        if hasattr(stats, "in_shape"):
            input_shape_str = format_shape(stats.in_shape)
            return f"in={input_shape_str}"
        return ""


class ForwardOutputShapeComponent(ForwardStatsComponent):
    """Component for displaying forward pass output shape"""
    display_name = "Output Shape"
    description = "Shows the shape of output tensors produced by this module"
    example = "out=2×320×64×64"
    shortcut_key = "2"
    
    def _get_text(self, module_node):
        if not module_node.module:
            return ""
        
        if not hasattr(module_node.module, "forward_stats") or not module_node.module.forward_stats:
            return ""
            
        # Get the most recent forward stats
        stats = module_node.module.forward_stats[-1]
        
        # Add output shape if available
        if hasattr(stats, "out_shape"):
            output_shape_str = format_shape(stats.out_shape)
            return f"out={output_shape_str}"
        return ""


class ForwardCallCountComponent(ForwardStatsComponent):
    """Component for displaying forward pass call count"""
    display_name = "Call Count"
    description = "Shows how many times this module has been called"
    example = "(5 calls)"
    shortcut_key = "3"
    
    def _get_text(self, module_node):
        if not module_node.module:
            return ""
        
        if not hasattr(module_node.module, "forward_stats") or not module_node.module.forward_stats:
            return ""
            
        # Include call count if more than one
        calls = len(module_node.module.forward_stats)
        if calls > 1:
            return f"({calls} calls)"
        return ""


class ModuleNameComponent(NodeLabelComponent):
    """Component for displaying the module name"""
    display_name = "Module Name"
    description = "Shows the module's name (always visible)"
    example = "(conv_in)"
    shortcut_key = None  # Always on, no toggle
    style = "bold yellow"
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
    display_name = "Module Type"
    description = "Shows the module's class name and constructor args (always visible)"
    example = "Conv2d(320, 4, kernel_size=3)"
    shortcut_key = "m"
    
    def __init__(self):
        # Module type components are always active
        super().__init__(active=True)
        
    def toggle_active(self):
        """Module type can't be toggled off"""
        return True


class ModuleTypeNameComponent(ModuleTypeBaseComponent):
    """Component for displaying the module class name"""
    style = "cyan"
    suffix = ""  # No space between type name and args
    
    def _get_text(self, module_node):
        return module_node.module_type


class ModuleTypeArgsComponent(ModuleTypeBaseComponent):
    """Component for displaying the module arguments"""
    style = "blue"
    
    def _get_text(self, module_node):
        if module_node.extra_info:
            return f"({module_node.extra_info})"
        return ""


class ParamShapesComponent(NodeLabelComponent):
    """Component for displaying parameter shapes"""
    display_name = "Parameter Shapes"
    description = "Shows the shapes of module parameters like weight and bias tensors"
    example = "weight: 4×320×3×3, bias: 4"
    shortcut_key = "t"
    style = "param-shape"
    prefix = " | "
    suffix = ""
    
    def _get_text(self, module_node):
        return module_node.state_dict_info if module_node.state_dict_info else ""


class ParamCountComponent(NodeLabelComponent):
    """Component for displaying parameter count"""
    display_name = "Parameter Count"
    description = "Shows the number of parameters in the module"
    example = "1.7M"
    shortcut_key = "p"
    style = "bold magenta"
    suffix = " "
    
    def _get_text(self, module_node):
        # Get parameter count from module_node's param_count property
        if hasattr(module_node, 'param_count') and module_node.param_count > 0:
            # Format the parameter count in a human-readable way
            return self.format_param_count(module_node.param_count)
        return ""
    
    def format_param_count(self, count):
        """Format parameter count as human-readable (e.g., 1.7M, 5.4B)"""
        if count < 1000:
            return f"{count}"
        elif count < 1_000_000:
            return f"{count/1000:.1f}K"
        elif count < 1_000_000_000:
            return f"{count/1_000_000:.1f}M"
        else:
            return f"{count/1_000_000_000:.1f}B"


class AlignmentComponent(NodeLabelComponent):
    """Component for aligning sibling nodes vertically"""
    display_name = "Alignment"
    description = "Aligns sibling nodes vertically by adding whitespace"
    example = "(aligned)"
    shortcut_key = "A"
    prefix = ""
    suffix = ""
    
    def _get_text(self, module_node):
        """Alignment component is special - it returns padding to align with siblings"""
        # Actual alignment calculation is done in ModuleNode.get_label()
        # This just returns an empty string as the text itself
        return ""

from textual.app import App, ComposeResult
from textual.widgets import Tree, Footer, Static, Button
from textual.binding import Binding 
from textual.containers import Horizontal, Vertical, Container
from textual.widgets._text_area import TextArea
from textual.reactive import reactive
from textual._text_area_theme import TextAreaTheme
from typing import Dict, Optional, Any, List, Tuple
import torch
from rich.text import Text
from rich.pretty import Pretty
from rich.console import Console
from rich.style import Style
from io import StringIO
import inspect
import numpy as np




class AttributeTree:
    """Helper class to build and manage attribute trees"""
    
    def __init__(self, tree_widget: Tree):
        """Initialize with a tree widget
        
        Args:
            tree_widget: The Tree widget to populate
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


def get_module_device_label(module):
    if module is None:
        return ''

    if hasattr(module, 'device'):
        return str(module.device)

    devices = set(x.device for x in module.parameters())
    devices = set(map(str,devices))
    
    #Condense down any combination of cuda:1, cuda:2, cuda:3 to cuda:1,2,3
    cuda_labels = set()
    cuda_devices = set(x for x in devices if x.startswith('cuda:'))
    if cuda_devices:
        cuda_numbers = ','.join(sorted(x.strip('cuda:') for x in cuda_devices))
        cuda_labels |= {f'cuda:{cuda_numbers}'}

    other_devices = devices - cuda_devices
    other_labels = set(map(str, other_devices))

    return '/'.join(sorted(other_labels | cuda_labels))
        


    

class ModuleNode:
    """Node representing a PyTorch module"""
    # Define component classes with their default active states
    # Ordered by how they appear in the label
    component_classes = [
        (DeviceLabelComponent, False),
        (SizeLabelComponent, True),
        (ParamCountComponent, True),  # Add parameter count display
        (ForwardInputShapeComponent, False),
        (ForwardOutputShapeComponent, False),
        (ForwardCallCountComponent, False),
        (ModuleNameComponent, None),  # None means use default constructor
        (ModuleTypeNameComponent, None),  # None means use default constructor
        (ModuleTypeArgsComponent, None),  # None means use default constructor
        (ParamShapesComponent, True),
        (AlignmentComponent, False)  # Alignment off by default
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
        self.device_label = get_module_device_label(module)
        
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
        
        # Add alignment prefix for nodes without children
        if current_node and not has_expandable_children.get(current_node, False):
            label_parts.append("│ ")
        
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
    """Class to manage state for a component type"""
    
    def __init__(self, component_class, default_active=False):
        self.component_class = component_class
        self.active = default_active
        self.display_name = component_class.display_name
        self.example = component_class.example
        self.style = component_class.style
        self.shortcut_key = component_class.shortcut_key
        
    def toggle(self):
        """Toggle the active state"""
        self.active = not self.active
        return self.active
        
    def set_active(self, active):
        """Set the active state directly"""
        self.active = active
        return self.active
        
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


class ModelTreeViewer(App):
    """Textual app to display a PyTorch model structure as a tree with folding"""
    
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
    
    #component-list {
        width: 100%;
        height: 1fr;
        border: none;
        layout: vertical;
    }
    
    #component-list Button {
        width: 100%;
        margin: 0 0 1 0;
        height: auto;
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
    
    .orange1 {
        color: #ffaf00;
        text-style: italic;
    }
    
    Tree > .tree--cursor {
        background: #3a3a3a;
        color: #ffffff;
    }
    """
    
    BINDINGS = [
        # Quit
        Binding("q", "quit", "Quit"),
        
        # Navigation - vim style + arrow keys
        Binding("j", "cursor_down", "↓"),
        Binding("k", "cursor_up", "↑"),
        Binding("h", "cursor_left", "←"),
        Binding("l", "cursor_right", "→"),
        Binding("down", "cursor_down", ""),
        Binding("up", "cursor_up", ""),
        Binding("left", "cursor_left", ""),
        Binding("right", "cursor_right", ""),
        Binding("page_up", "page_up", ""),
        Binding("page_down", "page_down", ""),
        
        # Expand/Collapse
        Binding("space", "toggle_node", "Toggle"),
        Binding("z", "toggle_all_folds", "Toggle All"),
        Binding("s", "toggle_siblings", "Toggle Siblings"),
        Binding("c", "toggle_same_class", "Toggle Class"),
        
        # Display options - individual toggles
        Binding("t", "toggle_param_shapes", "Parameters"),
        Binding("b", "toggle_size", "Sizes"),
        Binding("p", "toggle_param_count", "Param Count"),
        Binding("d", "toggle_device", "Devices"),
        Binding("m", "toggle_module_type", "Module Type"),
        Binding("1", "toggle_input_shape", "In Shape"),
        Binding("2", "toggle_output_shape", "Out Shape"),
        Binding("3", "toggle_call_count", "Call Count"),
        Binding("f", "toggle_forward_stats", "All Stats"),
        Binding("A", "toggle_alignment", "Alignment"),  # Capital A for alignment
        
        # Panel options
        Binding("i", "toggle_code_panel", "Code"),
        Binding("a", "toggle_attrs_panel", "Attributes"),
        Binding("L", "toggle_label_manager", "Labels"),
    ]
    
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        
        # Cache node_data for each tree node
        self.node_data: Dict[Any, ModuleNode] = {}
        
        # Flag to track if code panel is visible
        self.code_panel_visible = True
        
        # Flag to track if attributes panel is visible
        self.attrs_panel_visible = True
        
        # Flag to track if label manager is visible
        self.label_manager_visible = False
        
        # Flag to prevent recursive updates between UI and components
        self._updating_from_selection = False
        
        # Use a built-in theme for the editor
        self.editor_theme = TextAreaTheme.get_builtin_theme("vscode_dark")
        
        # Initialize component states with default values 
        self.component_states = {}
        
        # Map components to their default active states
        component_defaults = {
            DeviceLabelComponent: False,
            SizeLabelComponent: True,
            ParamCountComponent: True,
            ForwardInputShapeComponent: False,
            ForwardOutputShapeComponent: False,
            ForwardCallCountComponent: False,
            ModuleNameComponent: True,  # Always on
            ModuleTypeBaseComponent: True,  # Always on
            ParamShapesComponent: True,
            AlignmentComponent: False
        }
        
        # Create ComponentState objects for each component type
        for component_class, default_active in component_defaults.items():
            self.component_states[component_class.__name__] = ComponentState(
                component_class, default_active
            )
            
        # List of component classes in order, for the label manager
        self.component_classes = [
            DeviceLabelComponent,
            SizeLabelComponent,
            ParamCountComponent,
            ForwardInputShapeComponent,
            ForwardOutputShapeComponent,
            ForwardCallCountComponent,
            ModuleNameComponent,
            ModuleTypeBaseComponent,
            ParamShapesComponent,
            AlignmentComponent
        ]
    
    def compose(self) -> ComposeResult:
        """Compose the UI with label manager, tree view, and editor panes"""
        with Horizontal(id="main-container"):
            # Label manager panel (initially hidden)
            with Container(id="label-manager"):
                yield Static("Component Manager", id="label-manager-title")
                yield Static("Click buttons or use keyboard shortcuts", id="label-instructions")
                # Buttons will be added in init_label_manager
            
            # Tree view pane
            with Static(id="tree-pane"):
                yield Tree("Model Structure")
            
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
                    yield Tree("No Object Selected")
                
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up the UI when app is mounted"""
        # Set up the model tree
        tree = self.query_one("#tree-pane > Tree")
        tree.root.expand()
        
        # Register theme with editor
        editor = self.query_one("#code-editor > TextArea")
        if self.editor_theme:
            editor.register_theme(self.editor_theme)
            editor.theme = "vscode_dark"
        
        # Initialize attributes tree
        attrs_tree = self.query_one("#attrs-pane > Tree")
        attrs_tree.root.expand()
        
        # Initialize label manager
        self.init_label_manager()
        
        # Initialize panel layout
        self.update_panel_layout()
        
        # Populate the tree if we have a model
        if self.model:
            self.populate_tree(self.model, tree.root)
    
    def init_label_manager(self):
        """Initialize the label manager with buttons for each component"""
        # Get label manager container
        label_container = self.query_one("#label-manager")
        
        # Clear any existing buttons
        # NodeList doesn't have copy() - use a list comprehension instead
        children_to_remove = [child for child in label_container.children 
                              if isinstance(child, Button) or (hasattr(child, "id") and child.id == "component-list")]
        for child in children_to_remove:
            label_container.remove(child)
        
        # Create a vertical container for buttons
        button_container = Container(id="component-list")
        label_container.mount(button_container)
        
        # Add buttons for each component class
        for component_class in self.component_classes:
            # Get the component state for this class
            component_state = self.component_states[component_class.__name__]
            
            # Create a button with the component class name as ID
            button = Button(
                component_state.button_text, 
                id=f"btn-{component_class.__name__}", 
                variant="default"
            )
            
            # Add the button to the container
            button_container.mount(button)
    
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
                    # Calculate tensor size: num_elements * element_size_in_bytes
                    num_elements = np.prod(tensor.shape)
                    
                    # Count parameters (elements in the tensor)
                    param_count += num_elements
                    
                    # Get element size in bytes based on dtype
                    if tensor.dtype == torch.float32:
                        element_size = 4
                    elif tensor.dtype == torch.float16 or tensor.dtype == torch.bfloat16:
                        element_size = 2
                    elif tensor.dtype == torch.int64 or tensor.dtype == torch.double:
                        element_size = 8
                    elif tensor.dtype == torch.int32 or tensor.dtype == torch.float:
                        element_size = 4
                    elif tensor.dtype == torch.int16:
                        element_size = 2
                    elif tensor.dtype == torch.int8 or tensor.dtype == torch.uint8 or tensor.dtype == torch.bool:
                        element_size = 1
                    else:
                        # Default fallback, most common case is float32 (4 bytes)
                        element_size = 4
                        
                    tensor_size = num_elements * element_size
                    total_size += tensor_size
        except Exception as e:
            # If there's an error calculating stats, return zeros
            return 0, 0
            
        return total_size, int(param_count)
        
    def populate_tree(self, module, tree_node):
        """Recursively populate tree from PyTorch module"""
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
        
        node_data = ModuleNode(name=node_name, module_type=module_name, 
                              extra_info=extra_info, state_dict_info=state_dict_info, 
                              module=module, size_bytes=module_size, param_count=param_count)
        self.node_data[tree_node] = node_data
        
        # Set node display text
        tree_node.label = node_data.get_label()
        
        # Add all child modules
        has_children = bool(module._modules)
        
        # Set whether this node can be expanded
        tree_node.allow_expand = has_children
        
        # Add all child modules
        for key, child_module in module._modules.items():
            # Apply consistent formatting with yellow module name and syntax-colored code
            module_part = f"[bold yellow]({key})[/bold yellow]: "
            # Use cyan for the class name (typical Python syntax highlighting)
            code_part = f"[cyan]{child_module._get_name()}[/cyan]"
            formatted_label = module_part + code_part
            
            child_node = tree_node.add(formatted_label)
            self.populate_tree(child_module, child_node)
    
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
                # Build the path from this node up to the root
                path_parts = []
                current = node
                
                while current and current != self.query_one("#tree-pane > Tree").root:
                    # Get the node name - it's in parentheses in the label
                    label = str(current.label)
                    if "(" in label and ")" in label:
                        name = label.split("(")[1].split(")")[0]
                        path_parts.insert(0, name)
                    current = current.parent
                
                # Format the path parts into proper Python attribute notation
                if path_parts:
                    return self.format_python_attribute_path(path_parts)
        
        # If we can't find a path, return the class name
        return module.__class__.__name__
    
    def build_attributes_tree(self, obj):
        """Build a tree of attributes for the given object"""
        attrs_tree = self.query_one("#attrs-pane > Tree")
        attrs_title = self.query_one("#attrs-title")
        
        # Get the full path to the object
        path = self.get_module_path(obj)
        
        # Update the attributes title directly
        attrs_title.update(f"Attributes: {path}".replace('[',r'\[').replace(']',r'\]'))
        
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
    
    def action_cursor_down(self) -> None:
        """Move cursor down (j key)"""
        tree = self.query_one(Tree)
        tree.action_cursor_down()
    
    def action_cursor_up(self) -> None:
        """Move cursor up (k key)"""
        tree = self.query_one(Tree)
        tree.action_cursor_up()
    
    def action_cursor_left(self) -> None:
        """Move cursor left/collapse (h key)"""
        tree = self.query_one(Tree)
        node = tree.cursor_node
        if node and node.is_expanded:
            node.collapse()  # Use node.collapse() directly
        elif node and node.parent:
            tree.select_node(node.parent)
            tree.scroll_to_node(node.parent)
    
    def action_cursor_right(self) -> None:
        """Move cursor right/expand (l key)"""
        tree = self.query_one(Tree)
        node = tree.cursor_node
        if node and not node.is_expanded and node.allow_expand:
            node.expand()  # Use node.expand() directly
        elif node:
            # When pressing right on a selected node, update the editor
            if node in self.node_data and self.node_data[node].module:
                self.update_editor_with_module(self.node_data[node].module)
    
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
        self.toggle_node_state(tree.cursor_node)
    
    def process_nodes_recursively(self, start_node, expand: Optional[bool], subtree_only: bool = False) -> int:
        """Process nodes recursively to expand or collapse them
        
        Args:
            start_node: The node to start processing from
            expand: If True, expand nodes; if False, collapse nodes
            subtree_only: If True, only process the subtree under start_node
            
        Returns:
            Number of nodes processed
        """
        count = 0
        
        def process_node(node):
            nonlocal count
            if self.toggle_node_state(node, expand):
                count += 1
            for child in node.children:
                process_node(child)
                
        # Start processing from specified node
        process_node(start_node)
        return count
    
    def action_toggle_all_folds(self) -> None:
        """Toggle all nodes - collapse all if any are expanded, otherwise expand all"""
        tree = self.query_one(Tree)
        
        # Check if any nodes are expanded (excluding the root node)
        any_expanded = False
        
        def check_if_any_expanded(node):
            nonlocal any_expanded
            # Skip the root node itself in the check
            if node != tree.root and node.is_expanded:
                any_expanded = True
                return True  # Stop traversal once we find an expanded node
            for child in node.children:
                if check_if_any_expanded(child):
                    return True
            return False
        
        check_if_any_expanded(tree.root)
        
        # If any nodes are expanded, collapse all (except root), otherwise expand all
        if any_expanded:
            # Process children of root node individually to avoid collapsing root
            for child in tree.root.children:
                self.process_nodes_recursively(child, expand=False)
            self.notify("All nodes collapsed (except root)")
        else:
            # We need to do this in multiple passes to ensure all nodes get expanded
            # Because expanding a node may create new children
            for _ in range(10):  # Limit to 10 passes to avoid infinite loop
                if self.process_nodes_recursively(tree.root, expand=True) == 0:
                    break
            self.notify("All nodes expanded")
    
    def action_toggle_siblings(self) -> None:
        """Toggle all sibling nodes at the same level as the cursor node"""
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
        
        # Toggle all siblings including the current node
        count = 0
        for sibling in parent.children:
            if self.toggle_node_state(sibling, expand):
                count += 1
                
        action = "Processed" if expand else "Collapsed"
        self.notify(f"{action} {count} sibling nodes")
        
    
    def process_nodes_by_type(self, start_node, target_type: str, expand: bool) -> int:
        """Process all nodes of a specific type in a subtree
        
        Args:
            start_node: Node to start processing from
            target_type: Module type to match
            expand: Whether to expand (True) or collapse (False)
            
        Returns:
            Number of nodes processed
        """
        count = 0
        
        def process_node(node):
            nonlocal count
            # Check if this node matches the target type
            if node in self.node_data and self.node_data[node].module_type == target_type:
                if self.toggle_node_state(node, expand):
                    count += 1
            
            # Process all children
            for child in node.children:
                process_node(child)
        
        # Start from specified node
        process_node(start_node)
        return count
    
    def action_toggle_same_class(self) -> None:
        """Toggle all nodes with the same class type in the entire tree"""
        tree = self.query_one(Tree)
        if not tree.cursor_node or tree.cursor_node not in self.node_data:
            return
            
        current_node = tree.cursor_node
        target_module_type = self.node_data[current_node].module_type
        
        # Toggle based on current node's state
        expand = not current_node.is_expanded
        
        # Process nodes of the same type in the entire tree
        count = self.process_nodes_by_type(tree.root, target_module_type, expand)
        
        action = "Expanded" if expand else "Collapsed"
        self.notify(f"{action} {count} nodes of class {target_module_type}")
    
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
            # Mark nodes with children
            has_expandable_children[child] = (len(child.children) > 0)
            
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
    
    def apply_component_state(self, component_name):
        """Apply the component state to all component instances
        
        Args:
            component_name: The name of the component class to update
        """
        if component_name not in self.component_states:
            return
            
        component_state = self.component_states[component_name]
        is_active = component_state.active
        
        # Find the actual component class
        component_class = None
        for cls in self.component_classes:
            if cls.__name__ == component_name:
                component_class = cls
                break
                
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
        
        # Update the button if it exists
        if self.label_manager_visible:
            try:
                # Find the button for this component class
                button = self.query_one(f"#btn-{component_name}")
                if button:
                    # Update button with new state
                    button.label = component_state.button_text
            except Exception as e:
                # Just continue if there's an error
                pass
            
        status = "Showing" if component_state.active else "Hiding"
        self.notify(f"{status} {component_state.display_name}")
    
    def action_toggle_param_shapes(self) -> None:
        """Toggle parameter shapes display"""
        self.log("Keyboard shortcut: toggle parameter shapes")
        self._toggle_component_class(ParamShapesComponent)
        
    def action_toggle_size(self) -> None:
        """Toggle size display"""
        self.log("Keyboard shortcut: toggle size")
        self._toggle_component_class(SizeLabelComponent)
    
    def action_toggle_param_count(self) -> None:
        """Toggle parameter count display"""
        self.log("Keyboard shortcut: toggle parameter count")
        self._toggle_component_class(ParamCountComponent)
        
    def action_toggle_device(self) -> None:
        """Toggle device display"""
        self.log("Keyboard shortcut: toggle device")
        self._toggle_component_class(DeviceLabelComponent)
        
    def action_toggle_module_type(self) -> None:
        """Toggle module type display (name and args together)"""
        self._toggle_component_class(ModuleTypeBaseComponent)
        
    def action_toggle_input_shape(self) -> None:
        """Toggle input shape display"""
        self._toggle_component_class(ForwardInputShapeComponent)
        
    def action_toggle_output_shape(self) -> None:
        """Toggle output shape display"""
        self._toggle_component_class(ForwardOutputShapeComponent)
        
    def action_toggle_call_count(self) -> None:
        """Toggle call count display"""
        self._toggle_component_class(ForwardCallCountComponent)
    
    def action_toggle_forward_stats(self) -> None:
        """Toggle all forward stats components at once"""
        # Get all forward stats components
        forward_components = [
            ForwardInputShapeComponent,
            ForwardOutputShapeComponent,
            ForwardCallCountComponent
        ]
        
        # Find any component to determine current state
        sample_component = None
        for node, node_data in self.node_data.items():
            for component in node_data.label_components:
                if any(isinstance(component, cls) for cls in forward_components):
                    sample_component = component
                    break
            if sample_component:
                break
        
        if not sample_component:
            self.notify("No forward stats components found")
            return
            
        # Toggle to opposite state
        new_state = not sample_component.active
        
        # Apply to all forward stats components
        for node, node_data in self.node_data.items():
            for component in node_data.label_components:
                if any(isinstance(component, cls) for cls in forward_components):
                    component.active = new_state
        
        # Update UI
        self.update_all_node_labels()
        status = "Showing" if new_state else "Hiding"
        self.notify(f"{status} all forward stats")
    
    def action_toggle_alignment(self) -> None:
        """Toggle node label alignment for siblings"""
        # Use the helper method to toggle AlignmentComponent class
        self._toggle_component_class(AlignmentComponent)
        
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
        
        # Update layout based on which panels are visible
        self.update_panel_layout()
    
    def action_toggle_code_panel(self) -> None:
        """Toggle visibility of the code panel"""
        # Toggle code panel visibility flag
        self.code_panel_visible = not self.code_panel_visible
        
        # Update layout based on which panels are visible
        self.update_panel_layout()
        
    
    def toggle_component_via_manager(self, component_class, is_active):
        """Toggle a component class from the label manager
        
        Args:
            component_class: The component class to toggle
            is_active: Whether the component should be active
        """
        # Log what we're doing to debug
        self.log(f"Toggling {component_class.__name__} to {is_active}")
        
        # Apply to all matching components
        for node, node_data in self.node_data.items():
            for component in node_data.label_components:
                if isinstance(component, component_class):
                    component.active = is_active
        
        # Update the tree
        self.update_all_node_labels()
        
        # Update the label manager row (check if different than current state)
        try:
            self.sync_selection_list_with_component(component_class, is_active)
        except Exception as e:
            # Log the exception to help with debugging
            self.log(f"Error updating selection list: {str(e)}")
            pass
            
        # Notify user
        status = "Showing" if is_active else "Hiding"
        self.notify(f"{status} {component_class.display_name}")
    
    def on_button_pressed(self, event):
        """Handle button presses in the label manager"""
        # Check if this is one of our component buttons
        button_id = event.button.id
        if not button_id or not button_id.startswith("btn-"):
            return
            
        # Extract the component class name from the button ID
        component_name = button_id[4:]  # Remove "btn-" prefix
        
        # Toggle the component state
        if component_name in self.component_states:
            # Toggle the state
            component_state = self.component_states[component_name]
            component_state.toggle()
            
            # Update the button text
            event.button.label = component_state.button_text
            
            # Update the actual component instances in the tree
            self.apply_component_state(component_name)
            
            # Update tree labels
            self.update_all_node_labels()
            
            # Notify user
            status = "Showing" if component_state.active else "Hiding"
            self.notify(f"{status} {component_state.display_name}")
    
    def action_toggle_label_manager(self) -> None:
        """Toggle the label manager panel"""
        # Toggle visibility state
        self.label_manager_visible = not self.label_manager_visible
        
        # Update the UI
        self.update_panel_layout()
        
        # If showing the label manager, focus it
        if self.label_manager_visible:
            # Focus the selection list
            selection_list = self.query_one("#component-list")
            if selection_list:
                selection_list.focus()
    
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
            tree_pane.styles.width = "30%"
            if self.code_panel_visible or self.attrs_panel_visible:
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
            
            # Show the right panel
            editor_pane.display = True
            editor_pane.styles.width = "60%"
            tree_pane.styles.width = "40%"
        
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



def explore_module(module):
    """Start the interactive module explorer"""
    app = ModelTreeViewer(module)
    app.run()


def explore_torch_module_with_stats(module, *args, **kwargs):
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
    """
    # Check if we were given input data
    if len(args) > 0:
        # Run a forward pass (no stats collection on its own)
        module(*args, **kwargs)
    
    # Now explore the module (will show forward_stats if they exist)
    explore_module(module)


if __name__ == "__main__":
    # Load the model
    import diffusers
    model = diffusers.CogVideoXTransformer3DModel()
    
    # Run the interactive explorer
    explore_module(model)
