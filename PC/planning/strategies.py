import math
from random import randint
import time


class AttackerGrab:


	def __init__(self, world):
		self.world = world

	
		self.our_attacker = self.world.our_attacker
		self.ball = self.world.ball
		zone = self.world._pitch._zones[self.world.our_attacker.zone]
		min_x, max_x, min_y, max_y  = zone.boundingBox()

			

	def pick_action(self):

		distance, angle = self.our_attacker.get_direction_to_point(self.ball.x, self.ball.y)
		
		if self.our_attacker.can_catch_ball(self.ball):
			self.our_attacker.catcher='closed'
			return 'grab'

		elif not (distance is None):

			if abs(angle) > 11*math.pi/12:
				return 'backwards'

			if abs(angle) > math.pi/12:

				if angle > 0 :
					return 'turn_left'
				elif angle <0 :
					return 'turn_right'

			elif distance > 50 :
				return 'drive'
				
			else:
				return 'drive_slow'



class AttackerShoot:


	def __init__(self, world):
		self.world = world

	
		self.our_attacker = self.world.our_attacker
		self.ball = self.world.ball
		zone = self.world._pitch._zones[self.world.our_attacker.zone]
		min_x, max_x, min_y, max_y  = zone.boundingBox()
		self.goal_x=480
		self.goal_y=160
		self.center_x=315
		self.center_y=160

			

	def pick_action(self):

		distance, angle = self.our_attacker.get_direction_to_point(self.center_x, self.center_y)
		angle_to_goal = self.our_attacker.get_rotation_to_point(self.goal_x, self.goal_y)
		
		if distance < 30 and angle_to_goal < math.pi/12:
			self.our_attacker.catcher='open'
			return 'kick'

		elif distance < 30 and angle_to_goal > math.pi/12:

			if angle_to_goal > 0 :
				return 'turn_left'
			elif angle_to_goal <0 :
				return 'turn_right'

		elif distance > 30 and angle < math.pi/12:
			
			return 'drive_slow'
		elif distance > 50 and angle > 11*math.pi/12:
			return 'backwards'
		
		elif distance > 30 and angle > math.pi/12:

			if angle > 0 :
				return 'turn_left'
			elif angle <0 :
				return 'turn_right'










class DefenderIntercept:


    def __init__(self, world):
		self.world = world

		self.DISTANCE_THRESH = 15
		self.ANGLE_THRESH = math.pi/12

	
		self.our_attacker = world.our_attacker
		self.ball = world.ball
		self.zone = world._pitch._zones[self.world.our_attacker.zone]
		min_x, max_x, min_y, max_y  = self.zone.boundingBox()
		self.our_defender = world.our_defender
		self.our_attacker = world.our_attacker
		self.their_defender = world.their_defender
		self.their_attacker = world.their_attacker
	

    def predict_y_intersection(self, world, predict_for_x, robot, full_width=False, bounce=False):
        '''
        Predicts the (x, y) coordinates of the ball shot by the robot
        Corrects them if it's out of the bottom_y - top_y range.
        If bounce is set to True, predicts for a bounced shot
        Returns None if the robot is facing the wrong direction.
        '''
        x = robot.x
        y = robot.y
        top_y = world._pitch.height - 60 if full_width else world.our_goal.y + (world.our_goal.width/2) - 30
        bottom_y = 60 if full_width else world.our_goal.y - (world.our_goal.width/2) + 30
        angle = robot.angle
        predicted_y = (y + math.tan(angle) * (predict_for_x - x))
           
    	return predicted_y



    def pick_action(self):

		
		predicted_y = self.predict_y_intersection(self.world, self.our_defender.x, self.ball, bounce=False)
		distance, angle = self.our_defender.get_direction_to_point(self.our_defender.x, self.ball.y)
		print distance,'  ', angle
		return self.calculate_motor_speed(distance, angle)


	def calculate_motor_speed(self, distance, angle):
		angle_thresh = math.pi/7
		distance_threshhold = 15
		if not (distance is None):

		if distance < distance_threshhold:
			return 'stop'

		elif abs(angle) > angle_thresh:
			
				if angle > 0 :
					return 'turn_left'
				elif angle < 0 :
					return 'turn_right'
			else:
				return 'drive'
			

			
	
	


