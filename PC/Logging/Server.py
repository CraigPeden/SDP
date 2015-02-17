import struct
from multiprocessing import Process

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

TAG = "LOGSERVER"

class LogServer(LineReceiver):
    log = None

    def __init__(self, log):
        self.log = log

    def connectionMade(self):
        self.log.log(TAG, "Connection made")

    def connectionLost(self, _):
        self.log.log(TAG, "Connection lost")

    def lineReceived(self, line):
        self.handle_request(line)

    def handle_request(self, line):
        l = line[0]
        data = line[1:]

        # Length of the tag is encoded in a single unsigned byte
        (tagLength,) = struct.unpack('B', l)
        self.log.log(TAG, tagLength)

        # Extract the tag and the message
        tag = data [:tagLength]
        message = data[tagLength:]

        # Send it to the log
        self.log.log(tag, message)

class LogServerFactory(Factory):
    """ Listens for clients and creates vision servers for them when they connect """
    def __init__(self, log):
        self.log = log
    def buildProtocol(self, addr):
        return LogServer(self.log)

class LogServerStarter:
    def __init__(self, log):
        self.l = log
        self.lsf = LogServerFactory(log)

    def start(self, port):
        """ Start the subprocess """
        self._subp = Process(target=self._run, args=(port,))
        self._subp.start()

    def _run(self, port):
        """ Run the vision server """
        reactor.listenTCP(port, self.lsf)
        try:
            reactor.run()
        except KeyboardInterrupt:
            print "VISION: User exited"
            self.l.close()
