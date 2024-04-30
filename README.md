# SlurryBot

# Motor Driver for Stepper Motor

This driver gives you the ability to communicate with a NEMA 17 stepper motor, using an arduino nano, and A4988 motor driver through a serial port USB connection.

## Getting Started

### Wiring

Please wire the motor, arduino, and driver together using the diagram below.

![wiring_diagram](https://github.com/Helge-Stein-Group/Slurry_Bot/assets/148461262/1e0f1947-3164-45df-9854-c35ab379af1b)


Insure that the switches on the A4988 driver are in the off position and the pins D3 and D2 are wired to the driver at D and S, respectively.

### Arduino Setup

1. Plug your Arduino Nano into your computer.
2. Download the [Arduino IDE software](https://www.arduino.cc/en/software).
3. In the Library Manager make sure to install the AccelStepper.h library. 
4. Copy the code in the file [arduino_motor.ino](arduino_motor.ino) into the Arduino IDE editor and compile and upload the code to your arduino.
5. **If the code will not upload, try switching in the Tools tab the Processor to the Old Bootloader.**
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

## Contact

Danika Heaney - danika.heaney@tum.de or 
Helge Stein - helge.stein@tum.de
