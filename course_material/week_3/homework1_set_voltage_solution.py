#!/usr/bin/python

"""
   +---------------------------------------------------------+
   | Warning: This example demonstrates the impulse control  |
   | method to be used with solenoids and should NOT be used |
   | for servo motors with end-stops. ~~~~~~~~~~~~~~~~~~~~~~ |
   +---------------------------------------------------------+
"""

from src.sensorimotor import Sensorimotor
from time import sleep

def print_position(data):
    print(''.join('{0: .2f} '.format(k) for k in data))

def main():
    motors = Sensorimotor(number_of_motors = 2, verbose = False)

    try:
        # Check for motors
        N = motors.ping()
        print("Found {0} motors.".format(N))
        sleep(1.0)

        #TODO: set this according to your supply voltage and desired max. motor speed
        motors.set_voltage_limit([0.16, 0.16])

        # Start motors
        motors.start()

        counter = 0
        while(counter < 10):
            #moves left
            motors.apply_impulse([0.1, 0.1])
            print("tak")
            counter = counter +1
            sleep(0.1)
        counter = 0

        while(counter < 10):
            #move right
            motors.apply_impulse([0.1, -0.1])
            print("tak")
            counter = counter +1
            sleep(0.1)
        counter = 0
        motors.stop()

    except (KeyboardInterrupt, SystemExit):
        # Stop motors
        print("\rAborted, stopping motors")
        motors.stop()

    except:
        # Script crashed?
        print("\rException thrown, stopping motors")
        motors.stop()

    print("____\nDONE.")


if __name__ == "__main__":
    main()
