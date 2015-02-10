from Outputs import StdOut
from Server import LogServerStarter

from multiprocessing import Process, Queue, Value
from Queue import Empty

class Log(object):
    _subp = None
    def __init__(self, outputs=None):
        if outputs != None:
            self.outputs = outputs
        else:
            self.outputs = [StdOut()]
        self.logQueue = Queue()
        self.done = Value('B', False)

    def start(self):
        self._subp = Process(target=self.runLogQueue)
        self._subp.start()

    def serve(self, port=16180):
        self.lsf = LogServerStarter(self)
        self.lsf.start(port)

    def writeLog(self, tag, message):
        """ Performs the IO operation of logging """
        map(lambda o: o.write(tag, message), self.outputs)

    def log(self, tag, message):
        """ Adds a log item to the log """
        self.logQueue.put((tag, message))

    def runLogQueue(self):
        while not self.done.value:
            try:
                content = self.logQueue.get_nowait()
                (tag, message) = content
                self.writeLog(tag, message)
            except Empty:
                pass

    def close(self):
        self.done.value = True
        map(lambda o: o.close(), self.outputs)

    def addLog(self, log):
        self.outputs.append(log)
