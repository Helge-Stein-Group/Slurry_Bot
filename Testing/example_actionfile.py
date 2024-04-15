import os
import sys
import time

from xarm.wrapper import XArmAPI
from Robot_wrapper import *
from Drivers.scale_driver import *
from Drivers.motor_driver import *
from Drivers.pipette_driver import *

#initializing and setting up all systems

coms = {
    scaleCom: "COM11",
    motorsCom: "COM9",
    pipetteCom: "COM6"
}

#Robot Connection
robot = Robot()
robot.initialize()
robot.GoTo_InitialPoint()

#Scale Connection
scale = Scale(coms[scaleCom], 9600, 3)
scale.connect()

#Motors Connection
motors = SerialConnection(coms[motorsCom], 9600, 3)
homogenizer_motor = Motor(motors, 0)
dispenser_motor = Motor(motors, 1)

#Pipette Connection
pipette = Pipette(coms[pipetteCom])
pipette.initiate_rline()









time.sleep(0.5)
if arm.warn_code != 0:
    arm.clean_warn()
if arm.error_code != 0:
    arm.clean_error()

