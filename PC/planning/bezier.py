from math import *
from pylab import *

class Point:
	"""
	Simple 2D point class.
	"""

	def __init__(self, x = 0.0, y = 0.0):
		self.x = x
		self.y = y
	
	def distance(self, point):
		return sqrt((point.x - self.x)**2 + (point.y - self.y)**2)

	def length(self):
		return self.distance(Point())

	def __sub__(self, point):
		return Point(self.x - point.x, self.y - point.y)

	def __add__(self, point):
		return Point(self.x + point.x, self.y + point.y)

	def __mul__(self, scalar):
		return Point(scalar * self.x, scalar * self.y)

	def __eq__(self, point):
		return self.x == point.x and self.y == point.y

	def __ne__(self, point):
		return not (self == point)
	
	def towards(self, target, t):
		return self * (1 - t) + target * t
	
	def __repr__(self):
		return "Point(%s, %s)" % (self.x, self.y)  	
	
class Bezier():
	"""
	Creates a bezier curve given a few points.
	"""
	def __init__(self, points):
		self.points = points
	
	def getPoint(self, t):
		bezier = []
		for i in range(len(self.points) - 1):
			bezier.append(self.points[i].towards(self.points[i+1], t))
		for i in range(len(self.points) - 2):
			for j in range(len(self.points) - 2 - i):
				bezier[j] = bezier[j].towards(bezier[j+1], t)
		return bezier[0]

	def getPoints(self, n):
		return [self.getPoint(float(t)/n) for t in range(n+1)]

def plotPoints(points):
    plot([p.x for p in points], [p.y for p in points])

def demo():
	points = [Point(0, 0), Point(0.1, 1), Point(0.9, 0), Point(1, 1)]
        
	bezier = Bezier(points)
	plotPoints(points)
	bezierPoints = bezier.getPoints(100)
	print bezierPoints
	plotPoints(bezierPoints)
	
	show()

if __name__ == "__main__":
	demo()