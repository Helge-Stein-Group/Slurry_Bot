from Dispensing_wrapper_robot import *

# Define your parameters
acceleration = 10
speed = 5
material = "SuperP"
version_inside = "Design4"
version_outside = "Design1"
dispenser_motor = "motor"
scale = "scale"
robot = "robot"

my_calibration = Calibration(acceleration, speed, material, version_inside, version_outside, dispenser_motor, scale, robot)
my_calibration.test_function()