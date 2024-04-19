import os
import sys
import time

from xarm.wrapper import XArmAPI
from Robot_wrapper import *
from Drivers.scale_driver import *
from Drivers.motor_driver import *
from Drivers.pipette_driver import *
from dispensing_wrapper import *
from Overall_wrapper import *

##Initializing and setting up all systems:

coms = {
    'scaleCom': 'COM7',
    'motorsCom': 'COM5',
    'pipetteCom': 'COM6'
}

#Robot Connection
robot = Robot()
robot.initialize()
robot.GoTo_InitialPoint()

#Scale Connection
scale = Scale(coms['scaleCom'], 9600, 3)
scale.connect()
scale.tare()

#Motors Connection
motors = SerialConnection(coms['motorsCom'], 9600, 3)
homogenizer_motor = Motor(motors, 1)
homogenizer_motor.check_connection()
dispenser_motor = Motor(motors, 0)
dispenser_motor.check_connection()

#Pipette Connection
pipette = Pipette(coms['pipetteCom'])
pipette.initialize()


##Making  a Test slurry:
#Calibration
my_calibration = Calibration(100,100,"Test","NA", "NA")
my_calibration.calibrate([5, 15, 30, 70], 2, dispenser_motor, scale, robot, "Vial1")
my_calibration.save_calibration()

#Dispensing
dispense_precisely(0.9, 2,dispenser_motor,scale,robot, "Vial2")

#Pipetting
Pipetting(3000, "1")

#Mixing
StartingMixing (10)
StoppingMixing()
