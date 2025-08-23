# Integrated RP Modules

## Overview
These modules are integrated into RP's main `r.py` functionality and accessible through regular RP commands and imports.

## Quick Reference - Integration Points

### Direct Command Integration
- **`PPT`/`PPTA`** → `powerpoint_converter.py`
- **`EMA`** → `pytorch_module_explorer.py`
- **`DAPI`** → `pypi_inspection.py`
- **`CCA`/`CCH`** → AI code tools
- **`GEM`/`GEMA`** → AI code tools

### Function Integration
- **`debug_comment()`** → imported (`grep "from.*debug_comment import debug_comment" r.py`)
- **`explore_torch_module()`** → main interface (`grep "def explore_torch_module" r.py`)
- **`display_image_in_terminal()`** → uses `timg` (`grep "import rp.libs.timg" r.py`)

### Library Integration
- **`web_evaluator`** → lazy loaded as `we` (`grep "lazy_loader.load.*web_evaluator" r.py`)
- **`torch_hooks`** → used by PyTorch explorer (`grep "import rp.libs.torch_hooks" r.py`)
- **`graveyard.py`** → imported (`grep "from rp.libs.graveyard import" r.py`)
- **`stamp_tensor.py`** → imported (`grep "from rp.libs.stamp_tensor import" r.py`)
- **`torch_tools.py`** → used for model surgery (`grep "rp.libs.torch_tools" r.py`)
- **`pyfx`** → JSON viewer (`grep "from rp.libs.pyfx" r.py`)
- **`profile_vim_plugins.py`** → used (`grep "from rp.libs.profile_vim_plugins" r.py`)
- **`peepdis`** → bytecode disassembler (`grep "from rp.libs.peepdis" r.py`)
- **`pyflann`** → FLANN nearest neighbor (`grep "from rp.libs.pyflann" r.py`)
- **`pynput_recorder`** → input recording (`grep "from rp.libs.pynput_recorder" r.py`)
- **`refactor`** → f-string converter (`grep "from rp.libs.refactor" r.py`)

## PowerPoint Converter (`experimental/powerpoint_converter.py`)

### Integration
- **Functions**: `_convert_powerpoint_file(path, message=None)` (`grep "def _convert_powerpoint_file" r.py`)
- **Commands**: `PPT`, `PPTA` (`grep "PPT.*_convert_powerpoint_file" r.py`)
- **Import**: Uses experimental module (`grep "from rp.experimental import process_powerpoint_file" r.py`)

### Functionality
Converts PowerPoint files to be compatible with Google Slides by replacing MP4 videos with animated GIFs.

#### Problem Solved
When uploading PowerPoint files with MP4 videos to Google Slides, videos become static images. This tool converts the thumbnail images in PPTX files to animated GIFs that work in web browsers.

#### Usage
```python
# Via commands
PPT    # Select PowerPoint file interactively
PPTA   # Convert ans (must be .pptx path)

# Via function
_convert_powerpoint_file('/path/to/presentation.pptx')
```

#### How It Works
1. Extracts PPTX file (which is a ZIP archive)
2. Finds MP4-to-thumbnail mappings in XML structure
3. Converts MP4s to GIFs using MoviePy
4. Replaces PNG thumbnails with animated GIFs
5. Rebuilds PPTX file with working animations

#### Output
Creates a new PPTX file that maintains PowerPoint compatibility while providing animated content when viewed in Google Slides.

---

## Debug Comment System (`experimental/debug_comment.py`)

### Integration
- **Import**: `from rp.experimental.debug_comment import debug_comment` (`grep "from.*debug_comment import" r.py`)

### Functionality
Modifies source code files by adding inline comments showing evaluated values next to `debug_comment()` calls.

#### Core Function
```python
debug_comment(value)  # Modifies your source file!
```

#### How It Works
1. Captures caller's filename and line number
2. Evaluates the provided value/expression
3. On program exit (`atexit`), updates source files
4. Adds `# --> result` comments inline

#### Usage Examples
```python
# Before running
x = 10
debug_comment(x * 2)  # Gets modified

# After running, source file shows:
x = 10  
debug_comment(x * 2)  # --> 20
```

#### Advanced Features
- **Lambda evaluation**: `debug_comment(lambda: expensive_calculation())` 
- **Multi-line support**: Comments are `repr()` encoded
- **Alignment preservation**: Respects existing comment alignment
- **Last-value-wins**: Multiple calls update to final result

#### Safety Notes
- **Modifies source files directly**
- **Best practice**: Commit changes to git before using
- **Only adds comments**: Doesn't change line count

---

## Terminal Image Display (`libs/timg/`)

### Integration
- **Variable**: `_use_rp_timg = True` (`grep "_use_rp_timg.*True" r.py`)
- **Import**: `import rp.libs.timg as timg` (`grep "import rp.libs.timg" r.py`)
- **Integration**: Used by `display_image_in_terminal()` functions

### Functionality
High-performance terminal image rendering using optimized C libraries.

#### Integration Flow
```python
# In display functions:
if _use_rp_timg:
    try:
        import rp.libs.timg as timg
        timg_renderer = timg.Renderer()
        timg_renderer.load_image(as_pil_image(image))
        timg_renderer.render(timg.METHODS[method]['class'])
    except:
        _use_rp_timg = False  # Fall back to other methods
```

#### Supported Methods
- **ANSI**: 256-color terminal display
- **Sixel**: High-quality graphics protocol
- **ASCII**: Text-based representation

#### Performance Benefits
- C-optimized image processing
- Multiple rendering backends
- Graceful fallback system

---

## Web Evaluator (`web_evaluator.py`)

### Integration
- **Lazy loader**: `we = lazy_loader.load('web_evaluator')` (`grep "lazy_loader.load.*web_evaluator" r.py`)
- **Direct import**: `import web_evaluator as we` (`grep "import web_evaluator as we" r.py`)

### Functionality
Remote Python code execution over HTTP with distributed computing capabilities.

#### Core Components
- **`run_server()`**: HTTP server for remote code execution
- **`Client`**: Execute code on remote servers
- **`ClientDelegator`**: Load balancing across multiple servers
- **`ClientRoster`**: Server discovery and management

#### Key Features
1. **Remote execution**: Run Python code on other machines
2. **Web integration**: Serve HTML/JS with Python backend
3. **Distributed computing**: Balance load across server pools
4. **Real-time communication**: Bidirectional data streaming

#### Integration Usage
```python
# Server mode
we.run_server(port=43234)

# Client mode  
client = we.Client('192.168.1.100')
result = client.evaluate('import torch; torch.cuda.is_available()')
```

#### Advanced Features
- **Tmux cluster management**: `launch_tmux_delegation_cluster()`
- **JavaScript integration**: `/webeval/rp.js` endpoint
- **Binary responses**: Image/video streaming support
- **Error handling**: Connection resilience and failover

---

## AI Code Tools Integration

### Claude Code Integration
- **Commands**: `CCA`, `CCH` (`grep "CCA.*_run_claude_code" r.py`)
- **Functions**: `_run_claude_code(code)` (`grep "def _run_claude_code" r.py`)

### Gemini CLI Integration  
- **Commands**: `GEM`, `GEMA` (`grep "GEM.*_run_gemini_cli" r.py`)
- **Functions**: `_run_gemini_cli(code)` (`grep "def _run_gemini_cli" r.py`)

These integrate external AI coding assistants into RP's command system for automated code generation and analysis.