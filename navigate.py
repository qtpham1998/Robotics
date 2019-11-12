import movement
from math import pi, atan2, sqrt 
def navigateToWaypoint(X,Y, mcl, mov):
    xCoordinate, yCoordinate, theta = mcl.getAverageCoordinate()
    print("the current X coordinate is " + str(xCoordinate))
    print("the current Y coordinate is " + str(yCoordinate))
    print("the current angle is " + str(theta))
    
    xDiff = abs(X*99 - xCoordinate)
    yDiff = abs(Y*99 - yCoordinate)
    newTheta = atan2(yDiff, xDiff) * 180 / pi
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
        mov.rotateDegree(degree % 359)
    mov.wait()
    mov.moveLine(10, sqrt(xDiff * xDiff + yDiff * yDiff))
        
