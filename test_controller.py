import pygame
import time

pygame.init()
pygame.joystick.init()
pygame.display.set_mode((1,1), pygame.HIDDEN)

count = pygame.joystick.get_count()

print("Total controllers:", count)
controllers = []

for i in range(count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

    controllers.append(joystick)

    print("\n----------------------------------------------")
    print("Device Index:", i)
    print("Name:", joystick.get_name())
    print("Instance ID:", joystick.get_instance_id())
    print("Axes:", joystick.get_numaxes())
    print("Buttons:", joystick.get_numbuttons())
    print("Hats:", joystick.get_numhats())

print("\n----Monitoring all devices----")

try:
    while True:

        pygame.event.pump()

        for joystick in controllers:
            print(f"\nDevice {joystick.get_id()}")

            print("Axes:", [
                round(joystick.get_axis(i), 2)
                for i in range(joystick.get_numaxes())
            ])

            print("Buttons:", [
                joystick.get_button(i) 
                for i in range(joystick.get_numbuttons())
            ])                

            print("Hats:", [
                joystick.get_hat(i)
                for i in range(joystick.get_numhats())
            ])

        time.sleep(0.5)    

except KeyboardInterrupt:
    print("\nstopped.")   
    
finally:
    pygame.quit()            