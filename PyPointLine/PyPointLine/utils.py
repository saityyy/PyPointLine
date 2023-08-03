#
#
#
import math


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

def magnitude(x,y):
	return math.sqrt(x*x+y*y)

def dist(x0,y0,x1,y1):
	return magnitude(x0-x1, y0-y1)

def rotation(x0:float, y0:float, x1:float, y1:float, theta:float) :## theta : clockwise radian
	mx=(x0+x1)*0.5
	my=(y0+y1)*0.5
	ax, ay=x0-mx, y0-my
	bx, by=math.cos(theta)*ax-math.sin(theta)*ay, math.sin(theta)*ax+math.cos(theta)*ay
	return bx+mx, by+my, mx-bx, my-by


	pass