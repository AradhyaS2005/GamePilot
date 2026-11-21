class InputMapper:

    def __init__(self):
        # Default controller-to-action mappings
        self.button_mapping = {
            "A": "LEFT_CLICK",
            "B": "RIGHT_CLICK",
            "X": "KEY_E",
            "Y": "KEY_R",

            "LB": "KEY_Q",
            "RB": "KEY_F",

            "START": "KEY_ENTER",
            "BACK": "KEY_ESCAPE",

            "DPAD_UP": "MOVE_UP",
            "DPAD_DOWN": "MOVE_DOWN",
            "DPAD_LEFT": "MOVE_LEFT",
            "DPAD_RIGHT": "MOVE_RIGHT",
        }

        # Minimum stick movement required to register input
        self.deadzone = 8000

    def map_inputs(self, controller_state):

        if controller_state is None:
            return {}

        actions = {}

        # 1. Map buttons
        pressed_buttons = controller_state["buttons"]

        for button in pressed_buttons:

            action = self.button_mapping.get(button)

            if action:
                actions[action] = True

        # 2. Map left analog stick 
        left_x, left_y = controller_state["left_stick"]

        if left_x > self.deadzone:
            actions["MOVE_RIGHT"] = True

        elif left_x < -self.deadzone:
            actions["MOVE_LEFT"] = True      
 
        if left_y > self.deadzone:            # positive Y = down
            actions["MOVE_DOWN"] = True       # acc to XInput
        
        elif left_y < -self.deadzone:         # negative Y = down
            actions["MOVE_UP"] = True         # acc to XInput

        # 3. Map triggers
        if controller_state["left_trigger"] > 30:
            actions["LEFT_TRIGGER"] = True

        if controller_state["right_trigger"] > 30:
            action["RIGHT_TRIGGER"] = True 

        return actions                            