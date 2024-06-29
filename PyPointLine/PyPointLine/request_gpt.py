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
filepath = "./temp.xml"


def request_gpt(text, model=MODEL2, prev_output_xml=None):
    #     return """<figures>
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
    # </figures>""", "./test.xml"
    assistant_message = open("./assistant_xml.txt",
                             "r", encoding="utf-8").read()
    messages = [
        {
            "role": "system",       # ロール
            "content": assistant_message
        },
        {
            "role": "user",
            "content": text
        }
    ]
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
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(res)
    return res, filepath


if __name__ == "__main__":
    res, _ = request_gpt("三角形ABCがある")
    print(res)
