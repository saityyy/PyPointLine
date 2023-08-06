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
		self.panes=[]
		self.initPreference()
	def show(self):
		if self.thisis=="preference":
			self.showPreference()
		elif self.thisis=="logs":
			self.showLogs()
		else:
			self.canvas.delete("all")
		pass


	def initPreference(self):
		if getattr(self.parent, 'thisis', None)=='point':
			self.initPointPreference()
		elif  getattr(self.parent, 'thisis', None)=='line':
			self.initLinePreference()
		elif  getattr(self.parent, 'thisis', None)=='circle':
			self.initCirclePreference()
		pass

	class prefPane:
		def __init__(self, pref, type:str, label:str, radio1:str="", radio2:str="", radio:int=0, value:float=0.0, button1:str="Cancel", button2:str="OK"):
			self.preference=pref
			self.type=type# text, float, radio
			self.label=""
			self.text=label
			self.value=value
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
			elif self.type=="radio":
				self.widget1 = tk.Label(text=self.text, font=("",18))
				self.widget2 = tk.Radiobutton(text=self.radio1, font=("",18), variable = self.radio_variable, value=0, command = self.radio_click)
				self.widget3 = tk.Radiobutton(text=self.radio2, font=("",18), variable = self.radio_variable, value=1, command = self.radio_click)
				self.widget1.place(x=x, y=y)
				self.widget2.place(x=x+90, y=y)
				self.widget3.place(x=x+180, y=y)
			elif self.type=="float":
				self.entry_text=tk.StringVar(value="%0.3f"%(self.value))
				self.widget1 = tk.Label(text=self.text, font=("",18))
				self.widget2 = tk.Entry(width=10, font=("",18), textvariable=self.entry_text)
				self.widget1.place(x=x, y=y)
				self.widget2.place(x=x+90, y=y)
			elif self.type=="buttons":
				self.widget1=tk.Button(text="OK", background="green", font=("",20), anchor=tk.CENTER, width=8, height=1, command=self.click_OK_btn)
				self.widget2=tk.Button(text="Cancel", background="green", font=("",20), anchor=tk.CENTER, width=8, height=1, command=self.click_NG_btn )
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
			value = self.radio.get()
			print(f"radio button value is {value}.")
		def entry_click(self):
			value=self.entry_text.get()
			print("entry text is %s"%(value))
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

	def initPointPreference(self):
		parent = self.parent
		self.panes={}
		self.panes['label']=self.prefPane(self, "label","Point : ","")
		radio = 1 if parent.showName else 0
		self.panes['name']=self.prefPane(self, "radio","Name: ", radio1="Show", radio2="Hide", radio=radio)
		self.panes['x']=self.prefPane(self, "float","X:", value=parent.x)
		self.panes['y']=self.prefPane(self, "float","Y:", value=parent.y)
		radio = 1 if parent.fixed else 0
		self.panes['fixed']=self.prefPane(self, "radio","Fixed:", radio1="On", radio2="Off", radio=radio)
		self.panes["OKbutton"]=self.prefPane(self, "buttons", "")
		
		pass

	def restorePointPreference(self):
		parent=self.parent
		self.panes['label'].entry_text.set(parent.name)
		value=1 if parent.showName else 0
		self.panes['name'].radio_variable.set(value)
		self.panes['x'].entry_text.set("%0.3f"%(parent.x))
		self.panes['y'].entry_text.set("%0.3f"%(parent.y))
		value=1 if parent.fixed else 0
		self.panes['fixed'].radio_variable.set(value)

	def destroyAllPreference(self):
		for pane in self.panes.values():
			pane.destroy()


	def showPreference(self):
		x=910
		y=30
		for pane in self.panes.values():
			pane.show(x, y, self.application)
			y+=40




