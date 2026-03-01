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

df = pd.read_csv("fit_data.csv", dtype={"text": str})

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
        return 1949 <= year <= 2049 and 1 <= month <= 12 and 1 <= day <= 31
    except:
        return False
# ==============================
# 军官证
# ==============================

OFFICER_PATTERN = re.compile(r'^(军|海|空|武).{0,3}字第\d{5,8}号$')
DIGIT_MIDDLE_PATTERN = re.compile(r'字第(\d{5,8})号')


# ==============================
# 构建地址门牌结构单位字典
# ==============================

ADDRESS_NUMBER_PATTERN = re.compile(
    r"\d{1,5}(号|栋|单元|室|楼|层)"
)


# ==============================
# MAC
# ==============================
MAC_REGEX = re.compile(
    r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$|^[0-9A-Fa-f]{12}$'
)


# ==============================
# 构建地址行政区划关键词字典
# ==============================

address_region_keyword_dict = set([
    "省", "市", "区", "县",
    "镇", "乡", "街道",
    "开发区", "新区",
    "自治州"
])


# ==============================
# 构建地址道路关键词字典（完整版）
# ==============================

address_road_keyword_dict = set([

    # ===== 基础道路 =====
    "路", "街", "大道", "巷", "胡同", "弄", "里",
    "段", "号", "桥", "线",

    # ===== 主干道路 =====
    "快速路", "高速", "高速公路",
    "国道", "省道", "县道", "乡道",
    "环路", "环线", "中路", "东路", "西路", "南路", "北路",

    # ===== 城市扩展结构 =====
    "大街", "小路", "支路",
    "步行街", "商业街",
    "内环", "外环",

    # ===== 行政街道 =====
    "街道", "街道办事处",

    # ===== 园区类 =====
    "开发区", "工业园", "科技园",
    "产业园", "创业园", "物流园",
    "软件园", "园区",

    # ===== 商业建筑 =====
    "广场", "大厦", "中心", "写字楼",
    "商务楼", "办公楼",

    # ===== 住宅楼栋 =====
    "栋", "单元", "室", "楼", "层",
    "座", "幢", "号楼",

    # ===== 乡村结构 =====
    "村", "社区", "新区",

    # ===== 交通节点 =====
    "站", "出口", "入口", "收费站"
])


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
# 构建基金名称字典
# ==============================

fund_name_dict = set(
    fund_df["基金简称"].astype(str).str.strip()
)

# ==============================
# 构建中国城市字典
# ==============================

city_df = pd.read_csv("cities/city_dict.csv", dtype=str)

city_dict = set(
    city_df["city"].astype(str).str.strip()
)

# ==============================
# 构建中文姓氏字典
# ==============================

import json

with open("chinesename/surname_dict.json", "r", encoding="utf-8") as f:
    surname_list = json.load(f)

surname_dict = set(
    s.strip()
    for s in surname_list
    if isinstance(s, str) and s.strip()
)


# ==============================
# 构建企业名称关键词字典
# ==============================

enterprise_keyword_dict = set([
    "有限公司",
    "股份有限公司",
    "集团",
    "控股",
    "科技",
    "实业",
    "投资",
    "银行",
    "公司",
    "责任",
    "合伙",
    "有限合伙"
])

# ==============================
# 构建企业名称后缀字典
# ==============================

enterprise_suffix_dict = set([
    "有限公司",
    "股份有限公司",
    "集团有限公司",
    "集团",
    "公司",
    "有限责任公司",
    "责任公司",
    "有限合伙",
    "合伙企业",
    "银行",
    "研究院",
    "事务所",
    "基金会",
    "中心",
    "工作室"
])

# ==============================
# PASSPORT 护照正则
# ==============================

PASSPORT_REGEX = re.compile(r'^[A-Z]{1,2}\d{7,8}$')

# ==============================
# 基金名称关键词
# ==============================

FUND_KEYWORDS = [
    "基金", "混合", "灵活", "债券",
    "可转债", "纯债", "增强债",
    "成长", "一级", "二级", "股票"
]


# ==============================
# 加载 国家 字典 数据
# ==============================

# 读取本地字典
country_df = pd.read_csv("country/country_dict.csv", dtype=str)

# 构建字典（统一去空格）
country_dict = set(
    country_df["country"].astype(str).str.strip().str.upper()
)


print("国家字典数量:", len(country_dict))


# ==============================
# 拼音结构
# ==============================


def is_reasonable_pinyin(text):
    text = text.strip()

    if not re.fullmatch(r"[A-Za-z ]+", text):
        return False

    pure = text.replace(" ", "")

    # 允许大小写混合，但必须全部是字母
    return pure.isalpha()


# ==============================
# IP正则
# ==============================

IPV4_REGEX = re.compile(
    r'^((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}'
    r'(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$'
)

IPV6_REGEX = re.compile(
    r'^('
    r'([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|'
    r'([0-9a-fA-F]{1,4}:){1,7}:|'
    r'([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|'
    r'([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|'
    r'([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|'
    r'([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|'
    r'([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|'
    r'[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|'
    r':((:[0-9a-fA-F]{1,4}){1,7}|:)'
    r')$'
)

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
# 身份证 校验方法
# ==============================

ID_WEIGHTS = [
    7, 9, 10, 5, 8, 4, 2,
    1, 6, 3, 7, 9, 10,
    5, 8, 4, 2
]

ID_CHECK_MAP = {
    0: "1", 1: "0", 2: "X", 3: "9", 4: "8",
    5: "7", 6: "6", 7: "5", 8: "4", 9: "3", 10: "2"
}

def id_card_check(id_number):
    if not re.match(r"^\d{17}[\dXx]$", id_number):
        return False

    id_number = id_number.upper()

    total = 0
    for i in range(17):
        total += int(id_number[i]) * ID_WEIGHTS[i]

    remainder = total % 11
    return ID_CHECK_MAP[remainder] == id_number[17]



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
# URL 正则
# ==============================
URL_REGEX = re.compile(
    r'^(https?|ftp)://'
    r'([A-Za-z0-9\-\.]+)'
    r'(:\d+)?'
    r'(/[\w\-\.~:/?#\[\]@!$&\'()*+,;=%]*)?$'
)

