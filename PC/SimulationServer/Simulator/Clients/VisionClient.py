from math import pi
import socket
import struct

MESSAGE_LENGTH=30

RQ_BLUE = 1
RQ_YELLOW = 2
RQ_RED = 3
RQ_DIMENSIONS = 4
RQ_FPS = 5

class VisionClient:
    def __init__(self, tryPort=31410, host=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        h = host if host != None else socket.gethostname()
        p = tryPort
        connected = False
        while not connected:
            try:
                s.connect((h, p))
                connected = True
            except socket.error:
                p += 1
        self._socket = s

    def getBlueBot(self):
        self.sendLine(struct.pack('b', RQ_BLUE))
        (type, x, y, tp, ta, a) = self.receive()
        assert type == 'b', "Wrong type returned: expected 'b'; given %s"%type
        return (x, y, a+pi, tp, ta)

    def getYellowBot(self):
        self.sendLine(struct.pack('b', RQ_YELLOW))
        (type, x, y, tp, ta, a) = self.receive()
        assert type == 'y', "Wrong type returned: expected 'y'; given %s"%type
        return (x, y, a+pi, tp, ta)

    def getBall(self):
        self.sendLine(struct.pack('b', RQ_RED))
        (type, x, y, _, ta, _) = self.receive()
        assert type == 'r', "Wrong type returned: expected 'r'; given %s"%type
        return (x, y, ta)

    def getFps(self):
        self.sendLine(struct.pack('b', RQ_FPS))
        (type, x) = self.receive_fps()
        assert type == 'f', "Wrong type returned: expected 'f'; given %s"%type
        return x

    def getDimensions(self):    # returns (w,h)
        self.sendLine(struct.pack('b', RQ_DIMENSIONS))
        (type, cx, cy, dx, dy) = self.receiveDims()
        return (dx*2, dy*2)

    def receive(self):
        data = self._socket.recv(MESSAGE_LENGTH)
        assert len(data) == MESSAGE_LENGTH, "Wrong length, expected %d given %d"%(MESSAGE_LENGTH, len(data))
        return struct.unpack('cHHddf', data[:-2])

    def receiveDims(self):
        data = self._socket.recv(12)
        assert len(data) == 12, "Wrong length, expected 12 given %d"%len(data)
        return struct.unpack('cHHHH', data[:-2])
    # }

    def receive_fps(self):
        data = self._socket.recv(10)
        assert len(data) == 10, "Wrong length, expected %d given %d"%(10, len(data))
        return struct.unpack('cf', data[:-2])

    def sendLine(self, content):
        toSend = "%s\r\n" % content
        self._socket.send(toSend)
