# RP Layout and UI System

## Overview
The RP REPL features a sophisticated, multi-pane layout system built on top of prompt_toolkit, providing real-time feedback, multiple display modes, and highly customizable UI elements.

## Layout Architecture

### Core Components

1. **Main Input Area** - Where you type commands
2. **Sidebar** - Configuration options (F5)
3. **Signature Toolbar** - Function signatures
4. **Completions Display** - Multiple visualization modes
5. **Real-time Evaluation** - Live code results
6. **Variable Display** - Current namespace vars
7. **Parenthesis Automator** - Balanced parentheses
8. **Status Bars** - Various status indicators

## Prompt Styles

### Available Styles

#### 1. Classic Prompt
```python
class ClassicPrompt(PromptStyle):
    def in_tokens(self, cli):
        return [(Token.Prompt, '>>> ')]
    
    def in2_tokens(self, cli, width):
        return [(Token.Prompt.Dots, '...')]
```

#### 2. IPython Prompt
```python
class IPythonPrompt(PromptStyle):
    def in_tokens(self, cli):
        return [
            (Token.In, 'In ['),
            (Token.In.Number, '%s' % statement_index),
            (Token.In, ']: '),
        ]
```

#### 3. PseudoTerminal Prompt
```python
class PseudoTerminalPrompt(ClassicPrompt):
    def in_tokens(self, cli):
        return [(Token.Comment, ' ⮤ ')]
```

### Switching Styles
- Access via sidebar (F5)
- Stored in `python_input.prompt_style`
- Persistent across sessions

## Display Filters

### Core Filters

#### 1. ShowSidebar
- Controls sidebar visibility
- Toggle with F5
- Shows configuration options

#### 2. ShowSignature
- Displays function signatures
- Active during function calls
- Highlights current parameter

#### 3. ShowDocstring
- Shows documentation
- Below signature toolbar
- Context-aware

#### 4. ShowRealtimeInput
- Live evaluation display
- Shows result as you type
- Filter: `ShowRealtimeInput(python_input)`

#### 5. ShowVarSpace
- Displays user variables
- Updates in real-time
- Filter: `ShowVarSpace(python_input)`

#### 6. ShowParenthesisAutomator
- Shows balanced parentheses
- Auto-completes brackets
- Visual feedback

#### 7. ShowBatteryLife
- Battery status display
- Useful for mobile/laptop
- Optional feature

## Completion Visualizations

### Modes Available

#### 1. NONE
- No completions shown
- Minimal UI

#### 2. POP_UP (Default)
```python
CompletionVisualisation.POP_UP
# Traditional dropdown menu
```

#### 3. MULTI_COLUMN
```python
CompletionVisualisation.MULTI_COLUMN
# Grid layout for many completions
```

#### 4. TOOLBAR
```python
CompletionVisualisation.TOOLBAR
# Horizontal bar at bottom
```

### Configuration
```python
python_input.completion_visualisation = CompletionVisualisation.MULTI_COLUMN
```

## Layout Containers

### Main Layout Structure
```python
HSplit([
    # Signature toolbar
    signature_toolbar(python_input),
    
    # Main input/output area
    VSplit([
        # Sidebar (if enabled)
        python_sidebar(python_input),
        
        # Input area with margins
        Window(
            BufferControl(
                buffer_name=DEFAULT_BUFFER,
                input_processors=[...],
                lexer=PythonLexer,
            ),
            left_margins=[
                PythonPromptMargin(python_input),
            ],
        ),
    ]),
    
    # Bottom toolbars
    CompletionsToolbar(),
    ValidationToolbar(),
    SystemToolbar(),
])
```

## Special UI Features

### 1. Multi-Pane Display
```python
# Real-time eval + VARS display
ConditionalContainer(
    VSplit([
        realtime_display,
        separator,
        vars_display
    ]),
    filter=ShowVarSpaceAndShowRealtimeInput(python_input)
)
```

### 2. Dynamic Margins
```python
class PythonPromptMargin(PromptMargin):
    """Shows 'In [1]:' or '>>>' based on style"""
    def get_prompt_style():
        return python_input.all_prompt_styles[
            python_input.prompt_style
        ]
```

### 3. Scroll Offsets
```python
ScrollOffsets(top=1, bottom=1)
# Keeps cursor visible with padding
```

## Input Processors

### Active Processors

1. **HighlightMatchingBracketProcessor**
   - Highlights matching (), [], {}
   - Visual pairing feedback

