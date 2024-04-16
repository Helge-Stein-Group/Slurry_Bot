import time
from xarm.wrapper import XArmAPI


#This function is called when the error or warning code changes
def hangle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))

class Robot():
    def __init__(self):
        self.arm = XArmAPI('192.168.1.200')
        #self.vial_box = self.VialBox(self.arm)

    def restart(self):
        self.arm.disconnect()
        self.arm.connect()
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_gripper_enable(True)
        self.arm.set_gripper_mode(0)

    def initialize(self):
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_gripper_enable(True)
        self.arm.set_gripper_mode(0)
        self.arm.set_initial_point([-228, 0, 133, 0, 90, 180])
        self.arm.register_error_warn_changed_callback(hangle_err_warn_changed)
        self.arm.connect()
        self.arm.set_position(x=-228, y=0, z=133, roll=0, pitch=90, yaw=180, speed=20, wait=True)
        self.arm.set_linear_track_back_origin(wait=True)
        self.arm.set_linear_track_enable(True)
        self.arm.set_linear_track_speed(200)

    def close(self):
        self.arm.disconnect()

    def GoTo_InitialPoint(self, speedfactor):
        self.arm.set_position(x=-228, y=0, z=133, roll=0, pitch=90, yaw=180, speed=20*speedfactor, wait=True)
        self.arm.set_linear_track_pos(600, wait=True)
        self.arm.set_gripper_position(400, wait=True)

    def GoTo_Point(self, name, speed, wait=True):
        position = fixed_points[name]
        self.arm.set_position(x=position[0], y=position[1], z=position[2], roll=position[3], pitch=position[4], yaw=position[5], speed=speed, wait=wait)
    
    def GoTo_Vial(self, vial_number):
        vial_position = vials[vial_number]
        self.arm.set_position(x=vial_position[0], y=vial_position[1], relative= True, speed=20, wait=True)
    
    def GoTo_Tip(self, tip_number):
        tip_position = tips[tip_number]
        self.arm.set_position(x=tip_position[0], y=tip_position[1], relative= True, speed=20, wait=True)

    def GripperAction(self, name):
        width = gripper_position[name]
        self.arm.set_gripper_position(width=[0], wait=[1])

    def adjust_speed(speedfactor):
        if speedfactor is None:
            speedfactor = 1
        else:
            return speedfactor

    def PickUpVial(self, vial_number, speedfactor):
        speedfactor = self.adjust_speed(speedfactor)

        robot.GripperAction("ReleaseVial")
        robot.GoTo_Point("VialStoragePoint", 200*speedfactor)
        robot.GoTo_Vial(vial_number)
        robot.arm.set_position(z=-158, relative=True, speed=30*speedfactor, wait=True)
        robot.GripperAction("GrabVial")
        robot.arm.set_position(z=158, relative=True, speed=30*speedfactor, wait=True)
        robot.GoTo_Point("VialStoragePoint", 80*speedfactor)   

    def VialToScale(self, speedfactor):
        speedfactor = self.adjust_speed(speedfactor)

        robot.arm.set_position(x=-280, y=-100, z=125, roll=-160, pitch=90, yaw=0, speed=200*speedfactor, wait=True)#inbetween point
        robot.GoTo_Point("Scale", 180*speedfactor)
        robot.arm.set_position(y=130, relative=True, speed=60*speedfactor, wait=True)#moving into the scale
        robot.arm.set_position(z=-39.5, relative=True, speed=30*speedfactor, wait=True)#moving down on the scale
        robot.GripperAction("ReleaseVial")

    def ScaleToDispenser1(self, speedfactor):
        speedfactor = self.adjust_speed(speedfactor)

        robot.GripperAction("GrabVial")
        robot.arm.set_position(z=39.5, relative=True, speed=30*speedfactor, wait=True)#moving up on the scale
        robot.GoTo_Point("Scale", 60*speedfactor)#moving out of the scale 
        robot.GoTo_Point("DispenserPoint", 150*speedfactor)
        robot.GoTo_Point("Dispenser1", 80*speedfactor)
        robot.arm.set_position(z=35, relative=True, speed=20*speedfactor, wait=True)#closing the dispenser with the vial, needs adjustemnt as soon as the new piece is printed 
        
    def Dispenser1ToScale(self, speedfactor):
        robot.GoTo_Point("Dispenser1", 20*speedfactor)
        robot.GoTo_Point("DispenserPoint", 30*speedfactor)
        robot.GoTo_Point("Scale", 150*speedfactor)
        robot.arm.set_position(y=130, relative=True, speed=60*speedfactor, wait=True)#moving into the scale
        robot.arm.set_position(z=-39.5, relative=True, speed=30*speedfactor, wait=True)#moving down on the scale 
        robot.GripperAction("ReleaseVial")

    def ScaleToVialRestPoint(self, speedfactor):
        speedfactor = self.adjust_speed(speedfactor)

        robot.GripperAction("GrabVial")
        robot.arm.set_position(z=39.5, relative=True, speed=30*speedfactor, wait=True)#moving up on the scale 
        robot.GoTo_Point("Scale", 60*speedfactor)#moving out of the scale
        robot.GoTo_Point("DispenserPoint", 150*speedfactor)#used as inbetween point
        robot.arm.set_linear_track_pos(200, wait=True)
        robot.GoTo_Point("VialRestPoint", 80*speedfactor)
        robot.arm.set_position(z=-127, relative=True, speed=30*speedfactor, wait=True)#going down in the hole
        robot.GripperAction("ReleasePipette")

    def PickUpPipette(self, speedfactor):
        robot.GoTo_Point("VialRestPoint", 90*speedfactor)
        robot.GoTo_Point("PipettePoint", 150*speedfactor)
        robot.arm.set_position(x=-367, y=-212, z=193.2, roll= 90, pitch= 90, yaw=0, speed=60*speedfactor, wait=True) #grabbing pipette
        robot.GripperAction("GrabPipette")
        robot.arm.set_position(z=26.8, relative=True, speed=30*speedfactor, wait=True) #lifting pipette
                
    def PickUpPipetteTip(self, tip_number, speedfactor):
        speedfactor = self.adjust_speed(speedfactor)

        robot.GoTo_Point("PipettePoint", 40*speedfactor)
        robot.GoTo_Point("PipetteTip1", 30*speedfactor) #make it higher so we can reuse that with tip on (z=310)
        robot.GoTo_Tip(tip_number)
        robot.arm.set_position(z=-10, relative=True, speed=3*speedfactor, wait=True)#this then needs to be adjusted (310-220= 90 -> z=-100 instead)
        robot.arm.set_position(z=-10, relative=True, speed=3*speedfactor, wait=True)
        robot.arm.set_position(z=-10, relative=True, speed=6*speedfactor, wait=True)
        robot.arm.set_position(z=120, relative=True, speed=20*speedfactor, wait=True)

    def MoveToBinder(self, speedfactor):
        speedfactor = self.adjust_speed(speedfactor)

        robot.arm.set_position(x=-9, y=-19, relative=True, speed=20*speedfactor, wait=True)
        robot.arm.set_position(z=-35, relative=True, speed=20*speedfactor, wait=True)#still outside of vial
        robot.arm.set_position(z=-66, relative=True, speed=10*speedfactor, wait=True)#going into the vial
       
    def BinderToVialRestPoint(self, speedfactor):
        speedfactor = self.adjust_speed(speedfactor)

        robot.arm.set_position(z=140, relative=True, speed=20*speedfactor, wait=True)
        robot.GoTo_Point("PipetteVialRest", 30*speedfactor)
        robot.arm.set_position(z=-45, relative=True, speed=20*speedfactor, wait=True)   
    
    def PuttingBackPipetteTip (self, tip_number, speedfactor):
        speedfactor = self.adjust_speed(speedfactor)

        robot.arm.set_position(z=100, relative=True, speed=20*speedfactor, wait=True)
        robot.GoTo_Point("PipetteTip1", 30*speedfactor) #should be already so high that the pipett ecan go there without needing to go higher first
        #robot.arm.set_position(x=-263.5, y=-121, z=310, roll= 90, pitch= 91, yaw=0, speed=20*speedfactor, wait=True)
        robot.GoTo_Tip(tip_number)
        robot.arm.set_position(z=-60, relative=True, speed=3*speedfactor, wait=True)#this then needs to be adjusted (310-220= 90 -> z=-100 instead)

    def PuttingBackPipette (self, speedfactor):
        speedfactor = self.adjust_speed(speedfactor)

        robot.GoTo_Point("PipettePoint", 30*speedfactor)
        robot.arm.set_position(x=-367, y=-212, z=250, roll= 90, pitch= 90, yaw=0, speed=60*speedfactor, wait=True) #grabbing pipette
        robot.arm.set_position(z=-56.8, relative=True, speed=10*speedfactor, wait=True)
        robot.arm.GrpperAction("ReleasePipette")
        robot.GoTo_Point("PipettePoint", 30*speedfactor)

    
