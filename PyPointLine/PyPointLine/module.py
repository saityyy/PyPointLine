from object import object

class ModuleType:
	NONE=0
	MIDPOINT=10


class module(object):
	def __init__(self):
		self.moduletype=ModuleType.NONE
		self.obj1=None
		self.obj2=None
		self.obj3=None
		self.thisis='module'
	def evaluate(self):
		pass

class midpoint(module):
	def __init__(self, point1, point2, point3):
		self.moduletype=ModuleType.MIDPOINT
		self.p1=point1
		self.p2=point2
		self.p3=point3
		self.thisis='module'
	def evaluate(self):
		x1=(-self.p2.x+2*self.p3.x)*0.1+self.p1.x*0.9
		y1=(-self.p2.y+2*self.p3.y)*0.1+self.p1.y*0.9
		x2=(-self.p1.x+2*self.p3.x)*0.1+self.p2.x*0.9
		y2=(-self.p1.y+2*self.p3.y)*0.1+self.p2.y*0.9
		x3=(self.p1.x+self.p2.x)*0.5*0.1+self.p3.x*0.9
		y3=(self.p1.y+self.p2.y)*0.5*0.1+self.p3.y*0.9
		self.p1.x=x1
		self.p1.y=y1
		self.p2.x=x2
		self.p2.y=y2
		self.p3.x=x3
		self.p3.y=y3


