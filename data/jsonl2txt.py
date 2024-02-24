import json


data_list = []

jsonl_path="MedChatZH_valid.jsonl" #本地的jsonl格式的路径
txt_path="data.txt" #本地知识库路径

# 打开jsonl文件，读取每一行数据
with open(jsonl_path, "r",encoding="utf-8") as jsonl_file:
    # 遍历每一行数据
    for line in jsonl_file:
        # 将每一行数据转换为字典对象
        data_dict = json.loads(line)
        # 提取instruction和output字段
        instruction = data_dict["instruction"]
        output = data_dict["output"]
        # 将字典对象添加到列表中
        data_list.append(instruction+output)
        #data_list.append(output)

# 打开txt文件，写入数据
with open(txt_path, "w",encoding="utf-8") as txt_file:
    # 遍历列表中的每个字典对象
    for data_dict in data_list:
        # 将字典对象转换为字符串
        data_str = str(data_dict)
        # 将字符串写入txt文件，并换行
        txt_file.write(data_str + "\n")