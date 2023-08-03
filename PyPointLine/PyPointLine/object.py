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
		self.name=self.youngestName(app)
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
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="SeaGreen1",width=3)
		canvas.create_text(x+5,y+5,text="Point : %s"%(self.name), anchor=tk.NW, font=("",18), width=270 )
		thisLine="(%f,%f)"%(self.x, self.y)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Non Fixed, Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass
	def drawPreference(self, app):
		pass
	def youngestName(self, app):
		for name in ["A","B","C","D","E","F","G","H","J","K","L","M","N","P","Q","R","S","T","U","V","W","X","Y","Z",
			   "AA","AB","AC","AD","AE","AF","AG","AH","AJ","AK","AL","AM","AN","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ",]:
			for obj in app.points:
				if obj.name==name:
					break
			else:
				return name
		return "XX"



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
		self.name=self.youngestName(app)
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
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="Orchid1",width=3)
		canvas.create_text(x+5,y+5,text="Line : %s"%(self.name), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s - %s"%(self.point1.name, self.point2.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Not Isomed, Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass
	def drawPreference(self, app):
		pass
	def youngestName(self, app):
		for name in ["a","b","c","d","e","f","g","h","j","k","m","n","p","q","r","s","t","u","v","w","x","y","z","aa"]:
			for obj in app.lines:
				if obj.name==name:
					break
			else:
				return name
		return "xx"

class circle(object):
	def __init__(self, app, point:point, radius:float):
		self.point=point
		self.radius=radius
		self.thisis='circle'
		self.name=self.youngestName(app)
		self.showName=False
		self.tag="tag_%00d"%(app.nextID)
		app.nextID += 1
	
	def drawObject(self, app):
		x1,y1=app.world2Canvas(self.point.x, self.point.y)
		r=self.radius * app.zoom
		app.mainCanvas.create_oval(x1-r,y1-r,x1+r,y1+r, outline='grey', width=4)
		pass

	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="Bisque1",width=3)
		canvas.create_text(x+5,y+5,text="Circle : %s"%(self.name), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s - %f"%(self.point.name, self.radius)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass
	def drawPreference(self, app):
		pass

	def youngestName(self, app):
		for name in ["C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","C11","C12","C13","C14","C15","C16","C17","C18","C18","C19","C20"]:
			for obj in app.lines:
				if obj.name==name:
					break
			else:
				return name
		return "C0"

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

