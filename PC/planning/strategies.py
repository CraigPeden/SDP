import math
import time


class DefenderGrab:
	def __init__(self, world):
		self.world = world

		self.our_defender = self.world.our_defender
		self.ball = self.world.ball
		self.last_kicker_action = time.time()
		self.zone = world._pitch._zones[self.world.our_defender.zone]
		min_x, max_x, min_y, max_y = self.zone.boundingBox()
		self.center_y = (max_y + min_y)/2


	def pick_action(self):

		distance, angle = self.our_defender.get_direction_to_point(self.ball.x, self.ball.y)
		print 'Can catch ball:' + str(self.our_defender.can_catch_ball(self.ball))
		print 'Catcher closed:' + self.our_defender.catcher


		if not self.our_defender.can_catch_ball(self.ball) and self.our_defender.catcher == 'closed':

			self.our_defender.catcher = 'open'
			return 'open_catcher'

		opponent_zone = self.world._pitch._zones[self.world.their_attacker.zone]
		min_x, max_x, min_y, max_y = opponent_zone.boundingBox()
		angle_to_opponent_zone = self.our_defender.get_rotation_to_point((max_x - min_x)/2, self.our_defender.y)

		if self.our_defender.can_catch_ball(self.ball) and self.our_defender.catcher == 'open' and abs(self.ball.y - self.center_y)>80 and abs(angle_to_opponent_zone) > math.pi/4:

			self.our_defender.catcher = 'closed'
			return [('grab', 0.5), ('backwards', 2)]	

		if self.our_defender.can_catch_ball(self.ball) and self.our_defender.catcher == 'open':

			self.our_defender.catcher = 'closed'
			return 'grab'

		#if not self.our_defender.can_catch_ball(self.ball) and self.our_defender.catcher == 'closed':

		#	self.our_defender.catcher = 'open'
		#	return 'open_catcher'

		elif not (distance is None):


			if abs(angle) > math.pi / 9:
				if abs(angle) > math.pi / 4:
					if angle > 0:
						return [('turn_left', 0.2), ('stop', 0)]
					elif angle < 0:
						return [('turn_right', 0.2), ('stop', 0)]
				else:
					if angle > 0:
						return [('turn_left', 0.2), ('stop', 0)]
					elif angle < 0:
						return [('turn_right', 0.2), ('stop', 0)]

			elif distance > 120:
				return 'drive'

			else:
				return [('drive_slow', 0.2), ('stop', 0)]

class AttackerShoot(RobotStrategy):

	def __init__(self, world):
		RobotStrategy.__init__(self, world)

	#any extra variables or overrides can go here, all the rest is in RobotStrategy

	# def __init__(self, world):
	# 	self.world = world

	# 	self.our_attacker = self.world.our_attacker
	# 	self.ball = self.world.ball
	# 	zone = self.world._pitch._zones[self.world.our_attacker.zone]
	# 	min_x, max_x, min_y, max_y = zone.boundingBox()
	# 	self.goal_x = self.world.their_goal.x 
	# 	self.goal_y = self.world.their_goal.y + self.world.their_goal.height/2
	# 	if self.world.our_side == 'left':
	# 		self.center_x = 350
	# 		self.center_y = 160
	# 	else:
	# 		self.center_x = 160
	# 		self.center_y = 160



	def pick_action(self):			# I have rewritten this function with the methods in RobotStrategy

		distance, angle = self.our_attacker.get_direction_to_point(self.center_x, self.center_y)
		angle_to_goal = self.our_attacker.get_rotation_to_point(self.goal_x, self.goal_y)

		if distance > 30:
			return go_to(self.center_x, self.center_y)

		elif abs(angle) > math.pi / 12:
			return orient(self.goal_x, self.goal_y)

		elif distance < 30 and abs(angle_to_goal) < math.pi / 12:
			self.our_attacker.catcher = 'open'
			return 'kick'




		# if distance > 30 and abs(angle) < math.pi / 12:

		# 	return 'drive_slow'
		# elif distance > 50 and abs(angle) > 11 * math.pi / 12:
		# 	return 'backwards'

		# if abs(angle) > math.pi / 9:
		# 		if abs(angle) > math.pi / 4:
		# 			if angle > 0:
		# 				return 'turn_left'
		# 			elif angle < 0:
		# 				return 'turn_right'
		# 		else:
		# 			if angle > 0:
		# 				return 'turn_left_slow'
		# 			elif angle < 0:
		# 				return 'turn_right_slow'


		# elif distance < 30 and abs(angle_to_goal) < math.pi / 9:
		# 	self.our_attacker.catcher = 'open'
		# 	return 'kick'

		# elif distance < 30 and abs(angle_to_goal) > math.pi / 9:

		# 	if angle_to_goal > 0:
		# 		return 'turn_left_slow'
		# 	elif angle_to_goal < 0:
		# 		return 'turn_right_slow'

