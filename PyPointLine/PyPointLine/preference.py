
class preference:
	def __init__(self,application):
		self.label="Preference"
		self.parent=None
		self.application=application
		self.canvas=application.prefCanvas
		self.thisis="preference"
		self.lineFeedWidth:int=40
		self.width=300#self.canvas.width
		self.panes=[]
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
			self.type="label"# text, float, radio
			self.label=""
			self.text=""
			self.value=value
			self.radio1=radio1
			self.radio2=radio2
			self.radio=radio
			self.button1=button1
			self.button2=button2
			self.lineFeedWidth=self.preference.lineFeedWidth
		def show(self, y, canvas):
			pass


	def initPointPreference(self):
		self.panes=[]
		self.panes.append(self.prefPane(self, "label","Point",""))
		self.panes.append(self.prefPane(self, "radio","Show name", radio1="On", radio2="Off", radio=1))
		self.panes.append(self.prefPane(self, "float","X", value=0.0))
		self.panes.append(self.prefPane(self, "float","Y", value=0.0))
		self.panes.append(self.prefPane(self, "radio","Fixed", radio1="On", radio2="Off", radio=1))
		self.panes.append(self.prefPane(self, "buttons", ""))
		
		pass

	def showPreferenve(self):
		y=0
		for pane in self.panes:
			pane.show(y, self.canvas)

	def showLogs(self):
		pass



