from models import *
from collisions import *
from strategies import *
from utilities import *


class Planner:

    def __init__(self, our_side, pitch_num, our_color, our_role):
		self._world = World(our_side, pitch_num)
		self._world.our_defender.catcher_area = {'width' : 40, 'height' : 45, 'front_offset' : 12} #10
		self._world.our_attacker.catcher_area = {'width' : 35, 'height' : 30, 'front_offset' : 14}
		self._world.our_attacker.catcher='open'
		self.our_side = our_side
		self.our_color = our_color
		self.robot_role = our_role
		#needs to be checked

			
		self.attacker_grab_strategy = AttackerGrab(self._world)
		self.attacker_shoot_strategy= AttackerShoot(self._world)
		self.defender_intercept_strategy= DefenderIntercept(self._world)
		self.BALL_VELOCITY_THRESH = 10	
      
    def update_world(self, position_dictionary):
        self._world.update_positions(position_dictionary)

    def plan(self):
    	
		our_defender = self._world.our_defender
		our_attacker = self._world.our_attacker
		their_defender = self._world.their_defender
		their_attacker = self._world.their_attacker
		ball = self._world.ball
		
		if self.robot_role == 'defender':
			#Our robot is a defender
					print 'DefenderIntercept'					
					self._robot_current_strategy = self.defender_intercept_strategy
					return self._robot_current_strategy.pick_action()
		

		elif self.robot_role == 'attacker':
			#Our robot is an attacker
			if self._world.pitch.zones[our_attacker.zone].isInside(ball.x, ball.y):
				if our_attacker.has_ball(ball):
					print 'AttackerShoot'
					print our_attacker.catcher
					self._world.our_attacker.catcher_area = {'width' : 40, 'height' : 40, 'front_offset' : 10}
					self._robot_current_strategy = self.attacker_shoot_strategy
					return self._robot_current_strategy.pick_action()
				else:
					print 'AttackerGrab'
					print our_attacker.catcher
					self._world.our_attacker.catcher_area = {'width' : 30, 'height' : 35, 'front_offset' : 14}
					self._robot_current_strategy = self.attacker_grab_strategy
					return self._robot_current_strategy.pick_action()
		
			
"""
        else:
            # If the ball is in their defender zone we defend:
            if self._world.pitch.zones[their_defender.zone].isInside(ball.x, ball.y):
                if not self._attacker_state == 'defence':
                    self._attacker_state = 'defence'
                    self._attacker_current_strategy = self.choose_attacker_strategy(self._world)
                return self._attacker_current_strategy.generate()

            # If ball is in our attacker zone, then grab the ball and score:
            elif self._world.pitch.zones[our_attacker.zone].isInside(ball.x, ball.y):

                # Check if we should switch from a grabbing to a scoring strategy.
                if self._attacker_state == 'grab' and self._attacker_current_strategy.current_state == 'GRABBED':
                    self._attacker_state = 'score'
                    self._attacker_current_strategy = self.choose_attacker_strategy(self._world)

                elif self._attacker_state == 'grab':
                    # Switch to careful mode if the ball is too close to the wall.
                    if abs(self._world.ball.y - self._world.pitch.height) < 0 or abs(self._world.ball.y) < 0:
                        if isinstance(self._attacker_current_strategy, AttackerGrab):
                            self._attacker_current_strategy = AttackerGrabCareful(self._world)
                    else:
                        if isinstance(self._attacker_current_strategy, AttackerGrabCareful):
                            self._attacker_current_strategy = AttackerGrab(self._world)

                # Check if we should switch from a defence to a grabbing strategy.
                elif self._attacker_state in ['defence', 'catch'] :
                    self._attacker_state = 'grab'
                    self._attacker_current_strategy = self.choose_attacker_strategy(self._world)

                elif self._attacker_state == 'score' and self._attacker_current_strategy.current_state == 'FINISHED':
                    self._attacker_state = 'grab'
                    self._attacker_current_strategy = self.choose_attacker_strategy(self._world)

                return self._attacker_current_strategy.generate()
            # If the ball is in our defender zone, prepare to catch the passed ball:
            elif self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) or \
                 self._attacker_state == 'catch':
                 # self._world.pitch.zones[their_attacker.zone].isInside(ball.x, ball.y):
                if not self._attacker_state == 'catch':
                    self._attacker_state = 'catch'
                    self._attacker_current_strategy = self.choose_attacker_strategy(self._world)
                return self._attacker_current_strategy.generate()
            else:
                return calculate_motor_speed(0, 0)
"""
