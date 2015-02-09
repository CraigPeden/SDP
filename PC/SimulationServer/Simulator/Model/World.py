from collections import deque
import operator

from ..Clients import VisionClient
from ..Funcs.Funcs import weightNorm, vecSub

def getVel(history):
    """ Finds velocity vector of the robot, given previous positions. 
    Uses parameter to weigh how important the previous positions are. """
    try:
        coef = [0.05, 0.1, 0.25, 0.6]
        if len(history) < 5:
            return (0,0)

        positions = map(lambda x: x[:2], history)
        timestamps = map(lambda x: x[-1], history)
        dpos = map(vecSub, positions[1:], positions[:-1])
        dts = map(operator.sub, timestamps[1:], timestamps[:-1])
        vels = map(lambda (dx, dy), dt: (dx/dt, dy/dt), dpos, dts)
        out = vels[-1]
        return out
    except Exception, e:
        print "EXCEPTION, %s" % e

def appendIfNew(list, item):
    try:
        if len(item) == 5:          # robot
            timestamp_position = item[-2]
            old_position = list[-1][-2]
            if timestamp_position != old_position:
                list.append(item)
        else:                       # ball
            timestamp = item[-1]
            old_timestamp = list[-1][-1]
            if timestamp != old_timestamp:
                list.append(item)
    except IndexError:
        # Presumably it's the first item added
        list.append(item)

def getPosition(history):
    return history[-1][:2]

def getAngle(history):
    return history[-1][2]

def getAll(history):
    return history[-1][:3]

class World:
    blueRobot = deque(maxlen=5)
    yellowRobot = deque(maxlen=5)
    ball = deque(maxlen=5)
    _vc = None
    def __init__(self, vc=None):
        if vc:
            self._vc = vc
        else:
            self._vc = VisionClient()

    def updateBlue(self, out=None):
        pos = self._vc.getBlueBot()
        appendIfNew(self.blueRobot, list(pos))

    def getBluePosition(self):
        return getPosition(self.blueRobot)

    def getBlueAngle(self):
        return getAngle(self.blueRobot)

    def getBlueVelocity(self):
        return getVel(self.blueRobot)

    def getBlue(self, out=None):
        data = getAll(self.blueRobot)
        if out:
            out[0] = data[0]
            out[1] = data[1]
            out[2] = data[2]
        else:
            return data

    def getYellowPosition(self):
        return getPosition(self.yellowRobot)

    def updateYellow(self):
        pos = self._vc.getYellowBot()
        appendIfNew(self.yellowRobot, list(pos))

    def getYellowAngle(self):
        return getAngle(self.yellowRobot)

    def getYellowVelocity(self):
        return getVel(self.yellowRobot)

    def getYellow(self, out=None):
        data = getAll(self.yellowRobot)
        if out:
            out[0] = data[0]
            out[1] = data[1]
            out[2] = data[2]
        else:
            return data

    def updateBall(self):
        pos = self._vc.getBall()
        appendIfNew(self.ball, list(pos))

    def getBallPosition(self):
        return getPosition(self.ball)

    def getBallVelocity(self):
        return getVel(self.ball)

    def getBall(self, out=None):
        data = getAll(self.ball)
        if out:
            out[0] = data[0]
            out[1] = data[1]
        else:
            return data

    def updateAll(self):
        map(lambda f: f(), [self.updateBlue, self.updateYellow, self.updateBall])

    def getDimensions(self):
        return self._vc.getDimensions()
