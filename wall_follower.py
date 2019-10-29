#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code sets the robot to follow an obstacle at a set distance of 30
# 
# Hardware: Connect an NXT ultrasonic sensor to BrickPi3 Port 1.
# 
# Results:  When you run this program, you should see the distance in CM.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# Motor ports
rightMotor = BP.PORT_B
leftMotor = BP.PORT_C
# Sensor ports
sonarSensor = BP.PORT_4

# Configure for an NXT ultrasonic sensor.
def initialise():
    BP.set_motor_limits(leftMotor, 70, 200)
    BP.set_motor_limits(rightMotor, 70, 200)
    BP.set_sensor_type(sonarSensor, BP.SENSOR_TYPE.NXT_ULTRASONIC)

def resetPower():
    BP.set_motor_power(leftMotor, 0)
    BP.set_motor_power(rightMotor, 0)
    wait()

def move(power):
    print("advancing")
    BP.set_motor_power(leftMotor, power)
    BP.set_motor_power(rightMotor, power)

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

def wait():
    print("waiting")
    vLeft = BP.get_motor_status(leftMotor)[3]
    vRight = BP.get_motor_status(rightMotor)[3]
    while(vLeft != 0 or vRight != 0):
        vLeft = BP.get_motor_status(leftMotor)[3]
        vRight = BP.get_motor_status(rightMotor)[3]
        time.sleep(0.05)
    print("wait finished")

try:
    targetDist = 30
    initialise()
    while True:
        # read and display the sensor value
        try:
            value = BP.get_sensor(sonarSensor)
            print(value)                         # print the distance in CMi
            if (targetDist == value):
                move(30)
            else:
                rotateDegrees(targetDist - value)
        except brickpi3.SensorError as error:
            print(error)
        
        time.sleep(0.5) 

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
