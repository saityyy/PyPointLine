import random
from xml.etree import ElementTree as ET
from enum import Enum
from pprint import pprint


class XMLError(Enum):
    INCORRECT_REFID = "incorrect_refid"
    UNDEFINED_TAG = "undefined_tag"


def openXmlFile(filePath):
    tree = ET.parse(filePath)
    root = tree.getroot()
    print(type(root))
    result = xml_checker(root)


def xml_checker(root) -> list[dict] | XMLError:
    figures = []
    for data in root:
        attr = data.attrib
        name = None
        if data.find("name") is not None:
            name = data.find("name").text
        if data.tag == "point":
            figures.append({
                "type": "point",
                "id": attr["id"],
                "name": name
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
            if not all((point_id1 in point_ids, point_id2 in point_ids)):
                return XMLError.INCORRECT_REFID
            figures.append({
                "type": "line",
                "id": attr["id"],
                "name": name,
                "x": 10*random.random(),
                "y": 10*random.random(),
                "point-id1": point_id1,
                "point-id2": point_id2,
                "fixed": 0,
                "showName": 1,
                "active": 1})
        elif data.tag == "circle":
            center_point_id = None
            if "center-point-id" in attr:
                center_point_id = attr["center-point-id"]
                if center_point_id not in point_ids:
                    return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "circle",
                    "id": attr["id"],
                    "name": name,
                    "center-point-id": center_point_id})
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
                    "type": "middle-point",
                    "middle-point": middle_point_id,
                    "point-id1": point_id1,
                    "point-id2": point_id2
                }
            )
        elif data.tag == "point-on-line":
            point_id, line_id = (attr["point-id"], attr["line-id"])
            if point_id not in point_ids or line_id not in line_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "point-on-line",
                    "point-id": point_id,
                    "line-id": line_id
                }
            )
        elif data.tag == "point-on-circle":
            point_id, circle_id = (attr["point-id"], attr["circle-id"])
            if point_id not in point_ids or circle_id not in circle_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "point-on-circle",
                    "point-id": point_id,
                    "circle-id": circle_id
                }
            )
        elif data.tag == "line-tangent-circle":
            point_id, line_id, circle_id = (
                attr["tangent-point-id"], attr["line-id"], attr["circle-id"])
            if point_id not in point_ids or line_id not in line_ids or circle_id not in circle_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "line-tangent-circle",
                    "tangent-point-id": point_id,
                    "line-id": line_id,
                    "circle-id": circle_id
                }
            )
        elif data.tag == "vertical":
            line_id1, line_id2 = (attr["line-id1"], attr["line-id2"])
            if line_id1 not in line_ids or line_id2 not in line_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "vertical",
                    "line-id1": line_id1,
                    "line-id2": line_id2
                }
            )
        elif data.tag == "parallel":
            line_id1, line_id2 = (attr["line-id1"], attr["line-id2"])
            if line_id1 not in line_ids or line_id2 not in line_ids:
                return XMLError.INCORRECT_REFID
            figures.append(
                {
                    "type": "parallel",
                    "line-id1": line_id1,
                    "line-id2": line_id2
                }
            )
        else:
            continue
    pprint(figures)
    return figures


if __name__ == '__main__':
    openXmlFile('./xml/sample.xml')
