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

BP = brickpi3.BrickPi333()
S = Sensors(BP)
mcl = MCL.MCL()
mov = movement.Movement(BP, mcl, S)

from math import pi, atan2, sqrt, atan, sin, cos

def navigate():
    """
    Navigates around the map to find the three bottles and touch them before returning to starting position (if only)
    """
    coordinates = [(100, 70, 75,["d", "e", "f", "g", "h"]),(60, 40, 90, ["c", "d", "e"]),(84,30,-90, ["a", "b", "c"])]
    for x, y, theta, walls in coordinates:
        findBottle(walls)
        navigateToWaypoint(x, y, mcl, mov)
        fixOrientation(theta, mcl, mov)
    correction(S.getSensorReading(), mcl, mov)
    fixOrientation(-180, mcl, mov)
    correction(S.getSensorReading(), mcl, mov)

def findBottle(walls):
    """
    Scans the area for an obstacle in steps of 40cm and 180 area sweepings.
    Once detected, robot moves to touch the obstacle before returning to position when obstacle was detected.
    """
    detected = False
    abnormalList = []
    
    # Look for an obstacle
    while not detected:
        print("============================")
        x, y, theta = mcl.getAverageCoordinate()
        S.rotateSonarSensor(90)
        degree = 90
        S.setSensorDPS(-75)
        
        # Scan immediate surroundings
        while degree > -90:
            reading, degree = S.getSensorDegreeReading()
            (m, wall) = mcl.getWall(x, y, degree + theta)
            if reading < 100 and m - reading > 20 and wall[4] in walls:
                degreeDetected = degree
                print("Detecting abnormal distance: expecting %d, sensing object at %d when facing the wall %s" %(m, reading, str(wall)))
                abnormalList.append(degree)
                detected = True
            time.sleep(0.002)
            degree = S.getCurrentDegree()
            
        S.setSensorDPS(0)
        S.resetSonarSensorPos()
        if not detected:
            mov.moveForward(35, True)
    
    # An obstacle was found
    degreeDetected = statistics.mean(abnormalList)
    print("Turning towards object (hopefully) at angle %d, moving distance %d" %(degreeDetected, reading))
    mov.rotateDegree(fixAngle(degreeDetected))
    mov.touchObstacle(-300)

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

def navigateToWaypoint(xTarget, yTarget, mcl, mov):
    """
    Navigates robot to the provided waypoint
    @param xTarget The x-coordinate of the destination
    @param yTarget The y-coordinate of the destination
    @param mcl The mcl class for localisation
    @param mov The movement class for robot movements
    """
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
    """ 
    Corrects position if ditance from the wall is not as expected
    @param z The sonar sensor reading
    @param mcl The mcl class for localisation
    @param mov The movement class for robot movements
    """
    x, y, t = mcl.getAverageCoordinate()    
    (m, wall) = mcl.getWall(x, y, t)
    if 20 > abs(m - z) > 3:
        mov.moveForward(z-m, False)  

def fixOrientation(theta, mcl, mov):
    """
    Rotates the robot to face the given orientation with respect to positive x-axis
    @param theta The angle to face
    @param mcl THe mcl class for localisatoin
    @param mov THe movement class for robot movements
    """
    _, _, currTheta = mcl.getAverageCoordinate()
    print("Rotating to fix orientation, current angle is %d, rotating %d to get %d" %(currTheta, theta - fixAngle(currTheta), theta))
    mov.rotateDegree(theta - fixAngle(currTheta))

def getTravelInfo(mcl, targetX, targetY):
    """
    Calculates the distance to travel and degree to turn to reach the desired destination
    @param mcl The mcl class for localisation
    @param targetX The x-coordinate of the destination
    @param targetY The y-coordinate of the destination
    """
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
