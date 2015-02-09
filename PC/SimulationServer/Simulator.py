""" An executable that runs the simulation as a drop-in replacement for the real-world pitch and robots """
from math import pi
from optparse import OptionParser

import pymunk
import pygame
from twisted.internet import reactor

from Simulator.Drawing.Drawing import green
from Simulator.Model.WorldObjects import Ball, Robot, Pitch, CT_LEFT_GOAL, CT_BALL, CT_RIGHT_GOAL
from Simulator.Params import Params
from Simulator.Simulation import Simulation
from Simulator.Servers.VisionServer import VisionServerStarter
from Simulator.Servers.CommsServer import CommsServerFactory


parser = OptionParser()

parser.add_option( "-f", "--frame-rate"
                 , dest="fps"
                 , action="store"
                 , type="int"
                 , help="Which framerate the server runs at"
                 , default=25
                 )
(options, args) = parser.parse_args()

(w, h) = Params.pitchSize

objects = {}
objects['ball'] = Ball((w/2, h/2), (0, 0))

objects['blue'] = Robot((60, h/2), (0,0), 0, "blue")

objects['yellow'] = Robot((w-60, h/2), (0,0), pi, "yellow")

simulation = Simulation(objects, draw=True)
def goal_scored(simulation, space, arbiter, obj, goal):
    simulation.reset()
    robot_string = "Yellow" if goal == CT_LEFT_GOAL else "Blue"
    print "%s robot scored!" % robot_string
    return True

simulation.addGoalCollisionFunc(goal_scored, objects['ball'], CT_LEFT_GOAL)
simulation.addGoalCollisionFunc(goal_scored, objects['ball'], CT_RIGHT_GOAL)

vss = VisionServerStarter(simulation, options.fps * 5)  #FIXME: Multiplying by 5, because FPS is not correct - suspect that 5 clients connect
vss.start(31410)
csf = CommsServerFactory(simulation)
csf.start()

simulation.start()

while not simulation.done.value:
    pass
