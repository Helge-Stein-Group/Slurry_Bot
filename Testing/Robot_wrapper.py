import time
from xarm.wrapper import XArmAPI

#maybe I should put this on a .json file later
ip = '192.168.1.200'

#This function is called when the error or warning code changes
def hangle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))


fixed_points = {
    "InitialPoint": (-228, 0, 133, 0, 90, 180),
    "VialStoragePoint": (-280, -100, 125, -152, 88, 120),
    "Scale":(-291.9, 104.6, 92, -152.4, 88.8, -61.6),
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
    def __init__(self, ip):
        self.arm = XArmAPI(ip)
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_gripper_enable(True)
        self.arm.set_gripper_mode(0)
        self.arm.set_linear_track_back_origin(wait=True)
        self.arm.set_linear_track_enable(True)
        self.arm.set_linear_track_speed(500)
        self.arm.set_initial_point([-228, 0, 133, 0, 90, 180])
        self.arm.register_error_warn_changed_callback(hangle_err_warn_changed)
        self.arm.connect()

    def close(self):
        self.arm.disconnect()

    def GoTo_InitialPoint(self):
        self.arm.set_linear_track_pos(600, wait=True)
        self.arm.set_position(x=-228, y=0, z=133, roll=0, pitch=90, yaw=180, speed=20, wait=True)

    def GoTo_Point(self, name, speed, wait=True):
        position = fixed_points[name]
        self.arm.set_position(x=position[0], y=position[1], z=position[2], roll=position[3], pitch=position[4], yaw=position[5], speed=speed, wait=wait)
    
    def PickUpVial(self, vialnumber):
        self.arm.set_gripper_position(550, wait=True)
        self.arm.GoTo_Point("VialStoragePoint", 20)
        self.arm.GoTo_Tip(vialnumber)
        self.arm.set_gripper_position(205, wait=True)
        time.sleep(1)
        self.arm.set_position(x=365, y=470, z=450, roll=0, pitch=90, yaw=0, speed=20, wait=True)
        self.arm.GoTo_Point("VialStoragePoint", 20)

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
    
    class VialBox:
        def __init__(self, start_position=(-280, -100, -27.3)):
            self.row_count = 2
            self.column_count = 4
            self.row_spacing = 1  
            self.column_spacing = 1  
            self.start_position = start_position  

        def get_vial_position(self, vial_number): #Vial1(StartPosition) has index 0
            if vial_number == 0:
                return self.start_position
            else:
                row = vial_number // self.column_count
                column = vial_number % self.column_count
                x = self.start_position[0] + column * (self.column_spacing)  # Berechnung der Position in x-Richtung
                y = self.start_position[1] - row * (self.row_spacing)  # Berechnung der Position in y-Richtung
                z = self.start_position[2]
                return x, y, z

        def GoTo_Vial(self, vial_number):
            x, y, z = self.get_vial_position(vial_number)
            self.arm.set_position(x=x, y=y, z=z, roll=-152, pitch=88, yaw=120, speed=20, wait=True)

#Getting position of tips:
    class Tips:
        def __init__(self, start_position=(365, 470, 450)):
            self.row_count = 5
            self.column_count = 8
            self.row_spacing = 0.5  # Spacing zwischen den Reihen
            self.column_spacing = 0.5  # Spacing zwischen den Spalten
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

Test = Robot(ip)
Test.GoTo_InitialPoint()
Test.arm.set_gripper_position(550, wait=True)
Test.GoTo_Point("VialStoragePoint", 20)
Test.GoTo_Vial(0)
Test.arm.set_gripper_position(205, wait=True)
time.sleep(1)
Test.arm.set_position(x=365, y=470, z=450, roll=0, pitch=90, yaw=0, speed=20, wait=True)
Test.GoTo_Point("VialStoragePoint", 20)           