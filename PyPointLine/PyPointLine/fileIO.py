#import cv2
from object import point, line, circle, xxxxx
from module import *

class fileIO:
	def __init__(self, app):
		self.app=app
		pass
	def openFile(self, app, filePath):
		ext=filePath[-3:]
		if ext=="txt" or ext=="TXT":
			self.openTxtFile(app, filePath)
		elif ext=="png" or ext=="PNG":
			self.openImageFile(app, filePath)
		pass
	def saveFile(self, app, filePath):
		ext=filePath[-3:]
		if ext=="txt" or ext=="TXT":
			self.saveTxtFile(app, filePath)
		if ext=="tex" or ext=="TEX":
			self.saveTexFile(app, filePath)
		elif ext=="png" or ext=="PNG":
			self.saveImageFile(app, filePath)
		pass

	def openTxtFile(self, app, filePath):
		f = open(filePath, 'r')
		datalist = f.readlines()
		app.nextID=0
		# clear app.logs and destroy all objects on app.
		app.logs.clear()
		newXXXXX=xxxxx(app)
		app.logs.append(newXXXXX)
		for data in datalist:
			texts=data.split(',')
			if len(texts)==0:
				continue
			dic={}
			for text in texts:
				items=text.split('=')
				dic[items[0]]=items[1]
			if not "tag" in dic.keys():
				continue
			if dic['type']=='point':
				x=float(dic['x'])
				y=float(dic['y'])
				newPoint=point(app, x, y)
				newPoint.tag=dic['tag']
				newPoint.name=dic['name']
				newPoint.fixed=bool(int(dic['fixed']))
				if newPoint.fixed:
					newPoint.fixedX=x
					newPoint.fixedY=y
				newPoint.showName=bool(int(dic['showName']))
				newPoint.active=bool(int(dic['active']))
				app.logs.append(newPoint)
			elif dic['type']=='line':
				point1=app.findObjectByTag(dic['point1'])
				point2=app.findObjectByTag(dic['point2'])
				if point1==None or point2==None:
					continue
				newLine=line(app, point1, point2)
				newLine.tag=dic['tag']
				newLine.name=dic['name']
				newLine.showLength=bool(int(dic['showLength']))
				newLine.showName=bool(int(dic['showName']))
				newLine.fixedLength=bool(int(dic['fixedLength']))
				newLine.active=bool(int(dic['active']))
				app.logs.append(newLine)
			elif dic['type']=='circle':
				point1=app.findObjectByTag(dic['point1'])
				radius=float(dic['radius'])
				if point==None:
					continue
				newCircle=circle(app, point1, radius)
				newCircle.tag=dic['tag']
				newCircle.name=dic['name']
				newCircle.fixedRadius=bool(int(dic['fixedRadius']))
				newCircle.active=bool(int(dic['active']))
				app.logs.append(newCircle)
			elif dic['type']=='module':
				if dic['moduletype']=='midpoint':
					point1=app.findObjectByTag(dic['p1'])
					point2=app.findObjectByTag(dic['p2'])
					point3=app.findObjectByTag(dic['p3'])
					if point1==None or point2==None or point3==None:
						continue
					newModule=midpoint(app, point1, point2, point3)
					newModule.ratio1=int(dic['ratio1'])
					newModule.ratio2=int(dic['ratio2'])
					newModule.para1=float(dic['para1'])
					newModule.para2=float(dic['para2'])
					newModule.para3=float(dic['para3'])
					app.logs.append(newModule)
				elif dic['moduletype']=='point2point':
					point1=app.findObjectByTag(dic['p1'])
					point2=app.findObjectByTag(dic['p2'])
					if point1==None or point2==None:
						continue
					newModule=point2point(app, point1, point2)
					newModule.para1=float(dic['para1'])
					newModule.para2=float(dic['para2'])
					app.logs.append(newModule)
				elif dic['moduletype']=='point2line':
					point1=app.findObjectByTag(dic['p1'])
					line1=app.findObjectByTag(dic['l1'])
					newModule=point2line(app, point1, line1)
					newModule.onlyOnSegment=bool(int(dic['onlyOnSegment']))
					newModule.para1=float(dic['para1'])
					app.logs.append(newModule)
				elif dic['moduletype']=='point2circle':
					point1=app.findObjectByTag(dic['p1'])
					circle1=app.findObjectByTag(dic['c1'])
					newModule=point2circle(app, point1, circle1)
					newModule.para1=float(dic['para1'])
					app.logs.append(newModule)
				elif dic['moduletype']=='line2circle':
					line1=app.findObjectByTag(dic['ln'])
					circle1=app.findObjectByTag(dic['cc'])
					newModule=line2circle(app, line1, circle1)
					newModule.para1=float(dic['para1'])
					app.logs.append(newModule)
				elif dic['moduletype']=='circle2circle':
					circle1=app.findObjectByTag(dic['cc1'])
					circle2=app.findObjectByTag(dic['cc2'])
					newModule=circle2circle(app, circle1, circle2)
					newModule.para1=float(dic['para1'])
					app.logs.append(newModule)
				elif dic['moduletype']=='isometry':
					line1=app.findObjectByTag(dic['ln1'])
					line2=app.findObjectByTag(dic['ln2'])
					newModule=isometry(app, line1, line2)
					newModule.ratio1=int(dic['ratio1'])
					newModule.ratio2=int(dic['ratio2'])
					newModule.fixedRatio=bool(int(dic['fixedRatio']))
					newModule.para1=float(dic['para1'])
					app.logs.append(newModule)
				elif dic['moduletype']=='parallel':
					line1=app.findObjectByTag(dic['line1'])
					line2=app.findObjectByTag(dic['line2'])
					newModule=parallel(app, line1, line2)
					newModule.para1=float(dic['para1'])
					app.logs.append(newModule)
				elif dic['moduletype']=='perpendicular':
					line1=app.findObjectByTag(dic['line1'])
					line2=app.findObjectByTag(dic['line2'])
					newModule=perpendicular(app, line1, line2)
					newModule.para1=float(dic['para1'])
					app.logs.append(newModule)
				elif dic['moduletype']=='horizontal':
					line1=app.findObjectByTag(dic['line1'])
					newModule=horizontal(app, line1)
					newModule.para1=float(dic['para1'])
					app.logs.append(newModule)
				pass
		## app.nextID
		app.getNextID()
		pass

	def saveTxtFile(self, app, filePath):
		f = open(filePath, 'w')
		for obj in app.logs:
			f.write("%s\n"%(obj.toString()))
		f.close()
	
	def saveTexFile(self, app, filePath):
		f = open(filePath, 'w')
		f.write("\\documentclass[10pt,dvipdfmx]{article}\n")
		f.write("\\usepackage{pgf,tikz}\n")
		f.write("\\usepackage{mathrsfs}\n")
		f.write("\\pagestyle{empty}\n")
		f.write("\\begin{document}\n")
		f.write("\\begin{tikzpicture}[line cap=round,line join=round,x=1.0cm,y=1.0cm]\n")
		f.write("\\clip(%f, %f) rectangle (%f, %f);\n"%(app.left, app.bottom, app.right, app.top))
		for obj in app.logs:
			if obj.thisis!="module":
				f.write("%s\n"%(obj.toTeXString()))
		f.write("\\end{tikzpicture}");
		f.write("\\end{document}");
		f.close()
		pass
	
	def saveImageFile(self, app, filePath):
		app.mainCanvas.postscript(file=filePath, colormode='color')
		pass

	def openImageFile(self, app, filePath):
		#im0 = cv2.imread(self.filename)
		#width, height, x = im0.shape
		##


		##
		pass
