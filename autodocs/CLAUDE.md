# RP Module - Claude Code Documentation

## Overview
The **RP (Ryan's Python)** module is a comprehensive Python utility library containing thousands of functions for:
- File operations and system utilities
- Image/video processing and computer vision 
- Audio processing and MIDI operations
- Mathematical operations and data analysis
- Network utilities and communication
- Terminal interfaces and pseudo-terminals
- Machine learning and AI tools
- Web scraping and API interactions
- And much more...

## Key Features
- **Massive function library**: 53,000+ lines with 1625+ utility functions
- **Import everything pattern**: `from rp.r import *` or `import rp` 
- **Cross-platform compatibility**: Works on macOS, Linux, Windows
- **Self-contained**: All dependencies vendored - `pip install rp` just works
- **Ultra-fast import**: ~22ms despite 513K+ total lines (10x faster than NumPy!)

## RP Design Motifs
- **pip_import pattern**: Auto-installs dependencies on demand (436+ uses!) - users only get deps they need
- **Strategic vendoring**: Only vendor libraries with breaking changes, stable ones use pip_import
- **Aliases everywhere**: Functions often have multiple names (e.g. `invert_image` = `inverted_image`)
- **Accept anything**: Functions accept any reasonable input type and convert automatically
- **Batch operations**: Most functions have plural versions (`resize_image` → `resize_images`)
- **Symmetric pairs**: Encode/decode functions always come in pairs
- **Implementation multiplexing**: Base functions dispatch to `_via_` variants with different backends
  - **No useless args**: Base has only common args, variants have format-specific args (avoids ffmpeg problem)
  - Base multiplexes by file extension (`save_video` → `save_video_mp4` with `video_bitrate`)
  - Or by backend choice (`resize_image` tries `cv_resize_image` then `_resize_image_via_skimage`)
  - Variants can be private or public (e.g. `_load_image_from_file_via_PIL` vs `text_to_speech_via_google`)

## Image System
RP has ~285+ image functions with a flexible "accept anything, return what makes sense" philosophy:

- **Image types**: NumPy arrays (HW/HW3/HW4), PIL images, Torch tensors (CHW)
- **Data types**: float (0-1), uint8 (0-255), bool
- **Auto-conversion**: Functions accept any format via `is_*` validators and `as_*` converters
- **Key functions**: `load_image`, `save_image`, `display_image`, `resize_image`, `blend_images`
- **Batch operations**: Most have plural versions (`crop_images`, `resize_images`)

**See**: `documentation/claude/images.md` for complete image system documentation

## Multiplexing Pattern
RP uses a "no useless args" multiplexing pattern where base functions dispatch to implementation variants:

**See**: `documentation/claude/multiplexing.md` for detailed pattern documentation

## Graveyard Refactoring System
The RP module includes an **automated graveyard system**. This is an internal tool primarily for developers and AI assistants to safely refactor and manage the large codebase. **End-users do not need to interact with this system; all functions remain accessible through the standard `rp` import.**

- **Purpose**: Move unused or deprecated functions from `r.py` to `libs/graveyard.py` while maintaining accessibility.
- **Automation**: Fully automated with dependency resolution using AST manipulation.
- **Accessibility**: All moved functions remain accessible via `from rp.libs.graveyard import *`.
- **Private function support**: Automatically exports private functions (`_name`) in `__all__` lists.

### Usage
1. Mark functions with `#GRAVEYARD START` and `#GRAVEYARD END` markers
2. Run `/opt/homebrew/opt/python@3.10/bin/python3.10 move_to_graveyard.py` 
3. Functions are automatically moved with qualified dependencies (`rp.r.function_name()`)

**See**: `documentation/claude/graveyard.md` for complete technical documentation

## For Future Claude Sessions

### Documentation Created by Previous Claudes
The `documentation/claude/` folder contains comprehensive guides:

#### Core Documentation
- **breadcrumbs.md** - Navigation guide for finding functions and understanding RP
- **motifs.md** - Deep dive into RP's design patterns and philosophy
- **multiplexing.md** - Detailed explanation of the "no useless args" pattern
- **images.md** - Complete image system documentation
- **graveyard.md** - Graveyard refactoring system documentation
- **codebase_overview.md** - Bird's eye view of entire RP structure (2600+ files)

#### REPL System Deep Dive (`repl/` subdirectory)
- **repl_system.md** - Overview of RP's revolutionary custom REPL
- **repl/overview.md** - Complete REPL architecture
- **repl/realtime_eval.md** - Live evaluation as you type
- **repl/parenthesis.md** - ASCII art parenthesis visualization
- **repl/vars_tracking.md** - Real-time variable tracking
- **repl/commands.md** - 200+ command shortcuts reference
- **repl/microcompletions.md** - Smart auto-transformations
- **repl/history.md** - History, persistence, and UNDO/REDO

### Quick Stats (from codebase analysis)
- **Total Python files**: 2,654 (includes vendored libraries)
- **Total lines of code**: 513,231 (with all vendored deps)
- **Main r.py**: 53,184 lines, 1,625 functions
- **Import time**: ~22ms (NumPy: 207ms, Pandas: 771ms)
- **Top-level imports**: Only 22 (458+ lazy imports in functions)

### Key Insights
- **Graveyard system available**: Can help identify and move unused code to graveyard
- **Automated workflow**: No manual dependency resolution needed  
- **Safe refactoring**: All moved functions remain accessible
- **Consistent motifs**: Verb-noun naming, pluralization, _via_ backends, is_/as_ patterns

## File Structure
```
rp/
├── r.py                    # Main module (53,000+ lines)
├── move_to_graveyard.py   # Graveyard refactoring script  
├── libs/
│   └── graveyard.py       # Repository for moved functions
└── documentation/
    └── claude/
        └── graveyard.md   # Detailed graveyard documentation
```