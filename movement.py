from math import pi
import time
import MCL

class Movement:

    def __init__(self, bp, mcl):
        self.BP = bp
        self.leftMotor = bp.PORT_B
        self.rightMotor = bp.PORT_C
        self.sonarSensor = bp.PORT_3
        self.MCL = mcl
    
    def calculateTargetDistance(self, dist):
        '''
        Calculates the motor position needed to travel given distance
        @param dist The distance to travel
        @return The needed motor position
        '''
        return (dist / (7 * pi)) * 360

    def resetEncoder(self):
        '''
        Reset the motor encoder offset
        @throws IOError
        '''
        try:
            self.BP.offset_motor_encoder(self.leftMotor, self.BP.get_motor_encoder(self.leftMotor))
            self.BP.offset_motor_encoder(self.rightMotor, self.BP.get_motor_encoder(self.rightMotor))
        except IOError as error:
            print (error)


    def getMotorDps(self):
        '''
        Gets the motor velocity (dps)
        @return Left motor velocity, Right motor velocity
        '''
        return self.BP.get_motor_status(self.leftMotor)[3], self.BP.get_motor_status(self.rightMotor)[3]

    def wait(self):
        '''
        Waits for the robot to stop moving
        '''
        #print("Waiting for robot to stop.")
        time.sleep(1)
        vLeft, vRight = self.getMotorDps()
        while(vLeft != 0 or vRight != 0):
            vLeft, vRight = self.getMotorDps()
        #print("Wait finished")

    def moveForward(self, dist): #distance in cm
        '''
        Moves forward for a given distance
        @param dist The distance to move
        '''
        self.resetEncoder()
        targetDist = self.calculateTargetDistance(dist) 
        self.BP.set_motor_position(self.leftMotor, -targetDist)
        self.BP.set_motor_position(self.rightMotor, -targetDist)
        self.wait()
        self.MCL.updateParticles(dist, 0)


    def rotateDegree(self, degrees):
        '''
        Rotates left a certain number of degrees
        @param degrees The angle to rotate
        '''
        self.resetEncoder()
        pos = self.calculateTargetDistance(degrees / 360 * 13.0 * pi)
        self.BP.set_motor_position(self.rightMotor, pos)
        self.BP.set_motor_position(self.leftMotor, -pos)
        self.wait()
        self.MCL.updateParticles(0, degrees)

    def moveLine(self, interval, dist):
        '''
        Moves 'dist' metres in intervals of 'interval'
        @param interval Distance to move at a time
        @param dist Total distance to move
        '''
        print("Moving forward %d cm" %dist)
        while (dist >= interval):
            self.moveForward(interval)
            dist -= interval
        if (dist > 0):
            self.moveForward(dist)
