import tkinter as tk
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
	def drawObject(self, app):
		pass
	def drawLog(self, app):
		pass
	def drawPreference(self, app):
		pass



class point(object):
	def __init__(self, app, x, y):

		self.x=x
		self.y=y
		self.thisis='point'
		self.color='blue'
		self.fixed=False
		self.fixedColor='red'
		self.showName=True
		self.tag="tag_%00d"%(app.nextID)
		app.nextID += 1
		pass
	def drawObject(self, app):
		xx0,yy0=app.world2Canvas(self.x,self.y)
		app.mainCanvas.create_oval(xx0-5,yy0-5,xx0+5,yy0+5, fill='blue', tag=self.tag)
		pass
	def drawLog(self, app):
		canvas=app.prefCanvas
		x=5
		y=app.LoglineFeed+5
		app.LoglineFeed=100
		w=290
		h=90
		canvas.create_rectangle(x,y,x+w,y+h,fill="green",width=3)
		canvas.create_text(x+5,y+5,text="Point : A", anchor=tk.NW, font=("",18), width=290 )
		thisLine="(%f,%f)"%(self.x, self.y)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=290 )
		canvas.create_text(x+5,y+57,text="Non Fixed, Hide Name",  anchor=tk.NW, font=("",18), width=290 )
		pass
	def drawPreference(self, app):
		pass

class line(object):
	def __init__(self, app, point1:point, point2:point):
		self.point1=point1
		self.point2=point2
		self.thisis='line'
		self.length=1.0
		self.showLength=False
		self.isomID=-1
		self.showIsom=False
		self.showIsomFlag=0
		self.showName=False
		self.tag="tag_%00d"%(app.nextID)
		app.nextID += 1
	def drawObject(self, app):
		pt1=self.point1
		pt2=self.point2
		x1,y1=app.world2Canvas(pt1.x, pt1.y)
		x2,y2=app.world2Canvas(pt2.x, pt2.y)
		app.mainCanvas.create_line(x1,y1,x2,y2, fill='grey', width=4)
	def drawLog(self, app):
		pass
	def drawPreference(self, app):
		pass

class circle(object):
	def __init__(self, app, point:point, radius:float):
		self.point=point
		self.radius=radius
		self.thisis='circle'
		self.showName=False
		self.tag="tag_%00d"%(app.nextID)
		app.nextID += 1
		
	def drawObject(self, app):
		x1,y1=app.world2Canvas(self.point.x, self.point.y)
		r=self.radius * app.zoom
		app.mainCanvas.create_oval(x1-r,y1-r,x1+r,y1+r, outline='grey', width=4)

	pass
	def drawLog(self, app):
		pass
	def drawPreference(self, app):
		pass

class angle(object):
	def __init__(self, point1:point, point2:point, point3:point):
		self.point1=point1
		self.point2=point2
		self.point3=point3
		self.thisis='angle'
		self.showArc=True
		self.showIsom=False
		self.showIsomFrag=0
		self.showValue=False

	def drawObject(self, app):
		xx1,yy1=app.world2Canvas(self.point1.x,self.point1.y)
		xx2,yy2=app.world2Canvas(self.point2.x,self.point2.y)
		xx3,yy3=app.world2Canvas(self.point3.x,self.point3.y)
		theta1=math.atan2(-yy1+yy2, xx1-xx2)
		theta3=math.atan2(-yy3+yy2, xx3-xx2)
		rad2ang=180/math.pi
		if theta1+math.pi<theta3:
			start, extent = theta3*rad2ang, (theta1 - theta3 + 2*math.pi)*rad2ang
		elif theta1<theta3:
			start, extent = theta1*rad2ang, (theta3 - theta1)*rad2ang
		elif theta1-math.pi<theta3:
			start, extent = theta3*rad2ang, (theta1 - theta3)*rad2ang
		else:
			start, extent = theta1*rad2ang, (theta3 - theta1 + 2*math.pi)*rad2ang
		app.mainCanvas.create_arc(xx2-20, yy2-20, xx2+20, yy2+20, start=start, extent=extent, style=tk.ARC, width=4, outline='red')

	pass
	def drawLog(self, app):

		pass
	def drawPreference(self, app):
		pass

class locus(object):
	def __init__(self, point1:point):
		self.point1=point1
		self.thisis='locus'
	pass
	def drawLog(self, app):
		pass
	def drawPreference(self, app):
		pass

