#
#
#

class mousePosition:
	x=0## world
	y=0## world
	bpX=0## buttonPressedX
	bpY=0## buttonPressedY
	canvasX=0
	canvasY=0
	magneticPoint=None


def isNear(x0,y0,x1,y1,d):
	x,y = x0-x1, y0-y1
	if x*x+y*y<d*d:
		return True
	return False

def isIn(x,y,left,top,width,height):
	if left<x and x<left+width:
		if top<y and y<top+height:
			return True
	return False
