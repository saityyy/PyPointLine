# flake8:noqa E741
import random
from scipy.optimize import fsolve


class Solver:
    def __init__(self, figures_list):
        self.tag2point = {}
        self.tag2line = {}
        self.tag2circle = {}
        self.modules = []
        for figure in figures_list:
            if figure["type"] == "point":
                point = self.Point(figure["tag"])
                self.tag2point[figure["tag"]] = point
            elif figure["type"] == "line":
                line = self.Line(figure["tag"],
                                 self.tag2point[figure["point1"]], self.tag2point[figure["point2"]])
                self.tag2line[figure["tag"]] = line
                if not line.is_valid():
                    print("Invalid line")
            elif figure["type"] == "circle":

                circle = self.Circle(figure["tag"],
                                     self.tag2point[figure["point"]], figure["r"])
                self.tag2circle[figure["tag"]] = circle
                if not circle.is_valid():
                    print("Invalid circle")
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
                    point = self.Point(figure["tag"])
                    self.tag2point[figure["tag"]] = point
                    l2c = self.L2C(
                        self.tag2line[figure["ln"]], self.tag2circle[figure["cc"]])
                    self.modules.append(l2c)
                    if not l2c.is_valid():
                        print("Invalid module l2c")

    def solve(self):
        initial_guess = [random.uniform(-10.0, 10.0)
                         for _ in range(len(self.tag2point)*2)]

        def equations(vars):
            vars = list(vars)
            module_constraints = []
            tag2pxy = {}
            for tag in self.tag2point.keys():
                tag2pxy[tag] = (vars.pop(0), vars.pop(0))
            for m in self.modules:
                module_constraints.append(m.equation(tag2pxy))
            for _ in range(2*len(self.tag2point)-len(self.modules)):
                module_constraints.append(0)
            return module_constraints
        solution = fsolve(equations, initial_guess)
        print(solution)
        print(list(equations(solution)))

    class Object:
        def __init__(self, tag):
            self.tag = tag

        def __eq__(self, other):
            return self.tag == other.tag

    class Point(Object):
        def __init__(self, tag):
            super().__init__(tag)

        def is_valid(self):
            return True

    class Line(Object):
        def __init__(self, tag, p1, p2):
            super().__init__(tag)
            self.p1 = p1
            self.p2 = p2

        def is_valid(self):
            return self.p1 != self.p2 and self.p1.x != self.p2.x

    class Circle(Object):
        def __init__(self, tag, p, r):
            super().__init__(tag)
            self.p = p
            self.r = r

        def is_valid(self):
            return self.r > 0

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
            return ((x1+x2)/2-x3)**2+((y1+y2)/2-y3)**2

    class P2L:
        def __init__(self, p, l):
            self.p = p
            self.l = l

        def is_valid(self):
            return self.p != self.l.p1 and self.p != self.l.p2

        def equation(self, tag2pxy):
            px, py = tag2pxy[self.p.tag]
            p1_x, p1_y = tag2pxy[self.l.p1.tag]
            p2_x, p2_y = tag2pxy[self.l.p2.tag]
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
            return self.l.p1 != self.c.p and self.l.p2 != self.c.p

        def equation(self, tag2pxy):
            def f():
                l1x, l1y = tag2pxy[self.l.p1.tag]
                l2x, l2y = tag2pxy[self.l.p2.tag]
                l_a = (l2y-l1y)/(l2x-l1x)
                l_b = l1y-l_a*l1x
                cx, cy = tag2pxy[self.c.p.tag]
                a = (l_a**2+1)
                b = 2*l_a*(l_b-cy)-2*cx
                c = cx**2+(l_b-cy)**2-self.c.r**2
                return b**2-4*a*c
            return f

    class C2C:
        def __init__(self, c1, c2):
            self.c1 = c1
            self.c2 = c2

        def is_valid(self):
            return True

        def equation(self, tag2pxy):
            def f():
                c1x, c1y = tag2pxy[self.c1.p.tag]
                c2x, c2y = tag2pxy[self.c2.p.tag]
                r1 = self.c1.r
                r2 = self.c2.r
                return ((c1x-c2x)**2+(c1y-c2y)**2)-(r1+r2)**2
            return f

    class Parallel:
        def __init__(self, l1, l2):
            self.l1 = l1
            self.l2 = l2

        def is_valid(self):
            return self.l1.tag != self.l2.tag

        def equation(self, tag2pxy):
            def f():
                l1x1, l1y1 = tag2pxy[self.l1.p1.tag]
                l1x2, l1y2 = tag2pxy[self.l1.p2.tag]
                l2x1, l2y1 = tag2pxy[self.l2.p1.tag]
                l2x2, l2y2 = tag2pxy[self.l2.p2.tag]
                a1 = (l1y2-l1y1)/(l1x2-l1x1)
                a2 = (l2y2-l2y1)/(l2x2-l2x1)
                return a1-a2
            return f

    class Vertical:
        def __init__(self, l1, l2):
            self.l1 = l1
            self.l2 = l2

        def is_valid(self):
            return self.l1.tag != self.l2.tag

        def equation(self, tag2pxy):
            def f():
                l1x1, l1y1 = tag2pxy[self.l1.p1.tag]
                l1x2, l1y2 = tag2pxy[self.l1.p2.tag]
                l2x1, l2y1 = tag2pxy[self.l2.p1.tag]
                l2x2, l2y2 = tag2pxy[self.l2.p2.tag]
                a1 = (l1y2-l1y1)/(l1x2-l1x1)
                a2 = (l2y2-l2y1)/(l2x2-l2x1)
                return a1*a2+1
            return f


if __name__ == '__main__':
    figures_list = [
        {"type": "point", "tag": "p1", "x": 1, "y": 2},
        {"type": "point", "tag": "p2", "x": 4, "y": 3},
        {"type": "point", "tag": "p3", "x": 4, "y": 3},
        {"type": "line", "tag": "l1", "point1": "p1", "point2": "p2"},
        {"type": "circle", "tag": "c1", "point": "p2", "r": 5},
        {"type": "module", "moduletype": "point2line", "p1": "p3", "l1": "l1"},
        {"type": "module", "moduletype": "point2circle", "p1": "p1", "c1": "c1"}
    ]
    figures_list2 = [
        {"type": "point", "tag": "p1"},
        {"type": "point", "tag": "p2"},
        {"type": "point", "tag": "p3"},
        {"type": "module", "moduletype": "midpoint",
            "p1": "p1", "p2": "p2", "p3": "p3"},
    ]
    solver = Solver(figures_list2)
    solver.solve()
