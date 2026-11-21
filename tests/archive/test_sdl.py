import pygame
from pygame._sdl2 import controller

pygame.init()
pygame.display.set_mode((1, 1), pygame.HIDDEN)

pygame.joystick.init()
controller.init()

# Explicitly allow joystick and controller events
pygame.event.set_allowed(None)
controller.set_eventstate(True)

print("Joystick events:", pygame.event.get_blocked(pygame.JOYBUTTONDOWN))
print("Controller events:", controller.get_eventstate())

joystick = pygame.joystick.Joystick(0)
joystick.init()

gamepad = controller.Controller(0)

print("Joystick:", joystick.get_name())
print("Controller:", gamepad.name)

print("\nPress buttons and move sticks/D-pad. Ctrl+C to stop.")

try:
    while True:
        for event in pygame.event.get():
            if event.type in (
                pygame.JOYBUTTONDOWN,
                pygame.JOYBUTTONUP,
                pygame.JOYAXISMOTION,
                pygame.JOYHATMOTION,
                pygame.CONTROLLERBUTTONDOWN,
                pygame.CONTROLLERBUTTONUP,
                pygame.CONTROLLERAXISMOTION,
            ):
                print(event)

        pygame.time.wait(10)

except KeyboardInterrupt:
    print("Stopped.")

finally:
    gamepad.quit()
    joystick.quit()
    controller.quit()
    pygame.quit()