import time
from xarm.wrapper import XArmAPI

#maybe I should put this on a .json file later
ip = '192.168.1.200'

#This function is called when the error or warning code changes
def hangle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))


fixed_points = {
    "InitialPoint": (-228, 0, 133, 0, 90, 180),
    "VialStoragePoint": (-273, -100.5, 125, -160, 90, 110),
    "Vial0": (-273, -100.5, -33, -160, 90, 110),
    "Scale":(-287, 120, 92, -150, 90, -60),
    "DispenserPoint": (-419.3, 104.5, 92, -64.9, 90, -106),
    "Dispenser1": (-532.4, -96.8, 56.1, 127.7, 88.8, -52.4),
    "VialRestPoint": (-363.6, -105.4, 35.8, 127.7, 88.8, -52.4),
    "PipettePoint": (-497.3, -116.5, 192.5, -107.4, 88.2, 163.9),
    "LiquidStoragePoint": (-275.2, -174, 214.1, -107.4, 88.2, 163.9),
    "Binder": (600, 100, 250, 0, 90, 0),
    "Solvent": (700, -50, 180, 0, 90, 0),
    "Trash": (700, -50, 180, 0, 90, 0),
    "MixerPoint": (-639.3, 0, 317.8, -107.4, 88.2, 163.9),     
}
#Vial0(x=-283.4, y=-100, z=-31.2, roll=-152.4, pitch=88.8, yaw=120.6, speed=20, wait=True)
#GripperVialClose:185 Open:290, 
#Rail Pos.:600mm (till Dispenser 1)
#Rail Pos.:200mm
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
    
    def PickUpVial(self, vialnumber):
        robot.arm.set_gripper_position(500, wait=True)
        robot.GoTo_Point("VialStoragePoint", 100)
        robot.GoTo_Point("Vial0", 30)
        robot.arm.set_gripper_position(185, wait=True)
        robot.GoTo_Point("VialStoragePoint", 30)   

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

#PickUpVial0
robot.initialize()
robot.GoTo_InitialPoint()

robot.restart()

#PickUpVial0
robot.arm.set_gripper_position(500, wait=True)
robot.GoTo_Point("VialStoragePoint", 100)
robot.GoTo_Point("Vial0", 60)
robot.arm.set_gripper_position(185, wait=True)
robot.GoTo_Point("VialStoragePoint", 60)    

#VialToScale
robot.arm.set_position(x=-280, y=-100, z=125, roll=-160, pitch=90, yaw=0, speed=60, wait=True)
robot.GoTo_Point("Scale", 60)
robot.arm.set_position(x=-287, y=250, z=92, roll=-150, pitch=90, yaw=-60, speed=60, wait=True)
robot.arm.set_position(x=-287, y=250, z=52.5, roll=-150, pitch=90, yaw=-60, speed=30, wait=True)
robot.arm.set_gripper_position(500, wait=True)

#ScaleTODispenser
robot.arm.set_gripper_position(185, wait=True)
robot.arm.set_position(x=-287, y=250, z=92, roll=-150, pitch=90, yaw=-60, speed=60, wait=True)
robot.GoTo_Point("Scale", 60)
robot.GoTo_Point("DispenserPoint", 60)
robot.GoTo_Point("Dispenser1", 40)
robot.arm.set_position(x=-537, y=-98, z=75, roll= 127.7, pitch= 90, yaw=-52.4, speed=20, wait=True)
robot.GoTo_Point("Dispenser1", 20)


#DispenserToRestPoint
robot.GoTo_Point("DispenserPoint", 60)
robot.arm.set_linear_track_pos(200, wait=True)
robot.GoTo_Point("VialRestPoint", 60)
robot.arm.set_position(x=-367.7, y=-104.2, z=-35, roll= 127.7, pitch= 90, yaw=-52.4, speed=20, wait=True)
robot.arm.set_gripper_position(500, wait=True)

