import os
import sys
import time

from xarm.wrapper import XArmAPI
from Testing.Robot_wrapper import *
#from Drivers.scale_driver import *
from Drivers.motor_driver import *
#from Drivers.pipette_driver import *
#from PaperTest.Dispensing_wrapper_robot import *
#from Testing.Overall_wrapper import *

##Initializing and setting up all systems:

coms = {
    'scaleCom': 'COM7',
    'motorsCom': 'COM9',
    #'pipetteCom': 'COM6'
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

time.sleep(10)
dispenser_motor.move(100)


#Pipette Connection
pipette = Pipette(coms['pipetteCom'])
pipette.initialize()


##Making  a Test slurry:
#Calibration
my_calibration = Calibration(100,100,"Test","NA", "NA")
my_calibration.calibrate([5, 15, 30, 70], 2, dispenser_motor, scale, robot, "Vial1")
my_calibration.save_calibration()


robot.GoTo_Point("DispenserPoint", 20)

robot.GoTo_Point("Dispenser1", 10)

robot.GripperAction("ReleaseVial")



robot.PickUpVial("Vial1")
robot.VialToScale()
robot.ScaleToDispenser2()
robot.Dispenser2ToScale()
robot.ScaleToVialRestPoint()