DOMAIN_REGEX = re.compile(
    r'^(?:https?://)?'      # 可选 scheme
    r'(?:www\.)?'           # 可选 www
    r'([A-Za-z0-9-]+\.)+'   # 至少一个子域
    r'[A-Za-z]{2,}'         # 顶级域
)

# ==============================
# EMAIL 正则
# ==============================

EMAIL_REGEX = re.compile(
    r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
)



# ==============================
# VIN 结构正则（17位，排除 I O Q）
# ==============================
VIN_REGEX = re.compile(r'^[A-HJ-NPR-Z0-9]{17}$')


# ==============================
# VIN 校验位函数（第 9 位）
# ==============================
VIN_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10,
               0,
               9, 8, 7, 6, 5, 4, 3, 2]

VIN_TRANS = {
    **{str(i): i for i in range(10)},
    **dict(zip("ABCDEFGHJKLMNPRSTUVWXYZ",
               [1,2,3,4,5,6,7,8,9,
                1,2,3,4,5,7,8,9]))
}

def vin_check_digit_valid(vin):
    if not VIN_REGEX.match(vin):
        return False

    total = 0
    for i, c in enumerate(vin):
        value = VIN_TRANS.get(c, None)
        if value is None:
            return False
        total += value * VIN_WEIGHTS[i]

    remainder = total % 11
    check_char = 'X' if remainder == 10 else str(remainder)

    return vin[8] == check_char


# ==============================
# 车牌号正则
# ==============================

# 普通汽车牌照（7位）：省简称 + 1字母 + 5位（字母/数字） + 1位（字母/数字）
# 排除 I O（实际规则里常排除，先不做极致严格）
PLATE_NORMAL_REGEX = re.compile(r'^[京津沪渝冀晋辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云陕甘青蒙宁新藏港澳台][A-Z][A-Z0-9]{5}$')

# 新能源（8位）简化版：
# 小型新能源：省简称 + 字母 + D/F + 1位字母数字 + 4位数字
# 大型新能源：省简称 + 字母 + 5位数字 + D/F
PLATE_NEW_ENERGY_REGEX = re.compile(
    r'(^[京津沪渝冀晋辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云陕甘青蒙宁新藏港澳台][A-Z][DF][A-Z0-9]\d{4}$)|'
    r'(^[京津沪渝冀晋辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云陕甘青蒙宁新藏港澳台][A-Z]\d{5}[DF]$)'
)


# ==============================
# 中征码 校验函数（mod97）
# ==============================

CHAR_CODE_REGEX = re.compile(r'^[A-Z0-9]{3}\d{13}$')

# 55 → character_check_digit_ratio（校验位合法比例）
def char_numeric_value(ch: str) -> int:
    ch = ch.upper()
    if ch.isdigit():
        return int(ch)
    if "A" <= ch <= "Z":
        return ord(ch) - ord("A") + 10
    return -1  # 非法字符

def character_code_check(code: str) -> bool:
    code = code.strip().upper()

    # 必须满足结构：3位[A-Z0-9] + 13位数字（总16位）
    if not CHAR_CODE_REGEX.fullmatch(code):
        return False

    weight_factor = [1, 3, 5, 7, 11, 2, 13, 1, 1, 17, 19, 97, 23, 29]

    total = 0
    # 前14位参与计算（索引 0..13），与 Java 逻辑一致
    for i in range(14):
        v = char_numeric_value(code[i])
        if v < 0:
            return False
        total += v * weight_factor[i]

    reissue = total % 97 + 1
    verify = f"{reissue:02d}"
    return code[-2:] == verify

# ==============================
# 日期
# ==============================
DATE_REGEX = re.compile(
    r'^(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|\d{8})$'
)
from datetime import datetime

def valid_date(text):
    try:
        if "-" in text:
            datetime.strptime(text, "%Y-%m-%d")
        elif "/" in text:
            datetime.strptime(text, "%Y/%m/%d")
        elif "." in text:
            datetime.strptime(text, "%Y.%m.%d")
        elif len(text) == 8:
            datetime.strptime(text, "%Y%m%d")
        else:
            return False
        return True
    except:
        return False
# ==============================
# 日期-时间
# ==============================

DATE_TIME_REGEX = re.compile(
    r'^('
    r'\d{4}[-/.]\d{1,2}[-/.]\d{1,2}[ T]\d{1,2}:\d{1,2}(:\d{1,2})?'
    r'|\d{14}'
    r')$'
)
from datetime import datetime

def valid_datetime(text):
    try:
        if "-" in text or "/" in text or "." in text:
            if "T" in text:
                datetime.strptime(text, "%Y-%m-%dT%H:%M:%S")
            elif " " in text:
                try:
                    datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
                except:
                    datetime.strptime(text, "%Y-%m-%d %H:%M")
            else:
                return False
        elif len(text) == 14:
            datetime.strptime(text, "%Y%m%d%H%M%S")
        else:
            return False
        return True
    except:
        return False

# ==============================
# 开启许可
# ==============================
ACCOUNT_OPENING_REGEX = re.compile(r'^[A-Z]\d{14}$')


# ==============================
# （2）列级特征提取函数
# ==============================

