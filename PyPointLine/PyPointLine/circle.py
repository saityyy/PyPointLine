from object import object
from point import point

from utils import *

class circle(object):
	def __init__(self, point:point, radius):
		self.point=point
		self.radius=radius
		self.thisis='circle'

	def __init__(self, point1:point, point2:point):
		self.point=point1
		self.radius=dist(point1.x,point1.y,point2.x,point2.y)
		self.thisis='circle'

