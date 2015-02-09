from multiprocessing import Process, Array, Value

from Model.World import World
from Model.WorldObjects import Robot, Ball
from Simulation import Simulation
from Funcs.Funcs import getWheelSpeeds


class StrategyWrapper:
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
            self.simpleStrategy()


    def simpleStrategy(self):
        """ Simple strategy used for simulation ahead - just follows the ball"""
        # simulates simple Follow-the-Ball strategy for both robots
        
        w       = self.world                
        blue    = self.sim.objects['blue']
        yellow  = self.sim.objects['yellow']
        bpos    = w.getBluePosition()
        borient = w.getBlueAngle()
        ypos    = w.getYellowPosition()
        yorient = w.getYellowAngle()
        
        gpos = w.getBallPosition()
        ym = getWheelSpeeds(ypos, yorient, gpos)
        bm = getWheelSpeeds(bpos, borient, gpos)
        blue.move(*bm)
        yellow.move(*ym)

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
