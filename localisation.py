from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
from os import system
import MCL
import movement
import brickpi333 as brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi333() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.reset_all()

# MOTOR PORTS
leftMotor = BP.PORT_B
rightMotor = BP.PORT_C
# SENSOR PORTS
sonarSensor = BP.PORT_3

BP.set_motor_limits(leftMotor, 70, 200)
BP.set_motor_limits(rightMotor, 70, 200)
BP.set_sensor_type(sonarSensor, BP.SENSOR_TYPE.NXT_ULTRASONIC)

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
    #movement.setBP(BP)

def localisation():
    for i in range(50):
        try:
            particleSet = MCL.MCL(BP.get_sensor(sonarSensor))
            for p in particleSet:
                print("drawParticles:" + str((p.x, p.y, p.theta, p.w)))
                print(str((p.x, p.y, p.theta, p.w)))
            time.sleep(0.2)
        except brickpi3.SensorError as error:
            print(error)

try:
    #initialise()
    #print(BP.get_sensor(sonarSensor))
    #movement.rotateDegree(90)
    localisation()
    #navigate() 
    #drawSquare(10)
    #moveSquare(1, 10)

except KeyboardInterrupt:
    BP.reset_all()

