from models import *
from collisions import *
from strategies import *
from utilities import *


class Planner:

    def __init__(self, our_side, pitch_num, our_color):
		self._world = World(our_side, pitch_num)
		self._world.our_defender.catcher_area = {'width' : 40, 'height' : 45, 'front_offset' : 12} #10
		self._world.our_attacker.catcher_area = {'width' : 20, 'height' : 30, 'front_offset' : 14}
		self._world.our_attacker.catcher='open'
		self.our_side = our_side
		self.our_color = our_color
		#needs to be checked
		if (our_side == 'left' and our_color == 'blue'):
			self.robot_role = 'attacker'
		elif (our_side == 'left' and our_color == 'yellow'):
			self.robot_role = 'attacker'
		elif (our_side == 'right' and our_color == 'blue'):
			self.robot_role = 'attacker'
		elif (our_side == 'right' and our_color == 'yellow'):
			self.robot_role = 'attacker'
			
		self.attacker_grab_strategy = AttackerGrab(self._world)
		self.attacker_shoot_strategy= AttackerShoot(self._world)
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
			if self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y):
				if self._world.ball.velocity > self.BALL_VELOCITY_THRESH and our_defender.has_ball(ball) == False:
					print 'DefenderIntercept'					
					self._robot_current_strategy = self.attack_strategy
					return self._robot_current_strategy.pick_action()
				else:
					self._robot_current_strategy = self.attack_strategy
					print 'DefenderGrabPass'	
					return self._robot_current_strategy.pick_action()
			else:
				self._robot_current_strategy = self.attack_strategy
				print 'DefenderGrabPass'
				return self._robot_current_strategy.pick_action()
		

		elif self.robot_role == 'attacker':
			#Our robot is an attacker
			if self._world.pitch.zones[our_attacker.zone].isInside(ball.x, ball.y):
				if our_attacker.has_ball(ball):
					print 'AttackerShoot'
					self._robot_current_strategy = self.attacker_shoot_strategy
					return self._robot_current_strategy.pick_action()
				else:
					print 'AttackerGrab'
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
