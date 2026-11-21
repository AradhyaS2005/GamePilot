
import ctypes
from ctypes import wintypes


# XInput button bitmasks
BUTTONS = {
    0x1000: "A",
    0x2000: "B",
    0x4000: "X",
    0x8000: "Y",

    0x0100: "LB",
    0x0200: "RB",

    0x0010: "START",
    0x0020: "BACK",

    0x0040: "L3",
    0x0080: "R3",

    0x0001: "DPAD_UP",
    0x0002: "DPAD_DOWN",
    0x0004: "DPAD_LEFT",
    0x0008: "DPAD_RIGHT",
}


# Represents the controller's raw input data
class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons", wintypes.WORD),
        ("bLeftTrigger", ctypes.c_ubyte),
        ("bRightTrigger", ctypes.c_ubyte),
        ("sThumbLX", ctypes.c_short),
        ("sThumbLY", ctypes.c_short),
        ("sThumbRX", ctypes.c_short),
        ("sThumbRY", ctypes.c_short),
    ]


# Represents the complete controller state
class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPacketNumber", wintypes.DWORD),
        ("Gamepad", XINPUT_GAMEPAD),
    ]


class XInputController:

    def __init__(self, controller_index=0):
        self.controller_index = controller_index

        # Load the Windows XInput library
        self.xinput = ctypes.WinDLL("XInput1_4.dll")

        # Define the XInputGetState function signature
        self.xinput.XInputGetState.argtypes = [
            wintypes.DWORD,
            ctypes.POINTER(XINPUT_STATE)
        ]

        self.xinput.XInputGetState.restype = wintypes.DWORD

    def get_state(self):
        state = XINPUT_STATE()

        result = self.xinput.XInputGetState(
            self.controller_index,
            ctypes.byref(state)
        )

        # Result 0 means successful read
        if result != 0:
            return None

        pad = state.Gamepad

        # Find all currently pressed buttons
        pressed_buttons = [
            name for mask, name in BUTTONS.items()
            if pad.wButtons & mask
        ]

        return {
            "buttons": pressed_buttons,

            "left_trigger": pad.bLeftTrigger,
            "right_trigger": pad.bRightTrigger,

            "left_stick": (
                pad.sThumbLX,
                pad.sThumbLY
            ),

            "right_stick": (
                pad.sThumbRX,
                pad.sThumbRY
            ),

            "packet_number": state.dwPacketNumber
        }

    def is_connected(self):
        return self.get_state() is not None
