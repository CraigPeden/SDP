from ..Simulation import Simulation
from Defaults import objects
import numpy
import math
from ..Params import Params

class IntersectionNotFound(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def find_if_collision(sim, motion, timeout, obj):
    obj.collided = False

    def collide(space, arbiter):
        sim.done.value = True
        obj.collided = True
        return True

    obj.add_collision_handler(sim.space, collide)
    obj.move(*motion)
    sim.run_until(timeout)
    return obj.collided


def get_ball_pos_after(sim, timeout):
    sim.run_until(timeout)
    return sim.objects["ball"].body.position


def get_intersection_ball_us(sim, timeout):
    # speed in pixel/sec
    speed = Params.robotRealSpeed

    ball = sim.objects["ball"]
    us = sim.get_us_robot()

    coeff = Params.predictionCircleCenter
    reach_area_center = us.getPosition() + \
      numpy.array([math.cos(us.getOrientation()), math.sin(us.getOrientation())]) * coeff

    for t in range(1, timeout + 1):
        ball_pos = get_ball_pos_after(sim, t)
        if numpy.linalg.norm(reach_area_center - ball_pos) < speed * t:
            return ball_pos

    raise IntersectionNotFound("Intersection with ball and robot is not found")
