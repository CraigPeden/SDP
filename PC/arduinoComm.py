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
	0 |	Left Power Motor  | Arguments = 0-15 (7-8: STOP)|
	1 | Right Power Motor | Arguments = 0-15 (7-8: STOP)|
	2 | Rotational Motor  | Arguments = 0-14      	    |
	3 | Kicker 			  | Arguments = 1 to fire 	    |
	"""
	
	def __init__(self, port, baudrate = 115200, sig = 0b11000000):
		# Initialise a serial object, give it a port, then give it a baudrate
		self.ser = serial.Serial(port, baudrate)

		self.sig = sig
		self.left_motor_mask = 0b00000000
		self.right_motor_mask = 0b00010000
		self.rot_mask = 0b00100000
		self.kicker_mask = 0b00110000

	def write(self, mask, value = 0, attemps = 5):
		if value > 15 or value < 0:
			raise Exception("Argument value out of range")

		msg = self.sig | mask | value
		self.ser.write(chr(msg))
		#print bin(msg), bin(int((self.read()[0]).encode('hex'), 16))

		# if (int((self.read()[0]).encode('hex'), 16) != msg):
		# 	if attemps > 0:
		# 		self.write(mask, value, attemps - 1)
		# 	else:
		# 		raise Exception("Write failed")

	def read(self, timeout = 0.1,  buffer_size = 1):
		start_time = time.time()
		out = []

		while (timeout > time.time() - start_time):
			if (self.ser.inWaiting() > 0):
				out.append(self.ser.read())

				if len(out) == buffer_size:
					return out

		raise Exception("Read timed out")

	def grab(self):
		self.write(self.kicker_mask, 0)

	def kick(self):
		self.write(self.kicker_mask, 1)

	def rotation(self, angle):
		if angle > 14 or angle < 0:
			raise Exception("Rotation angle out of range")
		else:
			self.write(self.rot_mask, angle)

	def stop(self):
		self.write(self.left_motor_mask, 7)
		self.write(self.right_motor_mask, 7)

	def drive(self, left_wheel_speed, right_wheel_speed, left_forward = True, right_forward = True):
		# speed is an int value between 0 and 7
		if left_wheel_speed > 7 or left_wheel_speed < 0 or right_wheel_speed > 7 or right_wheel_speed < 0:
			raise Exception("Wheel speed out of range")
		else:
			if left_forward:
				self.write(self.left_motor_mask, left_wheel_speed + 8)
			else:
				self.write(self.left_motor_mask, 8 - left_wheel_speed)

			if right_forward:
				self.write(self.right_motor_mask, 8 - right_wheel_speed)
			else:
				self.write(self.right_motor_mask, right_wheel_speed + 8)

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
