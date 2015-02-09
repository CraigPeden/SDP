from Clients import CommsClient

class CommsWrapper:
    def __init__(self, sim):
        self.sim = sim
        self.done = sim.done
        self.r = CommsClient()

    def move(self, lwheel, rwheel):
        self.r.move(lwheel, rwheel)
        self.sim.move(lwheel, rwheel)

    def kick(self):
        self.r.kick()
        self.sim.kick()

    def stop(self):
        self.r.stop()
        self.sim.stop()

    def turn(self, angle):
        self.r.turn(angle)
        self.sim.turn(angle)

    def forwards(self, motor_speed=40):
        self.r.forwards(motor_speed)
        self.sim.forwards(motor_speed)

    def backwards(self, motor_speed=20):
        self.r.backwards(motor_speed)
        self.sim.backwards(motor_speed)
