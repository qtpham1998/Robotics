from math import pi
from MCL import updateParticles

def setBP(bp):
    global BP
    BP = bp
    global leftMotor
    leftMotor = BP.PORT_B
    global rightMotor
    rightMotor = BP.PORT_C
    global sonarSensor
    sonarSensor = BP.PORT_3
    
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