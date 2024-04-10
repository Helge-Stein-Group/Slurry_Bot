import time

from xarm.wrapper import XArmAPI

#;aybe I should put this on a .json file later
ipAddress = '192.168.1.240'
points = {
    'Name': 'VialStorage',
    'x' : 500,
    'y' : 0,
    'z' : 200}


print(points['VialStorage'])

#Do we need this section?
def hangle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))

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

    def GoToVialPickUp(self, vialNum):
        self.arm.set_gripper_position(550, wait=True)
        self.arm.set_position(x=)


        arm.set_position(x=500, y=0, z=200, roll=0, pitch=90, yaw=0, speed=20, wait=True)
        arm.set_gripper_position(460, wait=True)
        arm.set_position(x=365, y=470, z=450, roll=0, pitch=90, yaw=0, speed=20, wait=True)
        arm.set_position(x=365, y=470, z=350, roll=0, pitch=90, yaw=0, speed=20, wait=True)






def PickupPipette():
    arm.set_gripper_position(800, wait=True)
    arm.set_position(x=500, y=0, z=200, roll=0, pitch=90, yaw=0, speed=20, wait=True)
    arm.set_gripper_position(460, wait=True)
    arm.set_position(x=365, y=470, z=450, roll=0, pitch=90, yaw=0, speed=20, wait=True)
    arm.set_position(x=365, y=470, z=350, roll=0, pitch=90, yaw=0, speed=20, wait=True)

def VialPickUp():
    arm.set_gripper_position(500, wait=True, speed=700)
    arm.set_position(x=395, y=476, z=200, roll=0, pitch=90, yaw=0, speed=110, wait=True)
    arm.set_position(x=395, y=476, z=70, roll=0, pitch=90, yaw=0, speed=20, wait=True)
    arm.set_gripper_position(205, wait=True)
    time.sleep(1)
    arm.set_position(x=395, y=476, z=200, roll=0, pitch=90, yaw=0, speed=50, wait=True)


def VialToScale():
    arm.set_position(x=300, y=-400, z=200, roll=0, pitch=90, yaw=-90, speed=120, wait=True)
    arm.set_position(x=-20, y=-550, z=200, roll=0, pitch=90, yaw=-90, speed=120, wait=True)
    arm.set_position(x=-20, y=-627, z=200, roll=0, pitch=90, yaw=-90, speed=60, wait=True)
    arm.set_position(x=-20, y=-627, z=159, roll=0, pitch=90, yaw=-90, speed=20, wait=True)
    arm.set_gripper_position(500, wait=True)


def ScaleToDispenser():
    arm.set_gripper_position(205, wait=True)
    arm.set_position(x=-20, y=-627, z=200, roll=0, pitch=90, yaw=-90, speed=60, wait=True)
    arm.set_position(x=-20, y=-550, z=200, roll=0, pitch=90, yaw=-90, speed=120, wait=True)
    arm.set_position(x=400, y=-400, z=200, roll=0, pitch=90, yaw=-90, speed=120, wait=True)
    arm.set_position(x=170, y=735, z=90, roll=0, pitch=90, yaw=90, speed=80, wait=True)
    arm.set_position(x=170, y=835, z=90, roll=0, pitch=90, yaw=90, speed=20, wait=True)
    time.sleep(1)


def DispenserToScale():
    arm.set_position(x=170, y=735, z=90, roll=0, pitch=90, yaw=90, speed=20, wait=True)
    arm.set_position(x=300, y=483, z=133, roll=0, pitch=90, yaw=0, speed=120, wait=True)
    arm.set_position(x=400, y=-400, z=200, roll=0, pitch=90, yaw=-90, speed=120, wait=True)
    arm.set_position(x=-21, y=-627, z=200, roll=0, pitch=90, yaw=-90, speed=80, wait=True)
    arm.set_position(x=-21, y=-627, z=159, roll=0, pitch=90, yaw=-90, speed=20, wait=True)
    arm.set_gripper_position(500, wait=True)


def ScaleToVialHolder():
    arm.set_gripper_position(205, wait=True)
    arm.set_position(x=-20, y=-627, z=200, roll=0, pitch=90, yaw=-90, speed=80, wait=True)
    arm.set_position(x=300, y=-400, z=200, roll=0, pitch=90, yaw=-90, speed=120, wait=True)
    arm.set_position(x=395, y=476, z=200, roll=0, pitch=90, yaw=0, speed=120, wait=True)
    arm.set_position(x=395, y=476, z=70, roll=0, pitch=90, yaw=0, speed=20, wait=True)
    arm.set_gripper_position(500, wait=True)
    time.sleep(1)
    arm.set_position(x=394, y=475, z=200, roll=0, pitch=90, yaw=0, speed=50, wait=True)

def GoToInitialPosition():
    arm.set_position(x=400, y=0, z=133, roll=0, pitch=90, yaw=0, speed=120, wait=True)



scale.tare() 
VialPickUp()
VialToScale()
scale.tare()
time.sleep(5)
ScaleToDispenser()
motor.move(500)
time.sleep(9)
DispenserToScale()
weight1 = scale.getWeight()
time.sleep(5)
ScaleToVialHolder()
GoToInitialPosition()

print("The weight was: "+str(weight1)+"g")


def Test():
    GoToInitialPosition()
    VialPickUp()
    VialToScale()
    PickUpVialScale()
    ScaleToDispenser()
    DispenserToScale()
    PickUpVialScale()
    ScaleToVialHolder()
    GoToInitialPosition()

Test()

arm.set_gripper_position(205, wait=True)
arm.set_position(x=387, y=484, z=133, roll=0, pitch=90, yaw=0, speed=50, wait=True)
arm.set_position(x=387, y=484, z=70, roll=0, pitch=90, yaw=0, speed=10, wait=True)
arm.set_gripper_position(400, wait=True)










arm.set_gripper_position(400, wait=True)
arm.set_position(x=380, y=483, z=150, roll=0, pitch=90, yaw=0, speed=10, wait=True)
arm.set_servo_angle(angle=[0, 0, 0, -180, 90, 0], speed=10, wait=True)

arm.set_position(x=380, y=483, z=133, roll=0, pitch=90, yaw=0, speed=20, wait=True)


paths = [
    [400, 200, 133, 0, 90, 0],
    [300, 200, 133, 0, 90, 0],
    [400, 483, 133, 0, 90, 0],
]

arm.set_position(*paths[0], speed=10, wait=True)




arm.set_servo_angle(angle=[0, 0, 0, 0, -90, 0], speed=30, wait=True)
arm.set_servo_angle(angle=[45, 0, 0, 0, -90, 0], speed=30, wait=True)

arm.get_position()






arm.set_position(x=400, y=600, z=200, roll=0, pitch=-90, yaw=-90, speed=50, wait=True)

arm.set_position(x=000, y=500, z=200, roll=0, pitch=-90, yaw=-180, speed=30, wait=True)

arm.set_position(x=400, y=400, z=200, roll=0, pitch=-90, yaw=-90, speed=30, wait=True)

arm.set_position(x=100, y=0, z=150, roll=-180, pitch=0, yaw=0, speed=50, wait=True)


arm.set_position(x=20, y=-300, z=50, roll=-180, pitch=0, yaw=0, speed=50, wait=True)

time.sleep(10)

#For remebering the trajectory
arm = XArmAPI(ip, is_radian=True)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)