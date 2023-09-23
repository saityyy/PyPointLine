from itertools import filterfalse
import tkinter as tk
import random
from preference import preference
from utils import *

class object:
	""" """
	def __init__(self,app):
		""" """
		self.app=app
		self.id=-1
		self.pref=None
		self.name='X'
		self.thisis=None
		self.active=True
		self.toBeDestroyed=False
		pass
	pass
	def drawObject(self, app):
		pass
	def drawLog(self, app):
		pass
	def drawPreference(self, app):
		pass
	def matter(self, obj:object)->bool:
		return False


class xxxxx(object):
	def __init__(self, app):
		super().__init__(app)
		self.thisis:str='xxxxx'
		self.name=''
		self.pref=preference(app, self)
		pass
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="white",width=3)
		canvas.create_text(x+5,y+5,text="PointLine : application", anchor=tk.NW, font=("",18), width=270 )
		
		thisLine=""
		if app.conflictEvaluation:	
			canvas.create_text(x+5,y+31,text="Conflict evaluations", anchor=tk.NW, font=("",18), width=270, fill="red")
		#canvas.create_text(x+5,y+57,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		pass
	

class point(object):
	def __init__(self, app, x, y):
		super().__init__(app)
		self.x:float=x
		self.y:float=y
		self.thisis:str='point'
		self.color='blue'
		self.fixed=False
		self.fixedX=x
		self.fixedY=y
		self.para1=0.1
		self.name=self.youngestName(app)
		self.fixedColor='red'
		self.showName=True
		self.showNamePosition="free"
		self.id=app.nextID
		self.tag="tag_%00d"%(app.nextID)
		app.nextID += 1
		self.pref=preference(self.app, self)
		pass
	def drawObject(self, app):
		xx0,yy0=app.world2Canvas(self.x,self.y)
		r=app.pointRadius
		if self.fixed:
			app.mainCanvas.create_oval(xx0-r,yy0-r,xx0+r,yy0+r, fill=self.fixedColor, tag=self.tag)
		else:
			app.mainCanvas.create_oval(xx0-r,yy0-r,xx0+r,yy0+r, fill=self.color, tag=self.tag)
		if self.showName:
			if self.showNamePosition=="free":
				vx,vy=xx0-app.pointNameCenterX, yy0-app.pointNameCenterY
				mag=math.sqrt(vx*vx+vy*vy)
				vx,vy = vx*20/mag, vy*20/mag
				app.mainCanvas.create_text(xx0+vx, yy0+vy, text=self.name, anchor=tk.CENTER, font=("",24))
		pass
	def evaluate(self):
		if self.fixed:
			x1=(self.x-self.fixedX)*self.para1
			y1=(self.y-self.fixedY)*self.para1
			self.x -= x1
			self.y -= y1
			return magnitude(x1,y1)
		else:
			return 0
		pass
	@property
	def getNamePosition(self):
		xx0,yy0=self.app.world2Canvas(self.x,self.y)
		if self.showNamePosition=="free":
			vx,vy=xx0-self.app.pointNameCenterX, yy0-self.app.pointNameCenterY
			mag=math.sqrt(vx*vx+vy*vy)
			vx,vy = vx*25/mag, vy*25/mag
			return self.app.canvas2World(xx0+vx, yy0+vy)
		return 0,0
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="SeaGreen1",width=3)
		canvas.create_text(x+5,y+5,text="Point : %s"%(self.name), anchor=tk.NW, font=("",18), width=270 )
		thisLine="(%0.3f,%0.3f)"%(self.x, self.y)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		if self.fixed:
			text1="Fixed"
		else:
			text1="Not fixed"
		if self.showName:
			text2="Show name"
		else:
			text2="Hide name"
		canvas.create_text(x+5,y+57,text="%s, %s"%(text1, text2),  anchor=tk.NW, font=("",18), width=270 )
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
	def toString(self)-> str:
		return "type=point,x=%f,y=%f,tag=%s,name=%s,fixed=%d,showName=%d,active=%d"%(self.x, self.y, self.tag, self.name, int(self.fixed), int(self.showName), int(self.active))
	def toTeXString(self)-> str:
		if self.showName:
			return "\\draw[fill=black](%f, %f) circle  (1.5pt);\n\\draw[fill=black](%f, %f) node {%s};"%(self.x, self.y, self.getNamePosition[0], self.getNamePosition[1], self.name)
		else:
			return "\\draw[fill=black](%f, %f) circle  (1.5pt);"%(self.x, self.y)
	def purturb(self, delta):
		theta=math.pi*random.random()*2
		self.x += delta*math.cos(theta)
		self.y += delta*math.sin(theta)


