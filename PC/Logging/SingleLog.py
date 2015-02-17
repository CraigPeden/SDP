from Log import Log as L
from .Outputs import StdOut, Network, File

class SingleLog:
    def __init__(self):
        # Create an empty log
        self.log = L([])

    def addNetwork(self, host, port):
        self.log.addLog(Network(host, port))

    def addFile(self, filename):
        self.log.addLog(File(filename))

    def addStdOut(self):
        self.log.addLog(StdOut())

    def d(self, tag, message):
        self.log.log(tag, message)

    def start(self):
        self.log.start()

    def getProcess(self):
        return self.log._subp

Log = SingleLog()
