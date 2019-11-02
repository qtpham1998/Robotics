#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for running a motor to a target position set by the encoder of another motor.
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

leftMotor = BP.PORT_B
rightMotor = BP.PORT_C

def calculateTargetDistance(dist):
    return 1.5 * (dist / (7.3 * math.pi)) * 360

def moveForward(dist): # distance in cm
    try:
        print("forward")
        BP.offset_motor_encoder(leftMotor, BP.get_motor_encoder(leftMotor))
        BP.offset_motor_encoder(rightMotor, BP.get_motor_encoder(rightMotor))
    except IOError as error:
        print (error)
    targetDist = calculateTargetDistance(dist) 
    BP.set_motor_limits(leftMotor, 70, 200)
    BP.set_motor_limits(rightMotor, 70, 200)
    BP.set_motor_position(leftMotor, targetDist)
    BP.set_motor_position(rightMotor, targetDist)

def wait():
    print("waiting")
    time.sleep(1)
    vB = BP.get_motor_status(leftMotor)[3]
    vC = BP.get_motor_status(rightMotor)[3]
    while(vB != 0 or vC != 0):
        vB = BP.get_motor_status(leftMotor)[3]
        vC = BP.get_motor_status(rightMotor)[3]
    print("wait finished")


def rotateDegree(degrees):
    print("rotate")
    try:
        BP.offset_motor_encoder(leftMotor, BP.get_motor_encoder(leftMotor))
        BP.offset_motor_encoder(rightMotor, BP.get_motor_encoder(rightMotor))
    except IOError as error:
        print (error)
    pos = calculateTargetDistance(degrees / 360 * 14 * math.pi)
    print(pos)
    BP.set_motor_position(rightMotor, pos)
    BP.set_motor_position(leftMotor, -pos)

def moveSquare(num):
    for n in range(num):
        for i in range(4):
            moveForward(-42.2)
            wait()
            rotateDegree(90)
            wait()

def testTurn():
    moveForward(40)
    wait()
    rotateDegree(90)
    wait()
    moveForward(40)

try:

    moveSquare(1)
    #testTurn()


except KeyboardInterrupt:
    BP.reset_all()
