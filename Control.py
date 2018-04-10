from nanpy import ArduinoApi, SerialManager
from NanMotor import Motor
from robot import Robot
import sys
import pygame
import time

class Controller(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.btn0 = 0 # Square
        self.btn1 = 0 # X
        self.btn2 = 0 # Circle
        self.btn3 = 0 # Triangle
        self.btn4 = 0 # L1
        self.btn5 = 0 # R1
        self.btn6 = 0 # L2
        self.btn7 = 0 # R2
        self.btn8 = 0 # Share
        self.axis0 = 0 # Left analog x axis
        self.axis1 = 0 # Left analog y axis
        self.axis2 = 0 # Right analog x axis
        self.axis3 = -1.0 # L2 axis
        self.axis4 = -1.0 # R2 axis
        self.axis5 = 0 # Right analog y axis

class RobotController(object):
    def __init__(self, robo):
        self.cont = Controller()
        self.joystick = None
        self.robot = robo

    def init_joystick(self):
        pygame.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def loop(self):
        r2Pressed = 0
        l2Pressed = 0
        rAnalogMoved = 0
        while True:
            self.cont.reset()
            pygame.event.pump()

            for i in range(6):
                val = self.joystick.get_axis(i)
                if i in range(6) and val != 0:
                    tmp = "self.cont.axis" + str(i) + " = " + str(val)
                    exec(tmp)

            for i in range(9):
                if self.joystick.get_button(i) != 0:
                    tmp = "self.cont.btn" + str(i) + " = 1"
                    exec(tmp)

            if self.cont.btn8:
                break

            if self.cont.btn0:
                self.robot.stop()
            
            if self.cont.axis2 != 0:
                speed = -int(255*self.cont.axis2)
                self.robot.turn(speed)
                rAnalogMoved = 1

            if self.cont.axis2 == 0 and rAnalogMoved:
                self.robot.stop()
                rAnalogMoved = 0

            if self.cont.btn7:
                speed = int(127.5 + (127.5*self.cont.axis4))
                r2Pressed = 1
                self.robot.forward(speed) 
            
            if self.cont.btn7 == 0 and r2Pressed:
                self.robot.stop()
                r2Pressed = 0

            if self.cont.btn6:
                speed = int(127.5 + (127.5*self.cont.axis3))
                l2Pressed = 1
                self.robot.reverse(speed)

            if self.cont.btn6 == 0 and l2Pressed:
                self.robot.stop()
                l2Pressed = 0

    def close(self):
        self.robot.stop()
        if self.joystick:
            self.joystick.quit()

AI1 = 2
AI2 = 10
APWM = 3

BI1 = 4
BI2 = 5
BPWM = 6

CI1 = 8
CI2 = 7
CPWM = 9

DI1 = 12
DI2 = 13
DPWM = 11

STDBY1 = 0
STDBY2 = 1

def robotSetup():
    try:
        connection = SerialManager()
        a = ArduinoApi(connection = connection)
    except:
        print("Failed to connect to Arduino")
        sys.exit()

    a.pinMode(STDBY1, a.OUTPUT)
    a.pinMode(STDBY2, a.OUTPUT)

    FR = Motor(AI1, AI2, APWM)
    FR.setupMotor(a)

    BR = Motor(BI1, BI2, BPWM)
    BR.setupMotor(a)

    FL = Motor(CI1, CI2, CPWM)
    FL.setupMotor(a)

    BL = Motor(DI1, DI2, DPWM)
    BL.setupMotor(a)

    a.digitalWrite(STDBY1, a.HIGH)
    a.digitalWrite(STDBY2, a.HIGH)
    
    robot = Robot(FR, BR, FL, BL, a)

    return robot

'''
try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")
    sys.exit()

a.pinMode(STDBY1, a.OUTPUT)
a.pinMode(STDBY2, a.OUTPUT)

FR = Motor(AI1, AI2, APWM)
FR.setupMotor(a)

BR = Motor(BI1, BI2, BPWM)
BR.setupMotor(a)

FL = Motor(CI1, CI2, CPWM)
FL.setupMotor(a)

BL = Motor(DI1, DI2, DPWM)
BL.setupMotor(a)

a.digitalWrite(STDBY1, a.HIGH)
a.digitalWrite(STDBY2, a.HIGH)
'''
robot = robotSetup()
rc = RobotController(robot)
rc.init_joystick()
print("Init done")
try:
    while True:
        try:
            rc.loop()
        finally:
            rc.close()

except Exception as e:
    rc.close()
    print(e)



