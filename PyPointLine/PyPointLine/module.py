import tkinter as tk
from object import object, point, line, circle, angle, locus
from utils import *
import math

class module(object):
	def __init__(self, app):
		self.app=app
		self.moduletype="None"
		self.thisis='module'
		self.name=self.youngestName(app)
		self.showName=False
		self.tag="tag_%00d"%(app.nextID)
		app.nextID += 1
	def evaluate(self):
		pass
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="Bisque1",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.name), anchor=tk.NW, font=("",18), width=270 )
		thisLine="-- - --"%()
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass
	def drawPreference(self, app):
		pass
	def youngestName(self, app):
		for name in ["M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12","M13","M14","M15","M16","M17","M18","M18","M19","M20"]:
			for obj in app.lines:
				if obj.name==name:
					break
			else:
				return name
		return "C0"

class midpoint(module):
	def __init__(self, app, point1:point, point2:point, point3:point):
		super().__init__(app)
		self.moduletype="midpoint"
		self.p1=point1
		self.p2=point2
		self.p3=point3
		self.ratio1=1
		self.ratio2=1
		pass
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
	def drawPreference(self, app):
		pass
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s (%d) - %s - (%d) %s"%(self.p1.name, self.ratio1, self.p3.name, self.ratio2, self.p2.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass


class point2point(module):
	def __init__(self, app, point1:point, point2:point):
		super().__init__(app)
		self.moduletype="point2point"
		self.p1=point1
		self.p2=point2
	def evaluate(self):
		x1=self.p2.x*0.1+self.p1.x*0.9
		y1=self.p2.y*0.1+self.p1.y*0.9
		x2=self.p1.x*0.1+self.p2.x*0.9
		y2=self.p1.y*0.1+self.p2.y*0.9
		self.p1.x=x1
		self.p1.y=y1
		self.p2.x=x2
		self.p2.y=y2
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s - %s"%(self.p1.name, self.p2.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass


class point2line(module):
	def __init__(self, app, point:point, line:line):
		super().__init__(app)
		self.moduletype="point2line"
		self.p1=point
		self.l1=line
		self.thisis='module'
		self.onlyOnSegment=True
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
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s - %s"%(self.p1.name, self.l1.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass

class point2circle(module):
	def __init__(self, app, point:point, circle:circle):
		super().__init__(app)
		self.moduletype="point2circle"
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
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s - %s"%(self.p1.name, self.c1.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass


class line2circle(module):
	def __init__(self, app, line:line, circle:circle):
		super().__init__(app)
		self.moduletype="line2circle"
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
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s - %s"%(self.ln.name, self.cc.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass

class circle2circle(module):
	def __init__(self, app, circle1:circle, circle2:circle):
		super().__init__(app)
		self.moduletype="circle2circle"
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
		if mag==0.0:
			return
		deltaIn = mag - abs(radius1 - radius2)
		deltaOut = mag-(radius1 + radius2)
		if abs(deltaIn) > abs(deltaOut):## outer tangent
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
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s - %s"%(self.cc1.name, self.cc2.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass

class isometry(module):
	def __init__(self, app, line1:line, line2:line):
		super().__init__(app)
		self.moduletype="isometry"
		self.ln1=line1
		self.ln2=line2
		self.thisis='module'
		self.ratio1=1
		self.ratio2=1
	def evaluate(self):
		p1=self.ln1.point1
		p2=self.ln1.point2
		p3=self.ln2.point1
		p4=self.ln2.point2
		ax=p2.x-p1.x
		ay=p2.y-p1.y
		magA=magnitude(ax, ay)
		bx=p4.x-p3.x
		by=p4.y-p3.y
		magB=magnitude(bx, by)
		if magA==0.0 or magB==0.0:
			return
		difference=min((magB-magA)*0.1,0.01)
		cx, cy=ax/magA*difference, ay/magA*difference
		self.ln1.point1.x -= cx
		self.ln1.point1.y -= cy
		self.ln1.point2.x += cx
		self.ln1.point2.y += cy
		dx, dy=bx/magB*difference, by/magB*difference
		self.ln2.point1.x += dx
		self.ln2.point1.y += dy
		self.ln2.point2.x -= dx
		self.ln2.point2.y -= dy
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s - %s (%d : %d)"%(self.ln1.name, self.ln2.name, self.ratio1, self.ratio2)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass



class parallel(module):
	def __init__(self, app, line1:line, line2:line):
		pass
	def evaluate(self):
		pass
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s || %s "%(self.ln1.name, self.ln2.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass


class perpendicular(module):
	def __init__(self, app, line1:line, line2:line):
		pass
	def evaluate(self):
		pass
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s ⟂ %s "%(self.ln1.name, self.ln2.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass

class horizontal(module):
	def __init__(self, app, line1:line):
		super().__init__(app)
		self.thisis='module'
		self.line=line1
		pass
	def evaluate(self):
		p1:point=self.line.point1
		p2:point=self.line.point2
		theta=math.atan2(p2.y-p1.y, p2.x-p1.x)
		if -math.pi/2<=theta and theta<=math.pi/2:
			difference=-theta*0.1
		elif -math.pi/2>theta:
			difference=(-math.pi-theta)*0.1
		else:
			difference=(math.pi-theta)*0.1
		self.line.point1.x, self.line.point1.y, self.line.point2.x, self.line.point2.y = rotation(p1.x, p1.y, p2.x, p2.y, difference)

		pass
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s = "%(self.line.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass


