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

    def GoTo_InitialPoint(self):
        self.arm.set_position(x=-228, y=0, z=133, roll=0, pitch=90, yaw=180, speed=20, wait=True)
        self.arm.set_linear_track_pos(600, wait=True)

    def GoTo_Point(self, name, speed, wait=True):
        position = fixed_points[name]
        self.arm.set_position(x=position[0], y=position[1], z=position[2], roll=position[3], pitch=position[4], yaw=position[5], speed=speed, wait=wait)
    
    def PickUpVial0(self):
        robot.arm.set_gripper_position(400, wait=True)
        robot.GoTo_Point("VialStoragePoint", 100)
        robot.GoTo_Point("Vial0", 60)
        robot.arm.set_gripper_position(185, wait=True)#grab vial
        robot.GoTo_Point("VialStoragePoint", 60)  

    def VialToScale(self):
        robot.arm.set_position(x=-280, y=-100, z=125, roll=-160, pitch=90, yaw=0, speed=60, wait=True)#inbetween point
        robot.GoTo_Point("Scale", 60)
        robot.arm.set_position(y=130, relative=True, speed=60, wait=True)#moving into the scale
        robot.arm.set_position(z=-39.5, relative=True, speed=30, wait=True)#moving down on the scale
        robot.arm.set_gripper_position(400, wait=True)

    def ScaleToDispenser1(self):
        robot.arm.set_gripper_position(185, wait=True)
        robot.arm.set_position(z=39.5, relative=True, speed=30, wait=True)#moving up on the scale
        robot.GoTo_Point("Scale", 60)#moving out of the scale 
        robot.GoTo_Point("DispenserPoint", 60)
        robot.GoTo_Point("Dispenser1", 40)
        robot.arm.set_position(z=35, relative=True, speed=20, wait=True)#closing the dispenser with the vial 
        robot.GoTo_Point("Dispenser1", 20)

    def DispenserToScale(self):
        robot.GoTo_Point("DispenserPoint", 60)
        robot.GoTo_Point("Scale", 60)
        robot.arm.set_position(y=130, relative=True, speed=60, wait=True)#moving into the scale
        robot.arm.set_position(z=-39.5, relative=True, speed=30, wait=True)#moving down on the scale 
        robot.arm.set_gripper_position(400, wait=True)

    def ScaleToVialRestPoint(self):
        robot.arm.set_gripper_position(185, wait=True)
        robot.arm.set_position(z=39.5, relative=True, speed=30, wait=True)#moving up on the scale 
        robot.GoTo_Point("Scale", 60)#moving out of the scale
        robot.GoTo_Point("DispenserPoint", 60)#used as inbetween point
        robot.arm.set_linear_track_pos(200, wait=True)
        robot.GoTo_Point("VialRestPoint", 60)
        robot.arm.set_position(z=-127, relative=True, speed=20, wait=True)#going down in the hole
        robot.arm.set_gripper_position(500, wait=True)

    def PickUpPipette(self):
        robot.GoTo_Point("VialRestPoint", 60)
        robot.arm.set_gripper_position(800, wait=False)
        robot.GoTo_Point("PipettePoint", 60)
        robot.arm.set_position(x=-367, y=-215, z=193.2, roll= 90, pitch= 90, yaw=0, speed=20, wait=True) #grabbing pipette
        robot.arm.set_gripper_position(450, wait=True)
        robot.arm.set_position(z=26.8, relative=True, speed=20, wait=True) #lifting pipette
                
    #def PickUpPipetteTip(self):
    #def MoveToBinder(self):
    #
       
        
    
    class VialBox():
        def __init__(self, arm, start_position=(-280, -100, -27.3)):
            self.arm = Robot().arm
            print('in VialBox init')
            self.row_count = 2
            self.column_count = 4
            self.row_spacing = 50  
            self.column_spacing = 40  
            self.start_position = start_position  

        def get_vial_position(self, vial_number): #Vial1(StartPosition) has index 0
            if vial_number == 0:
                return self.start_position
            else:
                row = vial_number // self.column_count
                column = vial_number % self.column_count
                x = self.start_position[0] + column * (self.column_spacing)
                y = self.start_position[1] - row * (self.row_spacing) 
                z = self.start_position[2]
                return x, y, z

        def GoTo_Vial(self, vial_number):
            print('in GoTo_Vial')
            x, y, z = self.get_vial_position(vial_number)
            self.arm.set_position(x=x, y=y, z=z, roll=-152, pitch=88, yaw=120, speed=20, wait=True)


    
