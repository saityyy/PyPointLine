import tkinter as tk
from PIL import Image, ImageTk
from object import point, line, circle, angle, locus
from module import *

class menuItem:
	
	def __init__(self, name,x,y):
		self.falename=name
		self.x=x
		self.y=y
		self.menuIcon=None
		self.icon = Image.open(open(name, 'rb'))
		self.icon = self.icon.resize((75,75))
		self.icon = ImageTk.PhotoImage(self.icon)
		self.left = x*100
		self.top = y*100
		self.width = 100
		self.height = 100
		self.headerText = [""]

	def showIcon(self, canvas):
		canvas.create_image(100*self.x+12.5,100*self.y+12.5,image=self.icon, tag="menuIcon", anchor=tk.NW)
	pass
	def phaseActions(self, app):
		pass

class addPointItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click in the open area."]
	def phaseActions(self, app):
		if app.clickedPoint==None and app.clickedLine==None and app.clickedCircle==None:
			## create new point
			newPoint=point(app.mp.x, app.mp.y)
			app.points.append(newPoint)
			app.drawAll()
		pass


class midPointItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click another point."]
		self.point1=None
		self.point2=None
	def phaseActions(self, app):
		if app.clickedPoint!=None and app.onModePhase==0:
			self.point1=app.clickedPoint
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.clickedPoint!=None and app.onModePhase==1:
			self.point2=app.clickedPoint
			### add a new point
			x=(self.point1.x+self.point2.x)*0.5
			y=(self.point1.y+self.point2.y)*0.5
			newPoint=point(x,y)
			app.points.append(newPoint)			
			### add a new addMidPoint(module)
			newModule=midpoint(self.point1,self.point2,newPoint)
			app.modules.append(newModule)
			### post-process
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()

class addLineItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click another point."]
		self.point1=None
		self.point2=None
	def phaseActions(self, app):
		if app.onModePhase==0:
			if app.clickedPoint!=None:
				self.point1=app.clickedPoint
			elif app.clickedPoint==None:
				newPoint=point(app.mp.x, app.mp.y)
				app.points.append(newPoint)
				self.point1=newPoint
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedPoint!=None:
				self.point2=app.clickedPoint
			elif app.clickedPoint==None:
				newPoint=point(app.mp.x, app.mp.y)
				app.points.append(newPoint)
				self.point2=newPoint
			### add a new point
			newLine=line(self.point1, self.point2)
			app.lines.append(newLine)	
			### post-process
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass

class addCircleItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click in the open area."]
		self.point1=None
		self.point2=None
	def phaseActions(self, app):
		if app.onModePhase==0:
			if app.clickedPoint==None:
				newPoint=point(app.mp.x, app.mp.y)
				app.points.append(newPoint)
				self.point1=newPoint
			else:
				self.point1=app.clickedPoint
			if self.point1.thisis=='point':
				app.onModePhase=1
				app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedPoint==None:
				newPoint=point(app.mp.x, app.mp.y)
				app.points.append(newPoint)
				self.point2=newPoint
			else:
				self.point2=app.clickedPoint
			### add a new point
			newCircle=circle(self.point1, self.point2)
			app.circles.append(newCircle)	
			### post-process
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()

class addAngleItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click the second point.", "Click the third point."]
		self.point1=None
		self.point2=None
		self.point3=None
	def phaseActions(self, app):
		if app.onModePhase==0:
			if app.clickedPoint!=None:
				self.point1=app.clickedPoint
			elif app.clickedPoint==None:
				newPoint=point(app.mp.x, app.mp.y)
				app.points.append(newPoint)
				self.point1=newPoint
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedPoint!=None:
				self.point2=app.clickedPoint
			elif app.clickedPoint==None:
				newPoint=point(app.mp.x, app.mp.y)
				app.points.append(newPoint)
				self.point2=newPoint
			app.onModePhase=2
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==2:
			if app.clickedPoint!=None:
				self.point3=app.clickedPoint
			elif app.clickedPoint==None:
				newPoint=point(app.mp.x, app.mp.y)
				app.points.append(newPoint)
				self.point3=newPoint
			### add a new point
			newAngle:angle=angle(self.point1, self.point2, self.point3)
			app.angles.append(newAngle)	
			### post-process
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass

class addLocusItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point."]
	def phaseActions(self, app):
		pass

class menuP2PItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click another point."]
	def phaseActions(self, app):
		if app.onModePhase==0:
			if app.clickedPoint!=None:
				self.point1=app.clickedPoint
			else:
				return
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedPoint!=None:
				self.point2=app.clickedPoint
			else:
				return
			### add a new point
			newModule=point2point(self.point1, self.point2)
			app.modules.append(newModule)	
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass

class menuP2LItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click one line."]
		self.point1=None
		self.line1=None
	def phaseActions(self, app):
		if app.onModePhase==0:
			if app.clickedPoint!=None:
				self.point1=app.clickedPoint
			else:
				return
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedLine!=None:
				self.line1=app.clickedLine
			else:
				return
			### add a new point
			newModule=point2line(self.point1, self.line1)
			app.modules.append(newModule)	
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass

class menuP2CItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click one circle."]
		self.point1=None
		self.circle1=None

	def phaseActions(self, app):
		if app.onModePhase==0:
			if app.clickedPoint!=None:
				self.point1=app.clickedPoint
			else:
				return
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedCircle!=None:
				self.circle1=app.clickedCircle
			else:
				return
			### add a new point
			newModule=point2circle(self.point1, self.circle1)
			app.modules.append(newModule)	
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass

class menuL2CItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one line.", "Click one circle."]
		self.line1=None
		self.circle1=None

	def phaseActions(self, app):
		if app.onModePhase==0:
			if app.clickedLine!=None:
				self.line1=app.clickedLine
			else:
				return
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedCircle!=None:
				self.circle1=app.clickedCircle
			else:
				return
			### add a new point
			newModule=line2circle(self.line1, self.circle1)
			app.modules.append(newModule)	
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass

class menuC2CItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one circle.","Click another circle."]
		self.circle1=None
		self.circle2=None

	def phaseActions(self, app):
		if app.onModePhase==0:
			if app.clickedCircle!=None:
				self.circle1=app.clickedCircle
			else:
				return
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedCircle!=None:
				self.circle2=app.clickedCircle
			else:
				return
			### add a new point
			newModule=circle2circle(self.circle1, self.circle2)
			app.modules.append(newModule)	
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass


class menuIsomItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one line.","Click another line."]
	def phaseActions(self, app):
		pass


class menuRatioLengthItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one line.","Click another line."]
	def phaseActions(self, app):
		pass


class menuParaItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one line.","Click another line."]
	def phaseActions(self, app):
		pass


class menuPerpItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one line.","Click another line."]
	def phaseActions(self, app):
		pass


class menuHoriItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one line."]
	def phaseActions(self, app):
		pass


class menuBisectorItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.","Click the second point.","Click the third point."]
	def phaseActions(self, app):
		pass


