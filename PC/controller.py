from vision.vision import Vision, Camera, GUI
from planning.planner import Planner
from postprocessing.postprocessing import Postprocessing
from preprocessing.preprocessing import Preprocessing
import vision.tools as tools
from cv2 import waitKey
import cv2
import serial
import warnings
import time
import arduinoComm



warnings.filterwarnings("ignore", category=DeprecationWarning)


class Controller:
	"""
	Primary source of robot control. Ties vision and planning together.
	"""

	def __init__(self, pitch, color, our_side, video_port=0, comm_port='/dev/ttyUSB0', comms=1):
		"""
		Entry point for the SDP system.

		Params:
			[int] video_port                port number for the camera
			[string] comm_port              port number for the arduino
			[int] pitch                     0 - main pitch, 1 - secondary pitch
			[string] our_side               the side we're on - 'left' or 'right'
		
			*[int] port                     The camera port to take the feed from
			*[Robot_Controller] attacker    Robot controller object - Attacker Robot has a RED
											power wire
			*[Robot_Controller] defender    Robot controller object - Defender Robot has a YELLOW
											power wire
		"""
		assert pitch in [0, 1]
		assert color in ['yellow', 'blue']
		assert our_side in ['left', 'right']
		

		self.pitch = pitch


		# Set up the Arduino communications
		self.arduino = arduinoComm.Communication("/dev/ttyACM0", 9600) 
		

		# Set up camera for frames
		self.camera = Camera(port=video_port, pitch=self.pitch)
		frame = self.camera.get_frame()
		center_point = self.camera.get_adjusted_center(frame)

		# Set up vision
		self.calibration = tools.get_colors(pitch)
		self.vision = Vision(
			pitch=pitch, color=color, our_side=our_side,
			frame_shape=frame.shape, frame_center=center_point,
			calibration=self.calibration)

		# Set up postprocessing for vision
		self.postprocessing = Postprocessing()

		# Set up main planner
		self.planner = Planner(our_side=our_side, pitch_num=self.pitch, our_color=color)

		# Set up GUI
		self.GUI = GUI(calibration=self.calibration, arduino=self.arduino, pitch=self.pitch)

		self.color = color
		self.side = our_side

		self.preprocessing = Preprocessing()
	#it doesn't matter whether it is an Attacker or a Defender Controller
		self.controller = Attacker_Controller()


	def wow(self):
		"""
		Ready your sword, here be dragons.
		"""
		counter = 1L
		timer = time.clock()
		try:
			c = True
			while c != 27:  # the ESC key

				frame = self.camera.get_frame()
				pre_options = self.preprocessing.options
				# Apply preprocessing methods toggled in the UI
				preprocessed = self.preprocessing.run(frame, pre_options)
				frame = preprocessed['frame']
				if 'background_sub' in preprocessed:
					cv2.imshow('bg sub', preprocessed['background_sub'])
				# Find object positions
				# model_positions have their y coordinate inverted

				model_positions, regular_positions = self.vision.locate(frame)
				model_positions = self.postprocessing.analyze(model_positions)

				# Find appropriate action
				self.planner.update_world(model_positions)
				
				robot_action = self.planner.plan()

				

				if self.controller is not None:
					self.controller.execute(self.arduino, robot_action)
	   

				# Information about the grabbers from the world
				grabbers = {
					'our_defender': self.planner._world.our_defender.catcher_area,
					'our_attacker': self.planner._world.our_attacker.catcher_area
				}

				# Information about states
				robotState = 'test'
			   

				# Use 'y', 'b', 'r' to change color.
				c = waitKey(2) & 0xFF
				actions = []
				fps = float(counter) / (time.clock() - timer)
				# Draw vision content and actions

				self.GUI.draw(
					frame, model_positions, actions, regular_positions, fps, robotState,
				   "we dont need it", robot_action, "we dont need it", grabbers,
					our_color='blue', our_side=self.side, key=c, preprocess=pre_options)
				counter += 1

		except:
			if self.controller is not None:
				self.controller.shutdown(self.arduino)
			raise

		finally:
			# Write the new calibrations to a file.
			tools.save_colors(self.pitch, self.calibration)
			if self.controller is not None:
				self.controller.shutdown(self.arduino)


class Robot_Controller(object):
	"""
	Robot_Controller superclass for robot control.
	"""

	def __init__(self):
		"""
		Connect to Brick and setup Motors/Sensors.
		"""
		self.current_speed = 0

	def shutdown(self, comm):
		# TO DO
			pass




class Attacker_Controller(Robot_Controller):
	"""
	Attacker implementation.
	"""

	def __init__(self):
		"""
		Do the same setup as the Robot class, as well as anything specific to the Attacker.
		"""
		super(Attacker_Controller, self).__init__()
		self.last_kicker_action = time.time()

	def execute(self, comm, action):
		"""
		Execute robot action.
		"""
		if action != None:
			print action    

		if action == 'grab':

			comm.stop()
			comm.grabberDown()
			time.sleep(0.2)

		elif action == 'open_catcher':
			comm.stop()   
			comm.grabberUp()

	
		elif action == 'kick':

			comm.stop()
			comm.kick()
			time.sleep(0.2)

		elif action == 'turn_left':

		  
			comm.drive(-4, 4)

		elif action == 'turn_right':
		  
			comm.drive(4, -4)

		elif action == 'turn_left_slow':

		  
			comm.drive(-3, 3)

		elif action == 'turn_right_slow':
		  
			comm.drive(3, -3)

		elif action == 'backwards':
		  
			comm.drive(-4, -4)
		elif action == 'backwards_intercept':
		  
			comm.drive(-7, -7)	

		elif action == 'drive':
		  
			comm.drive(4, 4)
		elif action == 'drive_intercept':
		  
			comm.drive(7, 7)	
		elif action == 'drive_slow':
		  
			comm.drive(3, 3)

		elif action == 'backwards':
			comm.drive(-4, 4)

		elif action == 'stop':
		  
			comm.drive(0, 0)
		else:
			comm.stop()
		
			
			
			

	def shutdown(self, comm):
		comm.drive(0, 0)





if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("pitch", help="[0] Main pitch, [1] Secondary pitch")
	parser.add_argument("side", help="The side of our defender ['left', 'right'] allowed.")
	parser.add_argument("color", help="The color of our team - ['yellow', 'blue'] allowed.")
	parser.add_argument(
		"-n", "--nocomms", help="Disables sending commands to the robot.", action="store_true")

	args = parser.parse_args()
	if args.nocomms:
		c = Controller(
			pitch=int(args.pitch), color=args.color, our_side=args.side, comms=0).wow()
	else:
		c = Controller(
			pitch=int(args.pitch), color=args.color, our_side=args.side).wow()
