from object import object

class ModuleType:
	NONE=0
	MIDPOINT=10


class module(object):
	def __init__(self):
		self.moduletype=ModuleType.NONE
		self.input1=None
		self.input2=None
		self.input3=None
		self.output1=None
		self.output2=None
		self.output3=None
		self.thisis='module'

