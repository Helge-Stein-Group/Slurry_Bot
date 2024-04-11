import serial
import time
import sys
import threading

class MotorError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Motor:
    def __init__(self, num, conf, baud, timeout):
        """ Initializes the serial connection. """
        self.num = num
        self.conf = conf
        self.baud = baud
        self.timeout = timeout
        self.motor_moving = False
        self.ser = None
        self.lock = threading.Lock()  # Thread lock for serial communication

    def connect(self):
        """ Opens the serial connection if not already open. """
        if self.ser is None or not self.ser.isOpen():
            self.ser = serial.Serial(self.conf, self.baud, timeout=self.timeout)

    def close(self):
        """ Closes the serial connection. """
        if self.ser is not None and self.ser.isOpen():
            self.ser.close()

    def send(self, command):
        """ Sends a command to the motor. """
        self.connect()
        with self.lock:
            self.ser.write((command + "\n").encode('utf-8'))

    def check_connection(self):
        """ Checks if the motor is connected. """
        return self.ser is not None and self.ser.isOpen()

    def set_speed(self, speed):
        """ Sets the speed of the motor. """
        if 0 < speed < 1000:
            self.send(str(self.num) + "V" + str(speed))
        else:
            raise MotorError('Speed must be between 0 and 1000')

    def stop(self):
        """ Stops the motor. """
        self.send(str(self.num) + "S")

    def set_acceleration(self, acceleration):
        """ Sets the acceleration of the motor. """
        if 0 < acceleration < 1000:
            self.send(str(self.num) + "A" + str(acceleration))
        else:
            raise MotorError('Acceleration must be between 0 and 1000')

    def move(self, steps, wait_for_motor=True):
        """ Moves the motor clockwise for a set number of steps. """
        self.motor_moving = True
        self.send(str(self.num) + "F" + str(steps))
        if wait_for_motor:
            self.wait_for_motor()

    def wait_for_motor(self):
        """ Waits for acknowledgment from the motor that the task is finished. """
        while self.motor_moving:
            with self.lock:
                response = self.ser.readline().decode('utf-8').strip()
            if response == 'MOTOR_FINISHED':
                self.motor_moving = False

    def move_up(self, steps):
        """ Moves the motor clockwise for a set number of steps. """
        self.motor_moving = True
        self.send(str(self.num) + "F" + str(steps))

    def move_down(self, steps):
        """ Moves the motor counter-clockwise for a set number of steps. """
        self.motor_moving = True
        self.send(str(self.num) + "F-" + str(steps))

    def move_counter_clockwise(self, steps):
        """ Moves the motor counter-clockwise for a set number of steps. """
        self.motor_moving = True
        self.send(str(self.num) + "B" + str(steps))

# Example usage:
if __name__ == "__main__":
    motor1 = Motor('0', 'COM5', 9600, timeout=20)
    motor2 = Motor('1', 'COM5', 9600, timeout=20)

    # Define functions for motor movements
    def move_motor1():
        motor1.move(100)

    def move_motor2():
        motor2.move(200)

    # Create threads for each motor movement
    thread1 = threading.Thread(target=move_motor1)
    thread2 = threading.Thread(target=move_motor2)

    # Start threads
    thread1.start()
    thread2.start()

    # Wait for threads to finish
    thread1.join()
    thread2.join()
