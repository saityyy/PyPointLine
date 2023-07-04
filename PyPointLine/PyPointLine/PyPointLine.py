import tkinter as tk

from application import application



if __name__ == "__main__":

	ROOT = tk.Tk()
	ROOT.title("PyPointLine version 0.0")
	APP=application(ROOT)
	ROOT.bind("<KeyPress>",APP.keyPressed)
	ROOT.mainloop()



