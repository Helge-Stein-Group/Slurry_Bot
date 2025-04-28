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
        self.arm.set_initial_point([-400, 0, 133, 0, 90, 180])#TCP Gripper
        self.arm.connect()
        self.arm.set_position(x=-400, y=0, z=133, roll=0, pitch=90, yaw=180, speed=20, wait=True)#TCP Gripper
        self.arm.set_linear_track_back_origin(wait=True)
        self.arm.set_linear_track_enable(True)
        self.arm.set_linear_track_speed(200)

    def close(self):
        self.arm.disconnect()
    
    def GoTo_InitialPoint(self,speedfactor=1):
        self.arm.set_position(x=-400, y=0, z=133, roll=0, pitch=90, yaw=180, speed=20*speedfactor, wait=True)#TCP Gripper
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
        self.arm.set_position(x=tip_position[0], y=tip_position[1],z=tip_position[2], roll=tip_position[3], pitch=tip_position[4], yaw=tip_position[5], speed=speed, wait=True)

    def GripperAction(self, name):
        width = gripper_position[name]
        self.arm.set_gripper_position(width[0], wait=[1])

    def PickUpVial(self, vial_number, speedfactor=1):
        self.arm.set_linear_track_pos(600, wait=True)
        self.GripperAction("ReleaseVial")
        self.GoTo_Point("VialStoragePoint", 60*speedfactor)
        self.GoTo_Vial(vial_number,80*speedfactor)
        self.arm.set_position(z=-129, relative=True, speed=60*speedfactor, wait=True)
        self.GripperAction("GrabVial")
        self.arm.set_position(z=129, relative=True, speed=60*speedfactor, wait=True)
        self.GoTo_Point("VialStoragePoint", 60*speedfactor)   

    def VialToScale(self, speedfactor=1):
        self.arm.set_linear_track_pos(600, wait=True)
        self.GoTo_Point("VialStoragePoint", 80*speedfactor) #Start point 
        self.arm.set_position(x=-452, y=-100, z=125, roll=-160, pitch=90, yaw=0, speed=120*speedfactor, wait=True)#TCP Gripper
        self.GoTo_Point("Scale", 120*speedfactor)
        self.arm.set_position(y=140, relative=True, speed=80*speedfactor, wait=True)#moving into the scale
        self.arm.set_position(z=-26, relative=True, speed=50*speedfactor, wait=True)#moving down on the scale
        self.GripperAction("ReleaseVial")

    def LiftVial(self, speedfactor=1):
        self.GripperAction("GrabVial")
        self.arm.set_position(z=26, relative=True, speed=50*speedfactor, wait=True)#moving up on the scale

    def DropVial(self, speedfactor=1):
        self.arm.set_position(z=-26, relative=True, speed=50*speedfactor, wait=True)#moving up on the scale
        self.GripperAction("ReleaseVial")

    def ScaleToLiquidRestPoint (self, speedfactor=1):
        self.GripperAction('GrabVial')
        self.arm.set_position(z=26, relative=True, speed=60*speedfactor, wait=True)
        self.GoTo_Point("Scale", 80*speedfactor)
        self.arm.set_position(x=-452, y=-100, z=125, roll=-160, pitch=90, yaw=0, speed=120*speedfactor, wait=True)#inbetween point #TCP Gripper
        self.GoTo_Point("PipettePoint", 100*speedfactor)
        self.arm.set_linear_track_pos(200, wait=True)
        self.GoTo_Point("VialRestPoint", 100*speedfactor)
        self.arm.set_position(z=-182, relative=True, speed=30*speedfactor, wait=True)
        self.GripperAction('ReleaseVial')

    def PickUpPipette(self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.arm.set_position(z=182, relative=True, speed=50*speedfactor, wait=True)
        self.GripperAction("ReleasePipette")
        self.GoTo_Point("PipettePoint", 50*speedfactor)#Start point
        self.arm.set_position(y=-102, z=-56.8, relative=True, speed=50*speedfactor, wait=True) #grabbing pipette #TCP Gripper
        self.GripperAction("GrabPipette")
        self.arm.set_position(z=26.8, relative=True, speed=50*speedfactor, wait=True) #lifting pipette
        self.GoTo_Point("PipettePoint", 60*speedfactor)

    def GettingPipetteTip (self, tip_number, speedfactor=1):
        self.GoTo_Tip(tip_number,30*speedfactor)
        self.arm.set_position(z=-165, relative=True, speed=40*speedfactor, wait=True)
        self.arm.set_position(z=-33, relative=True, speed=20*speedfactor, wait=True)
        self.arm.set_position(z=198, relative=True, speed=40*speedfactor, wait=True)

    def TakingLiquid (self, tip_number, speedfactor=1):
        self.GoTo_Tip(tip_number,30*speedfactor)
        self.arm.set_position(x=15, y=-19, relative=True, speed=30, wait=True)
        self.arm.set_position(z=-120, relative=True, speed=30, wait=True)

    def LiquidToVial (self, speedfactor=1):
        self.arm.set_position(z=120, relative=True, speed=30*speedfactor, wait=True)
        self.GoTo_Point("PipetteVialRest", 30*speedfactor)
        self.arm.set_position(z=-60, relative=True, speed=30*speedfactor, wait=True)

    def PuttingBackPipetteTip (self, tip_number, speedfactor=1):
        self.arm.set_position(z=60, relative=True, speed=30, wait=True)
        self.GoTo_Tip(tip_number,30*speedfactor)
        self.arm.set_position(z=-65, relative=True, speed=30, wait=True)#Pipetten Spitze anfang rein
        self.arm.set_position(z=-100, relative=True, speed=30, wait=True)#Pipetten Spitze rein und dan loslassen

    def PuttingBackPipette (self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.GoTo_Point("PipettePoint", 100*speedfactor)#Start point
        self.arm.set_position(y=-102, relative=True, speed=50*speedfactor, wait=True) #grabbing pipette #TCP Gripper
        self.arm.set_position(z=-56.8, relative=True, speed=30*speedfactor, wait=True)
        self.GripperAction("ReleasePipette")
        self.GoTo_Point("PipettePoint", 100*speedfactor)
    
    def LiquidsToMixingPoint (self, speedfactor=1):
        self.GripperAction('ReleaseVial')
        self.GoTo_Point("VialRestPoint", 40*speedfactor)
        self.arm.set_position(z=-182, relative=True, speed=60*speedfactor, wait=True)
        self.GripperAction('GrabVial')
        self.arm.set_position(z=182, relative=True, speed=60*speedfactor, wait=True)
        self.GoTo_Point('MixerPoint', 60*speedfactor)
        self.arm.set_position(y=-95, relative=True, speed=40*speedfactor, wait=True)
        self.arm.set_position(z=-45, relative=True, speed=40*speedfactor, wait=True)
        self.GripperAction('ReleaseVial')
        self.GoTo_Point('MixerPoint', 30*speedfactor)

    def TurnOnHomogenizer (self, degree, speedfactor=1):#degree:10
        self.arm.set_linear_track_pos(200, wait=True)
        self.GripperAction("ReleaseHomogenizerDial")
        self.GoTo_Point("MixerPoint", 100*speedfactor)#Start point
        self.arm.set_position(z=308, relative=True, speed=80*speedfactor, wait=True)
        self.arm.set_position(x=-2, y=-39, relative=True, speed=30*speedfactor, wait=True)
        self.GripperAction("GrabHomogenizerDial")
        self.arm.set_position(pitch=-degree, relative=True, speed=30*speedfactor, wait=True)
        self.savedegree = degree
        self.GripperAction("ReleaseHomogenizerDial")
        self.arm.set_position(y=39, relative=True, speed=30*speedfactor, wait=True)
        self.GoTo_Point("MixerPoint", 60*speedfactor)#Start point

    def TurnOffHomogenizer (self, speedfactor=1):
        self.arm.set_linear_track_pos(200, wait=True)
        self.GripperAction("ReleaseHomogenizerDial")
        self.GoTo_Point("MixerPoint", 60*speedfactor)#Start point
        self.arm.set_position(z=308, pitch=-self.savedegree, relative=True, speed=80*speedfactor, wait=True)
        self.arm.set_position(x=-2, y=-39, relative=True, speed=30*speedfactor, wait=True)
        self.GripperAction("GrabHomogenizerDial")
        self.arm.set_position(pitch=self.savedegree, relative=True, speed=30*speedfactor, wait=True)
        self.GripperAction("ReleaseHomogenizerDial")
        self.arm.set_position(y=39, relative=True, speed=30*speedfactor, wait=True)
        self.GoTo_Point("MixerPoint", 60*speedfactor)

    def MixingPointToLiquids (self, speedfactor=1):
        self.GripperAction('ReleaseVial')
        self.GoTo_Point('MixerPoint', 30*speedfactor)
        self.arm.set_position(y=-95, relative=True, speed=20*speedfactor, wait=True)
        self.arm.set_position(z=-45, relative=True, speed=20*speedfactor, wait=True)
        self.GripperAction('GrabVial')
        self.arm.set_position(z=45, relative=True, speed=20*speedfactor, wait=True)
        self.arm.set_position(y=95, relative=True, speed=20*speedfactor, wait=True)
        self.GoTo_Point("PipettePoint", 40*speedfactor)
        self.arm.set_position(x=142.5, y=-14, relative=True, speed=30*speedfactor, wait=True)
        self.arm.set_position(z=-182, relative=True, speed=30*speedfactor, wait=True)
        self.GripperAction('ReleaseVial')
        self.arm.set_position(z=182, relative=True, speed=30*speedfactor, wait=True)
        self.GoTo_Point('MixerPoint', 30*speedfactor)

    def CleaningLiquidsToMixer (self, liquid, speedfactor=1):
        self.GoTo_Point('MixerPoint', 30*speedfactor)
        self.arm.set_position(x=-700, y=-179.7, z=54, roll=180, pitch=90, yaw=0, speed=40*speedfactor, wait=True)
        liquid_position = cleaningliquids[liquid]
        self.arm.set_position(x=liquid_position[0], y=liquid_position[1], relative= True, speed=20*speedfactor, wait=True)
        self.arm.set_position(x=-46, relative=True, speed=10*speedfactor, wait=True)
        self.arm.set_position(z=-58, relative=True, speed=10*speedfactor, wait=True)
        self.GripperAction('GrabVial')
        self.arm.set_position(z=58, relative=True, speed=10*speedfactor, wait=True)
        self.arm.set_position(x=46, relative=True, speed=10*speedfactor, wait=True)
        self.GoTo_Point('MixerPoint', 30*speedfactor)
        self.arm.set_position(y=-95, relative=True, speed=20*speedfactor, wait=True)
        self.arm.set_position(z=-45, relative=True, speed=20*speedfactor, wait=True)
        self.GripperAction('ReleaseVial')
        self.GoTo_Point('MixerPoint', 30*speedfactor)

    def CleaningLiquidsToStorage (self, liquid, speedfactor=1):
        self.GoTo_Point('MixerPoint', 30*speedfactor)
        self.GripperAction('ReleaseVial')
        self.arm.set_position(y=-95, relative=True, speed=20*speedfactor, wait=True)
        self.arm.set_position(z=-45, relative=True, speed=20*speedfactor, wait=True)
        self.GripperAction('GrabVial')
        self.arm.set_position(z=46, relative=True, speed=20*speedfactor, wait=True)
        self.arm.set_position(y=95, relative=True, speed=20*speedfactor, wait=True)
        self.arm.set_position(x=-700, y=-179.7, z=54, roll=180, pitch=90, yaw=0, speed=40*speedfactor, wait=True)
        liquid_position = cleaningliquids[liquid]
        self.arm.set_position(x=liquid_position[0], y=liquid_position[1], relative= True, speed=20*speedfactor, wait=True)
        self.arm.set_position(x=-46, relative=True, speed=10*speedfactor, wait=True)
        self.arm.set_position(z=-58, relative=True, speed=10*speedfactor, wait=True)
        self.GripperAction('ReleaseVial')
        self.arm.set_position(z=58, relative=True, speed=10*speedfactor, wait=True)
        self.arm.set_position(x=46, relative=True, speed=10*speedfactor, wait=True)
        self.GoTo_Point('MixerPoint', 30*speedfactor)


    
fixed_points = {
    "InitialPoint": (-400, 0, 133, 180, 90, 0),
    "VialStoragePoint": (-425.4, -270.5, 125, 90, 90, 0),#1 vorne
    "Vial0": (-425.4, -272.5, -33, 90, 90, 0),#1vorne
    "Scale":(-288, 292, 102, -90, 90, 0),
    "VialRestPoint": (-223.5, -296, 250, 90, 90, 0),
    "PipettePoint": (-367, -282, 250, 90, 90, 0),
    "PipetteTip1": (-285.5, -293, 400, 90, 90, 0),
    "PipetteVialRest": (-228.5, -267, 400, 90, 90, 0),
    "MixerPoint": (-585.5, -276.2, 54, 90, 90, 0),    
}

vials = { 
    "Vial1": (0, 0),
    "Vial2": (50.8, 0),
    "Vial3": (101.6, 0),
    "Vial4": (152.4, 0),
    "Vial5": (0, -41),
    "Vial6": (50.8, -41),
    "Vial7": (101.6, -41),
    "Vial8": (152.4, -41),
}

tips = {#needs to be checked
    "1": (-285.5, -293, 400, 90, 90, 0),
    "2": (-240.5, -293, 400, 90, 90, 0),
    "3": (-285.5, -338, 400, 90, 90, 0),
    "4": (-240, -338, 400, 90, 90, 0),
}

cleaningliquids = {
    "Water": (0, 0),
    "Isopropanol": (0, 50.8),
}

gripper_position = {
    "GrabVial": (250, True),
    "ReleaseVial": (500, True),
    "ReleasePipette": (850, True),
    "GrabPipette": (500, True),
    "ReleaseHomogenizerDial": (850, True),
    "GrabHomogenizerDial": (570, True),
}
