"""
Robot module helps to consolidate all 4 motors and arduino into one object
so rather than calling multiple functions to get the robot to drive only
one needs to be called on the robot object.
"""
from NanMotor import Motor
from nanpy import ArduinoApi, SerialManager

class Robot(object):
    """Holds all four motors and arduino they are connected to in
    one object for east driving of the robot
    
    Attributes:
        FR: Motor object for front right motor on robot
        BR: Motor object for back right motor on robot
        FL: Motor object for front left motor on robot
        BL: Motor object for back left motor on robot
        a: arduino that motors are connected to
    """
    def __init__(self, FR, BR, FL, BL, a):
        """Creates Robot objects with motors FR, BR, FL, BL and arduino
        a."""
        self.FR = FR
        self.BR = BR
        self.FL = FL
        self.BL = BL
        self.a = a

    def forward(self, speed):
        """Drives the robot forward with the given speed"""
        self.FR.drive(speed, self.a)
        self.BR.drive(speed, self.a)
        self.FL.drive(-speed, self.a)
        self.BL.drive(-speed, self.a)

    def reverse(self, speed):
        """Drives the robot backward with the given speed"""
        self.FR.drive(-speed, self.a)
        self.BR.drive(-speed, self.a)
        self.FL.drive(speed, self.a)
        self.BL.drive(speed, self.a)

    def turn(self, speed):
        """Turns the robot by spinning the motors in the same direction to
        turn similar to how a tank does"""
        self.FR.drive(speed, self.a)
        self.BR.drive(speed, self.a)
        self.FL.drive(speed, self.a)
        self.BL.drive(speed, self.a)

    def stop(self):
        """Stops all motors on the robot"""
        self.FR.drive(0, self.a)
        self.BR.drive(0, self.a)
        self.FL.drive(0, self.a)
        self.BL.drive(0, self.a)

    
