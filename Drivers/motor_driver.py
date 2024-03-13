import serial
import time
import sys

class motorError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Motor():
    def __init__(self,num,conf,baud,timeout):
        """ Initializes the serial connection. """
        self.num = num
        self.conf = conf
        self.baud = baud
        self.timeout = timeout
        #try: 
        self.ser = serial.Serial(conf, baud, timeout=timeout)
        # except serial.SerialException:
        #     print('Unable to connect to the motor or motor is already connected. Check the com port and try again.')
        #     sys.exit(1) #Exiting the program if the motor is not connected.

    def close(self):
        """ Closes the serial connection. """
        self.ser.close()
    
    def send(self, command):
        """ Sends a command to the motor. Can be used to send custom commands."""
        self.ser.write((command+"\n").encode('utf-8'))
        
    def checkConnection(self):
        """ Checks if the motor is connected. """
        return self.ser.isOpen()
    
    def setSpeed(self, speed):
        """ Sets the speed of the motor. """
        if speed > 0 and speed < 1000:
            self.send(str(self.num) + "V" + str(speed))
        else:
            raise motorError('Speed must be between 0 and 1000')
          
    def stop(self):
      """ Stops the motor. """
      self.send(str(self.num) + "S")

    def setAcceleration(self, acceleration):
        """ Sets the acceleration of the motor. """
        if acceleration > 0 and acceleration < 1000:
            self.send(str(self.num) + "A" + str(acceleration))
        else:
            raise motorError('Acceleration must be between 0 and 1000')

    def move(self, steps):
        """ Moves the motor clockwise at the current speed for a set number of steps. """
        self.send(str(self.num) + "F" + str(steps))

    def moveUp(self, steps):
        """ Moves the motor clockwise at the current speed for a set number of steps. """
        self.send(str(self.num) + "F" + str(steps))

    def moveDown(self, steps):
        """ Moves the motor clockwise at the current speed for a set number of steps. """
        self.send(str(self.num) + "F-" + str(steps))

''' def moveCounterClockwise(self, steps):
        """ Moves the motor counter-clockwise at the current speed for a set number of steps. """
        self.send(str(self.num) + "B" + str(steps) + "\n")'''
