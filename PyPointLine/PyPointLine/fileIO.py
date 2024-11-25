# import cv2
from pprint import pprint
import xml.etree.ElementTree as ET
from Solver import Solver
from object import point, line, circle, xxxxx
from module import *
from utils import xml2dict, draw_grid_lines


class fileIO:
    def __init__(self, app):
        self.app = app
        pass

    def openFile(self, app, filePath):
        ext = filePath[-3:]
        if ext == "txt" or ext == "TXT":
            self.openTxtFile(app, filePath)
        elif ext == "xml" or ext == "XML":
            self.openXmlFile(app, filePath)
        elif ext == "png" or ext == "PNG":
            self.openImageFile(app, filePath)
        pass

    def saveFile(self, app, filePath):
        ext = filePath[-3:]
        if ext == "txt" or ext == "TXT":
            self.saveTxtFile(app, filePath)
        elif ext == "tex" or ext == "TEX":
            self.saveTexFile(app, filePath)
        elif ext == "png" or ext == "PNG":
            self.saveImageFile(app, filePath)
        elif ext == "xml" or ext == "XML":
            self.saveXmlFile(app, filePath)
        pass

    def openTxtFile(self, app, filePath):
        f = open(filePath, 'r')
        datalist = f.readlines()
        app.nextID = 0
        # clear app.logs and destroy all objects on app.
        app.logs.clear()
        newXXXXX = xxxxx(app)
        app.logs.append(newXXXXX)
        for data in datalist:
            texts = data.split(',')
            if len(texts) == 0:
                continue
            dic = {}
            for text in texts:
                items = text.split('=')
                dic[items[0]] = items[1]
            self.dict2pointline(app, dic)
        # app.nextID
        app.getNextID()
        pass

    def openXmlFile(self, app, filePath):
        tree = ET.parse(filePath)
        app.nextID = 0
        # clear app.logs and destroy all objects on app.
        app.logs.clear()
        newXXXXX = xxxxx(app)
        app.logs.append(newXXXXX)
        figures = xml2dict(tree.getroot())
        for dic in figures:
            self.dict2pointline(app, dic)
        # app.nextID
        app.getNextID()
        # app.calculatorEvaluate()
        draw_grid_lines(app, point, line)
        pass

    def dict2pointline(self, app, dic):
        if "tag" not in dic.keys():
            return
        if dic['type'] == 'point':
            x = float(dic['x'])
            y = float(dic['y'])
            newPoint = point(app, x, y)
            newPoint.tag = dic['tag']
            newPoint.name = dic['name']
            newPoint.fixed = bool(int(dic['fixed']))
            if newPoint.fixed:
                newPoint.fixedX = x
                newPoint.fixedY = y
            newPoint.showName = bool(int(dic['showName']))
            newPoint.active = bool(int(dic['active']))
            app.logs.append(newPoint)
        elif dic['type'] == 'line':
            point1 = app.findObjectByTag(dic['point1'])
            point2 = app.findObjectByTag(dic['point2'])
            if point1 == None or point2 == None:
                return
            newLine = line(app, point1, point2)
            newLine.tag = dic['tag']
            newLine.name = dic['name']
            newLine.showLength = bool(int(dic['showLength']))
            newLine.showName = bool(int(dic['showName']))
            newLine.fixedLength = bool(int(dic['fixedLength']))
            newLine.active = bool(int(dic['active']))
            if newLine.fixedLength:
                newLine.length = float(dic['length'])
            app.logs.append(newLine)
        elif dic['type'] == 'circle':
            point1 = app.findObjectByTag(dic['point1'])
            radius = float(dic['radius'])
            if point == None:
                return
            newCircle = circle(app, point1, radius)
            newCircle.tag = dic['tag']
            newCircle.name = dic['name']
            newCircle.fixedRadius = bool(int(dic['fixedRadius']))
            newCircle.active = bool(int(dic['active']))
            app.logs.append(newCircle)
        elif dic['type'] == 'angle':
            point1 = app.findObjectByTag(dic['point1'])
            point2 = app.findObjectByTag(dic['point2'])
            point3 = app.findObjectByTag(dic['point3'])
            if point1 == None or point2 == None or point3 == None:
                return
            newAngle = angle(app, point1, point2, point3)
            newAngle.tag = dic['tag']
            newAngle.name = dic['name']
            newAngle.showArc = bool(int(dic['showArc']))
            newAngle.showValue = bool(int(dic['showValue']))
            newAngle.fixValue = bool(int(dic['fixValue']))
            newAngle.active = bool(int(dic['active']))
            if bool(int(dic['fixValue'])):
                newAngle.value = float(dic['value'])
            app.logs.append(newAngle)

        elif dic['type'] == 'module':
            if dic['moduletype'] == 'midpoint':
                point1 = app.findObjectByTag(dic['p1'])
                point2 = app.findObjectByTag(dic['p2'])
                point3 = app.findObjectByTag(dic['p3'])
                if point1 == None or point2 == None or point3 == None:
                    return
                newModule = midpoint(app, point1, point2, point3)
                newModule.ratio1 = int(dic['ratio1'])
                newModule.ratio2 = int(dic['ratio2'])
                newModule.para1 = float(dic['para1'])
                newModule.para2 = float(dic['para2'])
                newModule.para3 = float(dic['para3'])
                app.logs.append(newModule)
            elif dic['moduletype'] == 'point2point':
                point1 = app.findObjectByTag(dic['p1'])
                point2 = app.findObjectByTag(dic['p2'])
                if point1 == None or point2 == None:
                    return
                newModule = point2point(app, point1, point2)
                newModule.para1 = float(dic['para1'])
                newModule.para2 = float(dic['para2'])
                app.logs.append(newModule)
            elif dic['moduletype'] == 'point2line':
                point1 = app.findObjectByTag(dic['p1'])
                line1 = app.findObjectByTag(dic['l1'])
                newModule = point2line(app, point1, line1)
                newModule.onlyOnSegment = bool(int(dic['onlyOnSegment']))
                newModule.para1 = float(dic['para1'])
                app.logs.append(newModule)
            elif dic['moduletype'] == 'point2circle':
                point1 = app.findObjectByTag(dic['p1'])
                circle1 = app.findObjectByTag(dic['c1'])
                newModule = point2circle(app, point1, circle1)
                newModule.para1 = float(dic['para1'])
                app.logs.append(newModule)
            elif dic['moduletype'] == 'line2circle':
                line1 = app.findObjectByTag(dic['ln'])
                circle1 = app.findObjectByTag(dic['cc'])
                newModule = line2circle(app, line1, circle1)
                newModule.para1 = float(dic['para1'])
                app.logs.append(newModule)
            elif dic['moduletype'] == 'circle2circle':
                circle1 = app.findObjectByTag(dic['cc1'])
                circle2 = app.findObjectByTag(dic['cc2'])
                newModule = circle2circle(app, circle1, circle2)
                newModule.para1 = float(dic['para1'])
                app.logs.append(newModule)
            elif dic['moduletype'] == 'isometry':
                line1 = app.findObjectByTag(dic['line1'])
                line2 = app.findObjectByTag(dic['line2'])
                newModule = isometry(app, line1, line2)
                newModule.ratio1 = int(dic['ratio1'])
                newModule.ratio2 = int(dic['ratio2'])
                newModule.fixedRatio = bool(int(dic['fixedRatio']))
                newModule.para1 = float(dic['para1'])
                app.logs.append(newModule)
            elif dic['moduletype'] == 'bisector':
                angle1 = app.findObjectByTag(dic['angle1'])
                angle2 = app.findObjectByTag(dic['angle2'])
                newModule = bisector(app, angle1, angle2)
                newModule.para1 = float(dic['para1'])
                app.logs.append(newModule)
            elif dic['moduletype'] == 'parallel':
                line1 = app.findObjectByTag(dic['line1'])
                line2 = app.findObjectByTag(dic['line2'])
                newModule = parallel(app, line1, line2)
                newModule.para1 = float(dic['para1'])
                app.logs.append(newModule)
            elif dic['moduletype'] == 'perpendicular':
                line1 = app.findObjectByTag(dic['line1'])
                line2 = app.findObjectByTag(dic['line2'])
                newModule = perpendicular(app, line1, line2)
                newModule.para1 = float(dic['para1'])
                app.logs.append(newModule)
            elif dic['moduletype'] == 'horizontal':
                line1 = app.findObjectByTag(dic['line1'])
                newModule = horizontal(app, line1)
                newModule.para1 = float(dic['para1'])
                app.logs.append(newModule)
            elif dic['moduletype'] == "crossing":
                point0 = app.findObjectByTag(dic['point'])
                object1 = app.findObjectByTag(dic['object1'])
                object2 = app.findObjectByTag(dic['object2'])
                newModule = crossing(app, point0, object1, object2)
                app.logs.append(newModule)

    def saveTxtFile(self, app, filePath):
        f = open(filePath, 'w')
        for obj in app.logs[1:]:
            f.write("%s\n" % (obj.toString()))
        f.close()

    def saveTexFile(self, app, filePath):
        f = open(filePath, 'w')
        f.write("\\documentclass[10pt,dvipdfmx]{article}\n")
        f.write("\\usepackage{pgf,tikz}\n")
        f.write("\\usepackage{mathrsfs}\n")
        f.write("\\pagestyle{empty}\n")
        f.write("\\begin{document}\n")
        f.write(
            "\\begin{tikzpicture}[line cap=round,line join=round,x=1.0cm,y=1.0cm]\n")
        f.write("\\clip(%f, %f) rectangle (%f, %f);\n" %
                (app.left, app.bottom, app.right, app.top))
        for obj in app.logs:
            if obj.thisis != "module":
                f.write("%s\n" % (obj.toTeXString()))
        f.write("\\end{tikzpicture}")
        f.write("\\end{document}")
        f.close()
        pass

    def saveImageFile(self, app, filePath):
        app.mainCanvas.postscript(file=filePath, colormode='color')
        pass

    def openImageFile(self, app, filePath):
        # im0 = cv2.imread(self.filename)
        # width, height, x = im0.shape
        ##

        ##
        pass

    def saveXmlFile(self, app, filePath):
        root = ET.Element("figures")
        class_order = ["point", "line", "circle", "angle", "midpoint", "point2line", "point2circle", "line2circle",
                       "circle2circle", "isometry", "bisector", "parallel", "perpendicular", "horizontal", "crossing"]

        app_elements = sorted(
            app.logs[1:], key=lambda el: class_order.index(el.__class__.__name__))
        for obj in app_elements:
            if obj.name == "axis":
                continue
            obj.toXMLElement(root)
        tag2short_id = {}
        reference_id_attr = ["point-id", "point-id1", "point-id2", "point-id3",
                             "line-id", "line-id1", "line-id2", "center-point-id", "middle-point-id", "circle-id",
                             "circle-id1", "circle-id2", "angle-id1", "angle-id2",
                             "object-id1", "object-id2"]
        # idを連番で１から割り振り直す
        for i, element in enumerate(root, start=1):
            for attr in element.attrib:
                attr_value = element.attrib[attr]
                if attr == "id":
                    tag2short_id[attr_value] = str(i)
                    element.attrib["id"] = str(i)
        # idを参照している属性を書き換える
        for element in root:
            for attr in element.attrib:
                if attr in reference_id_attr:
                    attr_value = element.attrib[attr]
                    element.attrib[attr] = tag2short_id[attr_value]

        tree = ET.ElementTree(root)
        tree.write(filePath, encoding='utf-8', xml_declaration=True)
