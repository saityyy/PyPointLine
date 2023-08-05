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
		def __init__(self, pref, type:str, label:str, radio1:str="", radio2:str="", radio:int=1, value:float=0.0, button1:str="Cancel", button2:str="OK"):
			self.preference=pref
			self.type=type# text, float, radio
			self.label=""
			self.text=label
			self.value=value
			self.radio1=radio1
			self.radio2=radio2
			self.radio=radio
			self.button1=button1
			self.button2=button2
			self.lineFeedWidth=self.preference.lineFeedWidth
		def show(self, y, canvas):
			##canvas.delete("all")
			if self.type=="label":
				text="%s : %s"%(self.text,self.preference.parent.name)
				canvas.create_text(10,y*40+30,text=text, anchor=tk.W, font=("",18), width=270  )
			elif self.type=="radio":
				px_v = tk.IntVar(value=y)
				lbl = tk.Label(text=self.text, font=("",18))
				lbl.place(x=910, y=y*40+30)
				px_radio_1 = tk.Radiobutton(self.preference.application.root, text=self.radio1, font=("",18), value=1, variable=px_v )
				px_radio_1.place(x=1000, y=y*40+30)
				px_radio_2 = tk.Radiobutton(self.preference.application.root, text=self.radio2, font=("",18), value=2, variable=px_v )
				px_radio_2.place(x=1100, y=y*40+30)
			elif self.type=="float":
				lbl = tk.Label(text=self.text, font=("",18))
				lbl.place(x=930, y=y*40+30)
				txt = tk.Entry(width=10, font=("",18))
				txt.place(x=990, y=y*40+30)	
			elif self.type=="buttons":
				frame1 = tk.Frame(self.preference.application.prefCanvas )
				frame1.place(x=10,y=y*40+30)
				button1=tk.Button(frame1, text="OK", background="green", font=("",20), anchor=tk.CENTER, width=8, height=1)
				#button1.place(x=0, y=0 )
				button1.pack()
				frame2 = tk.Frame(self.preference.application.prefCanvas)
				frame2.place(x=150,y=y*40+30)
				button2=tk.Button(frame2, text="Cancel", background="green", font=("",20), anchor=tk.CENTER, width=8, height=1 )
				button2.pack()
			pass


	def initPointPreference(self):
		self.panes=[]
		self.panes.append(self.prefPane(self, "label","Point",""))
		self.panes.append(self.prefPane(self, "radio","Name", radio1="Show", radio2="Hide", radio=1))
		self.panes.append(self.prefPane(self, "float","X", value=0.0))
		self.panes.append(self.prefPane(self, "float","Y", value=0.0))
		self.panes.append(self.prefPane(self, "radio","Fixed", radio1="On", radio2="Off", radio=1))
		self.panes.append(self.prefPane(self, "buttons", ""))
		
		pass

	def showPreference(self):
		y=0
		for pane in self.panes:
			pane.show(y, self.canvas)
			y+=1




