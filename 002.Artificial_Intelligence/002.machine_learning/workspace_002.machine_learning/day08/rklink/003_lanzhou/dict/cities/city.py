import requests
import pandas as pd

# ==============================
# 下载中国城市 JSON 数据
# ==============================

url = "https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/cities.json"

resp = requests.get(url)
data = resp.json()

# ==============================
# 构建城市字典
# ==============================

city_list = []

for item in data:
    name = item.get("name")
    if name:
        city_list.append(name.strip())

# 加入去掉“市”的版本
city_list.extend(
    name.replace("市", "")
    for name in city_list
    if name.endswith("市")
)

# 去重
city_list = list(dict.fromkeys(city_list))

# 保存为 CSV
pd.DataFrame(city_list, columns=["city"]).to_csv(
    "city_dict.csv",
    index=False,
    encoding="utf-8"
)

print("城市数量:", len(city_list))