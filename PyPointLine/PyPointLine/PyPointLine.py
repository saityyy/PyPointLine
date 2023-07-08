import tkinter as tk
from PIL import Image, ImageTk

from application import application
import os

if __name__ == "__main__":

	ROOT = tk.Tk()
	ROOT.geometry("1200x1000")
	ROOT.title("PyPointLine version 0.0")
	APP=application(ROOT)
	ROOT.bind("<KeyPress>",APP.keyPressed)
	ROOT.bind("<B1-Motion>", APP.buttonDragging)  # 
	ROOT.bind("<Button-1>", APP.buttonPressed)  # 
	ROOT.bind("<ButtonRelease-1>", APP.buttonReleased)  # 
	ROOT.bind("<Motion>", APP.updateCoordinates) # 
	path = os.getcwd()# root directory


	ROOT.mainloop()



