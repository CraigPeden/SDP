import math
import time


class DefenderGrab:
	def __init__(self, world, comm):
		self.world = world

		self.our_defender = self.world.our_defender
		self.ball = self.world.ball
		self.last_kicker_action = time.time()
		self.zone = world._pitch._zones[self.world.our_defender.zone]
		min_x, max_x, min_y, max_y = self.zone.boundingBox()
		self.center_y = (max_y + min_y)/2

		self.comm = comm


	def pick_action(self):

		distance, angle = self.our_defender.get_direction_to_point(self.ball.x, self.ball.y)
		print 'Can catch ball:' + str(self.our_defender.can_catch_ball(self.ball))
		print 'Catcher closed:' + self.our_defender.catcher

		if self.comm.grabberArmed() == False and self.hasBall() == False:
			self.comm.grab()

		if not self.comm.hasBall() and self.our_defender.catcher == 'closed':

			self.our_defender.catcher = 'open'
			return [('open_catcher', 1)]

		opponent_zone = self.world._pitch._zones[self.world.their_attacker.zone]
		min_x, max_x, min_y, max_y = opponent_zone.boundingBox()
		angle_to_opponent_zone = self.our_defender.get_rotation_to_point((max_x - min_x)/2, self.our_defender.y)

		if self.comm.hasGrabbed() and self.our_defender.catcher == 'open' and abs(self.ball.y - self.center_y)>80 and abs(angle_to_opponent_zone) > math.pi/4:

			self.our_defender.catcher = 'closed'
			return [('stop', 1), ('backwards', 1)]	

		if self.comm.hasBall() and self.our_defender.catcher == 'open':

			self.our_defender.catcher = 'closed'
			return 'stop'

		#if not self.our_defender.can_catch_ball(self.ball) and self.our_defender.catcher == 'closed':

		#	self.our_defender.catcher = 'open'
		#	return 'open_catcher'

		elif not (distance is None):
		
			if abs(angle) > math.pi / 18:
				if angle > 0:
					return [('turn_left', 0.2), ('stop', 0)]
				elif angle < 0:
					return [('turn_right', 0.2), ('stop', 0)]

			elif distance > 120:
				return 'drive'

			else:
				return [('drive_slow', 0.3), ('stop', 0)]





