from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import random
from math import pi, cos, sin, tan, atan2, sqrt, exp
from os import system
import particleDataStructure

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# MOTOR PORTS
leftMotor = BP.PORT_B
rightMotor = BP.PORT_C
# SENSOR PORTS
sonarSensor = BP.PORT_4

# OFFSETS
OFFSETX = 400
OFFSETY = 200
SENSOR_OFFSET = 12.5 #cm
MULT = 10

N = 100 #Particle Num


def initialise():
    '''
    Prepares system and robot
    '''
    system('clear')
    global particleSet
    particletSet.initialise()
    BP.set_sensor_type(sonarSensor, BP.SENSOR_TYPE.NXT_ULTRASONIC)
    BP.set_motor_limits(leftMotor, 70, 200)
    BP.set_motor_limits(rightMotor, 70, 200)

try:
    initialise()
    navigate() 
    #drawSquare(10)
    #moveSquare(1, 10)


except KeyboardInterrupt:
    BP.reset_all()

