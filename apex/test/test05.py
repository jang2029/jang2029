import json
import os.path                          

data = {
    "Olivia" : {
        "gender": "female",
        "age" : 25,
        "hobby" : ["reading", "music"]
    },
    "Tyler" : {
        "gender": "male",
        "age" : 28,
        "hobby" : ["development", "painting"]
    }
}

file_path = "./test.json"

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent='\t')



# 기존 json 파일 읽어오기

with open(file_path, 'r') as file:
    data = json.load(file)

# 데이터 수정
data["Olivia"]["age"] = 26
data["Olivia"]["hobby"].append("take a picture")
data["Tyler"]["age"] = 29
data["Tyler"]["hobby"].append("travel")

# 기존 json 파일 덮어쓰기
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent='\t')