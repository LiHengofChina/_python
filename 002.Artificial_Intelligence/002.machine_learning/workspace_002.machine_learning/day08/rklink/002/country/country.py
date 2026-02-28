

# python -m pip install pycountry
# pip install pycountry babel

################################## 生成国家字典文件（干净版）
import pycountry
import pandas as pd
from babel import Locale

locale = Locale("zh")

country_list = []

for country in pycountry.countries:
    # 英文
    country_list.append(country.name.upper())
    country_list.append(country.alpha_2.upper())
    country_list.append(country.alpha_3.upper())

    # 中文（只取真实国家）
    name_cn = locale.territories.get(country.alpha_2)
    if name_cn and name_cn not in ["世界", "未知地区"]:
        country_list.append(name_cn.strip())

# 去重保持顺序
country_list = list(dict.fromkeys(country_list))

country_df = pd.DataFrame(country_list, columns=["country"])
country_df.to_csv("country_dict.csv", index=False, encoding="utf-8")

print("国家字典数量:", len(country_list))