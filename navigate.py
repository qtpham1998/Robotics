import movement
import brickpi333 as brickpi3 
from math import pi, atan2, sqrt, atan, sin, cos

BP = brickpi3.BrickPi333()
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.NXT_ULTRASONIC)
sonarSensor = BP.PORT_4
SENSOR_OFFSET = 12.5

def intervalCoordinates(X, Y, mcl, interval):
    
    xCoordinate, yCoordinate, _ = mcl.getAverageCoordinate()
    xDiff = X - xCoordinate
    yDiff = Y - yCoordinate
    diff = sqrt(xDiff * xDiff + yDiff * yDiff);
    newTheta = atan2(yDiff, xDiff)
    '''
    xSign = -1 if X < xCoordinate else 1
    ySign = -1 if Y < yCoordinate else 1
    '''
    coordinates = []
    
    while(diff >= interval):
        xCoordinate += cos(newTheta) * interval
        yCoordinate += sin(newTheta) * interval
        coordinates.append((xCoordinate, yCoordinate))
        diff -= interval
        
    if(diff > 0):
        coordinates.append((X,Y))
    
    return coordinates
    
    

def navigateToWaypoint(xTarget, yTarget, mcl, mov):
    
    coordinates = intervalCoordinates(xTarget, yTarget, mcl, 20)
    
    print("-----------------------------------------------------")
    previous_reading = 1000
    for (X, Y) in coordinates:
        xCoordinate, yCoordinate, theta = mcl.getAverageCoordinate()
        print("The current (X,Y) coordinates are (%d, %d)" %(xCoordinate,yCoordinate))
        print("Moving to coordinates (%d, %d)" %(X, Y))

        xDiff = X - xCoordinate
        yDiff = Y - yCoordinate
        newTheta = atan2(yDiff, xDiff) * 180 / pi - theta

        '''
        #if (X > xCoordinate and Y < yCoordinate):
         #    newTheta = 90 + newTheta
        if   (X == xCoordinate and Y < yCoordinate):
            newTheta = 270
        elif (X == xCoordinate and Y > yCoordinate):
            newTheta = 90
        elif (X > xCoordinate and Y == yCoordinate):
            newTheta = 0 
        elif (X < xCoordinate and Y == yCoordinate):
            newTheta = 180
        elif (X < xCoordinate and Y < yCoordinate):
            newTheta = 180 + newTheta
        elif (X < xCoordinate and Y > yCoordinate):
            newTheta = 180 - newTheta
        elif(X > xCoordinate and Y < yCoordinate):
            newTheta = 360 - newTheta
        print("The new Theta is %d" %newTheta)
        if (newTheta > theta):
            degree = newTheta - theta
        else:
            degree = 360 - (theta - newTheta)
        '''

        degToRot = fixAngle(newTheta)
        print("The current angle is %d, rotating %d degrees" %(theta, degToRot))
        if abs(degToRot) > 3:                          
            mov.rotateDegree(degToRot)
            
        distToMove = sqrt(xDiff * xDiff + yDiff * yDiff)
        mov.moveLine(distToMove, 20)
        
        reading = 1000;
        while reading > previous_reading:
            try:
                reading = BP.get_sensor(sonarSensor)
                print("The sensor reading is %d" %reading)
            except brickpi3.SensorError as error:
                continue
            
        if reading != 255:
            mcl.localisation(reading)
        
def correction(z, mcl, mov):
    x, y, t = mcl.getAverageCoordinate()    
    (m, wall) = mcl.getWall(x, y, t)
    if abs(m - z) > 5 and z < 250:
        mov.moveForward(z-m)
    
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
        
