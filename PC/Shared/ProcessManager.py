from multiprocessing import Process, Queue
from Queue import Empty

class ProcessManager(object):
    processes = None
    def __init__(self):
        self.processes = dict()

    def add(self, processName, process):
        self.processes[processName] = process

    def poll(self, processName):
        return self.processes[processName].is_alive()

    def kill(self, processName):
        try:
            self.processes[processName].terminate()
            return
        except AttributeError:
            pass

        try:
            self.processes[processName].stop()
            return
        except AttributeError:
            pass

    def killall(self):
        for processName in self.processes:
            self.kill(processName)

processes = ProcessManager()
