import ctypes
from ctypes import wintypes

# Windows SendInput constants

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

MOUSEEVENTF_MOVE = 0x0001

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

MOUSEEVENTF_RIGHTTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

KEYEVENTF_KEYUP = 0x0002

# Pointer-sized integer for 32-bit / 64-bit Windows
ULONG_PTR = (
    ctypes.c_ulonglong
    if ctypes.sizof(ctypes.c_void_p) == 8
    else ctypes.c_ulong
)

# Windows MOUSEINPUT structure
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]

# Windows KEYBOARDINPUT structure
class KEYBOARDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]    

# INPUT union
class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBOARDINPUT),
    ]    

# Complete Windows INPUT structure
class INPUT(ctypes.Structure):
    _anonymous_ = ("union",)

    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUT_UNION),
    ]

# Virtual key codes for keyboard actions
KEY_MAP = {
    "KEY_A": 0x41,
    "KEY_B": 0x42,
    "KEY_C": 0x43,
    "KEY_D": 0x44,
    "KEY_E": 0x45,
    "KEY_F": 0x46,
    "KEY_G": 0x47,
    "KEY_H": 0x48,
    "KEY_I": 0x49,
    "KEY_J": 0x4A,
    "KEY_K": 0x4B,
    "KEY_L": 0x4C,
    "KEY_M": 0x4D,
    "KEY_N": 0x4E,
    "KEY_O": 0x4F,
    "KEY_P": 0x50,
    "KEY_Q": 0x51,
    "KEY_R": 0x52,
    "KEY_S": 0x53,
    "KEY_T": 0x54,
    "KEY_U": 0x55,
    "KEY_V": 0x56,
    "KEY_W": 0x57,
    "KEY_X": 0x58,
    "KEY_Y": 0x59,
    "KEY_Z": 0x5A,

    "KEY_ENTER": 0x0D,
    "KEY_ESCAPE": 0x1B,
    "KEY_SPACE": 0x20,
    "KEY_TAB": 0x09,
    "KEY_BACKSPACE": 0x08,
}

class InputExecutor:

    def __init__(self, mouse_speed=6):

        # Load Windows User32 library
        self.user32 = ctypes.WinDLL("user32", use_last_error=True)

        # Configure SendInput function
        self.user32.SendInput.argtypes = [
            wintypes.UINT,
            ctypes.POINTER(INPUT),
            ctypes.c_int,
        ]

        self.user32.SendInput.restype = wintypes.UINT

        self.mouse_speed = mouse_speed

        # Track currently held inputs
        self.held_mouse_buttons = set()
        self.held_keys = set()

    def _send(self, input_data):

        result = self.user32.SendInput(
            1,
            ctypes.byref(input_data),
            ctypes.sizeof(INPUT),
        )

        if result != 1:
            error = ctypes.get_last_error()
            raise ctypes.WinError(error)

    def _mouse_event(self, flags, dx=0, dy=0):

        event = INPUT(
            type=INPUT_MOUSE,
            mi=MOUSEINPUT(
                dx,
                dy,
                0,
                flags,
                0,
                0,
            ),
        )

        self._send(event)

    def _keyboard_event(self, virtual_key, key_up=False):

        flags = KEYEVENTF_KEYUP if key_up else 0

        event = INPUT(
            type=INPUT_KEYBOARD,
            ki=KEYBOARDINPUT(
                virtual_key,
                0,
                flags,
                0,
                0,
            ),
        )

        self._send(event)

    def _update_mouse_buttons(self, actions):

        mouse_mapping = {
            "LEFT_CLICK": (
                MOUSEEVENTF_LEFTDOWN,
                MOUSEEVENTF_LEFTUP,
            ),
            "RIGHT_CLICK": (
                MOUSEEVENTF_RIGHTTDOWN,
                MOUSEEVENTF_RIGHTUP,
            ),
        }

        for action, (down_flag, up_flag) in mouse_mapping.items():

            is_pressed = bool(actions.get(action, False))

            if is_pressed and action not in self.held_mouse_buttons:

                self._mouse_event(down_flag)
                self.held_mouse_buttons.add(action)

            elif not is_pressed and action in self.held_mouse_buttons:

                self._mouse_event(up_flag)
                self.held_mouse_buttons.remove(action)

    def _update_keyboard(self, actions):

        for action, virtual_key in KEY_MAP.items():

            is_pressed = bool(actions.get(action, False))

            if is_pressed and action not in self.held_keys:

                self._keyboard_event(virtual_key)
                self.held_keys.add(action)

            elif not is_pressed and action in self.held_keys:

                self._keyboard_event(virtual_key, key_up=True)
                self.held_keys.remove(action)

    def _move_mouse(self, actions):

        dx = 0
        dy = 0

        if actions.get("MOVE_RIGHT", False):
            dx += self.mouse_speed

        if actions.get("MOVE_LEFT", False):
            dx -= self.mouse_speed

        if actions.get("MOVE_DOWN", False):
            dy += self.mouse_speed
        
        if actions.get("MOVE_UP", False):
            dy -= self.mouse_speed    

        if dx != 0 or dy != 0:
            self._mouse_event(MOUSEEVENTF_MOVE, dx, dy)

    def execute(self, actions):

        if actions is None:
            actions = {}

        self._update_mouse_buttons(actions)
        self._update_keyboard(actions)
        self._move_mouse(actions)

    def release_all(self):

        # Release every held mouse button
        for action in list(self.held_mouse_buttons):

            if action == "LEFT_CLICK":
                self._mouse_event(MOUSEEVENTF_LEFTUP)

            elif action == "RIGHT_CLICK":
                self._mouse_event(MOUSEEVENTF_RIGHTUP)

            self.held_mouse_buttons.remove(action)

        # Release every held keyboard key
        for action in list(self.held_keys):

            self._keyboard_event(KEY_MAP[action], key_up=True)
            self.held_keys.remove(action)                              