class DefenderIntercept:
	def __init__(self, world, our_side):
		self.world = world
		self.our_side = our_side
		self.zone = world._pitch._zones[self.world.our_defender.zone]
		min_x, max_x, min_y, self.max_y = self.zone.boundingBox()

		if self.our_side == 'left':
			self.center_x = ((min_x+max_x)/2) -10
		else:
			self.center_x = ((min_x+max_x)/2) +10	

		self.DISTANCE_THRESH = 15
		self.ANGLE_THRESH = math.pi / 12

		self.ball = world.ball
		self.our_defender = world.our_defender
		self.our_attacker = world.our_attacker
		self.their_defender = world.their_defender
		self.their_attacker = world.their_attacker



	def predict_y_intersection(self, world, predict_for_x, robot):
		
		x = robot.x
		y = robot.y
		#print x, y
		top_y = world.our_goal.y + (world.our_goal.width/2) - 15
		bottom_y = world.our_goal.y - (world.our_goal.width/2) + 15
		angle = robot.angle
		if (robot.x < predict_for_x and not (math.pi/2 < angle < 3*math.pi/2)) or (robot.x > predict_for_x and (3*math.pi/2 > angle > math.pi/2)):
			predicted_y = (y + math.tan(angle) * (predict_for_x - x))
		# Correcting the y coordinate to the closest y coordinate on the goal line:
			if predicted_y > top_y:
				return max((top_y + robot.y)/2, top_y)
			elif predicted_y < bottom_y:
				return min((bottom_y + robot.y)/2, bottom_y)
			return predicted_y
		else:
			return None


	


	def pick_action(self):


		self.predicted_y_intersecton = self.predict_y_intersection(self.world, self.center_x, self.their_attacker)
		self.predicted_y_intersecton_other_defender = self.predict_y_intersection(self.world, self.center_x, self.their_defender)
		
		if self.ball.velocity > 3 :
			top_y = self.world.our_goal.y + (self.world.our_goal.width/2)
			bottom_y = self.world.our_goal.y - (self.world.our_goal.width/2)
			center_y = (top_y +bottom_y)/2
			y = (self.ball.y + center_y)/2


		elif self.predicted_y_intersecton == None:
			if self.ball.y > 80 and self.ball.y < 215:
				y=(self.ball.y+150)/2
			elif self.ball.y < 80:
				y=95
			else: 
				y=180

		elif self.predicted_y_intersecton_other_defender == None and self.world.pitch.zones[self.their_defender.zone].isInside(self.ball.x, self.ball.y) == True:
			if self.ball.y > 80 and self.ball.y < 215:
				y=(self.ball.y+150)/2
			elif self.ball.y < 80:
				y=95
			else: 
				y=180

		elif self.world.pitch.zones[self.their_defender.zone].isInside(self.ball.x, self.ball.y) == True:
			print 'Predicting Intersection'
			y = self.predicted_y_intersecton_other_defender
		
		else:
			print 'Predicting Intersection'
			y = self.predicted_y_intersecton

	
			
		distance, angle = self.our_defender.get_direction_to_point(self.center_x, y)
		print self.center_x, y
		return self.calculate_motor_speed(distance, angle)
		   	


	def calculate_motor_speed(self, distance, angle):
		angle_thresh = math.pi / 4
		direction_threshhold = math.pi/6
		distance_threshhold = 30
		angle_align = self.our_defender.get_rotation_to_point(self.our_defender.x, self.max_y) 


		if not (distance is None):

			

			if distance < distance_threshhold:
				if abs(angle_align) < math.pi/15: 
					return 'stop'
				elif abs(angle_align) < math.pi/6:
					if angle_align > 0:
						return [('turn_left', 0.2), ('stop', 0.2)]
					elif angle_align < 0:
						return [('turn_right', 0.2), ('stop', 0.2)]
				else:
					if angle_align > 0:
						return 'turn_left_slow'
					elif angle_align < 0:
						return 'turn_right_slow'


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
	def __init__(self, world, our_side, pitch_num):
		self.world = world
		self.our_side = our_side
		self.pitch_num = pitch_num

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

		self.opponent_zone = self.world._pitch._zones[self.world.their_attacker.zone]
		self.opp_min_x, self.opp_max_x, self.opp_min_y, self.opp_max_y = self.opponent_zone.boundingBox()

		#if self.pitch_num == 0 and self.our_side == 'left':
			#self.opp_max_x = self.opp_max_x - 30
			#print 'Opponent max x:'







	def pick_action(self):

		distance_between_robots = self.our_defender.y - self.their_attacker.y


		if self.their_attacker.y < self.center_y:
			if self.our_side == 'left':
				angle_to_pass_point = self.our_defender.get_rotation_to_point(self.opp_max_x, self.opp_max_y)
			else:
				angle_to_pass_point = self.our_defender.get_rotation_to_point(self.opp_min_x, self.opp_max_y)
		else:
			if self.our_side == 'left':
				angle_to_pass_point = self.our_defender.get_rotation_to_point(self.opp_max_x, self.opp_min_y)
			else:
				angle_to_pass_point = self.our_defender.get_rotation_to_point(self.opp_min_x, self.opp_min_y)

			

		distance, angle = self.our_defender.get_direction_to_point(self.center_x, self.center_y)
		
		print 'Can catch ball:' + str(self.our_defender.can_catch_ball(self.ball))
		print 'Catcher closed:' + self.our_defender.catcher

		# When catching the ball if their attack is far from us, we shoot 
		if distance_between_robots > 150:
			print 'Direct Pass'
			angle_to_pass = self.our_defender.get_rotation_to_point(self.our_attacker.x, self.our_attacker.y)
			if abs(angle_to_pass) > math.pi/12:
				if angle_to_pass>0:
					return [('turn_left_slow', 0.3), ('stop', 0)]
				else:
					return [('turn_right_slow', 0.3), ('stop', 0)]
			else:
				self.our_defender.catcher = 'open'
				return [('open_catcher', 0.5), ('kick', 1)]



		if distance < 35 and abs(angle_to_pass_point) < math.pi / 27:
			self.our_defender.catcher = 'open'
			return [('open_catcher', 0.5), ('kick', 1)]

		elif distance < 35 and abs(angle_to_pass_point) > math.pi / 27:

			if angle_to_pass_point > 0:
				return [('turn_left_slow', 0.2), ('stop', 0)]
				#return [('turn_left', 0.2), ('stop', 0.2)]
			elif angle_to_pass_point < 0:
				return [('turn_right_slow', 0.2), ('stop', 0)]
				#return [('turn_right', 0.2), ('stop', 0.2)]

		elif distance > 20 and abs(angle) < math.pi / 12:

			return 'drive_slow'
		elif distance > 20 and abs(angle) >  math.pi / 2:
			return 'backwards'

		elif distance > 20 and abs(angle) <  math.pi / 2:

			if angle > 0:
				return [('turn_left', 0.2), ('stop', 0.1)]
			elif angle < 0:
				return [('turn_right', 0.2), ('stop', 0.1)]



class DefenderSave:
	def __init__(self, world, our_side):
		self.world = world
		self.our_side = our_side

		self.our_defender = self.world.our_defender
		self.ball = self.world.ball
		self.last_kicker_action = time.time()
		self.zone = world._pitch._zones[self.world.our_defender.zone]
		self.min_x, self.max_x, self.min_y, self.max_y = self.zone.boundingBox()
		self.center_y = (self.max_y + self.min_y)/2


	def pick_action(self):

		top_y = self.world.our_goal.y + (self.world.our_goal.width/2)
		bottom_y = self.world.our_goal.y - (self.world.our_goal.width/2) 
		if self.our_side == 'left':
			fixed_x = self.min_x + 10
		else:
			fixed_x =  self.max_x - 10

		if self.ball.y > self.center_y:
			fixed_y = bottom_y
		else:
			fixed_y = top_y	

		print fixed_x, '  ',   fixed_y	
				
		distance, angle = self.our_defender.get_direction_to_point(fixed_x, fixed_y)
		print 'Can catch ball:' + str(self.our_defender.can_catch_ball(self.ball))
		print 'Catcher closed:' + self.our_defender.catcher

		if not (distance is None):


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



