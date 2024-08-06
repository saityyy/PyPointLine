import tkinter as tk
from object import object, point, line, circle, angle, locus
from utils import *
import math
from preference import preference
from xml.etree import ElementTree as ET


class module(object):
    def __init__(self, app):
        self.app = app
        self.moduletype = "None"
        self.thisis = 'module'
        self.name = self.youngestName(app)
        self.showName = False
        self.tag = "tag_%00d" % (app.nextID)
        self.toBeDestroyed = False
        app.nextID += 1

    def evaluate(self):
        return 0

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="Bisque1", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.name), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "-- - --" % ()
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def drawPreference(self, app):
        pass

    def youngestName(self, app):
        for name in ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20",
                     "M21", "M22", "M23", "M24", "M25", "M26", "M27", "M28", "M29", "M30", "M31", "M32", "M33", "M34", "M35", "M36", "M37", "M38", "M39", "M40"]:
            for obj in app.lines:
                if obj.name == name:
                    break
            else:
                return name
        return "M0"

    def toString(self) -> str:
        return ""

    def toTeXString(self) -> str:
        return ""

    def toXMLElement(self, parent_element) -> str:
        return ""


class midpoint(module):
    def __init__(self, app, point1: point, point2: point, point3: point):
        super().__init__(app)
        self.moduletype = "midpoint"
        self.p1 = point1
        self.p2 = point2
        self.p3 = point3
        self.ratio1 = 1
        self.ratio2 = 1
        self.para1 = 0.02
        self.para2 = 0.02
        self.para3 = 0.1
        self.pref = preference(self.app, self)
        pass

    def evaluate(self):
        r1 = self.ratio1
        r2 = self.ratio2
        x1 = ((-self.p2.x*r1+(r1+r2)*self.p3.x)/r2-self.p1.x)*self.para1
        y1 = ((-self.p2.y*r1+(r1+r2)*self.p3.y)/r2-self.p1.y)*self.para1
        x2 = ((-self.p1.x*r2+(r1+r2)*self.p3.x)/r1-self.p2.x)*self.para2
        y2 = ((-self.p1.y*r2+(r1+r2)*self.p3.y)/r1-self.p2.y)*self.para2
        x3 = ((self.p1.x*r2+self.p2.x*r1)/(r1+r2)-self.p3.x)*self.para3
        y3 = ((self.p1.y*r2+self.p2.y*r1)/(r1+r2)-self.p3.y)*self.para3
        self.p1.x += x1
        self.p1.y += y1
        self.p2.x += x2
        self.p2.y += y2
        self.p3.x += x3
        self.p3.y += y3
        return magnitude(x1, y1)+magnitude(x2, y2)+magnitude(x3, y3)

    def drawPreference(self, app):
        pass

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "%s (%d) - %s - (%d) %s" % (self.p1.name,
                                               self.ratio1, self.p3.name, self.ratio2, self.p2.name)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=midpoint,tag=%s,p1=%s,p2=%s,p3=%s,ratio1=%d,ratio2=%d,para1=%f,para2=%f,para3=%f" % (self.tag, self.p1.tag, self.p2.tag, self.p3.tag, self.ratio1, self.ratio2, self.para1, self.para2, self.para3)

    def toXMLElement(self, parent_element):
        elem = ET.SubElement(parent_element, "middle-point")
        elem.set("point-id1", self.p1.tag)
        elem.set("point-id2", self.p2.tag)
        elem.set("middle-point-id", self.p3.tag)

    def matter(self, obj):
        if obj != None and obj == self.p1:
            return True
        if obj != None and obj == self.p2:
            return True
        if obj != None and obj == self.p3:
            return True
        return False


