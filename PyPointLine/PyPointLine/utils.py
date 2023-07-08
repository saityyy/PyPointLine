#
#
#

class mousePosition:
	x=0
	y=0
	bpX=0## buttonPressedX
	bpY=0## buttonPressedY
	magneticPoint=None


def isNear(x0,y0,x1,y1,d):
	x,y = x0-x1, y0-y1
	if x*x+y*y<d*d:
		return True
	return False
