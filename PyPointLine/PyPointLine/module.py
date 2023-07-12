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
	P2C=22
	TangentL2C=23
	TangentC2C=24

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
		dx *= 0.1
		dy *= 0.1
		self.p1.x += dx
		self.p1.y += dy
		self.l1.point1.x -= dx
		self.l1.point1.y -= dy
		self.l1.point2.x -= dx
		self.l1.point2.y -= dy
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
		self.p1.x += dx
		self.p1.y += dy
		self.c1.point.x -= dx
		self.c1.point.y -= dy
		self.c1.radius += difference

class line2circle(module):
	def __init__(self, line:line, circle:circle):
		self.moduletype=ModuleType.TangentL2C
		self.cc=circle
		self.ln=line
		self.thisis='module'
	def evaluate(self):
		p1=self.cc.point
		radius=self.cc.radius
		p2=self.ln.point1
		p3=self.ln.point2
		ax,ay=p1.x,p1.y
		bx,by=p2.x,p2.y
		cx,cy=p3.x,p3.y
		tn=(ax-bx)*(cx-bx)+(ay-by)*(cy-by)
		td=(cx-bx)*(cx-bx)+(cy-by)*(cy-by)
		if td==0:
			return
		tt=tn/td
		dx, dy=tt*(cx-bx)+(bx-ax), tt*(cy-by)+(by-ay)
		mag=magnitude(dx,dy)
		if mag==0:
			return
		difference=(mag-radius)*0.1
		ex,ey = dx/mag*difference, dy/mag*difference
		self.cc.point.x += ex
		self.cc.point.y += ey
		self.cc.radius += difference
		self.ln.point1.x -= ex
		self.ln.point1.y -= ey
		self.ln.point2.x -= ex
		self.ln.point2.y -= ey

class circle2circle(module):
	def __init__(self, circle1:circle, circle2:circle):
		self.moduletype=ModuleType.TangentC2C
		self.cc1=circle1
		self.cc2=circle2
		self.thisis='module'
	def evaluate(self):
		p1=self.cc1.point
		radius1=self.cc1.radius
		p2=self.cc2.point
		radius2=self.cc2.radius
		cx, cy = p2.x - p1.x, p2.y - p1.y
		mag = magnitude(cx,cy)
		deltaIn = mag - math.abs(radius1 - radius2)
		deltaOut = mag-(radius1 + radius2)
		if math.abs(deltaIn) > math.abs(deltaOut):## outer tangent
			difference = deltaOut * 0.025
			dx, dy = cx/mag*difference, cy/mag*difference
			self.cc1.point.x += dx
			self.cc1.point.y += dy
			self.cc1.radius += difference
			self.cc2.point.x -= dx
			self.cc2.point.y -= dy
			self.cc2.radius += difference
		else:## inner tangent
			difference=deltaIn*0.025
			dx, dy = cx/mag*difference, cy/mag*difference
			self.cc1.point.x += dx
			self.cc1.point.y += dy
			self.cc2.point.x -= dx
			self.cc2.point.y -= dy
			if radius1>radius2:
				self.cc1.radius += difference
				self.cc2.radius -= difference
			else:
				self.cc1.radius -= difference
				self.cc2.radius += difference


