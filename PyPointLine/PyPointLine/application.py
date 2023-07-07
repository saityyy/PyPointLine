
import tkinter as tk
import os

from utils import mousePosition
from pane import pane
from calculator import calculator
from menuitem import menuItem

class application:
	"""
	"""
	def __init__(self, root):
		""" """
		self.root = root
		self.canvas = tk.Canvas(root, width=1200, height=1000)
		self.canvas.pack()
		self.mp=mousePosition()
		self.canvas.bind("<B1-Motion>", self.buttonDragging)  # 
		self.canvas.bind("<Button-1>", self.buttonPressed)  # 
		self.canvas.bind("<ButtonRelease-1>", self.buttonReleased)  # 
		self.canvas.bind("<Motion>", self.updateCoordinates) # 
		self.nextID=0
		self.pointName='A'
		self.lineName='a'
		self.pointRadius=5# global radius of a point in canvas
		self.lineWidth=3# global width of a line in canvas
		self.cx=0
		self.cy=0
		self.zoom=1.0
		self.dispMenu=False
		self.dispPreference=False

		##self.file=fileIO(self)
		self.calculator=calculator()

		self.headerPane=pane(self, 0,0,1000,50)
		self.mainPane=pane(self,0,50,1000,950)
		self.rightPane=pane(self,1000,0,200,1000)
		self.initilizeMenuItems()
		self.drawAll(self.canvas)
		pass


	def world2Canvas(self, x,y):
		return self.cx+self.zoom * (x -500) + 500, self.cy+self.zoom * (y-500) + 500

	def canvas2World(self, x,y):
		return -self.cx+ (x -500) / self.zoom + 500 , -self.cy+ (y-500)/self.zoom + 500


	def drawAll(self, canvas):
		""" """
		self.canvas.delete("all")
		if self.dispMenu==False:
			self.drawMenuOnIcon(canvas)
			#self.drawAllObjects()
			#self.drawAllLogs()
			if self.dispPreference==True:
				#self.drawProference()
				pass
			pass
		else: # dispMenu==True:
			self.drawAllMenu(canvas)
			pass

	def updateCoordinates(self, event):
		""" """
		self.mp.x, self.mp.y = self.canvas2World( event.x, event.y)
		pass

	def buttonDragging(self, event):
		""" """
		self.canvas.delete("all")
		self.updateCoordinates(event)
		#if self.mp.magneticPoint!=None and getattr(self.mp.magneticND, 'this_is_point', False)==True:
		#	self.mp.magneticND.x=self.mp.x
		#	self.mp.magneticND.y=self.mp.y
		#	for ed in self.mp.magneticND.neighbors:
		#		if getattr(ed, 'this_is_edge', False):
		#			ed.scalingShapeModifier()
		#	self.mp.magneticND.modifyAngle()
		#self.drawAll(self.canvas)
	# 

	def buttonPressed(self, event):
		""" """
		self.updateCoordinates(event)
		self.mp.bpX, self.mp.bpY = self.mp.x, self.mp.y
		#for node in self.kg.nodes:
		#	if node.inUse and isNear(self.mp.x, self.mp.y, node.x, node.y, 10):
		#		self.mp.magneticND=node

	

	def buttonReleased(self, event):
		""" """
		self.updateCoordinates(event)
		#if isNear(self.mp.x,self.mp.y,self.mp.bpX,self.mp.bpY,5):## clicked
		#	for node in self.kg.nodes:
		#		if node.inUse and isNear(self.mp.x, self.mp.y, node.x, node.y, 10):
		#			if getattr(node,'this_is_midjoint', False):
		#				### clicking midJoint -> delete the midJoint
		#				break
		#			else:
		#				### clicking Node -> change crossing
		#				break
		self.mp.magneticND=None
		#self.drawAll(self.canvas)

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
		self.addPoint=menuItem("images\\AddPoint.png", 0, 1)

	def drawMenuOnIcon(self, canvas):
		self.menuOn.showIcon(canvas)

	def drawAllMenu(self, canvas):
		for icon in [self.menuOff, self.addPoint]:
			icon.showIcon(canvas)