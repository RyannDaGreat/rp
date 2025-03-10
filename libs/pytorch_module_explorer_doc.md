# PyTorch Module Explorer

> A powerful interactive TUI tool for exploring PyTorch models in real-time

## Overview

The PyTorch Module Explorer is a terminal-based interactive tool that lets you visually explore and analyze PyTorch models directly from your terminal. Unlike static analysis tools, it provides a **live, interactive view** of your model's actual state as loaded in memory, including a hierarchical view of model architecture with detailed information about each module, including parameter counts, memory usage, tensor shapes, and more.

## Why Use PyTorch Module Explorer?

- **Live, Interactive Analysis** - See exactly what's in your model as it exists in memory, not just static code analysis
- **Runtime Activation Inspection** - Visualize intermediate activations and tensor shapes through the network
- **Simultaneous Source Code View** - View implementation details alongside model structure in split panels
- **Full Attribute Inspection** - Examine all module attributes, parameters, and buffers in real-time
- **No Configuration Files** - Explore any model immediately without any setup or configuration

## Key Features

- **Terminal-based UI** - Works over SSH, no GUI needed
- **Interactive navigation** - Explore complex models with intuitive keyboard controls
- **Parameter visualization** - See shapes, counts, and memory usage of parameters
- **Runtime statistics** - View input/output tensor shapes and data types (after forward pass)
- **Source code access** - View the implementation of any module component
- **Customizable display** - Toggle different information components on/off
- **Module attribute inspection** - Examine all attributes of a module
- **Visual highlighting** - Same-class modules are tinted green for easy identification

## Getting Started

Import the required modules:

```python
import torch
import rp
```

Load your model:

```python
model = torch.nn.Sequential(
    torch.nn.Conv2d(3, 64, kernel_size=3, padding=1),
    torch.nn.ReLU(),
    torch.nn.MaxPool2d(2),
    torch.nn.Conv2d(64, 128, kernel_size=3, padding=1),
    torch.nn.ReLU(),
    torch.nn.Flatten(),
    torch.nn.Linear(128*16*16, 10)
)
```

Launch the explorer:

```python
# Basic exploration without runtime stats
rp.explore_torch_module(model)

# With runtime stats (after running a forward pass)
input_tensor = torch.randn(1, 3, 32, 32)
with rp.record_torch_module_forward_stats(model):
    output = model(input_tensor)

# Now explore with runtime stats available
rp.explore_torch_module(model)
```

## Keyboard Controls

### Navigation

| Key       | Action                                |
|-----------|---------------------------------------|
| `↑` / `k` | Move selection up                     |
| `↓` / `j` | Move selection down                   |
| `←` / `h` | Collapse node / go to parent         |
| `→` / `l` | Expand node / view selected module   |
| `space`   | Fold/unfold selected node             |

### Folding

| Key | Action                                 |
|-----|----------------------------------------|
| `z` | Fold/unfold subtree under selected node |
| `Z` | Fold/unfold all nodes in entire tree    |
| `s` | Fold/unfold siblings                   |
| `S` | Fold/unfold siblings and their descendants |
| `o` | Fold/unfold nodes with same class type |
| `O` | Fold/unfold nodes with same class type and descendants |

### Display Options

| Key | Display Component                      |
|-----|----------------------------------------|
| `t` | Parameter shapes                       |
| `b` | Memory sizes                           |
| `p` | Parameter counts                       |
| `d` | Device information                     |
| `f` | Forward statistics (requires forward pass) |
| `A` | Alignment of sibling nodes             |

### Panel Options

| Key | Action                                 |
|-----|----------------------------------------|
| `c` | Toggle code panel                      |
| `a` | Toggle attributes panel                |
| `L` | Toggle label customization panel       |
| `<` | Expand right panel width               |
| `>` | Contract right panel width             |
| `?` | Show this help page                    |
| `Enter` or `Esc` | Close help window         |

### Label Customization

When in the label customization panel (toggle with `L`):

| Key | Action                                 |
|-----|----------------------------------------|
| `space` / `enter` | Toggle selected component on/off |
| `Shift+J` | Move selected component down in the list |
| `Shift+K` | Move selected component up in the list |

## Label Components

The module labels can include various pieces of information, all of which can be toggled on/off:

- **Module Name** - The name of the module in the model hierarchy
- **Module Type** - The Python class of the module
- **Parameter Shapes** - Shapes of parameters like weights and biases
- **Parameter Count** - Total number of parameters in the module
- **Memory Usage** - Memory footprint of the module's parameters
- **Device** - Which device (CPU/GPU) the module is on
- **Input Shapes** - Shapes of input tensors (italic, requires forward pass)
- **Output Shapes** - Shapes of output tensors (non-italic, requires forward pass)
- **Data Types** - Data types of parameters and tensors

