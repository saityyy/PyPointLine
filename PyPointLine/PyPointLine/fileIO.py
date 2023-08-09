import cv2
from object import point, line, circle, angle, locus

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
		line=0
		app.nextID=0
		# clear app.logs and destroy all objects on app.
		app.logs.clear()
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
				newLine.
			lg = app.GetLogFromString(texts)
			line+=1
			if line>=len(datalist):
				f.close()
				return
		pass

	def saveTxtFile(self, app, filePath):
		f = open(filePath, 'w')
		for obj in app.logs:
			f.write("%s\n"%(obj.toString()))
		f.close()
	
	def saveTexFile(self, app, filePath):
		f = open(filePath, 'w')
		f.write("\\documentclass[10pt,dvipdfmx]{article}");
		f.write("\\usepackage{pgf,tikz}");
		f.write("\\usepackage{mathrsfs}");
		f.write("\\pagestyle{empty}");
		f.write("\\begin{document}");
		f.write("\\begin{tikzpicture}[line cap=round,line join=round,x=0.5cm,y=0.5cm]");
		f.write("\\clip(" + app.left + "," + app.bottom + ") rectangle (" + app.right + "," + app.top + ");");
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
		pass
