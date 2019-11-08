def toRads(theta):
    '''
    Converts angle in degrees to radians
    @param theta The angle in degrees
    @return The angle in radians
    '''
    return theta * pi / 180

def getAverageCoordinate():
    xCoord = 0
    yCoord = 0
    theta = 0
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
    for i in range(NUMBER_OF_PARTICLES):
        rand = random.uniform(0, 1)
        for(int i in range(NUMBER_OF_PARTICLES):
            if(cumulativeW[i] > rand):
                # i is the target particle
                newSet.append(copy.deepcopy(particleSet[i]))
                break
    particleSet = newSet
        

