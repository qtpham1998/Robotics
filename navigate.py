import brickpi333 as brickpi3
from math import pi, atan2, sqrt, sin, cos

BP = brickpi3.BrickPi333()
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.NXT_ULTRASONIC)
sonarSensor = BP.PORT_4

def getIntervalCoordinates(X, Y, mcl, interval):
    xCoordinate, yCoordinate, _ = mcl.getAverageCoordinate()
    diff, newTheta = getTravelInfo(mcl, X, Y, False)
    coordinates = []
    
    while diff >= interval:
        xCoordinate += cos(newTheta) * interval
        yCoordinate += sin(newTheta) * interval
        coordinates.append((xCoordinate, yCoordinate))
        diff -= interval       
    if diff > 0:
        coordinates.append((X,Y))
    
    return coordinates
    
def navigateToWaypoint(xTarget, yTarget, mcl, mov):
    xCoordinate, yCoordinate, theta = mcl.getAverageCoordinate()
    print("The current (X,Y) coordinates are (%d, %d)" % (xCoordinate, yCoordinate))
    print("Moving to coordinates (%d, %d)" %(xTarget, yTarget))

    distToMove, degToRot = getTravelInfo(mcl, xTarget, yTarget, True)
    print("The current angle is %d, rotating %d degrees" %(theta, degToRot))
    
    if abs(degToRot) > 3:
        mov.rotateDegree(degToRot)
    mov.moveLine(distToMove, 20)
        
        
def getTravelInfo(mcl, targetX, targetY, toTurn):
    xCoordinate, yCoordinate, theta = mcl.getAverageCoordinate()
    xDiff = targetX - xCoordinate
    yDiff = targetY - yCoordinate
    deg = atan2(yDiff, xDiff) #In radians
    if toTurn:
        deg = fixAngle(deg * 180 / pi - theta)
    distToTravel = sqrt(xDiff * xDiff + yDiff * yDiff)
    return distToTravel, deg

def fixAngle(angle):
    """
    Correct the angle such that it is in the [-180,180] range
    @param angle The angle to correct
    @return The corrected angle
    """
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle
        