class line(object):
	def __init__(self, app, point1:point, point2:point):
		super().__init__(app)
		self.point1=point1
		self.point2=point2
		self.thisis='line'
		self.length=1.0
		self.showLength=False
		self.fixedLength=False
		self.equationType=0
		self.isomID=-1
		self.isomColor='grey'
		self.isomParent=None
		self.name=self.youngestName(app)
		self.showName=False
		self.tag="tag_%00d"%(app.nextID)
		self.para1=0.1
		app.nextID += 1
		self.pref=preference(self.app, self)
	def drawObject(self, app):
		if self.isomParent!=None:
			self.isomColor=self.isomAncestor.isomColor
		pt1=self.point1
		pt2=self.point2
		x1,y1=app.world2Canvas(pt1.x, pt1.y)
		x2,y2=app.world2Canvas(pt2.x, pt2.y)
		isomID=0
		rx,ry=x2-x1,y2-y1
		sx,sy=y2-y1,-x2+x1
		mag=dist(x1,y1,x2,y2)
		rx,ry=rx/mag, ry/mag
		sx,sy=sx/mag, sy/mag
		tx,ty=(x1+x2)/2,(y1+y2)/2
		if self.showLength:
			app.mainCanvas.create_text(tx+sx*15,ty+sy*15,text="%0.3f"%(mag/app.zoom), font=("",18), anchor=tk.CENTER)
			pass
		width=app.lineWidth
		app.mainCanvas.create_line(x1,y1,x2,y2, fill=self.isomColor, width=width)
		if self.app.showIsom:
			if self.isomColor==app.isomColors[0]:
				app.mainCanvas.create_line(tx+sx*10,ty+sy*10,tx-sx*10,ty-sy*10, fill=self.isomColor, width=3)
			elif self.isomColor==app.isomColors[1]:
				app.mainCanvas.create_line(tx+sx*10+rx*5,ty+sy*10+ry*5,tx-sx*10+rx*5,ty-sy*10+ry*5, fill=self.isomColor, width=3)
				app.mainCanvas.create_line(tx+sx*10-rx*5,ty+sy*10-ry*5,tx-sx*10-rx*5,ty-sy*10-ry*5, fill=self.isomColor, width=3)
			elif self.isomColor==app.isomColors[2]:
				app.mainCanvas.create_oval(tx-10,ty-10,tx+10,ty+10, outline=self.isomColor, width=3)
			pass
	def evaluate(self):
		if self.fixedLength:
			p1=self.point1
			p2=self.point2
			ax, ay=p2.x-p1.x, p2.y-p1.y
			magA=magnitude(ax, ay)
			if magA==0.0:
				return
			delta= (self.length - magA) * self.para1 
			cx, cy=ax/magA*delta, ay/magA*delta
			if self.point1.fixed==False:
				self.point1.x -= cx
				self.point1.y -= cy
			if self.point2.fixed==False:
				self.point2.x += cx
				self.point2.y += cy
			return abs(delta)*2
		return 0
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="Orchid1",width=3)
		if self.showLength:
			thisLine="%s - %s (%0.3f)"%(self.point1.name, self.point2.name, dist(self.point1.x,self.point1.y,self.point2.x,self.point2.y))
		else:
			thisLine="%s - %s "%(self.point1.name, self.point2.name)
		canvas.create_text(x+5,y+5,text="Line : %s (%s)"%(self.name, thisLine), anchor=tk.NW, font=("",18), width=270 )
		if self.fixedLength==False:
			self.length=dist(self.point1.x,self.point1.y,self.point2.x,self.point2.y)
		if abs(self.point1.x-self.point2.x)<0.001:
			thisLine="x=(%0.3f)"%(self.point1.x)
		else:
			a=(self.point1.y-self.point2.y)/(self.point1.x-self.point2.x)
			b=(-self.point2.x*self.point1.y+self.point1.x*self.point2.y)/(self.point1.x-self.point2.x)
			if abs(a)<0.001:
				thisLine="y=%f0.3f"%(b)
			elif abs(b)<0.001:
				thisLine="y=%0.3fx"%(a)
			elif b<0:
				thisLine="y=%0.3fx%0.3f"%(a,b)
			else:
				thisLine="y=%0.3fx+%0.3f"%(a,b)
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
	def toString(self)-> str:
		return "type=line,point1=%s,point2=%s,tag=%s,name=%s,showLength=%d,showName=%d,fixedLength=%d,active=%d"%(self.point1.tag, self.point2.tag, self.tag, self.name, int(self.showLength), int(self.showName), int(self.fixedLength), int(self.active))
	def toTeXString(self)-> str:
		return "\\draw (%f, %f)-- (%f, %f);"%(self.point1.x, self.point1.y, self.point2.x, self.point2.y);
	@property
	def isomAncestor(self):
		count=len(self.app.lines)
		node=self
		for repeat in range(count):
			if node.isomParent==None:
				return None
			elif node.isomParent==node:
				return node
			else:
				node=node.isomParent
		return None
	def matter(self, obj):
		if obj!=None and obj==self.point1:
			return True
		if obj!=None and obj==self.point2:
			return True
		return False