## Forward Pass Statistics

One of the most powerful features is the ability to inspect **live tensor activations** throughout your model. To view runtime statistics (input/output shapes, data types, and tensor values), you must first record a forward pass:

```python
# Method 1: Using context manager
with rp.record_torch_module_forward_stats(model):
    output = model(input_tensor)

# Method 2: Using the explore function directly
rp.explore_torch_module_with_stats(model, input_tensor)
```

After recording stats, press `f` in the explorer to view forward pass information. This gives you unprecedented visibility into:

- Input/output tensor shapes at each layer (input shapes shown in italics)
- Data types of intermediate activations
- Call counts for each module (useful for modules called multiple times)
- Full inspection of actual tensor values through the attributes panel

This runtime information is invaluable for debugging, optimizing, and understanding complex model architectures.

### About Torch Hooks and Forward Stats

The `rp.record_torch_module_forward_stats()` function uses PyTorch hooks to monitor every module's forward pass. Here's what happens when you use it:

1. **Hook Registration**: Automatically registers forward hooks on every module and submodule in your model
2. **Data Collection**: During forward passes, collects comprehensive statistics for each module:

   **Input Tensor Statistics**:
   - Shape (`in_shape`) - Dimensions of the input tensor
   - Data type (`in_dtype`) - Precision of the tensor (float32, float16, etc.)
   - Device (`in_device`) - Which device the tensor is on (CPU, CUDA, etc.)
   - Value range (`in_min`, `in_max`) - Minimum and maximum values
   - Statistical metrics (`in_mean`, `in_std`) - Mean and standard deviation
   - Gradient info (`in_requires_grad`, `in_has_grad`) - Gradient tracking status
   - Memory usage (`in_memory_bytes`) - Memory consumption of the tensor

   **Output Tensor Statistics**:
   - Identical metrics as inputs but for output tensors (prefixed with `out_`)

3. **Clean Removal**: Hooks are automatically removed after the context manager exits

The recorded stats are stored directly in each module's `forward_stats` attribute as a list, with the most recent forward pass last, allowing for analysis of multiple forward passes. Access these stats programmatically, or use the Explorer's UI to visualize them by pressing `f`.

```python
# Example: Accessing stats programmatically
with rp.record_torch_module_forward_stats(model):
    output = model(input_tensor)

# Get stats for a specific layer
conv_layer = model[0]  # First layer
latest_stats = conv_layer.forward_stats[-1]
print(f"Input shape: {latest_stats.in_shape}, Output shape: {latest_stats.out_shape}")
print(f"Value range: {latest_stats.in_min:.3f} to {latest_stats.in_max:.3f}")
```

> **Note**: The module explorer will detect and display these statistics automatically whenever they're available.

## Advanced Example: Exploring a Diffusion Model

```python
from diffusers import StableDiffusionPipeline
import torch
import rp

# Setup
device = rp.select_torch_device()
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4", 
    revision="fp16", 
    torch_dtype=torch.float16
).to(device)

# Record statistics during a forward pass
with rp.record_torch_module_forward_stats(pipe.unet):
    pipe('A photograph of a cat', num_inference_steps=3)

# Explore the UNet with recorded statistics
rp.explore_torch_module(pipe.unet)
```

## Tips

- Use `b` to view memory usage for identifying large parameters
- Use `f` after a forward pass to see how tensor shapes change through the model
- Use `t` to view parameter shapes for understanding model architecture
- Use `o` to quickly find all instances of a specific layer type (also highlights them in green)
- When selecting a module, all modules of the same type are automatically highlighted in green
- Press `L` to customize exactly which components to display (use Shift+J/K to reorder them)
- Use the attributes panel (toggle with `a`) to explore tensor values and module settings
- Use the code panel (toggle with `c`) to view module source code
- Use `<` and `>` to adjust panel widths
- Don't worry about configuration files - just load your model and explore

## Practical Use Cases

- **Debugging Model Architectures** - Quickly identify shape mismatches and configuration errors
- **Optimizing Model Performance** - Find layers with excessive parameters/memory usage
- **Understanding Pre-trained Models** - Explore architectures you didn't create yourself
- **Validating Data Flow** - Confirm tensor shapes transform as expected through the network
- **Teaching Deep Learning** - Visualize concepts like channel dimensions and feature maps
- **Remote Development** - Inspect models on remote servers over SSH without a GUI

---

Created by Ryan Burgert. Explore your PyTorch models with confidence!