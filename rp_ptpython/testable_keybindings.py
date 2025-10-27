"""
Testable key bindings wrapper.

Provides a simple functional interface: func(document, keystroke) -> document
for testing microcompletions without needing the full event/CLI infrastructure.
"""
from rp.prompt_toolkit.document import Document
from rp.prompt_toolkit.buffer import Buffer
from rp.prompt_toolkit.key_binding.input_processor import KeyPressEvent
from rp.prompt_toolkit.keys import Keys


# Simple wrapper for single character keys
class CharKey:
    """Wraps a single character to provide .data attribute for KeyPressEvent"""
    def __init__(self, char):
        self.data = char

    def __eq__(self, other):
        if isinstance(other, CharKey):
            return self.data == other.data
        return self.data == other

    def __hash__(self):
        return hash(self.data)


# Wrapper for special keys to provide .data attribute
class KeyWrapper:
    """Wraps a special key (like Keys.Backspace) to provide .data attribute"""
    def __init__(self, key):
        self.key = key
        # Set data to key name as string for special keys
        # This allows post_handler to work (it expects event.data to be a string)
        self.data = str(key)

    def __eq__(self, other):
        if isinstance(other, KeyWrapper):
            return self.key == other.key
        return self.key == other

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return "KeyWrapper({})".format(self.key)


# Create the registry once
_registry = None
_python_input_mock = None

def _get_registry():
    """Get or create the key bindings registry"""
    global _registry, _python_input_mock
    if _registry is None:
        # Create a minimal mock python_input
        class MockPythonInput:
            show_sidebar = False
            vi_mode = False
            enable_microcompletions = True

        _python_input_mock = MockPythonInput()

        # Load the actual key bindings
        from rp.rp_ptpython.key_bindings import load_python_bindings
        _registry = load_python_bindings(_python_input_mock)

    return _registry


def apply_keystroke(document, keystroke):
    """
    Apply a keystroke to a document and return the resulting document.

    This uses the ACTUAL rp key_bindings registry to process keystrokes,
    so it should handle all the same features as the real rp terminal.

    Args:
        document: A Document instance (text, cursor_position, selection)
        keystroke: A single character or special key name ('backspace', 'enter', etc.)

    Returns:
        A new Document instance with the modifications applied

    Examples:
        >>> from rp.prompt_toolkit.document import Document
        >>> doc = Document("d", cursor_position=1)
        >>> result = apply_keystroke(doc, " ")
        >>> result.text
        'def ():'
    """
    # Create a buffer with the document
    buffer = Buffer(initial_document=document)

    # Get the registry
    registry = _get_registry()

    # Create a minimal mock CLI
    class MockCLI:
        def __init__(self, buffer):
            self.current_buffer = buffer
            self.buffers = {'default': buffer}
            # Give CLI access to python_input for filters
            self.python_input = _python_input_mock

    cli = MockCLI(buffer)

    # Convert keystroke string to Key object
    # Handle special keys
    if keystroke == 'backspace':
        key = Keys.Backspace
    elif keystroke == 'enter':
        key = Keys.Enter
    elif keystroke == 'tab':
        key = Keys.Tab
    elif keystroke == 'escape':
        key = Keys.Escape
    elif keystroke == 'delete':
        key = Keys.Delete
    elif keystroke == 'left':
        key = Keys.Left
    elif keystroke == 'right':
        key = Keys.Right
    elif keystroke == 'up':
        key = Keys.Up
    elif keystroke == 'down':
        key = Keys.Down
    elif keystroke == 'space':
        key = ' '
    elif len(keystroke) == 1:
        key = keystroke
    else:
        # Unknown special key, just insert as text
        buffer.insert_text(keystroke)
        return buffer.document

    # Get bindings for this key
    bindings = registry.get_bindings_for_keys((key,))

    if bindings:
        # Create a mock input processor
        class MockInputProcessor:
            def _cli_ref(self):
                return cli

        mock_input_processor = MockInputProcessor()

        # Wrap keys to provide .data attribute for event
        if isinstance(key, str) and len(key) == 1:
            key_obj = CharKey(key)
        else:
            # Wrap special keys (Backspace, Enter, etc.) in KeyWrapper
            key_obj = KeyWrapper(key)

        # Create a mock event
        event = KeyPressEvent(
            input_processor_ref=lambda: mock_input_processor,
            arg=None,
            key_sequence=(key_obj,),
            previous_key_sequence=(),
            is_repeat=False
        )

        # Call the LAST matching binding whose filter passes (matches real REPL behavior)
        # The real InputProcessor at line 186 calls matches[-1], not matches[0]
        matching_bindings = []
        for binding in bindings:
            # Check if the binding's filter allows execution
            try:
                # Evaluate the filter with the CLI
                if binding.filter(cli):
                    matching_bindings.append(binding)
            except Exception as e:
                # If binding fails, print exception and continue to next
                import traceback
                print("Exception in binding: {}".format(e))
                traceback.print_exc()
                pass

        # Execute the last matching binding (highest priority)
        if matching_bindings:
            matching_bindings[-1].call(event)
            executed = True
        else:
            executed = False
            # If no binding executed and it's a single char, insert it
            if len(keystroke) == 1:
                buffer.insert_text(keystroke)
    else:
        # No binding found, just insert the text
        if len(keystroke) == 1:
            buffer.insert_text(keystroke)

    return buffer.document


def apply_keystrokes(document, keystrokes):
    """
    Apply a sequence of keystrokes to a document.

    Args:
        document: Initial Document instance
        keystrokes: String or list of characters to apply sequentially

    Returns:
        Final Document instance after all keystrokes applied

    Examples:
        >>> doc = Document("", cursor_position=0)
        >>> result = apply_keystrokes(doc, "x = 5")
        >>> result.text
        'x = 5'
    """
    for keystroke in keystrokes:
        document = apply_keystroke(document, keystroke)
    return document
