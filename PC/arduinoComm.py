import time

import serial
from simulatorClient import simulatorClient

class Communication(object):
    """
    Class which will handle interfacing with the serial
    bus which will transmit to the arduino

    To save as much on arduino computation as possible, a protocol will be
    defined here to allow a single byte to contain both the operation and
    the required arguments.

    Command byte:
    |  1 bit  |  1 bit   |  2 bits  |  4 bits  |
    |   SIG   | CHECKSUM |  OPCODE  | ARGUMENT |

    SIG is the signature of our communication, the value is 1
    CHECKSUM is number of set bits (OPCODE ARGUMENT) % 2
    OPCODE is a 2 bit unsigned int.
    ARGUMENT is a 4 bit unsigned int.

    OPCODES
    0 |	Left Power Motor  | Arguments = 0-15 (7-8: STOP)|
    1 | Right Power Motor | Arguments = 0-15 (7-8: STOP)|
    2 | Rotational Motor  | Arguments = 0-14      	    |
    3 | Kicker 			  | Arguments = 1 to fire 	    |
    """

    def __init__(self, port, baudrate=115200, simulator=False):
        # Initialise a serial object, give it a port, then give it a baudrate
        
        
        if simulator:
            self.use_simulator = simulator
            self.simulatorClient = simulatorClient()
        else:
            self.ser = serial.Serial(port, baudrate)
        
        self.left_motor = 0b00000000
        self.right_motor = 0b00010000
        self.rotation = 0b00100000
        self.kicker = 0b00110000

    def write(self, opcode, value=0, attemps=5, signature=1):
       # print opcode
        if value > 15 or value < 0:
            raise Exception("Value out of range")

        #if opcode > 3 or opcode < 0:
         #   raise Exception("Opcode out of range")

        # Creating the checksum and composing the message
        message = (signature << 7) | (countSetBits(opcode | value) % 2 << 6) | opcode | value
        
        if self.use_simulator:
            self.simulatorClient.write(chr(message))
        else:
            self.ser.write(chr(message))

            # print bin(message), bin(int((self.read()[0]).encode('hex'), 16))

            if attemps > 0:
                try:
                    receivedMessage = int((self.read()[0]).encode('hex'), 16)

                    if receivedMessage != message:
                        self.write(opcode, value, attemps - 1, signature)
                except Exception:
                    self.write(opcode, value, attemps - 1, signature)
            else:
                raise Exception("Write failed")

    def read(self, timeout=0.1, buffer_size=1):
        start_time = time.time()
        out = []

        while (timeout > time.time() - start_time):
            if (self.ser.inWaiting() > 0):
                out.append(self.ser.read())

                if len(out) == buffer_size:
                    return out

        raise Exception("Read timed out")

    def grab(self):
        self.write(self.kicker, 0)

    def kick(self):
        self.write(self.kicker, 1)

    def rotation(self, angle):
        if angle > 14 or angle < 0:
            raise Exception("Rotation angle out of range")
        else:
            self.write(self.rotation, angle)

    def stop(self):
        self.write(self.left_motor, 7)
        self.write(self.right_motor, 7)

    def drive(self, left_wheel_speed, right_wheel_speed):
        # speed is an int value between -7 and 7
        if left_wheel_speed > 7 or left_wheel_speed < -7 or right_wheel_speed > 7 or right_wheel_speed < -7:
            raise Exception("Wheel speed out of range")
        else:
            if left_wheel_speed > 0:
                self.write(self.left_motor, left_wheel_speed + 8)
            else:
                self.write(self.left_motor, left_wheel_speed + 7)

            if right_wheel_speed > 0:
                self.write(self.right_motor, 7 - right_wheel_speed)
            else:
                self.write(self.right_motor, 8 - right_wheel_speed)


class Vision(object):
    """
    Class which will handle interfacing with the vision
    system to give required information about the scanario
    """

    def ball_position(self):
        # Function that will return the current position of the ball
        self.ball_position = (0, 0)

    def robot_position(self):
        # Function that will return the current position of the robot
        self.robot_position = (10, 10)


class Movement(object):
    def movement(self, robot_position, ball_position):
        # Maths to move the robot from it's current position to the ball
        self.test = "hello"


def countSetBits(n):
    count = 0
    while n > 0:
        count += n & 1
        n >>= 1

    return count

