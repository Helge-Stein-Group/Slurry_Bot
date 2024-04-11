import time
from xarm.wrapper import XArmAPI

#maybe I should put this on a .json file later
ipAddress = '192.168.1.240'


#Do we need this section?
def hangle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))

fixed_points = {
    "InitialPoint": (500, 0, 200, 0, 90, 0),
    "VialStoragePoint": (500, 0, 200, 0, 90, 0),
    "Scale":(600, 100, 250, 0, 90, 0),
    "DispenserPoint": (600, 100, 250, 0, 90, 0),
    "Dispenser1": (700, -50, 180, 0, 90, 0),
    "VialRestPoint": (600, 100, 250, 0, 90, 0),
    "PipettePoint": (600, 100, 250, 0, 90, 0),
    "TipsStoragePoint": (700, -50, 180, 0, 90, 0), 
    "LiquidStoragePoint": (600, 100, 250, 0, 90, 0),
    "Binder": (600, 100, 250, 0, 90, 0),
    "Solevnt": (700, -50, 180, 0, 90, 0),
    "Trash": (700, -50, 180, 0, 90, 0),
    "MixerPoint": (700, -50, 180, 0, 90, 0),     
}

class Robot():
    def _init_(self, ip):
        self.arm = XArmAPI(ip, do_not_open=True)
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_gripper_enable(True)
        self.arm.set_gripper_mode(0)
        self.arm.set_initial_point([0, 0, 0, -180, 90, 0])
        self.arm.register_error_warn_changed_callback(hangle_err_warn_changed)
        self.arm.connect()

    def close(self):
        self.arm.disconnect()
    
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
    
    def VialToMixer(self):
        

#Testing stuff
#Getting position of vials:

    class VialBox:
        def __init__(self, start_position=(365, 470, 450)):
            self.row_count = 2
            self.column_count = 4
            self.row_spacing = 1  
            self.column_spacing = 1  
            self.start_position = start_position  

        def get_vial_position(self, vial_number): #Vial1(StartPosition) has index 0
            row = vial_number // self.column_count
            column = vial_number % self.column_count
            x = self.start_position[0] + column * (self.column_spacing)  # Berechnung der Position in x-Richtung
            y = self.start_position[1] - row * (self.row_spacing)  # Berechnung der Position in y-Richtung
            z = self.start_position[2]
            return x, y, z

        def GoTo_Vial(self, vial_number, arm):
            x, y, z = self.get_vial_position(vial_number)
            arm.set_position(x=x, y=y, z=z, roll=0, pitch=90, yaw=0, speed=20, wait=True)

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
            arm.set_position(x=x, y=y, z=z, roll=0, pitch=90, yaw=0, speed=20, wait=True)

#For remebering the trajectory
arm = XArmAPI(ip, is_radian=True)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)