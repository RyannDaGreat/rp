# PyTorch Module Explorer

## Overview
**File**: `libs/pytorch_module_explorer.py`  
**Type**: Integrated RP tool (accessible via commands)  
**Purpose**: Advanced TUI (Terminal User Interface) for exploring and analyzing PyTorch model architectures

## Integration into RP
- **Command**: `EMA` - Explore PyTorch module ans (`grep "EMA.*explore_torch_module" r.py`)
- **Function**: `explore_torch_module(module)` - Main interface (`grep "def explore_torch_module" r.py`)
- **Related**: `record_torch_module_forward_stats()` - Performance analysis (`grep "def record_torch_module_forward_stats" r.py`)
- **Companion**: `torch_hooks.py` provides timing statistics (`grep "pytorch_module_explorer import explore_module" libs/torch_hooks.py`)

### Usage Workflow
```python
# Typical usage pattern in RP
with record_torch_module_forward_stats(model):
    output = model(input_data)  # Collect stats during forward pass

EMA  # Command to explore model with collected timing data
```

## Description
A sophisticated interactive browser built with Textual that provides deep inspection of PyTorch models, including parameter counts, shapes, execution statistics, and hierarchical module structure visualization.

## Core Features

### 1. Interactive Model Tree
- **Hierarchical display** of all model layers and submodules
- **Expandable/collapsible** structure navigation
- **Real-time filtering** and search capabilities
- **Parameter count summaries** at each level

### 2. Detailed Module Information
- **Parameter counts** with human-readable formatting (K, M, B)
- **Tensor shapes** with proper dimension formatting
- **Memory usage** analysis
- **Module type** and inheritance information

### 3. Performance Analysis (Optional)
- **Forward pass timing** statistics (if available)
- **Hook integration** with `torch_hooks.py` module
- **Execution profiling** data visualization
- **Memory allocation** tracking

## Key Components

### Formatting Utilities

#### Shape Formatting
```python
def format_shape(shape):
    """Format a shape tuple consistently with proper multiplication symbols"""
    return "×".join(str(dim) for dim in shape) if shape else ""

# Example: (3, 224, 224) → "3×224×224"
```

#### Parameter Count Formatting  
```python
def format_param_count(count):
    """Format parameter count as human-readable (e.g., 1.7M, 5.4B)"""
    if count < 1000:
        return f"{count}"
    elif count < 1_000_000:
        return f"{count/1000:.1f}K"
    elif count < 1_000_000_000:
        return f"{count/1_000_000:.1f}M"
    else:
        return f"{count/1_000_000_000:.1f}B"
```

#### Time Formatting
```python
def format_time(seconds):
    """Format time duration in a human-readable format"""
    if seconds < 1e-6:
        ns = seconds * 1e9
        return f"{ns:.1f}ns"
    elif seconds < 1e-3:
        us = seconds * 1e6
        return f"{us:.2f}μs"
    elif seconds < 1.0:
        ms = seconds * 1e3
        return f"{ms:.2f}ms"
    elif seconds < 60.0:
        return f"{seconds:.4f}s" if seconds < 10.0 else f"{seconds:.2f}s"
    else:
        minutes = seconds / 60.0
        return f"{minutes:.1f}min" if minutes < 60.0 else f"{minutes/60.0:.1f}h"
```

## Architecture

### TUI Framework Integration
Built on **Textual** for rich terminal interfaces:
```python
from textual import work
from textual.widgets._tree import Tree, TreeNode
from textual.worker import Worker, WorkerCancelled, WorkerFailed
```

### Asynchronous Operations
Uses async/await patterns for responsive UI:
```python
from asyncio import Queue, Lock
from textual.await_complete import AwaitComplete
```

### Data Structures
```python
@dataclass
class ModuleInfo:
    """Container for module analysis results"""
    name: str
    module_type: str
    parameter_count: int
    shapes: Dict[str, Tuple[int, ...]]
    timing_stats: Optional[Dict[str, float]] = None
    memory_usage: Optional[int] = None
```

## Usage Examples

### Basic Model Exploration
```python
import torch
import torchvision.models as models
from rp.libs.pytorch_module_explorer import explore_model

# Load a model
model = models.resnet50(pretrained=True)

# Launch interactive explorer
explore_model(model)
```

### Custom Model Analysis
```python
class CustomNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(3, 64, 3, padding=1)
        self.conv2 = torch.nn.Conv2d(64, 128, 3, padding=1)
        self.fc = torch.nn.Linear(128 * 56 * 56, 1000)
        
    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        return self.fc(x)

# Explore custom model
model = CustomNet()
explore_model(model)
```

## Interface Features

### Tree Navigation
- **Arrow keys**: Navigate through model hierarchy
- **Enter**: Expand/collapse modules
- **Space**: Toggle selection for detailed view
- **Tab**: Switch between panels

### Search and Filter
- **`/` key**: Enter search mode
- **Type to filter**: Real-time module filtering
- **Regex support**: Advanced pattern matching
- **Clear filters**: Reset view to full model

### Information Panels
- **Module Details**: Parameter counts, types, shapes
- **Performance Stats**: Timing and memory usage
- **Source Code**: Module definition and forward pass
- **Tensor Flow**: Data flow visualization

