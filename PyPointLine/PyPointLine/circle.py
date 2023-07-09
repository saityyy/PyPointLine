from object import object
from point import point

class circle(object):
	def __init__(self, point:point, radius):
		self.point=point
		self.radius=radius
		self.thisis='circle'