class point2point(module):
    def __init__(self, app, point1: point, point2: point):
        super().__init__(app)
        self.moduletype = "point2point"
        self.p1 = point1
        self.p2 = point2
        self.para1 = 0.1
        self.para2 = 0.1
        self.pref = preference(self.app, self)

    def evaluate(self):
        x1 = (self.p2.x-self.p1.x)*self.para1
        y1 = (self.p2.y-self.p1.y)*self.para1
        x2 = (self.p1.x-self.p2.x)*self.para2
        y2 = (self.p1.y-self.p2.y)*self.para2
        if self.p1.fixed == False:
            self.p1.x += x1
            self.p1.y += y1
        if self.p2.fixed == False:
            self.p2.x += x2
            self.p2.y += y2
        return magnitude(x1, y1)+magnitude(x2, y2)

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "%s - %s" % (self.p1.name, self.p2.name)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=point2point,tag=%s,p1=%s,p2=%s,para1=%f,para2=%f" % (self.tag, self.tag, self.p1.tag, self.p2.tag, self.para1, self.para2)

    def toXMLElement(self, parent_element):
        pass

    def matter(self, obj):
        if obj != None and obj == self.p1:
            return True
        if obj != None and obj == self.p2:
            return True
        return False


class point2line(module):
    def __init__(self, app, point1: point, line1: line):
        super().__init__(app)
        self.moduletype = "point2line"
        self.p1 = point1
        self.l1 = line1
        self.thisis = 'module'
        self.onlyOnSegment = True
        self.para1 = 0.02
        self.para2 = 0.1
        self.pref = preference(self.app, self)

    def evaluate(self):
        p2 = self.l1.point1
        p3 = self.l1.point2
        ax, ay = self.p1.x, self.p1.y
        bx, by = p2.x, p2.y
        cx, cy = p3.x, p3.y
        tn = (ax-bx)*(cx-bx)+(ay-by)*(cy-by)
        td = (cx-bx)*(cx-bx)+(cy-by)*(cy-by)
        if td == 0:
            return
        tt = tn/td
        if 0 <= tt and tt <= 1:
            dx, dy = tt*(cx-bx)+(bx-ax), tt*(cy-by)+(by-ay)
            if self.p1.fixed == False:
                self.p1.x += dx*self.para1
                self.p1.y += dy*self.para1
            if self.l1.point1.fixed == False:
                self.l1.point1.x -= dx*self.para2
                self.l1.point1.y -= dy*self.para2
            if self.l1.point2.fixed == False:
                self.l1.point2.x -= dx*self.para2
                self.l1.point2.y -= dy*self.para2
        elif tt < 0:
            tt = (-tt)/(1-tt)
            dx, dy = tt*(cx-ax)+(ax-bx), tt*(cy-ay)+(ay-by)
            if self.p1.fixed == False:
                self.p1.x -= dx*self.para2
                self.p1.y -= dy*self.para2
            if self.l1.point1.fixed == False:
                self.l1.point1.x += dx*self.para1
                self.l1.point1.y += dy*self.para1
            if self.l1.point2.fixed == False:
                self.l1.point2.x -= dx*self.para2
                self.l1.point2.y -= dy*self.para2
        else:
            tt = 1/tt
            dx, dy = tt*(ax-bx)+(bx-cx), tt*(ay-by)+(by-cy)
            if self.p1.fixed == False:
                self.p1.x -= dx*self.para2
                self.p1.y -= dy*self.para2
            if self.l1.point1.fixed == False:
                self.l1.point1.x -= dx*self.para2
                self.l1.point1.y -= dy*self.para2
            if self.l1.point2.fixed == False:
                self.l1.point2.x += dx*self.para1
                self.l1.point2.y += dy*self.para1
        return magnitude(dx, dy)*(self.para1+self.para2*2)

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "%s - %s" % (self.p1.name, self.l1.name)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=point2line,tag=%s,p1=%s,l1=%s,onlyOnSegment=%d,para1=%f" % (self.tag, self.p1.tag, self.l1.tag, int(self.onlyOnSegment), self.para1)

    def toXMLElement(self, parent_element):
        elem = ET.SubElement(parent_element, "point-on-line")
        elem.set("point-id", self.p1.tag)
        elem.set("line-id", self.l1.tag)

    def matter(self, obj):
        if obj != None and obj == self.p1:
            return True
        if obj != None and obj == self.l1:
            return True
        return False


