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


def rotation(x0: float, y0: float, x1: float, y1: float, theta: float):  # theta : clockwise radian
    mx = (x0+x1)*0.5
    my = (y0+y1)*0.5
    ax, ay = x0-mx, y0-my
    bx, by = math.cos(theta)*ax-math.sin(theta) * \
        ay, math.sin(theta)*ax+math.cos(theta)*ay
    return bx+mx, by+my, mx-bx, my-by

    pass


class XMLError(Enum):
    INCORRECT_REFID = "incorrect_refid"
    UNDEFINED_TAG = "undefined_tag"


def xml2dict(root) -> list[dict] | XMLError:
    figures = []
    id2tag = {}
    for data in root:
        attr = data.attrib
        name = None
        if data.find("name") is not None:
            name = data.find("name").text
        if data.tag == "point":
            id2tag[attr["id"]] = "tag_{}".format(len(figures))
            figures.append({
                "type": "point",
                "id": attr["id"],
                "tag": id2tag[attr["id"]],
                "x": 0,
                "y": 0,
                "name": name,
                "fixed": 0,
                "showName": 1,
                "active": 1
            })
    point_ids = [point["id"] for point in figures]
    for data in root:
        attr = data.attrib
        name = None
        if data.find("name") is not None:
            name = data.find("name").text
        # object
        if data.tag == "line-segment":
            point_id1, point_id2 = (
                attr["point-id1"], attr["point-id2"])
            id2tag[attr["id"]] = "tag_{}".format(len(figures))
            figures.append({
                "type": "line",
                "id": attr["id"],
                "tag": id2tag[attr["id"]],
                "name": name,
                "point1": id2tag[point_id1],
                "point2": id2tag[point_id2],
                "showLength": 0,
                "showName": 1,
                "fixedLength": 0,
                "active": 1
            })
        elif data.tag == "circle":
            center_point_id = None
            if "center-point-id" in attr:
                center_point_id = attr["center-point-id"]
                if center_point_id not in point_ids:
                    return XMLError.INCORRECT_REFID
            else:
                center_point_id = "cp_{}".format(len(figures))
                id2tag[center_point_id] = "tag_{}".format(len(figures))
                figures.append({
                    "type": "point",
                    "id": attr["id"],
                    "tag": id2tag[center_point_id],
                    "x": 0,
                    "y": 0,
                    "name": "",
                    "fixed": 0,
                    "showName": 1,
                    "active": 1
                })
            id2tag[attr["id"]] = "tag_{}".format(len(figures))
            figures.append(
                {
                    "type": "circle",
                    "id": attr["id"],
                    "point1": id2tag[center_point_id],
                    "radius": random_scale(a=0.5, b=1),
                    "tag": id2tag[attr["id"]],
                    "name": name,
                    "fixedRadius": 0,
                    "active": 1
                })
        else:
            pass

    line_ids = [fig["id"] for fig in figures if fig["type"] == "line"]
    circle_ids = [fig["id"] for fig in figures if fig["type"] == "circle"]
    # module
    for data in root:
        attr = data.attrib
        if data.tag == "middle-point":
            middle_point_id, point_id1, point_id2 = (
                attr["middle-point"], attr["point-id1"], attr["point-id2"])
            if not all((middle_point_id in point_ids, point_id1 in point_ids, point_id2 in point_ids)):
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "module",
                    "moduletype": "midpoint",
                    "tag": "tag_{}".format(len(figures)),
                    "p1": id2tag[point_id1],
                    "p2": id2tag[point_id2],
                    "p3": id2tag[middle_point_id],
                    "ratio1": 1,
                    "ratio2": 1,
                    "para1": 0.02,
                    "para2": 0.02,
                    "para3": 0.1
                }
            )
        elif data.tag == "point-on-line":
            point_id, line_id = (attr["point-id"], attr["line-id"])
            if point_id not in point_ids or line_id not in line_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "module",
                    "moduletype": "point2line",
                    "tag": "tag_{}".format(len(figures)),
                    "p1": id2tag[point_id],
                    "l1": id2tag[line_id],
                    "onlyOnSegment": 1,
                    "para1": 0.02
                }
            )
        elif data.tag == "point-on-circle":
            point_id, circle_id = (attr["point-id"], attr["circle-id"])
            if point_id not in point_ids or circle_id not in circle_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "module",
                    "moduletype": "point2circle",
                    "tag": "tag_{}".format(len(figures)),
                    "p1": id2tag[point_id],
                    "c1": id2tag[circle_id],
                    "para1": 0.1
                }
            )
        elif data.tag == "line-tangent-circle":
            line_id, circle_id = (attr["line-id"], attr["circle-id"])
            if line_id not in line_ids or circle_id not in circle_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "module",
                    "moduletype": "line2circle",
                    "tag": "tag_{}".format(len(figures)),
                    "ln": id2tag[line_id],
                    "cc": id2tag[circle_id],
                    "para1": 0.1
                }
            )
        elif data.tag == "circle-tangent-circle":
            circle_id1, circle_id2 = (attr["circle-id1"], attr["circle-id2"])
            if circle_id1 not in circle_ids or circle_id2 not in circle_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "module",
                    "moduletype": "circle2circle",
                    "tag": "tag_{}".format(len(figures)),
                    "cc1": id2tag[circle_id1],
                    "cc2": id2tag[circle_id2],
                    "para1": 0.1
                }
            )
        elif data.tag == "vertical":
            line_id1, line_id2 = (attr["line-id1"], attr["line-id2"])
            if line_id1 not in line_ids or line_id2 not in line_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "module",
                    "moduletype": "perpendicular",
                    "tag": "tag_{}".format(len(figures)),
                    "line1": id2tag[line_id1],
                    "line2": id2tag[line_id2],
                    "para1": 0.1
                }
            )
        elif data.tag == "parallel":
            line_id1, line_id2 = (attr["line-id1"], attr["line-id2"])
            if line_id1 not in line_ids or line_id2 not in line_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "module",
                    "moduletype": "parallel",
                    "tag": "tag_{}".format(len(figures)),
                    "line1": id2tag[line_id1],
                    "line2": id2tag[line_id2],
                    "para1": 0.1
                }
            )
        else:
            continue
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


def adjust_figure_location(figures):
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
