from copy import copy, deepcopy
import rp
import time
import abc
import subprocess

from pynput import mouse, keyboard
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

##############################################################################
# A C T I O N   C L A S S E S
##############################################################################

mouse_controller = MouseController()
keyboard_controller = KeyboardController()


class Reprable:
    def __repr__(self):
        attributes = [
            f"{attr}={str(value)}"
            for attr, value in self.__dict__.items()
            if not "__" in attr and value != []
        ]
        return f'{type(self).__name__}({", ".join(attributes)})'


class Action(abc.ABC, Reprable):
    """
    Base class for all actions. Each action is callable.
    """

    @abc.abstractmethod
    def __call__(self):
        """
        Perform the action, e.g. press a key, move the mouse, etc.
        """
        pass


class DelayAction(Action):
    """
    Sleeps for `seconds` when called.
    """

    def __init__(self, seconds: float):
        self.seconds = seconds

    def __call__(self):
        if self.seconds > 0:
            time.sleep(self.seconds)


# ------------------- Mouse Actions -------------------
class MouseAction(Action):
    """
    Base for mouse actions: provides x, y coordinates.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


class MouseMoveAction(MouseAction):
    """
    Moves the mouse pointer to (x, y).
    """

    def __init__(self, x, y):
        super().__init__(x, y)

    def __call__(self):
        mouse_controller.position = (self.x, self.y)


class MousePressAction(MouseAction):
    """
    Presses a mouse button at (x, y).
    """

    def __init__(self, x, y, button=Button.left):
        super().__init__(x, y)
        self.button = button

    def __call__(self):
        mouse_controller.position = (self.x, self.y)
        mouse_controller.press(self.button)


class MouseReleaseAction(MouseAction):
    """
    Releases a mouse button at (x, y).
    """

    def __init__(self, x, y, button=Button.left):
        super().__init__(x, y)
        self.button = button

    def __call__(self):
        mouse_controller.position = (self.x, self.y)
        mouse_controller.release(self.button)


class MouseScrollAction(MouseAction):
    """
    Scrolls the mouse wheel at (x, y) by (dx, dy).
    """

    def __init__(self, x, y, dx, dy):
        super().__init__(x, y)
        self.dx = dx
        self.dy = dy

    def __call__(self):
        mouse_controller.position = (self.x, self.y)
        mouse_controller.scroll(self.dx, self.dy)


# ------------------- Keyboard Actions -------------------
class KeyboardAction(Action):
    """
    Base for keyboard actions. Stores a Key or a character.
    """

    def __init__(self, key):
        self.key = key


class KeyboardPressAction(KeyboardAction):
    """
    Presses a key (character or special Key).
    """

    def __init__(self, key):
        super().__init__(key)

    def __call__(self):
        keyboard_controller.press(self.key)


class KeyboardReleaseAction(KeyboardAction):
    """
    Releases a key (character or special Key).
    """

    def __init__(self, key):
        super().__init__(key)

    def __call__(self):
        keyboard_controller.release(self.key)


##############################################################################
# T R I G G E R S
##############################################################################


class Trigger(abc.ABC, Reprable):
    """
    Each trigger is a callable that takes an Action object.
    It returns True if triggered, otherwise False.
    Triggers can manage internal state as needed.
    """

    NUM_ACTIONS = 0

    @abc.abstractmethod
    def __call__(self, action: Action) -> bool:
        pass


class NoStartTrigger(Trigger):
    """
    Always returns True immediately -> recording starts right away.
    """

    def __call__(self, action: Action) -> bool:
        return True


class NoEndTrigger(Trigger):
    """
    Never returns True -> must stop via Ctrl+C or other means.
    """

    def __call__(self, action: Action) -> bool:
        return False


class KeyDownTrigger(Trigger):
    NUM_ACTIONS = 1

    def __init__(self, target_key):
        self.target_key = target_key

    def __call__(self, action: Action) -> bool:
        return (
            isinstance(action, KeyboardReleaseAction) and action.key == self.target_key
        )


class KeyUpTrigger(Trigger):
    NUM_ACTIONS = 1

    def __init__(self, target_key):
        self.target_key = target_key

    def __call__(self, action: Action) -> bool:
        return isinstance(action, KeyboardPressAction) and action.key == self.target_key


class TwoKeyDownTrigger(Trigger):
    NUM_ACTIONS = 2

    def __init__(self, key1, key2):
        self.key1 = key1
        self.key2 = key2
        self.key1_pressed = False
        self.key2_pressed = False
        self.triggered = False

    def __call__(self, action: Action) -> bool:
        if self.triggered:
            return False

        if isinstance(action, KeyboardPressAction):
            if action.key in self.key1:
                self.key1_pressed = True
            elif action.key in self.key2:
                self.key2_pressed = True
            else:
                self.key1_pressed = False
                self.key2_pressed = False

            if self.key1_pressed and self.key2_pressed:
                self.triggered = True
                return True

        elif isinstance(action, KeyboardReleaseAction):
            self.key1_pressed = False
            self.key2_pressed = False

        return False


class TwoKeyUpTrigger(Trigger):
    NUM_ACTIONS = 2

    def __init__(self, key1, key2):
        self.key1 = key1
        self.key2 = key2
        self.key1_released = False
        self.key2_released = False
        self.down_trigger = TwoKeyDownTrigger(self.key1, self.key2)
        self.triggered = False
        self.ready = False

    def __call__(self, action: Action) -> bool:
        if self.triggered:
            return False

        self.ready |= self.down_trigger(action)

        if self.ready and isinstance(action, KeyboardReleaseAction):
            self.key1_released |= action.key in self.key1
            self.key2_released |= action.key in self.key2

            if self.ready and self.key1_released and self.key2_released:
                self.triggered = True
                return True

        #FOR DEBUGGING
        # print(
        #     line_join(
        #         [
        #             fansi(self, "white green"),
        #             fansi(action, "yellow white"),
        #             fansi(self.down_trigger, "orange"),
        #         ]
        #     )
        # )

        return False


class CmdEscUpTrigger(TwoKeyUpTrigger):
    def __init__(self):
        super().__init__([Key.cmd, Key.cmd_r], [Key.esc])


class CmdEscDownTrigger(TwoKeyDownTrigger):
    def __init__(self):
        super().__init__([Key.cmd, Key.cmd_r], [Key.esc])


class CmdShiftUpTrigger(TwoKeyUpTrigger):
    def __init__(self):
        super().__init__([Key.cmd, Key.cmd_r], [Key.shift])


class CmdShiftDownTrigger(TwoKeyDownTrigger):
    def __init__(self):
        super().__init__([Key.cmd, Key.cmd_r], [Key.shift])


class CmdCmdUpTrigger(TwoKeyUpTrigger):
    # This is buggy because pynput is buggy with respect to two cmd keys! Don't use
    def __init__(self):
        super().__init__([Key.cmd], [Key.cmd_r])


class CmdCmdDownTrigger(TwoKeyDownTrigger):
    def __init__(self):
        super().__init__([Key.cmd], [Key.cmd_r])


##############################################################################
# R E C O R D I N G  W I T H  S E P A R A T E  D E L A Y S
##############################################################################


def record_actions(start_trigger=None, end_trigger=None):
    """
    Capture a list of Action objects:
      - DelayAction(seconds)
      - MouseMoveAction, MousePressAction, etc.
      - KeyboardPressAction, KeyboardReleaseAction
    The action that triggers start or end is NOT recorded.
    """
    if start_trigger is None:
        start_trigger = NoStartTrigger()
    if end_trigger is None:
        end_trigger = NoEndTrigger()

    actions = []
    start_recording = False
    stop_recording = False
    last_time = None

    def create_action(event_type, data):
        """
        Convert a (event_type, data) from pynput into one of our Action objects.
        """
        if event_type == "mouse_move":
            x, y = data
            return MouseMoveAction(x, y)

        elif event_type == "mouse_press":
            btn, (x, y) = data
            button = Button.left if str(btn) == "Button.left" else Button.right
            return MousePressAction(x, y, button)

        elif event_type == "mouse_release":
            btn, (x, y) = data
            button = Button.left if str(btn) == "Button.left" else Button.right
            return MouseReleaseAction(x, y, button)

        elif event_type == "mouse_scroll":
            x, y, dx, dy = data
            return MouseScrollAction(x, y, dx, dy)

        elif event_type == "keyboard_press":
            return KeyboardPressAction(data)

        elif event_type == "keyboard_release":
            return KeyboardReleaseAction(data)

        return None  # Unknown event

    def handle_event(event_type, data):
        nonlocal stop_recording

        if stop_recording:
            return

        nonlocal start_recording, last_time

        # Convert to an Action object
        action = create_action(event_type, data)
        if action is None:
            return  # skip unknown events

        # Check triggers

        if not start_recording:
            rp.fansi_print(action, "italic dark gray")
            if start_trigger(action):
                # Just triggered the start
                start_recording = True
                last_time = time.time()
            return  # Don't add actions before starting!
        else:
            if end_trigger(action):
                # Just triggered the end
                print("BLOOBAH")
                for _ in range(end_trigger.NUM_ACTIONS):
                    while actions and isinstance(actions[-1], DelayAction):
                        actions.pop()
                    if actions:
                        actions.pop()
                        deleted_action = actions.pop()
                        # This is ugly logic...actions should instead be FILTERED through triggers.
                        # For this reason, I'll abstract this whole codebase away into an rp function, as I might improve this logic in the future to handle new types of triggers.
                        rp.fansi_print(
                            f"[{len(actions)}]: ACTIONS -= {action}", "orange red blue green"
                        )
                stop_recording = True
                return

        # If we are here, we are actively recording this action
        now = time.time()
        if last_time is None:
            last_time = now
        delta = now - last_time
        last_time = now

        # Add a DelayAction if delta > 0
        if delta > 0:
            actions.append(DelayAction(delta))

        # Add the actual action
        actions.append(action)
        rp.fansi_print(f"[{len(actions)}]: ACTIONS += {action}", "yellow blue green")

    # ---------------------------------------------------------------------
    #  Listener callbacks
    # ---------------------------------------------------------------------
    def on_move(x, y):
        handle_event("mouse_move", (x, y))

    def on_click(x, y, button, pressed):
        if pressed:
            handle_event("mouse_press", (button, (x, y)))
        else:
            handle_event("mouse_release", (button, (x, y)))

    def on_scroll(x, y, dx, dy):
        handle_event("mouse_scroll", (x, y, dx, dy))

    def on_press(key):
        handle_event("keyboard_press", key)

    def on_release(key):
        handle_event("keyboard_release", key)

    # Start listeners
    mouse_listener = mouse.Listener(
        on_move=on_move, on_click=on_click, on_scroll=on_scroll
    )
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener.start()
    keyboard_listener.start()

    print("Recording...Press cmd+shift anywhere or Ctrl+C in the terminal to stop.")
    try:
        while not stop_recording:
            time.sleep(0.000001)
    except KeyboardInterrupt:
        print("Stopped by KeyboardInterrupt.")
    finally:
        mouse_listener.stop()
        keyboard_listener.stop()

    print(f"Recorded {len(actions)} actions (including DelayActions).")
    return actions

##############################################################################
# T M U X
##############################################################################

# This section was generated with the help of Claude-Code, May 14 2025

# Mapping from pynput Key to tmux key name
PYNPUT_TO_TMUX_KEYS = {
    Key.alt: "M",         # Only for tracking active modifiers
    Key.alt_r: "M",       # Only for tracking active modifiers
    Key.backspace: "BSpace",
    Key.ctrl: "C",        # Only for tracking active modifiers
    Key.ctrl_r: "C",      # Only for tracking active modifiers
    Key.delete: "DC",
    Key.down: "Down",
    Key.end: "End",
    Key.enter: "Enter",
    Key.esc: "Escape",
    Key.f1: "F1",
    Key.f2: "F2",
    Key.f3: "F3",
    Key.f4: "F4",
    Key.f5: "F5",
    Key.f6: "F6",
    Key.f7: "F7",
    Key.f8: "F8",
    Key.f9: "F9",
    Key.f10: "F10",
    Key.f11: "F11",
    Key.f12: "F12",
    Key.f13: "F13",
    Key.f14: "F14",
    Key.f15: "F15",
    Key.f16: "F16",
    Key.f17: "F17",
    Key.f18: "F18",
    Key.f19: "F19",
    Key.f20: "F20",
    Key.home: "Home",
    Key.left: "Left",
    Key.page_down: "PageDown", 
    Key.page_up: "PageUp",
    Key.right: "Right",
    Key.space: "Space",
    Key.tab: "Tab",
    Key.up: "Up",
}

# Special characters that need escaping in tmux
TMUX_SPECIAL_CHARS = {
    ';': '\\;',
    '#': '\\#',
    ',': '\\,',
}

# macOS special characters to their original Alt/Option keystroke combinations
# These are the characters that appear when using Alt/Option + key combinations
MACOS_SPECIAL_CHAR_TO_KEYSTROKE = {
    # Option + letter combinations
    'Ω': ('M', 'z'),        # Option + z
    'π': ('M', 'p'),        # Option + p  
    'µ': ('M', 'm'),        # Option + m
    'ß': ('M', 's'),        # Option + s
    'ç': ('M', 'c'),        # Option + c
    '√': ('M', 'v'),        # Option + v
    '≈': ('M', 'x'),        # Option + x
    '∂': ('M', 'd'),        # Option + d
    '∆': ('M', 'j'),        # Option + j
    '∫': ('M', 'b'),        # Option + b
    '∑': ('M', 'w'),        # Option + w
    '∞': ('M', '5'),        # Option + 5
    '≤': ('M', ','),        # Option + comma
    '≥': ('M', '.'),        # Option + period
    '÷': ('M', '/'),        # Option + /
    '≠': ('M', '='),        # Option + =
    '±': ('M', '+'),        # Option + +
    '¬': ('M', 'l'),        # Option + l
    '∧': ('M', 'k'),        # Option + k
    '∨': ('M', 'v'),        # Option + v (logical or)
    '⊕': ('M', 'q'),        # Option + q
    '⊗': ('M', 'r'),        # Option + r
    '⊙': ('M', 'o'),        # Option + o
    '⊥': ('M', 'i'),        # Option + i
    '∪': ('M', 'u'),        # Option + u
    '∩': ('M', 'n'),        # Option + n
    '∅': ('M', 'h'),        # Option + h
    '∈': ('M', 'e'),        # Option + e
    '∉': ('M', 'f'),        # Option + f
    '∋': ('M', 'g'),        # Option + g
    '∌': ('M', 't'),        # Option + t
    '∠': ('M', 'a'),        # Option + a
    '£': ('M', '3'),        # Option + 3
    '¢': ('M', '4'),        # Option + 4
    '¥': ('M', 'y'),        # Option + y
    '¡': ('M', '1'),        # Option + 1
    '«': ('M', '\\'),       # Option + \
    '"': ('M', '['),        # Option + [
    "'": ('M', ']'),        # Option + ]
    '–': ('M', '-'),        # Option + -
    '…': ('M', ';'),        # Option + ;
    '†': ('M', 't'),        # Option + t
    '®': ('M', 'r'),        # Option + r
    '´': ('M', 'e'),        # Option + e (acute accent dead key)
    'œ': ('M', 'q'),        # Option + q
    'å': ('M', 'a'),        # Option + a
    'ƒ': ('M', 'f'),        # Option + f
    '©': ('M', 'g'),        # Option + g
    'ø': ('M', 'o'),        # Option + o
    'æ': ('M', "'"),        # Option + '
    '`': ('M', '`'),        # Option + `
    'ˆ': ('M', 'i'),        # Option + i (circumflex accent dead key)
    '™': ('M', '2'),        # Option + 2
    '§': ('M', '6'),        # Option + 6
    '¶': ('M', '7'),        # Option + 7
    '•': ('M', '8'),        # Option + 8
    'ª': ('M', '9'),        # Option + 9
    'º': ('M', '0'),        # Option + 0
    
    # Option + Shift combinations
    'Ç': ('M', 'S-c'),      # Option + Shift + c
    '◊': ('M', 'S-v'),      # Option + Shift + v
    '˛': ('M', 'S-x'),      # Option + Shift + x
    '¸': ('M', 'S-z'),      # Option + Shift + z
    '˝': ('M', 'S-w'),      # Option + Shift + w
    '˚': ('M', 'S-k'),      # Option + Shift + k
    '¯': ('M', 'S-h'),      # Option + Shift + h
    '˘': ('M', 'S-g'),      # Option + Shift + g
    '˙': ('M', 'S-h'),      # Option + Shift + h
    '¨': ('M', 'S-u'),      # Option + Shift + u
    '˜': ('M', 'S-n'),      # Option + Shift + n
    '¦': ('M', 'S-\\'),     # Option + Shift + \
    '€': ('M', 'S-2'),      # Option + Shift + 2
    '‰': ('M', 'S-r'),      # Option + Shift + r
    '°': ('M', 'S-8'),      # Option + Shift + 8
    '¿': ('M', 'S-/'),      # Option + Shift + /
    '»': ('M', 'S-\\'),     # Option + Shift + \
    '"': ('M', 'S-['),      # Option + Shift + [
    "'": ('M', 'S-]'),      # Option + Shift + ]
    '—': ('M', 'S--'),      # Option + Shift + -
    '‚': ('M', 'S-;'),      # Option + Shift + ;
    '„': ('M', 'S-w'),      # Option + Shift + w
    '‹': ('M', 'S-3'),      # Option + Shift + 3
    '›': ('M', 'S-4'),      # Option + Shift + 4
    'ﬁ': ('M', 'S-5'),      # Option + Shift + 5
    'ﬂ': ('M', 'S-6'),      # Option + Shift + 6
    '‡': ('M', 'S-7'),      # Option + Shift + 7
    '·': ('M', 'S-9'),      # Option + Shift + 9
    '⁄': ('M', 'S-1'),      # Option + Shift + 1
    'Œ': ('M', 'S-q'),      # Option + Shift + q
    'Å': ('M', 'S-a'),      # Option + Shift + a
    'Í': ('M', 'S-s'),      # Option + Shift + s
    'Î': ('M', 'S-d'),      # Option + Shift + d
    'Ï': ('M', 'S-f'),      # Option + Shift + f
    'Ó': ('M', 'S-h'),      # Option + Shift + h (duplicate with ¯)
    'Ô': ('M', 'S-j'),      # Option + Shift + j
    'Ò': ('M', 'S-k'),      # Option + Shift + k (duplicate with ˚)
    'Ú': ('M', 'S-l'),      # Option + Shift + l
    'Æ': ('M', 'S-\\'),     # Option + Shift + " (quote key)
    'Á': ('M', 'S-e'),      # Option + Shift + e
    'ˇ': ('M', 'S-t'),      # Option + Shift + t
    '´': ('M', 'S-e'),      # Option + Shift + e (duplicate)
    'Â': ('M', 'S-i'),      # Option + Shift + i
    'ı': ('M', 'S-b'),      # Option + Shift + b
    'Ø': ('M', 'S-o'),      # Option + Shift + o
    '∏': ('M', 'S-p'),      # Option + Shift + p
    '\u2019': ('M', 'S-]'),      # Option + Shift + ] (right single quote)
    '\u2018': ('M', 'S-['),      # Option + Shift + [ (left single quote)
    '\u201C': ('M', 'S-['),      # Option + Shift + [ (left double quote)
    '\u201D': ('M', 'S-]'),      # Option + Shift + ] (right double quote)
}


def _convert_macos_special_char(char, cls):
    """
    Helper function to convert macOS special characters to TmuxSendkeyAction.
    
    Args:
        char: The character to check and convert
        cls: The TmuxSendkeyAction class
        
    Returns:
        TmuxSendkeyAction or None: The converted action if char is a special character, None otherwise
    """
    if char in MACOS_SPECIAL_CHAR_TO_KEYSTROKE:
        modifier, keystroke = MACOS_SPECIAL_CHAR_TO_KEYSTROKE[char]
        # For special characters, we ignore the active_modifiers and use the mapped ones
        if keystroke.startswith('S-'):
            # Option + Shift combination
            return cls(keystroke[2:], [modifier, 'S'])
        else:
            # Option only combination
            return cls(keystroke, [modifier])
    return None


class TmuxSendkeyAction(Action):
    """
    Represents a tmux send-keys command.
    Can be initialized with a tmux key string or converted from a pynput key.
    """
    
    def __init__(self, key_str, modifiers=None):
        """
        Initialize with a tmux key string (e.g., "Enter", "Space", "C-c").
        
        Args:
            key_str (str): The key string in tmux format
            modifiers (list): Optional list of modifier keys ['C', 'M', 'S']
                              C = Control, M = Alt/Meta, S = Shift
        """
        self.key_str = key_str
        self.modifiers = modifiers or []
        
    def __call__(self):
        """
        Execute the tmux send-keys command to send this key to tmux.
        """
        
        # Tmux format for key combinations varies based on key type
        if self.modifiers:
            # For special keys with modifiers (like function keys, arrows, etc.)
            if self.key_str in ["Enter", "Space", "BSpace", "DC", "Down", "Up", "Left", "Right", 
                               "Home", "End", "PageUp", "PageDown", "Tab", "Escape"] or \
               (self.key_str.startswith("F") and self.key_str[1:].isdigit()):
                # Format as: prefix key_name (e.g., "C-M-Up")
                mod_prefix = '-'.join(self.modifiers)
                key_arg = f"{mod_prefix}-{self.key_str}"
                args = ["tmux", "send-keys", key_arg]
            else:
                # Regular character with modifiers
                mod_prefix = '-'.join(self.modifiers)
                key_arg = f"{mod_prefix}-{self.key_str}"
                args = ["tmux", "send-keys", key_arg]
        else:
            # For special keys without modifiers, use the name format
            if self.key_str in ["Enter", "Space", "BSpace", "DC", "Down", "Up", "Left", "Right", 
                               "Home", "End", "PageUp", "PageDown", "Tab", "Escape"] or \
               (self.key_str.startswith("F") and self.key_str[1:].isdigit()):
                args = ["tmux", "send-keys", self.key_str]
            else:
                # Regular character
                args = ["tmux", "send-keys", self.key_str]
                
        cmd_str = " ".join(args)
        
        try:
            # Actually execute the tmux command
            subprocess.run(args, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing tmux command: {e}")
        except FileNotFoundError:
            print("Error: tmux command not found. Is tmux installed and in your PATH?")
    
    @classmethod
    def from_pynput(cls, key, active_modifiers=None, strict=True):
        """
        Convert a pynput key to a TmuxSendkeyAction.
        
        Args:
            key: The pynput key to convert (Key enum, KeyCode, or char)
            active_modifiers (dict): Dictionary with current active modifiers
                                    e.g. {'ctrl': True, 'alt': False, 'shift': False}
            strict (bool): If True, raise an exception if the key can't be converted;
                          otherwise, return None
        
        Returns:
            TmuxSendkeyAction or None: The converted tmux action
            
        Raises:
            ValueError: If the key can't be converted and strict is True
        """
        modifiers = []
        if active_modifiers:
            if active_modifiers.get('ctrl'):
                modifiers.append('C')
            if active_modifiers.get('alt'):
                modifiers.append('M')
            if active_modifiers.get('shift'):
                modifiers.append('S')
        
        # Special keys (like Key.enter, Key.space, etc.)
        if isinstance(key, Key):
            # Don't convert modifier keys themselves when they're pressed
            if key in [Key.ctrl, Key.ctrl_r, Key.alt, Key.alt_r, 
                      Key.shift, Key.shift_r]:
                return None
                
            tmux_key = PYNPUT_TO_TMUX_KEYS.get(key)
            if tmux_key is None:
                if strict:
                    raise ValueError(f"Cannot convert pynput key {key} to tmux format")
                return None
            return cls(tmux_key, modifiers)
        
        # Regular characters: could be str or KeyCode object
        if hasattr(key, 'char') and key.char is not None:
            # KeyCode with character representation
            char = key.char
            
            # Check for macOS special characters first
            if result := _convert_macos_special_char(char, cls):
                return result
                    
            if char in TMUX_SPECIAL_CHARS:
                return cls(TMUX_SPECIAL_CHARS[char], modifiers)
            return cls(char, modifiers)
            
        # String literals
        elif isinstance(key, str):
            # Check for macOS special characters first
            if result := _convert_macos_special_char(key, cls):
                return result
                    
            # Escape special characters
            if key in TMUX_SPECIAL_CHARS:
                return cls(TMUX_SPECIAL_CHARS[key], modifiers)
            # Regular character
            return cls(key, modifiers)
        
        # Try to get string representation as fallback
        try:
            key_str = str(key)
            # Check if it's a quoted character like 'a'
            if key_str.startswith("'") and key_str.endswith("'") and len(key_str) == 3:
                char = key_str[1]
                
                # Check for macOS special characters first
                if result := _convert_macos_special_char(char, cls):
                    return result
                        
                if char in TMUX_SPECIAL_CHARS:
                    return cls(TMUX_SPECIAL_CHARS[char], modifiers)
                return cls(char, modifiers)
        except:
            pass
        
        # Unknown key type
        if strict:
            raise ValueError(f"Unknown key type: {type(key)} - {key}")
        return None

def pynput_casette_to_tmux(casette, *, strict):
    """
    Convert the PynputCasette to a list of TmuxSendkeyAction objects.
    
    This conversion:
    1. Keeps all DelayAction objects
    2. Converts KeyboardPressAction to TmuxSendkeyAction, including modifiers
    3. Removes all KeyboardReleaseAction objects
    4. Removes all mouse-related actions
    5. Tracks active modifiers (ctrl, alt, shift) for proper key combinations
    
    Args:
        strict (bool): If True, raise an exception if any key can't be converted;
                      if False, skip keys that can't be converted
                      
    Returns:
        PynputCasette: A new casette containing only DelayAction and TmuxSendkeyAction objects
        
    Raises:
        ValueError: If strict=True and a key can't be converted
    """
    tmux_actions = []
    
    # Track which modifier keys are currently pressed
    active_modifiers = {
        'ctrl': False,
        'alt': False,
        'shift': False,
    }
    
    for action in casette:
        if isinstance(action, (DelayAction, TmuxSendkeyAction)):
            # Keep all delay actions and tmux actions
            tmux_actions.append(copy(action))

        elif isinstance(action, KeyboardPressAction):
            # Update modifiers state
            if action.key in [Key.ctrl, Key.ctrl_r]:
                active_modifiers['ctrl'] = True
            elif action.key in [Key.alt, Key.alt_r]:
                active_modifiers['alt'] = True
            elif action.key in [Key.shift, Key.shift_r]:
                active_modifiers['shift'] = True
            else:
                # Try to convert keyboard press actions to tmux actions with current modifiers
                try:
                    tmux_action = TmuxSendkeyAction.from_pynput(
                        action.key, 
                        active_modifiers=active_modifiers,
                        strict=strict
                    )
                    if tmux_action is not None:
                        tmux_actions.append(tmux_action)
                except ValueError as e:
                    if strict:
                        raise ValueError(f"Failed to convert action {action}: {e}")
                    
        elif isinstance(action, KeyboardReleaseAction):
            # Update modifiers state on release
            if action.key in [Key.ctrl, Key.ctrl_r]:
                active_modifiers['ctrl'] = False
            elif action.key in [Key.alt, Key.alt_r]:
                active_modifiers['alt'] = False
            elif action.key in [Key.shift, Key.shift_r]:
                active_modifiers['shift'] = False
                
        # Skip all other actions (mouse actions)
        
    # Merge consecutive delay actions for cleaner output
    return PynputCasette(tmux_actions).merge_delays()

##############################################################################
# P L A Y B A C K
##############################################################################

def playback_actions(actions):
    """
    Replays each Action in sequence by simply calling it.
    Press escape to interrupt playback!
    """

    #A safekey
    abort=False
    abort_key=Key.esc
    def on_press(key):
        nonlocal abort
        if key==abort_key:
            abort=True
            safekey_listener.stop()
    safekey_listener = keyboard.Listener(on_press=on_press)
    safekey_listener.start()

    rp.fansi_print(f"Playing back {len(actions)} actions...press {abort_key} to abort!",'white white bold')
    for i, action in enumerate(actions, start=1):
        if abort:
            rp.fansi_print('Aborting playback!','red orange','bold')
            raise KeyboardInterrupt
        action()
        style = None
        if isinstance(action, DelayAction): style = 'dark gray italic'
        if isinstance(action, MouseMoveAction): style = 'dark light gray'
        elif isinstance(action, MouseAction): style = 'gray green yellow bold'
        if isinstance(action, KeyboardReleaseAction): style = 'white blue red blue magenta bold'
        if isinstance(action, KeyboardPressAction): style = 'white blue green blue cyan bold'
        if isinstance(action, TmuxSendkeyAction): style = 'light orange gray orange bold'
        action_str = rp.fansi(action, style)
        num_str = rp.fansi(f"[{i}/{len(actions)}]", "yellow gray")
        print(f"{num_str} {action_str}")

    rp.fansi_print("Playback finished.",'white white bold')


##############################################################################
# D E L A Y   U T I L I T I E S
##############################################################################


def lstrip_delays(actions):
    """
    If the first action is a DelayAction, set its .seconds = 0.
    """
    while actions and isinstance(actions[0], DelayAction):
        actions = actions[1:]
    return actions


def rstrip_delays(actions):
    """
    If the last action is a DelayAction, set its .seconds = 0.
    """
    while actions and isinstance(actions[-1], DelayAction):
        actions = actions[:-1]
    return actions


def strip_delays(actions):
    """
    Set the first and last DelayAction (if any) to 0.0
    """
    actions = lstrip_delays(actions)
    actions = rstrip_delays(actions)
    return actions


##############################################################################
# Default Recorder
##############################################################################


class PynputCasette(list):
    def __init__(self, actions=None):
        super().__init__([] if actions is None else actions)
        self.start_trigger = CmdShiftUpTrigger()
        self.end_trigger = CmdShiftDownTrigger()

    def record(self):
        return PynputCasette(
            self + record_actions(self.start_trigger, self.end_trigger)
        )

    def strip(self):
        return PynputCasette(strip_delays(copy(self)))

    def lstrip(self):
        return PynputCasette(lstrip_delays(copy(self)))

    def rstrip(self):
        return PynputCasette(rstrip_delays(copy(self)))

    def speedup(self, factor):
        self = deepcopy(self)
        for x in self:
            if isinstance(x, DelayAction):
                x.seconds /= factor
        return self

    def slowdown(self, factor):
        return self.speedup(1 / factor)

    def remove_mousemoves(self):
        return PynputCasette(x for x in self if not isinstance(x, MouseMoveAction)).merge_delays()

    def merge_delays(self):
        out = []
        for x in self:
            x = copy(x)
            if isinstance(x, DelayAction) and out and isinstance(out[-1], DelayAction):
                out[-1].seconds+=x.seconds
            else:
                out.append(x)
        return PynputCasette(out)

    def set_all_delays(self,func_or_float):
        """ Takes a float -> float func OR a float"""
        if callable(func_or_float):
            func = func_or_float
        else:
            func_or_float = float(func_or_float)
            func = lambda x: func_or_float

        out = []
        for x in self:
            x=copy(x)
            if isinstance(x, DelayAction):
                x.seconds=func(x.seconds)
            out.append(x)
        return PynputCasette(out)

    def cap_all_delays(self, seconds):
        return self.set_all_delays(lambda x: min(x, seconds))

    def round_all_delays(self, ndigits=2):
        """ Rounds all delays to ndigits decimals; good for compressing via rp.object_to_base64 """
        return self.set_all_delays(lambda x: round(x, ndigits))

    def to_tmux(self, *, strict=True):
        return pynput_casette_to_tmux(self, strict=strict)

    @property
    def duration(self):
        return sum(x.seconds for x in self if isinstance(x, DelayAction))

    def play(self, loop=False):
        for _ in range(1 + 999**999 * loop):
            playback_actions(self)

    def repr(self):
        return f"{type(self).__name__}({repr(self.actions)}"