class circle(object):
	def __init__(self, app, point:point, radius:float):
		super().__init__(app)		
		self.point1=point
		self.radius=radius
		self.thisis='circle'
		self.name=self.youngestName(app)
		self.showName=False
		self.fixedRadius=False
		self.tag="tag_%00d"%(app.nextID)
		self.pref=preference(self.app, self)
		app.nextID += 1
	
	def drawObject(self, app):
		x1,y1=app.world2Canvas(self.point1.x, self.point1.y)
		r=self.radius * app.zoom
		app.mainCanvas.create_oval(x1-r,y1-r,x1+r,y1+r, outline='grey', width=4)
		pass

	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="salmon1",width=3)
		canvas.create_text(x+5,y+5,text="Circle : %s"%(self.name), anchor=tk.NW, font=("",18), width=270 )
		thisLine="%s - %f"%(self.point1.name, self.radius)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
		pass
	def drawPreference(self, app):
		pass
	def youngestName(self, app):
		for name in ["C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","C11","C12","C13","C14","C15","C16","C17","C18","C18","C19","C20"]:
			for obj in app.circles:
				if obj.name==name:
					break
			else:
				return name
		return "C0"
	def toString(self)-> str:
		return "type=circle,point1=%s,radius=%f,tag=%s,name=%s,fixedRadius=%d,active=%d"%(self.point1.tag, self.radius, self.tag, self.name, int(self.fixedRadius), int(self.active))
	def toTeXString(self)-> str:
		return "\\draw(%f, %f) circle (%f);\n"%(self.point1.x, self.point1.y, self.radius)
	def matter(self, obj):
		if obj!=None and obj==self.point1:
			return True
		return False
		


