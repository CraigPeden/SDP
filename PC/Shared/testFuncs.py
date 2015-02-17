'''
Created on Feb 26, 2012

@author: Keith_Mac
'''
import unittest
from Funcs import *
from math import pi


class testFuncs(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testVecPlus(self):
        self.assertEquals([2, 3], vecPlus((1, 2), (1, 1)), 
                          "vecPlus() failed")
        self.assertEquals([600, 300], vecPlus((600, 300), (0, 0)), 
                          "vecPlus() failed")
        self.assertEquals([599, 499], vecPlus((100, 200), (499, 299)), 
                          "vecPlus() failed")

    def testVecSub(self):
        self.assertEquals([0, 1], vecSub((1, 2), (1, 1)), 
                          "vecSub() failed")
        self.assertEquals([600, 300], vecSub((600, 300), (0, 0)), 
                          "vecSub() failed")
        self.assertEquals([-399, -99], vecSub((100, 200), (499, 299)), 
                          "vecSub() failed")

    def testVecMult(self):
        self.assertEquals((1, 2), vecMult((1, 2), (1, 1)), 
                          "vecMult() failed")
        self.assertEquals((0, 0), vecMult((600, 300), (0, 0)), 
                          "vecMult() failed")
        self.assertEquals((49900, 59800), vecMult((100, 200), (499, 299)), 
                          "vecMult() failed")

    def testVecNorm(self):
        self.assertEquals(57.2713, round(vecNorm((12, 56)), 4), 
                          "vecNorm() failed")
        self.assertEquals(515.2058, round(vecNorm((459, 234)), 4), 
                          "vecNorm() failed")
        self.assertEquals(0.0, vecNorm((0, 0)), 
                          "vecNorm() failed")
        self.assertEquals(599.0008, round(vecNorm((599, 1)), 4), 
                          "vecNorm() failed")

    def testWeightNorm(self):
        self.assertEquals([0.14468085106382977, 0.8553191489361702], 
                          weightNorm((34, 201)), "weightNorm() failed")
        self.assertEquals([0.7485380116959064, 0.25146198830409355], 
                          weightNorm((512, 172)), "weightNorm() failed")
        self.assertEquals([0.6666666666666666, 0.3333333333333333], 
                          weightNorm((600, 300)), "weightNorm() failed")
        self.assertEquals([0.6554621848739496, 0.3445378151260504], 
                          weightNorm((234, 123)), "weightNorm() failed")
        self.assertRaises(ZeroDivisionError, weightNorm, (0,0))

    def testVecDist(self):
        self.assertEquals(222.2656, round(vecDist((1, 1), (100, 200)), 4), 
                          "vecDist() failed")
        self.assertEquals(0, vecDist((222, 111), (222, 111)), 
                          "vecDist() failed")
        self.assertEquals(520.5536, round(vecDist((543, 111), (23, 87)), 4), 
                          "vecDist() failed")
        self.assertEquals(1.4142, round(vecDist((23, 34), (24, 35)), 4), 
                          "vecDist() failed")

    def testVecAngle(self):
        self.assertEquals(2.7707, round(vecAngle((12, 200), (300, 88)), 4), 
                          "vecAngle() failed")
        self.assertEquals(-2.3562, round(vecAngle((1, 1), (3, 3)), 4), 
                          "vecAngle() failed")
        self.assertEquals(-2.6779, round(vecAngle((0, 0), (600, 300)), 4), 
                          "vecAngle() failed")
        self.assertEquals(3.1416, round(vecAngle((191, 200), (549, 200)), 4), 
                          "vecAngle() failed")
        self.assertEquals(0, vecAngle((22, 22), (321)), 
                          "vecAngle() failed")

    def testDotProduct(self):
        self.assertEquals(33038, dotProduct((34, 198), (401, 98)), 
                          "dotProduct() failed")
        self.assertEquals(60516, dotProduct((100, 34), (512, 274)), 
                          "dotProduct() failed")
        self.assertEquals(598, dotProduct((0, 299), (599, 2)), 
                          "dotProduct() failed")
        self.assertEquals(0, dotProduct((0, 0), (156, 178)), 
                          "dotProduct() failed")

    def testGet_Robot_Vertices(self):
        self.assertEquals([(2, -65), (2, 175), (22, 175), (22, -65)], 
                          get_robot_vertices((12, 55), (241, 21)), 
                          "get_robot_vertices() failed")
        self.assertEquals([(514, 31), (514, 371), (686, 371), (686, 31)], 
                          get_robot_vertices((600, 201), (340, 173)), 
                          "get_robot_vertices() failed")
        self.assertEquals([(-145, -173), (-145, 173), (145, 173), (145, -173)], 
                          get_robot_vertices((0, 0), (346, 291)), 
                          "get_robot_vertices() failed")
        self.assertEquals([(101, 240), (101, 312), (157, 312), (157, 240)], 
                          get_robot_vertices((129, 276), (72, 56)), 
                          "get_robot_vertices() failed")

    def testRotate(self):
        self.assertEquals((-34, -88), rotate((34, 88), pi), 
                          "rotate() failed")
        self.assertEquals((295, 123), rotate((123, 295), (3*pi/2)), 
                          "rotate() failed")
        self.assertEquals((212.1320343559643, 636.3961030678927), rotate((600, 300), pi/4), 
                          "rotate() failed")
        self.assertEquals((73, 19), rotate((73, 19), 2*pi), 
                          "rotate() failed")

    def testRotateAbout(self):
        self.assertEquals((195.0, 355.0), rotateAbout((3, 45), (99, 200), pi), 
                          "rotateAbout() failed")
        self.assertEquals((277.79096063693623, 364.7942286340599), 
                          rotateAbout((319, 229), (45, 220), pi/6), 
                          "rotateAbout() failed")
        self.assertEquals((257.99999999999994, -194.0), 
                          rotateAbout((449, 87), (213, 42), (3*pi/2)), 
                          "rotateAbout() failed")
        self.assertEquals((9.668434813674253, 50.71930009000633), 
                          rotateAbout((145, 294), (371, 9), pi/4), 
                          "rotateAbout() failed")

    def testSimpleAngle(self):
        self.assertEquals(-pi/2, simpleAngle((3*pi/2)), "simpleAngle() failed")
        self.assertEquals(pi, simpleAngle(pi), "simpleAngle() failed")
        self.assertEquals(pi, simpleAngle(-pi), "simpleAngle() failed")
        self.assertEquals(pi/2, simpleAngle(-3*pi/2), "simpleAngle() failed")
        self.assertEquals(pi/2, simpleAngle(pi/2), "simpleAngle() failed")
        self.assertEquals(pi/4, simpleAngle(pi/4), "simpleAngle() failed")


    def testConvert(self):
        self.assertEquals([51.0, 300.0], convert((34, 200), 2, 3), 
                          "convert() failed")
        self.assertEquals([4066.7747163695303, 2033.3873581847652], 
                          convert((600, 300), 1.234, 8.364), 
                          "convert() failed")
        self.assertEquals([20.16, 5.04], convert((8, 2), 1, 2.52), 
                          "convert() failed")
        self.assertEquals([153.21428571428572, 53.57142857142857], convert((429, 150), 56, 20), 
                          "convert() failed")
        self.assertEquals([15.0, 27.333333333333332], convert((45, 82), 9, 3), 
                          "convert() failed")
        self.assertEquals([333.0, 111.0], convert((333, 111), 1, 1), 
                          "convert() failed")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
