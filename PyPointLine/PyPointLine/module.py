import tkinter as tk
from object import object, point, line, circle, angle, locus
from utils import *
import math
from preference import preference

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
		return 0
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
		for name in ["M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12","M13","M14","M15","M16","M17","M18","M19","M20",
				"M21","M22","M23","M24","M25","M26","M27","M28","M29","M30","M31","M32","M33","M34","M35","M36","M37","M38","M39","M40"]:
			for obj in app.lines:
				if obj.name==name:
					break
			else:
				return name
		return "M0"
	def toString(self)-> str:
		return ""
	def toTeXString(self)-> str:
		return ""



class midpoint(module):
	def __init__(self, app, point1:point, point2:point, point3:point):
		super().__init__(app)
		self.moduletype="midpoint"
		self.p1=point1
		self.p2=point2
		self.p3=point3
		self.ratio1=1
		self.ratio2=1
		self.para1=0.1
		self.para2=0.1
		self.para3=0.1
		self.pref=preference(self.app, self)
		pass
	def evaluate(self):
		r1=self.ratio1
		r2=self.ratio2
		x1=((-self.p2.x*r1+(r1+r2)*self.p3.x)/r2-self.p1.x)*self.para1
		y1=((-self.p2.y*r1+(r1+r2)*self.p3.y)/r2-self.p1.y)*self.para1
		x2=((-self.p1.x*r2+(r1+r2)*self.p3.x)/r1-self.p2.x)*self.para2
		y2=((-self.p1.y*r2+(r1+r2)*self.p3.y)/r1-self.p2.y)*self.para2
		x3=((self.p1.x*r2+self.p2.x*r1)/(r1+r2)-self.p3.x)*self.para3
		y3=((self.p1.y*r2+self.p2.y*r1)/(r1+r2)-self.p3.y)*self.para3
		if self.p1.fixed==False:
			self.p1.x+=x1
			self.p1.y+=y1
		if self.p2.fixed==False:
			self.p2.x+=x2
			self.p2.y+=y2
		if self.p3.fixed==False:
			self.p3.x+=x3
			self.p3.y+=y3
		return magnitude(x1,y1)+magnitude(x2,y2)+magnitude(x3,y3)
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
	def toString(self)-> str:
		return "type=module,moduletype=midpoint,tag=%s,p1=%s,p2=%s,p3=%s,ratio1=%d,ratio2=%d,para1=%f,para2=%f,para3=%f"%(self.tag, self.p1.tag, self.p2.tag, self.p3.tag, self.ratio1, self.ratio2, self.para1, self.para2, self.para3)
	def toTeXString(self)-> str:
		return ""


class point2point(module):
	def __init__(self, app, point1:point, point2:point):
		super().__init__(app)
		self.moduletype="point2point"
		self.p1=point1
		self.p2=point2
		self.para1=0.1
		self.para2=0.1
		self.pref=preference(self.app, self)
	def evaluate(self):
		x1=(self.p2.x-self.p1.x)*self.para1
		y1=(self.p2.y-self.p1.y)*self.para1
		x2=(self.p1.x-self.p2.x)*self.para2
		y2=(self.p1.y-self.p2.y)*self.para2
		if self.p1.fixed==False:
			self.p1.x += x1
			self.p1.y += y1
		if self.p2.fixed==False:
			self.p2.x += x2
			self.p2.y += y2
		return magnitude(x1,y1)+magnitude(x2,y2)
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
	def toString(self)-> str:
		return "type=module,moduletype=point2point,tag=%s,p1=%s,p2=%s,para1=%f,para2=%f"%(self.tag,self.tag, self.p1.tag, self.p2.tag, self.para1, self.para2)


class point2line(module):
	def __init__(self, app, point1:point, line1:line):
		super().__init__(app)
		self.moduletype="point2line"
		self.p1=point1
		self.l1=line1
		self.thisis='module'
		self.onlyOnSegment=True
		self.para1=0.1
		self.pref=preference(self.app, self)
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
		if self.p1.fixed==False:
			self.p1.x += dx*self.para1
			self.p1.y += dy*self.para1
		if self.l1.point1.fixed==False:
			self.l1.point1.x -= dx*self.para1
			self.l1.point1.y -= dy*self.para1
		if self.l1.point2.fixed==False:
			self.l1.point2.x -= dx*self.para1
			self.l1.point2.y -= dy*self.para1
		return magnitude(dx,dy)*self.para1*3
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
	def toString(self)-> str:
		return "type=module,moduletype=point2line,tag=%s,p1=%s,l1=%s,onlyOnSegment=%d,para1=%f"%(self.tag,self.p1.tag, self.l1.tag, int(self.onlyOnSegment), self.para1)