class point2circle(module):
    def __init__(self, app, point: point, circle: circle):
        super().__init__(app)
        self.moduletype = "point2circle"
        self.p1 = point
        self.c1 = circle
        self.thisis = 'module'
        self.para1 = 0.1
        self.pref = preference(self.app, self)

    def evaluate(self):
        c1 = self.c1
        p2 = c1.point1
        radius = c1.radius
        ax, ay = p2.x-self.p1.x, p2.y-self.p1.y
        mag = magnitude(ax, ay)
        if mag == 0:
            return
        difference = (mag-radius)*self.para1
        dx, dy = ax/mag*difference, ay/mag*difference
        if self.p1.fixed == False:
            self.p1.x += dx
            self.p1.y += dy
        if self.c1.point1.fixed == False:
            self.c1.point1.x -= dx
            self.c1.point1.y -= dy
        if self.c1.fixedRadius == False:
            self.c1.radius += difference
        return abs(difference)*3

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "%s - %s" % (self.p1.name, self.c1.name)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=point2circle,tag=%s,p1=%s,c1=%s,para1=%f" % (self.tag, self.p1.tag, self.c1.tag, self.para1)

    def toXMLElement(self, parent_element):
        elem = ET.SubElement(parent_element, "point-on-circle")
        elem.set("point-id", self.p1.tag)
        elem.set("circle-id", self.c1.tag)

    def matter(self, obj):
        if obj != None and obj == self.p1:
            return True
        if obj != None and obj == self.c1:
            return True
        return False


class line2circle(module):
    def __init__(self, app, line1: line, circle1: circle):
        super().__init__(app)
        self.moduletype = "line2circle"
        self.cc = circle1
        self.ln = line1
        self.thisis = 'module'
        self.para1 = 0.1
        self.pref = preference(self.app, self)

    def evaluate(self):
        p1 = self.cc.point1
        radius = self.cc.radius
        p2 = self.ln.point1
        p3 = self.ln.point2
        ax, ay = p1.x, p1.y
        bx, by = p2.x, p2.y
        cx, cy = p3.x, p3.y
        tn = (ax-bx)*(cx-bx)+(ay-by)*(cy-by)
        td = (cx-bx)*(cx-bx)+(cy-by)*(cy-by)
        if td == 0:
            return
        tt = tn/td
        dx, dy = tt*(cx-bx)+(bx-ax), tt*(cy-by)+(by-ay)
        mag = magnitude(dx, dy)
        if mag == 0:
            return
        difference = (mag-radius)*self.para1
        ex, ey = dx/mag*difference, dy/mag*difference
        if self.cc.point1.fixed == False:
            self.cc.point1.x += ex
            self.cc.point1.y += ey
        if self.cc.fixedRadius == False:
            self.cc.radius += difference
        if self.ln.point1.fixed == False:
            self.ln.point1.x -= ex
            self.ln.point1.y -= ey
        if self.ln.point2.fixed == False:
            self.ln.point2.x -= ex
            self.ln.point2.y -= ey
        return abs(difference)*3

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "%s - %s" % (self.ln.name, self.cc.name)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=line2circle,tag=%s,ln=%s,cc=%s,para1=%f" % (self.tag, self.ln.tag, self.cc.tag, self.para1)

    def toXMLElement(self, parent_element):
        elem = ET.SubElement(parent_element, "line-tangent-circle")
        elem.set("line-id", self.ln.tag)
        elem.set("circle-id", self.cc.tag)

    def matter(self, obj):
        if obj != None and obj == self.cc:
            return True
        if obj != None and obj == self.ln:
            return True
        return False


