from preference import preference
from utils import *

class object:
	""" """
	def __init__(self,app):
		""" """
		self.app=app
		self.id=-1
		self.preference=None
		self.name='X'
		self.thisis=None
		pass
	pass



class point(object):
	def __init__(self, x, y):
		self.x=x
		self.y=y
		self.thisis='point'


class line(object):
	def __init__(self, point1:point, point2:point):
		self.point1=point1
		self.point2=point2
		self.thisis='line'


class circle(object):
	def __init__(self, point:point, radius):
		self.point=point
		self.radius=radius
		self.thisis='circle'

	def __init__(self, point1:point, point2:point):
		self.point=point1
		self.radius=dist(point1.x,point1.y,point2.x,point2.y)
		self.thisis='circle'
	pass

class angle(object):
	def __init__(self, point1:point, point2:point, point3:point):
		self.point1=point1
		self.point2=point2
		self.point3=point3
		self.thisis='angle'
	pass

class locus(object):
	def __init__(self, point1:point):
		self.point1=point1
		self.thisis='locus'
	pass

