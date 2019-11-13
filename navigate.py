import movement
from math import pi, atan2, sqrt, atan, sin, cos

def intervalCoordinates(X,Y, mcl, interval):
    
    xCoordinate, yCoordinate, _ = mcl.getAverageCoordinate()
    xDiff = abs(X - xCoordinate)
    yDiff = abs(Y - yCoordinate)
    diff = sqrt(xDiff * xDiff + yDiff * yDiff);
    newTheta = atan2(yDiff, xDiff)
    
    xSign = -1 if X < xCoordinate else 1
    ySign = -1 if Y < yCoordinate else 1
    
    coordinates = []
    
    while(diff >= interval):
        xCoordinate += xSign * cos(newTheta) * interval
        yCoordinate += ySign * sin(newTheta) * interval
        coordinates.append((xCoordinate, yCoordinate))
        diff -= interval
        
    if(diff > 0):
        coordinates.append((X,Y))
    
    return coordinates
    
    

def navigateToWaypoint(X,Y, mcl, mov, interval):
    
    coordinates = intervalCoordinates(X, Y, mcl, interval)
    
    for coord in coordinates:
        
        X = coord[0]
        Y = coord[1]
    
        xCoordinate, yCoordinate, theta = mcl.getAverageCoordinate()
        print("The current X coordinate is %d" %xCoordinate)
        print("The current Y coordinate is %d" %yCoordinate)
        print("The current angle is %d" %theta)

        xDiff = abs(X - xCoordinate)
        yDiff = abs(Y - yCoordinate)
        newTheta = atan2(yDiff, xDiff) * 180 / pi


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

        degToRot = fixAngle(degree)
        if not abs(degToRot) < 3 and not abs(degToRot - 360) < 3:                          
            mov.rotateDegree(degToRot)
        mov.wait()
        distToMove = sqrt(xDiff * xDiff + yDiff * yDiff)
        print("The distance to move is %.2f" %distToMove)
        mov.moveForward(distToMove)
        
    
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
        
