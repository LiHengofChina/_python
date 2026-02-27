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
# 手机号、身份证 正则规则
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
# 军官证
# ==============================

OFFICER_PATTERN = re.compile(r'^(军|海|空|武).{0,3}字第\d{5,8}号$')
DIGIT_MIDDLE_PATTERN = re.compile(r'字第(\d{5,8})号')

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
# 加载 邮编代码
# ==============================

import json

# 读取本地邮编 JSON
with open("zip_code/zip_code.txt", "r", encoding="utf-8") as f:
    zip_data = json.load(f)

zip_dict = set()

# 递归提取 postcode
def extract_postcodes(nodes):
    for node in nodes:
        if "postcode" in node and node["postcode"]:
            zip_dict.add(str(node["postcode"]).strip())

        if "children" in node and node["children"]:
            extract_postcodes(node["children"])

# 开始提取
extract_postcodes(zip_data)



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


# ==============================
# 年份正则
# ==============================

PERMIT_YEAR_PATTERN = re.compile(r'(19|20)\d{2}')

# ==============================
# 统一社会信用代码校验
# GB 32100-2015
# ==============================

CREDIT_CODE_MAP = {
    **{str(i): i for i in range(10)},
    **{c: i for i, c in enumerate("ABCDEFGHJKLMNPQRTUWXY", 10)}
}

CREDIT_CODE_CHARS = "0123456789ABCDEFGHJKLMNPQRTUWXY"
WEIGHTS = [1, 3, 9, 27, 19, 26, 16, 17,
           20, 29, 25, 13, 8, 24, 10, 30, 28]

def credit_code_check(code):
    if len(code) != 18:
        return False

    code = code.upper()

    # 检查非法字符
    for c in code:
        if c not in CREDIT_CODE_CHARS:
            return False

    total = 0
    for i in range(17):
        total += CREDIT_CODE_MAP[code[i]] * WEIGHTS[i]

    check_value = (31 - total % 31) % 31
    check_char = CREDIT_CODE_CHARS[check_value]

    return check_char == code[17]

# ==============================
# 省级简称字典
# ==============================
province_abbr_dict = {
    "京","津","沪","渝",
    "冀","晋","辽","吉","黑",
    "苏","浙","皖","闽","赣","鲁",
    "豫","鄂","湘","粤","桂","琼",
    "川","贵","云",
    "陕","甘","青",
    "蒙","宁","新","藏",
    "港","澳","台"
}

# ==============================
# （2）列级特征提取函数
# ==============================

