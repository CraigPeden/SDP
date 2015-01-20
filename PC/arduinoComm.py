import serial
import time

class Communication(object):
	"""
	Class which will handle interfacing with the serial
	bus which will transmit to the arduino

	To save as much on arduino computation as possible, a protocol will be
	defined here to allow a single string to contain both the operation and
	the required arguments.

	8 bit string of ASCII characters
	|	1 char	|	3 char	|
	|	OPCODE	|	Argument|

	OPCODE is 0-padded to 3 chars.
	ARGUMENT is 0-padded to 5 chars.

	OPCODES
	0 |	LED 					| Arguments = 0/1 off/on 	|
	1 | Kicker 					| Arguments = 1 to fire 	|
	2 | Left Rotational Motor	| Arguments = 0-360 degrees	|
	3 | Left Power Motor		| Arguments = 0/1 off/on 	|
	4 | Right Rotational Motor	| Arguments = 0-360 degrees	|
	5 | Right Power Motor		| Arguments = 0/1 off/on 	|
	6 | UNDEFINED 				| Arguments = UNDEFINED		|
	7 | UNDEFINED				| Arguments = UNDEFINED		|

	"""
	def __init__(self, port, baudrate = 115200, sig = 0b11000000):
		# Initialise a serial object, give it a port, then give it a baudrate
		self.ser = serial.Serial(port, baudrate)

		self.sig = sig
		self.led_mask = 0b00000000
		self.motor_mask = 0b00010000
		self.rot_mask = 0b00100000
		self.kicker_mask = 0b00110000

	def write(self, mask, value = 0):
		if value > 15 or value < 0:
			raise Exception("Argument value out of range")
		msg = self.sig | mask | value
		self.ser.write(chr(msg))

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

	def drive(self, front_wheel_status, back_wheel_status):
		# status is an int value between -1 and 1
		if front_wheel_status > 1 or front_wheel_status < -1 or back_wheel_status > 1 or back_wheel_status < -1:
			raise Exception("Wheel status out of range")
		else:
			self.write(self.motor_mask, ((front_wheel_status + 1) << 2) + (back_wheel_status + 1))

>>>>>>> basile-dev

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

a = Communication("/dev/ttyACM0", 9600)
a.led(5)
a.drive(1,1)
