from Testing.Robot_wrapper import *
from Testing.Pipette import *
from motor_driver import *
import time


class Actions():

    def __init__(self, robot, pipette, homogenizer_motor):
        self.robot = robot
        self.pipette = pipette
        self.homogenizer_motor = homogenizer_motor

    def Pipetting(self, volume, tip_number):
        self.robot.PickUpPipette()
        self.robot.PickUpPipetteTip(tip_number)
        self.robot.MoveToBinder()
        max_volume = 1000

        numberofpipetting = volume // max_volume

        for i in range(numberofpipetting):
            remaining_volume = volume if volume <= max_volume else max_volume
            self.pipette.aspirate(remaining_volume)
            time.sleep(2)
            self.robot.BinderToVialRestPoint()
            self.pipette.dispense(remaining_volume)
            time.sleep(2)
            self.pipette.blowout()
            time.sleep(2)
            self.robot.VialRestPointToBinder()
    
            volume -= max_volume
   
        self.robot.PuttingBackPipetteTip("1")
        self.pipette.eject()
        time.sleep(2)
        self.robot.PuttingBackPipette()

    def StartingMixing(self, degree):
        self.robot.VialToMixing()
        self.homogenizer_motor.moveDown('6000')#(ONLY RUN IF IT IS AT THE VERY TOP)The difference from the top to the bottom is 6000 steps
        self.robot.TurnOnHomogenizer(degree)
    
    def StoppingMixing(self):
        self.robot.TurnOffHomogenizer()
        self.homogenizer_motor.moveUp('6000')