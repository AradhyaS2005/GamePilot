import time
from core.controller import XInputController

controller = XInputController()

print("GamePilot XInput test started!")

previous_state = None

try:
    while True:
        state = controller.get_state()

        if state is None:
            if previous_state is not None:
                print("Controller disconnected.")

            previous_state = None

        elif state != previous_state:
            print("Buttons:", state["buttons"])
            print("Left trigger:", state["left_trigger"])
            print("Right trigger:", state["right_trigger"])
            print("Left stick:", state["left_stick"])
            print("Right stick:", state["right_stick"])
            print("-" * 40)

            previous_state = state

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nTest stopped.")