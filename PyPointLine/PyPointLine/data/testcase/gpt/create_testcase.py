import os
import json
from xml.etree import ElementTree as ET
from pprint import pprint

BASE_DIR = os.path.join(os.path.dirname(__file__), "")
mathematical_word_list = {
    "ひし形": "ひし形とは4本の辺の長さが全て等しい四角形である。",
    "三角形": "三角形とは同一直線上にない3点と、それらを結ぶ3つの線分からなる多角形。その3点を三角形の頂点、3つの線分を三角形の辺という。",
    "外接円": "多角形に外接する円（外接円）とは、その多角形の全ての頂点を通る円をいう。外接円の中心を外心といい、その半径を外接半径という。",
    "内接円": "多角形に内接する円（内接円）とは、その多角形の内部にあり全ての辺に接する—円を言う。内接円の中心を内心という。",
    "四角形": "四角形とは多角形の一種で、4つの頂点と4本の辺を持つ。",
    "正三角形": "正三角形とは正多角形である三角形である。つまり、3本の辺の長さが全て等しい三角形である。3つの内角の大きさが全て等しい三角形と定義してもよい。",
    "正方形": "正方形とは4つの辺の長さが全て等しく、かつ、4つの角の角度が全て等しい四角形のこと",
    "正六角形": "正六角形とは全ての辺の長さが等しく、全ての内角の大きさが等しい六角形である。",
    "台形": "台形とは四角形の一部で、少なくとも一組の対辺が互いに平行であるような図形である。平行な2本の対辺を台形の底辺といい、そのうち一方を上底、他方を下底とよぶ。また、もう一組の対辺を台形の脚とよぶ。",
    "長方形": "長方形（矩形）とは4つの角がすべて等しい四角形である。",
    "直角三角形": "2つの辺が直角をなす三角形である。記号⊿ を使って表すことがある。",
    "直角二等辺三角形": "直角二等辺三角形とは、二等辺三角形の持つ特徴に加え、直角三角形の持つ特徴を併せ持つ図形である。3つの角のうち2つの角がそれぞれ45°である三角形と定義してもよい。",
    "平行四辺形": "平行四辺形とは2組の対辺がそれぞれ平行である四角形のことである。",
    "六角形": "六角形とは6つの辺と頂点を持つ多角形の総称である。",
    "∠ABC": "∠ABCとは、点Bを頂点とし、線分BAと線分BCを辺とする角のことである。",
    "△ABC": "△ABCとは、点A、点B、点Cを頂点とする三角形のことである。",
    "⊿ABC": "⊿ABCとは、点A、点B、点Cを頂点とする直角三角形のことである。",
    "▱ABCD": "▱ABCDとは、点A、点B、点C、点Dを頂点とする平行四角形のことである。",
}
CATEGORY_LIST = ["word", "short", "problems"]
REPLACE_WORD_LIST = [{
    "_parallel_": "//",
}]


def convert_filename2text(text):
    text = text.split(".xml")[0]
    text = text.replace("_parallel_", "//")
    ZEN = "".join(chr(0xff01+i)for i in range(94))
    HAN = "".join(chr(0x21+i)for i in range(94))
    text = text.translate(str.maketrans(ZEN, HAN))
    return text


if __name__ == "__main__":
    testcases = []
    for category in CATEGORY_LIST:
        for f in os.scandir(os.path.join(BASE_DIR, category)):
            question_text = convert_filename2text(f.name)
            if category == "word":
                for word, word_addition in mathematical_word_list.items():
                    if word in question_text:
                        question_text = "{} {}".format(
                            question_text, word_addition)
            testcases.append({
                "question_text": question_text,
                "xmlfile_path": f.path
            })
    print(len(testcases))
    for t in testcases:
        print(t["question_text"])
    json_strs = []
    for tc in testcases:
        question_text = tc["question_text"]
        tree = ET.parse(tc["xmlfile_path"])
        root = tree.getroot()
        xml_str = ET.tostring(root, encoding="utf-8", method="xml")
        assistant_text = open(os.path.join(BASE_DIR, "prompt/assistant_xml.txt"),
                              "r", encoding="utf-8").read()
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": assistant_text
                },
                {
                    "role": "user",
                    "content": question_text
                },
                {
                    "role": "assistant",
                    "content": xml_str.decode("utf-8")
                }
            ]
        }
        json_strs.append(json.dumps(data, ensure_ascii=False))
    with open(os.path.join(BASE_DIR, "jsonl_testcase.jsonl"), "w", encoding="utf-8") as f:
        for json_str in json_strs:
            f.write(json_str + "\n")
