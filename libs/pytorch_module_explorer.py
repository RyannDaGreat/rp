import rp
rp.pip_import('textual')
rp.pip_import('textual','textual[syntax]')
rp.pip_import('rich')
rp.pip_import('numpy')

from textual.app import App, ComposeResult
from textual.widgets import Tree, Footer, Static
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets._text_area import TextArea
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
                    shape_str = 'x'.join(str(dim) for dim in value.shape)
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

def human_readable_file_size(file_size:int):
    """
    Given a file size in bytes, return a string that represents how large it is in megabytes, gigabytes etc - whatever's easiest to interperet
    EXAMPLES:
         >>> human_readable_file_size(0)
        ans = 0B
         >>> human_readable_file_size(100)
        ans = 100B
         >>> human_readable_file_size(1023)
        ans = 1023B
         >>> human_readable_file_size(1024)
        ans = 1KB
         >>> human_readable_file_size(1025)
        ans = 1.0KB
         >>> human_readable_file_size(1000000)
        ans = 976.6KB
         >>> human_readable_file_size(10000000)
        ans = 9.5MB
         >>> human_readable_file_size(1000000000)
        ans = 953.7MB
         >>> human_readable_file_size(10000000000)
        ans = 9.3GB
    """

    for count in 'B KB MB GB TB PB EB ZB YB BB GB'.split():
        #Bytes Kilobytes Megabytes Gigabytes Terrabytes Petabytes Exobytes Zettabytes Yottabytes Brontobytes Geopbytes
        if file_size > -1024.0 and file_size < 1024.0:
            if int(file_size)==file_size:
                return "%i%s" % (file_size, count)
            else:
                return "%3.1f%s" % (file_size, count)
        file_size /= 1024.0

class ModuleNode:
    """Node representing a PyTorch module"""
    def __init__(self, name: str, module_type: str, extra_info: str = "", state_dict_info: str = "", module=None, size_bytes: int = 0):
        self.name = name
        self.module_type = module_type
        self.extra_info = extra_info
        self.state_dict_info = state_dict_info
        self.module = module
        self.size_bytes = size_bytes

    def get_label(self, show_tensor_shapes=True, show_node_sizes=True) -> str:
        """Get the display label for this node"""
        # Format the size info with human readable size
        size_info = ""
        if show_node_sizes and self.size_bytes > 0:
            size_info = f"[bold green]{human_readable_file_size(self.size_bytes)}[/bold green] "
            
        # Use direct formatting tags for bold yellow for the name part
        if self.name:
            module_part = f"{size_info}[bold yellow]({self.name})[/bold yellow]: "
        else:
            module_part = f"{size_info}"
            
        # Create code string with color to simulate Python syntax highlighting
        # Use cyan (typical for class names in Python highlighting)
        code_part = f"[cyan]{self.module_type}[/cyan]"
        if self.extra_info:
            # Use blue (typical for function parameters in Python highlighting)
            code_part += f"[blue]({self.extra_info})[/blue]"
            
        # Combine parts - module_name in bold yellow, code in syntax colors
        node_text = module_part + code_part
        
        # Add tensor shape info if needed
        if show_tensor_shapes and self.state_dict_info:
            node_text += f" | [tensor-shape]{self.state_dict_info}[/tensor-shape]"
                
        return node_text

