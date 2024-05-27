from xarm.wrapper import XArmAPI

class Robot():

    def __init__(self):
        self.arm = XArmAPI('192.168.1.200')
        self.savedegree = 0

    def restart(self):
        self.arm.disconnect()
        self.arm.connect()
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_gripper_enable(True)
        self.arm.set_gripper_mode(0)

    def hangle_err_warn_changed(item):
        print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))

    def initialize(self):
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_gripper_enable(True)
        self.arm.set_gripper_mode(0)
        self.arm.set_initial_point([-228, 0, 133, 0, 90, 180])
        #self.arm.register_error_warn_changed_callback(self.hangle_err_warn_changed())
        self.arm.connect()
        self.arm.set_position(x=-228, y=0, z=133, roll=0, pitch=90, yaw=180, speed=20, wait=True)
        self.arm.set_linear_track_back_origin(wait=True)
        self.arm.set_linear_track_enable(True)
        self.arm.set_linear_track_speed(200)

    def close(self):
        self.arm.disconnect()
    
    def GoTo_InitialPoint(self,speedfactor=1):
        self.arm.set_position(x=-228, y=0, z=133, roll=0, pitch=90, yaw=180, speed=20*speedfactor, wait=True)
        self.arm.set_linear_track_pos(600, wait=True)
        self.arm.set_gripper_position(400, wait=True)

    def GoTo_Point(self, name, speed, wait=True):
        position = fixed_points[name]
        self.arm.set_position(x=position[0], y=position[1], z=position[2], roll=position[3], pitch=position[4], yaw=position[5], speed=speed, wait=wait)
    
    def GoTo_Vial(self, vial_number, speed):
        vial_position = vials[vial_number]
        self.arm.set_position(x=vial_position[0], y=vial_position[1], relative= True, speed=speed, wait=True)
    
    def GoTo_Tip(self, tip_number, speed):
        tip_position = tips[tip_number]
        self.arm.set_position(x=tip_position[0], y=tip_position[1], relative= True, speed=speed, wait=True)

    def GripperAction(self, name):
        width = gripper_position[name]
        self.arm.set_gripper_position(width[0], wait=[1])

    def PickUpVial(self, vial_number, speedfactor=1):
        self.arm.set_linear_track_pos(600, wait=True)
        self.GripperAction("ReleaseVial")
        self.GoTo_Point("VialStoragePoint", 200*speedfactor)
        self.GoTo_Vial(vial_number,80*speedfactor)
        self.arm.set_position(z=-158, relative=True, speed=60*speedfactor, wait=True)
        self.GripperAction("GrabVial")
        self.arm.set_position(z=158, relative=True, speed=60*speedfactor, wait=True)
        self.GoTo_Point("VialStoragePoint", 80*speedfactor)   

    def VialToScale(self, speedfactor=1):
        self.arm.set_linear_track_pos(600, wait=True)
        self.GoTo_Point("VialStoragePoint", 80*speedfactor) #Start point 
        self.arm.set_position(x=-280, y=-100, z=125, roll=-160, pitch=90, yaw=0, speed=180*speedfactor, wait=True)#inbetween point
        self.GoTo_Point("Scale", 200*speedfactor)
        self.arm.set_position(y=130, relative=True, speed=80*speedfactor, wait=True)#moving into the scale
        self.arm.set_position(z=-39.5, relative=True, speed=50*speedfactor, wait=True)#moving down on the scale
        self.GripperAction("ReleaseVial")

    def LiftVial(self, speedfactor=1):
        #self.arm.set_position(x=-287, y=250, z=52.5, roll=-90, pitch=90, yaw=0, speed=50*speedfactor, wait=True)#Start point, IN THE SCALE
        self.GripperAction("GrabVial")
        self.arm.set_position(z=20, relative=True, speed=50*speedfactor, wait=True)#moving up on the scale

    def DropVial(self, speedfactor=1):
        #self.arm.set_position(x=-287, y=250, z=72.5, roll=-90, pitch=90, yaw=0, speed=50*speedfactor, wait=True)#Start point, IN THE SCALE
        self.arm.set_position(z=-20, relative=True, speed=50*speedfactor, wait=True)#moving up on the scale
        self.GripperAction("ReleaseVial")

    def ScaleToDispenser1(self, speedfactor=1):
        self.arm.set_linear_track_pos(600, wait=True)
        self.arm.set_position(x=-287, y=250, z=52.5, roll=-90, pitch=90, yaw=0, speed=50*speedfactor, wait=True)#Start point, IN THE SCALE
        self.GripperAction("GrabVial")
        self.arm.set_position(z=39.5, relative=True, speed=50*speedfactor, wait=True)#moving up on the scale
        self.GoTo_Point("Scale", 80*speedfactor)#moving out of the scale 
        self.GoTo_Point("DispenserPoint", 250*speedfactor)
        self.GoTo_Point("Dispenser1", 60*speedfactor)
        self.arm.set_position(z=35, relative=True, speed=20*speedfactor, wait=True)#closing the dispenser with the vial, needs adjustemnt as soon as the new piece is printed 

    def ScaleToDispenser2(self, speedfactor=1):
        self.arm.set_linear_track_pos(600, wait=True)
        self.arm.set_position(x=-287, y=250, z=52.5, roll=-90, pitch=90, yaw=0, speed=50*speedfactor, wait=True)#Start point, IN THE SCALE
        self.GripperAction("GrabVial")
        self.arm.set_position(z=39.5, relative=True, speed=50*speedfactor, wait=True)#moving up on the scale
        self.GoTo_Point("Scale", 80*speedfactor)#moving out of the scale 
        self.GoTo_Point("DispenserPoint", 250*speedfactor)
        self.GoTo_Point("Dispenser2", 60*speedfactor)
        self.arm.set_position(z=35, relative=True, speed=20*speedfactor, wait=True)#closing the dispenser with the vial, needs adjustemnt as soon as the new piece is printed 
        
    def Dispenser1ToScale(self, speedfactor=1):
        self.arm.set_linear_track_pos(600, wait=True)
        self.GoTo_Point("Dispenser1", 20*speedfactor)#Start point
        self.GoTo_Point("DispenserPoint", 30*speedfactor)
        self.GoTo_Point("Scale", 250*speedfactor)
        self.arm.set_position(y=130, relative=True, speed=80*speedfactor, wait=True)#moving into the scale
        self.arm.set_position(z=-39.5, relative=True, speed=50*speedfactor, wait=True)#moving down on the scale 
        self.GripperAction("ReleaseVial")

    def Dispenser2ToScale(self, speedfactor=1):
        self.arm.set_linear_track_pos(600, wait=True)
        self.GoTo_Point("Dispenser2", 20*speedfactor)#Start point
        self.GoTo_Point("DispenserPoint", 30*speedfactor)
        self.GoTo_Point("Scale", 250*speedfactor)
        self.arm.set_position(y=130, relative=True, speed=80*speedfactor, wait=True)#moving into the scale
        self.arm.set_position(z=-39.5, relative=True, speed=50*speedfactor, wait=True)#moving down on the scale 
        self.GripperAction("ReleaseVial")

    def ScaleToVialRestPoint(self, speedfactor=1):
        self.arm.set_linear_track_pos(600, wait=True)
        self.arm.set_position(x=-287, y=250, z=52.5, roll=-90, pitch=90, yaw=0, speed=50*speedfactor, wait=True)#Start point, IN THE SCALE
        self.GripperAction("GrabVial")
        self.arm.set_position(z=39.5, relative=True, speed=50*speedfactor, wait=True)#moving up on the scale 
        self.GoTo_Point("Scale", 80*speedfactor)#moving out of the scale
        self.GoTo_Point("DispenserPoint", 150*speedfactor)#used as inbetween point
        self.arm.set_linear_track_pos(200, wait=True)
        self.GoTo_Point("VialRestPoint", 80*speedfactor)
        self.arm.set_position(z=-127, relative=True, speed=80*speedfactor, wait=True)#going down in the hole
        self.GripperAction("ReleasePipette")
        self.GoTo_Point("VialRestPoint", 80*speedfactor)

    def VialRestPointToScale(self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.GoTo_Point("VialRestPoint", 80*speedfactor)
        self.arm.set_position(z=-127, relative=True, speed=80*speedfactor, wait=True)
        self.GripperAction("GrabVial")
        self.GoTo_Point("VialRestPoint", 80*speedfactor)
        self.arm.set_linear_track_pos(600, wait=True)
        self.GoTo_Point("Scale", 80*speedfactor)
        self.arm.set_position(y=130, relative=True, speed=80*speedfactor, wait=True)#moving into the scale
        self.arm.set_position(z=-39.5, relative=True, speed=50*speedfactor, wait=True)#moving down on the scale 
        self.GripperAction("ReleaseVial")

    def PickUpPipette(self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.GripperAction("ReleasePipette")
        self.GoTo_Point("PipettePoint", 150*speedfactor)#Start point
        self.arm.set_position(x=-367, y=-212, z=193.2, roll= 90, pitch= 90, yaw=0, speed=100*speedfactor, wait=True) #grabbing pipette
        self.GripperAction("GrabPipette")
        self.arm.set_position(z=26.8, relative=True, speed=50*speedfactor, wait=True) #lifting pipette
                
    def PickUpPipetteTip(self, tip_number, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.GoTo_Point("PipettePoint", 60*speedfactor)#Start point
        self.GoTo_Point("PipetteTip1", 100*speedfactor)
        self.GoTo_Tip(tip_number,speedfactor)
        self.arm.set_position(z=-150, relative=True, speed=30*speedfactor, wait=True)
        self.arm.set_position(z=-10, relative=True, speed=3*speedfactor, wait=True)
        self.arm.set_position(z=-10, relative=True, speed=3*speedfactor, wait=True)
        self.arm.set_position(z=-10, relative=True, speed=6*speedfactor, wait=True)
        self.arm.set_position(z=120, relative=True, speed=50*speedfactor, wait=True)

    def MoveToBinder(self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.arm.set_position(x=-263.5, y=-121, z=310, roll= 90, pitch= 91, yaw=0, speed=100*speedfactor, wait=True) #Start point
        self.arm.set_position(x=-9, y=-19, relative=True, speed=40*speedfactor, wait=True)
        self.arm.set_position(z=-35, relative=True, speed=40*speedfactor, wait=True)#still outside of vial
        self.arm.set_position(z=-66, relative=True, speed=10*speedfactor, wait=True)#going into the vial
       
    def BinderToVialRestPoint(self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        #self.arm.set_position(x=-272.5, y=-140, z=209, roll= 90, pitch= 91, yaw=0, speed=100*speedfactor, wait=True) #Start point INSIDE BINDER
        self.arm.set_position(z=140, relative=True, speed=40*speedfactor, wait=True)
        self.GoTo_Point("PipetteVialRest", 100*speedfactor)
        self.arm.set_position(z=-45, relative=True, speed=40*speedfactor, wait=True)   
    
    def VialRestPointToBinder(self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.GoTo_Point("PipetteVialRest", 40*speedfactor)#Start point
        self.GoTo_Point("PipetteTip1", 120*speedfactor)
        self.arm.set_position(x=-9, y=-19, relative=True, speed=40*speedfactor, wait=True)
        self.arm.set_position(z=-95, relative=True, speed=40*speedfactor, wait=True)#still outside of vial
        self.arm.set_position(z=-66, relative=True, speed=10*speedfactor, wait=True)#going into the vial

    def PuttingBackPipetteTip (self, tip_number, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        #self.arm.set_position(x=-337, y=-104.5, z=245, roll= 180, pitch= 90, yaw=0, speed=100*speedfactor, wait=True) #Start point INSIDE VIAL
        self.arm.set_position(z=60, relative=True, speed=40*speedfactor, wait=True)
        self.GoTo_Point("PipetteTip1", 120*speedfactor)
        self.GoTo_Tip(tip_number, speedfactor)
        self.arm.set_position(z=-100, relative=True, speed=10*speedfactor, wait=True)

    def PuttingBackPipette (self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.GoTo_Point("PipettePoint", 100*speedfactor)#Start point
        self.arm.set_position(x=-367, y=-212, z=250, roll= 90, pitch= 90, yaw=0, speed=60*speedfactor, wait=True) 
        self.arm.set_position(z=-56.8, relative=True, speed=30*speedfactor, wait=True)
        self.GripperAction("ReleasePipette")
        self.GoTo_Point("PipettePoint", 100*speedfactor)

    def VialToMixing (self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.GripperAction("ReleasePipette")
        self.GoTo_Point("VialRestPoint", 120*speedfactor)#Start point
        self.arm.set_position(z=-129, relative=True, speed=80*speedfactor, wait=True)#going down in the hole
        self.GripperAction("GrabVial")
        self.GoTo_Point("VialRestPoint", 80*speedfactor)

        self.GoTo_Point("MixerPoint", 60*speedfactor)
        self.arm.set_position(y=-84.2, relative=True, speed=60*speedfactor, wait=True)
        self.arm.set_position(z=-49, relative=True, speed=20*speedfactor, wait=True)
        self.GripperAction("ReleaseVial")
        self.GoTo_Point("MixerPoint", 100*speedfactor)

    def TurnOnHomogenizer (self, degree, speedfactor=1):#degree:10
        self.arm.set_linear_track_pos(200, wait=True)
        self.GripperAction("ReleaseHomogenizerDial")
        self.GoTo_Point("MixerPoint", 100*speedfactor)#Start point
        self.arm.set_position(z=165, relative=True, speed=30*speedfactor, wait=True)
        self.arm.set_position(x=-10, y=-28, relative=True, speed=30*speedfactor, wait=True)
        self.GripperAction("GrabHomogenizerDial")
        self.arm.set_position(pitch=-degree, relative=True, speed=30*speedfactor, wait=True)
        self.savedegree = degree
        self.GripperAction("ReleaseHomogenizerDial")
        self.GoTo_Point("MixerPoint", 60*speedfactor)

    def TurnOffHomogenizer (self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.GripperAction("ReleaseHomogenizerDial")
        self.GoTo_Point("MixerPoint", 60*speedfactor)#Start point
        self.arm.set_position(z=165, pitch=-self.savedegree, relative=True, speed=30*speedfactor, wait=True)
        self.arm.set_position(x=-10, y=-28, relative=True, speed=30*speedfactor, wait=True)
        self.GripperAction("GrabHomogenizerDial")
        self.arm.set_position(pitch=self.savedegree, relative=True, speed=30*speedfactor, wait=True)
        self.GripperAction("ReleaseHomogenizerDial")
        self.GoTo_Point("MixerPoint", 60*speedfactor)
        self.GoTo_InitialPoint()


    
fixed_points = {
    "InitialPoint": (-228, 0, 133, 180, 90, 0),
    "VialStoragePoint": (-273, -100.5, 125, 90, 90, 0),
    "Vial0": (-273, -100.5, -33, 90, 90, 0),
    "Scale":(-287, 120, 92, -90, 90, 0),
    "DispenserPoint": (-400, 50, 92, 180, 90, 0),
    #"Dispenser1": (-537, -98, 40, 180, 90, 0) #the one on the right
    "Dispenser1": (-537, 52, 40, 180, 90, 0),#the one on the left
    "VialRestPoint": (-367.5, -102.5, 92, 180, 90, 0),
    "PipettePoint": (-370, -110, 250, 90, 91, 0),
    "PipetteTip1": (-263.5, -121, 370, 90, 91, 0),
    "PipetteVialRest": (-337, -104.5, 290, 180, 90, 0),
    "MixerPoint": (-600.7, -60.2, 19, 90, 90, 0),    
}

vials = {
    "Vial1": (0, 0),
    "Vial2": (-50, 0),
    "Vial3": (-100, 0),
    "Vial4": (-150, 0),
    "Vial5": (0, -40),
    "Vial6": (-50, -40),
    "Vial7": (-100, -40),
    "Vial8": (-150, -40),
}

tips = {#needs to be checked
    "1": (0, 0),
    "2": (50, 0),
    "3": (100, 0),
    "4": (0, -50),
    "5": (50, -50),
    "6": (100, -50),
}

gripper_position = {
    "GrabVial": (185, True),
    "ReleaseVial": (400, True),
    "ReleasePipette": (800, True),
    "GrabPipette": (380, True),
    "ReleaseHomogenizerDial": (800, True),
    "GrabHomogenizerDial": (510, True),
}