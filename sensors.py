from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import brickpi333 as brickpi3 # import the BrickPi3 drivers

class Sensors:
    def __init__(self, BP):
        self.BP = BP
        self.sonarSensor = BP.PORT_3
        self.sonarMotor = BP.PORT_A
        self.leftTouch = BP.PORT_4
        self.rightTouch = BP.PORT_2
        self.SENSOR_OFFSET = 10

    def initialise(self):
        """
        Sets the sensor types accordingly
        """
        self.BP.set_sensor_type(self.sonarSensor, BP.SENSOR_TYPE.NXT_ULTRASONIC)
        self.BP.set_sensor_type(self.leftTouch, BP.SENSOR_TYPE.TOUCH)
        self.BP.set_sensor_type(self.rightTouch, BP.SENSOR_TYPE.TOUCH)
	self.BP.set_motor_limits(self.sonarMotor, 70, 200)

    def resetSensorOffsets(self):
        """
        Reset the sonar sensor motor encoder offset
        @throws IOError
        """
        try:
            self.BP.offset_motor_encoder(self.sonarMotor, self.BP.get_motor_encoder(self.sonarMotor))
        except IOError as error:
            print (error)


    def getSensorReading(self):
        """
        Gets the current sensor reading
        """            
        reading = 255
        while True:
            try:
                reading = BP.get_sensor(sonarSensor)
                break
            except brickpi3.SensorError as error:
                pass
        return reading + self.SENSOR_OFFSET

    def rotateSonarSensor(self, degrees):
        """
        Rotates the motor with the sonar sensor
        """
        self.BP.set_motor_position(degrees)

    def resetSonarSensorPos(self):
        pos = BP.get_motor_encoder(sonarMotor)
        while abs(pos) > 1:
            self.BP.set_motor_position(sonarMotor, 0)
            pos = self.BP.get_motor_encoder(sonarMotor)
 
def fixAngle(angle):
    '''
    Corrects the angle such that it is in the [-180,180] range
    @param angle The angle to correct
    @return The corrected angle
    '''
    while (angle > 180):
        angle -= 360
    while (angle < -180):
        angle += 360
    return angle

    
