"""
脱敏识别 —— 多分类（列级特征版本）
列级特征版本
随机森林
"""

import numpy as np
import pandas as pd
import re
import sklearn.model_selection as ms
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score

# ==============================
# （1）加载数据
# 必须包含 column_id,text,label
# ==============================

df = pd.read_csv("phone_id_data.csv", dtype={"text": str})

# print("原始数据前5行：")
# print(df.head())
# print("=" * 60)

# ==============================
# 正则规则
# ==============================
PHONE_REGEX = re.compile(r"^1[3-9]\d{9}$")
ID_REGEX = re.compile(r"^\d{17}[\dXx]$")

def valid_birth(id_number):
    try:
        birth = id_number[6:14]
        year = int(birth[0:4])
        month = int(birth[4:6])
        day = int(birth[6:8])
        #TODO 注意生日范围
        return 1300 <= year <= 2925 and 1 <= month <= 12 and 1 <= day <= 31
    except:
        return False

# ==============================
# Luhn 函数
# ==============================
def luhn_check(card_number):
    try:
        digits = [int(d) for d in card_number]
        checksum = 0
        reverse = digits[::-1]

        for i, d in enumerate(reverse):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d

        return checksum % 10 == 0
    except:
        return False

# ==============================
# 加载 证券和基金 代码 数据
# ==============================
# 读取本地字典
stock_df = pd.read_csv("stock_fund/stock_code_dict.csv", dtype=str)
fund_df = pd.read_csv("stock_fund/fund_code_dict.csv", dtype=str)

# 构建字典
stock_dict = set(stock_df["code"].astype(str))
fund_dict = set(fund_df["基金代码"].astype(str))


# ==============================
# （2）列级特征提取函数
# ==============================

def extract_column_features(text_list):

    cleaned = [str(t).strip() for t in text_list if pd.notnull(t)]

    if len(cleaned) == 0:
        return [0] * 15

    lengths = [len(t) for t in cleaned]

    # 0 avg_length
    avg_length = np.mean(lengths)

    # 1 fixed_length_flag
    fixed_length_flag = 1 if len(set(lengths)) == 1 else 0

    # 2 avg_digit_ratio
    digit_ratios = []
    for t in cleaned:
        digits = sum(c.isdigit() for c in t)
        digit_ratios.append(digits / len(t))
    avg_digit_ratio = np.mean(digit_ratios)

    # 3 phone_regex_ratio
    phone_match = sum(1 for t in cleaned if PHONE_REGEX.match(t))
    phone_regex_ratio = phone_match / len(cleaned)

    # 4 id_regex_ratio
    id_match = sum(1 for t in cleaned if ID_REGEX.match(t))
    id_regex_ratio = id_match / len(cleaned)

    # 5 id_contains_valid_birth_ratio
    birth_match = sum(
        1 for t in cleaned
        if ID_REGEX.match(t) and valid_birth(t)
    )
    id_contains_valid_birth_ratio = birth_match / len(cleaned)

    # 6 银行卡长度匹配比例（16-19位 + 全数字）
    bank_length_match = sum(
        1 for t in cleaned
        if 16 <= len(t) <= 19 and t.isdigit()
    )
    bank_length_match_ratio = bank_length_match / len(cleaned)

    # 7 Luhn通过比例
    bank_luhn_match = sum(
        1 for t in cleaned
        if 16 <= len(t) <= 19 and t.isdigit() and luhn_check(t)
    )
    bank_luhn_ratio = bank_luhn_match / len(cleaned)

    # 8 CVV 长度比例
    cvv_match = sum(
        1 for t in cleaned
        if len(t) == 3 and t.isdigit()
    )
    cvv_length_ratio = cvv_match / len(cleaned)

    # 9 统计 6 位纯数字占比。
    zip6_digit_match = sum(
        1 for t in cleaned
        if len(t) == 6 and t.isdigit()
    )
    zip6_digit_ratio = zip6_digit_match / len(cleaned)

    # 10 统计前两位是否“稳定”。
    prefixes = [t[:2] for t in cleaned if len(t) == 6 and t.isdigit()]
    if prefixes:
        prefix_unique_ratio = len(set(prefixes)) / len(prefixes)
    else:
        prefix_unique_ratio = 1
    # 11 统计以 00 或 000 结尾的比例。
    zip_zero_tail_match = sum(
        1 for t in cleaned
        if len(t) == 6 and t.isdigit() and (t.endswith("00") or t.endswith("000"))
    )
    zip_zero_tail_ratio = zip_zero_tail_match / len(cleaned)

    # 12 证券代码字典匹配比例
    stock_dict_match = sum(
        1 for t in cleaned
        if t in stock_dict
    )
    stock_dict_ratio = stock_dict_match / len(cleaned)

    # 13 基金代码字典匹配比例
    fund_dict_match = sum(
        1 for t in cleaned
        if t in fund_dict
    )
    fund_dict_ratio = fund_dict_match / len(cleaned)



    return [
        avg_length,
        fixed_length_flag,
        avg_digit_ratio,
        phone_regex_ratio,
        id_regex_ratio,
        id_contains_valid_birth_ratio,
        bank_length_match_ratio,
        bank_luhn_ratio,
        cvv_length_ratio,
        zip6_digit_ratio,
        prefix_unique_ratio,
        zip_zero_tail_ratio,
        stock_dict_ratio,
        fund_dict_ratio
    ]

