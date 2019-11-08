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
            