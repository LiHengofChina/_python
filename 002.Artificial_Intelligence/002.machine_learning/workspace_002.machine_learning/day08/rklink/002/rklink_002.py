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
        return 1300 <= year <= 2925 and 1 <= month <= 12 and 1 <= day <= 31
    except:
        return False
# ==============================
# 军官证
# ==============================

OFFICER_PATTERN = re.compile(r'^(军|海|空|武).{0,3}字第\d{5,8}号$')
DIGIT_MIDDLE_PATTERN = re.compile(r'字第(\d{5,8})号')


# ==============================
# MAC
# ==============================
MAC_REGEX = re.compile(
    r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$|^[0-9A-Fa-f]{12}$'
)

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
# 加载 国家 字典 数据
# ==============================

# 读取本地字典
country_df = pd.read_csv("country/country_dict.csv", dtype=str)

# 构建字典（统一去空格）
country_dict = set(
    country_df["country"].astype(str).str.strip()
)

print("国家字典数量:", len(country_dict))

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

EMAIL_REGEX = re.compile(
    r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
)


# ==============================
# URL 正则
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

CHARACTER_CODE_REGEX = re.compile(r'^[A-Z0-9]{3}\d{13}$')

CHARACTER_CODE_WEIGHTS = [
    1, 3, 5, 7, 11, 2, 13,
    1, 1, 17, 19, 97, 23, 29
]


