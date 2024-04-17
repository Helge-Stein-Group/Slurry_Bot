import os
import sys
import time

from xarm.wrapper import XArmAPI
from Robot_wrapper import *
from Drivers.scale_driver import *
from Drivers.motor_driver import *
from Drivers.pipette_driver import *
from dispensing_wrapper import *

#initializing and setting up all systems

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
dispenser_motor = Motor(motors, 0)
dispenser_motor.check_connection()
print(motors.read_response())
#dispenser_motor.move('200')
homogenizer_motor.check_connection()
#homogenizer_motor.moveDown('5700') #(ONLY RUN IF IT IS AT THE VERY TOP)The difference from the top to the bottom is about 5700 steps
#homogenizer_motor.moveUp('5700')


#Pipette Connection
pipette = Pipette(coms['pipetteCom'])
pipette.initialize()


