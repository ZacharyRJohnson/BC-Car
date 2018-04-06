from nanpy import ArduinoApi, SerialManager
from NanMotor import Motor
import sys

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

try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")
    sys.exit()

#Setup
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
try:
    while True:
        speed = input("Input speed: ")
        if speed == "exit":
            break
        FR.drive(int(speed), a)
        BR.drive(int(speed), a)
        FL.drive(-int(speed), a)
        BL.drive(-int(speed), a)
except Exception as e:
    print(e)

FR.drive(0, a)
BR.drive(0, a)
FL.drive(0, a)
BL.drive(0, a)