robot = Robot()

robot.initialize()
robot.GoTo_InitialPoint()
robot.restart()

robot.PickUpVial0() 
robot.VialToScale() 
robot.ScaleToDispenser1()
robot.DispenserToScale()
robot.ScaleToVialRestPoint()
robot.PickUpPipette()


#PickUpVial0: (should work fine)
robot.arm.set_gripper_position(400, wait=True)
robot.GoTo_Point("VialStoragePoint", 100)
robot.GoTo_Point("Vial0", 60)
robot.arm.set_gripper_position(185, wait=True)#grab vial
robot.GoTo_Point("VialStoragePoint", 60)  

#VialToScale: (should work fine)
robot.arm.set_position(x=-280, y=-100, z=125, roll=-160, pitch=90, yaw=0, speed=60, wait=True)#inbetween point
robot.GoTo_Point("Scale", 60)
robot.arm.set_position(y=130, relative=True, speed=60, wait=True)#moving into the scale
robot.arm.set_position(z=-39.5, relative=True, speed=30, wait=True)#moving down on the scale
robot.arm.set_gripper_position(400, wait=True)

#ScaleToDispenser1: (should work fine)
robot.arm.set_gripper_position(185, wait=True)
robot.arm.set_position(z=39.5, relative=True, speed=30, wait=True)#moving up on the scale
robot.GoTo_Point("Scale", 60)#moving out of the scale 
robot.GoTo_Point("DispenserPoint", 60)
robot.GoTo_Point("Dispenser1", 40)
robot.arm.set_position(z=35, relative=True, speed=20, wait=True)#closing the dispenser with the vial 
robot.GoTo_Point("Dispenser1", 20)

#DispenserToScale:(should work fine)
robot.GoTo_Point("DispenserPoint", 60)
robot.GoTo_Point("Scale", 60)
robot.arm.set_position(y=130, relative=True, speed=60, wait=True)#moving into the scale
robot.arm.set_position(z=-39.5, relative=True, speed=30, wait=True)#moving down on the scale 
robot.arm.set_gripper_position(400, wait=True)

#ScaleToVialRestPoint: (should work fine)
robot.arm.set_gripper_position(185, wait=True)
robot.arm.set_position(z=39.5, relative=True, speed=30, wait=True)#moving up on the scale 
robot.GoTo_Point("Scale", 60)#moving out of the scale
robot.GoTo_Point("DispenserPoint", 60)#used as inbetween point
robot.arm.set_linear_track_pos(200, wait=True)
robot.GoTo_Point("VialRestPoint", 60)
robot.arm.set_position(z=-127, relative=True, speed=20, wait=True)#going down in the hole
robot.arm.set_gripper_position(500, wait=True)

#PickUpPipette:(should work fine)
robot.GoTo_Point("VialRestPoint", 60)
robot.arm.set_gripper_position(800, wait=False)
robot.GoTo_Point("PipettePoint", 60)
robot.arm.set_position(x=-367, y=-215, z=193.2, roll= 90, pitch= 90, yaw=0, speed=20, wait=True) #grabbing pipette
robot.arm.set_gripper_position(450, wait=True)
robot.arm.set_position(z=26.8, relative=True, speed=20, wait=True) #lifting pipette


#Picking up pipette tip (needs still work)
robot.GoTo_Point("PipettePoint", 20)

