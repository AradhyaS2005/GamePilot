import ctypes
from ctypes import wintypes
import time

# load windows XInput DLL
xinput = ctypes.WinDLL("XInput1_4.dll")

# XInput button constants
BUTTONS = {
    0x1000: "A",
    0x2000: "B",
    0x4000: "X",
    0x8000: "Y",

    0x0010: "START",
    0x0020: "BACK",

    0x0100: "LB",
    0x0200: "RB",

    0x0040: "L3",
    0x0080: "R3",

    0x0001: "DPAD_UP",
    0x0002: "DPAD_DOWN",
    0x0004: "DPAD_LEFT",
    0x0008: "DPAD_RIGHT"
}

# IInput datastructures
class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons", wintypes.WORD),
        ("bLeftTrigger", ctypes.c_ubyte),
        ("bRightTrigger", ctypes.c_ubyte),
        ("sThumbLX", ctypes.c_short),
        ("sThumbLY", ctypes.c_short),
        ("sThumbRX", ctypes.c_short),
        ("sThumbRY", ctypes.c_short)
    ]

class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPacketNumber", wintypes.DWORD),
        ("Gamepad", XINPUT_GAMEPAD),
    ]

# Define function signature
xinput.XInputGetState.argtypes = [
    wintypes.DWORD,
    ctypes.POINTER(XINPUT_STATE)
] 
xinput.XInputGetState.restype = wintypes.DWORD

print("XInput controller test started.")
print("Print buttons or move the sticks. Press ctrl+c to stop.\n")

previous_state = None

try:
    while True:
        state = XINPUT_STATE()

        # Controller index 0
        result = xinput.XInputGetState(0, ctypes.byref(state))

        if result == 0:
            pad = state.Gamepad

            current_state = (
                pad.wButtons,
                pad.bLeftTrigger,
                pad.bRightTrigger,
                pad.sThumbLX,
                pad.sThumbLY,
                pad.sThumbRX,
                pad.sThumbRY,
            )

            if current_state != previous_state:
                pressed = [
                    name for mask, name in BUTTONS.items()
                    if pad.wButtons & mask
                ]

                print("Buttons:", pressed)
                print("Triggers:", pad.bLeftTrigger, pad.bRightTrigger)
                print("Left stick:", pad.sThumbLX, pad.sThumbLY)
                print("Left stick:", pad.sThumbRX, pad.sThumbRY)
                print("-" * 40)

                previous_state = current_state

            elif previous_state is not None:
                print("Controller disconnected.")
                previous_state = None

            time.sleep(0.4)

except KeyboardInterrupt:
    print("\nTest stopped.")                

