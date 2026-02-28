



################################## 下载 数据集
# import akshare as ak
#
# # A股股票列表
# stock_df = ak.stock_info_a_code_name()
# stock_df.to_csv("stock_code_dict.csv", index=False, encoding="utf-8-sig")
#
# # 基金列表
# fund_df = ak.fund_name_em()
# fund_df.to_csv("fund_code_dict.csv", index=False, encoding="utf-8-sig")
#
# print("股票和基金代码已保存到本地 CSV 文件")


################################## 加载数据
import pandas as pd
# 读取本地字典
stock_df = pd.read_csv("stock_code_dict.csv", dtype=str)
fund_df = pd.read_csv("fund_code_dict.csv", dtype=str)

# 构建字典
stock_dict = set(stock_df["code"].astype(str))
fund_dict = set(fund_df["基金代码"].astype(str))

print("股票字典数量:", len(stock_dict))
print("基金字典数量:", len(fund_dict))


