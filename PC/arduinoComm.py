import serial
import time

class Communication(object):
	"""
	Class which will handle interfacing with the serial
	bus which will transmit to the arduino

	To save as much on arduino computation as possible, a protocol will be
	defined here to allow a single byte to contain both the operation and
	the required arguments.

	Command byte:
	|  2 bits  |  2 bits  |  4 bits  |
	|   SIG    |  OPCODE  | ARGUMENT |

	SIG is the signature for the communication.
	OPCODE is a 2 bit unsigned int.
	ARGUMENT is a 4 bit unsigned int.

	OPCODES
	0 |	LED 			 | Arguments = blinks     	  |
	1 | Power Motor	     | Arguments = -1/0/1, -1/0/1 |
	2 | Rotational Motor | Arguments = 0-14      	  |
	3 | Kicker 			 | Arguments = 1 to fire 	  |
	"""
	
	def __init__(self, port, baudrate = 115200, sig = 0b11000000):
		# Initialise a serial object, give it a port, then give it a baudrate
		self.ser = serial.Serial(port, baudrate)

		self.sig = sig
		self.led_mask = 0b00000000
		self.motor_mask = 0b00010000
		self.rot_mask = 0b00100000
		self.kicker_mask = 0b00110000

	def write(self, mask, value = 0, attemps = 5):
		if value > 15 or value < 0:
			raise Exception("Argument value out of range")

		msg = self.sig | mask | value
		self.ser.write(chr(msg))

		if (int((self.read()[0]).encode('hex'), 16) != msg):
			if attemps > 0:
				self.write(mask, value, attemps - 1)
			else:
				raise Exception("Write failed")

	def read(self, timeout = 0.1,  buffer_size = 1):
		start_time = time.time()
		out = []

		while (timeout > time.time() - start_time):
			if (self.ser.inWaiting() > 0):
				out.append(self.ser.read())

				if len(out) == buffer_size:
					return out

		raise Exception("Read timed out")

	def led(self, iteration):
		self.write(self.led_mask, iteration)

	def kicker(self):
		self.write(self.kicker_mask)
		# Kicker recharge mechanism here

	def rotation(self, angle):
		if angle > 14 or angle < 0:
			raise Exception("Rotation angle out of range")
		else:
			self.write(self.rot_mask, angle)

	def drive(self, left_wheel_status, right_wheel_status):
		# status is an int value between -1 and 1
		if left_wheel_status > 1 or left_wheel_status < -1 or right_wheel_status > 1 or right_wheel_status < -1:
			raise Exception("Wheel status out of range")
		else:
			self.write(self.motor_mask, ((left_wheel_status + 1) << 2) + (right_wheel_status + 1))

class Vision(object):
	"""
	Class which will handle interfacing with the vision
	system to give required information about the scanario 
	"""
	def ball_position(self):
		# Function that will return the current position of the ball
		self.ball_position = (0,0)

	def robot_position(self):
		# Function that will return the current position of the robot
		self.robot_position = (10,10)

class Movement(object):
	def movement(self, robot_position, ball_position):
		# Maths to move the robot from it's current position to the ball
		self.test = "hello"

#a = Communication("/dev/ttyACM0", 9600)
#a.led(3)
#a.rotation(10)
#a.drive(1,1)