class circle2circle(module):
    def __init__(self, app, circle1: circle, circle2: circle):
        super().__init__(app)
        self.moduletype = "circle2circle"
        self.cc1 = circle1
        self.cc2 = circle2
        self.thisis = 'module'
        self.para1 = 0.025
        self.pref = preference(self.app, self)

    def evaluate(self):
        p1 = self.cc1.point1
        radius1 = self.cc1.radius
        p2 = self.cc2.point1
        radius2 = self.cc2.radius
        cx, cy = p2.x - p1.x, p2.y - p1.y
        mag = magnitude(cx, cy)
        if mag == 0.0:
            return
        deltaIn = mag - abs(radius1 - radius2)
        deltaOut = mag-(radius1 + radius2)
        if abs(deltaIn) > abs(deltaOut):  # outer tangent
            difference = deltaOut * self.para1
            dx, dy = cx/mag*difference, cy/mag*difference
            self.cc1.point1.x += dx
            self.cc1.point1.y += dy
            if self.cc1.fixedRadius == False:
                self.cc1.radius += difference
            self.cc2.point1.x -= dx
            self.cc2.point1.y -= dy
            if self.cc2.fixedRadius == False:
                self.cc2.radius += difference
            return abs(difference)*2
        else:  # inner tangent
            difference = deltaIn * self.para1
            dx, dy = cx/mag*difference, cy/mag*difference
            if self.cc1.point1.fixed == False:
                self.cc1.point1.x += dx
                self.cc1.point1.y += dy
            if self.cc2.point1.fixed == False:
                self.cc2.point1.x -= dx
                self.cc2.point1.y -= dy
            if radius1 > radius2:
                if self.cc1.fixedRadius == False:
                    self.cc1.radius += difference
                if self.cc2.fixedRadius == False:
                    self.cc2.radius -= difference
            else:
                if self.cc1.fixedRadius == False:
                    self.cc1.radius -= difference
                if self.cc2.fixedRadius == False:
                    self.cc2.radius += difference
            return abs(difference)*2

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "%s - %s" % (self.cc1.name, self.cc2.name)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=circle2circle,tag=%s,cc1=%s,cc2=%s,para1=%f" % (self.tag, self.cc1.tag, self.cc2.tag, self.para1)

    def toXMLElement(self, parent_element):
        elem = ET.SubElement(parent_element, "circle-tangent-circle")
        elem.set("circle-id1", self.cc1.tag)
        elem.set("circle-id2", self.cc2.tag)

    def matter(self, obj):
        if obj != None and obj == self.cc1:
            return True
        if obj != None and obj == self.cc2:
            return True
        return False


class isometry(module):
    def __init__(self, app, line1: line, line2: line):
        super().__init__(app)
        self.moduletype = "isometry"
        self.ln1 = line1
        self.ln2 = line2
        self.thisis = 'module'
        self.ratio1 = 1
        self.ratio2 = 1
        self.fixedRatio = True
        self.para1 = 0.25
        self.pref = preference(self.app, self)
        if self.ln1.isomParent != None:
            if self.ln2.isomParent != None:
                self.ln2.isomAncestor.isomParent = self.ln1.isomAncestor
            else:  # if self.ln2.isomParent==None:
                self.ln2.isomParent = self.ln1
        else:  # if self.ln1.isomParent==None:
            self.ln1.isomParent = self.ln1
            self.ln2.isomParent = self.ln1

    def evaluate(self):
        p1 = self.ln1.point1
        p2 = self.ln1.point2
        p3 = self.ln2.point1
        p4 = self.ln2.point2
        ax, ay = p2.x-p1.x, p2.y-p1.y
        magA = magnitude(ax, ay)
        bx, by = p4.x-p3.x, p4.y-p3.y
        magB = magnitude(bx, by)
        if magA == 0.0 or magB == 0.0:
            return
        delta = (magB*self.ratio1 - magA*self.ratio2) * \
            self.para1 / (self.ratio1 + self.ratio2)
        delta1 = delta*self.ratio2 / (self.ratio1 + self.ratio2)
        delta2 = delta*self.ratio1 / (self.ratio1 + self.ratio2)
        cx, cy = ax/magA*delta1, ay/magA*delta1
        dx, dy = bx/magB*delta2, by/magB*delta2
        if self.ln1.point1.fixed == False:
            self.ln1.point1.x -= cx
            self.ln1.point1.y -= cy
        if self.ln1.point2.fixed == False:
            self.ln1.point2.x += cx
            self.ln1.point2.y += cy
        if self.ln2.point1.fixed == False:
            self.ln2.point1.x += dx
            self.ln2.point1.y += dy
        if self.ln2.point2.fixed == False:
            self.ln2.point2.x -= dx
            self.ln2.point2.y -= dy
        return abs(delta)*2

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "%s - %s (%d : %d)" % (self.ln1.name,
                                          self.ln2.name, self.ratio1, self.ratio2)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=isometry,tag=%s,ln1=%s,ln2=%s,ratio1=%d,ratio2=%d,fixedRatio=%d,para1=%f" % (self.tag, self.ln1.tag, self.ln2.tag, self.ratio1, self.ratio2, int(self.fixedRatio), self.para1)

    def toXMLElement(self, parent_element):
        elem = ET.SubElement(parent_element, "isometry")
        elem.set("line-id1", self.ln1.tag)
        elem.set("line-id2", self.ln2.tag)

    def matter(self, obj):
        if obj != None and obj == self.ln1:
            return True
        if obj != None and obj == self.ln2:
            return True
        return False


