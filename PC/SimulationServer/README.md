# Running
Simply run `./start_simulator` in the main directory.
This adds pymunk and pygame to the PYTHONPATH and adds chipmunk to the LD_LIBRARY_DIR then runs Simulator.py

To run a keyframing vision server, run `. .bashrc && python testVisionServe.py`. You will need to have a vision server of some kind for this to connect to; also it is buggy when running on the real server.

# Using as a library
The simulator can also be run as a library; simply instantiate Simulator.Simulation.Simulation and run its "start" method. This will spawn the simulation as a subprocess.

Alternatively, one may use the `simulation.run_until(timeout, control=False)` method to advance the state of the simulation by `timeout` seconds as quickly as possible.

# Design
## Model
The model deals with the meat of the work in this simulator, running a physics simulation and calling the drawing methods. It makes use of pymunk (a Python wrapper for Chipmunk) for physics simulations (I couldn't be arsed to write collision detection; that stuff is *tricky*) which makes it fairly speedy.

### Ball
The ball is a simple circle mass with high elasticity, low mass, and low friction.

### Robot
A robot is a rectangular body with wheels attached as sub-bodies using PivotJoints. This means that to move the robot you should move its wheels, though for mouse dragging I would move the robot itself (which would bring the wheels along)
The robot's kicker is a small, high-mass, rectangle attached on a very stiff spring with two GrooveJoints to ensure it can only move forwards and to ensure it cannot extend too far.

### Pitch
The pitch is a bounding box for the simulation to occur in. It also provides goal objects to detect collisions.

## Drawing
This simply handles the process of drawing the objects to a pygame surface. This should be obsolete when the simulator has a vision server attached; meaning we can run it headlessly (on the compute server, for instance) and connect one of the drawing systems from strategy to it.

## Servers
The servers deal with sending data out to a strategy and receiving commands back from strategy

# Future
The simulator seems to be roughly feature complete to me now. It could do with fine-tuning of parameters to make it realistic though.

Another possibly useful capability would be updating parameters on the fly. I have some ideas on this that I hope to soon put into action.
