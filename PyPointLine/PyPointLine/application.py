
import tkinter as tk
import os

from utils import mousePosition, isNear
from pane import pane
from calculator import calculator
from menuitem import menuItem
from point import point
from module import midpoint

class application:
	"""
	"""
	def __init__(self, root):
		""" """
		self.root = root
		self.canvas = tk.Canvas(root, width=1200, height=1000)
		self.canvas.pack()
		self.mp=mousePosition()
		self.nextID=0
		self.pointName='A'
		self.lineName='a'
		self.pointRadius=5# global radius of a point in canvas
		self.lineWidth=3# global width of a line in canvas
		self.cx=500
		self.cy=500
		self.zoom=100
		self.points=[]
		self.modules=[]

		self.dispMenu=False
		self.dispPreference=False

		##self.file=fileIO(self)
		self.calculator=calculator()

		self.headerPane=pane(self, 0,0,1000,50)
		self.mainPane=pane(self,0,50,1000,950)
		self.rightPane=pane(self,1000,0,200,1000)
		self.initilizeMenuItems()


		point0=point(0,0)
		self.points.append(point0)
		point1=point(1,1)
		self.points.append(point1)
		point2=point(1,0)
		self.points.append(point2)

		module0=midpoint(point0,point1,point2)
		self.modules.append(module0)

		self.drawAll(self.canvas)
		pass


	def world2Canvas(self, x,y):
		return self.cx+self.zoom * x, self.cy+self.zoom * y

	def canvas2World(self, x,y):
		return (-self.cx+ x) / self.zoom , (-self.cy+ y)/self.zoom


	def drawAll(self, canvas):
		""" """
		self.canvas.delete("all")
		if self.dispMenu==False:
			self.drawMenuOnIcon(canvas)
			self.drawAllObjects(canvas)
			#self.drawAllLogs()
			if self.dispPreference==True:
				#self.drawProference()
				pass
			pass
		else: # dispMenu==True:
			self.drawAllMenu(canvas)
			pass

	def drawAllObjects(self, canvas):
		for pt in self.points:
			xx0,yy0=self.world2Canvas(pt.x,pt.y)
			canvas.create_oval(xx0-5,yy0-5,xx0+5,yy0+5, fill='blue')

	def updateCoordinates(self, event):
		""" """
		self.mp.x, self.mp.y = self.canvas2World( event.x, event.y)
		pass



	def buttonDragging(self, event):
		""" """
		self.canvas.delete("all")
		self.updateCoordinates(event)
		if self.mp.magneticPoint!=None:
			if getattr(self.mp.magneticPoint, 'thisis', None)=='point':
				self.mp.magneticPoint.x, self.mp.magneticPoint.y=self.mp.x, self.mp.y
				#self.calculator.evaluate()
				for i in range(10):
					for md in self.modules:
						md.evaluate()
				self.drawAll(self.canvas)
	# 

	def buttonPressed(self, event):
		""" """
		self.updateCoordinates(event)
		self.mp.bpX, self.mp.bpY = self.mp.x, self.mp.y
		x,y = self.world2Canvas(self.mp.x, self.mp.y)
		if self.mainPane.inside(x,y):
			for pt in self.points:
				if isNear(pt.x, pt.y, self.mp.x, self.mp.y, 10/self.zoom):
					self.mp.magneticPoint = pt
					break
			pass

	

	def buttonReleased(self, event):
		""" """
		self.updateCoordinates(event)
		if isNear(self.mp.x,self.mp.y,self.mp.bpX,self.mp.bpY,5/self.zoom):## has clicked
			##if mouse cursor is on a point
			##if mouse cousor is on a line
			##if mouse corsor is on a circle
			##which object hass majority
			pass
		else:## finishing drag
			##if self.mp.magenticPoint
			#	if magneticPoint!=None:
			#		self.calculator.evaluate()
			#		self.drawAll(self.canvas)
			#		self.mp.magneticPoint=None
			#else:## 空ドラッグ
			#	図全体を平行移動する。		
			pass

	def wheelTurned(self, event):
		""" """
		pass

	def keyPressed(self, event):
		"""
		keyPressed event"""
		if event.keysym=="Up":
			self.cy -= 10
			self.drawAll(self.canvas)		
			pass
		elif event.keysym=="Down":
			self.cy += 10
			self.drawAll(self.canvas)		
			pass
		elif event.keysym=="Right":
			self.cx += 10
			self.drawAll(self.canvas)		
			pass
		elif event.keysym=="Left":
			self.cx -= 10
			self.drawAll(self.canvas)	
			pass
		pass

	def initilizeMenuItems(self):
		self.menuOn=menuItem("images\\MenuOn.png", 0, 0)
		self.menuOff=menuItem("images\\MenuOff.png", 0, 0)
		self.menuAddPoint=menuItem("images\\AddPoint.png", 0, 1)

	def drawMenuOnIcon(self, canvas):
		self.menuOn.showIcon(canvas)

	def drawAllMenu(self, canvas):
		for icon in [self.menuOff, self.menuAddPoint]:
			icon.showIcon(canvas)