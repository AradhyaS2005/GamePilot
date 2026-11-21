from core.input_mapper import InputMapper

mapper = InputMapper()

# Simulated controller input
controller_state = {
    "buttons": ["A", "DPAD_UP"],
    "left_trigger": 0,
    "right_trigger": 0,
    "left_stick": (20000, 15000),
    "right_stick": (0, 0),
    "packet_number": 1
}

actions = mapper.map_inputs(controller_state)

print("Controller actions: ")
print(actions)