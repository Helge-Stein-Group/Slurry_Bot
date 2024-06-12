# SlurryBot 🔋🤖🧪

The SlurryBot system automates the dispensing, weighing, and mixing of electrode slurries for battery production. It forms a component of a larger automated pouch cell assembly system currently under development by the Digital Catalysis Group at the Technical University of Munich, under the supervision of Prof. Helge Stein. This document serves as a comprehensive guide for constructing and operating the SlurryBot system.

<img src="https://github.com/Helge-Stein-Group/Slurry_Bot/blob/3c1a557d6fe76c7eba93cc6abedd6eded894a3c7/slurry_robot_system.png" height="400"/>

#### Table of Contents  
[XArm Robot](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/main/README.md#xarm-robot)<br />
[Motors and Wiring](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/main/README.md#motors-and-wiring)<br />
[Scale Setup for a Sartorius Secura](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/main/README.md#scale-setup-for-a-sartorius-secura)<br />
[Pipette Control for a Sartorius rLINE](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/main/README.md#pipette-control-for-a-sartorius-rline)<br />
[Dispensing Model Assembly](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/main/README.md#dispensing-model-assembly)

## XArm Robot

The six-axis XArm robot is responsible for the movement of vials, pipetting, and other physical tasks within the automated system. The robot can be controlled using the Python driver provided by the manufacturer.

### Getting Started 

#### Setup

1. Follow the hardware setup directions provided in the manual. A manual for the xArm 6 can be found [here](https://www.ufactory.cc/wp-content/uploads/2023/05/xArm-User-Manual-V2.0.0.pdf).
2. Ensure that your IP address is set correctly to 192.168.1.*.
3. In your terminal run `pip install xArm-Python-SDK`
4. Clone this whole repository and run the robot testing code in the begining of the testing_ground.ipynb file.

## Motors and Wiring

This section provides an overview of the wiring and motor control within the system. The motor driver enables communication via a serial port USB connection, allowing control of up to six NEMA 17 or 23 stepper motors, all connected to a single Arduino Nano.

### Getting Started

#### Wiring of NEMA 17

The NEMA 17 motor can be operated using an A4988 driver and a 9-volt power supply. Ensure that the switches on the A4988 driver are in the off position, then wire the motor, Arduino, and driver together according to the diagram below. In this diagram, the Arduino pins D2 and D3 are connected to the driver's S and D pins, respectively, meaning in the Python code, this motor would be referred to as motor 0. Motor 1 would be wired to pins D4 and D5, Motor 2 to pins D6 and D7, and so on.

<img src="https://github.com/Helge-Stein-Group/Slurry_Bot/assets/148461262/1e0f1947-3164-45df-9854-c35ab379af1b" width="500" height="500"/>

#### Wiring of NEMA 23

The NEMA 23 is a larger and more powerful motor which is operated with a TB6600 motor driver and a 12 volt power supply. (ADD WIRING DIAGRAM HERE AND DISCRIBE)

<img src="https://github.com/Helge-Stein-Group/Slurry_Bot/blob/35829d3e5a5cdf57512fba0788122d6e9e0ffcd1/wiring_diagram_2.jpeg" width="500" height="500"/>

### Arduino Setup

1. Download the file [motor_driver.py](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/14724c3a567890dc80b1c11155cd3a25eb4a3e9f/Drivers/motor_driver.py).
2. Plug your Arduino Nano into your computer.
3. Download the [Arduino IDE software](https://www.arduino.cc/en/software).
4. In the Library Manager make sure to install the AccelStepper.h library. 
5. Copy the code in the file [arduino_motor_code.ino](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/14724c3a567890dc80b1c11155cd3a25eb4a3e9f/Drivers/arduino_motor_code.ino) into the Arduino IDE editor and compile and upload the code to your arduino.
6. **If the code will not upload, try going to the Tools tab ans switching the Processor to the Old Bootloader.**
7. Once your code has properly compiled and uploaded to your arduino then you are ready to run the python driver.

### Python Setup

1. Connect your computer to the Arduino via a USB cable. (If it is not already connected.)
2. Confirm the COM Port of your connection using the device manager.
3. To test the setup you should open a file and run the testing code in the example section below.


## Features

### Max Speed and Acceleration

You can set the max speed using `setSpeed()` and I would recommend a speed around 70. To set the acceleration use `setAcceleration()`.

### Moving the Motor

To get a simple movement of the motor use `move()`. The integer value that you give this function will determine the number of steps the motor takes. For example, if you would like it to make a full circle use `move(200)`. When opperating the linear rail you can use the functions `moveUp()` and `moveDown()`. The motor can be stopped using the `stop()` function.

## Example

```python

from motor_driver import Motor

motors = SerialConnection('COM1', 9600, 10) #add your specific com port here
motor_1 = Motor(motors, 0)
motor_1.check_connection()
motor_1.setAcceleration(10)
motor_1.setSpeed(100)
motor_1.move(100)
motor_1.close()

```

## Scale Setup for a Sartorius Secura 

This setup and driver give you the ability to communicate with a Sartorius brand Secura scale through a serial port USB connection.

The manual for this scale can be found [here](https://www.ricelake.com/media/nwmbmkzb/m_sartorius_user_manual_secura_quintix_practum.pdf).

### Getting Started

#### Scale Settings

1. Insure that under "USB Port" setting the device protocol is set to PC-SBI. 
2. Set the "Printout" status to manual with stability.
3. Confirm that in the "Calibration/Adjustment" settings section isoCAL is set to "Info, manual start."

#### Setup

1. Turn on scale and manually level.
2. Connect the scale via a USB cable.

### Features

- Communicate with the scale to get weight measurements
- Process scale responses and raw data
- Configure the scale settings
- Error handling for scale communication

#### Tare and Calibration

To tare the scale use `tare()` and to preform an internal callibration use `intCal()`.

#### Measuring

To get a simple weight measurement use the `measure()` or `measure_stable()` functions. 

### Example

```python

from scale_driver import Scale

my_scale = Scale('COM7',9600,timeout=3) # Adjust these to your specific system
my_scale.tare()
my_scale.measure()

```

## Pipette Control for a Sartorius rLINE

EDIT THIS! This is the driver to the pippeting robot rLINE® 1-ch 200 µl dispensing module from Sartorius. The hardware is connected to your PC via USB-B

For a quick start, refer to the script "rLine.py", you will first need to correctlly configure the port of your setup and put it into the script.

The hardware need to initiate a connection with your PC everytime it starts up. Use the initiate_rline function to establisch the connection, usually it will take a couple of seconds.

The most useful functions you would use are:

aspirate
dispense
clear_and_reset
reset
blowout
eject
disconnect_pipette
After usage, you need to run disconnect_pipette function to properly disconnect the pipette.

## Dispensing Model Assembly


## Contact

Leah Nuss - leah.nuss@tum.de <br/>
Danika Heaney - danika.heaney@tum.de <br/>
Helge Stein - helge.stein@tum.de

## Acknowledgements

The scale driver code was modeled after [sartoriususb](https://github.com/holgi/sartoriusb).
