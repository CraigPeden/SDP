#!/usr/bin/env python
from Simulator.VisionWrapper import VisionWrapper
from Simulator.CommsWrapper import CommsWrapper
from Simulator.StrategyWrapper import StrategyWrapper
from Simulator.Servers.VisionServer import VisionServerStarter
from Simulator.Servers.CommsServer import CommsServerFactory
from Simulator.Simulation import Simulation
from Simulator.Model.WorldObjects import Robot, Ball

objects = { 'blue' : Robot((0,0), (0,0), 0, "blue")
          , 'yellow' : Robot((0,0), (0,0), 0, "yellow")
          , 'ball' : Ball((0,0), (0,0))
          }
sim = Simulation(objects, draw=True)
sim.start()

try:
    vw = VisionWrapper(sim)
except Exception, e:
    print "VisionWrapper Error: %s" % e

try:
    cw = CommsWrapper(sim)
except Exception, e:
    print "CommsWrapper Error: %s" % e
    
try:
    sw = StrategyWrapper(sim)
except Exception, e:
    print "StrategyWrapper Error: %s" % e

try:
    vss = VisionServerStarter(vw, 400)
    vss.start(31430)
except Exception, e:
    print "VSS Error: %s" % e

try:
    csf = CommsServerFactory(cw)
    csf.start(31420)
except Exception, e:
    print "CSF Error: %s" % e


done = False
while not done:
    try:
        pass
    except KeyboardInterrupt:
        done = True
        sim.finish()
