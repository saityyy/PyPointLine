import tkinter as tk
from PIL import Image, ImageTk


class menuItem:
	
	def __init__(self, name,x,y):
		self.falename=name
		self.x=x
		self.y=y
		self.menuIcon=None
		self.icon = Image.open(open(name, 'rb'))
		self.icon = self.icon.resize((75,75))
		self.icon = ImageTk.PhotoImage(self.icon)
		self.left = x*100
		self.top = y*100+100
		self.width = 100
		self.height = 100

	def showIcon(self, canvas):
		canvas.create_image(100*self.x+12.5,100*self.y+12.5,image=self.icon, tag="menuIcon", anchor=tk.NW)
	pass

class addPointItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click in the open area."]

class midPointItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click another point."]
		self.point1=None
		self.point2=None
class addLineItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click another point."]
class addCircleItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click in the open area."]
class addAngleItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point.", "Click the second point.", "Click the third point."]
class addLocusItem(menuItem):
	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.headerText=["Click one point."]
