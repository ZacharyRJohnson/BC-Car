from NanMotor import Motor
from nanpy import ArduinoApi, SerialManager

class Robot(object):
    def __init__(self, FR, BR, FL, BL, a):
        self.FR = FR
        self.BR = BR
        self.FL = FL
        self.BL = BL
        self.a = a

    def forward(self, speed):
        self.FR.drive(speed, self.a)
        self.BR.drive(speed, self.a)
        self.FL.drive(-speed, self.a)
        self.BL.drive(-speed, self.a)

    def reverse(self, speed):
        self.FR.drive(-speed, self.a)
        self.BR.drive(-speed, self.a)
        self.FL.drive(speed, self.a)
        self.BL.drive(speed, self.a)

    def turn(self, speed):
        self.FR.drive(speed, self.a)
        self.BR.drive(speed, self.a)
        self.FL.drive(speed, self.a)
        self.BL.drive(speed, self.a)

    def stop(self):
        self.FR.drive(0, self.a)
        self.BR.drive(0, self.a)
        self.FL.drive(0, self.a)
        self.BL.drive(0, self.a)

    
