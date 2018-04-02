from nanpy import (ArduinoApi, SerialManager)
import math

class Motor(object):
    """A motor hooked up to a sparkfun TB6612FNG dual motor driver
    uses nanpy so a raspberrypi or other computer can control the motor
    through an arduino and do the logic elsewhere. Motors have the following
    properties:

    Attributes:
        m1: pin on the arduino connected to an input1 on the driver
        m2: pin on the arduino connected to an input2 on the driver
        pwm: pwm pin on the arduino connected to a pwm pin on the driver. 
            Controls the speed of the motor
    """

    def __init__(self, i1, i2,  pwm):
        """Return a motor object with pin numbers i1, i2, and pwm for the
        corresponding object attributes."""
        self.in1 = i1
        self.in2 = i2
        self.pwm = pwm
    
    def setupMotor(self, a):
        a.pinMode(self.in1, a.OUTPUT)
        a.pinMode(self.in2, a.OUTPUT)
        a.pinMode(self.pwm, a.OUTPUT)


    def drive(self, speed, a):
        """Drive the motor connected to arduino 'a' with the given speed,
        if speed is positive the motor will spin CW, if it is negative it 
        will spin CCW, and if it is zero the motor will stop spinning."""
        if speed > 0:
            a.digitalWrite(self.in1, a.HIGH)
            a.digitalWrite(self.in2, a.LOW)
            a.analogWrite(self.pwm, speed)
        elif speed < 0:
            a.digitalWrite(self.in1, a.LOW)
            a.digitalWrite(self.in2, a.HIGH)
            a.analogWrite(self.pwm, abs(speed)) 
        else:
            a.digitalWrite(self.in1, a.LOW)
            a.digitalWrite(self.in2, a.LOW)
            a.analogWrite(self.pwm, 0)