## Advanced Features

### Integration with torch_hooks.py
```python
# If torch_hooks is available, show timing statistics
try:
    from rp.libs.torch_hooks import get_forward_stats
    timing_data = get_forward_stats(model)
    display_timing_in_explorer(timing_data)
except ImportError:
    # Explorer still works without timing data
    pass
```

### Memory Analysis
```python
def analyze_memory_usage(model):
    """Calculate memory usage for each parameter"""
    memory_stats = {}
    
    for name, param in model.named_parameters():
        element_size = param.element_size()  # bytes per element
        num_elements = param.numel()
        total_bytes = element_size * num_elements
        memory_stats[name] = total_bytes
    
    return memory_stats
```

### Parameter Statistics
```python
def get_parameter_statistics(model):
    """Comprehensive parameter analysis"""
    stats = {
        'total_params': sum(p.numel() for p in model.parameters()),
        'trainable_params': sum(p.numel() for p in model.parameters() if p.requires_grad),
        'non_trainable_params': sum(p.numel() for p in model.parameters() if not p.requires_grad),
        'memory_usage': sum(p.numel() * p.element_size() for p in model.parameters()),
    }
    return stats
```

## Display Formatting

### Tree Structure
```
ResNet(
├── 145.5M parameters
├── conv1: Conv2d(3→64, 7×7) [9.4K params]
├── bn1: BatchNorm2d(64) [128 params]
├── relu: ReLU(inplace=True) [0 params]
├── maxpool: MaxPool2d(3×3, stride=2) [0 params]
├── layer1: Sequential [295.9K params]
│   ├── 0: BasicBlock [147.7K params]
│   │   ├── conv1: Conv2d(64→64, 3×3) [36.9K params]
│   │   ├── bn1: BatchNorm2d(64) [128 params]
│   │   └── ...
│   └── 1: BasicBlock [147.7K params]
└── fc: Linear(2048→1000) [2.0M params]
```

### Performance Overlay
```
layer1.0.conv1    36.9K params   Shape: 64×64×3×3   Time: 1.23ms   Mem: 147KB
├─ forward()      ⚡ 0.85ms     Input: 1×64×56×56   Output: 1×64×56×56
├─ backward()     ⚡ 0.38ms     Gradient: computed
└─ memory         📊 147KB      Parameters: 36,864 × 4 bytes
```

## Configuration Options

### Display Settings
```python
class ExplorerConfig:
    show_parameter_counts: bool = True
    show_shapes: bool = True
    show_timing: bool = True
    show_memory: bool = True
    compact_view: bool = False
    color_scheme: str = "dark"
    max_depth: Optional[int] = None
```

### Export Options
```python
def export_model_summary(model, format='text'):
    """Export analysis results"""
    if format == 'text':
        return generate_text_summary(model)
    elif format == 'json':
        return generate_json_summary(model)
    elif format == 'html':
        return generate_html_summary(model)
```

## Performance Considerations

### Large Model Handling
```python
@work(exclusive=True)
async def analyze_model_async(model):
    """Non-blocking model analysis for large models"""
    try:
        # Process in chunks to maintain UI responsiveness
        for i, (name, module) in enumerate(model.named_modules()):
            if i % 100 == 0:  # Yield control periodically
                await asyncio.sleep(0.01)
            
            analyze_module(name, module)
    except WorkerCancelled:
        # Handle cancellation gracefully
        pass
```

### Memory Optimization
```python
def lazy_parameter_analysis(model):
    """Analyze parameters on-demand to save memory"""
    def get_module_info(module_path):
        # Only analyze when requested
        module = get_module_by_path(model, module_path)
        return analyze_module_detailed(module)
    
    return get_module_info
```

## Integration with RP Ecosystem

### Model Loading Integration
```python
# Works with RP's model loading functions
model_path = rp.input_select_file(extension_filter='pth')
model = torch.load(model_path)
explore_model(model)
```

### Visualization Integration
```python
# Generate model diagrams using RP's plotting
def generate_architecture_diagram(model):
    graph_data = extract_model_graph(model)
    return rp.plot_network_graph(graph_data)
```

### Export Integration
```python
# Save analysis results using RP's file functions
summary = generate_model_summary(model)
rp.save_text_file(summary, 'model_analysis.txt')
```

## Dependencies

### Core Requirements
- **textual**: TUI framework
- **rich**: Terminal formatting
- **torch**: PyTorch model analysis
- **numpy**: Numerical computations

### Optional Dependencies
- **torch_hooks**: For timing analysis
- **matplotlib**: For visualization export
- **graphviz**: For architecture diagrams

## Future Enhancements

### Visualization Features
- **Model graph visualization** with interactive nodes
- **Activation maps** display during forward pass
- **Gradient flow** visualization
- **Architecture comparison** between models

### Analysis Features
- **FLOPS calculation** for computational complexity
- **Quantization analysis** for model optimization
- **Pruning suggestions** based on parameter importance
- **Batch size optimization** recommendations

This tool represents the pinnacle of PyTorch model introspection, combining RP's utility-focused design with sophisticated TUI capabilities to create an invaluable debugging and analysis tool for deep learning practitioners.