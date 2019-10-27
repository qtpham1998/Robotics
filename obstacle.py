#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code moves the robot forward and back followed by a rotation when it encounters an obstacle.
#
# Hardware: Connect EV3 or NXT motors to the BrickPi3 motor ports B and C. Make sure that the BrickPi3 is running on a 9v power supply.
#
# Results:  When you run this program, motor C power will be controlled by the position of motor B. Manually rotate motor B, and motor C's power will change.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import math

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# Motor ports
rightMotor = BP.PORT_B
leftMotor = BP.PORT_C
# Sensor ports 
rightSensor = BP.PORT_4
leftSensor = BP.PORT_3

def initialise():
    BP.set_motor_limits(leftMotor, 70, 200)
    BP.set_motor_limits(rightMotor, 70, 200)
    BP.set_sensor_type(leftSensor, BP.SENSOR_TYPE.TOUCH)
    BP.set_sensor_type(rightSensor, BP.SENSOR_TYPE.TOUCH)
    print("Finalised initialisation")

def getSensorReadings():
    return BP.get_sensor(leftSensor), BP.get_sensor(rightSensor)

def resetPower():
    BP.set_motor_power(leftMotor, 0)
    BP.set_motor_power(rightMotor, 0)
    wait()

def moveForward():
    print("advancing")
    BP.set_motor_power(leftMotor, -30)
    BP.set_motor_power(rightMotor, -30)

def moveBack():
    print("moving back")
    BP.set_motor_power(leftMotor, 30)
    BP.set_motor_power(rightMotor, 30)

def wait():
    print("waiting")
    time.sleep(1)
    vLeft = BP.get_motor_status(leftMotor)[3]
    vRight = BP.get_motor_status(rightMotor)[3]
    while(vLeft != 0 or vRight != 0):
        vLeft = BP.get_motor_status(leftMotor)[3]
        vRight = BP.get_motor_status(rightMotor)[3]
    print("wait finished")

def rotateDegrees(degrees):
    pos = 12.7 * degrees / 7.3
    print("rotating %d degrees" % degrees)
    try:
        BP.offset_motor_encoder(rightMotor, BP.get_motor_encoder(rightMotor))
        BP.offset_motor_encoder(leftMotor, BP.get_motor_encoder(leftMotor))
    except IOError as error:
        print (error)
    print(pos)
    BP.set_motor_position(rightMotor, -pos)
    BP.set_motor_position(leftMotor, pos)

def backTrack():
    print("obstacle detected")
    resetPower()
    moveBack()
    leftSense, rightSense = getSensorReadings()
    while (leftSense == 1 or rightSense == 1):
        time.sleep(1)
        leftSense, rightSense = getSensorReadings()
    resetPower()

def turnRight():
    rotateDegrees(-90)

def turnLeft():
    rotateDegrees(90)

def turnAround():
    rotateDegrees(180)

try:
    initialise()
    moveForward()
    while True:
        try:
            leftSense, rightSense = getSensorReadings()
            print("Left sensor: %d; Right sensor: %d" % (leftSense, rightSense))
            if (leftSense == 1 or rightSense == 1):
		backTrack()
	        if (leftSense == 1 and rightSense == 1):
	            turnAround()
	        elif (leftSense == 1):
	            turnRight()
	        elif (rightSense == 1):
	            turnLeft()
                wait()
		moveForward()
        except brickpi3.SensorError as error:
            print(error)
        time.sleep(1)


except KeyboardInterrupt:
    BP.reset_all()
