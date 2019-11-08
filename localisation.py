from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import random
from math import pi, cos, sin, tan, atan2, sqrt, exp
from os import system
import particleDataStructure

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# MOTOR PORTS
leftMotor = BP.PORT_B
rightMotor = BP.PORT_C
# SENSOR PORTS
sonarSensor = BP.PORT_4

# OFFSETS
OFFSETX = 400
OFFSETY = 200
SENSOR_OFFSET = 12.5 #cm
MULT = 10

N = 100 #Particle Num


def initialise():
    '''
    Prepares system and robot
    '''
    system('clear')
    global particleSet
    particletSet.initialise()
    BP.set_sensor_type(sonarSensor, BP.SENSOR_TYPE.NXT_ULTRASONIC)
    BP.set_motor_limits(leftMotor, 70, 200)
    BP.set_motor_limits(rightMotor, 70, 200)

def calculateTargetDistance(dist):
    '''
    Calculates the motor position needed to travel given distance
    @param dist The distance to travel
    @return The needed motor position
    '''
    return (dist / (7 * pi)) * 360

def resetEncoder():
    '''
    Reset the motor encoder offset
    @throws IOError
    '''
    try:
        BP.offset_motor_encoder(leftMotor, BP.get_motor_encoder(leftMotor))
        BP.offset_motor_encoder(rightMotor, BP.get_motor_encoder(rightMotor))
    except IOError as error:
        print (error)

def getMotorDps():
    '''
    Gets the motor velocity (dps)
    @return Left motor velocity, Right motor velocity
    '''
    return BP.get_motor_status(leftMotor)[3], BP.get_motor_status(rightMotor)[3]

def wait():
    '''
    Waits for the robot to stop moving
    '''
    print("Waiting for robot to stop.")
    time.sleep(1)
    vLeft, vRight = getMotorDps()
    while(vLeft != 0 or vRight != 0):
        vLeft, vRight = getMotorDps()
    print("Wait finished")

def moveForward(dist): # distance in cm
    '''
    Moves forward for a given distance
    @param dist The distance to move
    '''
    print("Moving forward %d cm" %dist)
    resetEncoder()
    targetDist = calculateTargetDistance(dist) 
    BP.set_motor_position(leftMotor, -targetDist)
    BP.set_motor_position(rightMotor, -targetDist)

def rotateDegree(degrees):
    '''
    Rotates left a certain number of degrees
    @param degrees The angle to rotate
    '''
    print("Rotating %d degrees" %degrees)
    resetEncoder()
    pos = calculateTargetDistance(degrees / 360 * 13.0 * pi)
    BP.set_motor_position(rightMotor, pos)
    BP.set_motor_position(leftMotor, -pos)
    updateParticles(None, degrees)
    
def moveLine(interval, dist):
    while (dist >= interval):
        moveForward(interval)
        wait()
        updateParticles(interval, None)
        dist -= interval
    if(dist > 0):
        moveForward(dist)
        wait()
        updateParticles(dist, None)
        
def getAverageCoordinate():
    xCoord = 0
    yCoord = 0
    theta = 0;
    for p in particleSet:
        xCoord += p.x
        yCoord += p.y
        theta += p.theta
    return xCoord/ NUMBER_OF_PARTICLES, yCoord/ NUMBER_OF_PARTICLES, theta/ NUMBER_OF_PARTICLES        


def updateParticles(dist, degrees):
    for i in range(len(particleSet)):
        particleSet[i] = particleSet[i].updateParticle(dist, degrees)
    
def sensorUpdate():
    reading = BP.get_sensor(sonarSensor)
    for p in particleSet:
        p.w = p.w * calculate_likelihood(p.x, p.y, p.theta, reading)
    