2. **HighlightSearchProcessor**
   - Highlights search matches
   - During Ctrl+R search

3. **HighlightSelectionProcessor**
   - Shows selected text
   - Visual selection mode

4. **AppendAutoSuggestion**
   - Gray auto-suggestions
   - Based on history

5. **DisplayMultipleCursors**
   - Multiple cursor support
   - For advanced editing

6. **IndentGuideProcessor**
   - Shows indent levels
   - Visual structure

7. **ShowWhitespaceProcessor**
   - Displays spaces/tabs
   - Optional feature

## Sidebar Configuration

### Categories and Options

```python
def python_sidebar(python_input):
    """Configuration sidebar with options"""
    
    categories = [
        Category("Display", [
            Option("Complete while typing"),
            Option("Show signature"),
            Option("Show docstring"),
            Option("Show vars"),
            Option("Realtime evaluation"),
        ]),
        Category("Colors", [
            Option("Syntax highlighting"),
            Option("Use 256 colors"),
        ]),
        Category("Input", [
            Option("Vi mode"),
            Option("Emacs mode"),
            Option("Mouse support"),
        ]),
    ]
```

### Navigation
- Arrow keys to navigate
- Space/Enter to toggle
- F5 to show/hide
- Settings persist

## Custom Windows

### 1. Realtime Display Window
```python
Window(
    BufferControl(
        buffer_name='realtime_display',
        lexer=SimpleLexer(Token.Comment)
    ),
    wrap_lines=True
)
```

### 2. VARS Display Window
```python
Window(
    BufferControl(
        buffer_name='vars',
        lexer=SimpleLexer(Token.Docstring)
    ),
    wrap_lines=True
)
```

### 3. Parenthesizer Window
```python
Window(
    BufferControl(
        buffer_name='parenthesizer_buffer',
        lexer=SimpleLexer(Token.String)
    )
)
```

## Responsive Design

### Terminal Size Handling
```python
def calculate_layout_dimensions(cli):
    term_width = cli.output.get_size().columns
    term_height = cli.output.get_size().rows
    
    # Adjust layout based on size
    if term_width < 80:
        # Narrow layout
        hide_sidebar()
    if term_height < 24:
        # Short layout
        hide_extra_toolbars()
```

### Dynamic Resizing
- Layout recalculates on terminal resize
- Windows adjust proportionally
- Maintains usability at all sizes

## Color Schemes

### Token Types
```python
Token.Prompt        # >>> prompt
Token.In           # IPython In[]
Token.Out          # IPython Out[]
Token.Comment      # Real-time eval
Token.Docstring    # VARS display
Token.Sidebar      # Sidebar text
Token.Toolbar      # Toolbar text
```

### Theming
- Configurable via pygments styles
- 256-color support
- True color when available

## Mouse Support

### Clickable Elements
- Sidebar options
- Completion items
- Buffer text selection
- Scrolling support

### Implementation
```python
@if_mousedown
def select_item(cli, mouse_event):
    python_input.selected_option_index = index
```

## Performance Optimizations

### 1. Lazy Rendering
- Only visible parts rendered
- Virtual scrolling for long content

### 2. Cached Layouts
- Layout calculations cached
- Invalidated on changes only

### 3. Conditional Containers
- UI elements only created when shown
- Reduces memory usage

## Configuration

### Settings File
```python
# In settings or RPRC
settings = {
    'completion_visualisation': 'multi-column',
    'show_signature': True,
    'show_docstring': True,
    'show_vars': True,
    'show_realtime_input': True,
    'prompt_style': 'classic',
}
```

### Runtime Toggle
- Most UI elements toggleable
- Commands like `PT ON/OFF`
- Sidebar for visual config

## Tips & Tricks

### 1. Minimal UI
```python
# Hide everything for focus
PT OFF
# Hides all extra UI elements
```

### 2. Maximum Information
```python
# Show everything
show_vars = True
show_realtime_input = True
show_signature = True
show_docstring = True
```

### 3. Custom Layout
```python
# In RPRC, modify layout
def custom_layout():
    return HSplit([
        # Your custom arrangement
    ])
```

## Integration Points

### With Completion System
- Completions displayed in chosen mode
- Layout adjusts for completion display

### With Real-time Evaluation
- Results shown in dedicated pane
- Updates without blocking input

### With History
- History browser in separate window
- Maintains main input state

This sophisticated layout system makes RP one of the most visually rich and informative Python REPLs available, with real-time feedback and extensive customization options.