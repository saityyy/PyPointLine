# flake8:noqa E741
import math
import warnings
from pprint import pprint
import xml.etree.ElementTree as ET
import os
import random
import numpy as np
from scipy.optimize import fsolve

from utils import xml2dict

EPSILON = 1e-18


class Solver:
    def __init__(self, figures_list):
        self.tag2point = {}
        self.tag2line = {}
        self.tag2circle = {}
        self.tag2angle = {}
        self.modules = []
        for figure in figures_list:
            if figure["type"] == "point":
                point = self.Point(figure["tag"], figure["x"], figure["y"])
                self.tag2point[figure["tag"]] = point
            elif figure["type"] == "line":
                line = self.Line(figure["tag"],
                                 self.tag2point[figure["point1"]], self.tag2point[figure["point2"]])
                self.tag2line[figure["tag"]] = line
                if not line.is_valid():
                    print("Invalid line")
            elif figure["type"] == "circle":

                circle = self.Circle(figure["tag"],
                                     self.tag2point[figure["point1"]], figure["radius"])
                self.tag2circle[figure["tag"]] = circle
                if not circle.is_valid():
                    print("Invalid circle")
            elif figure["type"] == "angle":
                angle = self.Angle(figure["tag"], self.tag2point[figure["point1"]],
                                   self.tag2point[figure["point2"]], self.tag2point[figure["point3"]])
                self.tag2angle[figure["tag"]] = angle
                if not angle.is_valid():
                    print("Invalid angle")
            elif figure["type"] == "module":
                if figure["moduletype"] == "midpoint":
                    midpoint = self.MidPoint(
                        self.tag2point[figure["p1"]], self.tag2point[figure["p2"]], self.tag2point[figure["p3"]])
                    self.modules.append(midpoint)
                    if not midpoint.is_valid():
                        print("Invalid module midpoint")
                if figure["moduletype"] == "point2line":
                    p2l = self.P2L(self.tag2point[figure["p1"]],
                                   self.tag2line[figure["l1"]])
                    self.modules.append(p2l)
                    if not p2l.is_valid():
                        print("Invalid module p2l")
                elif figure["moduletype"] == "point2circle":
                    p2c = self.P2C(
                        self.tag2point[figure["p1"]], self.tag2circle[figure["c1"]])
                    self.modules.append(p2c)
                    if not p2c.is_valid():
                        print("Invalid module p2c")
                elif figure["moduletype"] == "line2circle":
                    l2c = self.L2C(
                        self.tag2line[figure["ln"]], self.tag2circle[figure["cc"]])
                    self.modules.append(l2c)
                    if not l2c.is_valid():
                        print("Invalid module l2c")
                elif figure["moduletype"] == "circle2circle":
                    c2c = self.C2C(
                        self.tag2circle[figure["cc1"]], self.tag2circle[figure["cc2"]])
                    self.modules.append(c2c)
                    if not c2c.is_valid():
                        print("Invalid module c2c")
                elif figure["moduletype"] == "parallel":
                    parallel = self.Parallel(
                        self.tag2line[figure["line1"]], self.tag2line[figure["line2"]])
                    self.modules.append(parallel)
                    if not parallel.is_valid():
                        print("Invalid module parallel")
                elif figure["moduletype"] == "perpendicular":
                    vertical = self.Vertical(
                        self.tag2line[figure["line1"]], self.tag2line[figure["line2"]])
                    self.modules.append(vertical)
                    if not vertical.is_valid():
                        print("Invalid module vertical")
                elif figure["moduletype"] == "isometry":
                    isometry = self.Isometry(
                        self.tag2line[figure["line1"]], self.tag2line[figure["line2"]])
                    self.modules.append(isometry)
                    if not isometry.is_valid():
                        print("Invalid module isometry")
                elif figure["moduletype"] == "bisector":
                    bisector = self.Bisector(
                        self.tag2angle[figure["angle1"]], self.tag2angle[figure["angle2"]])
                    self.modules.append(bisector)
                    if not bisector.is_valid():
                        print("Invalid module bisector")
                elif figure["moduletype"] == "crossing":
                    if figure["object1"] in self.tag2line.keys():
                        o1 = self.tag2line[figure["object1"]]
                    else:
                        pass
                    if figure["object2"] in self.tag2line.keys():
                        o2 = self.tag2line[figure["object2"]]
                    else:
                        pass
                    crossing = self.Crossing(
                        self.tag2point[figure["point"]], o1, o2)
                    self.modules.append(crossing)
                    if not crossing.is_valid():
                        print("Invalid module crossing")

    def equations(self, vars):
        vars = list(vars)
        module_constraints = []
        tag2pxy = {}
        for tag in self.tag2point.keys():
            tag2pxy[tag] = (vars.pop(0), vars.pop(0))
        for m in self.modules:
            module_constraints.append(m.equation(tag2pxy))
        for _ in range(2*len(self.tag2point)-len(self.modules)):
            module_constraints.append(0.0)
        return module_constraints

    def validate(self, tag2pxy):
        for tag in self.tag2point.keys():
            x, y = tag2pxy[tag]
            self.tag2point[tag].x = x
            self.tag2point[tag].y = y
        for tag in self.tag2line.keys():
            p1tag = self.tag2line[tag].p1.tag
            p2tag = self.tag2line[tag].p2.tag
            self.tag2line[tag].p1 = self.tag2point[p1tag]
            self.tag2line[tag].p2 = self.tag2point[p2tag]
        for tag in self.tag2circle.keys():
            ptag = self.tag2circle[tag].p.tag
            self.tag2circle[tag].p = self.tag2point[ptag]
        for tag in self.tag2angle.keys():
            p1tag = self.tag2angle[tag].p1.tag
            p2tag = self.tag2angle[tag].p2.tag
            p3tag = self.tag2angle[tag].p3.tag
            self.tag2angle[tag].p1 = self.tag2point[p1tag]
            self.tag2angle[tag].p2 = self.tag2point[p2tag]
            self.tag2angle[tag].p3 = self.tag2point[p3tag]
        for i, m in enumerate(self.modules):
            if m.__class__.__name__ == "MidPoint":
                self.modules[i].p1 = self.tag2point[m.p1.tag]
                self.modules[i].p2 = self.tag2point[m.p2.tag]
                self.modules[i].p3 = self.tag2point[m.p3.tag]
            elif m.__class__.__name__ == "P2L":
                self.modules[i].p = self.tag2point[m.p.tag]
                self.modules[i].l = self.tag2line[m.l.tag]
            elif m.__class__.__name__ == "P2C":
                self.modules[i].p = self.tag2point[m.p.tag]
                self.modules[i].c = self.tag2circle[m.c.tag]
            elif m.__class__.__name__ == "L2C":
                self.modules[i].l = self.tag2line[m.l.tag]
                self.modules[i].c = self.tag2circle[m.c.tag]
            elif m.__class__.__name__ == "C2C":
                self.modules[i].c1 = self.tag2circle[m.c1.tag]
                self.modules[i].c2 = self.tag2circle[m.c2.tag]
            elif m.__class__.__name__ == "Parallel":
                self.modules[i].l1 = self.tag2line[m.l1.tag]
                self.modules[i].l2 = self.tag2line[m.l2.tag]
            elif m.__class__.__name__ == "Vertical":
                self.modules[i].l1 = self.tag2line[m.l1.tag]
                self.modules[i].l2 = self.tag2line[m.l2.tag]
            elif m.__class__.__name__ == "Isometry":
                self.modules[i].l1 = self.tag2line[m.l1.tag]
                self.modules[i].l2 = self.tag2line[m.l2.tag]
            elif m.__class__.__name__ == "Bisector":
                self.modules[i].a1 = self.tag2angle[m.a1.tag]
                self.modules[i].a2 = self.tag2angle[m.a2.tag]
            elif m.__class__.__name__ == "Crossing":
                self.modules[i].p = self.tag2point[m.p.tag]
                if m.o1.__class__.__name__ == "Line":
                    self.modules[i].o1 = self.tag2line[m.o1.tag]
                else:
                    # line and circle or circle and circle is not supported
                    pass
                if m.o2.__class__.__name__ == "Line":
                    self.modules[i].o2 = self.tag2line[m.o2.tag]
                else:
                    # line and circle or circle and circle is not supported
                    pass
        for l in self.tag2line.values():
            if not l.is_valid():
                print('invalid line')
                return False
        for c in self.tag2circle.values():
            if not c.is_valid():
                print('invalid circle')
                return False
        for m in self.modules:
            if not m.is_valid():
                print('invalid module:' + m.__class__.__name__)
                return False
        return True

    def solve(self, iteration=1000, threshold=1e-9):
        cnt = 0
        var_num = len(self.tag2point)*2
        best_solution = [0 for _ in range(var_num)]
        for _ in range(iteration):
            initial_guess = [random.uniform(-1.0, 1.0)
                             for _ in range(var_num)]
            solution = fsolve(self.equations, initial_guess)
            if sum([abs(r) for r in self.equations(solution)]) < threshold:
                cnt += 1
                best_solution = list(solution)
        if cnt > 0:
            print("solved_cnt:{}/{}".format(cnt, iteration))
            tag2pxy = {}
            for tag in self.tag2point.keys():
                tag2pxy[tag] = (best_solution.pop(0), best_solution.pop(0))
            return {"ok": True, "tag2pxy": tag2pxy}
        else:
            return {"ok": False}

    def check(self, tag2pxy):
        vars = []
        for x, y in tag2pxy.values():
            vars.append(x)
            vars.append(y)
        return self.equations(vars)

    class Object:
        def __init__(self, tag):
            self.tag = tag

        def __eq__(self, other):
            return self.tag == other.tag

        def is_valid(self):
            return True

    class Point(Object):
        def __init__(self, tag, x, y):
            super().__init__(tag)
            self.x = x
            self.y = y

        def is_valid(self):
            return True

    class Line(Object):
        def __init__(self, tag, p1, p2):
            super().__init__(tag)
            self.p1 = p1
            self.p2 = p2

        def is_valid(self):
            return self.p1 != self.p2

    class Circle(Object):
        def __init__(self, tag, p, r):
            super().__init__(tag)
            self.p = p
            self.r = r

        def is_valid(self):
            return self.r > 0

    class Angle(Object):
        def __init__(self, tag, p1, p2, p3):
            super().__init__(tag)
            self.p1 = p1
            self.p2 = p2
            self.p3 = p3

        def is_valid(self):
            return self.p1 != self.p2 and self.p1 != self.p3 and self.p2 != self.p3

    class MidPoint:
        def __init__(self, p1, p2, p3):
            self.p1 = p1
            self.p2 = p2
            self.p3 = p3

        def is_valid(self):
            return self.p1 != self.p2 and self.p1 != self.p3 and self.p2 != self.p3

        def equation(self, tag2pxy):
            x1, y1 = tag2pxy[self.p1.tag]
            x2, y2 = tag2pxy[self.p2.tag]
            x3, y3 = tag2pxy[self.p3.tag]
            return (x1+x2)-2*x3+(y1+y2)-2*y3

    class P2L:
        def __init__(self, p, l):
            self.p = p
            self.l = l

        def is_valid(self):
            p1x, p2x = self.l.p1.x, self.l.p2.x
            X = self.p.x
            if not (p1x <= X <= p2x or p2x <= X <= p1x):
                return False
            return self.p != self.l.p1 and self.p != self.l.p2

        def equation(self, tag2pxy):
            px, py = tag2pxy[self.p.tag]
            p1_x, p1_y = tag2pxy[self.l.p1.tag]
            p2_x, p2_y = tag2pxy[self.l.p2.tag]
            if p2_x-p1_x == 0:
                a = (p2_y-p1_y)/EPSILON
            else:
                a = (p2_y-p1_y)/(p2_x-p1_x)
            b = p1_y-a*p1_x
            return a * px + b - py

    class P2C:
        def __init__(self, p, c):
            self.p = p
            self.c = c

        def is_valid(self):
            return self.p != self.c.p

        def equation(self, tag2pxy):
            px, py = tag2pxy[self.p.tag]
            cx, cy = tag2pxy[self.c.p.tag]
            return (px-cx)**2 + (py-cy)**2 - self.c.r**2

    class L2C:
        def __init__(self, l, c):
            self.l = l
            self.c = c

        def is_valid(self):
            p1x, p1y = self.l.p1.x, self.l.p1.y
            p2x, p2y = self.l.p2.x, self.l.p2.y
            cx, cy = self.c.p.x, self.c.p.y
            l_a = (p2y-p1y)/(p2x-p1x)
            l_b = p1y-l_a*p1x
            X = (l_a*(l_b-cy)-cx)/(l_a**2+1)
            if not (p1x <= X <= p2x or p2x <= X <= p1x):
                return False
            if self.l.p1 == self.c.p or self.l.p2 == self.c.p:
                return False
            else:
                return True

        def equation(self, tag2pxy):
            l1x, l1y = tag2pxy[self.l.p1.tag]
            l2x, l2y = tag2pxy[self.l.p2.tag]
            cx, cy = tag2pxy[self.c.p.tag]
            return ((l1y-l2y)*(cx-l1x)+(l1x-l2x)*(cy-l1y))**2-(self.c.r**2)*((l1y-l2y)**2+(l1x-l2x)**2)

    class C2C:
        def __init__(self, c1, c2):
            self.c1 = c1
            self.c2 = c2

        def is_valid(self):
            return True

        def equation(self, tag2pxy):
            c1x, c1y = tag2pxy[self.c1.p.tag]
            c2x, c2y = tag2pxy[self.c2.p.tag]
            r1 = self.c1.r
            r2 = self.c2.r
            return ((c1x-c2x)**2+(c1y-c2y)**2)-(r1+r2)**2

    class Parallel:
        def __init__(self, l1, l2):
            self.l1 = l1
            self.l2 = l2

        def is_valid(self):
            return self.l1.tag != self.l2.tag

        def equation(self, tag2pxy):
            l1x1, l1y1 = tag2pxy[self.l1.p1.tag]
            l1x2, l1y2 = tag2pxy[self.l1.p2.tag]
            l2x1, l2y1 = tag2pxy[self.l2.p1.tag]
            l2x2, l2y2 = tag2pxy[self.l2.p2.tag]
            if l1x2-l1x1 == 0:
                a1 = (l1y2-l1y1)/EPSILON
            else:
                a1 = (l1y2-l1y1)/(l1x2-l1x1)
            if l2x2-l2x1 == 0:
                a2 = (l2y2-l2y1)/(EPSILON)
            else:
                a2 = (l2y2-l2y1)/(l2x2-l2x1)
            return a1-a2

    class Vertical:
        def __init__(self, l1, l2):
            self.l1 = l1
            self.l2 = l2

        def is_valid(self):
            return self.l1.tag != self.l2.tag

        def equation(self, tag2pxy):
            l1x1, l1y1 = tag2pxy[self.l1.p1.tag]
            l1x2, l1y2 = tag2pxy[self.l1.p2.tag]
            l2x1, l2y1 = tag2pxy[self.l2.p1.tag]
            l2x2, l2y2 = tag2pxy[self.l2.p2.tag]
            if l1x2-l1x1 == 0:
                a1 = (l1y2-l1y1)/EPSILON
            else:
                a1 = (l1y2-l1y1)/(l1x2-l1x1)
            if l2x2-l2x1 == 0:
                a2 = (l2y2-l2y1)/EPSILON
            else:
                a2 = (l2y2-l2y1)/(l2x2-l2x1)
            return a1*a2+1

    class Isometry:
        def __init__(self, l1, l2):
            self.l1 = l1
            self.l2 = l2

        def is_valid(self):
            return self.l1.tag != self.l2.tag

        def equation(self, tag2pxy):
            l1x1, l1y1 = tag2pxy[self.l1.p1.tag]
            l1x2, l1y2 = tag2pxy[self.l1.p2.tag]
            l2x1, l2y1 = tag2pxy[self.l2.p1.tag]
            l2x2, l2y2 = tag2pxy[self.l2.p2.tag]

            return (l1x2-l1x1)**2+(l1y2-l1y1)**2-(l2x2-l2x1)**2-(l2y2-l2y1)**2

    class Bisector:
        def __init__(self, a1, a2):
            self.a1 = a1
            self.a2 = a2

        def is_valid(self):
            return self.a1.tag != self.a2.tag

        def equation(self, tag2pxy):
            a1x1, a1y1 = tag2pxy[self.a1.p1.tag]
            a1x2, a1y2 = tag2pxy[self.a1.p2.tag]
            a1x3, a1y3 = tag2pxy[self.a1.p3.tag]
            a2x1, a2y1 = tag2pxy[self.a2.p1.tag]
            a2x2, a2y2 = tag2pxy[self.a2.p2.tag]
            a2x3, a2y3 = tag2pxy[self.a2.p3.tag]
            if a1x2-a1x1 == 0:
                l1 = (a1y2-a1y1)/EPSILON
            else:
                l1 = (a1y2-a1y1)/(a1x2-a1x1)
            if a1x3-a1x2 == 0:
                l2 = (a1y3-a1y2)/EPSILON
            else:
                l2 = (a1y3-a1y2)/(a1x3-a1x2)
            angle1 = abs(np.arctan(l1)-np.arctan(l2))
            if a2x2-a2x1 == 0:
                l1 = (a2y2-a2y1)/EPSILON
            else:
                l1 = (a2y2-a2y1)/(a2x2-a2x1)
            if a2x3-a2x2 == 0:
                l2 = (a2y3-a2y2)/EPSILON
            else:
                l2 = (a2y3-a2y2)/(a2x3-a2x2)
            angle2 = abs(np.arctan(l1)-np.arctan(l2))
            return angle1-angle2

    class Crossing:
        def __init__(self, p, o1, o2):
            self.p = p
            self.o1 = o1
            self.o2 = o2

        def is_valid(self):
            return self.o1.tag != self.o2.tag

        # 2直線上に点がある＆2直線が平行でない
        def equation(self, tag2pxy):
            px, py = tag2pxy[self.p.tag]
            o1_class = self.o1.__class__.__name__
            o2_class = self.o2.__class__.__name__
            if o1_class == "Line" and o2_class == "Line":
                o1p1x, o1p1y = tag2pxy[self.o1.p1.tag]
                o1p2x, o1p2y = tag2pxy[self.o1.p2.tag]
                o2p1x, o2p1y = tag2pxy[self.o2.p1.tag]
                o2p2x, o2p2y = tag2pxy[self.o2.p2.tag]
            else:
                # line and circle or circle and circle is not supported
                return
            if o1p1x-o1p2x == 0:
                a1 = (o1p1y-o1p2y)/EPSILON
            else:
                a1 = (o1p1y-o1p2y)/(o1p1x-o1p2x)
            if o2p1x-o2p2x == 0:
                a2 = (o2p1y-o2p2y)/EPSILON
            else:
                a2 = (o2p1y-o2p2y)/(o2p1x-o2p2x)
            b1 = o1p1y-a1*o1p1x
            b2 = o2p1y-a2*o2p1x
            if abs(a1-a2) < 0.0001:
                return 1
            return a1*px+b1-a2*px-b2