class point2circle(module):
	def __init__(self, app, point:point, circle:circle):
		super().__init__(app)
		self.moduletype="point2circle"
		self.p1=point
		self.c1=circle
		self.thisis='module'
		self.para1=0.1
		self.pref=preference(self.app, self)
	def evaluate(self):
		c1=self.c1
		p2=c1.point1
		radius=c1.radius
		ax,ay=p2.x-self.p1.x, p2.y-self.p1.y
		mag=magnitude(ax,ay)
		if mag==0:
			return
		difference=(mag-radius)*self.para1
		dx, dy=ax/mag*difference, ay/mag*difference
		if self.p1.fixed==False:
			self.p1.x += dx
			self.p1.y += dy
		if self.c1.point1.fixed==False:
			self.c1.point1.x -= dx
			self.c1.point1.y -= dy
		if self.c1.fixedRadius==False:
			self.c1.radius += difference
		return abs(difference)*3
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
	def toString(self)-> str:
		return "type=module,moduletype=point2circle,tag=%s,p1=%s,c1=%s,para1=%f"%(self.tag,self.p1.tag, self.c1.tag, self.para1)


class line2circle(module):
	def __init__(self, app, line1:line, circle1:circle):
		super().__init__(app)
		self.moduletype="line2circle"
		self.cc=circle1
		self.ln=line1
		self.thisis='module'
		self.para1=0.1
		self.pref=preference(self.app, self)
	def evaluate(self):
		p1=self.cc.point1
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
		difference=(mag-radius)*self.para1
		ex,ey = dx/mag*difference, dy/mag*difference
		self.cc.point1.x += ex
		self.cc.point1.y += ey
		if self.cc.fixedRadius==False:
			self.cc.radius += difference
		self.ln.point1.x -= ex
		self.ln.point1.y -= ey
		self.ln.point2.x -= ex
		self.ln.point2.y -= ey
		return abs(difference)*3
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
	def toString(self)-> str:
		return "type=module,moduletype=line2circle,tag=%s,ln=%s,cc=%s,para1=%f"%(self.tag,self.ln.tag, self.cc.tag, self.para1)

class circle2circle(module):
	def __init__(self, app, circle1:circle, circle2:circle):
		super().__init__(app)
		self.moduletype="circle2circle"
		self.cc1=circle1
		self.cc2=circle2
		self.thisis='module'
		self.para1=0.025
		self.pref=preference(self.app, self)
	def evaluate(self):
		p1=self.cc1.point1
		radius1=self.cc1.radius
		p2=self.cc2.point1
		radius2=self.cc2.radius
		cx, cy = p2.x - p1.x, p2.y - p1.y
		mag = magnitude(cx,cy)
		if mag==0.0:
			return
		deltaIn = mag - abs(radius1 - radius2)
		deltaOut = mag-(radius1 + radius2)
		if abs(deltaIn) > abs(deltaOut):## outer tangent
			difference = deltaOut * self.para1
			dx, dy = cx/mag*difference, cy/mag*difference
			self.cc1.point1.x += dx
			self.cc1.point1.y += dy
			if self.cc1.fixedRadius==False:
				self.cc1.radius += difference
			self.cc2.point1.x -= dx
			self.cc2.point1.y -= dy
			if self.cc2.fixedRadius==False:
				self.cc2.radius += difference
			return abs(difference)*2
		else:## inner tangent
			difference=deltaIn * self.para1
			dx, dy = cx/mag*difference, cy/mag*difference
			self.cc1.point1.x += dx
			self.cc1.point1.y += dy
			self.cc2.point1.x -= dx
			self.cc2.point1.y -= dy
			if radius1>radius2:
				if self.cc1.fixedRadius==False:
					self.cc1.radius += difference
				if self.cc2.fixedRadius==False:
					self.cc2.radius -= difference
			else:
				if self.cc1.fixedRadius==False:
					self.cc1.radius -= difference
				if self.cc2.fixedRadius==False:
					self.cc2.radius += difference
			return abs(difference)*2
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
	def toString(self)-> str:
		return "type=module,moduletype=circle2circle,tag=%s,cc1=%s,cc2=%s,para1=%f"%(self.tag,self.cc1.tag, self.cc2.tag, self.para1)

