from object import object
from point import point
from line import line
from circle import circle
from utils import *

class ModuleType:
	NONE=0
	MIDPOINT=10
	P2P=20
	P2L=21

class module(object):
	def __init__(self):
		self.moduletype=ModuleType.NONE
		self.thisis='module'
	def evaluate(self):
		pass

class midpoint(module):
	def __init__(self, point1:point, point2:point, point3:point):
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


class point2point(module):
	def __init__(self, point1:point, point2:point):
		self.moduletype=ModuleType.P2P
		self.p1=point1
		self.p2=point2
		self.thisis='module'
	def evaluate(self):
		x1=self.p2.x*0.1+self.p1.x*0.9
		y1=self.p2.y*0.1+self.p1.y*0.9
		x2=self.p1.x*0.1+self.p2.x*0.9
		y2=self.p1.y*0.1+self.p2.y*0.9
		self.p1.x=x1
		self.p1.y=y1
		self.p2.x=x2
		self.p2.y=y2


class point2line(module):
	def __init__(self, point:point, line:line):
		self.moduletype=ModuleType.P2L
		self.p1=point
		self.l1=line
		self.thisis='module'
	def evaluate(self):
		p2=self.l1.point1
		p3=self.l1.point2
		ax,ay=self.p1.x, self.p1.y
		bx,by=p2.x,p2.y
		cx,cy=p3.x,p3.y
		tn=(ax-bx)*(cx-bx)+(ay-by)*(cy-by)
		td=(cx-bx)*(cx-bx)+(cy-by)*(cy-by)
		if td==0:
			return
		tt=tn/td
		dx, dy=tt*(cx-bx)+(bx-ax), tt*(cy-by)+(by-ay)
		self.p1.x += dx*0.1
		self.p1.y += dy*0.1
		self.l1.point1.x -= dx*0.1
		self.l1.point1.y -= dy*0.1
		self.l1.point2.x -= dx*0.1
		self.l1.point2.y -= dy*0.1
		##unfinished

class point2circle(module):
	def __init__(self, point:point, circle:circle):
		self.moduletype=ModuleType.P2C
		self.p1=point
		self.c1=circle
		self.thisis='module'
	def evaluate(self):
		c1=self.c1
		p2=c1.point
		radius=c1.radius
		ax,ay=p2.x-self.p1.x, p2.y-self.p1.y
		mag=magnitude(ax,ay)
		if mag==0:
			return
		difference=(mag-radius)*0.1
		dx, dy=ax/mag*difference, ay/mag*difference
		