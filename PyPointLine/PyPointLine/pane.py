#
#
#

class paneType:
	NONE=0
	FIGURE=1
	FIGURE_LOG=2
	FIGURE_PREFERENCE=3
	MENU=3

class pane:
	"""  """
	def __init__(self, parent, left, top, width, height):
		self.parent=parent
		self.left=left
		self.top=top
		self.width=width
		self.height=height
	pass

	def inside(self, x, y):
		if self.left<x and x<self.left+self.width:
			if self.top<y and y<self.top+self.height:
				return True
		return False


