
import tkinter as tk
import os
import math 

from utils import mousePosition, isNear, isIn
from pane import pane
from menuitem import *
from object import point, line, circle, angle, locus
from module import *
from preference import preference


class application:
	"""
	"""
	def __init__(self, root):
		""" """
		self.root = root
		self.headerCanvas=tk.Canvas(root, width=900, height=100)
		self.headerCanvas.place(x=0, y=0)
		self.headerPane=pane(self, 0,0,900,100)
		self.mainCanvas = tk.Canvas(root, width=900, height=900)
		self.mainCanvas.place(x=0, y=100)
		self.mainPane=pane(self,0,100,900,900)
		self.prefCanvas = tk.Canvas(root, width=300, height=1000)
		self.prefCanvas.place(x=900, y=0)
		self.prefPane=pane(self,900,0,300,1000)
		self.mp=mousePosition()
		self.pref=preference(self)
		self.nextID=0
		self.pointName='A'
		self.lineName='a'
		self.pointRadius=5# global radius of a point in canvas
		self.lineWidth=3# global width of a line in canvas
		self.cx=500
		self.cy=500
		self.logs=[]
		self.zoom=100
		self.clickedPoint=None
		self.clickedLine=None
		self.clickedCircle=None
		
		self.dispMenu=False
		self.onMode=None
		self.dispPreference=False
		self.LoglineFeed=0
		self.headerText=""
		##self.file=fileIO(self)

		self.initilizeMenuItems()


		#point0=point(0,0)
		#self.points.append(point0)
		#point1=point(1,1)
		#self.points.append(point1)
		#point2=point(1,0)
		#self.points.append(point2)
		
		#angle0=angle(point0, point1, point2)
		#self.angles.append(angle0)

		#point3=point(-1,0)
		#self.points.append(point3)

		#line0=line(point0, point1)
		#self.lines.append(line0)

		
		#self.circles.append(circle(point0, point1))
		
		#self.circles.append(circle(point2, point3))


		#module20=point2point(point0,point1)
		#self.modules.append(module20)

		#module21=point2line(point2,line0)
		#self.modules.append(module21)

		#module31=point2circle(point3, circle0)
		#self.modules.append(module31)

		#module41=line2circle(line0, circle0)
		#self.modules.append(module41)
		
		#module51=circle2circle(self.circles[0], self.circles[1])
		#self.modules.append(module51)

		self.drawAll()
		pass


	def world2Canvas(self, x,y):
		return self.cx+self.zoom * x, self.cy+self.zoom * y

	def canvas2World(self, x,y):
		return (-self.cx+ x) / self.zoom , (-self.cy+ y)/self.zoom

	@property
	def points(self):
		return [obj for obj in self.logs if obj.thisis=="point"]

	@property
	def lines(self):
		return [obj for obj in self.logs if obj.thisis=="line"]

	@property
	def circles(self):
		return [obj for obj in self.logs if obj.thisis=="circle"]

	@property
	def modules(self):
		return [obj for obj in self.logs if obj.thisis=="module"]

	@property
	def angles(self):
		return [obj for obj in self.logs if obj.thisis=="angle"]

	def drawAll(self):
		""" """
		self.mainCanvas.delete("all")
		self.headerCanvas.delete("all")
		self.prefCanvas.delete("all")
		self.LoglineFeed=0
		if self.dispMenu==False:
			self.drawMenuOnIcon()
			self.headerCanvas.create_text(125 ,50, text=self.headerText, fill='black', anchor="w", font=("", 54))
			self.drawAllObjects()
			#self.drawAllLogs()
			if self.dispPreference==True:
				#self.drawPreference()
				pass
			pass
		else: # dispMenu==True:
			self.drawAllMenu()
			pass


	def drawAllObjects(self):
		if self.dispPreference:
			## draw preference
			pass
		else:
			## draw logs
			for obj in self.logs:
				obj.drawLog(self)

		## draw angles
		for ag in self.angles:
			ag.drawObject(self)

		## draw lines
		for ln in self.lines:
			ln.drawObject(self)
		
		## draw circles
		for cn in self.circles:
			cn.drawObject(self)

		## draw points
		for pt in self.points:
			pt.drawObject(self)


		## draw locus


	def updateCoordinates(self, event):
		""" """
		self.mp.canvasX, self.mp.canvasY = event.x, event.y
		if self.mp.magneticPoint!=None:
			self.mp.x, self.mp.y = self.canvas2World( event.x, event.y)
		elif self.headerPane.isIn(self.mp.canvasX, self.mp.canvasY):
			self.mp.x, self.mp.y = self.mp.canvasX, self.mp.canvasY
		elif self.mainPane.isIn(self.mp.canvasX, self.mp.canvasY):
			self.mp.x, self.mp.y = self.canvas2World( event.x, event.y)
		elif self.prefPane.isIn(self.mp.canvasX, self.mp.canvasY):
			self.mp.x, self.mp.y = self.mp.canvasX-900, self.mp.canvasY
		pass



	def buttonDragging(self, event):
		""" """
		#self.mainCanvas.delete("all")
		self.updateCoordinates(event)
		if self.mp.magneticPoint!=None:
			if getattr(self.mp.magneticPoint, 'thisis', None)=='point':
				self.mp.magneticPoint.x, self.mp.magneticPoint.y=self.mp.x, self.mp.y
				self.calculatorEvaluate()
	# 

	def calculatorEvaluate(self, repeat=10):
		for i in range(repeat):
			for md in self.modules:
				md.evaluate()
		self.drawAll()


	def buttonPressed(self, event):
		""" """
		self.updateCoordinates(event)
		self.mp.bpX, self.mp.bpY = self.mp.x, self.mp.y
		x,y = self.world2Canvas(self.mp.x, self.mp.y)
		if self.mainPane.isIn(x,y):
			for pt in self.points:
				if isNear(pt.x, pt.y, self.mp.x, self.mp.y, 10/self.zoom):
					self.mp.magneticPoint = pt
					break
			pass

	def mouseOnPoint(self):
		for pt in self.points:
			if pt.thisis=='point':
				if isNear(pt.x, pt.y, self.mp.x, self.mp.y, 10/self.zoom):
					return pt
		return None

	def mouseOnLine(self):
		for ln in self.lines:
			if ln.thisis=='line':
				ax,ay=self.mp.x, self.mp.y
				bx,by=ln.point1.x, ln.point1.y
				cx,cy=ln.point2.x, ln.point2.y
				tn=(ax-bx)*(cx-bx)+(ay-by)*(cy-by)
				td=(cx-bx)*(cx-bx)+(cy-by)*(cy-by)
				if td==0:
					continue
				tt=tn/td
				dx, dy=tt*(cx-bx)+(bx-ax), tt*(cy-by)+(by-ay)
				if magnitude(dx, dy)<10/self.zoom:
					return ln
		return None

	def mouseOnCircle(self):
		for cc in self.circles:
			if cc.thisis=='circle':
				mag=dist(cc.point.x, cc.point.y, self.mp.x, self.mp.y)
				if abs(mag-cc.radius)<10/self.zoom:
					return cc

		return None

	def buttonReleased(self, event):
		""" """
		self.updateCoordinates(event)
		if isNear(self.mp.x,self.mp.y,self.mp.bpX,self.mp.bpY,5/self.zoom):## has clicked
			if self.dispMenu==False and isIn(self.mp.canvasX, self.mp.canvasY, 0, 0, 100, 100):
				self.dispMenu=True
				self.onMode=None
				self.headerText=""
				self.mp.magneticPoint=None
				self.drawAll()
			elif self.dispMenu==True and isIn(self.mp.canvasX, self.mp.canvasY, 0, 0, 100, 100):
				self.dispMenu=False
				self.onMode=self.menuAddPoint
				self.headerText=""
				self.mp.magneticPoint=None
				self.drawAll()
			elif self.dispMenu==False:
				self.clickedPoint = self.mouseOnPoint()
				self.clickedLine = self.mouseOnLine()
				self.clickedCircle = self.mouseOnCircle()
				if self.onMode==None:
					self.onMode=self.menuAddPoint
				self.onMode.phaseActions(self)
				pass
			elif self.dispMenu==True:
				self.onMode=None
				self.headerText=""
				for icon in self.allButtonIcons:
					if isIn(self.mp.canvasX, self.mp.canvasY, icon.left, icon.top, icon.width, icon.height):
						self.onMode=icon
						self.onMode.onActions(self)
						self.onModePhase=0
						self.headerText=icon.headerText[self.onModePhase]
						self.dispMenu=False
						self.drawAll()
						break
				else:
					self.onMode=self.menuAddPoint
			pass
		else:## finishing drag
			##if self.mp.magenticPoint
			#	if magneticPoint!=None:
			#		self.drawAll(self.mainCanvas)
			#		self.mp.magneticPoint=None
			#else:## 空ドラッグ
			#	図全体を平行移動する。		
			self.mp.magneticPoint=None
			self.calculatorEvaluate()
			pass

	def wheelTurned(self, event):
		""" """
		self.updateCoordinates(event)
		if event.delta>0:
			ratio:float=41/40
		elif event.delta<0:
			ratio:float=39/40
		else:
			return
		self.cx=(self.cx-self.mp.canvasX)*ratio+self.mp.canvasX
		self.cy=(self.cy-self.mp.canvasY)*ratio+self.mp.canvasY
		self.zoom = self.zoom * ratio
		##print("%f->%f"%(event.delta, self.zoom))
		self.drawAll()
		pass

	def keyPressed(self, event):
		"""
		keyPressed event"""
		if event.keysym=="Up":
			self.cy -= 10
			self.drawAll()		
			pass
		elif event.keysym=="Down":
			self.cy += 10
			self.drawAll()		
			pass
		elif event.keysym=="Right":
			self.cx += 10
			self.drawAll()		
			pass
		elif event.keysym=="Left":
			self.cx -= 10
			self.drawAll()	
			pass
		pass

	def initilizeMenuItems(self):
		self.menuOn=menuItem("images\\MenuOn.png", 0, 0)
		self.menuOff=menuItem("images\\MenuOff.png", 0, 0)
		#####
		self.menuAddPoint=addPointItem("images\\AddPoint.png", 0, 0)
		self.menuMidPoint=midPointItem("images\\MidPoint.png", 1, 0)
		self.menuAddLine=addLineItem("images\\AddLine.png", 2, 0)
		self.menuAddCircle=addCircleItem("images\\AddCircle.png", 3, 0)
		self.menuAddAngle=addAngleItem("images\\Angle.png", 4, 0)
		self.menuAddLocus=menuItem("images\\AddLocus.png",5 , 0)
		#####
		self.menuP2P=menuP2PItem("images\\P2P.png", 0, 1)
		self.menuP2L=menuP2LItem("images\\P2L.png", 1, 1)
		self.menuP2C=menuP2CItem("images\\P2C.png", 2, 1)
		self.menuTangentL2C=menuL2CItem("images\\TangentL2C.png", 3, 1)
		self.menuTangentC2C=menuC2CItem("images\\TangentC2C.png", 4, 1)
		#####
		self.menuIsom=menuIsomItem("images\\Isom.png", 0, 2)
		self.menuRatioLength=menuRatioLengthItem("images\\RatioLength.png", 1, 2)
		self.menuPara=menuParaItem("images\\Para.png", 2, 2)
		self.menuPerp=menuPerpItem("images\\Perp.png", 3, 2)
		self.menuHori=menuHoriItem("images\\Hori.png", 4, 2)
		self.menuBisector=menuBisectorItem("images\\Bisector.png", 5, 2)
		#####
		self.menuFixPoint=menuItem("images\\FixPoint.png", 0, 3)
		self.menuUndo=menuItem("images\\Undo.png", 1, 3)
		self.menuRedo=menuItem("images\\Redo.png", 2, 3)
		self.menuDeletePoint=menuItem("images\\DeletePoint.png", 3, 3)
		self.menuDeleteLocus=menuItem("images\\DeleteLocus.png", 4, 3)
		self.menuDeleteAll=menuItem("images\\DeleteAll.png", 5, 3)
		#####
		self.menuLogs=menuItem("images\\Logs.png", 0, 4)
		self.menuOpen=menuItem("images\\Open.png", 1, 4)
		self.menuSave=menuItem("images\\Save.png", 2, 4)
		self.menuSave2TeX=menuItem("images\\Save2TeX.png", 3, 4)
		self.menuQuit=menuQuitItem("images\\Quit.png", 4, 4)
		

	def drawMenuOnIcon(self):
		self.menuOn.showIcon(self.headerCanvas)

	@property
	def allButtonIcons(self):
		return [\
			self.menuAddPoint, self.menuMidPoint,self.menuAddLine,self.menuAddCircle,self.menuAddLocus,self.menuAddAngle,
			self.menuP2P,self.menuP2L,self.menuP2C,self.menuTangentL2C,self.menuTangentC2C,
			self.menuIsom,self.menuRatioLength,self.menuPara,self.menuPerp,self.menuHori,self.menuHori,self.menuBisector,
			self.menuFixPoint,self.menuUndo,self.menuRedo,self.menuDeletePoint,self.menuDeleteLocus,self.menuDeleteAll,
			self.menuLogs,self.menuOpen,self.menuSave,self.menuSave2TeX,self.menuSave2TeX,self.menuQuit
			]

	def drawAllMenu(self):
		self.menuOff.showIcon(self.headerCanvas)
		for icon in self.allButtonIcons:
			icon.showIcon(self.mainCanvas)