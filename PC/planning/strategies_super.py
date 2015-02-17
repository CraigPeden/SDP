

class RobotStrategy:

	def __init__(self, world):
		self.world = world

		self.our_attacker = self.world.our_attacker
		self.ball = self.world.ball
		zone = self.world._pitch._zones[self.world.our_attacker.zone]
		min_x, max_x, min_y, max_y = zone.boundingBox()
		self.goal_x = self.world.their_goal.x
		self.goal_y = self.world.their_goal.y + self.world.their_goal.height/2
		if self.world.our_side == 'left': 		#how are these chosen
			self.center_x = 350
			self.center_y = 160
		else:
			self.center_x = 160
			self.center_y = 160

		self.angle_acc = 12  	# somewhere between 9 and 15 ?
		self.position_acc = 30  # must be changed in init_per_strategy -- particulary for ball catching methods

		init_per_strategy()


	def init_per_strategy(self):

		#this is where any strategy specific instance variables should be created


				


	def pick_action(self):
		print 'Warning! Using default action picker for a strategy.'
		


	def go_to(self, dest_x, dest_y ):		#basic movement to a point defined by angle and position acc

		distance, angle = self.our_attacker.get_direction_to_point(dest_x, dest_y)  #either this method or the get direction to point needs to check for out of bounds

		if distance > self.position_acc and abs(angle) < math.pi / self.angle_acc:

			return 'drive_slow'  #may need drive_fast

		elif distance > self.position_acc and abs(angle) > 11 * math.pi / self.angle_acc:

			return 'backwards'

		if abs(angle) > math.pi / self.angle_acc:

				if abs(angle) >  3 * math.pi / self.angle_acc:  #large angle
					if angle > 0:
						return 'turn_left'
					elif angle < 0:
						return 'turn_right'
				else:									#small angle
					if angle > 0:
						return 'turn_left_slow'
					elif angle < 0:
						return 'turn_right_slow'

	def go_fast(self, dest_x, dest_y, motor_speed=None):	#fast to point optional motor speed	
		
		#an experimental method that allows for a less accurate and reversing approach to the ball with variable speed

		if motor_speed == None:			#Superfluous?
			motor_speed = 'drive'
		else:
			assert motor_speed in [ 'drive', 'drive_slow', 'drive_intercept' ]

		distance, angle = self.our_attacker.get_direction_to_point(dest_x, dest_y)  #either this method or the get direction to point needs to check for out of bounds

		if distance > self.position_acc and abs(angle) < math.pi / self.angle_acc:

			return motor_speed

		elif distance > self.position_acc and abs(angle) > math.pi - math.pi / self.angle_acc: 
			#makes the robot reverse at the right speed
			if motor_speed == 'drive_intercept' :
				return 'backwards_intercept'
			elif motor_speed == 'drive_slow':
				return 'backwards_slow'
			else:
				return 'backwards'

		if abs(angle) > math.pi / self.angle_acc:

				if abs (angle) > math.pi - math.pi / self.angle_acc  #if near to a backwards angle then turn to that
					if angle > 0:
						return 'turn_right_slow'
					elif angle < 0:
						return 'turn_left_slow'
				elif abs(angle) >  3 * math.pi / self.angle_acc:  	#large angle
					if angle > 0:
						return 'turn_left'
					elif angle < 0:
						return 'turn_right'
				else:												#small angle
					if angle > 0:
						return 'turn_left_slow'
					elif angle < 0:
						return 'turn_right_slow'

	def orient(self, dest_x, dest_y):								#maybe it would be better to pass this function an angle

		distance, angle = self.our_attacker.get_direction_to_point(dest_x, dest_y)

		if abs(angle) > math.pi / self.angle_acc:

				if abs(angle) > 3 * math.pi / self.angle_acc:
					if angle > 0:
						return 'turn_left'
					elif angle < 0:
						return 'turn_right'
				else:
					if angle > 0:
						return 'turn_left_slow'
					elif angle < 0:
						return 'turn_right_slow'



	def calculate_motor_speed(self, distance, angle):
		angle_thresh = math.pi / 7
		direction_threshhold = math.pi/7
		distance_threshhold = 15
		if not (distance is None):

			

			if distance < distance_threshhold:
				return 'stop'

			elif math.pi - abs(angle) < direction_threshhold:
				return 'backwards_intercept' 		

			elif abs(angle) > angle_thresh:

				if angle > 0:
					return 'turn_left'
				elif angle < 0:
					return 'turn_right'
			else:
				return 'drive_intercept'
