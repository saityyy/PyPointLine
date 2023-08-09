import cv2

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
		while True:
			texts=datalist[line].split(',')
			# clear app.logs and destroy all objects on app.
			app.logs.clear()
			# clear 
			app.nextID=0
			# create a new objest on app (atama pon pon)
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

					writer.Flush();
					for (int i = 0; i < LogLength; i++)
					{
						Log l = logs[i];
						//Debug.Log(""+ l.ObjectType);
						if (l.Active == false)
						{
							;
						}
						else if (l.ObjectType == "Circle")
						{
						}
						else if (l.ObjectType == "Line")
						{
							int j1 = -1, j2 = -1;
							for (int j = 0; j < AppMgr.pts.Length; j++)
							{
								if (AppMgr.pts[j].Id == l.Object1Id)
									j1 = j;
								if (AppMgr.pts[j].Id == l.Object2Id)
									j2 = j;
							}
							writer.Flush();
						}
						else if (l.ObjectType == "Point")
						{
							int id = l.Id;
							//FindPointFromId();
							Point pt = null;
							for (int k = 0; k < AppMgr.pts.Length; k++)
							{
								if (AppMgr.pts[k].Id == id)
								{
									pt = AppMgr.pts[k];
								}
							}
							writer.WriteLine("\\draw[fill=black](" + pt.Vec.x + "," + pt.Vec.y + ") circle  (1.5pt);");
							if (pt.PTobject != null)							// 文字を添えるかどうか
							{
								if (pt.ShowPointName)
								{// 文字を表示するかどうかのフラグ。
									Vector3 textPos = pt.PTobject.transform.position;
									writer.WriteLine("\\draw[fill=black](" + textPos.x + "," + textPos.y + ") node  {" + pt.PointName + "};");
								}
							}
							writer.Flush();
						}
					}
					writer.WriteLine("\\end{tikzpicture}");
					writer.WriteLine("\\end{document}");
					writer.Flush();
					writer.Close();
				}
		pass
	
	def saveImageFile(self, app, filePath):
		pass

	def openImageFile(self, app, filePath):
		pass
