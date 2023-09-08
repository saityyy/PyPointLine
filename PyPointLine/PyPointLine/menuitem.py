import tkinter as tk
import sys
from PIL import Image, ImageTk

from object import point, line, circle, angle, xxxxx
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
	def onActions(self, app):
		pass

class addPointItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click in the open area."]
	def phaseActions(self, app):
		if app.mp.widget!=app.mainCanvas:
			return
		if app.clickedPoint==None and app.clickedLine==None and app.clickedCircle==None:
			## create new point
			newPoint=point(app, app.mp.x, app.mp.y)
			app.logs.append(newPoint)
			app.drawAll()
		elif app.clickedPoint==None and app.clickedLine!=None:
			## create new point
			newPoint=point(app, app.mp.x, app.mp.y)
			app.logs.append(newPoint)
			newModule=point2line(app, newPoint, app.clickedLine)
			app.logs.append(newModule)
			app.drawAll()


		pass


class midPointItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click another point."]
		self.point1=None
		self.point2=None
	def phaseActions(self, app):
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedPoint!=None:
				self.point1=app.clickedPoint
				app.onModePhase=1
				app.headerText=app.onMode.headerText[app.onModePhase]
				app.drawAll()
		elif app.onModePhase==1:
			if app.clickedPoint!=None and app.clickedPoint!=self.point1:
				self.point2=app.clickedPoint
			else:
				return
			### add a new point
			x=(self.point1.x+self.point2.x)*0.5
			y=(self.point1.y+self.point2.y)*0.5
			newPoint=point(app, x, y)
			app.logs.append(newPoint)			
			### add a new addMidPoint(module)
			newModule=midpoint(app, self.point1, self.point2, newPoint)
			app.logs.append(newModule)
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
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedPoint!=None:
				self.point1=app.clickedPoint
			else:#if app.clickedPoint==None:
				newPoint=point(app, app.mp.x, app.mp.y)
				app.logs.append(newPoint)
				self.point1=newPoint
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedPoint!=None:
				if app.clickedPoint!=self.point1:
					self.point2=app.clickedPoint
				else:
					return
			elif app.clickedPoint==None:
				newPoint=point(app, app.mp.x, app.mp.y)
				app.logs.append(newPoint)
				self.point2=newPoint
			else:
				return
			### add a new point
			newLine=line(app, self.point1, self.point2)
			app.logs.append(newLine)	
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
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedPoint==None:
				newPoint=point(app, app.mp.x, app.mp.y)
				app.logs.append(newPoint)
				self.point1=newPoint
			else:
				self.point1=app.clickedPoint
			if self.point1.thisis=='point':
				app.onModePhase=1
				app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedPoint==None:
				### add a new point
				newCircle=circle(app, self.point1, dist(self.point1.x, self.point1.y, app.mp.x, app.mp.y))
				app.logs.append(newCircle)	
			else:
				self.point2=app.clickedPoint
				### add a new point
				newCircle=circle(app, self.point1, dist(self.point1.x, self.point1.y, self.point2.x, self.point2.y))
				app.logs.append(newCircle)	
				newModule=point2circle(app, self.point2, newCircle)
				app.logs.append(newModule)	
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
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedPoint!=None:
				self.point1=app.clickedPoint
			elif app.clickedPoint==None:
				newPoint=point(app, app.mp.x, app.mp.y)
				app.logs.append(newPoint)
				self.point1=newPoint
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedPoint!=None:
				if app.clickedPoint!=self.point1:
					self.point2=app.clickedPoint
				else:
					return
			elif app.clickedPoint==None:
				newPoint=point(app, app.mp.x, app.mp.y)
				app.logs.append(newPoint)
				self.point2=newPoint
			app.onModePhase=2
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==2:
			if app.clickedPoint!=None:
				if app.clickedPoint!=self.point1 and app.clickedPoint!=self.point2:
					self.point3=app.clickedPoint
				else:
					return
			elif app.clickedPoint==None:
				newPoint=point(app, app.mp.x, app.mp.y)
				app.logs.append(newPoint)
				self.point3=newPoint
			### add a new point
			newAngle:angle=angle(app, self.point1, self.point2, self.point3)
			app.logs.append(newAngle)	
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
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedPoint!=None:
				self.point1=app.clickedPoint
			else:
				return
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedPoint!=None and app.clickedPoint!=self.point1:
				self.point2=app.clickedPoint
			else:
				return
			### add a new point
			newModule=point2point(app, self.point1, self.point2)
			app.logs.append(newModule)	
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
		if app.mp.widget!=app.mainCanvas:
			return
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
			newModule=point2line(app, self.point1, self.line1)
			app.logs.append(newModule)	
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
		if app.mp.widget!=app.mainCanvas:
			return
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
			newModule=point2circle(app, self.point1, self.circle1)
			app.logs.append(newModule)	
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
		if app.mp.widget!=app.mainCanvas:
			return
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
			newModule=line2circle(app, self.line1, self.circle1)
			app.logs.append(newModule)	
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
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedCircle!=None:
				self.circle1=app.clickedCircle
			else:
				return
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedCircle!=None and app.clickedCircle!=self.circle1:
				self.circle2=app.clickedCircle
			else:
				return
			### add a new module
			newModule=circle2circle(app, self.circle1, self.circle2)
			app.logs.append(newModule)	
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
		self.line1=None
		self.line2=None
	def phaseActions(self, app):
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedLine!=None:
				self.line1=app.clickedLine
			else:
				return
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedLine!=None and self.line1!=app.clickedLine:
				self.line2=app.clickedLine
			else:
				return
			### add a new module
			newModule=isometry(app, self.line1, self.line2)
			app.logs.append(newModule)	
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass


class menuRatioLengthItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one line.","Click another line."]
	def phaseActions(self, app):
		if app.mp.widget!=app.mainCanvas:
			return
		pass


class menuParaItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one line.","Click another line."]
		self.line1=None
		self.line2=None
	def phaseActions(self, app):
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedLine!=None:
				self.line1=app.clickedLine
			else:
				return
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedLine!=None and self.line1!=app.clickedLine:
				self.line2=app.clickedLine
			else:
				return
			### add a new module
			newModule=parallel(app, self.line1, self.line2)
			app.logs.append(newModule)	
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass


class menuPerpItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one line.","Click another line."]
		self.line1=None
		self.line2=None
	def phaseActions(self, app):
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedLine!=None:
				self.line1=app.clickedLine
			else:
				return
			app.onModePhase=1
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		elif app.onModePhase==1:
			if app.clickedLine!=None and self.line1!=app.clickedLine:
				self.line2=app.clickedLine
			else:
				return
			### add a new module
			newModule=perpendicular(app, self.line1, self.line2)
			app.logs.append(newModule)	
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass
		pass


class menuHoriItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one line."]
		self.line=None
	def phaseActions(self, app):
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedLine!=None:
				self.line=app.clickedLine
			else:
				return
			### add a new module
			newModule=horizontal(app, self.line)
			app.logs.append(newModule)	
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass

class menuFixPointItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point."]
	def phaseActions(self, app):
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedPoint!=None:
				app.clickedPoint.fixed = not app.clickedPoint.fixed
			else:
				return
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass		
	
class menuDeleteAllItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=[""]
	def onActions(self, app):
		app.logs.clear()
		newXXXXX=xxxxx(app)
		app.logs.append(newXXXXX)
		pass
	

class menuBisectorItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.angle1=None
		self.angle2=None
		self.headerText=["Click one angle.","Click another angle."]
	def phaseActions(self, app):
		if app.mp.widget!=app.mainCanvas:
			return
		if app.onModePhase==0:
			if app.clickedAngle!=None:
				self.angle1=app.clickedAngle
				app.onModePhase=1
				app.headerText=app.onMode.headerText[app.onModePhase]
				app.drawAll()
			else:
				return
		elif app.onModePhase==1:
			if app.clickedAngle!=None and app.clickedAngle!=self.angle1:
				self.angle2=app.clickedAngle
				newModule=bisector(app, self.angle1, self.angle2)
				app.logs.append(newModule)
			else:
				return
			### post-process
			app.calculatorEvaluate(repeat=50)
			app.onModePhase=0
			app.headerText=app.onMode.headerText[app.onModePhase]
			app.drawAll()
		pass


class menuOpenItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=[""]
	def onActions(self, app):
		app.openFile()
		pass

class menuSaveItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=[""]
	def onActions(self, app):
		app.saveFile()
		pass


class menuQuitItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=[""]
	def onActions(self, app):
		app.quitApp()

	pass



