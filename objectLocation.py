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

import os
import sys
import MCL
import movement
from sensors import Sensors
import brickpi333 as brickpi3
BP = brickpi3.BrickPi333()
S = Sensors(BP)

# MOTOR PORTS
leftMotor = BP.PORT_B
rightMotor = BP.PORT_C
# SENSOR PORTS

BP.set_motor_limits(leftMotor, 70, 200)
BP.set_motor_limits(rightMotor, 70, 200)

# OFFSETS
SENSOR_OFFSET = 10  # cm
N = 100  # Particle Num
ORIGIN_X = 84
ORIGIN_Y = 30
mcl = MCL.MCL()
mov = movement.Movement(BP, mcl, S)

from math import pi, atan2, sqrt, atan, sin, cos

def navigate():
    coordinates = [(120, 30,90)]
    for x, y, start in coordinates:
        #navigateToWaypoint(x, y, mcl, mov)
        findBottle(start)
        mov.wait()
        moveToBottle()
        mov.moveForward(-20, True)


def findBottle(start):
    x, y, theta = mcl.getAverageCoordinate()
    rots = 10
    diff = list(range(19))
    max_degree = 0
    max_diff = -1
    while True:
        average_loc = 0
        S.rotateSonarSensor(100)
        S.setSensorDPS(-100)
        diff = -1
        degree = 0
        while (degree >= start - 180):
            reading = S.getSensorReading()
            degree = S.getCurrentDegree()
            (m, wall) = mcl.getWall(x, y, degree)
            if reading != 255 and (abs(reading - m)) > 25 and reading < m:
                diff = abs(reading - m)
            if diff > max_diff:
                max_degree = degree
                max_diff = diff
        S.setSensorDPS(0)    
        S.resetSonarSensorPos() 
        print("The max index is "+ str(max_degree))
        if max_diff != -1:
            break
        mov.moveForward(40, True)
    mov.rotateDegree(fixAngle(theta - max_degree))


def moveToBottle():
    reading = S.getSensorReading()
    mov.moveForward(reading - 30, True)
    #mov.setMotorDPS(-200,reading)    

def fixAngle(angle):
    '''
    Correct the angle such that it is in the [-180,180] range
    @param angle The angle to correct
    @return The corrected angle
    '''
    while (angle > 180):
        angle -= 360
    while (angle < -180):
        angle += 360
    return angle


def intervalCoordinates(xTarget, yTarget, mcl, interval):
    xCoord, yCoord, _ = mcl.getAverageCoordinate()
    xDiff = abs(xCoord - xTarget)
    yDiff = abs(yCoord - yTarget)
    theta = atan2(yDiff, xDiff)
    distance = sqrt(xDiff * xDiff + yDiff * yDiff)

    coordinates = []

    xSign = 1
    ySign = 1

    if (xTarget < xCoord):
        xSign = -1
    if (yTarget < yCoord):
        ySign = -1

    while (distance >= interval):
        xCoord += xSign * cos(theta) * interval
        yCoord += ySign * sin(theta) * interval
        coordinates.append((xCoord, yCoord))
        distance -= interval

    if (distance > 0):
        coordinates.append((xTarget, yTarget))

    return coordinates


def navigateToWaypoint(xTarget, yTarget, mcl, mov):
    print("-----------------------------------------------------")
    coordinates = intervalCoordinates(xTarget, yTarget, mcl, 20)
    for (X,Y) in coordinates:
        distToMove, degToRot = getTravelInfo(mcl, X, Y)
        if abs(degToRot) > 3:
            mov.rotateDegree(degToRot)
        mov.moveForward(distToMove, True)
        reading = S.getSensorReading()
        if reading < 255:
            mcl.localisation(reading)
    reading = S.getSensorReading()
    if reading < 255:
        correction(reading, mcl, mov)
        reading = S.getSensorReading()
        if reading < 255:
            mcl.localisation(reading)

def correction(z, mcl, mov):
    pass
    #x, y, t = mcl.getAverageCoordinate()    
    #(m, wall) = mcl.getWall(x, y, t)
    #if abs(m - z) > 3 and z < 250:
    #    mov.moveForward(z-m, False)            


def getTravelInfo(mcl, targetX, targetY):
    xCoordinate, yCoordinate, theta = mcl.getAverageCoordinate()
    print("The current (X,Y) coordinates are (%d, %d). Moving to (%d, %d)" %(xCoordinate,yCoordinate,targetX,targetY))
    xDiff = targetX - xCoordinate
    yDiff = targetY - yCoordinate
    deg = fixAngle(atan2(yDiff, xDiff) * 180 / pi - theta)
    print("The current angle is %d, rotating %d degrees" %(theta, deg))
    distToTravel = sqrt(xDiff * xDiff + yDiff * yDiff)
    return distToTravel, deg

try: 
    navigate()
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()     
