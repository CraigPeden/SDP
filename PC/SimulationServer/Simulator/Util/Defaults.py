from ..Simulation import Simulation
from ..Model.WorldObjects import Robot, Ball
from ..Params import Params

from math import pi

(w, h) = Params.pitchSize

objects = { 'ball'   : Ball((w/2, h/2), (0, 0))
          , 'blue'   : Robot((60, h/2), (0, 0), 0, "blue")
          , 'yellow' : Robot((w-60, h/2), (0, 0), pi, "yellow")
          }

def basicSim():
    return Simulation(objects)
def nonDrawingSim():
    return Simulation(objects, draw=False)