warnings.filterwarnings('ignore', 'The iteration is not making good progress')
warnings.filterwarnings(
    'ignore', 'The number of calls to function has reached maxfev')

if __name__ == '__main__':
    ITER = 1
    fname = "crossing.xml"
    print("--- OK ---")
    for f in os.scandir("./data/testcase/solver/ok"):
        if fname != f.name:
            continue
        tree = ET.parse(f.path)
        figures = xml2dict(tree.getroot())
        solver = Solver(figures)
        count = 0
        for i in range(ITER):
            geometry_solve_result = solver.solve()
            if geometry_solve_result["ok"]:
                count += 1
        if count == ITER:
            print("{}:pass({}/{})".format(f.name, count, ITER))
        else:
            print("{}:out({}/{})".format(f.name, count, ITER))

    print("--- NG ---")
    for f in os.scandir("./data/testcase/solver/ng"):
        tree = ET.parse(f.path)
        figures = xml2dict(tree.getroot())
        solver = Solver(figures)
        count = 0
        for i in range(ITER):
            geometry_solve_result = solver.solve()
            if geometry_solve_result["ok"]:
                count += 1
        if count == 0:
            print("{}:pass({}/{})".format(f.name, ITER-count, ITER))
        else:
            print("{}:out({}/{})".format(f.name, ITER-count, ITER))