class parallel(module):
    def __init__(self, app, line1: line, line2: line):
        super().__init__(app)
        self.line1 = line1
        self.line2 = line2
        self.moduletype = "parallel"
        self.thisis = 'module'
        self.para1 = 0.05
        self.pref = preference(self.app, self)
        pass

    def evaluate(self):
        p1: point = self.line1.point1
        p2: point = self.line1.point2
        p3: point = self.line2.point1
        p4: point = self.line2.point2
        theta1 = math.atan2(p2.y-p1.y, p2.x-p1.x)
        theta2 = math.atan2(p4.y-p3.y, p4.x-p3.x)
        line1mag = dist(p1.x, p1.y, p2.x, p2.y)
        line2mag = dist(p3.x, p3.y, p4.x, p4.y)
        # print("theta = %f"%(theta2-theta1))
        if theta1 < theta2-math.pi*3/2:
            difference = -(math.pi*2-theta2+theta1)*self.para1
        elif theta1 < theta2-math.pi:
            difference = (theta2-theta1-math.pi)*self.para1
        elif theta1 < theta2-math.pi/2:
            difference = -(math.pi-theta2+theta1)*self.para1
        elif theta1 < theta2:
            difference = (theta2-theta1)*self.para1
        elif theta1 < theta2+math.pi/2:
            difference = -(theta1-theta2)*self.para1
        elif theta1 < theta2+math.pi:
            difference = (math.pi-theta1+theta2)*self.para1
        elif theta1 < theta2+math.pi*3/2:
            difference = -(theta1-theta2-math.pi)*self.para1
        else:  # if theta1<theta1-math.pi*3/2:
            difference = (math.pi*2-theta1+theta2)*self.para1
        x1, y1, x2, y2 = rotation(
            self.line1.point1.x, self.line1.point1.y, self.line1.point2.x, self.line1.point2.y,
            difference*line2mag/(line1mag+line2mag)
        )
        if self.line1.point1.fixed == False:
            self.line1.point1.x, self.line1.point1.y = x1, y1
        if self.line1.point2.fixed == False:
            self.line1.point2.x, self.line1.point2.y = x2, y2
        x3, y3, x4, y4 = rotation(
            self.line2.point1.x, self.line2.point1.y, self.line2.point2.x, self.line2.point2.y,
            -difference*line1mag/(line1mag+line2mag)
        )
        if self.line2.point1.fixed == False:
            self.line2.point1.x, self.line2.point1.y = x3, y3
        if self.line2.point2.fixed == False:
            self.line2.point2.x, self.line2.point2.y = x4, y4
        return abs(difference)*2
        pass

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "%s || %s " % (self.line1.name, self.line2.name)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=parallel,tag=%s,line1=%s,line2=%s,para1=%f" % (self.tag, self.line1.tag, self.line2.tag, self.para1)

    def toXMLElement(self, parent_element):
        elem = ET.SubElement(parent_element, "parallel")
        elem.set("line-id1", self.line1.tag)
        elem.set("line-id2", self.line2.tag)

    def matter(self, obj):
        if obj != None and obj == self.line1:
            return True
        if obj != None and obj == self.line2:
            return True
        return False


