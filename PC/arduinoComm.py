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
	def __init__(self):
		# Initialise a serial object, give it a port, then give it a baudrate
		self.ser = serial.Serial()
		self.ser.port = 0
		self.ser.baudrate = 115200

	def led(self, on_off):
		if on_off == 0:
			self.ser.write("0000")
			time.sleep(1)
		elif on_off == 1:
			self.ser.write("0001")
			time.sleep(1)

	def kicker(self):
		self.ser.write("1001")
		# Kicker recharge mechanism here

	def rotation(self,wheel,angle):
		if wheel == "left":
			self.ser.write("2" + str(angle))
		elif wheel == "right":
			self.ser.write("4" + str(angle))

	def drive(self,wheel,on_off):
		if wheel == "left":
			if on_off == 0:
				self.ser.write("3000")
			if on_off == 1:
				self.ser.write("3001")
		if wheel == "right":
			if on_off == 0:
				self.ser.write("5000")
			if on_off == 1:
				self.ser.write("54001")

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

a = Communication()
print a.ser
#a.led()
