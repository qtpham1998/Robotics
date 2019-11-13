from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import brickpi333 as brickpi3 # import the BrickPi3 drivers
import MCL
import movement
from navigate import navigateToWaypoint, getIntervalCoordinates

BP = brickpi3.BrickPi333() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# MOTOR PORTS
leftMotor = BP.PORT_B
rightMotor = BP.PORT_C
BP.set_motor_limits(leftMotor, 70, 200)
BP.set_motor_limits(rightMotor, 70, 200)

# SONAR SENSOR
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.NXT_ULTRASONIC)
sonarSensor = BP.PORT_4
SENSOR_OFFSET = 12.5 #cm

# CONSTANTS
N = 100 #Particle Num
mcl = MCL.MCL()
mov = movement.Movement(BP, mcl)

def navigate():
    coordinates = [(180, 30), (180, 54), (138, 54), (138, 168), (114, 168), (114, 84), (84, 84), (84, 30)]
    for xTarget, yTarget in coordinates:
        print("-----------------------------------------------------")
        navigationCoordinates = getIntervalCoordinates(xTarget, yTarget, mcl, 20)
        for x, y in navigationCoordinates:
            navigateToWaypoint(x, y, mcl, mov)
        reading = BP.get_sensor(sonarSensor)
        print("The sensor readings are %d" %reading)
        if reading < 255:
            mcl.localisation(reading)


try:
    navigate()
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()