robot = Robot()

robot.initialize()
robot.GoTo_InitialPoint()
robot.restart()

robot.PickUpVial(1) 
robot.VialToScale() 
robot.ScaleToDispenser1()
robot.DispenserToScale()
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


fixed_points = {
    "InitialPoint": (-228, 0, 133, 180, 90, 0),
    "VialStoragePoint": (-273, -100.5, 125, 90, 90, 0),
    "Vial0": (-273, -100.5, -33, 90, 90, 0),
    "Scale":(-287, 120, 92, -90, 90, 0),
    "DispenserPoint": (-400, 50, 92, 180, 90, 0),
    "Dispenser1": (-537, -98, 40, 180, 90, 0),
    "VialRestPoint": (-367.5, -102.5, 92, 180, 90, 0),
    "PipettePoint": (-370, -110, 250, 90, 91, 0),
    "PipetteTip1": (-263.5, -121, 220, 90, 91, 0), #i want to make pipettetip1 so high that the pipette can go over it when the tip is on 
    "PipetteVialRest": (-337, -104.5, 290, 180, 90, 0),
    "MixerPoint": (-600.7, -60.2, 19, 90, 90, 0),    
}

vials = {
    "1": (0, 0),
    "2": (-50, 0),
    "3": (-100, 0),
    "4": (-150, 0),
    "5": (0, -50),
    "6": (-50, -50),
    "7": (-100, -50),
    "8": (-150, -50),
}

tips = {
    "1": (0, 0),
    "2": (-25, 0),
    "3": (-50, 0),
    "4": (-75, 0),
}
gripper_position = {
    "GrabVial": (185, True),
    "ReleaseVial": (400, True),
    "ReleasePipette": (800, True),
    "GrabPipette": (380, True),
}