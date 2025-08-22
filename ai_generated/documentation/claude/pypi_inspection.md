# PyPI Package Inspection

## Overview
**File**: `pypi_inspection.py`  
**Type**: Integrated RP tool (accessible via commands)  
**Purpose**: Extract and display metadata information from installed PyPI packages

## Integration into RP
- **Command**: `DAPI` - Display all PyPI info (`grep "DAPI.*display_all_pypi_info" r.py`)
- **Function**: Uses `display_all_pypi_info()` to show comprehensive package information
- **Module**: Imported as `__import__('rp.pypi_inspection').pypi_inspection`

## Functionality
Analyzes installed Python packages by parsing their `.dist-info` directories to extract comprehensive package metadata including dependencies, console scripts, and module information.

## Core Functions

### `get_dist_infos()`
Returns a comprehensive mapping of Python modules to their PyPI package information.

```python
info_map = get_dist_infos()
# Returns: {'torch': {'Name': 'torch', 'Version': '1.7.0', ...}, ...}
```

### `display_module_pypi_info(object, info=None)`
Displays formatted package information for a given module or object.

```python
import torch
display_module_pypi_info(torch)
```

**Output:**
```
PyPI package info for module torch:
    Author Email: packages@pytorch.org
    Dependencies: ['dataclasses', 'future', 'numpy']
    Homepage: https://pytorch.org/
    Keywords: pytorch machine learning
    Modules: ['torch']
    Name: torch
    Requires Python: >=3.6.1
    Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
    Version: 1.7.0
```

### `get_pypi_info_from_module(module)`
Extracts PyPI information for a specific module.

```python
import numpy
info = get_pypi_info_from_module(numpy)
print(info['Version'])  # '1.21.0'
```

## Implementation Details

### Package Discovery
```python
def get_site_packages_directory():
    import sysconfig
    return sysconfig.get_paths()["purelib"]

def get_dist_info_paths():        
    infos = [x for x in get_subdirectories(get_site_packages_directory()) 
             if x.endswith('.dist-info')]
    return infos
```

### Metadata Parsing
Parses `METADATA` files in `.dist-info` directories:

```python
def get_pypi_info(dist_info_path):
    metadata = path_join(dist_info_path, 'METADATA')
    metadata = text_file_to_string(metadata)
    lines = line_split(metadata)
    
    def get_field(prefix):
        return [x[len(prefix):].strip() for x in lines if x.startswith(prefix)]
    
    for prefix in 'Name Version Home-page Summary Keywords Requires-Python Author-email Requires-Dist'.split():
        fields = get_field(prefix+':')
        # Process fields...
```

### Console Scripts Extraction
Parses `entry_points.txt` to find command-line scripts:

```python
def get_console_scripts(entry_points):
    entry_points = text_file_to_string(entry_points)
    lines = line_split(entry_points)
    output = []
    flag = False
    
    for line in lines:
        if line.strip() == '[console_scripts]':
            flag = True
            continue
        elif line.startswith('[') and line.endswith(']'):
            break
        if flag and line:
            output.append(line.split('=')[0].strip())
    
    return sorted(set(output))
```

## Advanced Features

### Dependency Processing
Normalizes complex dependency specifications:

```python
# Converts: "prompt-toolkit ; extra == 'ptk'" 
# To: "prompt-toolkit"

if 'Requires-Dist' in output:
    if isinstance(output['Requires-Dist'], list):
        output['Requires-Dist'] = sorted(set([x.split()[0] for x in output['Requires-Dist']]))
```

### Module-to-Package Mapping
```python
def get_pypi_info_from_module_name(module_name, info=None):
    name = module_name.split('.')[0]  # rp.prompt_toolkit -> rp
    info = info or get_dist_infos()
    if name in info:
        return info[name]
    return None
```

### Object Introspection
```python
def get_module_name_from_object(o):
    if isinstance(o, str):
        return o
    if is_a_module(o):
        return o.__name__
    
    import inspect
    module = inspect.getmodule(o)
    if module is None:
        module = inspect.getmodule(type(o))
    
    return module.__name__
```

## Usage Examples

### Basic Package Information
```python
from rp.pypi_inspection import *

# Get all package info
all_packages = get_dist_infos()
print(f"Found {len(all_packages)} packages")

# Look up specific package
torch_info = all_packages.get('torch')
if torch_info:
    print(f"PyTorch version: {torch_info['Version']}")
```

### Display Package Details
```python
import numpy
import pandas

# Display info for imported modules
display_module_pypi_info(numpy)
display_module_pypi_info(pandas)

# Display info by name
display_module_pypi_info('requests')
```

