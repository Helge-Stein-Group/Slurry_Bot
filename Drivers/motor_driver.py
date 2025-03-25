import serial
import time
import sys

class SerialConnection:
    def __init__(self, port, baudrate, timeout):
        """ Initializes the serial connection. """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            time.sleep(2)  # Wait for Arduino to reset
        except serial.SerialException:
            print('Unable to connect to the motor or motor is already connected. Check the com port and try again.')
            sys.exit(1)  # Exiting the program if the motor is not connected.

    def close(self):
        """ Closes the serial connection. """
        self.ser.close()

    def send_command(self, command):
        """ Sends a command to the serial connection. """
        self.ser.write((command + "\n").encode('utf-8'))

    def read_response(self):
        """ Reads and returns the response from the serial connection. """
        return self.ser.readline().decode('utf-8').strip()


class Motor:
    def __init__(self, connection, num):
        self.connection = connection
        self.num = num

    def check_connection(self):
        # Check if the motor responds to a connection test
        self.connection.send_command(f"{self.num:02}Q")
        return self.connection.read_response() == 'MOTOR_CONNECTED'

    def stop(self):
        # Immediately stop the motor
        self.connection.send_command(f"{self.num:02}S")
        self._wait_for_motor()

    def set_speed(self, speed):
        # Set motor speed (1 to 1000)
        if 0 < speed <= 1000:
            self.connection.send_command(f"{self.num:02}V{speed}")
            self._wait_for_motor()
        else:
            raise ValueError("Speed must be between 1 and 1000")

    def move_relative(self, steps):
        # Move the motor relative to its current position
        self.connection.send_command(f"{self.num:02}M{steps}")
        self._wait_for_motor()

    def move_down(self, steps):
        # Move motor up (positive direction)
        self.move_relative(abs(steps))

    def move_up(self, steps):
        # Move motor down (negative direction)
        self.move_relative(-abs(steps))

    def move_absolute(self, target):
        # Move motor to an absolute position
        self.connection.send_command(f"{self.num:02}A{target}")
        self._wait_for_motor()

    def move_to_top(self):
        # Move motor to its top position (maxPosition in Arduino)
        self.connection.send_command(f"{self.num:02}A0")  # Arduino constrains to maxPosition
        self._wait_for_motor()

    def move_to_bottom(self):
        # Move motor to the bottom (position 0)
        self.connection.send_command(f"{self.num:02}A999999")
        self._wait_for_motor()

    def set_home(self):
        # Set the current position as the new home (zero)
        self.connection.send_command(f"{self.num:02}H")
        response = self.connection.read_response()
        if response == "HOME_SET":
            print("Home position set.")

    def _wait_for_motor(self):
        # Wait until the motor has finished its task
        while True:
            response = self.connection.read_response()
            if response == 'MOTOR_FINISHED':
                break
            elif "ERROR" in response:
                print(response)
            elif "WARNING" in response:
                print(response)
                break
