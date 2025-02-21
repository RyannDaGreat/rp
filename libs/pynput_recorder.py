from copy import copy, deepcopy
import rp
import time
import abc

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
            if not "__" in attr
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

    def cap_all_delays(self,seconds):
        return self.set_all_delays(lambda x:min(x,seconds))

    def play(self, loop=False):
        for _ in range(1 + 999**999 * loop):
            playback_actions(self)

    def repr(self):
        return f"{type(self).__name__}({repr(self.actions)}"

