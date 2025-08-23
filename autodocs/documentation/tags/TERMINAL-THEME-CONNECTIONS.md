# RP Terminal/CLI Functions and Their Relationships

## Overview
This document maps all terminal/CLI related functions in the RP module and their interconnections. RP has a comprehensive terminal ecosystem with 80+ functions spanning display, interaction, formatting, and system integration.

## Core Function Categories

### 1. Terminal Detection & Compatibility
**Base Functions:**
- `terminal_supports_ansi()` - Checks ANSI escape sequence support
- `terminal_supports_unicode()` - Checks Unicode character support  
- `currently_running_windows()`, `currently_running_posix()`, `currently_running_macos()` - OS detection
- `get_terminal_size()`, `get_terminal_width()`, `get_terminal_height()` - Terminal dimensions

**Relationship Flow:**
```
OS Detection → Terminal Capability Detection → Display Function Selection
```

### 2. ANSI Formatting System (fansi)
**Core ANSI Functions:**
- `fansi()` - Main ANSI formatting function with colors, styles, backgrounds
- `fansi_print()` - Print with ANSI formatting
- `fansi_is_enabled()`, `fansi_is_disabled()` - State management
- `disable_fansi()`, `enable_fansi()` - Toggle ANSI formatting
- `without_fansi()` - Context manager to temporarily disable

**Advanced ANSI Functions:**
- `fansi_syntax_highlighting()` - Syntax highlighting for code
- `fansi_pygments()` - Pygments-powered highlighting
- `fansi_highlight_path()` - File path highlighting
- `_transform_fansi_arg()` - Internal argument processing

**ANSI Workflow:**
```
fansi() → Color/Style Processing → ANSI Escape Codes → Terminal Output
                ↓
        fansi_print() → Direct terminal display
                ↓  
    fansi_syntax_highlighting() → Code syntax coloring
```

### 3. Terminal Display Functions
**Image Display:**
- `display_image_in_terminal()` - Black & white Unicode image display
- `display_image_in_terminal_color()` - Full color image display using timg
- `display_image_in_terminal_imgcat()` - iTerm2 imgcat protocol

**Data Visualization:**
- `display_qr_code_in_terminal()` - QR code rendering
- `display_website_in_terminal()` - Web content display
- `histogram_in_terminal()` - Terminal histograms  
- `line_graph_in_terminal()` - Line plots in terminal
- `bar_graph()` - Bar chart visualization

**Display System Relationships:**
```
Image/Data Input → Format Detection → Terminal Capability Check → Optimal Display Method
                                    ↓
                            display_image_in_terminal_color() (preferred)
                                    ↓
                            display_image_in_terminal() (fallback)
```

### 4. Interactive Input System  
**Basic Input Functions:**
- `input_default()` - Input with editable default value
- `input_multiline()` - Multi-line input
- `input_conditional()` - Input with validation
- `input_yes_no()` - Boolean confirmation
- `input_integer()` - Numeric input

**Selection Functions:**
- `input_select()` - Single choice from options
- `input_select_multiple()` - Multiple choice selection
- `input_select_path()` - File/directory picker
- `input_select_file()`, `input_select_folder()` - Specific path types
- `input_keypress()` - Single key capture

**Input Function Hierarchy:**
```
input_conditional() → Base validation system
        ↓
    input_select() → Single choice interface
        ↓
input_select_multiple() → Multi-choice interface
        ↓
    input_select_path() → File system navigation
```

### 5. Advanced REPL System (ptpython)
**Main REPL Functions:**
- `pseudo_terminal()` - Full-featured Python REPL with 200+ commands
- `python_input()` - Ptpython-powered input with syntax highlighting
- `_multi_line_python_input()` - Multi-line code input

