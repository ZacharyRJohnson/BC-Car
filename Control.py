from nanpy import ArduinoApi, SerialManager
from NanMotor import Motor
import sys
import pygame
import time

class Controller(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.r2btn = 0
        self.r2axis = 0
        self.l2btn = 0
        self.l2axis = 0
        self.r1button = 0
        self.l1button = 0
        self.btn1 = 0  # x button
        self.btn2 = 0  # circle button
        self.btn3 = 0  # triangle button
        self.btn4 = 0  # square button
        self.rxaxis = 0
        self.ryaxis = 0
        self.lxaxis = 0
        self.lyaxis = 0

class RobotController(object):
    def __init__(self):
        self.cont = Controller()
        self.joystick = None

    def init_joystick(self):
        pygame.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def loop(self):
        while True:
            self.cont.reset()

            for i in range(0, self.joystick.get_numaxes()):
                val = self.joystick.get_axis(i)


    def close(self):
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

def driveMotors(FR, BR, FL, BL, speed, a):
    FR.drive(speed, a)
    BR.drive(speed, a)
    FL.drive(-speed, a)
    BL.drive(-speed, a)

def arduinoSetup():
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
    
    return a

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
 
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print("Init done")
try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if j.get_button(1):
                    driveMotors(FR, BR, FL, BL, 0, a)
            elif event.type == pygame.JOYAXISMOTION:
                print("Button pressed")
                if j.get_button(6):
                    reverseSpeed = -int(127.5 + (127.5*j.get_axis(3)))
                    print(reverseSpeed)
                    FR.drive(reverseSpeed, a)
                    BR.drive(reverseSpeed, a)
                    FL.drive(-reverseSpeed, a)
                    BL.drive(-reverseSpeed, a)
                    #driveMotors(FR, BR, FL, BL, reverseSpeed, a)
                if j.get_button(7):
                    forwardSpeed = int(127.5 + (127.5*j.get_axis(4)))
                    print(forwardSpeed)
                    driveMotors(FR, BR, FL, BL, forwardSpeed, a)

except Exception as e:
    driveMotors(FR, BR, FL, BL, 0, a)
    print(e)



