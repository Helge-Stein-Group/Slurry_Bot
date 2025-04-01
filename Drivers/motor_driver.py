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
    def __init__(self, connection, num, max_position=None):
        self.connection = connection
        self.num = num
        self.max_position = max_position  # Optional: max steps

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

    def check_connection(self):
        # Check if the motor responds to a connection test
        self.connection.send_command(f"{self.num}Q")
        return self.connection.read_response() == 'MOTOR_CONNECTED'

    def stop(self):
        # Immediately stop the motor
        self.connection.send_command(f"{self.num}S")
        self._wait_for_motor()

    def set_speed(self, speed):
        # Set motor speed (1 to 1000)
        if 0 < speed <= 1000:
            self.connection.send_command(f"{self.num}V{speed}")
            self._wait_for_motor()
        else:
            raise ValueError("Speed must be between 1 and 1000")

    def set_home(self):
        """Sets the current position as home (0)."""
        self.connection.send_command(f"{self.num}H")
        self._wait_for_motor()

    def move_relative(self, steps):
        """Moves the motor by a relative number of steps (positive or negative)."""
        if self.max_position is not None and abs(steps) > self.max_position:
            print(f"Movement of {steps} steps exceeds allowed limit of {self.max_position}. Skipped.")
            return
        self.connection.send_command(f"{self.num}M{steps}")
        self._wait_for_motor()

    def move_down(self, steps):
        # Move motor up (positive direction)
        self.move_relative(-abs(steps))

    def move_up(self, steps):
        # Move motor down (negative direction)
        self.move_relative(abs(steps))

    def move_to_top(self):
        """Moves to the maximum defined steps (upward)."""
        if self.max_position is not None:
            self.move_relative(self.max_position)
        else:
            print("No max_position defined for move_to_top().")

    def move_to_bottom(self):
        """Moves to bottom by going down the max_position steps."""
        if self.max_position is not None:
            self.move_relative(-self.max_position)
        else:
            print("No max_position defined for move_to_bottom().")

    

    
