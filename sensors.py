from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import brickpi333 as brickpi3 # import the BrickPi3 drivers
import time

class Sensors:
    def __init__(self, BP):
        self.BP = BP
        self.sonarSensor = BP.PORT_4
        self.sonarMotor = BP.PORT_A
        self.leftTouch = BP.PORT_2
        self.rightTouch = BP.PORT_1
        self.SENSOR_OFFSET = 10
        self.initialise()

    def initialise(self):
        """
        Sets the sensor types accordingly
        """
        self.BP.set_sensor_type(self.sonarSensor, self.BP.SENSOR_TYPE.NXT_ULTRASONIC)
        self.BP.set_sensor_type(self.leftTouch, self.BP.SENSOR_TYPE.TOUCH)
        self.BP.set_sensor_type(self.rightTouch, self.BP.SENSOR_TYPE.TOUCH)
        self.BP.set_motor_limits(self.sonarMotor, 70, 200)
        self.resetSensorOffset()
    
    def setSensorDPS(self,dps):
        self.BP.set_motor_dps(self.sonarMotor,dps)

    def resetSensorOffset(self):
        """
        Reset the sonar sensor motor encoder offset
        @throws IOError
        """
        try:
            self.BP.offset_motor_encoder(self.sonarMotor, self.BP.get_motor_encoder(self.sonarMotor))
        except IOError as error:
            print (error)

    
    def getTouchSensorReading(self):
        return self.BP.get_sensor(self.leftTouch), self.BP.get_sensor(self.rightTouch)


    def getSensorReading(self):
        """
        Gets the current sensor reading
        """            
        reading = 255
        while True:
            try:
                reading = self.BP.get_sensor(self.sonarSensor)
                break
            except brickpi3.SensorError as error:
                pass
        return reading + self.SENSOR_OFFSET

    def getSensorDegreeReading(self):
        return self.getSensorReading(), self.getCurrentDegree()

    def rotateSonarSensor(self, degrees):
        """
        Rotates the motor with the sonar sensor
        """
        self.BP.set_motor_position(self.sonarMotor, degrees)
        self.waitSonar()
        
    def getCurrentDegree(self):
        return self.BP.get_motor_encoder(self.sonarMotor)

    def resetSonarSensorPos(self):
        self.BP.set_motor_position(self.sonarMotor, 0)
        self.waitSonar()
            
    def waitSonar(self):
        '''
        Waits for the sensor to stop moving
        '''
        time.sleep(0.05)
        vMotor = self.BP.get_motor_status(self.sonarMotor)[3]
        while(vMotor != 0):
            vMotor = self.BP.get_motor_status(self.sonarMotor)[3]

    
