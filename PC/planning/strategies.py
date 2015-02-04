from utilities import *
import math
from random import randint


class AttackerGrab(role):


    def __init__(self, world):
        super(AttackerGrab, self).__init__(world, self.STATES)

	
        self.our_attacker = self.world.our_attacker
        self.ball = self.world.ball

    def generate(self):

	
        if self.our_attacker.catcher == 'closed':
            self.our_attacker.catcher = 'open'
            return 'open_catcher'

        displacement, angle = self.our_attacker.get_direction_to_point(self.ball.x, self.ball.y)
        elif self.our_attacker.can_catch_ball(self.ball):
            
            return 'grab'
       
	 elif:
            return calculate_motor_speed(displacement, angle)

    def calculate_motor_speed(distance, angle):
    '''
    Simplistic view of calculating the speed: no modes or trying to be careful
    '''

      angle_thresh = pi/7
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
