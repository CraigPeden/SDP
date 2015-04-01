import time
import serial
import threading
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
    1 |	Left Power Motor  | Arguments = 0-15 (7-8: STOP)|
    2 | Right Power Motor | Arguments = 0-15 (7-8: STOP)|
    3 | Kicker 			  | Arguments = 1 to fire 	    |
    """

    def __init__(self, port, baudrate=9600, simulator=False):

        if simulator:
            self.use_simulator = True
            self.simulatorClient = simulatorClient()
        else:
            self.use_simulator = False
        	# Initialise a serial object, give it a port, then give it a baudrate
            self.ser = serial.Serial(port, baudrate)
        
        self.left_motor = 0b00010000
        self.right_motor = 0b00100000
        self.kicker = 0b00110000

        self.has_ball = False
        self.has_grabed = False
        self.last_received = None

        read_thread = threading.Thread(target=self.readMsg)
        read_thread.setDaemon(True)
        read_thread.start()

    def write(self, opcode, value=0, attemps=-1, signature=1):
       # print opcode
        if value > 15 or value < 0:
            raise Exception("Value out of range")

        # Creating the checksum and composing the message
        message = (signature << 7) | (countSetBits(opcode | value) % 2 << 6) | opcode | value
        
        if self.use_simulator:
            self.simulatorClient.write(chr(message))
        else:
            self.ser.write(chr(message))

            if attemps > 0:
                try:
                    receivedMessage = int((self.read()[0]).encode('hex'), 16)

                    if receivedMessage != message:
                        self.write(opcode, value, attemps - 1, signature)
                except Exception:
                    self.write(opcode, value, attemps - 1, signature)
            elif attemps != -1:
                raise Exception("Write failed")

    # def read(self, timeout=0.1, buffer_size=1):
    #     start_time = time.time()
    #     out = []

    #     while (timeout > time.time() - start_time):
    #         if (self.ser.inWaiting() > 0):
    #             out.append(self.ser.read())

    #             if len(out) == buffer_size:
    #                 return out

    #     raise Exception("Read timed out")

    def readMsg(self):
        while True:
            if (self.ser.inWaiting() > 0):
                msg = self.ser.read(1)

                # Has ball
                if msg == 0b10111111:
                    self.has_ball = True

                elif msg == 0b11111110:
                    self.has_ball = False

                # Has grabbed
                elif msg == 0b11111101:
                    self.has_grabed = True

                else:
                    self.last_received = msg
            else:
                time.sleep(0.005)

    def grabberDown(self):
        self.write(self.kicker, 0)

    def grabberUp(self):
        self.write(self.kicker, 1)

    def kick(self):
        """
            The kicker kicks and retracts the kicker by itself.
        """
        self.write(self.kicker, 2)

    def kickerKick(self):
        """
            The kicker simply kicks.
        """
        self.write(self.kicker, 3)

    def kickerRetract(self):
        """
            The kicker simply retracts.
        """
        self.write(self.kicker, 4)

    def hasBall(self):
        """
            Check if the robot has the ball.
        """
        return self.has_ball

    def hasGrabbed(self):
        """
            Check if the robot has executed the grab command.
        """
        return self.has_grabed

    def getLastReceived(self):
        # TODO
        return "action"

    def grab(self):
        self.write(self.kicker, 5)
        self.has_grabed = False

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
                self.write(self.right_motor, right_wheel_speed + 8)
            else:
                self.write(self.right_motor, right_wheel_speed + 7)

def countSetBits(n):
    count = 0
    while n > 0:
        count += n & 1
        n >>= 1

    return count

