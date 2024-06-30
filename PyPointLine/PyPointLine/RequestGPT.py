import openai
# jsonを読み込む
import json


with open("E://workspace/python/LLM/.secret/secret.json") as f:
    json_load = json.load(f)
    org_api_key = json_load["organization"]
    secret_key = json_load["secret_key"]
openai.organization = org_api_key
openai.api_key = secret_key


MODEL1 = "gpt-3.5-turbo"
MODEL2 = "ft:gpt-3.5-turbo-1106:personal::9Lu3oxB1"


class RequestGPT:
    def __init__(self, model=MODEL2, filepath="./temp.xml"):
        self.assistant_message = open("./assistant_xml.txt",
                                      "r", encoding="utf-8").read()
        self.model = model
        self.filepath = "./temp.xml"
        self.figures_history = [
            {
                "input": None,
                "output": """<?xml version='1.0' encoding='utf-8'?>
                            <figures />"""
            }
        ]
        self.now_index = 0
        self.prev_input = None
        self.prev_output = None
        # self.prev_input = "三角形ABCがある"
        # self.prev_output = """<figures>
        #     <point id="tag_0">
        #         <name>A</name>
        #     </point>
        #     <point id="tag_1">
        #         <name>B</name>
        #     </point>
        #     <point id="tag_2">
        #         <name>C</name>
        #     </point>
        #     <line-segment id="tag_3" point-id1="tag_0" point-id2="tag_1">
        #         <name>AB</name>
        #     </line-segment>
        #     <line-segment id="tag_4" point-id1="tag_2" point-id2="tag_1">
        #         <name>CB</name>
        #     </line-segment>
        #     <line-segment id="tag_5" point-id1="tag_0" point-id2="tag_2">
        #         <name>AC</name>
        #     </line-segment>
        # </figures>"""

    def request_gpt(self, text, interaction_mode, model=MODEL2, prev_output_xml=None):
        messages = [
            {
                "role": "system",       # ロール
                "content": self.assistant_message
            },
        ]
        if self.prev_input is not None and self.prev_output is not None and interaction_mode == True:
            messages.extend([
                {
                    "role": "user",
                    "content": self.prev_input
                },
                {
                    "role": "assistant",
                    "content": self.prev_output
                }
            ]
            )
        messages.append(
            {
                "role": "user",
                "content": text
            }
        )
        print(messages)
        completion = openai.ChatCompletion.create(
            model=model,     # モデルを選択
            messages=messages,
            max_tokens=2048,             # 生成する文章の最大単語数
            n=1,                # いくつの返答を生成するか
            stop=None,             # 指定した単語が出現した場合、文章生成を打ち切る
            temperature=0,              # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
            stream=False,            # 生成した回答を段階的に出力するか否か
        )
        res = completion["choices"][0].message.content
        # res = """<figures>
        #     <point id="tag_0">
        #         <name>A</name>
        #     </point>
        #     <point id="tag_1">
        #         <name>B</name>
        #     </point>
        #     <point id="tag_2">
        #         <name>C</name>
        #     </point>
        #     <line-segment id="tag_3" point-id1="tag_0" point-id2="tag_1">
        #         <name>AB</name>
        #     </line-segment>
        #     <line-segment id="tag_4" point-id1="tag_2" point-id2="tag_1">
        #         <name>CB</name>
        #     </line-segment>
        #     <line-segment id="tag_5" point-id1="tag_0" point-id2="tag_2">
        #         <name>AC</name>
        #     </line-segment>
        # </figures>"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(res)
        self.figures_history.append(
            {"input": text, "output": res}
        )
        self.now_index += 1
        self.prev_input = text
        self.prev_output = res
        return res, self.filepath

    def undo(self):
        if self.now_index == 0:
            return {
                "ok": False,
                "result": None
            }
        self.now_index -= 1
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(self.figures_history[self.now_index]["output"])
        return {
            "ok": True,
            "result": (self.figures_history[self.now_index]["output"], self.filepath)
        }

    def redo(self):
        if self.now_index == len(self.figures_history)-1:
            return {
                "ok": False,
                "result": None
            }
        self.now_index += 1
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(self.figures_history[self.now_index]["output"])
        return {
            "ok": True,
            "result": (self.figures_history[self.now_index]["output"], self.filepath)
        }


if __name__ == "__main__":
    rg = RequestGPT(model=MODEL2)
    res, _ = rg.request_gpt("三角形ABCがある", interaction_mode=False)
    print(res)