class ModelTreeViewer(App):
    """Textual app to display a PyTorch model structure as a tree with folding"""
    
    CSS = """
    #main-container {
        layout: horizontal;
        height: 100%;
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
    
    .tensor-shape {
        color: #5fd700;
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
        
        # Display options
        Binding("t", "toggle_tensor_shapes", "Shapes"),
        Binding("b", "toggle_node_sizes", "Sizes"),
        Binding("i", "toggle_code_panel", "Code"),
        Binding("a", "toggle_attrs_panel", "Attributes"),
    ]
    
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        
        # Cache node_data for each tree node
        self.node_data: Dict[Any, ModuleNode] = {}
        
        # Flag to control whether to show tensor shapes
        self.show_tensor_shapes = True
        
        # Flag to control whether to show node sizes
        self.show_node_sizes = True
        
        # Flag to track if code panel is visible
        self.code_panel_visible = True
        
        # Flag to track if attributes panel is visible
        self.attrs_panel_visible = True
        
        # Use a built-in theme for the editor
        self.editor_theme = TextAreaTheme.get_builtin_theme("vscode_dark")
    
    def compose(self) -> ComposeResult:
        """Compose the UI with two panes"""
        with Horizontal(id="main-container"):
            # Left pane with tree view
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
        
        # Initialize panel layout
        self.update_panel_layout()
        
        # Populate the tree if we have a model
        if self.model:
            self.populate_tree(self.model, tree.root)
    
    def calculate_module_size(self, module):
        """Calculate the size of a module in bytes based on its state_dict tensors"""
        total_size = 0
        try:
            state_dict = module.state_dict()
            for param_name, tensor in state_dict.items():
                if isinstance(tensor, torch.Tensor):
                    # Calculate tensor size: num_elements * element_size_in_bytes
                    num_elements = np.prod(tensor.shape)
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
            # If there's an error calculating size, return 0
            return 0
            
        return total_size
        
    def populate_tree(self, module, tree_node):
        """Recursively populate tree from PyTorch module"""
        module_name = module._get_name()
        extra_info = module.extra_repr()
        
        # Calculate the module size in bytes
        module_size = self.calculate_module_size(module)
        
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
                            shape_str = f"{param_name}: {tuple(tensor.shape)}"
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
                              module=module, size_bytes=module_size)
        self.node_data[tree_node] = node_data
        
        # Set node display text
        tree_node.label = node_data.get_label(show_tensor_shapes=self.show_tensor_shapes, 
                                              show_node_sizes=self.show_node_sizes)
        
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
        attrs_title.update(f"Attributes: {path}".replace('[',r'\[').replace(']',r']'))#Markdown: You gotta escape the [
        
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
    
    def action_toggle_tensor_shapes(self) -> None:
        """Toggle display of tensor shapes in the tree"""
        self.show_tensor_shapes = not self.show_tensor_shapes
        
        # Update all node labels
        tree = self.query_one(Tree)
        
        def update_node_label(node):
            if node in self.node_data:
                node.label = self.node_data[node].get_label(
                    show_tensor_shapes=self.show_tensor_shapes,
                    show_node_sizes=self.show_node_sizes
                )
            for child in node.children:
                update_node_label(child)
        
        update_node_label(tree.root)
        
        status = "Showing" if self.show_tensor_shapes else "Hiding"
        self.notify(f"{status} tensor shapes")
        
    def action_toggle_node_sizes(self) -> None:
        """Toggle display of node sizes in the tree"""
        self.show_node_sizes = not self.show_node_sizes
        
        # Update all node labels
        tree = self.query_one(Tree)
        
        def update_node_label(node):
            if node in self.node_data:
                node.label = self.node_data[node].get_label(
                    show_tensor_shapes=self.show_tensor_shapes,
                    show_node_sizes=self.show_node_sizes
                )
            for child in node.children:
                update_node_label(child)
        
        update_node_label(tree.root)
        
        status = "Showing" if self.show_node_sizes else "Hiding"
        self.notify(f"{status} node sizes")
        
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
        
    
    def update_panel_layout(self) -> None:
        """Update the layout based on which panels are visible"""
        # Get all the relevant panes
        editor_pane = self.query_one("#editor-pane")
        tree_pane = self.query_one("#tree-pane")
        code_editor = self.query_one("#code-editor")
        attrs_pane = self.query_one("#attrs-pane")
        attrs_title = self.query_one("#attrs-title")
        
        # Handle visibility of the entire right panel
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
    assert rp.is_torch_module(module), 'Is not a torch.nn.Module: '+str(type(module))
    app = ModelTreeViewer(module)
    app.run()


if __name__ == "__main__":
    # Load the model
    import diffusers
    model = diffusers.CogVideoXTransformer3DModel()
    
    # Run the interactive explorer
    explore_module(model)