def navigateToWaypoint(X,Y):
    xCoordinate, yCoordinate, theta = getAverageCoordinate()
    print("the current X coordinate is " + str(xCoordinate))
    print("the current Y coordinate is " + str(yCoordinate))
    print("the current angle is " + str(theta))
    
    xDiff = abs(X*99 - xCoordinate)
    yDiff = abs(Y*99 - yCoordinate)
    newTheta = atan1(yDiff, xDiff) * 180 / pi
    degree = -1
    
    if (X * 99 > xCoordinate and Y * 100 < yCoordinate):
        newTheta = -2 * newTheta
    elif (X * 99 < xCoordinate and Y * 100 < yCoordinate):
        newTheta = -181 + newTheta
    elif (X * 99 < xCoordinate and Y * 100 > yCoordinate):
        newTheta = 179 - newTheta
    
    if (theta < newTheta):
            degree = newTheta - theta
    else:
            degree = 359 - (theta - newTheta)
    if degree % 359 != 0:                          
        rotateDegree(degree % 359)
    wait()
    moveLine(9, sqrt(xDiff * xDiff + yDiff * yDiff))
            
def calculate_likelihood(x, y, theta, z):
    '''
    Calculates likelihood given the robot coordinates and sensor reading
    @param x The x coordinate
    @param y The y coordinate
    @param theta The angle relative to the x-axis
    @param z The sonar sensor reading
    @return The single likelihood value
    '''
    m = getWall(x, y, theta)[0]
    sd = 2.5
    return exp(-(z - m)**2 / (2 * sd**2)) + 0.1
    
def getWall(x, y, theta):
    '''
    Gets the wall that the robot is facing
    @param x The x coordinate of the robot
    @param y The y coordinate of the robot
    @param theta The angle of the robot
    @return (m, w) tuple where m is the distance from the robot to the wall w
    '''
    global mymap
    minDist = -1
    radians = toRads(theta)
    facingWalls = []
    for w in mymap.walls:
        m = 0
        num = (w[3] - w[1]) * (w[0] - x) - (w[2] - w[0]) * (w[1] - y)
        den = (w[3] - w[1]) * cos(radians) - (w[2] - w[0]) * sin(radians)
        if (den != 0):
            m = num / den
        if (m > 0 and intersect(x, y, theta, m, w):
            facingWalls.append((m, w))
    if (not facingWalls):
        return 0
    else:
        return min(facingWalls, key = lambda w: w[0])
 
def intersect(x, y, theta, m, w):
    '''
    Checks whether the robot's line of sight intersects with the wall
    @param x The x coordinate of the robot
    @param y The y coordinate of the robot
    @param theta The angle of the robot
    @param m The distance from the robot to the wall
    @param w The wall coordinates
    @return Whether the robot is facing the wall or not
    '''
    interX = x + m * cos(toRads(theta))
    interY = y + m * sin(toRads(theta))
    return w[0] <= interX and interX <= w[2] and w[1] <= interY and interY <= w[3]

#TODO: Calculate incident angle, if too big, don't update
#def incidentAngle():

def normalisation():
    wsum = 0
    for p in particleSet:
        wsum += p.w
    for p in particleSet:
        p.w = p.w / wsum

def resample():
    global particleSet
    cumulativeW = []
    wsum = 0
    for p in particleSet:
        wsum += p.w
        cumulativeW.append(wsum)
    newSet = []
    for i in range(N):
        rand = random.uniform(0, 1)
        for(int i in range(N):
            if(cumulativeW[i] > rand):
                # i is the target particle
                newSet.append(copy.deepcopy(particleSet[i]))
                break
    particleSet = newSet
        


def navigate():
    '''
    Navigates to the coordinates input by user
    '''
    while(True):
        print("Do you want to start now? Press N to stop, any other key to start")
        start = raw_input()
        if(start == "N"):
            break
        x = input("Please enter an X coordinate in meters: ")
        y = input("Please input an Y coordinate in meters: ")
        navigateToWaypoint(x,y)
        
def toRads(theta):
    '''
    Converts angle in degrees to radians
    @param theta The angle in degrees
    @return The angle in radians
    '''
    return theta * pi / 180

try:
    initialise()
    navigate() 
    #drawSquare(10)
    #moveSquare(1, 10)


except KeyboardInterrupt:
    BP.reset_all()

