import tkinter as tk
from PIL import Image, ImageTk
from point import point
from line import line
from circle import circle
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

class addPointItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click in the open area."]
	def phaseActions(self, app):
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
class addCircleItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click in the open area."]
class addAngleItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click the second point.", "Click the third point."]
class addLocusItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point."]
