import tkinter as tk

from application import application



if __name__ == "__main__":

	ROOT = tk.Tk()
	ROOT.geometry("1200x1000")
	ROOT.title("PyPointLine version 0.0")
	APP=application(ROOT)
	ROOT.bind("<KeyPress>",APP.keyPressed)
	ROOT.mainloop()