def extract_column_features(text_list):

    cleaned = [str(t).strip() for t in text_list if pd.notnull(t)]

    if len(cleaned) == 0:
        return [0] * 104

    lengths = [len(t) for t in cleaned]

    # ==============================
    # （1）PHONE
    # ==============================
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

    # ==============================
    # （2）ID_CARD
    # ==============================
    # 4 id_regex_ratio
    id_match = sum(1 for t in cleaned if ID_REGEX.match(t))
    id_regex_ratio = id_match / len(cleaned)

    # 5 生日验证
    birth_valid_ratio = sum(
        1 for t in cleaned
        if len(t) >= 14 and t[6:14].isdigit() and valid_birth(t)
    ) / len(cleaned)

    # 6 身份证校验
    id_check_match = sum(
        1 for t in cleaned
        if id_card_check(t)
    )
    id_check_ratio = id_check_match / len(cleaned)

    # 7 → 身份证前 6 位在行政区划字典中的比例
    region_prefix_ratio = sum(
        1 for t in cleaned
        if len(t) >= 6 and t[:6].isdigit() and t[:6] in region_dict
    ) / len(cleaned)

    # ==============================
    # （3）BANK_CARD
    # ==============================
    # 8 银行卡长度匹配比例（16-19位 + 全数字）
    bank_length_match = sum(
        1 for t in cleaned
        if 16 <= len(t) <= 19 and t.isdigit()
    )
    bank_length_match_ratio = bank_length_match / len(cleaned)

    # 9 Luhn通过比例
    bank_luhn_match = sum(
        1 for t in cleaned
        if 16 <= len(t) <= 19 and t.isdigit() and luhn_check(t)
    )
    bank_luhn_ratio = bank_luhn_match / len(cleaned)

    # ==============================
    # （4）CVV
    # ==============================
    # 10 CVV 长度比例
    cvv_match = sum(
        1 for t in cleaned
        if len(t) == 3 and t.isdigit()
    )
    cvv_length_ratio = cvv_match / len(cleaned)

    # ==============================
    # （5）ZIP_CODE
    # ==============================
    # 11 统计 6 位纯数字占比。
    zip6_digit_match = sum(
        1 for t in cleaned
        if len(t) == 6 and t.isdigit()
    )
    zip6_digit_ratio = zip6_digit_match / len(cleaned)

    # 12 统计前两位是否“稳定”。
    prefixes = [t[:2] for t in cleaned if len(t) == 6 and t.isdigit()]

    if prefixes:
        prefix_stability_ratio = 1 if len(set(prefixes)) == 1 else 0
    else:
        prefix_stability_ratio = 0
    # 13 统计以 00 或 000 结尾的比例。
    zip_zero_tail_match = sum(
        1 for t in cleaned
        if len(t) == 6 and t.isdigit() and (t.endswith("00") or t.endswith("000"))
    )
    zip_zero_tail_ratio = zip_zero_tail_match / len(cleaned)

    # 14 -> zip_dict_ratio
    zip_dict_match = sum(
        1 for t in cleaned
        if t in zip_dict
    )
    zip_dict_ratio = zip_dict_match / len(cleaned)

    # ==============================
    # （6）STOCK_CODE
    # ==============================
    # 15 证券代码字典匹配比例
    stock_dict_match = sum(
        1 for t in cleaned
        if t in stock_dict
    )
    stock_dict_ratio = stock_dict_match / len(cleaned)

    # ==============================
    # （7）FUND_CODE
    # ==============================

    # 16 基金代码字典匹配比例
    fund_dict_match = sum(
        1 for t in cleaned
        if t in fund_dict
    )
    fund_dict_ratio = fund_dict_match / len(cleaned)

    # ==============================
    # （8）CREDIT_CODE 统一社会信用代码
    # ==============================
    # 17 长度 = 18 且 全为数字 + 大写字母 的比例
    credit_length_match = sum(
        1 for t in cleaned
        if len(t) == 18 and all(c in CREDIT_CODE_CHARS for c in t)
    )
    credit_length_match_ratio = credit_length_match / len(cleaned)
    # 18 第 3-8 位是纯数字的比例
    credit_region_digit_match = sum(
        1 for t in cleaned
        if len(t) == 18 and t[2:8].isdigit()
    )
    credit_region_digit_ratio = credit_region_digit_match / len(cleaned)

    # 19 行政区划 ID 就是 6 位数字：
    credit_region_dict_match = sum(
        1 for t in cleaned
        if len(t) == 18 and t[2:8].isdigit() and t[2:8] in region_dict
    )
    credit_region_dict_ratio = credit_region_dict_match / len(cleaned)

    # 20 实现统一社会信用代码校验算法
    credit_check_match = sum(
        1 for t in cleaned
        if credit_code_check(t)
    )
    credit_check_digit_ratio = credit_check_match / len(cleaned)

    # ==============================
    # （9）OFFICER_CARD 军官证
    # ==============================
    # 21 -> 特殊汉字的比例
    officer_keyword_match = sum(
        1 for t in cleaned
        if any(k in t for k in ["军", "海", "空", "武", "字第", "号"])
    )
    officer_keyword_ratio = officer_keyword_match / len(cleaned)

    # 22 -> 军官格式正则
    officer_pattern_match = sum(
        1 for t in cleaned
        if OFFICER_PATTERN.match(t)
    )
    officer_pattern_ratio = officer_pattern_match / len(cleaned)

    # 23 -> 最后一个字 "号"
    officer_end_with_hao_match = sum(
        1 for t in cleaned
        if t.endswith("号")
    )
    officer_end_with_hao_ratio = officer_end_with_hao_match / len(cleaned)

    # 24 -> "字第" 和 "号" 之间一定是数字
    officer_digit_middle_match = sum(
        1 for t in cleaned
        if DIGIT_MIDDLE_PATTERN.search(t)
    )
    officer_digit_middle_ratio = officer_digit_middle_match / len(cleaned)

    # ==============================
    # （10）PERMIT
    # ==============================
    # 25 → 特殊汉字比例（经营许可证）
    permit_keyword_match = sum(
        1 for t in cleaned
        if any(k in t for k in ["许可", "经营", "证", "监", "卫", "药", "械", "消"])
    )
    permit_keyword_ratio = permit_keyword_match / len(cleaned)

    permit_no_di_ratio = sum(
        1 for t in cleaned
        if "第" not in t
    ) / len(cleaned)

    permit_xu_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in ["许可", "许可证", "经营许可", "生产许可"])
    ) / len(cleaned)

    # 26 → 包含年份数字
    permit_year_match = sum(
        1 for t in cleaned
        if PERMIT_YEAR_PATTERN.search(t)
    )
    permit_contains_year_ratio = permit_year_match / len(cleaned)

    # 27 → 偶尔出现括号 ()（）
    permit_parenthesis_match = sum(
        1 for t in cleaned
        if any(p in t for p in ["(", ")", "（", "）"])
    )
    permit_contains_parenthesis_ratio = permit_parenthesis_match / len(cleaned)

    # 28 → 偶尔出现横杠 -
    permit_dash_match = sum(
        1 for t in cleaned
        if "-" in t
    )
    permit_dash_structure_ratio = permit_dash_match / len(cleaned)

    # 29 → 包含一个省级简称
    permit_province_match = sum(
        1 for t in cleaned
        if any(abbr in t for abbr in province_abbr_dict)
    )
    permit_province_abbr_ratio = permit_province_match / len(cleaned)

    # 30 → 不包含“第”的比例（排他特征：区分 OFFICER_CARD）
    permit_no_di_ratio = sum(
        1 for t in cleaned
        if "第" not in t
    ) / len(cleaned)

    # 31 → 许可证关键词命中比例（强语义特征）
    # 长关键词放前面，避免被“许可”提前覆盖（但 any() 本身不影响结果，只是语义更清晰）
    permit_xu_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in ["经营许可证", "生产许可证", "许可证", "许可"])
    ) / len(cleaned)


    # ==============================
    # （11）CAR_DRIVING_LICENSE
    # ==============================
    # 30 → 长度为 18 的比例
    driving_length_18_match = sum(
        1 for t in cleaned
        if len(t) == 18
    )
    driving_length_18_ratio = driving_length_18_match / len(cleaned)

    # 31 → 整列纯数字比例
    driving_all_digit_match = sum(
        1 for t in cleaned
        if t.isdigit()
    )
    driving_all_digit_ratio = driving_all_digit_match / len(cleaned)

    # ==============================
    # （12）IP
    # ==============================
    # 32 IPv4 正则匹配比例
    ipv4_regex_ratio = sum(
        1 for t in cleaned
        if IPV4_REGEX.match(t)
    ) / len(cleaned)

    # 33 IPv4 含 3 个点的比例
    ipv4_dot_ratio = sum(
        1 for t in cleaned
        if t.count('.') == 3
    ) / len(cleaned)

    # 34 IPv6 正则匹配比例
    ipv6_regex_ratio = sum(
        1 for t in cleaned
        if IPV6_REGEX.match(t)
    ) / len(cleaned)

    # ==============================
    # （13）MAC
    # ==============================
    # 35 → MAC 正则匹配比例
    # 35 → mac_regex_ratio（严格正则匹配比例）
    mac_regex_ratio = sum(
        1 for t in cleaned
        if MAC_REGEX.match(t)
    ) / len(cleaned)

    # 36 → mac_colon_format_ratio（冒号分隔格式比例）
    mac_colon_format_ratio = sum(
        1 for t in cleaned
        if re.fullmatch(r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', t)
    ) / len(cleaned)

    # 37 → mac_dash_format_ratio（短横线分隔格式比例）
    mac_dash_format_ratio = sum(
        1 for t in cleaned
        if re.fullmatch(r'([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}', t)
    ) / len(cleaned)

    # 38 → mac_plain_hex_12_ratio（纯 12 位十六进制比例）
    mac_plain_hex_12_ratio = sum(
        1 for t in cleaned
        if re.fullmatch(r'[0-9A-Fa-f]{12}', t)
    ) / len(cleaned)

    mac_strict_format_ratio = sum(
        1 for t in cleaned
        if re.fullmatch(r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', t)
    ) / len(cleaned)

    # 含有5个冒号占比
    mac_5_colon_ratio = sum(
        1 for t in cleaned
        if t.count(":") == 5
    ) / len(cleaned)


    # ==============================
    # （14）URL
    # ==============================
    # 38 → URL 正则匹配比例
    url_regex_ratio = sum(
        1 for t in cleaned
        if URL_REGEX.match(t)
    ) / len(cleaned)

    # 39 → 含 "://"
    url_scheme_ratio = sum(
        1 for t in cleaned
        if t.count("://") == 1
    ) / len(cleaned)

    # 40 → 含 "." 且含 "/"
    url_structure_ratio = sum(
        1 for t in cleaned
        if "." in t and "/" in t
    ) / len(cleaned)


    # 41 → url 关键字比例
    URL_KEYWORDS = [
        # 协议
        "http://", "https://", "ftp://",

        # 常见子域
        "www.", "m.", "api.", "cdn.", "static.",

        # 顶级域（常见）
        ".com", ".cn", ".net", ".org", ".io", ".gov",
        ".edu", ".co", ".uk", ".jp", ".de", ".fr",
        ".info", ".biz", ".top", ".xyz",

        # URL 结构符号
        "/api/", "/index", "/home", "/login",
        "?id=", "?page=", "&", "=",

        # 常见路径特征
        "/v1/", "/v2/", "/static/", "/assets/"
    ]
    url_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t.lower() for k in URL_KEYWORDS)
    ) / len(cleaned)

    # 域名结构合法比例
    domain_structure_ratio = sum(
        1 for t in cleaned
        if DOMAIN_REGEX.match(t)
    ) / len(cleaned)

    # 不包含@
    url_no_at_ratio = sum(
        1 for t in cleaned
        if "@" not in t
    ) / len(cleaned)

    # 一般URL只包含两个冒号
    url_colon_reasonable_ratio = sum(
        1 for t in cleaned
        if 1 <= t.count(":") <= 2
    ) / len(cleaned)

    url_letter_slash_ratio = sum(
        1 for t in cleaned
        if re.search(r'[A-Za-z]/', t)
    ) / len(cleaned)

    url_dot_alpha_ratio = sum(
        1 for t in cleaned
        if re.search(r'[A-Za-z]\.[A-Za-z]', t)
    ) / len(cleaned)

    # ==============================
    # （15）EMAIL
    # ==============================

    # 42 → Email 正则匹配比例
    email_regex_ratio = sum(
        1 for t in cleaned
        if EMAIL_REGEX.match(t)
    ) / len(cleaned)

    # 43 → 含单个 "@"
    email_at_ratio = sum(
        1 for t in cleaned
        if t.count("@") == 1
    ) / len(cleaned)

    # ==============================
    # （16）CAR_VIN
    # ==============================
    # 44 → VIN 正则匹配比例
    vin_regex_ratio = sum(
        1 for t in cleaned
        if VIN_REGEX.match(t)
    ) / len(cleaned)

    # 45 → 长度为 17 的比例
    vin_length_ratio = sum(
        1 for t in cleaned
        if len(t) == 17
    ) / len(cleaned)

    # 46 → VIN 校验位合法比例
    vin_check_digit_ratio = sum(
        1 for t in cleaned
        if vin_check_digit_valid(t)
    ) / len(cleaned)

    # 47 → VIN 校验位合法比例
    VIN_REGION_PREFIX = set("123456789ABCDEFGHJKLMNPRSTUVWXYZ")
    vin_region_prefix_ratio = sum(
        1 for t in cleaned
        if len(t) >= 1 and t[0] in VIN_REGION_PREFIX
    ) / len(cleaned)

    # 48 → VIN 不含冒号比例
    vin_no_colon_ratio = sum(
        1 for t in cleaned
        if ":" not in t
    ) / len(cleaned)

    # ==============================
    # （17）PLATE_NUMBER 车牌号
    # ==============================

    # 48 → plate_regex_ratio
    plate_regex_ratio = sum(
        1 for t in cleaned
        if (PLATE_NORMAL_REGEX.match(t.upper()) or PLATE_NEW_ENERGY_REGEX.match(t.upper()))
    ) / len(cleaned)

    # 49 → plate_province_ratio
    plate_province_ratio = sum(
        1 for t in cleaned
        if len(t) >= 1 and t[0] in province_abbr_dict
    ) / len(cleaned)

    # 50 → plate_length_ratio
    plate_length_ratio = sum(
        1 for t in cleaned
        if len(t) in (7, 8)
    ) / len(cleaned)

    # 51 → plate_new_energy_ratio
    plate_new_energy_ratio = sum(
        1 for t in cleaned
        if PLATE_NEW_ENERGY_REGEX.match(t.upper())
    ) / len(cleaned)

    # ==============================
    # （18）CHARACTER_CODE 中征码
    # ==============================

    # 52 → character_regex_ratio（严格结构匹配比例）
    character_regex_ratio = sum(
        1 for t in cleaned
        if CHAR_CODE_REGEX.fullmatch(t.strip())
    ) / len(cleaned)

    # 53 → character_length_16_ratio（长度为16比例）
    character_length_16_ratio = sum(
        1 for t in cleaned
        if len(t.strip()) == 16
    ) / len(cleaned)

    # 54 → character_suffix_digit_ratio（后13位全数字比例）
    character_suffix_digit_ratio = sum(
        1 for t in cleaned
        if len(t.strip()) == 16 and t.strip()[3:].isdigit()
    ) / len(cleaned)

    # 55 → character_check_digit_ratio（校验位合法比例）
    character_check_digit_ratio = sum(
        1 for t in cleaned
        if len(t.strip()) == 16 and character_code_check(t.strip())
    ) / len(cleaned)

    # 56 → character_no_separator_ratio（无分隔符比例）
    character_no_separator_ratio = sum(
        1 for t in cleaned
        if ":" not in t and "-" not in t and "_" not in t
    ) / len(cleaned)

    # ==============================
    # （19）DATE 年月日（不含时间）
    # ==============================

    # 55 → date_regex_ratio
    date_regex_ratio = sum(
        1 for t in cleaned
        if DATE_REGEX.match(t)
    ) / len(cleaned)

    # 56 → date_valid_ratio
    date_valid_ratio = sum(
        1 for t in cleaned
        if valid_date(t)
    ) / len(cleaned)

    # 57 → date_year_reasonable_ratio
    date_year_reasonable_ratio = 0
    for t in cleaned:
        if DATE_REGEX.match(t):
            years = re.findall(r'\d{4}', t)
            if years:
                year = int(years[0])
                if 1900 <= year <= 2100:
                    date_year_reasonable_ratio += 1

    date_year_reasonable_ratio /= len(cleaned)

    # 58 → date_separator_ratio
    date_separator_ratio = sum(
        1 for t in cleaned
        if any(sep in t for sep in ["-", "/", "."])
    ) / len(cleaned)

    # ==============================
    # （20）DATE_TIME 年月日 + 时间
    # ==============================

    # 59 → datetime_regex_ratio
    datetime_regex_ratio = sum(
        1 for t in cleaned
        if DATE_TIME_REGEX.match(t)
    ) / len(cleaned)

    # 60 → datetime_valid_ratio
    datetime_valid_ratio = sum(
        1 for t in cleaned
        if valid_datetime(t)
    ) / len(cleaned)

    # 61 → datetime_contains_colon_ratio
    datetime_contains_colon_ratio = sum(
        1 for t in cleaned
        if ":" in t
    ) / len(cleaned)

    # 62 → datetime_length_14_ratio
    datetime_length_14_ratio = sum(
        1 for t in cleaned
        if len(t) == 14 and t.isdigit()
    ) / len(cleaned)
    # ==============================
    # （21）ACCOUNT_OPENING 开户许可证
    # ==============================

    # 63 → account_opening_regex_ratio 开户许可证正则匹配比例
    account_opening_regex_ratio = sum(
        1 for t in cleaned
        if ACCOUNT_OPENING_REGEX.match(t)
    ) / len(cleaned)

    # 64 → account_opening_length_ratio 长度为15位比例
    account_opening_length_ratio = sum(
        1 for t in cleaned
        if len(t) == 15
    ) / len(cleaned)

    # 65 → account_opening_prefix_alpha_ratio 首位为字母比例
    account_opening_prefix_alpha_ratio = sum(
        1 for t in cleaned
        if len(t) == 15 and t[0].isalpha()
    ) / len(cleaned)

    # ==============================
    # （22）COUNTRY
    # ==============================

    # 66 → country_dict_ratio 国家字典匹配比例
    country_dict_ratio = sum(
        1 for t in cleaned
        if t.strip().upper() in country_dict
    ) / len(cleaned)

    # 67 → country_alpha_ratio 纯字母比例
    country_alpha_ratio = sum(
        1 for t in cleaned
        if t.strip().isalpha()
    ) / len(cleaned)

    # 68 → country_chinese_ratio 含中文比例
    country_chinese_ratio = sum(
        1 for t in cleaned
        if any('\u4e00' <= c <= '\u9fff' for c in t)
    ) / len(cleaned)

    # 69 → country_short_length_ratio 合理长度比例（2~20）
    country_short_length_ratio = sum(
        1 for t in cleaned
        if 2 <= len(t.strip()) <= 20
    ) / len(cleaned)

    # ==============================
    # （23）FUNDS_NAME 基金名称
    # ==============================

    # 70 → chinese_char_ratio 中文字符占比（结构型特征）
    total_chars = sum(len(t) for t in cleaned)
    chinese_chars = sum(
        1 for t in cleaned for c in t
        if '\u4e00' <= c <= '\u9fff'
    )
    chinese_char_ratio = chinese_chars / total_chars if total_chars > 0 else 0

    # 71 → fund_keyword_ratio 行业关键词比例
    fund_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in FUND_KEYWORDS)
    ) / len(cleaned)

    # 72 → fund_name_dict_ratio 基金名称字典匹配比例
    fund_name_dict_ratio = sum(
        1 for t in cleaned
        if t.strip() in fund_name_dict
    ) / len(cleaned)

    # 73 → fund_length_reasonable_ratio 合理长度比例（4~30）
    fund_length_reasonable_ratio = sum(
        1 for t in cleaned
        if 4 <= len(t.strip()) <= 30
    ) / len(cleaned)

    # ==============================
    # （24）PASSPORT 护照
    # ==============================

    # 74 → passport_regex_ratio 护照正则匹配比例
    passport_regex_ratio = sum(
        1 for t in cleaned
        if PASSPORT_REGEX.match(t.upper())
    ) / len(cleaned)

    # 75 → passport_letter_digit_ratio 字母+数字结构比例
    passport_letter_digit_ratio = sum(
        1 for t in cleaned
        if len(t) >= 2 and t[0].isalpha() and t[1:].isdigit()
    ) / len(cleaned)

    # 76 → passport_prefix_letter_ratio 首位为字母比例
    passport_prefix_letter_ratio = sum(
        1 for t in cleaned
        if len(t) > 0 and t[0].isalpha()
    ) / len(cleaned)

    # 77 → passport_length_9_ratio 长度为9位比例
    passport_length_9_ratio = sum(
        1 for t in cleaned
        if len(t) == 9
    ) / len(cleaned)


    # ==============================
    # （25）PINYIN_NAME 拼音姓名
    # ==============================

    # 78 → pinyin_alpha_ratio 纯字母比例
    pinyin_alpha_ratio = sum(
        1 for t in cleaned
        if t.replace(" ", "").isalpha()
    ) / len(cleaned)

    # 79 → pinyin_capital_ratio 首字母大写比例
    pinyin_capital_ratio = sum(
        1 for t in cleaned
        if len(t) > 0 and t[0].isupper()
    ) / len(cleaned)

    # 80 → pinyin_space_ratio 含空格比例
    pinyin_space_ratio = sum(
        1 for t in cleaned
        if " " in t
    ) / len(cleaned)

    # 81 → pinyin_length_reasonable_ratio 合理长度比例（6~20）
    pinyin_length_reasonable_ratio = sum(
        1 for t in cleaned
        if 6 <= len(t.strip()) <= 20
    ) / len(cleaned)

    # 82 → pinyin_pure_alpha_ratio 100 字母
    pinyin_pure_alpha_ratio = sum(
        1 for t in cleaned if is_reasonable_pinyin(t)
    ) / len(cleaned)

    # ==============================
    # （26）ENTERPRISE_NAME 企业名称
    # ==============================

    # 83 → enterprise_keyword_ratio 企业名称关键字占比
    enterprise_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in enterprise_keyword_dict)
    ) / len(cleaned)

    # 84 → enterprise_parenthesis_city_ratio 左括号 + 城市名 占比
    CITY_PREFIXES = tuple(
        [f"（{c}" for c in city_dict] +
        [f"({c}" for c in city_dict]
    )

    enterprise_parenthesis_city_ratio = sum(
        1 for t in cleaned
        if any(prefix in t for prefix in CITY_PREFIXES)
    ) / len(cleaned)

    # 85 → enterprise_length_reasonable_ratio 长度较长比例（6~40）
    enterprise_length_reasonable_ratio = sum(
        1 for t in cleaned
        if 6 <= len(t.strip()) <= 40
    ) / len(cleaned)

    # 86 → enterprise_suffix_ratio 固定后缀占比
    enterprise_suffix_ratio = sum(
        1 for t in cleaned
        if any(t.endswith(suffix) for suffix in enterprise_suffix_dict)
    ) / len(cleaned)



    # ==============================
    # （27）ADDRESS 地址
    # ==============================

    # 87 → address_region_ratio 行政区划关键词比例
    address_region_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in address_region_keyword_dict)
    ) / len(cleaned)

    # 88 → address_road_keyword_ratio 道路关键词比例
    address_road_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in address_road_keyword_dict)
    ) / len(cleaned)

    # 89 → address_number_structure_ratio 门牌数字结构比例
    address_number_structure_ratio = sum(
        1 for t in cleaned
        if ADDRESS_NUMBER_PATTERN.search(t)
    ) / len(cleaned)

    # 90 → address_length_reasonable_ratio 合理长度比例（8~60）
    address_length_reasonable_ratio = sum(
        1 for t in cleaned
        if 8 <= len(t.strip()) <= 60
    ) / len(cleaned)

    # 91 → address_contains_building_ratio 楼栋结构比例
    address_contains_building_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in ["栋", "单元", "室", "楼", "层"])
    ) / len(cleaned)


    # ==============================
    # （28）NAME 中文姓名
    # ==============================
    # 92 → name_length_reasonable_ratio 合理长度比例（2~3）
    name_length_reasonable_ratio = sum(
        1 for t in cleaned
        if 2 <= len(t.strip()) <= 3
    ) / len(cleaned)


    # 93 → name_all_chinese_ratio 全为中文比例
    name_all_chinese_ratio = sum(
        1 for t in cleaned
        if len(t) >= 2 and all('\u4e00' <= c <= '\u9fff' for c in t)
    ) / len(cleaned)


    # 94 → name_surname_dict_ratio 首字在姓氏字典中的比例
    name_surname_dict_ratio = sum(
        1 for t in cleaned
        if len(t) >= 2 and (
            t[:2] in surname_dict or   # 复姓优先
            t[0] in surname_dict
        )
    ) / len(cleaned)


    # 95 → name_no_digit_ratio 不含数字比例
    name_no_digit_ratio = sum(
        1 for t in cleaned
        if not any(c.isdigit() for c in t)
    ) / len(cleaned)


    # 96 → name_short_length_stability 列内长度稳定性（2或3居多）
    short_lengths = [len(t) for t in cleaned if len(t) in (2, 3)]
    if short_lengths:
        name_short_length_stability = len(short_lengths) / len(cleaned)
    else:
        name_short_length_stability = 0

    # ==============================
    # （29）MONEY 金额
    # ==============================

    # 97 → money_numeric_ratio 纯数字或数字+小数比例
    money_numeric_ratio = sum(
        1 for t in cleaned
        if re.match(r'^[+-]?\d+(\.\d+)?$', t.replace(",", ""))
    ) / len(cleaned)


    # 98 → money_decimal_ratio 含小数比例
    money_decimal_ratio = sum(
        1 for t in cleaned
        if "." in t and re.match(r'^[+-]?\d+(\.\d+)?$', t.replace(",", ""))
    ) / len(cleaned)


    # 99 → money_currency_symbol_ratio 含货币符号比例
    money_currency_symbol_ratio = sum(
        1 for t in cleaned
        if any(sym in t for sym in ["¥", "￥", "$", "€", "£"])
    ) / len(cleaned)


    # 100 → money_comma_ratio 含千分位逗号比例
    money_comma_ratio = sum(
        1 for t in cleaned
        if "," in t
    ) / len(cleaned)


    # 101 → money_reasonable_length_ratio 合理长度（1~15）
    money_reasonable_length_ratio = sum(
        1 for t in cleaned
        if 1 <= len(t.strip()) <= 15
    ) / len(cleaned)


    # 102 →
    money_unit_ratio = sum(
        1 for t in cleaned
        if re.match(
            r'^[+-]?\d+(,\d{3})*(\.\d+)?\s*(元|万元|万|亿|USD|RMB|CNY)?$',
            t.replace("¥", "").replace("￥", "").strip(),
            re.IGNORECASE
        )
    ) / len(cleaned)

    return [
        avg_length,
        fixed_length_flag,
        avg_digit_ratio,
        phone_regex_ratio,
        id_regex_ratio,
        birth_valid_ratio,
        id_check_ratio,
        region_prefix_ratio,
        bank_length_match_ratio,
        bank_luhn_ratio,
        cvv_length_ratio,
        zip6_digit_ratio,
        prefix_stability_ratio,
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
        permit_province_abbr_ratio,

        permit_no_di_ratio,
        permit_xu_keyword_ratio,

        driving_length_18_ratio,
        driving_all_digit_ratio,
        ipv4_regex_ratio,
        ipv4_dot_ratio,
        ipv6_regex_ratio,

        mac_regex_ratio,
        mac_colon_format_ratio,
        mac_dash_format_ratio,
        mac_plain_hex_12_ratio,
        mac_strict_format_ratio,
        mac_5_colon_ratio,

        url_regex_ratio,
        url_scheme_ratio,
        url_structure_ratio,
        url_keyword_ratio,
        domain_structure_ratio,
        url_no_at_ratio,

        url_colon_reasonable_ratio,
        url_letter_slash_ratio,
        url_dot_alpha_ratio,

        email_regex_ratio,
        email_at_ratio,

        vin_regex_ratio,
        vin_length_ratio,
        vin_check_digit_ratio,
        vin_region_prefix_ratio,
        vin_no_colon_ratio,


        plate_regex_ratio,
        plate_province_ratio,
        plate_length_ratio,
        plate_new_energy_ratio,


        character_regex_ratio,
        character_length_16_ratio,
        character_suffix_digit_ratio,
        character_check_digit_ratio,
        character_no_separator_ratio,

        date_regex_ratio,
        date_valid_ratio,
        date_year_reasonable_ratio,
        date_separator_ratio,

        datetime_regex_ratio,
        datetime_valid_ratio,
        datetime_contains_colon_ratio,
        datetime_length_14_ratio,

        account_opening_regex_ratio,
        account_opening_length_ratio,
        account_opening_prefix_alpha_ratio,

        country_dict_ratio,
        country_alpha_ratio,
        country_chinese_ratio,
        country_short_length_ratio,

        chinese_char_ratio,
        fund_keyword_ratio,
        fund_name_dict_ratio,
        fund_length_reasonable_ratio,

        passport_regex_ratio,
        passport_letter_digit_ratio,
        passport_prefix_letter_ratio,
        passport_length_9_ratio,

        pinyin_alpha_ratio,
        pinyin_capital_ratio,
        pinyin_space_ratio,
        pinyin_length_reasonable_ratio,
        pinyin_pure_alpha_ratio,

        enterprise_keyword_ratio,
        enterprise_parenthesis_city_ratio,
        enterprise_length_reasonable_ratio,
        enterprise_suffix_ratio,

        address_region_ratio,
        address_road_keyword_ratio,
        address_number_structure_ratio,
        address_length_reasonable_ratio,
        address_contains_building_ratio,

        name_length_reasonable_ratio,
        name_all_chinese_ratio,
        name_surname_dict_ratio,
        name_no_digit_ratio,
        name_short_length_stability,

        money_numeric_ratio,
        money_decimal_ratio,
        money_currency_symbol_ratio,
        money_comma_ratio,
        money_reasonable_length_ratio,

        money_unit_ratio,

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
    random_state=42,
    class_weight='balanced'
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
# （10）批量测试整列
# ==============================
all_test_columns = {


    "PHONE": [
        "13888888888","13999999999","13700001111","15812345678",
        "18688889999","15066668888","13123456789",
        "600519","2023-01-01","粤B12345"
    ],


    "ID_CARD": [
        "110105199001011234","440106198806158765","320311199508073210",
        "510107197502299999","330102197902307777",
        "210102198812123456","370102199306123210",
        "600519","test@example.com","粤B12345"
    ],


    "BANK_CARD": [
        "6222021234567893","6222021234567802","6222021234567810",
        "6222021234567828","6222021234567836",
        "6222021234567844","6222021234567852",
        "110105199001011234","600519","China"
    ],

    "CVV": [
        "123","456","789","321","654","987","147",
        "600519","2023-01-01","粤B12345"
    ],

    "ZIP_CODE": [
        "100000","200000","300000","400000",
        "710000","610000","510000",
        "600519","test@example.com","110105199001011234",
        "100000","200000","300000","400000","710000","610000","510000",
        "600519","test@example.com","110105199001011234"
    ],

    "STOCK_CODE": [
        "600000",
        "600036",
        "600519",
        "601318",
        "601398",
        "603288",
        "603259",
        "000001",
        "000858",
        "002415"
    ],

    "FUNDS": [
        "000001","110011","519674","160119","003095",
        "001234","002345",
        "600519","粤B12345","China"
    ],


    "CREDIT_CODE": [
        "9144030071526726X","91310000631696382C","91110108MA01G90MXE",
        "914401007594278192","91350100MA2D6J0A5X",
        "91420500MA4KW8F67W","91440300MA5G21P972",
        "600519","2023-01-01","粤B12345"
    ],


    "OFFICER_CARD": [
        "军字第2001988号","海字第123456号","空字第765432号",
        "武字第112233号","军字第888888号",
        "军字第123456号","海字第987654号",
        "600519","test@example.com","粤B12345"
    ],


    "PERMIT": [
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
    ],


    "CAR_DRIVING_LICENCE": [
            "110105199001011234",
            "110105198806158765",
            "110105199508073210",
            "11010519750228999X",
            "110105199912317777",
            "110105200001018888",
            "110105198003056666",
            "110105199607077777"
    ],



    "IP": [
        "192.168.1.10",
        "10.0.0.5",
        "172.16.100.200",
        "8.8.8.8",
        "2001:db8::1",
        "fe80::1ff:fe23:4567:890a",
        "::1",
        "300.168.1.1"   # 干扰（非法IPv4）
    ],



    "MAC": [
        "00:1A:2B:3C:4D:5E","10:9A:BC:DE:F0:11","AA:BB:CC:DD:EE:FF",
        "12:34:56:78:9A:BC","DE:AD:BE:EF:00:01",
        "01:23:45:67:89:AB","FE:DC:BA:98:76:54",
        "600519","110105199001011234","China"
    ],

    "URL": [
        "https://www.example.com","http://www.test.com",
        "ftp://ftp.example.org/file.txt","https://openai.com/research",
        "https://subdomain.example.com","https://www.linkedin.com",
        "https://www.youtube.com",
        "600519","110105199001011234","China"
    ],

    "EMAIL": [
        "test@example.com","user123@gmail.com","admin@openai.com",
        "contact@company.cn","user.name+tag@gmail.com",
        "hello@world.com","info@test.cn",
        "600519","2023-01-01","粤B12345"
    ],

    "CAR_VIN": [
        "1HGCM82633A004352",
        "JH4KA9650MC000000",
        "1FAFP404X1F123456",
        "5YJSA1E26HF000001",
        "1M8GDM9AXKP042788",
        "2FTRX18W1XCA12345",
        "WAUZZZ8P29A123456",
        "SALWR2VF4FA000001",
        "KMHCG45C12U123456",
        "3VWFE21C04M000001"
    ],

    "PLATE_NUMBER": [
        "粤B12345","京A1B2C3","苏A12345D","沪C88888",
        "浙A6F3K9","鲁B7L2Q4","川A1234D",
        "600519","2023-01-01","110105199001011234"
    ],


    "CHARACTER_CODE": [
        "ABC1234567890123",
        "XYZ9876543210987",
        "A1B0000000000001",
        "1234567890123456",   # 干扰（纯数字）
        "600519",             # 股票干扰
        "110105199001011234", # 身份证干扰
        "粤B12345",           # 车牌干扰
        "not_code"            # 噪音
    ],



    "DATE": [
        "2023-01-01","2023-02-15","2023-03-20",
        "20230101","2022-12-31","2021-08-08","2020-06-18",
        "600519","粤B12345","test@example.com"
    ],

    "DATE_TIME": [
        "2023-01-01 12:30:45","2023-02-15 08:15:30",
        "20230101123045","2022-12-31 23:59:59",
        "2021-08-08 06:06:06","2020-06-18 18:18:18","2019-05-05 05:05:05",
        "600519","粤B12345","China"
    ],

    "PASSPORT": [
        "E12345678", "G98765432", "P12345678",
        "D12345678", "E87654321", "G12349876", "P87651234",
        "600519", "粤B12345", "2023-01-01"
    ],

    "ACCOUNT_OPENING": [
        "J12345678901234",
        "K44030012345678",
        "L11010512345678",
        "123456789012345",
        "600519",
        "粤B12345"
    ],

    "COUNTRY": [
        "China","United States","USA","CN","中国","日本","JP",
        "600519","2023-01-01","粤B12345"
    ],

    "FUNDS_NAME": [
        "华夏成长混合","中海可转债债券A","南方中证500ETF",
        "易方达消费行业股票","广发稳健增长混合",
        "博时信用债纯债","嘉实沪深300指数",
        "600519","2023-01-01","粤B12345"
    ],

    "PINYIN_NAME": [
        "ZhangSan","Li Ming","WangWei","Chen Hao",
        "LiuYang","ZhaoMin","HuangLei",
        "600519","China","110105199001011234"
    ],

    "ENTERPRISE_NAME": [
        "北京华瑞科技有限公司","上海腾飞投资集团有限公司",
        "深圳中科实业股份有限公司","杭州未来能源有限公司",
        "广州博雅教育科技有限公司","中国工商银行股份有限公司",
        "成都金桥资产管理有限公司",
        "600519","2023-01-01","粤B12345"
    ],

    "ADDRESS": [
        "北京市朝阳区建国路88号","广东省深圳市南山区科技园科苑路15号",
        "上海市浦东新区世纪大道100号A座","杭州市西湖区文三路90号",
        "成都市高新区天府大道北段28号",
        "广州市天河区体育西路123号","苏州市工业园区星湖街328号",
        "600519","China","test@example.com"
    ],

    "NAME": [
        "张伟","王在芳","李娜","刘洋","陈杰","赵敏","黄磊",
        "600519","13888888888","test@example.com"
    ],

    "MONEY": [
        "100","¥3000","1,200.50","-500","3万元","4500元","￥8800",
        "600519","China","test@example.com"
    ],

    "DEFAULT": [
        "hello world","系统参数A","config_value",
        "alpha-beta","raw data","测试文本","meta.info",
        "600519","2023-01-01","粤B12345"
    ]
}

# ==============================
# 循环预测
# ==============================

for label_name, test_column in all_test_columns.items():

    feature = np.array([extract_column_features(test_column)])

    prediction = model.predict(feature)[0]
    probability = model.predict_proba(feature)[0]

    print("\n==============================")
    print("测试类型:", label_name)
    print("预测类别:", prediction)

    # 打印概率排序（从高到低）
    sorted_probs = sorted(
        zip(model.classes_, probability),
        key=lambda x: x[1],
        reverse=True
    )

    print("置信度,概率分布:")
    for cls, prob in sorted_probs[:5]:   # 只显示前3个最高概率
        print(f"{cls}: {prob:.4f}")


