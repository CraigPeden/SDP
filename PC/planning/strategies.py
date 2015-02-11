import math
import time


class AttackerGrab:
	def __init__(self, world):
		self.world = world

		self.our_attacker = self.world.our_attacker
		self.ball = self.world.ball
		zone = self.world._pitch._zones[self.world.our_attacker.zone]
		min_x, max_x, min_y, max_y = zone.boundingBox()
		self.last_kicker_action = time.time()


	def pick_action(self):

		distance, angle = self.our_attacker.get_direction_to_point(self.ball.x, self.ball.y)

		if self.our_attacker.can_catch_ball(self.ball) and time.time() > self.last_kicker_action + 2:

			self.last_kicker_action = time.time()
			self.our_attacker.catcher = 'closed'
			return 'grab'

		if not self.our_attacker.can_catch_ball(self.ball) and self.our_attacker.catcher == 'closed' and time.time() > self.last_kicker_action + 1:

			self.last_kicker_action = time.time()
			self.our_attacker.catcher = 'open'
			return 'open_catcher'

		elif not (distance is None):


			if abs(angle) > math.pi / 9:
				if abs(angle) > math.pi / 4:
					if angle > 0:
						return 'turn_left'
					elif angle < 0:
						return 'turn_right'
				else:
					if angle > 0:
						return 'turn_left_slow'
					elif angle < 0:
						return 'turn_right_slow'

			elif distance > 70:
				return 'drive'

			else:
				return 'drive_slow'


class AttackerShoot:
	def __init__(self, world):
		self.world = world

		self.our_attacker = self.world.our_attacker
		self.ball = self.world.ball
		zone = self.world._pitch._zones[self.world.our_attacker.zone]
		min_x, max_x, min_y, max_y = zone.boundingBox()
		self.goal_x = self.world.their_goal.x 
		self.goal_y = self.world.their_goal.y + self.world.their_goal.height/2
		if self.world.our_side == 'left':
			self.center_x = 350
			self.center_y = 160
		else:
			self.center_x = 160
			self.center_y = 160
				


	def pick_action(self):

		distance, angle = self.our_attacker.get_direction_to_point(self.center_x, self.center_y)
		angle_to_goal = self.our_attacker.get_rotation_to_point(self.goal_x, self.goal_y)

		if distance > 30 and abs(angle) < math.pi / 12:

			return 'drive_slow'
		elif distance > 50 and abs(angle) > 11 * math.pi / 12:
			return 'backwards'

		if abs(angle) > math.pi / 9:
				if abs(angle) > math.pi / 4:
					if angle > 0:
						return 'turn_left'
					elif angle < 0:
						return 'turn_right'
				else:
					if angle > 0:
						return 'turn_left_slow'
					elif angle < 0:
						return 'turn_right_slow'


		elif distance < 30 and abs(angle_to_goal) < math.pi / 9:
			self.our_attacker.catcher = 'open'
			return 'kick'

		elif distance < 30 and abs(angle_to_goal) > math.pi / 9:

			if angle_to_goal > 0:
				return 'turn_left_slow'
			elif angle_to_goal < 0:
				return 'turn_right_slow'


class DefenderIntercept:
	def __init__(self, world):
		self.world = world

		self.DISTANCE_THRESH = 15
		self.ANGLE_THRESH = math.pi / 12

		self.our_attacker = world.our_attacker
		self.ball = world.ball
		self.zone = world._pitch._zones[self.world.our_attacker.zone]
		min_x, max_x, min_y, max_y = self.zone.boundingBox()
		self.our_defender = world.our_defender
		self.our_attacker = world.our_attacker
		self.their_defender = world.their_defender
		self.their_attacker = world.their_attacker


	


	def pick_action(self):


		if self.ball.velocity > 0.5:
			if 	self.our_defender.catcher == 'open':
				self.our_defender.catcher = 'closed'
				return 'grab'
			if self.ball.y > self.world.our_goal.y + 45 and self.ball.y < self.world.our_goal.y+ self.world.our_goal.height -45:
				y=self.ball.y
			else:
				top_diff =  self.ball.y -  self.world.our_goal.y+ self.world.our_goal.height
				bottom_diff = 	self.world.our_goal.y - self.ball.y

				if top_diff > bottom_diff:
					y = self.world.our_goal.y
				else:
					y = self.world.our_goal.y+ self.world.our_goal.height


			distance, angle = self.our_defender.get_direction_to_point(self.our_defender.x, self.ball.y)
			print distance, '  ', angle
			return self.calculate_motor_speed(distance, angle)
		else:
			print self.ball.velocity    	


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


