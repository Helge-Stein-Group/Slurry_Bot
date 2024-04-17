from Testing.Robot_wrapper import *
from Testing.dispensing_wrapper import *

robot = Robot()

robot.initialize()
robot.GoTo_InitialPoint()
robot.restart()

robot.PickUpVial('Vial1') 
robot.VialToScale() 
robot.LiftVial()
robot.DropVial()
robot.ScaleToDispenser1()
robot.Dispenser1ToScale()
robot.ScaleToVialRestPoint()
robot.PickUpPipette()
robot.PickUpPipetteTip()
robot.MoveToBinder()

robot.arm.set_linear_track_pos(200, wait=True)

#FromPipetteToVialRestPointToMixer(needs to be finished)
robot.GoTo_Point("VialRestPoint", 30)
robot.arm.set_position(z=-127, relative=True, speed=30, wait=True)#going down in the hole
robot.GripperAction("GrabVial")
robot.GoTo_Point("VialRestPoint", 30)

robot.GoTo_Point("MixerPoint", 30)
robot.arm.set_position(y=-84.2, relative=True, speed=20, wait=True)
robot.arm.set_position(z=-49, relative=True, speed=5, wait=True)
robot.GripperAction("ReleaseVial")
robot.GoTo_Point("MixerPoint", 10)
#Turning on Mixer ist still in  progess. We need to wait till we know th eposition of the mixer when being completely down





#Test Dispensing
from Drivers.scale_driver import *
from Drivers.motor_driver import *
from Testing.dispensing_wrapper import *

coms = {
    'scaleCom': 'COM7',
    'motorsCom': 'COM5',
    'pipetteCom': 'COM6'
}

motors = SerialConnection(coms['motorsCom'], 9600, 3)
dispenser_motor = Motor(motors, 0)

#Scale Connection
scale = Scale(coms['scaleCom'], 9600, 3)
scale.connect()
scale.tare()

my_calibration = Calibration(100,100,"Test","NA", "NA")
my_calibration.calibrate([100,500], 2, dispenser_motor, scale, robot, "Vial1")


#dispense
dispense_precisely(0.1, 1,dispenser_motor,scale,robot, "Vial2")