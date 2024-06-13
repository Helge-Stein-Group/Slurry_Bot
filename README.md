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
4. Clone this whole repository and run the robot testing code in the begining of the `examples.ipynb` file.

## Motors and Wiring

This section provides an overview of the wiring and motor control within the system. The motor driver enables communication via a serial port USB connection, allowing control of up to six NEMA 17 or 23 stepper motors, all connected to a single Arduino Nano.

### Getting Started

#### Wiring of NEMA 17

The NEMA 17 motor can be operated using an A4988 driver and a 9-volt power supply. Ensure that the switches on the A4988 driver are in the off position, then wire the motor, Arduino, and driver together according to the diagram below. In this diagram, the Arduino pins D2 and D3 are connected to the driver's S and D pins, respectively, meaning in the Python code, this motor would be referred to as motor 0. Motor 1 would be wired to pins D4 and D5, Motor 2 to pins D6 and D7, and so on.

<img src="https://github.com/Helge-Stein-Group/Slurry_Bot/assets/148461262/1e0f1947-3164-45df-9854-c35ab379af1b" width="500" height="500"/>

#### Wiring of NEMA 23

The NEMA 23 is a larger and more powerful motor, operated using a TB6600 motor driver and a 12-volt power supply. Ensure that the switches are set to the correct positions as shown in the diagram. In this example, the motor is wired to pins D4 and D5, so in the Python code, it is referred to as motor 1. This configuration is detailed and can be tested by cloning the repository and running the motor lines in the file `examples.ipynb`.

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
2. Insure you cloned the repository.
3. Confirm the COM Port of your connection using the device manager.
4. To test the setup you should open a file and run the motor testing code in `examples.ipynb`.


## Features

### Max Speed and Acceleration

You can set the max speed using `setSpeed()` and I would recommend a speed around 70. To set the acceleration use `setAcceleration()`.

### Moving the Motor

To get a simple movement of the motor use `move()`. The integer value that you give this function will determine the number of steps the motor takes. For example, if you would like it to make a full circle use `move(200)`. When opperating the linear rail you can use the functions `moveUp()` and `moveDown()`. The motor can be stopped using the `stop()` function. Any updates or additional methods can be added to the `motor_driver.py` file.


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
3. Insure you cloned the repository.
4. Confirm the COM Port of your connection using the device manager.
5. To test the setup you should open a file and run the scale testing code in `examples.ipynb`.

### Features

- Communicate with the scale to get weight measurements
- Process scale responses and raw data
- Configure the scale settings
- Error handling for scale communication

#### Tare and Calibration

To tare the scale use `tare()` and to preform an internal callibration use `intCal()`.

#### Measuring

To get a simple weight measurement use the `measure()` or `measure_stable()` functions. 


## Pipette Control for a Sartorius rLINE

Here you can find information on operating the automated pipette rLINE® 1-channel 5000 µl dispensing module from Sartorius. This device is integrated into our system for liquid and slurry dispensing.

The manual for this pipette can be found [here](https://shop.sartorius.com/medias/rLINE-dispensing-module-user-manual.pdf?context=bWFzdGVyfGRvY3VtZW50c3wxMDQ1NjEzfGFwcGxpY2F0aW9uL3BkZnxhRFJsTDJneFlpODVNelkyTXpnME5UUXhOekkyfDMyMTFlYjlkNGRhMjdmNjc1ZTJhMGRmOWQ0NTgwZmNmNzkyNmZhNjliYzg3MmJjYTE4MzcyNTBlODIwM2UzYjY).

### Getting Started 

#### Setup

1. Connect the pipette to your PC via the USB-B cable included in the kit.
2. Check your COM port connection and ensure its configuration matches the settings in the `pipette_driver.py` file.
3. Run the testing code for the pipette, which can be found at the bottom of the `examples.ipynb` file. The `initiate_rline` function must be used to establish the connection with the module, which usually takes a few seconds.

### Features

#### Functions Avalible

To draw liquid into the pipette tip, use the `aspirate()` function, and to dispense it, use the `dispense()` function. If some liquid remains in the tip, you can use either the `blowout()` or `clear_and_reset()` functions. Ensure that you run `reset()` (which will eject the tip) after `blowout()` before performing another `aspirate()`. The `eject()` function will eject the tip, and after usage, you need to run the `disconnect_pipette()` function to properly close the serial port.

## Contact

Leah Nuss - leah.nuss@tum.de <br/>
Danika Heaney - danika.heaney@tum.de <br/>
Helge Stein - helge.stein@tum.de

## Acknowledgements

The scale driver code was modeled after [sartoriususb](https://github.com/holgi/sartoriusb).
The pipette driver code was provided by [Bojing Zhang](https://github.com/Bojing4313).
