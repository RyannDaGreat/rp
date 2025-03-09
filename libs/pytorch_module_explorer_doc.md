# PyTorch Module Explorer

An interactive TUI (Text User Interface) for exploring PyTorch models

## Installation

For the best experience, install Textual and its syntax highlighting extension:

```bash
pip install textual
pip install textual[syntax]
```

## Usage

The PyTorch Module Explorer allows you to interactively explore and visualize the structure of PyTorch models, including nested modules, parameters, memory usage, and runtime statistics.

### Basic Usage

```python
import torch
import rp

# Create a simple model
model = torch.nn.Sequential(
    torch.nn.Conv2d(3, 64, 3, padding=1),
    torch.nn.ReLU(),
    torch.nn.MaxPool2d(2),
    torch.nn.Conv2d(64, 128, 3, padding=1),
    torch.nn.ReLU(),
    torch.nn.AdaptiveAvgPool2d((1, 1)),
    torch.nn.Flatten(),
    torch.nn.Linear(128, 10)
)

# Launch the interactive explorer
rp.explore_torch_module(model)
```

### Exploring with Forward Pass Statistics

To view forward pass statistics (tensor shapes, memory usage, runtime), you can either:

#### Method 1: Use explore_torch_module_with_forward_stats

```python
import rp

# Create sample input data
x = torch.randn(1, 3, 224, 224)

# Run a forward pass and explore the model
rp.explore_torch_module_with_forward_stats(model, x)
```

#### Method 2: Use record_torch_module_forward_stats context manager

```python
import rp

# Create sample input data
x = torch.randn(1, 3, 224, 224)

# Collect statistics during forward pass
with rp.record_torch_module_forward_stats(model):
    model(x)

# Explore the model with the collected statistics
rp.explore_torch_module(model)
```

### Exploring Non-Module Objects

You can explore objects that aren't PyTorch modules themselves but contain modules in their attributes. This is useful for exploring model containers, HuggingFace pipelines, diffusers pipelines, and similar structures.

```python
from diffusers import StableDiffusionPipeline
import rp
import torch

# Load a diffusion model pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

# Explore the pipeline - it will automatically identify and display all PyTorch modules
rp.explore_torch_module(pipe)
```

Example with a custom model container:

```python
import torch
import rp

class ModelContainer:
    def __init__(self):
        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(784, 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, 64)
        )
        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(64, 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, 784)
        )
        self.config = {"latent_dim": 64, "training": True}  # Non-module attribute
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

# Create container and explore it
container = ModelContainer()
rp.explore_torch_module(container)  # Will show encoder and decoder modules in the tree
```

### Example with Diffusion Pipeline and Forward Stats Recording

You can explore any object with PyTorch modules one level deep in the attribute hierarchy, including diffusion pipelines:

```python
from diffusers import StableDiffusionPipeline
import rp
import torch

device = rp.select_torch_device()

pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16", torch_dtype=torch.float16)
pipe = pipe.to(device)

# Record input/output tensor shapes, etc for all modules
with rp.record_torch_module_forward_stats(pipe):
    pipe('Image of Doggy', num_inference_steps=3)

# Explore the collected stats - press 'f' to see them
rp.explore_torch_module(pipe)
```

## Key Controls

### Navigation
- Arrow keys or hjkl: Navigate tree
- Space: Toggle node fold/unfold
- Enter: Expand selected node

### Display Options
- f: Toggle forward statistics (runtime tensor shapes, requires forward pass)
- t: Toggle parameter shapes 
- b: Toggle memory usage display
- p: Toggle parameter counts
- d: Toggle device information
- A: Toggle node alignment

### Panels
- c: Toggle code panel
- a: Toggle attributes panel
- L: Toggle label customization
- <: Expand the rightmost sidepanel width
- >: Contract the rightmost sidepanel width

### Folding
- z: Fold/unfold the selected node and all its descendants
- Z: Fold/unfold all nodes in the entire tree
- s: Fold/unfold immediate sibling nodes (same level only)
- S: Fold/unfold all sibling nodes and their descendants
- o: Fold/unfold all nodes of the same class type globally
- O: Fold/unfold all nodes of the same class type and their descendants

Press ESC or Enter to close this help window.