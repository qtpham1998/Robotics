#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for reading an NXT ultrasonic sensor connected to PORT_1 of the BrickPi3
# 
# Hardware: Connect an NXT ultrasonic sensor to BrickPi3 Port 1.
# 
# Results:  When you run this program, you should see the distance in CM.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi333 as brickpi3 # import the BrickPi3 drivers
from os import system
import MCL
import movement
import random
import particleDataStructures
from navigate import navigateToWaypoint, correction

BP = brickpi3.BrickPi333() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# Configure for an NXT ultrasonic sensor.
# BP.set_sensor_type configures the BrickPi3 for a specific sensor.
# BP.PORT_1 specifies that the sensor will be on sensor port 1.
# BP.SENSOR_TYPE.NXT_ULTRASONIC specifies that the sensor will be an NXT ultrasonic sensor.
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.NXT_ULTRASONIC)

# MOTOR PORTS
leftMotor = BP.PORT_B
rightMotor = BP.PORT_C
# SENSOR PORTS
sonarSensor = BP.PORT_4
 
BP.set_motor_limits(leftMotor, 70, 200)
BP.set_motor_limits(rightMotor, 70, 200)

# OFFSETS
OFFSETX = 40
OFFSETY = 200
SENSOR_OFFSET = 12.5 #cm
MULT = 10

N = 100 #Particle Num
mcl = MCL.MCL()
mov = movement.Movement(BP, mcl)

def navigate():
    coordinates = [(180, 30), (180, 54), (138, 54), (138, 168), (114, 168), (114, 84), (84, 84), (84, 30)]
    for x, y in coordinates:
        navigateToWaypoint(x, y, mcl, mov)
        '''
        reading = BP.get_sensor(sonarSensor) + SENSOR_OFFSET
        print("The sensor reading is %d" %reading)
        correction(reading, mcl, mov)
        while not isinstance(reading, int):
            try:
                reading = BP.get_sensor(sonarSensor) + SENSOR_OFFSET
            except brickpi3.SensorError as error:
                pass
        if reading != 255:
            mcl.localisation(reading)
        '''    
            #TODO: Take the mean of the particles and the senesor reading. calculate the error and make adjustment, Notice that we should use the 2% erorr rate we got last time
            
try:
    navigate()
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all() 
    
    # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
'''
try:
    i = 0
    for i in range(15):
        # read and display the sensor value
        # BP.get_sensor retrieves a sensor value.
        # BP.PORT_1 specifies that we are looking for the value of sensor port 1.
        # BP.get_sensor returns the sensor value (what we want to display).
        mov.rotateDegree(45)
        mov.wait()
        reading = None
        while not isinstance(reading, int):
            try:
                reading = BP.get_sensor(sonarSensor)
            except brickpi3.SensorError as error:
                #print(error)
                pass
        print(reading)
        if reading != 255:
            mcl.localisation(reading)
        mov.moveForward(10)
        mov.wait()
        reading = None
        while not isinstance(reading, int):
            try:
                reading = BP.get_sensor(sonarSensor)
            except brickpi3.SensorError as error:
                #print(error)
                pass
        time.sleep(0.2)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all() 
    '''
    # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
