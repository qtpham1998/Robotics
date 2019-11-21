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
from math import pi, atan2, sqrt, atan, sin, cos


BP = brickpi3.BrickPi333() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

mcl = MCL.MCL()
mov = movement.Movement(BP, mcl)

def scanAndNavigate():


def intervalCoordinates(xTarget, yTarget, mcl, interval):
    xCoord, yCoord, _ = mcl.getAverageCoordinate()
    xDiff = abs(xCoord - xTarget)
    yDiff = abs(yCoord - yTarget)
    theta = atan2(yDiff, xDiff)
    distance = sqrt(xDiff * xDiff + yDiff * yDiff)
    
    coordinates = []
    
    xSign = 1
    ySign = 1
    
    if(xTarget < xCoord):
        xSign = -1
    if(yTarget < yCoord):
        ySign = -1
    
    while(distance >= interval):
        xCoord += xSign * cos(theta) * interval
        yCoord += ySign * sin(theta) * interval
        coordinates.append((xCoord, yCoord))
        distance -= interval
        
    if(distance > 0):
        coordinates.append((xTarget,yTarget))
    
    return coordinates
    
    
def navigateToWaypoint(xTarget, yTarget, mcl, mov):
    print("-----------------------------------------------------")
    coordinates = intervalCoordinates(xTarget, yTarget, mcl, 20)
    for (X,Y) in coordinates:
        distToMove, degToRot = getTravelInfo(mcl, X, Y)
        if abs(degToRot) > 3:                          
            mov.rotateDegree(degToRot)
        mov.moveForward(distToMove, True)
        reading = getSensorReading()
        if reading < 255: 
            mcl.localisation(reading)
    reading = getSensorReading()        
    if reading < 255: 
        correction(reading, mcl, mov)
        reading = getSensorReading()
        if reading < 255:
            mcl.localisation(reading)   
        
def getTravelInfo(mcl, targetX, targetY):
    xCoordinate, yCoordinate, theta = mcl.getAverageCoordinate()
    print("The current (X,Y) coordinates are (%d, %d). Moving to (%d, %d)" %(xCoordinate,yCoordinate,targetX,targetY))
    xDiff = targetX - xCoordinate
    yDiff = targetY - yCoordinate
    deg = fixAngle(atan2(yDiff, xDiff) * 180 / pi - theta)
    print("The current angle is %d, rotating %d degrees" %(theta, deg))
    distToTravel = sqrt(xDiff * xDiff + yDiff * yDiff)
    return distToTravel, deg
 
def correction(z, mcl, mov):
    x, y, t = mcl.getAverageCoordinate()    
    (m, wall) = mcl.getWall(x, y, t)
    if abs(m - z) > 3 and z < 250:
        mov.moveForward(z-m, False)              
    
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

try:
    
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all() 
    
