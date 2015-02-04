import math
from random import randint


class AttackerGrab:


    def __init__(self, world):
        self.world = world

	
        self.our_attacker = self.world.our_attacker
        self.ball = self.world.ball

    def generate(self):

	
        if self.our_attacker.catcher == 'closed':
            self.our_attacker.catcher = 'open'
            return 'open_catcher'

        displacement, angle = self.our_attacker.get_direction_to_point(self.ball.x, self.ball.y)
        if self.our_attacker.can_catch_ball(self.ball):
            
            return 'grab'
       
	
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
