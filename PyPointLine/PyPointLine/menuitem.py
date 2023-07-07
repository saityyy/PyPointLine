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

	def showIcon(self, canvas):
		canvas.create_image(100*self.x+12.5,100*self.y+12.5,image=self.icon, tag="menuIcon", anchor=tk.NW)
	pass