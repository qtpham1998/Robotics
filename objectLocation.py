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
    coordinates = [(120, 30,90),(120,30,90)]
    for x, y, start in coordinates:
        #navigateToWaypoint(x, y, mcl, mov)
        findBottle3()
    #navigateToWaypoint(84, 30, mcl, mov)


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
            degree = S.getCurrentDegree() + 2
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
    
    
def findBottle2(start):
    x, y, theta = mcl.getAverageCoordinate()
    rots = 10
    diff = list(range(19))
    max_degree = 0
    max_diff = -1
    while True:
        average_loc = 0
        S.rotateSonarSensor(90)
        S.setSensorDPS(-100)
        nextAngle = start
        diff = -1
        degree = 0
        for i in range(0,19):
            S.rotateSonarSensor(nextAngle)
            reading = S.getSensorReading()
            degree = start - i * 10
            (m, wall) = mcl.getWall(x, y, degree)
            if reading != 255 and (abs(reading - m)) > 25 and reading < m:
                diff = abs(reading - m)
            if diff > max_diff:
                max_degree = degree
                max_diff = diff
            nextAngle -= 10    
        S.setSensorDPS(0)    
        S.resetSonarSensorPos() 
        print("The max index is "+ str(max_degree))
        if max_diff != -1:
            break
        mov.moveForward(40, True)
    mov.rotateDegree(fixAngle(theta - max_degree))    

def findBottle3():
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
        
    """
    x, y, theta = mcl.getAverageCoordinate()
    rots = 10
    diff = list...
    max_degree = 0
    max_diff = -1
    li = []
    while True:
        nextAngle = start
        diff = -1
        degree = 0
        for i in range(0,19):
            S.rotateSonarSensor(nextAngle)
            reading = S.getSensorReading()
            degree = start - i * 10
            (m, wall) = mcl.getWall(x, y, degree)
            if reading != 255 and (abs(reading - m)) > 25 and reading < m:
                diff = abs(reading - m)
            if diff > max_diff:
                max_degree = degree
                max_diff = diff
            if diff >= 20:
                li.append(degree)
                print("seeing " + str(degree))
            nextAngle -= 10    
        S.setSensorDPS(0)    
        S.resetSonarSensorPos() 
        print("The max index is "+ str(max_degree))
        if li:
            break
        mov.moveForward(40, True)
    """

def moveToBottle(reading, degreeRotated):
    #mov.moveForward(reading, True)
    mov.setMotorDPS(-200, reading - 30)
    mov.moveForward(-20, True)
    mov.rotateDegree(90 - degreeRotated)
    mov.moveForward(40, True)

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
