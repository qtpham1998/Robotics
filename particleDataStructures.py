#!/usr/bin/env python 

# Some suitable functions and data structures for drawing a map and particles

import time
import random
from math import cos, sin, pi

# Constants
NUMBER_OF_PARTICLES = 100

# Functions to generate some dummy particles data:
def calcX():
    return random.gauss(80,3) + 70*(math.sin(t)); # in cm

def calcY():
    return random.gauss(70,3) + 60*(math.sin(2*t)); # in cm

def calcW():
    return random.random()

def calcTheta():
    return random.randint(0,360)

# A Canvas class for drawing a map and particles:
#     - it takes care of a proper scaling and coordinate transformation between
#      the map frame of reference (in cm) and the display (in pixels)
class Canvas:
    def __init__(self,map_size=210):
        self.map_size    = map_size;    # in cm;
        self.canvas_size = 768;         # in pixels;
        self.margin      = 0.05*map_size
        self.scale       = self.canvas_size/(map_size+2*self.margin)

    def drawLine(self,line):
        x1 = self.__screenX(line[0])
        y1 = self.__screenY(line[1])
        x2 = self.__screenX(line[2])
        y2 = self.__screenY(line[3])
        print ("drawLine:" + str((x1,y1,x2,y2)))

    def drawParticles(self,data):
        display = [(self.__screenX(d[0]),self.__screenY(d[1])) + d[2:] for d in data]
        print ("drawParticles:" + str(display))

    def __screenX(self,x):
        return (x + self.margin)*self.scale

    def __screenY(self,y):
        return (self.map_size + self.margin - y)*self.scale

# A Map class containing walls
class Map:
    def __init__(self):
        self.walls = []

    def add_wall(self,wall):
        self.walls.append(wall)

    def clear(self):
        self.walls = []

    def draw(self):
        for wall in self.walls:
            canvas.drawLine(wall)

# Simple Particles set
class Particles:
    def __init__(self):
        self.n = NUMBER_OF_PARTICLES
        self.data = []
        pos1 = 168/420
        pos2 = 210/420 + pos1
        pos3 = 1
        for i in range(self.n):
            self.data.append(Particle(84, 30, 0))


    def draw(self):
        canvas.drawParticles(self.data)

# A Particle
class Particle:
    def __init__(self, x, y, theta, w=1/NUMBER_OF_PARTICLES):
        self.x = x
        self.y = y
        self.theta = theta
        self.w = w

    def calcX(self, dist):
        return self.x + (dist + random.gauss(0, 0.5)) * cos(self.theta / 180 * pi)
 
    def calcY(self, dist):
        return self.y + (dist + random.gauss(0, 0.5)) * sin(self.theta / 180 * pi)

    def calcTheta(self, degrees):
        return self.theta + (degrees + random.gauss(0, 0.1)) 
    
    def updateParticleCoords(self, dist):
        return updateParticle(self, dist, 0)
    
    def updateParticleAngle(self, degrees):
        return updateParticle(self, None, degrees)

    def updateParticle(self, dist, degrees):
        x = self.x
        y = self.y
        theta = self.calcTheta(degrees)
        #theta = theta + 360 if theta < 0 else theta
        #theta = theta - 360 if theta > 360 else theta
        if(dist != None):
            x = self.calcX(dist)
            y = self.calcY(dist)
        return Particle(x, y, theta)
        
    def getCoords(self):
        return (self.x, self.y, self.theta, self.w)
        
canvas = Canvas();    # global canvas we are going to draw on

mymap = Map()
# Definitions of walls
# a: O to A
# b: A to B
# c: C to D
# d: D to E
# e: E to F
# f: F to G
# g: G to H
# h: H to O
mymap.add_wall((0,0,0,168));        # a
mymap.add_wall((0,168,84,168));     # b
mymap.add_wall((84,126,84,210));    # c
mymap.add_wall((84,210,168,210));   # d
mymap.add_wall((168,210,168,84));   # e
mymap.add_wall((168,84,210,84));    # f
mymap.add_wall((210,84,210,0));     # g
mymap.add_wall((210,0,0,0));        # h
mymap.draw()

particleSet = Particles()