class perpendicular(module):
    def __init__(self, app, line1: line, line2: line):
        super().__init__(app)
        self.line1 = line1
        self.line2 = line2
        self.moduletype = "perpendicular"
        self.thisis = 'module'
        self.para1 = 0.1
        self.pref = preference(self.app, self)
        pass

    def evaluate(self):
        p1: point = self.line1.point1
        p2: point = self.line1.point2
        p3: point = self.line2.point1
        p4: point = self.line2.point2
        theta1 = math.atan2(p2.y-p1.y, p2.x-p1.x)
        theta2 = math.atan2(p4.y-p3.y, p4.x-p3.x)
        # print("theta = %f"%(theta2-theta1))
        if theta1 < theta2-math.pi:
            difference = -(math.pi*3/2-theta2+theta1)*self.para1
        elif theta1 < theta2:
            difference = (theta2-theta1-math.pi/2)*self.para1
        elif theta1 < theta2+math.pi:
            difference = -(theta1-theta2-math.pi/2)*self.para1
        else:
            difference = (math.pi*3/2-theta1+theta2)*self.para1
        x1, y1, x2, y2 = rotation(
            self.line1.point1.x, self.line1.point1.y, self.line1.point2.x, self.line1.point2.y, difference
        )
        if self.line1.point1.fixed == False:
            self.line1.point1.x, self.line1.point1.y = x1, y1
        if self.line1.point2.fixed == False:
            self.line1.point2.x, self.line1.point2.y = x2, y2
        x3, y3, x4, y4 = rotation(
            self.line2.point1.x, self.line2.point1.y, self.line2.point2.x, self.line2.point2.y, -difference
        )
        if self.line2.point1.fixed == False:
            self.line2.point1.x, self.line2.point1.y = x3, y3
        if self.line2.point2.fixed == False:
            self.line2.point2.x, self.line2.point2.y = x4, y4
        return abs(difference)*2

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "%s ⟂ %s " % (self.line1.name, self.line2.name)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=perpendicular,tag=%s,line1=%s,line2=%s,para1=%f" % (self.tag, self.line1.tag, self.line2.tag, self.para1)

    def toXMLElement(self, parent_element):
        elem = ET.SubElement(parent_element, "vertical")
        elem.set("line-id1", self.line1.tag)
        elem.set("line-id2", self.line2.tag)

    def matter(self, obj):
        if obj != None and obj == self.line1:
            return True
        if obj != None and obj == self.line2:
            return True
        return False


