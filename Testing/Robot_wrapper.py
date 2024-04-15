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
    
    def PickUpVial(self):
        robot.arm.set_gripper_position(400, wait=True)
        robot.GoTo_Point("VialStoragePoint", 100)
        robot.GoTo_Point("Vial0", 60)
        robot.arm.set_gripper_position(185, wait=True)
        robot.GoTo_Point("VialStoragePoint", 60)  

    def VialToScale(self):
        self.arm.GoTo_point("scale")
        self.arm.set_position(x=300, y=-400, z=200, roll=0, pitch=90, yaw=-90, speed=120, wait=True)
        self.arm.set_position(x=-20, y=-550, z=200, roll=0, pitch=90, yaw=-90, speed=120, wait=True)
        self.arm.set_gripper_position(500, wait=True)

    def ScaleToDispenser(self, Dispensername):
        self.arm.set_gripper_position(205, wait=True)
        self.arm.set_position(x=-20, y=-627, z=200, roll=0, pitch=90, yaw=-90, speed=60, wait=True)
        self.arm.set_position(x=-20, y=-550, z=200, roll=0, pitch=90, yaw=-90, speed=120, wait=True)
        self.arm.GoTo_point("DispenserPoint")
        self.arm.GoTo_point(Dispensername)
        self.arm.GoTo_point("DispenserPoint")

    def DispenserToScale(self):
        self.arm.GoTo_point("Scale")
        self.arm.set_gripper_position(500, wait=True)

    def ScaleToVialRestPoint(self):
        self.arm.set_gripper_position(205, wait=True)
        self.arm.GoTo_point("VialRestPoint")
        self.arm.set_gripper_position(500, wait=True)
        time.sleep(1)
        self.arm.GoTo_point("VialRestPoint")

    def PickUpPipette(self):
        self.arm.GoTo_point("PipettePoint")
        self.arm.set_position(x=500, y=0, z=200, roll=0, pitch=90, yaw=0, speed=20, wait=True)
        self.arm.set_gripper_position(260, wait=True)
        self.arm.GoTo_point("PipettePoint")

    def GoToLiquid(self, Liquidname):
        self.arm.GoTo_point("LiquidStoragePoint")
        self.arm.GoTo_point(Liquidname)
    
    def LiquidToVial (self):
        self.arm.GoTo_point("VialRestPoint")
    
    def Trash(self):
        self.arm.GoTo_point("Trash")
    
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

#Getting position of tips:
    class Tips():
        def __init__(self, start_position=(365, 470, 450)):
            self.row_count = 5
            self.column_count = 8
            self.row_spacing = 0.5
            self.column_spacing = 0.5
            self.start_position = start_position

        def get_tip_position(self, tip_number):
            row = tip_number // self.column_count
            column = tip_number % self.column_count
            x = self.start_position[0] + column * self.column_spacing
            y = self.start_position[1] - row * self.row_spacing
            z = self.start_position[2]
            return x, y, z

        def GoTo_Tip(self, tip_number, arm):
            x, y, z = self.get_tip_position(tip_number)
            self.arm.set_position(x=x, y=y, z=z, roll=0, pitch=90, yaw=0, speed=20, wait=True)

    class Inner():
        def __init__(self):
            print('in Inner init')
            self.outer = Robot().arm
            print('self.outer')

        def printing(self):
            print('In prinitng mode')
    
    def callinner(self):
        self.newinner.printing()
        print('called inner')


robot = Robot()

robot.initialize()
robot.GoTo_InitialPoint()
robot.restart()

robot.PickUpVial()  

#VialToScale
robot.arm.set_position(x=-280, y=-100, z=125, roll=-160, pitch=90, yaw=0, speed=60, wait=True)
robot.GoTo_Point("Scale", 60)
robot.arm.set_position(x=-287, y=250, z=92, roll=-90, pitch=90, yaw=0, speed=60, wait=True)
robot.arm.set_position(x=-287, y=250, z=52.5, roll=-90, pitch=90, yaw=0, speed=30, wait=True)
robot.arm.set_gripper_position(400, wait=True)

#ScaleTODispenser
robot.arm.set_gripper_position(185, wait=True)
robot.arm.set_position(x=-287, y=250, z=92, roll=-90, pitch=90, yaw=0, speed=60, wait=True)
robot.GoTo_Point("Scale", 60)
robot.GoTo_Point("DispenserPoint", 60)
robot.GoTo_Point("Dispenser1", 40)
robot.arm.set_position(x=-537, y=-98, z=75, roll= 180, pitch= 90, yaw=0, speed=20, wait=True)
robot.GoTo_Point("Dispenser1", 20)

#DispenserToRestPoint
robot.GoTo_Point("DispenserPoint", 60)
robot.arm.set_linear_track_pos(200, wait=True)
robot.GoTo_Point("VialRestPoint", 60)
robot.arm.set_position(x=-367.7, y=-104.2, z=-35, roll= 180, pitch= 90, yaw=0, speed=20, wait=True)
robot.arm.set_gripper_position(500, wait=True)

#From rest to Picking up Pipette
robot.GoTo_Point("VialRestPoint", 60)
robot.arm.set_gripper_position(800, wait=False)
robot.GoTo_Point("PipettePoint", 60)
robot.arm.set_position(x=-367, y=-215, z=193.2, roll= 90, pitch= 90, yaw=0, speed=20, wait=True) #grabbing pipette
robot.arm.set_gripper_position(450, wait=True)
robot.arm.set_position(x=-367, y=-212, z=220, roll= 90, pitch= 90, yaw=0, speed=20, wait=True) #lifting pipette

#Picking up pipette tip
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

#Pipette to Vial Rest Point
robot.arm.set_position(x=-367, y=-215, z=193.2, roll= 90, pitch= 90, yaw=0, speed=20, wait=True)
robot.arm.set_gripper_position(800, wait=False)
robot.GoTo_Point("PipettePoint", 60)
robot.GoTo_Point("VialRestPoint", 60)

#Vial Rest Point to Mixer Point
robot.arm.set_position(x=-367.7, y=-104.2, z=-35, roll= 180, pitch= 90, yaw=0, speed=20, wait=True)
robot.arm.set_gripper_position(185, wait=True)
robot.GoTo_Point("VialRestPoint", 30)
robot.arm.set_position(x=-602, y=-60.2, z=19, roll= 90, pitch= 90, yaw=0, speed=30, wait=True)
robot.arm.set_position(x=-602, y=-142, z=19, roll= 90, pitch= 90, yaw=0, speed=20, wait=True)
robot.arm.set_position(x=-602, y=-142, z=-30, roll= 90, pitch= 90, yaw=0, speed=20, wait=True)
robot.arm.set_gripper_position(480, wait=False)
robot.arm.set_position(x=-602, y=-30, z=19, roll= 90, pitch= 90, yaw=0, speed=30, wait=True)



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



#    "PipettePoint": (-370, -110, 193.2, -107.4, 90, 163.9),