**REPL Supporting System:**
- **rp_ptpython/** module - Complete ptpython customization
  - `python_input.py` - Main CLI interface
  - `key_bindings.py` - 200+ keyboard shortcuts
  - `layout.py` - Terminal layout management
  - `completer.py` - Advanced autocompletion
  - `history_browser.py` - Interactive history navigation

**REPL Architecture:**
```
pseudo_terminal() → python_input() → ptpython system
                        ↓
            Advanced Features: Syntax highlighting, autocompletion,
            history, command shortcuts, real-time evaluation
```

### 6. Progress & Status Display
**Progress Bars:**
- `unicode_loading_bar()` - Unicode progress bar
- `get_box_char_bar_graph()` - Box character graphs  
- `get_progress_bar_image()` - Visual progress bar images
- `image_with_progress_bar()`, `video_with_progress_bar()` - Media with progress

**Status Functions:**
- `_print_status()` - Status message display
- `fansi_progress()` - Colored progress display
- Many functions have `show_progress` parameters

**Progress System Integration:**
```
File Operations → Progress Tracking → unicode_loading_bar() → Terminal Display
(load_images, save_video, etc.)          ↓
                                Status Updates via fansi_progress()
```

### 7. Clipboard & Copy/Paste System
**Local Clipboard:**
- `string_to_clipboard()`, `string_from_clipboard()` - System clipboard
- `load_image_from_clipboard()`, `copy_image_to_clipboard()` - Image clipboard
- `accumulate_clipboard_text()` - Clipboard history

**Terminal-Specific Clipboard:**
- `_copy_text_over_terminal()` - Terminal escape sequence copying
- `vim_copy()`, `vim_paste()` - Vim integration
- `tmux_copy()`, `tmux_paste()` - Tmux clipboard
- `local_copy()`, `local_paste()` - Process-local clipboard

**Multi-Platform Clipboard Flow:**
```
Data → Platform Detection → Appropriate Clipboard Method
                ↓
    System Clipboard (default) ↔ Terminal Clipboard ↔ Application Clipboard
                    ↓
            Cross-platform abstraction layer
```

### 8. Terminal Control & Manipulation
**Cursor Control:**
- `_terminal_move_cursor_to_top_left()` - Cursor positioning
- `_terminal_move_cursor_to_bottom_left()` - Bottom positioning
- `set_cursor_to_bar()` - Cursor style changes

**Screen Control:**
- `clear_terminal_screen()` - Screen clearing
- `_erase_terminal_line()` - Line erasing
- `ring_terminal_bell()` - Audio notification
- `_disable_terminal_mouse_reporting()` - Mouse handling

**Control Function Chain:**
```
Terminal State Change → Cursor/Screen Control → ANSI Escape Sequences → Terminal
```

### 9. Shell & Process Integration
**Process Management:**
- `get_process_cwd()` - Process working directory
- `run_as_new_process()` - Process spawning  
- `search_processes()` - Process search with progress display

**Shell Integration:**
- `shell_command()` - Command execution (from core RP)
- `vim()` - Vim editor integration with line number support
- Various file operation functions integrated with shell

### 10. Mouse & Keyboard Input
**Mouse Control:**
- `get_mouse_position()`, `set_mouse_position()` - Mouse positioning
- `mouse_left_click()`, `mouse_right_click()`, `mouse_middle_click()` - Mouse clicks
- `mouse_left_press()`, `mouse_left_release()` - Mouse press states
- `record_mouse_positions()`, `playback_mouse_positions()` - Mouse automation

**Keyboard Input:**
- `type_string_with_keyboard()` - Automated typing
- `input_keypress()` - Single key capture
- Integration with ptpython key binding system

### 11. TMUX Integration System
**TMUX Functions:**
- `running_in_tmux()` - TMUX detection
- `tmux_copy()`, `tmux_paste()` - TMUX clipboard
- `tmux_get_current_session_name()`, `tmux_get_current_window_name()` - Session info
- `tmux_kill_session()`, `tmux_kill_sessions()` - Session management
- `tmux_type_in_all_panes()` - Multi-pane input
- `tmux_get_scrollback()` - Terminal history access
- `tmuxp_create_session_yaml()` - Session configuration

**TMUX Workflow Integration:**
```
TMUX Detection → Session Management → Multi-pane Operations → Clipboard Integration
                        ↓
                Terminal multiplexing with RP integration
```

## Function Interconnection Patterns

### 1. Capability Detection Pattern
```
OS/Terminal Detection → Feature Selection → Fallback Chain
```
Most terminal functions follow this pattern, checking capabilities before operation.

### 2. Format Multiplexing Pattern
```
Base Function → Format/Backend Detection → Specialized Implementation
```
Example: `display_image_in_terminal_color()` → timg backend vs fallback

### 3. Progressive Enhancement Pattern
```
Basic Functionality → Feature Detection → Enhanced Features
```
Example: Basic input → ptpython available → Enhanced REPL

### 4. Integration Layer Pattern  
```
RP Function → Terminal Integration → External Tool Integration
```
Example: `vim()` function integrates RP data with vim editor

## Key Workflow Chains

### Complete Terminal Display Workflow:
```
Data/Content → Format Detection → Terminal Capability Check → Optimal Display Method → ANSI Formatting → Terminal Output
```

### Interactive Input Workflow:
```
Input Request → Terminal Setup → ptpython Integration → User Interaction → Validation → Result Processing
```

### REPL System Workflow:
```
pseudo_terminal() → Namespace Setup → ptpython CLI → Command Processing → Result Display → History Update
```

### Progress Display Workflow:
```
Long Operation → Progress Tracking → Status Updates → Terminal Display → Completion Notification
```

## Integration Points

### External Tool Integration:
- **Vim**: Seamless editor integration with line numbers, clipboard
- **TMUX**: Full session management, clipboard, multi-pane operations  
- **Shell**: Command execution with progress tracking
- **System Clipboard**: Cross-platform clipboard abstraction

### Library Integration:
- **ptpython**: Advanced REPL with syntax highlighting
- **Pygments**: Code syntax highlighting
- **drawille**: Unicode graphics for image display
- **timg**: High-quality terminal image display

### RP Internal Integration:
- All terminal functions integrate with RP's core utilities
- Progress display integrated into file operations
- ANSI formatting used throughout RP ecosystem
- Input functions used in interactive RP workflows

## Design Philosophy

**1. Progressive Enhancement**: Functions detect terminal capabilities and provide the best experience possible
**2. Graceful Degradation**: Fallback methods ensure functionality on all terminals  
**3. Cross-Platform**: Abstracts platform differences while maintaining full functionality
**4. Integration-First**: Terminal functions integrate seamlessly with RP's broader ecosystem
**5. User Experience**: Prioritizes ease of use with sensible defaults and rich features

The terminal system in RP represents one of the most comprehensive terminal integration layers available in Python, providing everything from basic ANSI formatting to advanced REPL systems with seamless tool integration.