robot.arm.set_gripper_position(380, wait=True)
x1 = -263.5
y1 = -123.2 
robot.arm.set_position(x=x1, y=y1, z=250, roll= 90, pitch= 91, yaw=0, speed=60, wait=True)
robot.arm.set_position(x=x1, y=y1, z=210, roll= 90, pitch= 91, yaw=0, speed=20, wait=True)
robot.arm.set_position(x=x1, y=y1, z=205, roll= 90, pitch= 91, yaw=0, speed=20, wait=True)
robot.arm.set_position(x=x1, y=y1, z=200, roll= 90, pitch= 91, yaw=0, speed=20, wait=True)
robot.arm.set_position(x=x1, y=y1, z=190, roll= 90, pitch= 91, yaw=0, speed=20, wait=True)
robot.arm.set_position(x=-263.5, y=-123.2, z=320, roll= 90, pitch= 91, yaw=0, speed=20, wait=True)
robot.arm.set_position(x=x1, y=-120.2, z=300, roll= 90, pitch= 91, yaw=0, speed=60, wait=True)
robot.arm.set_position(x=-263.5, y=-123.2, z=300, roll= 90, pitch= 91, yaw=0, speed=20, wait=True)
robot.arm.set_position(x=-263.5, y=-123.2, z=260, roll= 90, pitch= 91, yaw=0, speed=20, wait=True)

#PipetteToVialRestPoint (needs to be checked again)
robot.arm.set_position(x=-367, y=-215, z=193.2, roll= 90, pitch= 90, yaw=0, speed=20, wait=True)
robot.arm.set_gripper_position(800, wait=False)
robot.GoTo_Point("PipettePoint", 60)
robot.GoTo_Point("VialRestPoint", 60)

#VialRestPointToMixer(needs to be checked again)
robot.arm.set_position(x=-367.7, y=-104.2, z=-35, roll= 180, pitch= 90, yaw=0, speed=20, wait=True)
robot.arm.set_gripper_position(185, wait=True)
robot.GoTo_Point("VialRestPoint", 30)
robot.arm.set_position(x=-602, y=-60.2, z=19, roll= 90, pitch= 90, yaw=0, speed=30, wait=True)
robot.arm.set_position(y=-81.8, relative=True, speed=20, wait=True)
robot.arm.set_position(z=-49, relative=True, speed=20, wait=True)
robot.arm.set_gripper_position(480, wait=False)
robot.arm.set_position(y=112, z=49, relative=True speed=30, wait=True)



#Turn on mixer
robot.arm.set_gripper_position(800, wait=False)

robot.arm.set_position(x=-602, y=-30, z=300, roll= 90, pitch= 90, yaw=0, speed=20, wait=True)

robot.arm.set_position(x=-610, y=-82.5, z=307.8, roll= 90, pitch= 90, yaw=0, speed=20, wait=True)

robot.arm.set_gripper_position(500, wait=False)







fixed_points = {
    "InitialPoint": (-228, 0, 133, 180, 90, 0),
    "VialStoragePoint": (-273, -100.5, 125, 90, 90, 0),
    "Vial0": (-273, -100.5, -33, 90, 90, 0),
    "Scale":(-287, 120, 92, -90, 90, 0),
    "DispenserPoint": (-400, 50, 92, 180, 90, 0),
    "Dispenser1": (-537, -98, 40, 180, 90, 0),
    "VialRestPoint": (-367.7, -104.2, 92, 180, 90, 0),
    "PipettePoint": (-370, -110, 250, 90, 90, 0),
    "LiquidStoragePoint": (-275.2, -174, 214.1, -107.4, 88.2, 163.9),
    "Binder": (600, 100, 250, 0, 90, 0),
    "Solvent": (700, -50, 180, 0, 90, 0),
    "Trash": (700, -50, 180, 0, 90, 0),
    "MixerPoint": (-639.3, 0, 317.8, -107.4, 88.2, 163.9),  
       
}
