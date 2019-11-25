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
import statistics
import brickpi333 as brickpi3
import time

ORIGIN_X = 84
ORIGIN_Y = 30
BP = brickpi3.BrickPi333()
S = Sensors(BP)
mcl = MCL.MCL()
mov = movement.Movement(BP, mcl, S)

from math import pi, atan2, sqrt, atan, sin, cos

def navigate():
    coordinates = [(90, 70, 70),(90, 70, 135),(84,30,0)]
    for x, y, theta in coordinates:
        findBottle()
        navigateToWaypoint(x, y, mcl, mov)
        fixOrientation(theta, mcl, mov)
    #navigateToWaypoint(84, 30, mcl, mov)

def findBottle():
    detected = False
    abnormalList = []
    while not detected:
        print("============================")
        x, y, theta = mcl.getAverageCoordinate()
        S.rotateSonarSensor(90)
        degree = 90
        S.setSensorDPS(-50)
        while degree > -90:
            reading, degree = S.getSensorDegreeReading()
            (m, wall) = mcl.getWall(x, y, degree + theta)
            if reading < 100 and m - reading > 20:
                degreeDetected = degree
                print("Detecting abnormal distance: expecting %d, sensing object at %d" %(m, reading))
                print("Facing the wall %s" %str(wall))
                abnormalList.append(degree)
                detected = True
            time.sleep(0.05)
            degree = S.getCurrentDegree()
        S.setSensorDPS(0)
        S.resetSonarSensorPos()
        if not detected:
            mov.moveForward(40, True)
    degreeDetected = statistics.mean(abnormalList)
    print("Turning towards object (hopefully) at angle %d, moving distance %d" %(degreeDetected, reading))
    mov.rotateDegree(fixAngle(degreeDetected))
    moveToBottle(reading, degreeDetected)
        
def moveToBottle(reading, degreeRotated):
    mov.setMotorDPS(-200, reading - 30)
    mov.moveForward(-20, True)

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
    distToMove, degToRot = getTravelInfo(mcl, xTarget, yTarget)
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
    if z > 20: 
        return
    x, y, t = mcl.getAverageCoordinate()    
    (m, wall) = mcl.getWall(x, y, t)
    if abs(m - z) > 3:
        mov.moveForward(z-m, False)  

def fixOrientation(theta, mcl, mov):
    _, _, currTheta = mcl.getAverageCoordinate()
    mov.rotateDegree(theta - fixAngle(currTheta))

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
