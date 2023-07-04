from object import object

class ModuleType:
	NONE=0
	MIDPOINT=10


class module(object):
	def __init__(self):
		self.moduletype=ModuleType.NONE
		self.thisis='module'