def character_code_check(code: str) -> bool:
    if not code:
        return False

    code = code.strip().upper()

    # 长度必须 16
    if len(code) != 16:
        return False

    # 正则校验
    if not CHARACTER_CODE_REGEX.match(code):
        return False

    try:
        total = 0
        for i, ch in enumerate(code):
            # Java 的 Character.getNumericValue 行为：
            # '0'-'9' -> 0-9
            # 'A'-'Z' -> 10-35
            value = int(ch) if ch.isdigit() else ord(ch) - ord('A') + 10
            total += value * CHARACTER_CODE_WEIGHTS[i]

        # Java 逻辑：num % 97 + 1
        reissue = total % 97 + 1

        # 校验位是最后 2 位
        verify_code = f"{reissue:02d}"

        return code[-2:] == verify_code

    except Exception:
        return False


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
        return [0] * 66

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

    # 10 CVV 长度比例
    cvv_match = sum(
        1 for t in cleaned
        if len(t) == 3 and t.isdigit()
    )
    cvv_length_ratio = cvv_match / len(cleaned)

    # 11 统计 6 位纯数字占比。
    zip6_digit_match = sum(
        1 for t in cleaned
        if len(t) == 6 and t.isdigit()
    )
    zip6_digit_ratio = zip6_digit_match / len(cleaned)

    # 12 统计前两位是否“稳定”。
    prefixes = [t[:2] for t in cleaned if len(t) == 6 and t.isdigit()]
    if prefixes:
        prefix_unique_ratio = len(set(prefixes)) / len(prefixes)
    else:
        prefix_unique_ratio = 1
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

    # 15 证券代码字典匹配比例
    stock_dict_match = sum(
        1 for t in cleaned
        if t in stock_dict
    )
    stock_dict_ratio = stock_dict_match / len(cleaned)


    # 16 基金代码字典匹配比例
    fund_dict_match = sum(
        1 for t in cleaned
        if t in fund_dict
    )
    fund_dict_ratio = fund_dict_match / len(cleaned)

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

    # 25 → 特殊汉字比例（经营许可证）
    permit_keyword_match = sum(
        1 for t in cleaned
        if any(k in t for k in ["许可", "经营", "证", "监", "卫", "药", "械", "消"])
    )
    permit_keyword_ratio = permit_keyword_match / len(cleaned)

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

    # 35 → MAC 正则匹配比例
    mac_regex_ratio = sum(
        1 for t in cleaned
        if MAC_REGEX.match(t)
    ) / len(cleaned)

    # 36 → 含 5 个相同分隔符比例（必须相同）
    mac_separator_ratio = sum(
        1 for t in cleaned
        if (t.count(':') == 5 and '-' not in t)
        or (t.count('-') == 5 and ':' not in t)
    ) / len(cleaned)

    # 37 → 长度为 12 或 17 的比例
    mac_length_ratio = sum(
        1 for t in cleaned
        if len(t) in (12, 17)
    ) / len(cleaned)

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
    URL_KEYWORDS = ["http", "https", "www.", ".com", ".cn", ".net", ".org"]
    url_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t.lower() for k in URL_KEYWORDS)
    ) / len(cleaned)


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
    VIN_REGION_PREFIX = set("12345JKLMNSTVWXYZ9")
    vin_region_prefix_ratio = sum(
        1 for t in cleaned
        if len(t) >= 1 and t[0] in VIN_REGION_PREFIX
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

    # 52 → character_length_16_ratio
    character_length_16_ratio = sum(
        1 for t in cleaned
        if len(t) == 16
    ) / len(cleaned)

    # 53 → character_prefix_alnum_ratio
    character_prefix_alnum_ratio = sum(
        1 for t in cleaned
        if len(t) == 16 and re.match(r'^[A-Z0-9]{3}', t.upper())
    ) / len(cleaned)

    # 54 → character_check_digit_ratio
    character_check_digit_ratio = sum(
        1 for t in cleaned
        if len(t) == 16 and character_code_check(t)
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
    date_year_reasonable_ratio = sum(
        1 for t in cleaned
        if DATE_REGEX.match(t) and 1900 <= int(t[:4]) <= 2100
    ) / len(cleaned)

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
    # （21）COUNTRY 国籍
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
        permit_province_abbr_ratio,
        driving_length_18_ratio,
        driving_all_digit_ratio,
        ipv4_regex_ratio,
        ipv4_dot_ratio,
        ipv6_regex_ratio,
        mac_regex_ratio,
        mac_separator_ratio,
        mac_length_ratio,
        url_regex_ratio,
        url_scheme_ratio,
        url_structure_ratio,
        url_keyword_ratio,
        email_regex_ratio,
        email_at_ratio,
        vin_regex_ratio,
        vin_length_ratio,
        vin_check_digit_ratio,
        vin_region_prefix_ratio,
        plate_regex_ratio,
        plate_province_ratio,
        plate_length_ratio,
        plate_new_energy_ratio,
        character_length_16_ratio,
        character_prefix_alnum_ratio,
        character_check_digit_ratio,
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
        country_short_length_ratio

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
# （10）手动测试整列
# ==============================


#手机号
# test_column = [
#     "13888888888",
#     "13999999999",
#     "+8613777777777",
#     "13666666666"
# ]

# 身份证
# test_column = [
#     "110105199001011234",
#     "440106198806158765",
#     "320311199508073210",
#     "510107197502299999",
#     "330102197902307777",
#     "110105123456789012",
#     "110105199001011230",
#     "12345678901234567X",
#     "600519",
#     "91440300715267260"
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

# 经营许可
# test_column = [
#     "粤食药监械经营许20180001号",       # 标准
#     "苏B-2021-000123",               # 横杠结构
#     "赣卫消证字(2019)第0012号",        # 括号 + 年份
#     "经营许可证20200111号",            # 只有关键词+年份
#     "许可证编号2022-000321",          # 年份+横杠
#     "食药监械经营许20201111号",        # 无省简称
#     "京食药监械经营许20230004号",       # 省简称+年份
#     "许可2023第0099号",               # 简化结构
#     "营业执照20200123",               # 噪音（非许可证）
#     "1234567890"                     # 强噪音
# ]


#
# # 驾驶证
# test_column = [
#     "110105199001011234",
#     "110105198806158765",
#     "110105199508073210",
#     "11010519750228999X",
#     "110105199912317777",
#     "110105200001018888",
#     "110105198003056666",
#     "110105199607077777"
# ]

# IP 混合测试列
# test_column = [
#     "192.168.1.10",
#     "10.0.0.5",
#     "172.16.100.200",
#     "8.8.8.8",
#     "2001:db8::1",
#     "fe80::1ff:fe23:4567:890a",
#     "::1",
#     "300.168.1.1"   # 干扰（非法IPv4）
# ]

# # URL 测试列
# test_column = [
#     "https://www.baidu.com",
#     "http://example.com/index.html",
#     "https://openai.com/research?type=ai",
#     "ftp://ftp.example.org/file.txt",
#     "http://192.168.1.1/login",
#     "www.sample.net",
#     "example.com/path/to/page",
#     "not_a_url"   # 干扰
# ]

# EMAIL 测试列
# test_column = [
#     "test@example.com",
#     "user123@gmail.com",
#     "admin@openai.com",
#     "contact@company.cn",
#     "user.name+tag@gmail.com",
#     "abc@@wrong.com",      # 干扰（两个@）
#     "not_an_email",        # 干扰
#     "hello@world"          # 干扰（无后缀）
# ]


# VIN 测试列
# test_column = [
#     "1HGCM82633A004352",
#     "JH4KA9650MC000000",
#     "1FAFP404X1F123456",
#     "5YJSA1E26HF000001",
#     "1M8GDM9AXKP042788",
#     "ABCDEFG123456789",   # 干扰（包含非法字母）
#     "12345678901234567",  # 干扰（纯数字）
#     "SHORTVIN123"         # 干扰（长度不够）
# ]


# 车牌号
# test_column = [
#     "粤B12345",
#     "京A1B2C3",
#     "苏A12345D",   # 新能源
#     "沪C88888",
#     "1234567",     # 噪音
#     "abcdefg",     # 噪音
#     "600519",      # 股票干扰
#     "110105199001011234"  # 身份证干扰
# ]

#中征码
# test_column = [
#     "ABC1234567890123",
#     "XYZ9876543210987",
#     "A1B0000000000001",
#     "1234567890123456",   # 干扰（纯数字）
#     "600519",             # 股票干扰
#     "110105199001011234", # 身份证干扰
#     "粤B12345",           # 车牌干扰
#     "not_code"            # 噪音
# ]


#日期
# test_column = [
#     "2023-01-01",
#     "2023-02-15",
#     "2023-03-20",
#     "20230101",
#     "not_date",
#     "600519",
#     "粤B12345"
# ]
#日期-时间
# test_column = [
#     "2023-01-01 12:30:45",
#     "2023-02-15 08:15:30",
#     "20230101123045",
#     "600519",
#     "2023-01-01",
#     "粤B12345"
# ]

# 开启许可
# test_column = [
#     "J12345678901234",
#     "K44030012345678",
#     "L11010512345678",
#     "123456789012345",
#     "600519",
#     "粤B12345"
# ]

test_column = [
    "China",
    "United States",
    "USA",
    "CN",
    "中国",
    "日本",
    "JP",
    "600519",              # 噪音（股票）
    "2023-01-01",          # 噪音（日期）
    "粤B12345",            # 噪音（车牌）
    "abcdef123",           # 噪音
    "110105199001011234"   # 噪音（身份证）
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