### Console Scripts Discovery
```python
# Find all available command-line tools
all_packages = get_dist_infos()
for package_name, info in all_packages.items():
    if 'Console Scripts' in info:
        print(f"{package_name}: {info['Console Scripts']}")

# Example output:
# pip: ['pip', 'pip3', 'pip3.8']
# matplotlib: ['matplotlib']
# jupyter: ['jupyter', 'jupyter-lab', 'jupyter-notebook']
```

### Dependency Analysis
```python
def analyze_dependencies(package_name):
    info = get_dist_infos().get(package_name)
    if not info:
        return f"Package {package_name} not found"
    
    deps = info.get('Dependencies', [])
    print(f"{package_name} depends on:")
    for dep in deps:
        print(f"  - {dep}")
        
# Usage
analyze_dependencies('torch')
```

## Comprehensive Package Analysis

### System-Wide Package Report
```python
def display_all_pypi_info():
    info_map = get_dist_infos()
    for name in sorted(info_map):
        info = get_pypi_info_from_module_name(name, info_map)
        display_module_pypi_info(name, info)
        print()
```

### Package Statistics
```python
def package_statistics():
    all_packages = get_dist_infos()
    
    # Count packages by Python version requirement
    python_versions = {}
    for pkg_info in all_packages.values():
        req_python = pkg_info.get('Requires Python', 'Unknown')
        python_versions[req_python] = python_versions.get(req_python, 0) + 1
    
    print("Python version requirements:")
    for version, count in sorted(python_versions.items()):
        print(f"  {version}: {count} packages")
    
    # Count packages with console scripts
    with_scripts = sum(1 for info in all_packages.values() 
                      if 'Console Scripts' in info)
    print(f"\nPackages with console scripts: {with_scripts}")
```

## Module Name Mapping

### Known PyPI Name Differences
```python
def get_pypi_module_package_names():
    """Handle cases where module name != package name"""
    o = get_dist_infos()
    q = {}
    for module_name in o:
        q[module_name] = o[module_name]['Name']
    
    # Add known mappings (e.g., cv2 -> opencv-python)
    q.update(r.known_pypi_module_package_names)
    
    # Filter identical names
    q = {x: y for x, y in q.items() if x and x != y}
    
    return dict(sorted(q.items()))
```

## Error Handling

### Robust Parsing
```python
def get_pypi_info(dist_info_path):
    output = {}
    try:
        # Metadata parsing with error handling
        metadata = path_join(dist_info_path, 'METADATA')
        if file_exists(metadata):
            # Parse fields safely
            pass
    except Exception as e:
        print_verbose_stack_trace(e)
        # Continue processing other fields
    
    try:
        # Console scripts parsing
        entry_points = path_join(dist_info_path, 'entry_points.txt')
        scripts = get_console_scripts(entry_points)
        if scripts:
            output['Console Scripts'] = scripts
    except Exception:
        pass  # Skip if entry_points.txt missing
    
    return output
```

## Integration with RP

### Enhanced Module Information
Could be integrated into RP's help system:
```python
def enhanced_help(obj):
    # Standard help
    help(obj)
    
    # Add PyPI info
    print("\n" + "="*50)
    display_module_pypi_info(obj)
```

### Dependency Management
```python
def check_package_dependencies(required_packages):
    """Verify all required packages are installed"""
    installed = get_dist_infos()
    missing = []
    
    for package in required_packages:
        if package not in installed:
            missing.append(package)
    
    if missing:
        print(f"Missing packages: {missing}")
        print("Install with: pip install " + " ".join(missing))
    else:
        print("All required packages are installed")
```

## Performance Considerations

### Caching Strategy
The module processes all `.dist-info` directories once and caches results:

```python
# Heavy operation done once
def get_dist_infos():
    output = []
    for path in get_dist_info_paths():
        try:
            processed = process(path)
            output.append(processed)
        except Exception:
            pass  # Skip corrupted packages
    
    # Build module -> info mapping
    result = {}
    for info, modules in output:
        for module in modules:
            result[module] = info
    
    return result
```

### Lazy Loading
Could be enhanced with lazy loading for better performance:

```python
@lru_cache(maxsize=None)
def get_package_info_lazy(package_name):
    """Load package info only when requested"""
    return get_pypi_info_from_module_name(package_name)
```

This tool provides comprehensive insight into the Python package ecosystem on a system, making it valuable for dependency management, environment analysis, and package discovery.