def extract_column_features(text_list):

    cleaned = [str(t).strip() for t in text_list if pd.notnull(t)]

    if len(cleaned) == 0:
        return [0] * 28

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

    # 12 -> zip_dict_ratio
    zip_dict_match = sum(
        1 for t in cleaned
        if t in zip_dict
    )
    zip_dict_ratio = zip_dict_match / len(cleaned)

    # 13 证券代码字典匹配比例
    stock_dict_match = sum(
        1 for t in cleaned
        if t in stock_dict
    )
    stock_dict_ratio = stock_dict_match / len(cleaned)


    # 14 基金代码字典匹配比例
    fund_dict_match = sum(
        1 for t in cleaned
        if t in fund_dict
    )
    fund_dict_ratio = fund_dict_match / len(cleaned)

    # 15 长度 = 18 且 全为数字 + 大写字母 的比例
    credit_length_match = sum(
        1 for t in cleaned
        if len(t) == 18 and all(c in CREDIT_CODE_CHARS for c in t)
    )
    credit_length_match_ratio = credit_length_match / len(cleaned)
    # 16 第 3-8 位是纯数字的比例
    credit_region_digit_match = sum(
        1 for t in cleaned
        if len(t) == 18 and t[2:8].isdigit()
    )
    credit_region_digit_ratio = credit_region_digit_match / len(cleaned)

    # 17 行政区划 ID 就是 6 位数字：
    credit_region_dict_match = sum(
        1 for t in cleaned
        if len(t) == 18 and t[2:8] in region_dict
    )
    credit_region_dict_ratio = credit_region_dict_match / len(cleaned)

    # 18 实现统一社会信用代码校验算法
    credit_check_match = sum(
        1 for t in cleaned
        if credit_code_check(t)
    )
    credit_check_digit_ratio = credit_check_match / len(cleaned)

    # 19 -> 特殊汉字的比例
    officer_keyword_match = sum(
        1 for t in cleaned
        if any(k in t for k in ["军", "海", "空", "武", "字第", "号"])
    )
    officer_keyword_ratio = officer_keyword_match / len(cleaned)

    # 20 -> 军官格式正则
    officer_pattern_match = sum(
        1 for t in cleaned
        if OFFICER_PATTERN.match(t)
    )
    officer_pattern_ratio = officer_pattern_match / len(cleaned)

    # 21 -> 最后一个字 "号"
    officer_end_with_hao_match = sum(
        1 for t in cleaned
        if t.endswith("号")
    )
    officer_end_with_hao_ratio = officer_end_with_hao_match / len(cleaned)

    # 22 -> "字第" 和 "号" 之间一定是数字
    officer_digit_middle_match = sum(
        1 for t in cleaned
        if DIGIT_MIDDLE_PATTERN.search(t)
    )
    officer_digit_middle_ratio = officer_digit_middle_match / len(cleaned)

    # 23 → 特殊汉字比例（经营许可证）
    permit_keyword_match = sum(
        1 for t in cleaned
        if any(k in t for k in ["许可", "经营", "证", "监", "卫", "药", "械", "消"])
    )
    permit_keyword_ratio = permit_keyword_match / len(cleaned)

    # 24 → 包含年份数字
    permit_year_match = sum(
        1 for t in cleaned
        if PERMIT_YEAR_PATTERN.search(t)
    )
    permit_contains_year_ratio = permit_year_match / len(cleaned)

    # 25 → 偶尔出现括号 ()（）
    permit_parenthesis_match = sum(
        1 for t in cleaned
        if any(p in t for p in ["(", ")", "（", "）"])
    )
    permit_contains_parenthesis_ratio = permit_parenthesis_match / len(cleaned)

    # 26 → 偶尔出现横杠 -
    permit_dash_match = sum(
        1 for t in cleaned
        if "-" in t
    )
    permit_dash_structure_ratio = permit_dash_match / len(cleaned)

    # 27 → 包含一个省级简称
    permit_province_match = sum(
        1 for t in cleaned
        if any(abbr in t for abbr in province_abbr_dict)
    )
    permit_province_abbr_ratio = permit_province_match / len(cleaned)


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
        zip_dict_ratio,
        stock_dict_ratio,
        fund_dict_ratio,
        credit_length_match_ratio,
        credit_region_digit_ratio,
        credit_region_dict_ratio,
        credit_check_digit_ratio,
        officer_keyword_ratio,
        officer_pattern_ratio,
        officer_end_with_hao_ratio,
        officer_digit_middle_ratio,
        permit_keyword_ratio,
        permit_contains_year_ratio,
        permit_contains_parenthesis_ratio,
        permit_dash_structure_ratio,
        permit_province_abbr_ratio

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



# # 基金代码
# test_column = [
#     "000001",  # 华夏成长混合
#     "110011",  # 华夏成长混合
#     "519674",  # 华泰柏瑞沪深300ETF
#     "160119",  # 南方中证500ETF
#     "003095"   # 易方达消费行业ETF
# ]

# 统一社会信用代码
# test_column = [
#     "9144030071526726X",
#     "91310000631696382C",
#     "91110108MA01G90MXE",
#     "914401007594278192",
#     "91350100MA2D6J0A5X",
#     "91420500MA4KW8F67W",
#     "91440300MA5G21P972",
#     "91320594670131819W"
# ]

# 军官证
# test_column = [
#     "军字第2001988号",      # 正常军官证
#     "海字第123456号",      # 正常军官证
#     "空字第765432号",      # 正常军官证
#     "武字第112233号",      # 正常军官证
#     "军字第ABC123号",      # 中间不是纯数字（干扰）
#     "军第123456号",        # 少了“字”
#     "字第123456号",        # 少了前缀
#     "军字第12345号",       # 数字长度边界（5位）
#     "军字第123456789号",   # 数字过长（9位）
#     "军字第888888号X"      # 末尾多字符
# ]

#
test_column = [
    "粤食药监械经营许20180001号",       # 标准
    "苏B-2021-000123",               # 横杠结构
    "赣卫消证字(2019)第0012号",        # 括号 + 年份
    "经营许可证20200111号",            # 只有关键词+年份
    "许可证编号2022-000321",          # 年份+横杠
    "食药监械经营许20201111号",        # 无省简称
    "京食药监械经营许20230004号",       # 省简称+年份
    "许可2023第0099号",               # 简化结构
    "营业执照20200123",               # 噪音（非许可证）
    "1234567890"                     # 强噪音
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