class isometry(module):
	def __init__(self, app, line1:line, line2:line):
		super().__init__(app)
		self.moduletype="isometry"
		self.ln1=line1
		self.ln2=line2
		self.thisis='module'
		self.ratio1=1
		self.ratio2=1
		self.fixedRatio=True
		self.para1=0.25
		self.pref=preference(self.app, self)
		if self.ln1.isomParent!=None:
			if self.ln2.isomParent!=None:
				self.ln2.isomAncestor.isomParent=self.ln1.isomAncestor
			else:#if self.ln2.isomParent==None:
				self.ln2.isomParent=self.ln1
		else:#if self.ln1.isomParent==None:
			self.ln1.isomParent=self.ln1
			self.ln2.isomParent=self.ln1
	def evaluate(self):
		p1=self.ln1.point1
		p2=self.ln1.point2
		p3=self.ln2.point1
		p4=self.ln2.point2
		ax, ay=p2.x-p1.x, p2.y-p1.y
		magA=magnitude(ax, ay)
		bx, by=p4.x-p3.x, p4.y-p3.y
		magB=magnitude(bx, by)
		if magA==0.0 or magB==0.0:
			return
		delta= (magB*self.ratio1 - magA*self.ratio2) * self.para1 / (self.ratio1 + self.ratio2)
		delta1=delta*self.ratio2/ (self.ratio1 + self.ratio2)
		delta2=delta*self.ratio1/ (self.ratio1 + self.ratio2)
		cx, cy=ax/magA*delta1, ay/magA*delta1
		dx, dy=bx/magB*delta2, by/magB*delta2
		if self.ln1.point1.fixed==False:
			self.ln1.point1.x -= cx
			self.ln1.point1.y -= cy
		if self.ln1.point2.fixed==False:
			self.ln1.point2.x += cx
			self.ln1.point2.y += cy
		if self.ln2.point1.fixed==False:
			self.ln2.point1.x += dx
			self.ln2.point1.y += dy
		if self.ln2.point2.fixed==False:
			self.ln2.point2.x -= dx
			self.ln2.point2.y -= dy
		return abs(delta)*2
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
	def toString(self)-> str:
		return "type=module,moduletype=isometry,tag=%s,ln1=%s,ln2=%s,ratio1=%d,ratio2=%d,fixedRatio=%d,para1=%f"%(self.tag,self.ln1.tag, self.ln2.tag, self.ratio1, self.ratio2, int(self.fixedRatio), self.para1)



class parallel(module):
	def __init__(self, app, line1:line, line2:line):
		super().__init__(app)
		self.line1=line1
		self.line2=line2
		self.moduletype="parallel"
		self.thisis='module'
		self.para1=0.1
		self.pref=preference(self.app, self)
		pass
	def evaluate(self):
		p1:point=self.line1.point1
		p2:point=self.line1.point2
		p3:point=self.line2.point1
		p4:point=self.line2.point2
		theta1=math.atan2(p2.y-p1.y, p2.x-p1.x)
		theta2=math.atan2(p4.y-p3.y, p4.x-p3.x)
		##print("theta = %f"%(theta2-theta1))
		if theta1<theta2-math.pi*3/2:
			difference=-(math.pi*2-theta2+theta1)*self.para1
		elif theta1<theta2-math.pi:
			difference=(theta2-theta1-math.pi)*self.para1
		elif theta1<theta2-math.pi/2:
			difference=-(math.pi-theta2+theta1)*self.para1
		elif theta1<theta2:
			difference=(theta2-theta1)*self.para1
		elif theta1<theta2+math.pi/2:
			difference=-(theta1-theta2)*self.para1
		elif theta1<theta2+math.pi:
			difference=(math.pi-theta1+theta2)*self.para1
		elif theta1<theta2+math.pi*3/2:
			difference=-(theta1-theta2-math.pi)*self.para1
		else:#if theta1<theta1-math.pi*3/2:
			difference=(math.pi*2-theta1+theta2)*self.para1
		x1,y1,x2,y2 = rotation(
			self.line1.point1.x, self.line1.point1.y, self.line1.point2.x, self.line1.point2.y, difference
			)
		if self.line1.point1.fixed==False:
			self.line1.point1.x, self.line1.point1.y=x1,y1
		if self.line1.point2.fixed==False:
			self.line1.point2.x, self.line1.point2.y=x2,y2
		x3,y3,x4,y4 = rotation(
			self.line2.point1.x, self.line2.point1.y, self.line2.point2.x, self.line2.point2.y, -difference
			)
		if self.line2.point1.fixed==False:
			self.line2.point1.x, self.line2.point1.y=x3,y3
		if self.line2.point2.fixed==False:
			self.line2.point2.x, self.line2.point2.y=x4,y4
		return abs(difference)*2
		pass
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s || %s "%(self.line1.name, self.line2.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass
	def toString(self)-> str:
		return "type=module,moduletype=parallel,tag=%s,line1=%s,line2=%s,para1=%f"%(self.tag,self.line1.tag, self.line2.tag, self.para1)


