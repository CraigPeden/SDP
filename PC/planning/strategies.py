import math
from random import randint


class AttackerGrabShoot:


    def __init__(self, world):
        self.world = world

	
        self.our_attacker = self.world.our_attacker
        self.ball = self.world.ball
        zone = self.world._pitch._zones[self.world.our_attacker.zone]
        min_x, max_x, min_y, max_y  = zone.boundingBox()
        self.center_x = (min_x + max_x)/2
        self.center_y = (min_y + max_y)/2
        self.goal_x = self.world.our_goal.x
        self.goal_y = self.world.out_goal.y + self.world.our.goal.height()/2
	

    def pick_action(self):

	if self.has_ball(self.ball):
		#We have the ball so we need to get into a shooting position and shoot
		distance_to_zone_center = self.our_attacker.get_displacement_to_point(self.center_x, self.center_y)
		if distance_to_zone_center < 20:
			#We have reached the center of the zone
			angle_to_goal = self.our_attacker.get_rotation_to_point(self.goal_x, self.goal_y)
			if math.abs(angle_to_goal) < pi/12:
				return 'kick'
			elif angle_to_goal < 0:
				return 'turn_right'
			else:
				return 'turn_left'
		else:
			displacement, angle = self.our_attacker.get_direction_to_point(self.center_x, self.center_y)
			return self.calculate_motor_speed(displacement, angle)
	else:
		
	#if our catcher is closed than we will open it since our goal is to grab the ball
        	if self.our_attacker.catcher == 'closed':
            		self.our_attacker.catcher = 'open'
            		return 'open_catcher'

        	displacement, angle = self.our_attacker.get_direction_to_point(self.ball.x, self.ball.y)
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
              elif angle <0 :
                return 'turn_right'

          else:
           
             return 'drive'