class DefenderGrab:
	def __init__(self, world):
		self.world = world

		self.DISTANCE_THRESH = 15
		self.ANGLE_THRESH = math.pi / 12

		self.our_attacker = self.world.our_attacker
		self.ball = self.world.ball
		self.zone = self.world._pitch._zones[self.world.our_attacker.zone]
		min_x, max_x, min_y, max_y = self.zone.boundingBox()
		self.center_x = (min_x + max_x) / 2
		self.center_y = (min_y + max_y) / 2
		self.goal_x = self.world.their_goal.x
		self.goal_y = self.world.their_goal.y + self.world.their_goal.height / 2

		self.our_defender = self.world.our_defender
		self.our_attacker = self.world.our_attacker
		self.their_defender = self.world.their_defender
		self.their_attacker = self.world.their_attacker
		self.ball = self.world.ball





	def pick_action(self):

		distance, angle = self.our_defender.get_direction_to_point(self.ball.x, self.ball.y)

		


		if self.our_defender.can_catch_ball(self.ball):
			self.our_defender.catcher = 'closed'
			return 'grab'

		elif not (distance is None):


			if abs(angle) > math.pi / 12:
				if abs(angle) > math.pi / 4:
					if angle > 0:
						return 'turn_left'
					elif angle < 0:
						return 'turn_right'
				else:
					if angle > 0:
						return 'turn_left_slow'
					elif angle < 0:
						return 'turn_right_slow'

			elif distance > 100:
				return 'drive'

			else:
				return 'drive_slow'



class DefenderPass:
	def __init__(self, world):
		self.world = world

		self.DISTANCE_THRESH = 15
		self.ANGLE_THRESH = math.pi / 12

		self.our_attacker = self.world.our_attacker
		self.ball = self.world.ball
		self.zone = self.world._pitch._zones[self.world.our_attacker.zone]
		min_x, max_x, min_y, max_y = self.zone.boundingBox()
		self.center_x = (min_x + max_x) / 2
		self.center_y = (min_y + max_y) / 2
		self.goal_x = self.world.their_goal.x
		self.goal_y = self.world.their_goal.y + self.world.their_goal.height / 2

		self.our_defender = self.world.our_defender
		self.our_attacker = self.world.our_attacker
		self.their_defender = self.world.their_defender
		self.their_attacker = self.world.their_attacker
		self.ball = self.world.ball





	def pick_action(self):

		distance, angle = self.our_defender.get_direction_to_point(self.center_x, self.center_y)
		angle_to_goal = self.our_defender.get_rotation_to_point(self.goal_x, self.goal_y)

		if distance < 30 and angle_to_goal < math.pi / 12:
			self.our_defender.catcher = 'open'
			return 'kick'

		elif distance < 30 and angle_to_goal > math.pi / 12:

			if angle_to_goal > 0:
				return 'turn_left'
			elif angle_to_goal < 0:
				return 'turn_right'

		elif distance > 30 and angle < math.pi / 12:

			return 'drive_slow'
		elif distance > 50 and angle > 11 * math.pi / 12:
			return 'backwards'

		elif distance > 30 and angle > math.pi / 12:

			if angle > 0:
				return 'turn_left'
			elif angle < 0:
				return 'turn_right'