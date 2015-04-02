from models import *
from collisions import *
from strategies import *
from utilities import *



class Planner:

	def __init__(self, our_side, pitch_num, our_color, gui, comm):
		self._world = World(our_side, pitch_num)
		self.gui = gui
		self._world.our_defender.catcher_area = {'width' : 20, 'height' : self.gui.getCatcherArea(), 'front_offset' : 10} 
		self._world.our_attacker.catcher_area = {'width' : 35, 'height' : 30, 'front_offset' : 12} 
		self._world.our_defender.catcher='open'
		self.our_side = our_side
		self.comm = comm
		#needs to be checked

			

		self.defender_intercept_strategy= DefenderIntercept(self._world, our_side)
		self.defender_grab_strategy= DefenderGrab(self._world, self.comm)
		self.defender_save_strategy= DefenderSave(self._world, our_side)
		self.defender_pass_strategy= DefenderPass(self._world, our_side, pitch_num, self.comm)
		self.BALL_VELOCITY_THRESH = 10

		self.passing_action = time.time()
	  
	def update_world(self, position_dictionary):
		self._world.update_positions(position_dictionary)

	def plan(self):
		
		our_defender = self._world.our_defender
		our_attacker = self._world.our_attacker
		their_defender = self._world.their_defender
		their_attacker = self._world.their_attacker
		ball = self._world.ball
		self.zone = self._world._pitch._zones[self._world.our_defender.zone]
		min_x, max_x, min_y, max_y = self.zone.boundingBox()
		if self.our_side == 'left':
			fixed_x = min_x
		else:
			fixed_x = max_x	
		
		self.center_y = (max_y + min_y)/2
		top_y = self._world.our_goal.y + (self._world.our_goal.width/2)
		bottom_y = self._world.our_goal.y - (self._world.our_goal.width/2)

		print ""
		if (ball.y > bottom_y) and (ball.y > top_y) and self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) == True and abs(ball.x - fixed_x) < 30 and abs(our_defender.x - fixed_x) > 40 and ((self.center_y > our_defender.y and self.center_y > ball.y ) or (self.center_y < our_defender.y and self.center_y < ball.y )) :
			print 'DefenderSave'
			self._robot_current_strategy = self.defender_save_strategy
			return self._robot_current_strategy.pick_action() 

		elif self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) == False:
			print 'DefenderIntercept'
			self._robot_current_strategy = self.defender_intercept_strategy
			return self._robot_current_strategy.pick_action() 

		elif ball.velocity > 3 and self.comm.hasBall() == False:
			print 'DefenderIntercept'
			self._robot_current_strategy = self.defender_intercept_strategy
			return self._robot_current_strategy.pick_action() 			

		elif self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) and self.comm.hasBall() == False and self.passing_action + 2 < time.time():
			print 'DefenderGrab'
			self._world.our_defender.catcher_area = {'width' : 25, 'height' : self.gui.getCatcherArea(), 'front_offset' : 10}           
			self._robot_current_strategy = self.defender_grab_strategy
			return self._robot_current_strategy.pick_action()

		elif self.comm.hasBall():
			print 'DefenderPass'   
			self.passing_action = time.time()
			self._world.our_defender.catcher_area = {'width' : 100, 'height' : 100, 'front_offset' : -40} 
			self._robot_current_strategy = self.defender_pass_strategy
			return self._robot_current_strategy.pick_action()

		else:
			return 'stop'

		
		
