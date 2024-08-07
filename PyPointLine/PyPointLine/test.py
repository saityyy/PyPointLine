import os
from xml.etree import ElementTree as ET
from fileIO import xml2dict

for f in os.scandir("./data/testcase/gpt"):
    print(f.path)
    tree = ET.parse(f.path)
    figures = xml2dict(tree.getroot())
