import os
import sys
import time

from xarm.wrapper import XArmAPI
from Robot_wrapper import Robot


arm.connect()

time.sleep(0.5)
if arm.warn_code != 0:
    arm.clean_warn()
if arm.error_code != 0:
    arm.clean_error()

