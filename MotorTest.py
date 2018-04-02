from NanMotor import Motor
from nanpy import (ArduinoApi, SerialManager)

AI1 = 7
AI2 = 8
PWM = 9
stdby = 10

try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("Failed to connect to Arduino")

#Setup
#a.pinMode(AI1, a.OUTPUT)
#a.pinMode(AI2, a.OUTPUT)
#a.pinMode(PWM, a.OUTPUT)
a.pinMode(stdby, a.OUTPUT)

m1 = Motor(AI1, AI2, PWM)
m1.setupMotor(a)

a.digitalWrite(stdby, a.HIGH)
try:
    while True:
        speed = input("Input speed: ")
        if speed == "exit":
            break
        m1.drive(int(speed), a)
except Exception as e:
    print(e)

m1.drive(0, a)
