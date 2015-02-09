""" pygame drawing functions for various objects """
from math import cos, sin, pi

from ..Shared.Funcs import get_robot_vertices, rotateAbout
from ..Params import Params

import pygame
# Some colours
red    = (239,  39,  19)
green  = ( 70, 111,  32)
blue   = ( 12, 170, 205)
yellow = (234, 234,  45)
white  = (255, 255, 255)

def drawPitch(screen, w, h):
    """ Draw the pitch """
    hw = w/2
    hh = h/2
    z = -2
    pygame.draw.polygon(screen, white, ((z,z),(z,h),(w,h),(w,z)), 10)
    pygame.draw.line(screen, white, (hw, 0), (hw, h), 5)
    pygame.draw.circle(screen, white, (hw, hh), 20, 0)
    pygame.draw.line(screen, darken(blue), (0, Params.goalY), (0, Params.goalH+Params.goalY), 20)
    pygame.draw.line(screen, darken(yellow), (w, Params.goalY), (w, Params.goalH+Params.goalY), 20)

def drawRobot(screen, colour, (x, y), (w, b), a, (kx, ky), ka):
    """ Draw a robot and its kicker """
    x2 = x+((b/2)*cos(float(a)))
    y2 = y+((b/2)*sin(float(a)))
    middle = (x, y)

    points = map( lambda point: rotateAbout(point, middle, a)
                , get_robot_vertices((x, y), (w, b))
                )

    kickerPoints = map( lambda point: rotateAbout(point, (kx, ky), ka)
                      , get_robot_vertices((kx, ky), Params.kickerDims)
                      )

    pygame.draw.polygon(screen, darken(colour), kickerPoints)
    pygame.draw.polygon(screen, colour, points)
    pygame.draw.line(screen, white, middle, (x2, y2), 2)
    pygame.draw.circle(screen, darken(colour), middle, 10, 0)

def drawBall(screen, (x, y), radius):
    """ Draw the ball """
    pygame.draw.circle(screen, red, (x, y), radius, 0)

def darken((R, G, B)):
    """ Make a colour a little darker """
    return (R/4, G/4, B/4)
