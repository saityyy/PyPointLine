#
#
#
from collections import defaultdict
from enum import Enum
import math
import random


class mousePosition:
    x = 0  # world
    y = 0  # world
    bpX = 0  # buttonPressedX
    bpY = 0  # buttonPressedY
    canvasX = 0
    canvasY = 0
    magneticPoint = None


def isNear(x0, y0, x1, y1, d):
    x, y = x0-x1, y0-y1
    if x*x+y*y < d*d:
        return True
    return False


def isIn(x, y, left, top, width, height):
    if left < x and x < left+width:
        if top < y and y < top+height:
            return True
    return False


def magnitude(x, y):
    return math.sqrt(x*x+y*y)


def dist(x0, y0, x1, y1):
    return magnitude(x0-x1, y0-y1)


def draw_grid_lines(app, point, line):
    # グリッド線
    return
    for i in [-10, 0, 10]:
        _l = line(app, point(app, i, -10), point(app, i, 10))
        _l.name = "axis"
        app.logs.append(_l)
    for i in [-10, 0, 10]:
        _l = line(app, point(app, -10, i), point(app, 10, i))
        _l.name = "axis"
        app.logs.append(_l)


def rotation(x0: float, y0: float, x1: float, y1: float, theta: float):  # theta : clockwise radian
    mx = (x0+x1)*0.5
    my = (y0+y1)*0.5
    ax, ay = x0-mx, y0-my
    bx, by = math.cos(theta)*ax-math.sin(theta) * \
        ay, math.sin(theta)*ax+math.cos(theta)*ay
    return bx+mx, by+my, mx-bx, my-by

    pass