class DefenderGrabPass:


    def __init__(self, world):
        self.world = world

        self.DISTANCE_THRESH = 15
        self.ANGLE_THRESH = math.pi/12


        self.our_attacker = self.world.our_attacker
        self.ball = self.world.ball
        self.zone = self.world._pitch._zones[self.world.our_attacker.zone]
        min_x, max_x, min_y, max_y  = self.zone.boundingBox()
        self.center_x = (min_x + max_x)/2
        self.center_y = (min_y + max_y)/2
        self.goal_x = self.world.their_goal.x
        self.goal_y = self.world.their_goal.y + self.world.their_goal.height/2
            
        self.our_defender = self.world.our_defender
        self.our_attacker = self.world.our_attacker
        self.their_defender = self.world.their_defender
        self.their_attacker = self.world.their_attacker
        self.ball = self.world.ball
	

    def predict_y_intersection(world, predict_for_x, robot, full_width=False, bounce=False):
        '''
        Predicts the (x, y) coordinates of the ball shot by the robot
        Corrects them if it's out of the bottom_y - top_y range.
        If bounce is set to True, predicts for a bounced shot
        Returns None if the robot is facing the wrong direction.
        '''
        x = robot.x
        y = robot.y
        top_y = world._pitch.height - 60 if full_width else world.our_goal.y + (world.our_goal.width/2) - 30
        bottom_y = 60 if full_width else world.our_goal.y - (world.our_goal.width/2) + 30
        angle = robot.angle
        if (robot.x < predict_for_x and not (pi/2 < angle < 3*pi/2)) or (robot.x > predict_for_x and (3*pi/2 > angle > pi/2)):
            if bounce:
                if not (0 <= (y + tan(angle) * (predict_for_x - x)) <= world._pitch.height):
                    bounce_pos = 'top' if (y + tan(angle) * (predict_for_x - x)) > world._pitch.height else 'bottom'
                    x += (world._pitch.height - y) / tan(angle) if bounce_pos == 'top' else (0 - y) / tan(angle)
                    y = world._pitch.height if bounce_pos == 'top' else 0
                    angle = (-angle) % (2*pi)
            predicted_y = (y + tan(angle) * (predict_for_x - x))
            # Correcting the y coordinate to the closest y coordinate on the goal line:
            if predicted_y > top_y:
                return top_y
            elif predicted_y < bottom_y:
                return bottom_y
            return predicted_y
        else:
            return None



    def pick_action(self):

		if self.our_defender.has_ball(self.ball):
			#We have the ball so we need to get into a shooting position and pass
			distance_to_zone_center = self.our_attacker.get_displacement_to_point(self.center_x, self.center_y)
			if distance_to_zone_center < self.DISTANCE_THRESH:
				#We have reached the center of the zone
				angle_to_goal = self.our_defender.get_rotation_to_point(self.goal_x, self.goal_y)
				if math.abs(angle_to_goal) < self.ANGLE_THRESH:
					return 'kick'
				elif angle_to_goal < 0:
					return 'turn_right'
				else:
					return 'turn_left'
			else:
				displacement, angle = self.our_defender.get_direction_to_point(self.center_x, self.center_y)
				return self.calculate_motor_speed(displacement, angle)
		else:
		
		#if our catcher is closed than we will open it since our goal is to grab the ball
		    	if self.our_attacker.catcher == 'closed':
		    		self.our_attacker.catcher = 'open'
		    		return 'open_catcher'

				displacement, angle = self.our_defender.get_direction_to_point(self.ball.x, self.ball.y)
				if self.our_attacker.can_catch_ball(self.ball):
					return 'grab'
				
				else:
					return self.calculate_motor_speed(displacement, angle)



    def calculate_motor_speed(self, distance, angle):

        angle_thresh = math.pi/7
        distance_threshhold = 15

        if not (distance is None):

            if distance < distance_threshhold:
               return 'stop'

            elif abs(angle) > angle_thresh:
           
                if angle > 0 :
                    return 'turn_left'
                elif angle < 0 :
                    return 'turn_right'
            else:
               
                 return 'drive'
