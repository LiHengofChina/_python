

# python -m pip install chinesename



##################################
# 加载中文姓氏字典
##################################

import json

with open("surname_dict.json", "r", encoding="utf-8") as f:
    surname_list = json.load(f)

surname_dict = set(surname_list)

print("姓氏字典数量:", len(surname_dict))
print("前20个:", surname_list[:20])

print("原始数量:", len(surname_list))
print("去重后数量:", len(surname_dict))