class perpendicular(module):
	def __init__(self, app, line1:line, line2:line):
		super().__init__(app)
		self.line1=line1
		self.line2=line2
		self.moduletype="perpendicular"
		self.thisis='module'
		self.para1=0.1
		self.pref=preference(self.app, self)
		pass
	def evaluate(self):
		p1:point=self.line1.point1
		p2:point=self.line1.point2
		p3:point=self.line2.point1
		p4:point=self.line2.point2
		theta1=math.atan2(p2.y-p1.y, p2.x-p1.x)
		theta2=math.atan2(p4.y-p3.y, p4.x-p3.x)
		##print("theta = %f"%(theta2-theta1))
		if theta1<theta2-math.pi:
			difference=-(math.pi*3/2-theta2+theta1)*self.para1
		elif theta1<theta2:
			difference=(theta2-theta1-math.pi/2)*self.para1
		elif theta1<theta2+math.pi:
			difference=-(theta1-theta2-math.pi/2)*self.para1
		else:#
			difference=(math.pi*3/2-theta1+theta2)*self.para1
		x1,y1,x2,y2 = rotation(
			self.line1.point1.x, self.line1.point1.y, self.line1.point2.x, self.line1.point2.y, difference
			)
		if self.line1.point1.fixed==False:
			self.line1.point1.x, self.line1.point1.y=x1,y1
		if self.line1.point2.fixed==False:
			self.line1.point2.x, self.line1.point2.y=x2,y2
		x3,y3,x4,y4 = rotation(
			self.line2.point1.x, self.line2.point1.y, self.line2.point2.x, self.line2.point2.y, -difference
			)
		if self.line2.point1.fixed==False:
			self.line2.point1.x, self.line2.point1.y=x3,y3
		if self.line2.point2.fixed==False:
			self.line2.point2.x, self.line2.point2.y=x4,y4
		return abs(difference)*2
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s ⟂ %s "%(self.line1.name, self.line2.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass
	def toString(self)-> str:
		return "type=module,moduletype=perpendicular,tag=%s,line1=%s,line2=%s,para1=%f"%(self.tag,self.line1.tag, self.line2.tag, self.para1)



class horizontal(module):
	def __init__(self, app, line1:line):
		super().__init__(app)
		self.thisis='module'
		self.moduletype='horizontal'
		self.line1=line1
		self.para1=0.1
		self.pref=preference(self.app, self)
		pass
	def evaluate(self):
		p1:point=self.line1.point1
		p2:point=self.line1.point2
		theta=math.atan2(p2.y-p1.y, p2.x-p1.x)
		if -math.pi/2<=theta and theta<=math.pi/2:
			difference=-theta*self.para1
		elif -math.pi/2>theta:
			difference=(-math.pi-theta)*self.para1
		else:
			difference=(math.pi-theta)*self.para1
		x1,y1,x2,y2 = rotation(p1.x, p1.y, p2.x, p2.y, difference)
		if self.line1.point1.fixed==False:
			self.line1.point1.x, self.line1.point1.y = x1,y1
		if self.line1.point2.fixed==False:
			self.line1.point2.x, self.line1.point2.y = x2,y2
		return abs(difference)
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="turquoise",width=3)
		canvas.create_text(x+5,y+5,text="Module : %s"%(self.moduletype), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s = "%(self.line1.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass
	def toString(self)-> str:
		return "type=module,moduletype=horizontal,tag=%s,line1=%s,para1=%f"%(self.tag,self.line1.tag, self.para1)