class horizontal(module):
    def __init__(self, app, line1: line):
        super().__init__(app)
        self.thisis = 'module'
        self.moduletype = 'horizontal'
        self.line1 = line1
        self.para1 = 0.1
        self.pref = preference(self.app, self)
        pass

    def evaluate(self):
        p1: point = self.line1.point1
        p2: point = self.line1.point2
        theta = math.atan2(p2.y-p1.y, p2.x-p1.x)
        if -math.pi/2 <= theta and theta <= math.pi/2:
            difference = -theta*self.para1
        elif -math.pi/2 > theta:
            difference = (-math.pi-theta)*self.para1
        else:
            difference = (math.pi-theta)*self.para1
        x1, y1, x2, y2 = rotation(p1.x, p1.y, p2.x, p2.y, difference)
        if self.line1.point1.fixed == False:
            self.line1.point1.x, self.line1.point1.y = x1, y1
        if self.line1.point2.fixed == False:
            self.line1.point2.x, self.line1.point2.y = x2, y2
        return abs(difference)

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "%s = " % (self.line1.name)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        canvas.create_text(x+5, y+57, text="Hide Name",
                           anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=horizontal,tag=%s,line1=%s,para1=%f" % (self.tag, self.line1.tag, self.para1)

    def matter(self, obj):
        if obj != None and obj == self.line1:
            return True
        return False


class bisector(module):
    def __init__(self, app, angle1: angle, angle2: angle):
        super().__init__(app)
        self.thisis = 'module'
        self.moduletype = 'bisector'
        self.angle1 = angle1
        self.angle2 = angle2
        self.para1 = 0.1
        self.pref = preference(self.app, self)
        pass

    def getDelta(self, angle1: angle, radianValue: float) -> float:
        theta1 = math.atan2(angle1.point1.y-angle1.point2.y,
                            angle1.point1.x-angle1.point2.x)
        theta3 = math.atan2(angle1.point3.y-angle1.point2.y,
                            angle1.point3.x-angle1.point2.x)
        rad2ang = 180/math.pi
        if theta1+math.pi < theta3:
            extent = theta1 - theta3 + 2*math.pi
            delta = -(extent - radianValue)*self.para1
        elif theta1 < theta3:
            extent = theta3 - theta1
            delta = (extent - radianValue)*self.para1
        elif theta1-math.pi < theta3:
            extent = theta1 - theta3
            delta = -(extent - radianValue)*self.para1
        else:
            extent = theta3 - theta1 + 2*math.pi
            delta = (extent - radianValue)*self.para1
        return delta

    def evaluate(self):
        ang2rad = math.pi/180
        self.angle2.restoreValue()
        delta1 = self.getDelta(self.angle1, self.angle2.value*ang2rad)
        ret = 0.0
        if self.angle1.fixValue == False:
            x1, y1, x2, y2 = rotation(
                self.angle1.point1.x, self.angle1.point1.y, self.angle1.point2.x, self.angle1.point2.y, delta1)
            x3, y3, x4, y4 = rotation(
                self.angle1.point3.x, self.angle1.point3.y, x2, y2, -delta1)
            if self.angle1.point1.fixed == False:
                self.angle1.point1.x, self.angle1.point1.y = x1, y1
                ret += abs(delta1)
            if self.angle1.point2.fixed == False:
                self.angle1.point2.x, self.angle1.point2.y = x4, y4
                ret += abs(delta1)
            if self.angle1.point3.fixed == False:
                self.angle1.point3.x, self.angle1.point3.y = x3, y3
                ret += abs(delta1)
        self.angle1.restoreValue()
        delta2 = self.getDelta(self.angle2, self.angle1.value*ang2rad)
        if self.angle2.fixValue == False:
            x1, y1, x2, y2 = rotation(
                self.angle2.point1.x, self.angle2.point1.y, self.angle2.point2.x, self.angle2.point2.y, delta2)
            x3, y3, x4, y4 = rotation(
                self.angle2.point3.x, self.angle2.point3.y, x2, y2, -delta2)
            if self.angle2.point1.fixed == False:
                self.angle2.point1.x, self.angle2.point1.y = x1, y1
                ret += abs(delta2)
            if self.angle2.point2.fixed == False:
                self.angle2.point2.x, self.angle2.point2.y = x4, y4
                ret += abs(delta2)
            if self.angle2.point3.fixed == False:
                self.angle2.point3.x, self.angle2.point3.y = x3, y3
                ret += abs(delta2)
        # self.angle1.restoreValue()
        # self.angle2.restoreValue()
        return ret*2

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        thisLine = "∠%s%s%s = ∠%s%s%s" % (self.angle1.point1.name, self.angle1.point2.name, self.angle1.point3.name,
                                          self.angle2.point1.name, self.angle2.point2.name, self.angle2.point3.name)
        canvas.create_text(x+5, y+31, text=thisLine,
                           anchor=tk.NW, font=("", 18), width=270)
        # canvas.create_text(x+5,y+57,text="Hide Name",  anchor=tk.NW, font=("",18), width=270 )
        pass

    def toString(self) -> str:
        return "type=module,moduletype=bisector,tag=%s,angle1=%s,angle2=%s,para1=%f" % (self.tag, self.angle1.tag, self.angle2.tag, self.para1)

    def toXMLElement(self, parent_element):
        elem = ET.SubElement(parent_element, "bisector")
        elem.set("angle-id1", self.angle1.tag)
        elem.set("angle-id2", self.angle2.tag)

    def matter(self, obj):
        if obj != None and obj == self.angle1:
            return True
        if obj != None and obj == self.angle2:
            return True
        return False


class crossing(module):
    def __init__(self, app, point0: point, object1: object, object2: object):
        super().__init__(app)
        self.thisis = 'module'
        self.moduletype = 'crossing'
        self.point0 = point0
        self.object1 = object1
        self.object2 = object2
        self.para1 = 0.1
        self.para2 = 0.03
        self.pref = preference(self.app, self)
        pass

    def evaluate(self) -> float:
        err: float = 0
        if self.object1.thisis == "line" and self.object2.thisis == "line":
            point11: point = self.object1.point1
            point12: point = self.object1.point2
            line1a: float = point11.y-point12.y
            line1b: float = -point11.x+point12.x
            line1c: float = point11.x*point12.y - point12.x*point11.y
            point21 = self.object2.point1
            point22 = self.object2.point2
            line2a: float = point21.y-point22.y
            line2b: float = -point21.x+point22.x
            line2c: float = point21.x*point22.y - point22.x*point21.y
            point3x: float = line1b*line2c - line1c*line2b
            point3y: float = line1c*line2a - line1a*line2c
            point3z: float = line1a*line2b - line1b*line2a
            if point3z != 0:
                point3x /= point3z
                point3y /= point3z
                if self.point0.fixed == False:
                    self.point0.x += (point3x - self.point0.x)*self.para1
                    self.point0.y += (point3y - self.point0.y)*self.para1
                    err += dist(point3x, point3y, self.point0.x,
                                self.point0.y)*self.para1
            ax, ay = self.point0.x, self.point0.y
            bx, by = point11.x, point11.y
            cx, cy = point12.x, point12.y
            tn = (ax-bx)*(cx-bx)+(ay-by)*(cy-by)
            td = (cx-bx)*(cx-bx)+(cy-by)*(cy-by)
            if td != 0:
                tt = tn/td
                dx, dy = tt*(cx-bx)+(bx-ax), tt*(cy-by)+(by-ay)
                if self.object1.point1.fixed == False:
                    self.object1.point1.x -= dx*self.para2
                    self.object1.point1.y -= dy*self.para2
                    err += magnitude(dx, dy)*self.para2
                if self.object1.point2.fixed == False:
                    self.object1.point2.x -= dx*self.para2
                    self.object1.point2.y -= dy*self.para2
                    err += magnitude(dx, dy)*self.para2
            ax, ay = self.point0.x, self.point0.y
            bx, by = point21.x, point21.y
            cx, cy = point22.x, point22.y
            tn = (ax-bx)*(cx-bx)+(ay-by)*(cy-by)
            td = (cx-bx)*(cx-bx)+(cy-by)*(cy-by)
            if td != 0:
                tt = tn/td
                dx, dy = tt*(cx-bx)+(bx-ax), tt*(cy-by)+(by-ay)
                if self.object2.point1.fixed == False:
                    self.object2.point1.x -= dx*self.para2
                    self.object2.point1.y -= dy*self.para2
                    err += magnitude(dx, dy)*self.para2
                if self.object2.point2.fixed == False:
                    self.object2.point2.x -= dx*self.para2
                    self.object2.point2.y -= dy*self.para2
                    err += magnitude(dx, dy)*self.para2
            return err

    def drawLog(self, app):
        canvas = app.prefCanvas
        x, y, w, h = 5, app.logLineFeed+5, 280, 90
        app.logLineFeed += 100
        canvas.create_rectangle(x, y, x+w, y+h, fill="turquoise", width=3)
        canvas.create_text(x+5, y+5, text="Module : %s" %
                           (self.moduletype), anchor=tk.NW, font=("", 18), width=270)
        if self.object1.thisis == "line" and self.object2.thisis == "line":
            thisLine = "Line %s%s : line %s%s" % (
                self.object1.point1.name, self.object1.point2.name, self.object2.point1.name, self.object2.point2.name)
            canvas.create_text(x+5, y+31, text=thisLine,
                               anchor=tk.NW, font=("", 18), width=270)
        pass

    def toString(self) -> str:
        return "type=module,moduletype=crossing,tag=%s,point0=%s, object1=%s,object2=%s,para1=%f,para2=%f" % (self.tag, self.point0.tag, self.object1.tag, self.object2.tag, self.para1, self.para2)

    def toXMLElement(self, parent_element):
        elem = ET.SubElement(parent_element, "crossing")
        elem.set("point-id", self.point0.tag)
        elem.set("object-id1", self.object1.tag)
        elem.set("object-id2", self.object2.tag)

    def matter(self, obj) -> bool:
        if obj != None and obj == self.object1:
            return True
        if obj != None and obj == self.object2:
            return True
        if obj != None and obj == self.point0:
            return True
        return False
