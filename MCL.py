import particleDataStructures
import random
from math import pi, cos, sin, tan, atan2, sqrt, exp
import copy 
import time

NUMBER_OF_PARTICLES = 100
class MCL:
    def __init__(self):
        self.particles = particleDataStructures.Particles()
        self.particleSet = self.particles.data
        self.mymap = particleDataStructures.mymap

    def MCL(self, reading):
        self.sensorUpdate(reading)
        self.normalisation()
        self.resample()
        return self.particleSet
    
    def localisation(self,reading):
        self.particleSet = self.MCL(reading)
        draw = []
        for p in self.particleSet:
            draw.append((p.x, p.y, p.theta, p.w))
        particleDataStructures.canvas.drawParticles(draw)
        time.sleep(0.2)

    def toRads(self, theta):
        '''
        Converts angle in degrees to radians
        @param theta The angle in degrees
        @return The angle in radians
        '''
        return theta * pi / 180

    def getAverageCoordinate(self):
        xCoord = 0
        yCoord = 0
        theta = 0
        for p in self.particleSet:
            xCoord += p.x * p.w
            yCoord += p.y * p.w
            theta += p.theta * p.w
        return xCoord, yCoord, theta     


    def updateParticles(self, dist, degrees):
        for i in range(NUMBER_OF_PARTICLES):
            self.particleSet[i] = self.particleSet[i].updateParticle(dist, degrees)
    
    def sensorUpdate(self, reading):
        for p in self.particleSet:
            p.w = p.w * self.calculate_likelihood(p.x, p.y, p.theta, reading)

    def calculate_likelihood(self, x, y, theta, z):
        '''
        Calculates likelihood given the robot coordinates and sensor reading
        @param x The x coordinate
        @param y The y coordinate
        @param theta The angle relative to the x-axis
        @param z The sonar sensor reading
        @return The single likelihood value
        '''
        m = self.getWall(x, y, theta)
        if m != None:
            sd = 2.5
            res = exp((-(z - m[0])**2) / (2 * sd**2)) + 0.1
            #print("likelihood: " + str(res))
            return res
        else:
            #print("Not facing wall")
            return 1
    
    def getWall(self, x, y, theta):
        '''
        Gets the wall that the robot is facing
        @param x The x coordinate of the robot
        @param y The y coordinate of the robot
        @param theta The angle of the robot
        @return (m, w) tuple where m is the distance from the robot to the wall w
        '''
        minDist = -1
        radians = self.toRads(theta)
        facingWalls = []
        for w in self.mymap.walls:
            m = 0.0
            num = (w[3] - w[1]) * (w[0] - x) - (w[2] - w[0]) * (w[1] - y)
            den = (w[3] - w[1]) * cos(radians) - (w[2] - w[0]) * sin(radians)
            if (den != 0):
                m = num / den
            #print(m)
            if (m != 0 and self.intersect(x, y, theta, m, w)):
                facingWalls.append((m, w))
            #print(facingWalls)
            if (not facingWalls):
                return None 
            else:
                #print("looking at wall : " + str(min(facingWalls, key = lambda w: w[0])))
                return min(facingWalls, key = lambda w: w[0])
    
    def intersect(self, x, y, theta, m, w):
        '''
        Checks whether the robot's line of sight intersects with the wall
        @param x The x coordinate of the robot
        @param y The y coordinate of the robot
        @param theta The angle of the robot
        @param m The distance from the robot to the wall
        @param w The wall coordinates
        @return Whether the robot is facing the wall or not
        '''
        interX = x + m * cos(self.toRads(theta))
        interY = y + m * sin(self.toRads(theta))
        #print(w[0] <= interX and interX <= w[2] and w[1] <= interY and interY <= w[3])
        return w[0] <= interX and interX <= w[2] and w[1] <= interY and interY <= w[3]

    #TODO: Calculate incident angle, if too big, don't update
    #def incidentAngle():

    def normalisation(self):
        wsum = 0
        for p in self.particleSet:
            wsum += p.w
        for p in self.particleSet:
            p.w = p.w / wsum

    def resample(self):
        cumulativeW = []
        wsum = 0
        for p in self.particleSet:
            wsum += p.w
            cumulativeW.append(wsum)
        newSet = []
        for i in range(NUMBER_OF_PARTICLES):
            rand = random.uniform(0, 1)
            for i in range(NUMBER_OF_PARTICLES):
                if(cumulativeW[i] > rand):
                    # i is the target particle
                    newSet.append(copy.deepcopy(self.particleSet[i]))
                    break
        self.particleSet = newSet
        

