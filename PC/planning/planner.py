from models import *
from collisions import *
from strategies import *
from utilities import *


class Planner:

	def __init__(self, our_side, pitch_num, our_color):
		self._world = World(our_side, pitch_num)
		self._world.our_defender.catcher_area = {'width' : 30, 'height' : 30, 'front_offset' : 5} 
		self._world.our_attacker.catcher_area = {'width' : 35, 'height' : 30, 'front_offset' : 12} 
		self._world.our_defender.catcher='open'
		self.our_side = our_side
		#needs to be checked

			

		self.defender_intercept_strategy= DefenderIntercept(self._world)
		self.defender_grab_strategy= DefenderGrab(self._world)
		self.defender_pass_strategy= DefenderPass(self._world)
		self.BALL_VELOCITY_THRESH = 10	
	  
	def update_world(self, position_dictionary):
		self._world.update_positions(position_dictionary)

	def plan(self):
		
		our_defender = self._world.our_defender
		our_attacker = self._world.our_attacker
		their_defender = self._world.their_defender
		their_attacker = self._world.their_attacker
		ball = self._world.ball

		
		print ""
		if self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) == False:
			self._robot_current_strategy = self.defender_intercept_strategy
			return self._robot_current_strategy.pick_action() 
		elif self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) and our_defender.has_ball(ball) == False:
			print 'DefenderGrab'
			self._world.our_defender.catcher_area = {'width' : 35, 'height' : 30, 'front_offset' : 8}           
			self._robot_current_strategy = self.defender_grab_strategy
			return self._robot_current_strategy.pick_action()
		elif our_defender.has_ball(ball):
			print 'DefenderPass'   
			self._world.our_defender.catcher_area = {'width' : 100, 'height' : 100, 'front_offset' : -40} 
			self._robot_current_strategy = self.defender_pass_strategy
			return self._robot_current_strategy.pick_action()

		
		