class DefenderIntercept:
	def __init__(self, world):
		self.world = world

		self.DISTANCE_THRESH = 15
		self.ANGLE_THRESH = math.pi / 12

		self.ball = world.ball
		self.zone = world._pitch._zones[self.world.our_defender.zone]
		min_x, max_x, min_y, self.max_y = self.zone.boundingBox()
		self.center_x = (min_x + max_x) / 2
		self.our_defender = world.our_defender
		self.our_attacker = world.our_attacker
		self.their_defender = world.their_defender
		self.their_attacker = world.their_attacker


	


	def pick_action(self):

		if self.ball.y > 80 and self.ball.y < 215:
			y=(self.ball.y+150)/2
		elif self.ball.y < 80:
			y=95
		else: 
			y=180	
			
		distance, angle = self.our_defender.get_direction_to_point(self.center_x, y)
		print self.center_x, y
		return self.calculate_motor_speed(distance, angle)

		else:
			y=180

		distance, angle = self.our_defender.get_direction_to_point(self.center_x, y)
			print self.center_x, y
			return self.calculate_motor_speed(distance, angle)

		if self.ball.y > 80 and self.ball.y < 215:
			y=(self.ball.y+150)/2
		elif self.ball.y < 80:
			y=95
		else:
			y=180

		distance, angle = self.our_defender.get_direction_to_point(self.center_x, y)
		print self.center_x, y
		return self.calculate_motor_speed(distance, angle)


	def calculate_motor_speed(self, distance, angle):
		angle_thresh = math.pi / 4
		direction_threshhold = math.pi/7
		distance_threshhold = 30

		if not (distance is None):



			if distance < distance_threshhold:
				return 'stop'

			elif math.pi - abs(angle) < direction_threshhold:
				return 'backwards_intercept'

			elif abs(angle) > angle_thresh:

				if angle > 0:
					return 'turn_left_slow'
				elif angle < 0:
					return 'turn_right_slow'
			else:
				return 'drive_intercept'

class DefenderPass:
	def __init__(self, world):
		self.world = world

		self.DISTANCE_THRESH = 15
		self.ANGLE_THRESH = math.pi / 12

		self.our_defender = self.world.our_defender
		self.our_attacker = self.world.our_attacker
		self.ball = self.world.ball
		self.zone = self.world._pitch._zones[self.world.our_defender.zone]
		min_x, max_x, min_y, max_y = self.zone.boundingBox()
		self.center_x = (min_x + max_x) / 2
		self.center_y = (min_y + max_y) / 2


		self.their_defender = self.world.their_defender
		self.their_attacker = self.world.their_attacker
		self.ball = self.world.ball

		self.opponent_zone = self.world._pitch._zones[self.world.our_attacker.zone]
		self.opp_min_x, self.opp_max_x, self.opp_min_y, self.opp_max_y = self.opponent_zone.boundingBox()
		self.opponent_x = (self.opp_max_x + self.opp_min_x)/2







	def pick_action(self):
		
		if self.their_attacker.y < self.center_y:
			angle_to_pass_point = self.our_defender.get_rotation_to_point(self.opp_max_x, self.opp_max_y)
		else:
			angle_to_pass_point = self.our_defender.get_rotation_to_point(self.opp_max_x, self.opp_min_y)
			

		distance, angle = self.our_defender.get_direction_to_point(self.center_x, self.center_y)
		
		print 'Can catch ball:' + str(self.our_defender.can_catch_ball(self.ball))
		print 'Catcher closed:' + self.our_defender.catcher

		if distance < 35 and abs(angle_to_pass_point) < math.pi / 18:
			self.our_defender.catcher = 'open'
			return [('open_catcher', 0.5), ('kick', 1)]

		elif distance < 35 and abs(angle_to_pass_point) > math.pi / 18:

			if angle_to_pass_point > 0:
				return [('turn_left', 0.2), ('stop', 0.2)]
			elif angle_to_pass_point < 0:
				return [('turn_right', 0.2), ('stop', 0.2)]

		elif distance > 20 and abs(angle) < math.pi / 12:

			return 'drive_slow'
		elif distance > 20 and abs(angle) > 11 * math.pi / 12:
			return 'backwards'

		elif distance > 20 and abs(angle) > math.pi / 12:

			if angle > 0:
				return [('turn_left', 0.2), ('stop', 0.2)]
			elif angle < 0:
				return [('turn_right', 0.2), ('stop', 0.2)]