# ==============================
# （3）构造列级训练数据
# ==============================

grouped = df.groupby("column_id") #按照 column_id 把数据分组

X = []
y = []

for column_id, group in grouped:
    texts = group["text"].tolist()
    label = group["label"].iloc[0]

    features = extract_column_features(texts)

    # print(f"{column_id} -> {features}")

    X.append(features)
    y.append(label)

X = np.array(X)
y = np.array(y)

# print("=" * 60)
# print("特征矩阵：")
# print(X)
# print("标签：")
# print(y)
# print("=" * 60)

# ==============================
# （4）划分训练 / 测试集
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y
)


# ==============================
# （5）构建随机森林模型
# ==============================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# ==============================
# （6）交叉验证
# ==============================

if len(X_train) >= 5:
    score = ms.cross_val_score(
        model,
        X_train,
        y_train,
        cv=4,
        scoring="f1_weighted"
    )

    print("交叉验证得分:", score)
    print("平均得分:", score.mean())
    print("-" * 50)

# ==============================
# （7）训练模型
# ==============================

model.fit(X_train, y_train)

print("特征重要性：")
print(model.feature_importances_)
print("=" * 60)

# ==============================
# （8）预测
# ==============================

pred = model.predict(X_test)

print("测试集真实值：", y_test)
print("测试集预测值：", pred)
print("=" * 60)

# ==============================
# （9）分类报告
# ==============================

print("分类报告：")
print(classification_report(y_test, pred))

# ==============================
#（9）F1得分
# ==============================
print("F1得分:", f1_score(y_test, pred, average="weighted"))
print("=" * 60)

# ==============================
# （10）手动测试整列
# ==============================


#手机号
# test_column = [
#     "13888888888",
#     "13999999999",
#     "+8613777777777",
#     "13666666666"
# ]
# #银行卡号
# test_column = [
#     "6222021234567893",
#     "6222021234567802",
#     "6222021234567810",
#     "6222021234567828",
#     "6222021234567836"
# ]
# 标准CVV列
# test_column = [
#     "123",
#     "456",
#     "789",
#     "321",
#     "654"
# ]

# 邮编
# test_column = [
#     "510000",
#     "510030",
#     "510100",
#     "510220",
#     "510300"
# ]

# # 股票代码
# test_column = [
#     "600000",  # 浦发银行
#     "600036",  # 招商银行
#     "600519",  # 贵州茅台
#     "601318",  # 中国平安
#     "601398",  # 工商银行
#     "603288",  # 海天味业
#     "603259",  # 药明康德
#     "605499"
# ]

# 基金代码
test_column = [
    "000001",  # 华夏成长混合
    "110011",  # 华夏成长混合
    "519674",  # 华泰柏瑞沪深300ETF
    "160119",  # 南方中证500ETF
    "003095"   # 易方达消费行业ETF
]
feature = np.array([extract_column_features(test_column)])

prediction = model.predict(feature)[0]
probability = model.predict_proba(feature)[0]

print("输入：", test_column)
print("预测类别:", prediction)

print("=" * 60)

print("置信度（每颗树的观点）：")
for cls, prob in zip(model.classes_, probability):
    print(f"  {cls} : {prob:.4f}")