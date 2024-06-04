# SlurryBot 🔋🤖🧪

The SlurryBot system automates the dispensing, weighing, and mixing of electrode slurries for battery production. It forms a component of a larger automated pouch cell assembly system currently under development by the Digital Catalysis Group at the Technical University of Munich, under the supervision of Prof. Helge Stein. This document serves as a comprehensive guide for constructing and operating the SlurryBot system.

#### Table of Contents  
[XArm Robot](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/main/README.md#xarm-robot)<br />
[Motors and Wiring](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/main/README.md#motors-and-wiring)<br />
[Scale Setup for a Sartorius Secura](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/main/README.md#scale-setup-for-a-sartorius-secura)<br />
[Pipette Control for a Sartorius rLINE](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/main/README.md#pipette-control-for-a-sartorius-rline)<br />
[Dispensing Model Assembly](https://github.com/Helge-Stein-Group/Slurry_Bot/blob/main/README.md#dispensing-model-assembly)

## XArm Robot
## Motors and Wiring

This section provides an overview of the wiring and motor control within the system. The motor driver enables communication via a serial port USB connection, allowing control of up to six NEMA 17 or 23 stepper motors, all connected to a single Arduino Nano.

### Getting Started

#### Wiring of NEMA 17

The NEMA 17 motor can be run using a A
Please wire the motor, arduino, and driver together using the diagram below.

![wiring_diagram](https://github.com/Helge-Stein-Group/Slurry_Bot/assets/148461262/1e0f1947-3164-45df-9854-c35ab379af1b)

#### Wiring of NEMA 23

Insure that the switches on the A4988 driver are in the off position and the pins D3 and D2 are wired to the driver at D and S, respectively.

### Arduino Setup

1. Plug your Arduino Nano into your computer.
2. Download the [Arduino IDE software](https://www.arduino.cc/en/software).
3. In the Library Manager make sure to install the AccelStepper.h library. 
4. Copy the code in the file [arduino_motor.ino](arduino_motor.ino) into the Arduino IDE editor and compile and upload the code to your arduino.
5. **If the code will not upload, try going to the Tools tab ans switching the Processor to the Old Bootloader.**
6. Once your code has properly compiled and uploaded to your arduino then you are ready to run the python driver.

### Python Setup

1. Clone this repository.
2. Connect your computer to the Arduino via a USB cable. (If it is not already connected.)
3. Confirm the COM Port of your connection using the device manager.
5. Open example.py and run it to check the connetion to the motor.

## Features

### Max Speed and Acceleration

You can set the max speed using `setSpeed()` and I would recommend a speed around 70. To set the acceleration use `setAcceleration()`.

### Moving the Motor

To get a simple movement of the motor use `move()`. The integer value that you give this function will determine the number of steps the motor takes. For example, if you would like it to make a full circle use `move(200)`.

## Example

```python

from motor_driver import Motor

motor = Motor('COM11', 9600, timeout=3) #add your specific com port here
motor.setAcceleration(10)
motor.setSpeed(100)
motor.move(100)
motor.close()

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


## Dispensing Model Assembly


## Contact

Leah Nuss - leah.nuss@tum.de or
Danika Heaney - danika.heaney@tum.de or 
Helge Stein - helge.stein@tum.de

## Acknowledgements

The scale driver code was modeled after [sartoriususb](https://github.com/holgi/sartoriusb).