def xml2dict(root):
    figures = []
    id2tag = {}
    xmltag_order = ["point", "straight-line", "line-segment", "circle", "angle", "middle-point", "point-on-line", "point-on-circle",
                    "line-tangent-circle", "circle-tangent-circle", "vertical", "parallel",
                    "horizontal", "isometry", "bisector", "crossing"]
    sorted_xml_elements = sorted(root, key=lambda x: xmltag_order.index(x.tag))
    exist_object_ids = {"point": [],
                        "line": [], "circle": [], "angle": []}
    for data in sorted_xml_elements:
        attr = data.attrib
        serial_num = len(figures)+1
        if data.tag == "point":
            id2tag[attr["id"]] = "tag_{}".format(serial_num)
            x, y = map(float, attr["position"].split(","))
            figures.append({
                "type": "point",
                "id": attr["id"],
                "tag": id2tag[attr["id"]],
                "x": x,
                "y": y,
                "name": attr["name"],
                "fixed": 0,
                "showName": 1,
                "active": 1
            })
            exist_object_ids["point"].append(attr["id"])
        elif data.tag == "line-segment" or data.tag == "straight-line":
            if attr.get("point-id1") not in exist_object_ids["point"]:
                raise Exception(
                    f"xmlerror: incorrect_refid in {data.tag} tag.(not exist {attr.get('point-id1')})")
            if attr.get("point-id2") not in exist_object_ids["point"]:
                raise Exception(
                    f"xmlerror: incorrect_refid in {data.tag} tag.(not exist {attr.get('point-id2')})")
            id2tag[attr["id"]] = "tag_{}".format(serial_num)
            pt1_tag = id2tag[attr["point-id1"]]
            pt2_tag = id2tag[attr["point-id2"]]
            figures.append({
                "type": "line",
                "id": attr["id"],
                "tag": id2tag[attr["id"]],
                "name": attr["name"],
                "point1": pt1_tag,
                "point2": pt2_tag,
                "showName": 1,
                "showLength": 1 if attr.get("length") is not None else 0,
                "fixedLength": 1 if attr.get("length") is not None else 0,
                "length": attr.get("length"),
                "active": 1
            })
            if data.tag == "straight-line":
                for i in range(len(figures)):
                    ftag = figures[i]["tag"]
                    if ftag == pt1_tag or ftag == pt2_tag:
                        figures[i]["showName"] = 0

            exist_object_ids["line"].append(attr["id"])
        elif data.tag == "circle":
            if attr.get("center-point-id") not in exist_object_ids["point"]:
                raise Exception("xmlerror: incorrect_refid")
            id2tag[attr["id"]] = "tag_{}".format(serial_num)
            figures.append(
                {
                    "type": "circle",
                    "id": attr["id"],
                    "point1": id2tag[attr["center-point-id"]],
                    "radius": attr["radius"],
                    "tag": id2tag[attr["id"]],
                    "name": attr["name"],
                    "fixedRadius": 0,
                    "active": 1
                })
            exist_object_ids["circle"].append(attr["id"])
        elif data.tag == "angle":
            if attr.get("point-id1") not in exist_object_ids["point"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("point-id2") not in exist_object_ids["point"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("point-id3") not in exist_object_ids["point"]:
                raise Exception("xmlerror: incorrect_refid")
            id2tag[attr["id"]] = "tag_{}".format(serial_num)
            figures.append({
                "type": "angle",
                "id": attr["id"],
                "tag": id2tag[attr["id"]],
                "name": attr["name"],
                "point1": id2tag[attr["point-id1"]],
                "point2": id2tag[attr["point-id2"]],
                "point3": id2tag[attr["point-id3"]],
                "showArc": 1,
                "showValue": 1,
                "fixValue": 1 if attr.get("value") is not None else 0,
                "value": attr.get("value"),
                "active": 1
            })
            exist_object_ids["angle"].append(attr["id"])
        elif data.tag == "middle-point":
            if attr.get("middle-point-id") not in exist_object_ids["point"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("point-id1") not in exist_object_ids["point"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("point-id2") not in exist_object_ids["point"]:
                raise Exception("xmlerror: incorrect_refid")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "midpoint",
                    "tag": "tag_{}".format(serial_num),
                    "p1": id2tag[attr["point-id1"]],
                    "p2": id2tag[attr["point-id2"]],
                    "p3": id2tag[attr["middle-point-id"]],
                    "ratio1": 1,
                    "ratio2": 1,
                    "para1": 0.02,
                    "para2": 0.02,
                    "para3": 0.1
                }
            )
        elif data.tag == "point-on-line":
            if attr.get("point-id") not in exist_object_ids["point"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("line-id") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "point2line",
                    "tag": "tag_{}".format(serial_num),
                    "p1": id2tag[attr["point-id"]],
                    "l1": id2tag[attr["line-id"]],
                    "onlyOnSegment": 1,
                    "para1": 0.02
                }
            )
        elif data.tag == "point-on-circle":
            if attr.get("point-id") not in exist_object_ids["point"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("circle-id") not in exist_object_ids["circle"]:
                raise Exception("xmlerror: incorrect_refid")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "point2circle",
                    "tag": "tag_{}".format(serial_num),
                    "p1": id2tag[attr["point-id"]],
                    "c1": id2tag[attr["circle-id"]],
                    "para1": 0.1
                }
            )
        elif data.tag == "line-tangent-circle":
            if attr.get("line-id") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("circle-id") not in exist_object_ids["circle"]:
                raise Exception("xmlerror: incorrect_refid")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "line2circle",
                    "tag": "tag_{}".format(serial_num),
                    "ln": id2tag[attr["line-id"]],
                    "cc": id2tag[attr["circle-id"]],
                    "para1": 0.1
                }
            )
        elif data.tag == "circle-tangent-circle":
            if attr.get("circle-id1") not in exist_object_ids["circle"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("circle-id2") not in exist_object_ids["circle"]:
                raise Exception("xmlerror: incorrect_refid")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "circle2circle",
                    "tag": "tag_{}".format(serial_num),
                    "cc1": id2tag[attr["circle-id1"]],
                    "cc2": id2tag[attr["circle-id2"]],
                    "para1": 0.1
                }
            )
        elif data.tag == "vertical":
            if attr.get("line-id1") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("line-id2") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "perpendicular",
                    "tag": "tag_{}".format(serial_num),
                    "line1": id2tag[attr["line-id1"]],
                    "line2": id2tag[attr["line-id2"]],
                    "para1": 0.1
                }
            )
        elif data.tag == "parallel":
            if attr.get("line-id1") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("line-id2") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "parallel",
                    "tag": "tag_{}".format(serial_num),
                    "line1": id2tag[attr["line-id1"]],
                    "line2": id2tag[attr["line-id2"]],
                    "para1": 0.1
                }
            )
        elif data.tag == "horizontal":
            if attr.get("line-id") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "horizontal",
                    "tag": "tag_{}".format(serial_num),
                    "line1": id2tag[attr["line-id"]],
                    "para1": 0.1
                }
            )
        elif data.tag == "isometry":
            if attr.get("line-id1") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("line-id2") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            ratio1, ratio2 = attr["ratio"].split(":")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "isometry",
                    "tag": "tag_{}".format(serial_num),
                    "line1": id2tag[attr["line-id1"]],
                    "line2": id2tag[attr["line-id2"]],
                    "ratio1": ratio1,
                    "ratio2": ratio2,
                    "fixedRatio": 1,
                    "para1": 0.25
                }
            )
        elif data.tag == "bisector":
            if attr.get("angle-id1") not in exist_object_ids["angle"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("angle-id2") not in exist_object_ids["angle"]:
                raise Exception("xmlerror: incorrect_refid")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "bisector",
                    "tag": "tag_{}".format(serial_num),
                    "angle1": id2tag[attr["angle-id1"]],
                    "angle2": id2tag[attr["angle-id2"]],
                    "para1": 0.1
                }
            )
        elif data.tag == "crossing":
            if attr.get("point-id") not in exist_object_ids["point"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("object-id1") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            if attr.get("object-id2") not in exist_object_ids["line"]:
                raise Exception("xmlerror: incorrect_refid")
            figures.append(
                {
                    "type": "module",
                    "moduletype": "crossing",
                    "tag": "tag_{}".format(serial_num),
                    "point": id2tag[attr["point-id"]],
                    "object1": id2tag[attr["object-id1"]],
                    "object2": id2tag[attr["object-id2"]],
                    "para1": 0.1
                }
            )
        else:
            raise Exception("xmlerror: undefined_tag")
    return figures


def random_scale(a=-2.0, b=2.0):
    return random.uniform(a, b)


def locate_polygon_vertex(number_of_vertex: int,
                          center: tuple[float, float] = (0.0, 0.0),
                          radius: float = 2.0,
                          random_variation: float = 1.0) -> list[tuple[float, float]]:
    vertices = []
    for i in range(number_of_vertex):
        angle = 2*math.pi/number_of_vertex*i
        x = center[0] + radius*math.cos(angle)+random_variation*random.random()
        y = center[1] + radius*math.sin(angle)+random_variation*random.random()
        vertices.append((x, y))
    return vertices


def adjust_figure_location(figures, tag2pxy):
    for tag, (x, y) in tag2pxy.items():
        for i, fig in enumerate(figures):
            if fig["tag"] == tag:
                figures[i]["x"], figures[i]["y"] = x, y
                print(tag, figures[i]['x'], figures[i]['y'])
    return figures
    graph = defaultdict(list)
    points_ids = []
    tag2pointname = {}
    tag2point_index = {}
    for i, fig in enumerate(figures):
        if fig["type"] == "line":
            p1, p2 = fig["point1"], fig["point2"]
            points_ids.append(p1)
            points_ids.append(p2)
        if fig["type"] == "point":
            tag2pointname[fig["tag"]] = fig["name"]
            tag2point_index[fig["tag"]] = i
    points_ids = list(set(points_ids))
    for fig in figures:
        if fig["type"] == "line":
            p1, p2 = (points_ids.index(fig["point1"]),
                      points_ids.index(fig["point2"]))
            graph[p1].append(p2)
            graph[p2].append(p1)

    # Step 2: Find cycles (polygons)
    cycles = find_all_cycles(graph, len(points_ids))
    checked_points = set()
    for point_id in points_ids:
        if point_id in checked_points:
            continue
        max_len_cycle = []
        for cycle in cycles:
            # print([tag2pointname[points_ids[point]] for point in cycle])
            if len(cycle) > len(max_len_cycle) and point_id in [points_ids[point] for point in cycle]:
                max_len_cycle = cycle
        # print([tag2pointname[points_ids[point]] for point in max_len_cycle])
        polygon_vertex_coodinates = locate_polygon_vertex(
            len(max_len_cycle), center=(random_scale(), random_scale()),
            radius=random_scale(a=1.0, b=2.0), random_variation=0.5)
        for pid, (x, y) in zip(max_len_cycle, polygon_vertex_coodinates):
            point_tag = points_ids[pid]
            figures[tag2point_index[point_tag]]["x"] = x
            figures[tag2point_index[point_tag]]["y"] = y
            checked_points.add(pid)
    return figures


def find_all_cycles(graph, N):
    def dfs(node, start, path, visited):
        visited[node] = True
        path.append(node)
        for neighbor in graph[node]:
            if not visited[neighbor]:
                if dfs(neighbor, start, path, visited):
                    return True
            elif neighbor == start and len(path) > 2:
                cycles.append(path[:])
        path.pop()
        visited[node] = False
        return False

    cycles = []
    visited = [False] * N
    for start in range(N):
        path = []
        dfs(start, start, path, visited)

    return cycles
