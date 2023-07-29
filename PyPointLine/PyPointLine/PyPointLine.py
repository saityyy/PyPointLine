import tkinter as tk
import os

from application import application

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
	ROOT.bind("<MouseWheel>", APP.wheelTurned)
	path = os.getcwd()# root directory


	ROOT.mainloop()



