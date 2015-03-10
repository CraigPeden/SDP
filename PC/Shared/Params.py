import atexit
import os.path
from math import pi
import sys
from inspect import getsourcelines, getfile, getsourcefile
import re
import pyinotify

class ParameterStore:
    def __init__(self, name, autoload=True):

        # Get the path of the current file
        self.path = os.path.abspath(getsourcefile(self.__class__))
        self.filename = os.path.basename(self.path)
        self.n = name

        # Autoreloading code
        if autoload:
            # Get an object to manage this stuff (Bleugh)
            wm = pyinotify.WatchManager()

            # We only care about when the file has been modified
            # Gedit has a stupid way of writing files so we have to listen for writes as well
            mask = pyinotify.IN_MODIFY | pyinotify.IN_CLOSE_WRITE

            # A local class to handle the reloading
            class EventHandler(pyinotify.ProcessEvent):
                def process_IN_MODIFY(s, event):
                    """ This is called when a file is modified """
                    s.doReload(event)
                def process_IN_CLOSE_WRITE(s, event):
                    """ This is called when a file is closed """
                    s.doReload(event)
                def doReload(s, event):
                    if event.name == self.filename:
                        self.reload()
            handler = EventHandler()

            # The notifier itself
            notifier = pyinotify.ThreadedNotifier(wm, handler)
            # Watch the current directory recursively
            wdd = wm.add_watch('.', mask, rec=True)

            # Start watching
            notifier.start()
            self.notifier = notifier

            # Try to close the notifier down if we're exiting
            atexit.register(self.stop)

    def stop(self):
        self.notifier.stop()

    def writeFile(self):
        lines = self.getLines()
        # Parameter definition line regex
        IDENT = "[a-zA-Z_][a-zA-Z0-9_]*"
        pdlr = re.compile("^%s\.(%s) = (.*)$" % (self.n, IDENT))
        str = ""
        for line in lines:
            m = pdlr.match(line)
            if m:
                varName = m.group(1)
                newVal = self.__dict__[varName]
                line = "%s.%s = %s"%(self.n, varName, repr(newVal))
            str += "%s\n" % line
        f = open(self.path, 'w')
        f.write(str)

    def reload(self):
        lines = self.getLines()
        IDENT = "[a-zA-Z_][a-zA-Z0-9_]*"
        pdlr = re.compile("^%s\.(%s) = (.*)$" % (self.n, IDENT))
        for line in lines:
            m = pdlr.match(line)
            if m:
                varName = m.group(1)
                newVal = m.group(2)
                setattr(self, varName, eval(newVal))

    def getLines(self):
        file = open(self.path, 'r')
        lines = file.read().splitlines()
        file.close()
        return lines

    def getThread(self):
        return self.notifier
