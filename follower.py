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
    BP.set_motor_position_kp(leftMotor, 70)
    BP.set_motor_position_kp(rightMotor, 70)
    BP.set_sensor_type(sonarSensor, BP.SENSOR_TYPE.NXT_ULTRASONIC)
    print("Finalised initialisation")

def move(power):
    print("setting DPS as %d" % power)
    BP.set_motor_dps(leftMotor, power)
    BP.set_motor_dps(rightMotor, power)

def resetPower():
    print("Reset power")
    BP.set_motor_dps(leftMotor, 0)
    BP.set_motor_dps(rightMotor, 0)
    wait()

def wait():
    print("wait")
    time.sleep(1)
    vLeft = BP.get_motor_status(leftMotor)[3]
    vRight = BP.get_motor_status(rightMotor)[3]
    while(vLeft != 0 or vRight != 0):
        vLeft = BP.get_motor_status(leftMotor)[3]
        vRight = BP.get_motor_status(rightMotor)[3]
    print("wait finished")

try:
    targetDist = 30
    threshold = 3
    initialise()
    while True:
        # read and display the sensor value
        try:
            value = BP.get_sensor(sonarSensor)
            diff = targetDist - value
            print(value)                         # print the distance in CMi
            if (abs(diff) < threshold):
                resetPower()
            elif (abs(diff) < 10):
                move(diff * 10)
            else:
                move(targetDist - value)
        except brickpi3.SensorError as error:
            print(error)
        
        time.sleep(0.5) 

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
