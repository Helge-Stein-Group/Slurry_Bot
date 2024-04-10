import os
import sys
import time

from xArm_Robot.xarm.wrapper import XArmAPI
from xarm.wrapper import XArmAPI

print(os.getcwd())
print(sys.path)

ip = '192.168.1.240'
arm = XArmAPI(ip, do_not_open=True)

def hangle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))
    
arm.register_error_warn_changed_callback(hangle_err_warn_changed)
arm.connect()

time.sleep(0.5)
if arm.warn_code != 0:
    arm.clean_warn()
if arm.error_code != 0:
    arm.clean_error()

# enabling:
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)
arm.set_gripper_enable(True)
arm.set_gripper_mode(0)

arm.set_initial_point([0, 0, 0, -180, 90, 0])

#Setting boundry fence
x_max, x_min, y_max, y_min, z_max, z_min = 700, -200, 900, -700, 500, -400
arm.set_reduced_tcp_boundary([x_max, x_min, y_max, y_min, z_max, z_min])
arm.set_fense_mode(True)

arm.set_servo_angle(angle=[0, 0, 0, -180, 90, 0], speed=20, wait=True)

def GoToInitialPosition():
    arm.set_position(x=400, y=0, z=133, roll=0, pitch=90, yaw=0, speed=120, wait=True)

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











#For remebering the trajectory
arm = XArmAPI(ip, is_radian=True)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

