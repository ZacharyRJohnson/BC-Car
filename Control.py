"""
Main controller program being run on the raspberry pi and sending commands to
the arduino. Program runs as soon as the raspberry pi starts up and then just
waits for a PS4 controller to be connected and send input.
"""
from nanpy import ArduinoApi, SerialManager
from NanMotor import Motor
from robot import Robot
import sys
import pygame
import time

class Controller(object):
    """Object to hold all values of the buttons and axes being used on the
    controller. Each atribute corresponds to the button or axis that is
    mapped to the PS4."""
    def __init__(self):
        """Creates new controller object"""
        self.reset()

    def reset(self):
        """Resets all values on the controller to their default off value"""
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
    """Object for the whole setup used to control the robot with the PS4
    controller. Each RobotController has the following values:

    Attributes:
        cont: Controller object holding vutton values
        joystick: pygame joystick object to get input from the controller
        robot: Robot object being controlled
    """

    def __init__(self, robo):
        """Creates a new RobotController object with robo as the Robot 
        object"""
        self.cont = Controller()
        self.joystick = None
        self.robot = robo

    def init_joystick(self):
        """Initializes pygame and the connected PS4 controller as a pygame
        joystick"""
        pygame.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def loop(self):
        """Main loop for getting input from the controller and driving
        the robot."""
        r2Pressed = 0
        l2Pressed = 0
        rAnalogMoved = 0
        while True:
            self.cont.reset()
            pygame.event.pump()

            for i in range(6): #Reads value of axes 0-5 and puts value into cont
                val = self.joystick.get_axis(i)
                if i in range(6) and val != 0:
                    tmp = "self.cont.axis" + str(i) + " = " + str(val)
                    exec(tmp)

            for i in range(9): #Reads values of buttons 0-8 and puts value into cont
                if self.joystick.get_button(i) != 0:
                    tmp = "self.cont.btn" + str(i) + " = 1"
                    exec(tmp)

            if self.cont.btn8: #If share button is pressed stop program
                break

            if self.cont.btn0: #Stop robot when square is pressed
                self.robot.stop()
            
            if self.cont.axis2 != 0: #Turn robot in direction the right analog stick is moved
                speed = -int(255*self.cont.axis2)
                self.robot.turn(speed)
                rAnalogMoved = 1

            if self.cont.axis2 == 0 and rAnalogMoved: #Stop robot when analog stick is at 0
                self.robot.stop()
                rAnalogMoved = 0

            if self.cont.btn7: #Drive robot forward when R2 is pressed
                speed = int(127.5 + (127.5*self.cont.axis4))
                r2Pressed = 1
                self.robot.forward(speed) 
            
            if self.cont.btn7 == 0 and r2Pressed: #Stop robot when R2 is released
                self.robot.stop()
                r2Pressed = 0

            if self.cont.btn6: #Drive robot backwards when L2 is pressed
                speed = int(127.5 + (127.5*self.cont.axis3))
                l2Pressed = 1
                self.robot.reverse(speed)

            if self.cont.btn6 == 0 and l2Pressed: #Stop robot when L2 is released
                self.robot.stop()
                l2Pressed = 0

    def close(self):
        """Stops motors and closes the joystick for when the program is done"""
        self.robot.stop()
        if self.joystick:
            self.joystick.quit()

# Motor controller pins and the pins they are connected to on the arduino
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

"""
Setup and initalize the robot and all of its motors with the proper motor
pins. Returns the initalized robot object
"""
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

#Creates new robot object and RobotController object then runs the main loop
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
            break

except Exception as e:
    rc.close()
    print(e)



