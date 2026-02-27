
# https://gitcode.com/Premium-Resources/dd955/blob/main/%E5%85%A8%E5%9B%BD%E9%82%AE%E7%BC%96%E5%A4%A7%E5%85%A8json%E6%A0%BC%E5%BC%8F.txt


import json

# ==============================
# 读取本地邮编 JSON
# ==============================

with open("zip_code.txt", "r", encoding="utf-8") as f:
    zip_data = json.load(f)

zip_dict = set()

# ==============================
# 递归提取 postcode
# ==============================

def extract_postcodes(nodes):
    for node in nodes:
        if "postcode" in node and node["postcode"]:
            zip_dict.add(str(node["postcode"]).strip())

        if "children" in node and node["children"]:
            extract_postcodes(node["children"])

# 开始提取
extract_postcodes(zip_data)

print("邮编字典数量:", len(zip_dict))


# ==============================
# 构建 行政区划代码 字典（6位 ID）
# ==============================

region_dict = set()

def extract_region_ids(nodes):
    for node in nodes:
        # ID 是行政区划代码
        if "ID" in node and node["ID"]:
            region_id = str(node["ID"]).strip()
            if len(region_id) == 6 and region_id.isdigit():
                region_dict.add(region_id)

        if "children" in node and node["children"]:
            extract_region_ids(node["children"])

# 开始提取
extract_region_ids(zip_data)

print("行政区划字典数量:", len(region_dict))
