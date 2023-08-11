import tkinter as tk


class preference:
	import tkinter as tk

	def __init__(self,application, parent):
		self.label="Preference"
		self.parent=parent
		self.application=application
		self.canvas=application.prefCanvas
		self.thisis="preference"
		self.lineFeedWidth:int=40
		self.width=300#self.canvas.width
		self.panes={}
		self.initPreference()
	def show(self):
		if self.thisis=="preference":
			self.showPreference()
		elif self.thisis=="logs":
			self.showLogs()
		else:
			self.canvas.delete("all")
		pass


	class prefPane:
		def __init__(self, pref, type:str, label:str, radio1:str="", radio2:str="", radio:int=0, value:float=0.0, iValue:int=0, tValue:str="", button1:str="Cancel", button2:str="OK"):
			self.preference=pref
			self.type=type# text, float, radio
			self.label=""
			self.text=label
			self.value=value
			self.iValue=iValue
			self.tValue=tValue
			self.radio1=radio1
			self.radio2=radio2
			self.radio_variable=tk.IntVar(value = radio)
			self.button1=button1
			self.button2=button2
			self.lineFeedWidth=self.preference.lineFeedWidth
			self.entry_text=tk.StringVar(value="")
			self.widget1=None
			self.widget2=None
			self.widget3=None
		def show(self, x, y, app):
			##canvas.delete("all")
			if self.type=="label":
				self.entry_text=tk.StringVar(value="%s"%(self.preference.parent.name))
				self.widget1 = tk.Label(app.root, text=self.text, font=("",18))
				self.widget2 = tk.Entry(app.root, width=8, font=("",18), textvariable=self.entry_text)
				self.widget1.place(x=x, y=y)
				self.widget2.place(x=x+90, y=y)
			elif self.type=="moduleLabel":
				self.widget1 = tk.Label(app.root, text=self.text, font=("",18))
				self.widget1.place(x=x, y=y)
			elif self.type=="radio":
				self.widget1 = tk.Label(app.root, text=self.text, font=("",18))
				self.widget2 = tk.Radiobutton(app.root, text=self.radio1, font=("",18), variable = self.radio_variable, value=0, command = self.radio_click)
				self.widget3 = tk.Radiobutton(app.root, text=self.radio2, font=("",18), variable = self.radio_variable, value=1, command = self.radio_click)
				self.widget1.place(x=x, y=y)
				self.widget2.place(x=x+90, y=y)
				self.widget3.place(x=x+180, y=y)
			elif self.type=="int":
				self.entry_text=tk.StringVar(app.root, value="%d"%(self.iValue))
				self.widget1 = tk.Label(app.root, text=self.text, font=("",18))
				self.widget2 = tk.Entry(app.root, width=10, font=("",18), textvariable=self.entry_text)
				self.widget1.place(x=x, y=y)
				self.widget2.place(x=x+90, y=y)
			elif self.type=="float":
				self.entry_text=tk.StringVar(app.root, value="%0.3f"%(self.value))
				self.widget1 = tk.Label(app.root, text=self.text, font=("",18))
				self.widget2 = tk.Entry(app.root, width=10, font=("",18), textvariable=self.entry_text)
				self.widget1.place(x=x, y=y)
				self.widget2.place(x=x+90, y=y)
			if self.type=="text":
				self.entry_text=tk.StringVar(value=self.tValue)
				self.widget1 = tk.Label(app.root, text=self.text, font=("",18))
				self.widget2 = tk.Entry(app.root, width=8, font=("",18), textvariable=self.entry_text)
				self.widget1.place(x=x, y=y)
				self.widget2.place(x=x+90, y=y)
			elif self.type=="para":
				self.entry_text=tk.StringVar(app.root, value="%0.3f"%(self.value))
				self.widget1 = tk.Label(app.root, text=self.text, font=("",18), background="plum1")
				self.widget2 = tk.Entry(app.root, width=10, font=("",18), textvariable=self.entry_text, background="plum1")
				self.widget1.place(x=x, y=y)
				self.widget2.place(x=x+90, y=y)
			elif self.type=="destroyButton":
				self.widget1=tk.Button(app.root, text="Destroy", background="red", font=("",18), anchor=tk.CENTER, width=8, command=self.click_destroy_btn)
				self.widget1.place(x=x, y=y)
			elif self.type=="buttons":
				self.widget1=tk.Button(app.root, text="OK", background="OliveDrab1", font=("",18), anchor=tk.CENTER, width=8, command=self.click_OK_btn)
				self.widget2=tk.Button(app.root, text="Cancel", background="OliveDrab1", font=("",18), anchor=tk.CENTER, width=8, command=self.click_NG_btn )
				self.widget1.place(x=x, y=y)
				self.widget2.place(x=x+150, y=y)
			pass
		def destroy(self):
			if self.widget1!=None:
				self.widget1.destroy()
			if self.widget2!=None:
				self.widget2.destroy()
			if self.widget3!=None:
				self.widget3.destroy()
		def radio_click(self):
			value = self.radio_variable.get()
			print(f"radio button value is {value}.")
		def entry_click(self):
			value=self.entry_text.get()
			print("entry text is %s"%(value))
		def click_destroy_btn(self):
			app=self.preference.application
			obj=self.preference.parent
			app.dispPreference=False
			self.preference.destroyAllPreference()
			app.logs.remove(obj)
			del obj
			app.showLogs()
			pass
		def click_OK_btn(self):
			pref=self.preference
			parent=pref.parent
			app=pref.application
			if parent.thisis=="point":
				parent.name = pref.panes['label'].entry_text.get()
				parent.showName = pref.panes['name'].radio_variable.get()
				parent.x = float(pref.panes['x'].entry_text.get())
				parent.y = float(pref.panes['y'].entry_text.get())
				parent.fixed = pref.panes['fixed'].radio_variable.get()
			elif parent.thisis=="line":
				parent.name = pref.panes['label'].entry_text.get()
				parent.showName = pref.panes['name'].radio_variable.get()
				newPoint = pref.application.findPointByName(pref.panes['point1'].entry_text.get())
				if newPoint:
					parent.point1 = newPoint
				newPoint = pref.application.findPointByName(pref.panes['point2'].entry_text.get())
				if newPoint:
					parent.point2 = newPoint
				parent.showLength = pref.panes['showLength'].radio_variable.get()
				parent.fixedLength = pref.panes['fixedLength'].radio_variable.get()
			elif parent.thisis=="circle":
				parent.name = pref.panes['label'].entry_text.get()
				parent.showName = pref.panes['name'].radio_variable.get()
				parent.fixedRadius = pref.panes['fixedRadius'].radio_variable.get()
			elif parent.thisis=="module":
				if parent.moduletype=="midpoint":
					r1=int(pref.panes['ratio1'].entry_text.get())
					r2=int(pref.panes['ratio2'].entry_text.get())
					if r1!=0 and r2!=0 and r1!=r2:
						parent.ratio1=r1
						parent.ratio2=r2
					p1=float(pref.panes['para1'].entry_text.get())
					if p1!=0.0 and p1!=1.0:
						parent.para1=p1
					p2=float(pref.panes['para2'].entry_text.get())
					if p2!=0.0 and p2!=1.0:
						parent.para2=p2
					p3=float(pref.panes['para3'].entry_text.get())
					if p3!=0.0 and p3!=1.0:
						parent.para3=p3
				elif parent.moduletype=="point2point":
					p1=float(pref.panes['para1'].entry_text.get())
					if p1!=0.0 and p1!=1.0:
						parent.para1=p1
				elif parent.moduletype=="point2line":
					p1=float(pref.panes['para1'].entry_text.get())
					if p1!=0.0 and p1!=1.0:
						parent.para1=p1
				elif parent.moduletype=="point2circle":
					p1=float(pref.panes['para1'].entry_text.get())
					if p1!=0.0 and p1!=1.0:
						parent.para1=p1
				elif parent.moduletype=="line2circle":
					p1=float(pref.panes['para1'].entry_text.get())
					if p1!=0.0 and p1!=1.0:
						parent.para1=p1
				elif parent.moduletype=="circle2circle":
					p1=float(pref.panes['para1'].entry_text.get())
					if p1!=0.0 and p1!=1.0:
						parent.para1=p1
				elif parent.moduletype=="isometry":
					r1=int(pref.panes['ratio1'].entry_text.get())
					r2=int(pref.panes['ratio2'].entry_text.get())
					if r1!=0 and r2!=0 and r1!=r2:
						parent.ratio1=r1
						parent.ratio2=r2
					p1=float(pref.panes['para1'].entry_text.get())
					if p1!=0.0 and p1!=1.0:
						parent.para1=p1
				elif parent.moduletype=="parallel":
					p1=float(pref.panes['para1'].entry_text.get())
					if p1!=0.0 and p1!=1.0:
						parent.para1=p1
				elif parent.moduletype=="perpendicular":
					p1=float(pref.panes['para1'].entry_text.get())
					if p1!=0.0 and p1!=1.0:
						parent.para1=p1
				elif parent.moduletype=="horizontal":
					p1=float(pref.panes['para1'].entry_text.get())
					if p1!=0.0 and p1!=1.0:
						parent.para1=p1
				pass

			app.dispPreference=False
			self.preference.destroyAllPreference()
			app.showLogs()
			pass
		def click_NG_btn(self):
			app=self.preference.application
			app.dispPreference=False
			self.preference.destroyAllPreference()
			app.showLogs()
			pass

	def initPreference(self):
		if getattr(self.parent, 'thisis', None)=='point':
			self.initPointPreference()
		elif  getattr(self.parent, 'thisis', None)=='line':
			self.initLinePreference()
		elif  getattr(self.parent, 'thisis', None)=='circle':
			self.initCirclePreference()
		elif  getattr(self.parent, 'thisis', None)=='module':
			self.initModulePreference()
		pass

	def initPointPreference(self):
		parent = self.parent
		self.panes={}
		self.panes['label']=self.prefPane(self, "label","Point : ","")
		radio = 1 if parent.showName else 0
		self.panes['name']=self.prefPane(self, "radio","Name: ", radio1="Hide", radio2="Show", radio=1)
		self.panes['x']=self.prefPane(self, "float","X:", value=parent.x)
		self.panes['y']=self.prefPane(self, "float","Y:", value=parent.y)
		radio = 1 if parent.fixed else 0
		self.panes['fixed']=self.prefPane(self, "radio","Fixed:", radio1="Off", radio2="On", radio=0)
		self.panes["destroyButton"]=self.prefPane(self, "destroyButton", "")
		self.panes["OKbutton"]=self.prefPane(self, "buttons", "")
		
		pass

	def initLinePreference(self):
		parent = self.parent
		self.panes={}
		self.panes['label']=self.prefPane(self, "label","Line : ","")
		radio = 1 if parent.showName else 0
		self.panes['name']=self.prefPane(self, "radio","Name: ", radio1="Hide", radio2="Show", radio=0)
		self.panes['point1']=self.prefPane(self, "text","P1:", tValue=parent.point1.name)
		self.panes['point2']=self.prefPane(self, "text","P2:", tValue=parent.point2.name)
		radio = 1 if parent.showLength else 0
		self.panes['showLength']=self.prefPane(self, "radio","Length:", radio1="Hide", radio2="Show", radio=radio)
		radio = 1 if parent.fixedLength else 0
		self.panes['fixedLength']=self.prefPane(self, "radio","Fixed :", radio1="Off", radio2="On", radio=radio)
		self.panes["destroyButton"]=self.prefPane(self, "destroyButton", "")
		self.panes["OKbutton"]=self.prefPane(self, "buttons", "")
		pass

	def initCirclePreference(self):
		parent = self.parent
		self.panes={}
		self.panes['label']=self.prefPane(self, "label","Circle : ","")
		radio = 1 if parent.showName else 0
		self.panes['name']=self.prefPane(self, "radio","Name: ", radio1="Hide", radio2="Show", radio=1)
		radio = 1 if parent.fixedRadius else 0
		self.panes['fixedRadius']=self.prefPane(self, "radio","Fixed :", radio1="Off", radio2="On", radio=radio)
		self.panes["destroyButton"]=self.prefPane(self, "destroyButton", "")
		self.panes["OKbutton"]=self.prefPane(self, "buttons", "")

	def initModulePreference(self):
		parent = self.parent
		self.panes={}
		self.panes['label']=self.prefPane(self, "moduleLabel","Module : %s"%(parent.moduletype),"")
		if parent.moduletype=='midpoint':
			self.panes['ratio1']=self.prefPane(self, "int", "Ratio1=", iValue=parent.ratio1)
			self.panes['ratio2']=self.prefPane(self, "int", "Ratio2=", iValue=parent.ratio2)
			self.panes['para1']=self.prefPane(self, "para", "Para1=", iValue=parent.para1)
			self.panes['para2']=self.prefPane(self, "para", "Para2=", iValue=parent.para2)
			self.panes['para3']=self.prefPane(self, "para", "Para3=", iValue=parent.para3)
		elif parent.moduletype=='point2point':
			self.panes['para1']=self.prefPane(self, "para", "Para1=", iValue=parent.para1)
		elif parent.moduletype=='point2line':
			self.panes['para1']=self.prefPane(self, "para", "Para1=", iValue=parent.para1)
		elif parent.moduletype=='point2circle':
			self.panes['para1']=self.prefPane(self, "para", "Para1=", iValue=parent.para1)
		elif parent.moduletype=='line2circle':
			self.panes['para1']=self.prefPane(self, "para", "Para1=", iValue=parent.para1)
		elif parent.moduletype=='circle2circle':
			self.panes['para1']=self.prefPane(self, "para", "Para1=", iValue=parent.para1)
		elif parent.moduletype=='isometry':
			self.panes['ratio1']=self.prefPane(self, "int", "Ratio1=", iValue=parent.ratio1)
			self.panes['ratio2']=self.prefPane(self, "int", "Ratio2=", iValue=parent.ratio2)
			self.panes['para1']=self.prefPane(self, "para", "Para1=", iValue=parent.para1)
		elif parent.moduletype=='parallel':
			self.panes['para1']=self.prefPane(self, "para", "Para1=", iValue=parent.para1)
		elif parent.moduletype=='perpendicular':
			self.panes['para1']=self.prefPane(self, "para", "Para1=", iValue=parent.para1)
		elif parent.moduletype=='horizontal':
			self.panes['para1']=self.prefPane(self, "para", "Para1=", iValue=parent.para1)
		self.panes["destroyButton"]=self.prefPane(self, "destroyButton", "")
		self.panes["OKbutton"]=self.prefPane(self, "buttons", "")


	def restorePreference(self):
		if getattr(self.parent, 'thisis', None)=='point':
			self.restorePointPreference()
		elif  getattr(self.parent, 'thisis', None)=='line':
			self.restoreLinePreference()
		elif  getattr(self.parent, 'thisis', None)=='circle':
			self.restoreCirclePreference()
		elif  getattr(self.parent, 'thisis', None)=='module':
			self.restoreModulePreference()
		pass

	def restorePointPreference(self):
		parent=self.parent
		self.panes['label'].entry_text.set(parent.name)
		value=1 if parent.showName else 0
		self.panes['name'].radio_variable.set(value)
		self.panes['x'].value=parent.x
		self.panes['y'].value=parent.y
		value=1 if parent.fixed else 0
		self.panes['fixed'].radio_variable.set(value)
		self.application.root.update()
		pass
	def restoreLinePreference(self):
		parent=self.parent
		self.panes['label'].entry_text.set(parent.name)
		value=1 if parent.showName else 0
		self.panes['name'].radio_variable.set(value)
		self.panes['point1'].entry_text.set(parent.point1.name)
		self.panes['point2'].entry_text.set(parent.point2.name)
		value=1 if parent.showLength else 0
		self.panes['showLength'].radio_variable.set(value)
		value=1 if parent.fixedLength else 0
		self.panes['fixedLength'].radio_variable.set(value)
		pass
	def restoreCirclePreference(self):
		parent=self.parent
		self.panes['label'].entry_text.set(parent.name)
		value=1 if parent.showName else 0
		self.panes['name'].radio_variable.set(value)
		value=1 if parent.fixedRadius else 0
		self.panes['fixedRadius'].radio_variable.set(value)
		pass
	def restoreModulePreference(self):
		parent=self.parent
		if parent.moduletype=='midpoint':
			self.panes['ratio1'].iValue=parent.ratio1
			self.panes['ratio2'].iValue=parent.ratio2
			self.panes['para1'].value=parent.para1
			self.panes['para2'].value=parent.para2
			self.panes['para3'].value=parent.para3
		elif parent.moduletype=='point2point':
			self.panes['para1'].value=parent.para1
		elif parent.moduletype=='point2line':
			self.panes['para1'].value=parent.para1
		elif parent.moduletype=='point2circle':
			self.panes['para1'].value=parent.para1
		elif parent.moduletype=='line2circle':
			self.panes['para1'].value=parent.para1
		elif parent.moduletype=='circle2circle':
			self.panes['para1'].value=parent.para1
		elif parent.moduletype=='isometry':
			self.panes['ratio1'].iValue=parent.ratio1
			self.panes['ratio2'].iValue=parent.ratio2
			self.panes['para1'].value=parent.para1
		elif parent.moduletype=='parallel':
			self.panes['para1'].value=parent.para1
		elif parent.moduletype=='perpendicular':
			self.panes['para1'].value=parent.para1
		elif parent.moduletype=='horizontal':
			self.panes['para1'].value=parent.para1
		pass



	def destroyAllPreference(self):
		for pane in self.panes.values():
			pane.destroy()


	def showPreference(self):
		x=910
		y=30
		for pane in self.panes.values():
			pane.show(x, y, self.application)
			y+=45