class angle(object):
	def __init__(self, app, point1:point, point2:point, point3:point):
		super().__init__(app)		
		self.point1=point1
		self.point2=point2
		self.point3=point3
		self.thisis='angle'
		self.name=self.youngestName(app)		
		self.showArc=True
		self.showValue=True
		self.fixValue=False
		self.value=0
		self.tag="tag_%03d"%(app.nextID)
		app.nextID += 1
		self.pref=preference(self.app, self)
		self.start=0
		self.extent=90
		self.value=math.pi/2
		self.para1=0.1
	def restoreValue(self):
		if self.fixValue==False:
			theta1=math.atan2(self.point1.y-self.point2.y, self.point1.x-self.point2.x)
			theta3=math.atan2(self.point3.y-self.point2.y, self.point3.x-self.point2.x)
			rad2ang=180/math.pi
			if theta1+math.pi<theta3:
				self.start, self.extent = theta3, (theta1 - theta3 + 2*math.pi)
			elif theta1<theta3:
				self.start, self.extent = theta1, (theta3 - theta1)
			elif theta1-math.pi<theta3:
				self.start, self.extent = theta3, (theta1 - theta3)
			else:
				self.start, self.extent = theta1, (theta3 - theta1 + 2*math.pi)
			self.value=self.extent*rad2ang
	def drawObject(self, app):
		xx1,yy1=app.world2Canvas(self.point1.x,self.point1.y)
		xx2,yy2=app.world2Canvas(self.point2.x,self.point2.y)
		xx3,yy3=app.world2Canvas(self.point3.x,self.point3.y)
		theta1=math.atan2(-yy1+yy2, xx1-xx2)
		theta3=math.atan2(-yy3+yy2, xx3-xx2)
		rad2ang=180/math.pi
		if theta1+math.pi<theta3:
			self.start, self.extent = theta3, (theta1 - theta3 + 2*math.pi)
		elif theta1<theta3:
			self.start, self.extent = theta1, (theta3 - theta1)
		elif theta1-math.pi<theta3:
			self.start, self.extent = theta3, (theta1 - theta3)
		else:
			self.start, self.extent = theta1, (theta3 - theta1 + 2*math.pi)
		midpoint = self.start+self.extent/2
		start=self.start*rad2ang
		extent=self.extent*rad2ang
		if self.fixValue==False:
			self.value=extent
		if self.showArc:
			app.mainCanvas.create_arc(xx2-35, yy2-35, xx2+35, yy2+35, start=start, extent=extent, style=tk.ARC, width=4, outline='DarkGoldenrod4')
		if self.showValue:
			app.mainCanvas.create_text(xx2+55*math.cos(midpoint), yy2-55*math.sin(midpoint),text="%d"%(int(self.value)), anchor=tk.CENTER, font=("",18))
	def evaluate(self):
		if self.fixValue:
			rad2ang=180/math.pi
			if self.point1.fixed and (not self.point2.fixed) and self.point3.fixed:
				Ax, Ay = self.point1.x, self.point1.y
				Bx, By = self.point2.x, self.point2.y
				Cx, Cy = self.point3.x, self.point3.y
				BA = dist(Ax, Ay, Bx, By)
				BC = dist(Cx, Cy, Bx, By)
				AC = dist(Ax, Ay, Cx, Cy)
				Mx = (Ax * BC + Cx * BA) / (BA + BC)
				My = (Ay * BC + Cy * BA) / (BA + BC)
				Dx, Dy = Bx - Mx, By - My
				ND = dist(Dx, Dy, 0, 0)
				if ND < 0.00001: 
					return 0
				Dx /= ND
				Dy /= ND
				DeclineBA = math.atan2(Ay - By, Ax - Bx)
				DeclineBC = math.atan2(Cy - By, Cx - Bx)
				Angle = DeclineBC - DeclineBA
				PI = math.pi
				if Angle < -2*PI:
					Angle += 2*PI
				if Angle < 0:
					Angle += 2*PI
				if Angle >= 2*PI:
					Angle -= 2*PI
				if PI <= Angle and Angle < 2*PI:
					Angle = 2*PI - Angle
				Error = (Angle - self.value/rad2ang) * AC * 0.1 * self.para1;
				Dx *= Error;
				Dy *= Error;
				self.point2.x += Dx
				self.point2.y += Dy
				return abs(Error);
			theta1=math.atan2(self.point1.y-self.point2.y, self.point1.x-self.point2.x)
			theta3=math.atan2(self.point3.y-self.point2.y, self.point3.x-self.point2.x)
			if theta1+math.pi<theta3:
				self.start, self.extent = theta3, (theta1 - theta3 + 2*math.pi)
				delta= -(self.extent - self.value/rad2ang)*self.para1
			elif theta1<theta3:
				self.start, self.extent = theta1, (theta3 - theta1)
				delta= (self.extent - self.value/rad2ang)*self.para1
			elif theta1-math.pi<theta3:
				self.start, self.extent = theta3, (theta1 - theta3)
				delta= -(self.extent - self.value/rad2ang)*self.para1
			else:
				self.start, self.extent = theta1, (theta3 - theta1 + 2*math.pi)
				delta= (self.extent - self.value/rad2ang)*self.para1
			x1,y1,x2,y2=rotation(self.point1.x,self.point1.y,self.point2.x,self.point2.y,delta)
			x3,y3,x4,y4=rotation(self.point3.x,self.point3.y,x2,y2,-delta)
			if self.point1.fixed==False:
				self.point1.x, self.point1.y = x1,y1
			if self.point2.fixed==False:
				self.point2.x, self.point2.y = x4,y4
			if self.point3.fixed==False:
				self.point3.x, self.point3.y = x3,y3
				
			return abs(delta)*2
		return 0.0
	def drawLog(self, app):
		canvas=app.prefCanvas
		x,y,w,h=5, app.logLineFeed+5, 280, 90
		app.logLineFeed += 100
		canvas.create_rectangle(x,y,x+w,y+h,fill="gold1",width=3)
		canvas.create_text(x+5,y+5,text="Angle : %s"%(self.name), anchor=tk.NW, font=("",18), width=270 )
		if self.showValue:
			thisLine="∠%s - %s - %s (%d)"%(self.point1.name, self.point2.name, self.point3.name, int(self.value))
		else:
			thisLine="∠%s - %s - %s"%(self.point1.name, self.point2.name, self.point3.name)
		canvas.create_text(x+5,y+31,text=thisLine, anchor=tk.NW, font=("",18), width=270 )
		canvas.create_text(x+5,y+57,text="Hide Value",  anchor=tk.NW, font=("",18), width=270 )
		pass
	def drawPreference(self, app):
		pass
	def youngestName(self, app):
		for name in ["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13","A14","A15","A16","A17","A18","A18","A19","A20"]:
			for obj in app.angles:
				if obj.name==name:
					break
			else:
				return name
		return "A0"
	def toString(self)-> str:
		return "type=angle,point1=%s,point2=%s,point3=%s,tag=%s,name=%s,showArc=%d,showValue=%d,value=%d,fixValue=%d,active=%d"%(
			self.point1.tag, self.point2.tag, self.point3.tag, self.tag, self.name, int(self.showArc), int(self.showValue), int(self.value), int(self.fixValue), int(self.active))
	def toTeXString(self)-> str:
		##
		return ""
	def matter(self, obj):
		if obj!=None and obj==self.point1:
			return True
		if obj!=None and obj==self.point2:
			return True
		if obj!=None and obj==self.point3:
			return True
		return False


class locus(object):
	def __init__(self, point1:point):
		self.point1=point1
		self.thisis='locus'
	pass
	def drawLog(self, app):
		pass
	def drawPreference(self, app):
		pass

