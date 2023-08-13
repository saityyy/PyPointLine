
import tkinter as tk
import os
import math 

from tkinter import filedialog
from utils import mousePosition, isNear, isIn
from pane import pane
from menuitem import *
from object import point, line, circle, angle, locus
from module import *
from preference import preference
from fileIO import fileIO

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
		self.nextID=0
		self.pointName='A'
		self.lineName='a'
		self.pointRadius=5# global radius of a point in canvas
		self.lineWidth=3# global width of a line in canvas
		self.cx=500
		self.cy=450
		self.pointNameCenterX=500
		self.pointNameCenterY=450
		self.logs=[]
		self.zoom=100
		self.clickedPoint=None
		self.clickedLine=None
		self.clickedCircle=None
		
		self.dispMenu=False
		self.onMode=None
		self.dispPreference=False
		self.preferenceObject=None
		self.logLineFeedDragging=False
		self.logLineFeedDraggingWidth=0
		self.logLineFeedStart=0## negative OK
		self.logLineFeedMin=0
		self.logLineFeedMax=0
		self.headerText=""
		self.fileIO=fileIO(self)

		self.initilizeMenuItems()

		self.showIsom=True
		self.isomColors=["aquamarine4","chartreuse4","chocolate4","darkorchid3","indianred3"]
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
		return self.cx+self.zoom * x, self.cy-self.zoom * y

	def canvas2World(self, x,y):
		return (-self.cx+ x) / self.zoom , -(-self.cy+ y)/self.zoom

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
	@property
	def left(self):
		return -self.cx/self.zoom
	@property
	def right(self):
		# cx+right*zoom=900
		return (900.0-self.cx)/self.zoom
	@property
	def top(self):
		return self.cy/self.zoom
	@property
	def bottom(self):
		return -(900.0-self.cy)/self.zoom

	def findObjectByTag(self, tagstr):
		answer=[obj for obj in self.logs if obj.tag==tagstr]
		if len(answer):
			return answer[0]
		return None

	def getNextID(self):
		ids=[int(obj.tag[4:]) for obj in self.logs]
		self.nextID=max(ids)+1
		pass




	def drawAll(self):
		""" """
		self.mainCanvas.delete("all")
		self.headerCanvas.delete("all")
		self.prefCanvas.delete("all")
		self.logLineFeed=self.logLineFeedStart+self.logLineFeedDraggingWidth
		self.showLogs()
		if self.dispMenu==False:
			self.drawMenuOnIcon()
			self.headerCanvas.create_text(125 ,50, text=self.headerText, fill='black', anchor="w", font=("", 54))
			self.drawAllObjects()
			pass
		else: # dispMenu==True:
			self.drawAllMenu()
			pass


	def showLogs(self):
		if self.dispPreference==False:
			for obj in self.logs:
				obj.drawLog(self)
	def showPreference(self):
		if self.dispPreference:
			self.preferenceObject.pref.restorePreference()
			self.preferenceObject.pref.showPreference()
			pass

	def drawAllObjects(self):

		## draw angles
		for ag in self.angles:
			ag.drawObject(self)

		## draw lines
		if self.showIsom:
			count=0
			for obj in [obj for obj in self.lines if obj.isomParent==obj]:
				obj.isomColor=self.isomColors[count]
				count+=1
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
		self.mp.x, self.mp.y = self.canvas2World( event.x, event.y)
		self.mp.widget=event.widget
		pass



	def buttonDragging(self, event):
		""" """
		#self.mainCanvas.delete("all")
		self.updateCoordinates(event)
		if self.mp.magneticPoint!=None:
			if getattr(self.mp.magneticPoint, 'thisis', None)=='point':
				self.mp.magneticPoint.x, self.mp.magneticPoint.y=self.mp.x, self.mp.y
				self.calculatorEvaluate()
		elif self.logLineFeedDragging:
			self.logLineFeedDraggingWidth=(-self.mp.y+self.mp.bpY)*self.zoom
			##print("%f"%(self.logLineFeedDraggingWidth))
			self.drawAll()

	# 

	def calculatorEvaluate(self, repeat=10):
		for i in range(repeat):
			for md in self.modules+self.lines:
				md.evaluate()
		self.drawAll()


	def buttonPressed(self, event):
		""" """
		self.updateCoordinates(event)
		if self.mp.widget==self.mainCanvas:
			self.mp.bpX, self.mp.bpY = self.mp.x, self.mp.y
			self.mp.magneticPoint = None
			for pt in self.points:
				if isNear(pt.x, pt.y, self.mp.x, self.mp.y, 10/self.zoom):
					self.mp.magneticPoint = pt
					break
			pass
		elif self.mp.widget==self.headerCanvas:
			self.mp.bpX, self.mp.bpY = self.mp.x, self.mp.y
			pass
		elif self.mp.widget==self.prefCanvas:
			self.mp.bpX, self.mp.bpY = self.mp.x, self.mp.y
			self.logLineFeedDragging=True
			self.logLineFeedDraggingWidth=0


	def mouseOnPoint(self):
		for pt in self.points:
			if isNear(pt.x, pt.y, self.mp.x, self.mp.y, 10/self.zoom):
				return pt
		return None

	def mouseOnLine(self):
		for ln in self.lines:
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
			mag=dist(cc.point1.x, cc.point1.y, self.mp.x, self.mp.y)
			if abs(mag-cc.radius)<10/self.zoom:
				return cc

		return None

	def buttonReleased(self, event):
		""" """
		self.updateCoordinates(event)
		self.mp.magneticPoint=None
		self.calculatorEvaluate(repeat=50)
		if isNear(self.mp.x,self.mp.y,self.mp.bpX,self.mp.bpY,5/self.zoom):## has clicked
			self.mp.bpX,self.mp.bpY=0,0
			self.buttonClicked(event)
		else:## finishing drag
			if self.logLineFeedDragging:
				self.logLineFeedStart+=self.logLineFeedDraggingWidth
				self.logLineFeedDraggingWidth=0
				lenLogs=len(self.logs)
				## 1000=window's height
				## 100=logbox's height
				if lenLogs<=1000/100:
					self.logLineFeedStart=0
				else:
					if self.logLineFeedStart<1000-lenLogs*100:
						self.logLineFeedStart=1000-lenLogs*100
					elif self.logLineFeedStart>0:
						self.logLineFeedStart=0
				self.drawAll()
			##if self.mp.magenticPoint
			#	if magneticPoint!=None:
			#		self.drawAll(self.mainCanvas)
			#		self.mp.magneticPoint=None
			#else:## 空ドラッグ
			#	図全体を平行移動する。		
			self.calculatorEvaluate()
			pass

	def buttonClicked(self, event):
		#if self.mp.widget==self.headerCanvas:
		#	print("headerCanvas")
		#elif self.mp.widget==self.mainCanvas:
		#	print("mainCanvas")
		if self.dispMenu==False:
			if self.mp.widget==self.headerCanvas:
				if isIn(self.mp.canvasX, self.mp.canvasY, 0, 0, 100, 100):
					self.dispMenu=True
					self.onMode=None
					self.headerText=""
					self.drawAll()
			elif self.mp.widget==self.mainCanvas:
				self.clickedPoint = self.mouseOnPoint()
				self.clickedLine = self.mouseOnLine()
				self.clickedCircle = self.mouseOnCircle()
				if self.onMode==None:
					self.onMode=self.menuAddPoint
				self.onMode.phaseActions(self)
				pass
			elif self.mp.widget==self.prefCanvas:
				if self.dispPreference==False:
					y=self.mp.canvasY
					y=int(math.floor((y-self.logLineFeedStart)/100))
					if y>=len(self.logs):
						return
					self.preferenceObject=self.logs[y]
					self.dispPreference=True
					self.prefCanvas.delete("all")
					self.showPreference()
		else:# elif self.dispMenu==True:
			if self.mp.widget==self.headerCanvas and isIn(self.mp.canvasX, self.mp.canvasY, 0, 0, 100, 100):
				self.dispMenu=False
				self.onMode=self.menuAddPoint
				self.headerText=""
				self.drawAll()
			else:
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
		x=0
		y=0
		self.menuAddPoint=addPointItem("images\\AddPoint.png", x, y)
		x+=1
		self.menuMidPoint=midPointItem("images\\MidPoint.png", x, y)
		x+=1
		self.menuAddLine=addLineItem("images\\AddLine.png", x, y)
		x+=1
		self.menuAddCircle=addCircleItem("images\\AddCircle.png", x, y)
		x+=1
		self.menuAddAngle=addAngleItem("images\\Angle.png", x, y)
		x+=1
		#####
		y+=1
		x=0
		self.menuP2P=menuP2PItem("images\\P2P.png", x, y)
		x+=1
		self.menuP2L=menuP2LItem("images\\P2L.png", x, y)
		x+=1
		self.menuP2C=menuP2CItem("images\\P2C.png", x, y)
		x+=1
		self.menuTangentL2C=menuL2CItem("images\\TangentL2C.png", x, y)
		x+=1
		self.menuTangentC2C=menuC2CItem("images\\TangentC2C.png", x, y)
		#####
		y+=1
		x=0
		self.menuIsom=menuIsomItem("images\\Isom.png", x, y)
		x+=1
		self.menuPara=menuParaItem("images\\Para.png", x, y)
		x+=1
		self.menuPerp=menuPerpItem("images\\Perp.png", x, y)
		x+=1
		self.menuHori=menuHoriItem("images\\Hori.png", x, y)
		#####
		y+=1
		x=0
		self.menuFixPoint=menuItem("images\\FixPoint.png", x, y)
		x+=1
		self.menuDeleteAll=menuItem("images\\DeleteAll.png", x, y)
		x+=1
		self.menuOpen=menuOpenItem("images\\Open.png", x, y)
		x+=1
		self.menuSave=menuSaveItem("images\\Save.png", x, y)
		x+=1
		self.menuQuit=menuQuitItem("images\\Quit.png", x, y)
		##self.menuAddLocus=menuItem("images\\AddLocus.png", x, y)
		##self.menuRatioLength=menuRatioLengthItem("images\\RatioLength.png", 1, 2)
		##self.menuBisector=menuBisectorItem("images\\Bisector.png", 5, 2)
		#self.menuUndo=menuItem("images\\Undo.png", 1, y)
		#self.menuRedo=menuItem("images\\Redo.png", 2, y)
		#self.menuDeletePoint=menuItem("images\\DeletePoint.png", 3, y)
		#self.menuDeleteLocus=menuItem("images\\DeleteLocus.png", 4, y)
		#self.menuLogs=menuItem("images\\Logs.png", 0, y)
		#self.menuSave2TeX=menuItem("images\\Save2TeX.png", x, y)
		

	def drawMenuOnIcon(self):
		self.menuOn.showIcon(self.headerCanvas)

	@property
	def allButtonIcons(self):
		return [\
			self.menuAddPoint, self.menuMidPoint,self.menuAddLine,self.menuAddCircle,self.menuAddAngle,
			self.menuP2P,self.menuP2L,self.menuP2C,self.menuTangentL2C,self.menuTangentC2C,
			self.menuIsom,self.menuPara,self.menuPerp,self.menuHori,self.menuHori,
			self.menuFixPoint,self.menuDeleteAll,self.menuOpen,self.menuSave,self.menuQuit
			]
	###self.menuAddLocus,self.menuRatioLength,self.menuBisector,self.menuUndo,self.menuRedo,self.menuDeletePoint,self.menuDeleteLocus,self.menuLogs,self.menuSave2TeX,self.menuSave2TeX,

	def drawAllMenu(self):
		self.menuOff.showIcon(self.headerCanvas)
		for icon in self.allButtonIcons:
			icon.showIcon(self.mainCanvas)

	def findPointByName(self, name:str):
		for obj in self.points:
			if obj.name==name:
				return obj
		return None

	def openFile(self):
		fTyp = [("", "*"),("", "txt, TXT"),("", "png,PNG")]
		iDir = os.path.abspath(os.path.dirname(__file__))
		filePath = tk.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
		print(filePath)
		self.fileIO.openFile(self, filePath)
		pass
	def saveFile(self):
		fTyp = [("text file", ".txt"),("image file", ".ps"),("TeX file", ".tex")]
		iDir = os.path.abspath(os.path.dirname(__file__))
		filePath = filedialog.asksaveasfilename(filetypes=fTyp, initialdir=iDir, defaultextension = "txt", initialfile="untitled.txt")
		print(filePath)
		self.fileIO.saveFile(self, filePath)
		pass
	def quitApp(self):
		self.root.destroy()
		#sys.exit(0)
		pass