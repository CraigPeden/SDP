from multiprocessing import Process, Array, Value

from Model.World import World
from Model.WorldObjects import Robot, Ball
from Simulation import Simulation

class VisionWrapper:
    world = None
    blue = Array('f', range(3))
    yellow = Array('f', range(3))
    ball = Array('f', range(2))
    dims = Array('i', range(2))
    sim = None
    def __init__(self, sim):
        self.world = World()
        self.sim = sim
        self.done = sim.done
        self._run_subprocess()

    def _run_subprocess(self):
        self._subp = Process(target=self.mainLoop)
        self._subp.start()

    def mainLoop(self):
        dims = self.world.getDimensions()
        self.dims[0] = dims[0]
        self.dims[1] = dims[1]
        while not self.done.value:
            self.world.updateAll()
            self.keyframe()


    def keyframe(self):
        w = self.world
        keyframe = { 'blue' : { 'position' : w.getBluePosition()
                              , 'angle'    : w.getBlueAngle()
                              , 'velocity' : w.getBlueVelocity()
                              }
                   , 'yellow':{ 'position' : w.getYellowPosition()
                              , 'angle'    : w.getYellowAngle()
                              , 'velocity' : w.getYellowVelocity()
                              }
                   , 'ball' : { 'position' : w.getBallPosition()
                              , 'velocity' : w.getBallVelocity()
                              , 'angle'    : 0
                              }
                   }
        self.sim.keyFrame(keyframe, external=True)

    def getBlueBot(self):
        return self.sim.getBlueBot()

    def getBlueRobot(self):
        return self.getBlueBot()

    def getYellowBot(self):
        return self.sim.getYellowBot()

    def getYellowRobot(self):
        return self.getYellowBot()

    def getBall(self):
        return self.sim.getBall()

    def getDimensions(self):
        return tuple(self.dims)