#From rest to Picking up Pipette
robot.GoTo_Point("VialRestPoint", 60)
robot.arm.set_gripper_position(800, wait=False)
robot.GoTo_Point("PipettePoint", 60)
robot.arm.set_position(x=-420, y=-215, z=193.2, roll= -107.4, pitch= 90, yaw=163.9, speed=20, wait=True) #grabbing pipette
robot.arm.set_gripper_position(480, wait=True)
robot.arm.set_position(x=-420, y=-215, z=220, roll= -107.4, pitch= 90, yaw=163.9, speed=20, wait=True) #lifting pipette

#Pipette to Vial Rest Point
robot.arm.set_position(x=-420, y=-215, z=193.2, roll= -107.4, pitch= 90, yaw=163.9, speed=20, wait=True)
robot.arm.set_gripper_position(800, wait=False)
robot.GoTo_Point("PipettePoint", 60)
robot.GoTo_Point("VialRestPoint", 60)

#Vial Rest Point to Mixer Point
robot.arm.set_position(x=-367.7, y=-104.2, z=-35, roll= 127.7, pitch= 90, yaw=-52.4, speed=20, wait=True)
robot.arm.set_gripper_position(185, wait=True)
robot.GoTo_Point("VialRestPoint", 30)


robot.GoTo_Point("MixerPoint", 20)
robot.arm.set_position(x=-420, y=20, z=40, roll= -18, pitch= 88.2, yaw=163.9, speed=20, wait=True)
robot.arm.set_linear_track_pos(20, wait=True)




robot.arm.set_position(x=-660, y=-90, z=17, roll= -107.4, pitch= 90, yaw=163.9, speed=20, wait=True)


-497.3, -116.5, 192.5, -107.4, 88.2, 163.9

robot.arm.set_position(x=-410, y=-119, z=192.5, roll= -107.4, pitch= 90, yaw=163.9, speed=20, wait=True)
robot.arm.set_position(x=-420, y=-215, z=193.2, roll= -107.4, pitch= 90, yaw=163.9, speed=20, wait=True)
robot.arm.set_position(x=-420, y=-215, z=220, roll= -107.4, pitch= 90, yaw=163.9, speed=20, wait=True)


robot.arm.set_position(x=-367.7, y=-104.2, z=-35, roll= 127.7, pitch= 90, yaw=-52.4, speed=20, wait=True)


robot.arm.set_position(x=-287, y=120, z=92, roll= -150, pitch= 90, yaw=-60, speed=40, wait=True)

robot.arm.set_position(x=-400, y=50, z=92, roll= 120, pitch= 90, yaw=-60, speed=40, wait=True) #DispenserPoint

robot.arm.set_position(x=-537, y=-97.5, z=40, roll= 127.7, pitch= 90, yaw=-52.4, speed=40, wait=True)
robot.arm.set_position(x=-537, y=-98, z=75, roll= 127.7, pitch= 90, yaw=-52.4, speed=20, wait=True)




fixed_points = {
    "InitialPoint": (-228, 0, 133, 0, 90, 180),
    "VialStoragePoint": (-273, -100.5, 125, -160, 90, 110),
    "Vial0": (-273, -100.5, -33, -160, 90, 110),
    "Scale":(-287, 120, 92, -150, 90, -60),
    "DispenserPoint": (-400, 50, 92, 120, 90, -60),
    "Dispenser1": (-537, -98, 40, 127.7, 90, -52.4),
    "VialRestPoint": (-367.7, -104.2, 92, 127.7, 90, -52.4),
    "PipettePoint": (-420, -110, 193.2, -107.4, 90, 163.9),
    "LiquidStoragePoint": (-275.2, -174, 214.1, -107.4, 88.2, 163.9),
    "Binder": (600, 100, 250, 0, 90, 0),
    "Solvent": (700, -50, 180, 0, 90, 0),
    "Trash": (700, -50, 180, 0, 90, 0),
    "MixerPoint": (-639.3, 0, 317.8, -107.4, 88.2, 163.9),     
}