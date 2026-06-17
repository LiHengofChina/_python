"""
脱敏识别 —— 多分类（列级特征版本）
列级特征版本
随机森林
"""

import json
import os
import numpy as np
import pandas as pd
import re
import joblib
from datetime import date
import sklearn.model_selection as ms
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score
from sklearn.calibration import CalibratedClassifierCV

# ==============================
# （1）加载数据
# 必须包含 column_id,text,label
# 训练样本在 fit_data/ 目录：每种类型一个 CSV（如 PHONE.csv、LANDLINE.csv）
# ==============================

_rk002_dir = os.path.dirname(os.path.abspath(__file__))
_dict_root = os.path.join(_rk002_dir, "dict")
_fit_data_dir = os.path.join(_rk002_dir, "fit_data")


def _read_fit_csv(path):
    part = pd.read_csv(path, dtype={"text": str}, skipinitialspace=True)
    part.columns = part.columns.str.strip()
    part["column_id"] = part["column_id"].astype(str).str.strip()
    return part


def _load_fit_data():
    if not os.path.isdir(_fit_data_dir):
        raise FileNotFoundError("未找到训练数据目录: %s" % _fit_data_dir)
    frames = []
    for fname in sorted(os.listdir(_fit_data_dir)):
        if not fname.lower().endswith(".csv"):
            continue
        path = os.path.join(_fit_data_dir, fname)
        if not os.path.isfile(path):
            continue
        part = _read_fit_csv(path)
        frames.append(part)
        print("已加载训练样本: %s （+%d 行）" % (fname, len(part)))
    if not frames:
        raise FileNotFoundError("fit_data 目录下无 CSV 训练文件: %s" % _fit_data_dir)
    merged = pd.concat(frames, ignore_index=True)
    print("训练数据合计: %d 行, 目录=%s" % (len(merged), _fit_data_dir))
    return merged


df = _load_fit_data()

# print("原始数据前5行：")
# print(df.head())
# print("=" * 60)

# ==============================
# 手机号、身份证 正则规则
# ==============================
PHONE_REGEX = re.compile(r"^1[3-9]\d{9}$")
# 固话形态（与 Java PhoneRecognizeHeuristics.LANDLINE_PHONE_REGEX 一致）：
# 主格式（0+区号+本地，共 11 位）：0XX+8 位本地（如 01012345678 / 010-12345678）；
# 0XXX+7 位本地（如 07551234567 / 0755-1234567）；部分城市 0XXX+8 位本地（如 0755-83301199）。
# 另含：本市 7~8 位本地号、400/800、95·12·100 短号、+86/86 国际写法。
LANDLINE_PHONE_REGEX = re.compile(
    r'^('
    r'(\+?86[- ]?)?0\d{2}[- ]?\d{8}|'
    r'(\+?86[- ]?)?0\d{3}[- ]?\d{7}|'
    r'(\+?86[- ]?)?0\d{3}[- ]?\d{8}|'
    r'\+?86[- ]?\d{2,3}[- ]?\d{7,8}|'
    r'400[- ]?\d{3}[- ]?\d{4}|'
    r'800[- ]?\d{7,8}|'
    r'9[56]\d{3,6}|'
    r'12\d{3}|'
    r'100\d{2,4}|'
    r'[2-8]\d{2,3}[- ]?\d{4}|'
    r'[2-8]\d{6,7}'
    r')$'
)
ISO_DATE_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}$')
ISO_DATE_TIME_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$')

def _looks_like_iso_date_digits(norm):
    """去横杠后 8 位 YYYYMMDD，避免与本地固话 [2-8]\\d{6,7} 冲突。"""
    if len(norm) != 8 or not norm.isdigit():
        return False
    try:
        y, m, d = int(norm[:4]), int(norm[4:6]), int(norm[6:8])
        return 1900 <= y <= 2100 and 1 <= m <= 12 and 1 <= d <= 31
    except ValueError:
        return False

def _is_date_like_phone_exclusion(text):
    s = str(text).strip()
    if ISO_DATE_REGEX.match(s) or ISO_DATE_TIME_REGEX.match(s):
        return True
    return _looks_like_iso_date_digits(_normalize_phone_digits(s))

def _normalize_phone_digits(text):
    norm = re.sub(r'[\s\-+]', '', str(text).strip())
    if norm.startswith('86') and len(norm) > 11:
        norm = norm[2:]
    return norm

def is_mobile_phone_value(text):
    s = str(text).strip()
    if not s:
        return False
    if PHONE_REGEX.match(s):
        return True
    return bool(PHONE_REGEX.match(_normalize_phone_digits(s)))

def _is_invalid_landline_digits(norm):
    """占位/脏数据：全 0、本地段全 0、或无区号的同数字占位（如 999999999）。"""
    if not norm or not norm.isdigit():
        return False
    if all(c == '0' for c in norm):
        return True
    if norm.startswith('0') and len(norm) >= 10:
        return all(c == '0' for c in norm[-8:])
    if not norm.startswith('0') and len(norm) == 9 and len(set(norm)) == 1:
        return True
    return False

def is_landline_phone_value(text):
    s = str(text).strip()
    if not s or is_mobile_phone_value(s) or _is_date_like_phone_exclusion(s):
        return False
    if LANDLINE_PHONE_REGEX.match(s):
        return not _is_invalid_landline_digits(_normalize_phone_digits(s))
    norm = _normalize_phone_digits(s)
    if _looks_like_iso_date_digits(norm):
        return False
    return bool(LANDLINE_PHONE_REGEX.match(norm)) and not _is_invalid_landline_digits(norm)

def is_phone_value(text):
    return is_mobile_phone_value(text) or is_landline_phone_value(text)

PURE_100XX_SHORT_REGEX = re.compile(r'^100\d{2,4}$')
YEAR_RANGE_REGEX = re.compile(r'^\d{4}-\d{4}$')
PHONE_COLUMN_STRICT_RATIO = 0.75


def _is_pure_100xx_short_code(text):
    """纯 100xx 运营商/客服短号（如 10086、10099），非联系电话列。"""
    norm = _normalize_phone_digits(str(text).strip())
    return norm.isdigit() and len(norm) <= 6 and bool(PURE_100XX_SHORT_REGEX.match(norm))


def _is_pure_7_8_digit_bare_code(text):
    """无区号格式的裸 7~8 位数字（业务编号/工号等），且非固话形态。"""
    s = str(text).strip()
    if re.search(r'[- ]', s):
        return False
    norm = _normalize_phone_digits(s)
    if not (norm.isdigit() and len(norm) in (7, 8)):
        return False
    if is_landline_phone_value(text):
        return False
    return True


def _is_year_range_like(text):
    return bool(YEAR_RANGE_REGEX.match(str(text).strip()))


def _is_bare_10_digit_code(text):
    """裸 10 位数字（常见日期/编号，非手机）。"""
    s = str(text).strip()
    if re.search(r'[- ]', s):
        return False
    norm = _normalize_phone_digits(s)
    return norm.isdigit() and len(norm) == 10 and not is_mobile_phone_value(s)


def _landline_column_noise_excluded(text_list):
    """固话列噪声：纯 100xx / 裸 7~8 位非固话编号 / 学年 / 裸 10 位等占比过高则不算固话列。"""
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return True
    n = len(cleaned)
    pure_100 = sum(1 for t in cleaned if _is_pure_100xx_short_code(t)) / n
    pure_78 = sum(1 for t in cleaned if _is_pure_7_8_digit_bare_code(t)) / n
    year_rng = sum(1 for t in cleaned if _is_year_range_like(t)) / n
    bare_10 = sum(1 for t in cleaned if _is_bare_10_digit_code(t)) / n
    return (pure_100 >= PHONE_COLUMN_STRICT_RATIO
            or pure_78 >= PHONE_COLUMN_STRICT_RATIO
            or year_rng >= PHONE_COLUMN_STRICT_RATIO
            or bare_10 >= PHONE_COLUMN_STRICT_RATIO)


def _looks_like_strict_mobile_column(text_list):
    """严格手机列：≥75% 为 11 位手机号形态。"""
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return False
    n = len(cleaned)
    mobile_hit = sum(1 for t in cleaned if is_mobile_phone_value(t)) / n
    return mobile_hit >= PHONE_COLUMN_STRICT_RATIO


def _looks_like_strict_landline_column(text_list):
    """严格固话列：≥75% 为固话形态，且非手机主导列、非典型噪声列。"""
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return False
    n = len(cleaned)
    landline_hit = sum(1 for t in cleaned if is_landline_phone_value(t)) / n
    if landline_hit < PHONE_COLUMN_STRICT_RATIO:
        return False
    if _looks_like_strict_mobile_column(text_list):
        return False
    return not _landline_column_noise_excluded(text_list)


def _looks_like_strict_phone_column(text_list):
    """
    严格电话列（手机或固话）：兼容旧逻辑；新类型请用 mobile/landline 分列判断。
    """
    return _looks_like_strict_mobile_column(text_list) or _looks_like_strict_landline_column(text_list)

def _digit_only_length(text):
    """行内数字字符个数（去掉非数字后长度）。"""
    return sum(1 for c in str(text) if c.isdigit())

def _phone_digit_len_13_11_8_hit(text):
    """电话常见纯数字长度：8 位本地号 / 11 位手机或区号+座机 / 13 位 86+手机。"""
    n = _digit_only_length(text)
    return n in (8, 11, 13)

ID_REGEX = re.compile(r"^\d{17}[\dXx]$")

def valid_birth(id_number):
    """身份证第 7–14 位须为合法公历 YYYYMMDD，且 1949 ≤ 年 ≤ 当前年（与 Java IdCardRecognizeHeuristics 一致）。"""
    try:
        if id_number is None or len(id_number) < 14:
            return False
        birth = id_number[6:14]
        if not birth.isdigit():
            return False
        year = int(birth[0:4])
        month = int(birth[4:6])
        day = int(birth[6:8])
        if year < 1949 or year > date.today().year:
            return False
        date(year, month, day)
        return True
    except (ValueError, TypeError):
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
# 加载证券代码相关字典（A 股段 + 场内等辅助段，特征 fund_dict_ratio 与 Java 一致）
# ==============================
# 读取本地字典
stock_df = pd.read_csv(os.path.join(_dict_root, "stock_fund", "stock_code_dict.csv"), dtype=str)
fund_df = pd.read_csv(os.path.join(_dict_root, "stock_fund", "fund_code_dict.csv"), dtype=str)

# 构建字典
stock_dict = set(stock_df["code"].astype(str))
fund_dict = set(fund_df["证券代码"].astype(str))
# 证券代码与基金代码在业务上合并识别；两路字典命中统一用并集（与 Java RecognizeDicts 一致）
stock_fund_code_union = stock_dict | fund_dict


# ==============================
# 构建基金名称字典
# ==============================

fund_name_dict = set(
    fund_df["基金简称"].astype(str).str.strip()
)

# ==============================
# 构建中国城市字典
# ==============================

city_df = pd.read_csv(os.path.join(_dict_root, "cities", "city_dict.csv"), dtype=str)

city_dict = set(
    city_df["city"].astype(str).str.strip()
)

# ==============================
# 构建中文姓氏字典
# ==============================

import json

with open(os.path.join(_dict_root, "chinesename", "surname_dict.json"), "r", encoding="utf-8") as f:
    surname_list = json.load(f)

surname_dict = set(
    s.strip()
    for s in surname_list
    if isinstance(s, str) and s.strip()
)


def _surname_head_in_dict(text):
    """姓名首字或复姓前两字是否在姓氏字典（百家姓）中。"""
    t = str(text).strip()
    if not t:
        return False
    if len(t) >= 2 and t[:2] in surname_dict:
        return True
    return t[0] in surname_dict


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
country_df = pd.read_csv(os.path.join(_dict_root, "country", "country_dict.csv"), dtype=str)

# 构建字典（统一去空格）
country_dict = set(
    country_df["country"].astype(str).str.strip().str.upper()
)


def _pure_han_country_names(source):
    """country_dict 中纯汉字国名，并入姓名排除黑名单（与 Java NameRecognizeHeuristics 一致）。"""
    out = set()
    for item in source:
        s = str(item).strip()
        if s and all("\u4e00" <= ch <= "\u9fff" for ch in s):
            out.add(s)
    return frozenset(out)


COUNTRY_NAME_HAN_EXACT_TOKENS = _pure_han_country_names(country_dict)



# ==============================
# 拼音结构
# ==============================


# 拼音姓名格式：全小写字母，末尾可有数字防重复（如 zhangsan1）
PINYIN_NAME_FORMAT = re.compile(r"^[a-z]+[0-9]*$")

# 有效拼音音节集合（用于校验能否拼出汉字）
def _load_pinyin_syllables():
    try:
        from pypinyin import lazy_pinyin, Style
        import unicodedata
        s = set()
        for cp in range(0x4e00, 0x9fff):
            try:
                c = chr(cp)
                if unicodedata.category(c) == 'Lo':
                    for py in lazy_pinyin(c, style=Style.NORMAL):
                        if py and py.isalpha():
                            s.add(py.lower())
            except Exception:
                pass
        return frozenset(s)
    except ImportError:
        # 无 pypinyin 时从本地 JSON 加载（与脚本同目录）
        for base in [_dict_root, os.path.dirname(os.path.abspath(__file__)), ".", os.getcwd()]:
            try:
                path = os.path.join(base, "pinyin", "pinyin_syllables.json")
                if os.path.isfile(path):
                    with open(path, "r", encoding="utf-8") as f:
                        return frozenset(json.load(f))
            except Exception:
                continue
        return frozenset()  # 空集时该特征恒为 0

PINYIN_SYLLABLES = _load_pinyin_syllables()


def _is_valid_pinyin_syllable_sequence(text, syllables):
    """贪心最长匹配：整串能否拆成有效拼音音节。text 已去空格、转小写、去掉末尾数字"""
    if not text or not syllables:
        return False
    # 去掉末尾数字
    pure = re.sub(r"[0-9]+$", "", text).lower()
    if not pure or not pure.isalpha():
        return False
    # 按长度降序，优先匹配长音节
    sorted_syl = sorted(syllables, key=len, reverse=True)
    pos = 0
    while pos < len(pure):
        found = False
        for syl in sorted_syl:
            if pure[pos:].startswith(syl):
                pos += len(syl)
                found = True
                break
        if not found:
            return False
    return True


def is_reasonable_pinyin(text):
    """拼音格式：字母（可含空格）+ 末尾可选数字"""
    text = text.strip()
    # 去掉空格后：字母 + 末尾可选数字
    pure = text.replace(" ", "")
    if not pure:
        return False
    # 允许 [a-zA-Z]+[0-9]* 或纯字母
    return bool(re.fullmatch(r"[a-zA-Z]+[0-9]*", pure))


# ==============================
# IP正则
# ==============================

IPV4_REGEX = re.compile(
    r'^((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}'
    r'(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$'
)

# Informix INET 格式：.A0000.00000.00001. 对应 10.0.0.1
INFORMIX_IP_REGEX = re.compile(r'^\.[A-Fa-f0-9]{1,4}\d*\.\d+\.\d+\.$')

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
# 加载行政区划树 JSON（仅用于 region_dict；已移除邮政编码 ZIP_CODE 类别与 zip_dict 特征）
# ==============================
with open(os.path.join(_dict_root, "zip_code", "zip_code.txt"), "r", encoding="utf-8") as f:
    zip_data = json.load(f)

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
# 加载 bank_bin_prefixes（用于 bank_bin_prefix_ratio 特征）
# 训练用字典：dict/bank_bin/bank_bin_prefixes.json
# all_dicts.json 是给 Java SDK 用的，训练时只用模型侧字典
# ==============================
_bank_bin_training_path = os.path.join(_dict_root, "bank_bin", "bank_bin_prefixes.json")
bank_bin_prefixes = set()
if os.path.exists(_bank_bin_training_path):
    try:
        with open(_bank_bin_training_path, "r", encoding="utf-8") as f:
            bank_bin_prefixes = set(json.load(f))
    except Exception:
        pass

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
    if not valid_birth(id_number):
        return False

    id_number = id_number.upper()

    total = 0
    for i in range(17):
        total += int(id_number[i]) * ID_WEIGHTS[i]

    remainder = total % 11
    return ID_CHECK_MAP[remainder] == id_number[17]


def _looks_like_strict_id_card_column(text_list):
    """列内每行均为 18 位身份证形态且第 7–14 位生日 100% 合法（与 Java IdCardRecognizeHeuristics 一致）。"""
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return False
    for t in cleaned:
        if not ID_REGEX.match(t):
            return False
        if not valid_birth(t):
            return False
    return True


# ==============================
# MIXED：行内嵌入型 5 维特征（121 基础 + 5 = 126，与 mask-sdk ColumnFeatureExtractor 一致）
# mixed_embed_phone_ratio：行内嵌手机或固话命中比例（与 Java MixedMaskHandler.containsEmbeddedPhone 一致）
# ==============================
_EMBEDDED_PHONE = re.compile(r"1[3-9]\d{9}")
_EMBEDDED_PASSPORT_BLOCK = re.compile(r"[A-Za-z]{1,2}\d{7,8}")


def _mixed_embedded_phone_hit(text):
    return bool(_EMBEDDED_PHONE.search(text))


def _mixed_embedded_landline_hit(text):
    """行内滑动 7~20 位子串检测固话（与 Java MixedMaskHandler + LandlineMaskHandler 一致）。"""
    n = len(text)
    if n < 7:
        return False
    max_len = min(20, n)
    for length in range(7, max_len + 1):
        for i in range(0, n - length + 1):
            if is_landline_phone_value(text[i : i + length]):
                return True
    return False


def _mixed_embedded_phone_or_landline_hit(text):
    return _mixed_embedded_phone_hit(text) or _mixed_embedded_landline_hit(text)


def _mixed_embedded_passport_hit(text):
    u = text.upper()
    for m in _EMBEDDED_PASSPORT_BLOCK.finditer(u):
        seg = m.group(0)
        if 8 <= len(seg) <= 10 and re.fullmatch(r"[A-Z]{1,2}\d{7,8}", seg):
            return True
    return False


def _mixed_sliding_any(length, text, pred):
    if len(text) < length:
        return False
    for i in range(0, len(text) - length + 1):
        if pred(text[i : i + length]):
            return True
    return False


def _mixed_embedded_id_valid_hit(text):
    return _mixed_sliding_any(18, text, id_card_check)


def _mixed_embedded_credit_valid_hit(text):
    return _mixed_sliding_any(18, text, credit_code_check)


def _mixed_has_chinese(text):
    return any("\u4e00" <= c <= "\u9fff" for c in text)


def _mixed_long_cn_digit_token_hit(text):
    s = text.strip()
    if len(s) < 10:
        return False
    if not _mixed_has_chinese(s):
        return False
    if not any(c.isdigit() for c in s):
        return False
    if " " in s or "、" in s or "，" in s:
        return True
    return len(s) >= 18


def _mixed_embedding_ratios(cleaned):
    n = len(cleaned)
    if n == 0:
        return (0.0, 0.0, 0.0, 0.0, 0.0)
    r_phone = sum(1 for t in cleaned if _mixed_embedded_phone_or_landline_hit(t)) / n
    r_id = sum(1 for t in cleaned if _mixed_embedded_id_valid_hit(t)) / n
    r_pass = sum(1 for t in cleaned if _mixed_embedded_passport_hit(t)) / n
    r_credit = sum(1 for t in cleaned if _mixed_embedded_credit_valid_hit(t)) / n
    r_long = sum(1 for t in cleaned if _mixed_long_cn_digit_token_hit(t)) / n
    return (r_phone, r_id, r_pass, r_credit, r_long)


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
        text = str(text).strip()
        if "-" in text:
            datetime.strptime(text, "%Y-%m-%d")
        elif "/" in text:
            datetime.strptime(text, "%Y/%m/%d")
        elif "." in text:
            datetime.strptime(text, "%Y.%m.%d")
        elif len(text) == 8:
            # 紧凑 YYYYMMDD：前两位（世纪前缀）须 < 21，最多 20 开头
            if text.isdigit() and int(text[:2]) >= 21:
                return False
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
        text = str(text).strip()
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
            # 紧凑 yyyyMMddHHmmss：日期部分前两位须 < 21
            if text.isdigit() and int(text[:2]) >= 21:
                return False
            datetime.strptime(text, "%Y%m%d%H%M%S")
        else:
            return False
        return True
    except:
        return False

# ==============================
# 开启许可（开户许可证：1 位字母 + 14 位数字 = 15 位，与 Java 一致支持 A-Za-z）
# ==============================
ACCOUNT_OPENING_REGEX = re.compile(r'^[A-Za-z]\d{14}$')

permit_strong_keyword_dict = {
    "许可",
    "许可证",
    "经营许可证",
    "生产许可证",
    "批准文号",
    "登记证",
    "备案",
    "食药监",
    "械",
    "消",
    "药",
    "字第",  # 许可证典型结构，地址通常不含
}

# ==============================
# （2）列级特征提取函数
# ==============================

def _is_compact_date_8(text):
    s = str(text).strip()
    return len(s) == 8 and s.isdigit()


def _compact_date_yy_lt_21(text):
    if not _is_compact_date_8(text):
        return False
    return int(str(text).strip()[:2]) < 21


def _compact_date_mm_lt_24(text):
    if not _is_compact_date_8(text):
        return False
    return int(str(text).strip()[4:6]) < 24


def _compact_date_dd_lt_24(text):
    if not _is_compact_date_8(text):
        return False
    return int(str(text).strip()[6:8]) < 24


def _is_plausible_date_value(text):
    """真实日期形态：紧凑 8 位须 yy 前缀 <21 且年份 1900–2100；分隔格式须 valid_date 且年份合理。"""
    s = str(text).strip()
    if _is_compact_date_8(s):
        if not valid_date(s):
            return False
        year = int(s[:4])
        return 1900 <= year <= 2100
    if DATE_REGEX.match(s):
        if not valid_date(s):
            return False
        years = re.findall(r'\d{4}', s)
        if not years:
            return False
        year = int(years[0])
        return 1900 <= year <= 2100
    return False


def _looks_like_strict_date_column(text_list):
    """严格日期列：≥75% 为真实日期形态（排除 6602 等伪紧凑日期）。"""
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return False
    n = len(cleaned)
    hit = sum(1 for t in cleaned if _is_plausible_date_value(t)) / n
    return hit >= PHONE_COLUMN_STRICT_RATIO


def _is_plausible_datetime_value(text):
    s = str(text).strip()
    if not DATE_TIME_REGEX.match(s):
        return False
    if not valid_datetime(s):
        return False
    years = re.findall(r'\d{4}', s)
    if not years:
        return False
    year = int(years[0])
    return 1900 <= year <= 2100


def _looks_like_strict_datetime_column(text_list):
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return False
    n = len(cleaned)
    hit = sum(1 for t in cleaned if _is_plausible_datetime_value(t)) / n
    return hit >= PHONE_COLUMN_STRICT_RATIO


# ==============================
# COLUMN_MIXED：多行混合（每格单一敏感形态，不同行类型不同）
# ==============================

COLUMN_MIXED_MIN_SINGLE_ROW_RATIO = 0.67
COLUMN_MIXED_MAX_DOMINANT_KIND_RATIO = 0.75
COLUMN_MIXED_MAX_INTRA_CELL_MULTI_RATIO = 0.25


def _row_intra_cell_multi_embed_hit(text):
    """单格内嵌 ≥2 类敏感形态 → MIXED 单行，非 COLUMN_MIXED。"""
    hits = 0
    if _mixed_embedded_phone_or_landline_hit(text):
        hits += 1
    if _mixed_embedded_id_valid_hit(text):
        hits += 1
    if _mixed_embedded_passport_hit(text):
        hits += 1
    if _mixed_embedded_credit_valid_hit(text):
        hits += 1
    return hits >= 2


def _row_single_sensitive_kind(text):
    if _row_intra_cell_multi_embed_hit(text):
        return None
    s = str(text).strip()
    if not s:
        return None
    if is_mobile_phone_value(s):
        return "PHONE"
    if is_landline_phone_value(s):
        return "LANDLINE"
    if ID_REGEX.match(s) and id_card_check(s):
        return "ID_CARD"
    if PASSPORT_REGEX.match(s.upper()):
        return "PASSPORT"
    if len(s) == 18 and credit_code_check(s):
        return "CREDIT_CODE"
    if EMAIL_REGEX.match(s):
        return "EMAIL"
    return None


def _looks_like_column_mixed_column(text_list):
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if len(cleaned) < 2:
        return False
    n = len(cleaned)
    kinds = [_row_single_sensitive_kind(t) for t in cleaned]
    labeled = [k for k in kinds if k]
    if len(labeled) < 2:
        return False
    from collections import Counter
    c = Counter(labeled)
    if len(c) < 2:
        return False
    if len(labeled) / n < COLUMN_MIXED_MIN_SINGLE_ROW_RATIO:
        return False
    intra_multi = sum(1 for t in cleaned if _row_intra_cell_multi_embed_hit(t)) / n
    if intra_multi > COLUMN_MIXED_MAX_INTRA_CELL_MULTI_RATIO:
        return False
    if max(c.values()) / n >= COLUMN_MIXED_MAX_DOMINANT_KIND_RATIO:
        return False
    return True


def _column_mixed_kind_diversity_ratio(cleaned):
    kinds = set(k for t in cleaned if (k := _row_single_sensitive_kind(t)))
    if len(kinds) < 2:
        return 0.0
    return min(1.0, (len(kinds) - 1) / 4.0)


def _column_mixed_single_type_row_ratio(cleaned):
    if not cleaned:
        return 0.0
    hit = sum(1 for t in cleaned if _row_single_sensitive_kind(t))
    return hit / len(cleaned)


def _column_mixed_intra_cell_multi_row_ratio(cleaned):
    if not cleaned:
        return 0.0
    hit = sum(1 for t in cleaned if _row_intra_cell_multi_embed_hit(t))
    return hit / len(cleaned)


def extract_column_features(text_list):

    cleaned = [str(t).strip() for t in text_list if pd.notnull(t)]

    if len(cleaned) == 0:
        return [0] * 136  # 121 基础 + 5 MIXED + 3 姓名 + 1 电话 + 3 紧凑日期 + 3 COLUMN_MIXED（与 mask-sdk Java 一致）

    lengths = [len(t) for t in cleaned]

    # ==============================
    # （1）PHONE
    # ==============================
    # 0 → avg_length
    avg_length = np.mean(lengths)

    # 1 → fixed_length_flag
    fixed_length_flag = 1 if len(set(lengths)) == 1 else 0

    # 2 → avg_digit_ratio
    digit_ratios = []
    for t in cleaned:
        digits = sum(c.isdigit() for c in t)
        digit_ratios.append(digits / len(t))
    avg_digit_ratio = np.mean(digit_ratios)

    # 3 → phone_regex_ratio = 手机占比 + 固话占比（混合列相加，互斥划分，上限 1.0）
    mobile_phone_ratio = sum(1 for t in cleaned if is_mobile_phone_value(t)) / len(cleaned)
    landline_phone_ratio = sum(1 for t in cleaned if is_landline_phone_value(t)) / len(cleaned)
    phone_regex_ratio = min(1.0, mobile_phone_ratio + landline_phone_ratio)

    # 3b → phone_digit_len_13_11_8_ratio 纯数字长度为 8/11/13 的占比（86+手机/11位手机座机/8位本地号）
    phone_digit_len_13_11_8_ratio = sum(
        1 for t in cleaned if _phone_digit_len_13_11_8_hit(t)
    ) / len(cleaned)

    # ==============================
    # （2）ID_CARD
    # ==============================
    # 4 → id_regex_ratio
    id_match = sum(1 for t in cleaned if ID_REGEX.match(t))
    id_regex_ratio = id_match / len(cleaned)

    # 5 → birth_valid_ratio 第 7–14 位合法公历生日（1949≤年≤当前年）比例
    birth_valid_ratio = sum(
        1 for t in cleaned
        if ID_REGEX.match(t) and valid_birth(t)
    ) / len(cleaned)

    # 6 → id_check_ratio 身份证校验
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
    # 8 → bank_length_match_ratio 银行卡长度匹配比例（16-19位 + 全数字）
    bank_length_match = sum(
        1 for t in cleaned
        if 16 <= len(t) <= 19 and t.isdigit()
    )
    bank_length_match_ratio = bank_length_match / len(cleaned)

    # 9 → bank_luhn_ratio Luhn通过比例
    bank_luhn_match = sum(
        1 for t in cleaned
        if 16 <= len(t) <= 19 and t.isdigit() and luhn_check(t)
    )
    bank_luhn_ratio = bank_luhn_match / len(cleaned)

    # 10 → bank_bin_prefix_ratio 前6位在银行卡BIN前缀字典中的比例（16-19位数字）
    bank_bin_prefix_match = sum(
        1 for t in cleaned
        if 16 <= len(t) <= 19 and t.isdigit() and len(t) >= 6 and t[:6] in bank_bin_prefixes
    )
    bank_bin_prefix_ratio = bank_bin_prefix_match / len(cleaned)

    # ==============================
    # （5）STOCK_CODE（原 ZIP_CODE 四维邮编特征已删除；另删 6 维低贡献/冗余，维数 127→121）
    # ==============================
    # → stock_dict_ratio：命中「证券字典 ∪ 基金代码字典」比例（两表合并使用）
    stock_dict_match = sum(1 for t in cleaned if t in stock_fund_code_union)
    stock_dict_ratio = stock_dict_match / len(cleaned)

    # fund_dict_ratio：特征名历史沿用；语义与 stock_dict_ratio 相同，均为并集命中（与 Java 一致）
    fund_dict_match = sum(1 for t in cleaned if t in stock_fund_code_union)
    fund_dict_ratio = fund_dict_match / len(cleaned)

    # ==============================
    # （8）CREDIT_CODE 统一社会信用代码（含营业执照所载 18 位码，不单列「营业执照编号」类）
    # ==============================
    # 17 → credit_length_match_ratio 长度=18且全为数字+大写字母的比例
    credit_length_match = sum(
        1 for t in cleaned
        if len(t) == 18 and all(c in CREDIT_CODE_CHARS for c in t)
    )
    credit_length_match_ratio = credit_length_match / len(cleaned)

    # 18 → credit_region_digit_ratio 第3-8位是纯数字的比例
    credit_region_digit_match = sum(
        1 for t in cleaned
        if len(t) == 18 and t[2:8].isdigit()
    )
    credit_region_digit_ratio = credit_region_digit_match / len(cleaned)

    # 19 → credit_region_dict_ratio 行政区划ID为6位数字
    credit_region_dict_match = sum(
        1 for t in cleaned
        if len(t) == 18 and t[2:8].isdigit() and t[2:8] in region_dict
    )
    credit_region_dict_ratio = credit_region_dict_match / len(cleaned)

    # 20 → credit_check_digit_ratio 统一社会信用代码校验
    credit_check_match = sum(
        1 for t in cleaned
        if credit_code_check(t)
    )
    credit_check_digit_ratio = credit_check_match / len(cleaned)

    # ==============================
    # （9）OFFICER_CARD 军官证
    # ==============================
    # 21 → officer_keyword_ratio 特殊汉字的比例
    officer_keyword_match = sum(
        1 for t in cleaned
        if any(k in t for k in ["军", "海", "空", "武", "字第", "号"])
    )
    officer_keyword_ratio = officer_keyword_match / len(cleaned)

    # 22 → officer_pattern_ratio 军官格式正则
    officer_pattern_match = sum(
        1 for t in cleaned
        if OFFICER_PATTERN.match(t)
    )
    officer_pattern_ratio = officer_pattern_match / len(cleaned)

    # 23 → officer_end_with_hao_ratio 最后一个字"号"
    officer_end_with_hao_match = sum(
        1 for t in cleaned
        if t.endswith("号")
    )
    officer_end_with_hao_ratio = officer_end_with_hao_match / len(cleaned)

    # 24 → officer_digit_middle_ratio "字第"和"号"之间为数字
    officer_digit_middle_match = sum(
        1 for t in cleaned
        if DIGIT_MIDDLE_PATTERN.search(t)
    )
    officer_digit_middle_ratio = officer_digit_middle_match / len(cleaned)

    # ==============================
    # （10）PERMIT 优化版
    # ==============================

    # （已移除 permit_strict_keyword_ratio：RF 重要性为 0，与 zheng/xuke 等强重叠）

    # 25 → permit_wenzi_pattern_ratio 文号结构比例（字第xxx号）
    permit_wenzi_pattern_ratio = sum(
        1 for t in cleaned
        if re.search(r'字第\d{3,}号', t)
    ) / len(cleaned)

    # 27 → permit_year_hao_ratio 年份+号结构比例
    permit_year_hao_ratio = sum(
        1 for t in cleaned
        if re.search(r'(19|20)\d{2}.*号', t)
    ) / len(cleaned)

    # 28 → permit_long_digit_ratio 数字连续长度>=4比例（编号特征）
    permit_long_digit_ratio = sum(
        1 for t in cleaned
        if re.search(r'\d{4,}', t)
    ) / len(cleaned)

    # 30 → permit_contains_zheng_ratio 包含“证”字比例（核心结构）
    permit_contains_zheng_ratio = sum(
        1 for t in cleaned
        if "证" in t
    ) / len(cleaned)

    # （已移除 permit_contains_xuke_ratio：RF 重要性≈0）

    # 31 → permit_no_road_keyword_ratio 不包含道路关键词比例（抑制ADDRESS）
    permit_no_road_keyword_ratio = sum(
        1 for t in cleaned
        if not any(k in t for k in address_road_keyword_dict)
    ) / len(cleaned)

    # 33 → permit_not_address_pattern_ratio 不符合地址强结构比例（市+区+路）
    permit_not_address_pattern_ratio = sum(
        1 for t in cleaned
        if not re.search(r".+市.+区.+(路|街|大道)", t)
    ) / len(cleaned)

    # 34 → permit_parenthesis_ratio 包含括号比例
    permit_parenthesis_ratio = sum(
        1 for t in cleaned
        if any(p in t for p in ["(", ")", "（", "）"])
    ) / len(cleaned)




    # ==============================
    # （11）通用辅助特征（与 Java ColumnFeatureExtractor f35/f36 对齐；用于身份证等 18 位数字列）
    # ==============================
    # 35 → driving_length_18_ratio 长度为 18 的样本占比
    driving_length_18_match = sum(
        1 for t in cleaned
        if len(t) == 18
    )
    driving_length_18_ratio = driving_length_18_match / len(cleaned)

    # 36 → driving_all_digit_ratio 整列纯数字串占比
    driving_all_digit_match = sum(
        1 for t in cleaned
        if t.isdigit()
    )
    driving_all_digit_ratio = driving_all_digit_match / len(cleaned)

    # ==============================
    # （12）IP
    # ==============================
    # 37 → ipv4_regex_ratio IPv4 正则匹配比例
    ipv4_regex_ratio = sum(
        1 for t in cleaned
        if IPV4_REGEX.match(t)
    ) / len(cleaned)

    # （已移除 ipv4_dot_ratio：与 ipv4_regex 高度冗余）

    # 38 → ipv6_regex_ratio IPv6 正则匹配比例
    ipv6_regex_ratio = sum(
        1 for t in cleaned
        if IPV6_REGEX.match(t)
    ) / len(cleaned)

    # 40 → informix_ip_ratio Informix INET 格式 IP 比例（.A0000.00000.00001. 对应 10.0.0.1）
    informix_ip_ratio = sum(
        1 for t in cleaned
        if INFORMIX_IP_REGEX.match(t)
    ) / len(cleaned)

    # ==============================
    # （13）MAC
    # ==============================
    # 39 → MAC 正则匹配比例
    mac_regex_ratio = sum(
        1 for t in cleaned
        if MAC_REGEX.match(t)
    ) / len(cleaned)

    # 40 → mac_colon_format_ratio（冒号分隔格式比例）
    mac_colon_format_ratio = sum(
        1 for t in cleaned
        if re.fullmatch(r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', t)
    ) / len(cleaned)

    # 41 → mac_dash_format_ratio（短横线分隔格式比例）
    mac_dash_format_ratio = sum(
        1 for t in cleaned
        if re.fullmatch(r'([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}', t)
    ) / len(cleaned)

    # （已移除 mac_plain_hex_12_ratio：与 mac_regex/分格式特征重叠）

    # 42 → MAC 全为大写十六进制比例
    mac_uppercase_ratio = sum(
        1 for t in cleaned
        if re.fullmatch(r'([0-9A-F]{2}:){5}[0-9A-F]{2}', t)
    ) / len(cleaned)

    # 44 含有5个冒号占比
    mac_5_colon_ratio = sum(
        1 for t in cleaned
        if t.count(":") == 5
    ) / len(cleaned)


    # ==============================
    # （14）URL
    # ==============================
    # 45  → URL 正则匹配比例
    url_regex_ratio = sum(
        1 for t in cleaned
        if URL_REGEX.match(t)
    ) / len(cleaned)

    # 46  → 含 "://"
    url_scheme_ratio = sum(
        1 for t in cleaned
        if t.count("://") == 1
    ) / len(cleaned)

    # 47 → 含 "." 且含 "/"
    url_structure_ratio = sum(
        1 for t in cleaned
        if "." in t and "/" in t
    ) / len(cleaned)


    # 48 → url 关键字比例
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

    # 49 域名结构合法比例
    domain_structure_ratio = sum(
        1 for t in cleaned
        if DOMAIN_REGEX.match(t)
    ) / len(cleaned)

    # 50 不包含@
    url_no_at_ratio = sum(
        1 for t in cleaned
        if "@" not in t
    ) / len(cleaned)

    # 51 一般URL只包含两个冒号
    url_colon_reasonable_ratio = sum(
        1 for t in cleaned
        if 1 <= t.count(":") <= 2
    ) / len(cleaned)

    # 52
    url_letter_slash_ratio = sum(
        1 for t in cleaned
        if re.search(r'[A-Za-z]/', t)
    ) / len(cleaned)
    # 53
    url_dot_alpha_ratio = sum(
        1 for t in cleaned
        if re.search(r'[A-Za-z]\.[A-Za-z]', t)
    ) / len(cleaned)

    # ==============================
    # （15）EMAIL
    # ==============================

    # 54 → Email 正则匹配比例
    email_regex_ratio = sum(
        1 for t in cleaned
        if EMAIL_REGEX.match(t)
    ) / len(cleaned)

    # 55 → 含单个 "@"
    email_at_ratio = sum(
        1 for t in cleaned
        if t.count("@") == 1
    ) / len(cleaned)

    # ==============================
    # （16）CAR_VIN
    # ==============================
    # 56 → VIN 正则匹配比例
    vin_regex_ratio = sum(
        1 for t in cleaned
        if VIN_REGEX.match(t)
    ) / len(cleaned)

    # （已移除 vin_length_ratio：VIN 正则已约束 17 位，与 vin_regex 冗余）

    # 57 → VIN 校验位合法比例
    vin_check_digit_ratio = sum(
        1 for t in cleaned
        if vin_check_digit_valid(t)
    ) / len(cleaned)

    # 59 → VIN 校验位合法比例
    VIN_REGION_PREFIX = set("123456789ABCDEFGHJKLMNPRSTUVWXYZ")
    vin_region_prefix_ratio = sum(
        1 for t in cleaned
        if len(t) >= 1 and t[0] in VIN_REGION_PREFIX
    ) / len(cleaned)

    # 60 → VIN 不含冒号比例
    vin_no_colon_ratio = sum(
        1 for t in cleaned
        if ":" not in t
    ) / len(cleaned)

    # ==============================
    # （17）PLATE_NUMBER 车牌号
    # ==============================

    # 61 → plate_regex_ratio
    plate_regex_ratio = sum(
        1 for t in cleaned
        if (PLATE_NORMAL_REGEX.match(t.upper()) or PLATE_NEW_ENERGY_REGEX.match(t.upper()))
    ) / len(cleaned)

    # 62 → plate_province_ratio
    plate_province_ratio = sum(
        1 for t in cleaned
        if len(t) >= 1 and t[0] in province_abbr_dict
    ) / len(cleaned)

    # 63 → plate_length_ratio
    plate_length_ratio = sum(
        1 for t in cleaned
        if len(t) in (7, 8)
    ) / len(cleaned)

    # ==============================
    # （18）CHARACTER_CODE 中征码
    # ==============================

    # 65 → character_regex_ratio（严格结构匹配比例）
    character_regex_ratio = sum(
        1 for t in cleaned
        if CHAR_CODE_REGEX.fullmatch(t.strip())
    ) / len(cleaned)

    # 66 → character_length_16_ratio（长度为16比例）
    character_length_16_ratio = sum(
        1 for t in cleaned
        if len(t.strip()) == 16
    ) / len(cleaned)

    # 67 → character_suffix_digit_ratio（后13位全数字比例）
    character_suffix_digit_ratio = sum(
        1 for t in cleaned
        if len(t.strip()) == 16 and t.strip()[3:].isdigit()
    ) / len(cleaned)

    # 68 → character_check_digit_ratio（校验位合法比例）
    character_check_digit_ratio = sum(
        1 for t in cleaned
        if len(t.strip()) == 16 and character_code_check(t.strip())
    ) / len(cleaned)

    # 69 → character_no_separator_ratio（无分隔符比例）
    character_no_separator_ratio = sum(
        1 for t in cleaned
        if ":" not in t and "-" not in t and "_" not in t
    ) / len(cleaned)

    # ==============================
    # （19）DATE 年月日（不含时间）
    # ==============================

    # 70 → date_regex_ratio
    date_regex_ratio = sum(
        1 for t in cleaned
        if DATE_REGEX.match(t)
    ) / len(cleaned)

    # 71 → date_valid_ratio
    date_valid_ratio = sum(
        1 for t in cleaned
        if valid_date(t)
    ) / len(cleaned)

    # 72 → date_year_reasonable_ratio
    date_year_reasonable_ratio = 0
    for t in cleaned:
        if DATE_REGEX.match(t):
            years = re.findall(r'\d{4}', t)
            if years:
                year = int(years[0])
                if 1900 <= year <= 2100:
                    date_year_reasonable_ratio += 1

    date_year_reasonable_ratio /= len(cleaned)

    # 73 → date_separator_ratio
    date_separator_ratio = sum(
        1 for t in cleaned
        if any(sep in t for sep in ["-", "/", "."])
    ) / len(cleaned)

    # 130 → compact_date_yy_lt_21_ratio 紧凑 8 位日期前两位（世纪前缀）小于 21 的占比（最多 20 开头）
    compact_date_yy_lt_21_ratio = sum(
        1 for t in cleaned if _compact_date_yy_lt_21(t)
    ) / len(cleaned)

    # 131 → compact_date_mm_lt_24_ratio 紧凑 8 位日期第 5–6 位数值小于 24 的占比（月份字段）
    compact_date_mm_lt_24_ratio = sum(
        1 for t in cleaned if _compact_date_mm_lt_24(t)
    ) / len(cleaned)

    # 132 → compact_date_dd_lt_24_ratio 紧凑 8 位日期第 7–8 位数值小于 24 的占比（日字段）
    compact_date_dd_lt_24_ratio = sum(
        1 for t in cleaned if _compact_date_dd_lt_24(t)
    ) / len(cleaned)

    # ==============================
    # （20）DATE_TIME 年月日 + 时间
    # ==============================

    # 74 → datetime_regex_ratio
    datetime_regex_ratio = sum(
        1 for t in cleaned
        if DATE_TIME_REGEX.match(t)
    ) / len(cleaned)

    # 75 → datetime_valid_ratio
    datetime_valid_ratio = sum(
        1 for t in cleaned
        if valid_datetime(t)
    ) / len(cleaned)

    # 76 → datetime_contains_colon_ratio
    datetime_contains_colon_ratio = sum(
        1 for t in cleaned
        if ":" in t
    ) / len(cleaned)

    # 77 → datetime_length_14_ratio
    datetime_length_14_ratio = sum(
        1 for t in cleaned
        if len(t) == 14 and t.isdigit()
    ) / len(cleaned)
    # ==============================
    # （21）ACCOUNT_OPENING 开户许可证
    # ==============================

    # 78 → account_opening_regex_ratio 开户许可证正则匹配比例
    account_opening_regex_ratio = sum(
        1 for t in cleaned
        if ACCOUNT_OPENING_REGEX.match(t)
    ) / len(cleaned)

    # 79 → account_opening_length_ratio 长度为15位比例
    account_opening_length_ratio = sum(
        1 for t in cleaned
        if len(t) == 15
    ) / len(cleaned)

    # 80 → account_opening_prefix_alpha_ratio 首位为字母比例
    account_opening_prefix_alpha_ratio = sum(
        1 for t in cleaned
        if len(t) == 15 and t[0].isalpha()
    ) / len(cleaned)

    # ==============================
    # （22）COUNTRY
    # ==============================

    # 81 → country_dict_ratio 国家字典匹配比例
    country_dict_ratio = sum(
        1 for t in cleaned
        if t.strip().upper() in country_dict
    ) / len(cleaned)

    # 82 → country_alpha_ratio 纯字母比例
    country_alpha_ratio = sum(
        1 for t in cleaned
        if t.strip().isalpha()
    ) / len(cleaned)

    # 83 → country_chinese_ratio 含中文比例
    country_chinese_ratio = sum(
        1 for t in cleaned
        if any('\u4e00' <= c <= '\u9fff' for c in t)
    ) / len(cleaned)

    # 84 → country_short_length_ratio 合理长度比例（2~20）
    country_short_length_ratio = sum(
        1 for t in cleaned
        if 2 <= len(t.strip()) <= 20
    ) / len(cleaned)

    # 85 → country_ends_with_guo_ratio 以"国"结尾的比例（国家名常见，姓名极少以国结尾，用于与NAME区分）
    country_ends_with_guo_ratio = sum(
        1 for t in cleaned
        if t.strip().endswith("国")
    ) / len(cleaned)

    # ==============================
    # （23）FUNDS_NAME 产品名称（原基金名称类）
    # ==============================

    # 86 → chinese_char_ratio 中文字符占比（结构型特征）
    total_chars = sum(len(t) for t in cleaned)
    chinese_chars = sum(
        1 for t in cleaned for c in t
        if '\u4e00' <= c <= '\u9fff'
    )
    chinese_char_ratio = chinese_chars / total_chars if total_chars > 0 else 0

    # 87 → fund_keyword_ratio 行业关键词比例
    fund_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in FUND_KEYWORDS)
    ) / len(cleaned)

    # 88 → fund_name_dict_ratio 基金名称字典匹配比例
    fund_name_dict_ratio = sum(
        1 for t in cleaned
        if t.strip() in fund_name_dict
    ) / len(cleaned)

    # 89 → fund_length_reasonable_ratio 合理长度比例（4~30）
    fund_length_reasonable_ratio = sum(
        1 for t in cleaned
        if 4 <= len(t.strip()) <= 30
    ) / len(cleaned)

    # ==============================
    # （24）PASSPORT 护照
    # ==============================

    # 89 → passport_regex_ratio 护照正则匹配比例
    passport_regex_ratio = sum(
        1 for t in cleaned
        if PASSPORT_REGEX.match(t.upper())
    ) / len(cleaned)

    # 90 → passport_letter_digit_ratio 字母+数字结构比例
    passport_letter_digit_ratio = sum(
        1 for t in cleaned
        if len(t) >= 2 and t[0].isalpha() and t[1:].isdigit()
    ) / len(cleaned)

    # 91 → passport_prefix_letter_ratio 首位为字母比例
    passport_prefix_letter_ratio = sum(
        1 for t in cleaned
        if len(t) > 0 and t[0].isalpha()
    ) / len(cleaned)

    # 92 → passport_length_9_ratio 长度为9位比例
    passport_length_9_ratio = sum(
        1 for t in cleaned
        if len(t) == 9
    ) / len(cleaned)


    # ==============================
    # （25）PINYIN_NAME 拼音姓名
    # ==============================

    # 93 → pinyin_alpha_ratio 纯字母比例
    pinyin_alpha_ratio = sum(
        1 for t in cleaned
        if t.replace(" ", "").isalpha()
    ) / len(cleaned)

    # 94 → pinyin_capital_ratio 首字母大写比例
    pinyin_capital_ratio = sum(
        1 for t in cleaned
        if len(t) > 0 and t[0].isupper()
    ) / len(cleaned)

    # 95 → pinyin_space_ratio 含空格比例
    pinyin_space_ratio = sum(
        1 for t in cleaned
        if " " in t
    ) / len(cleaned)

    # 96 → pinyin_length_reasonable_ratio 合理长度比例（6~20）
    pinyin_length_reasonable_ratio = sum(
        1 for t in cleaned
        if 6 <= len(t.strip()) <= 20
    ) / len(cleaned)

    # 97 → pinyin_pure_alpha_ratio 字母+末尾可选数字
    pinyin_pure_alpha_ratio = sum(
        1 for t in cleaned if is_reasonable_pinyin(t)
    ) / len(cleaned)

    # 98 → pinyin_name_format_ratio 强格式：全小写字母+末尾可选数字，长度4~25
    pinyin_name_format_ratio = sum(
        1 for t in cleaned
        if 4 <= len(t.strip()) <= 25 and PINYIN_NAME_FORMAT.match(t.strip().lower())
    ) / len(cleaned)

    # 99 → pinyin_valid_syllables_ratio 能否拆成有效拼音音节（贪心最长匹配）
    pinyin_valid_syllables_ratio = sum(
        1 for t in cleaned
        if _is_valid_pinyin_syllable_sequence(t.strip(), PINYIN_SYLLABLES)
    ) / len(cleaned)

    # ==============================
    # （26）ENTERPRISE_NAME 企业名称
    # ==============================

    # 98 → enterprise_keyword_ratio 企业名称关键字占比
    enterprise_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in enterprise_keyword_dict)
    ) / len(cleaned)

    # 99 → enterprise_length_reasonable_ratio 长度较长比例（6~40）
    enterprise_length_reasonable_ratio = sum(
        1 for t in cleaned
        if 6 <= len(t.strip()) <= 40
    ) / len(cleaned)

    # 100 → enterprise_suffix_ratio 固定后缀占比
    enterprise_suffix_ratio = sum(
        1 for t in cleaned
        if any(t.endswith(suffix) for suffix in enterprise_suffix_dict)
    ) / len(cleaned)




    # ==============================
    # （27）ADDRESS 优化版
    # ==============================

    # 101 → address_region_ratio 行政区划关键词比例
    address_region_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in address_region_keyword_dict)
    ) / len(cleaned)

    # 102 → address_road_keyword_ratio 道路关键词比例
    address_road_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t for k in address_road_keyword_dict)
    ) / len(cleaned)

    # 103 → address_number_structure_ratio 门牌数字结构比例
    address_number_structure_ratio = sum(
        1 for t in cleaned
        if ADDRESS_NUMBER_PATTERN.search(t)
    ) / len(cleaned)

    # 104 → address_length_reasonable_ratio 合理长度比例
    address_length_reasonable_ratio = sum(
        1 for t in cleaned
        if 8 <= len(t.strip()) <= 60
    ) / len(cleaned)

    # 105 → address_multi_region_ratio 多行政层级比例（至少两个行政单位）
    address_multi_region_ratio = sum(
        1 for t in cleaned
        if sum(k in t for k in address_region_keyword_dict) >= 2
    ) / len(cleaned)

    # 106 → address_strong_pattern_ratio 地址结构强匹配（市+区+路+号）
    address_strong_pattern_ratio = sum(
        1 for t in cleaned
        if re.search(r".+市.+区.+(路|街|大道).+\d+号", t)
    ) / len(cleaned)

    # 107 → address_no_permit_keyword_ratio 排除许可证关键词比例
    address_no_permit_keyword_ratio = sum(
        1 for t in cleaned
        if not any(k in t for k in permit_strong_keyword_dict)
    ) / len(cleaned)

    # 108 → address_road_density 道路关键词密度（出现次数/长度）
    address_road_density = np.mean([
        sum(k in t for k in address_road_keyword_dict) / len(t)
        for t in cleaned
    ])

    # 109 → address_digit_tail_ratio 数字位置集中在末尾比例（地址通常数字在末尾）
    address_digit_tail_ratio = sum(
        1 for t in cleaned
        if re.search(r"\d+号?$", t.strip())
    ) / len(cleaned)

    # 地址中通常不含“第”
    address_no_di_ratio = sum(
        1 for t in cleaned
        if "第" not in t
    ) / len(cleaned)

    # 111 → address_contains_qu_ratio 含"区"比例
    address_contains_qu_ratio = sum(
        1 for t in cleaned
        if "区" in t
    ) / len(cleaned)

    # 112 → address_typical_end_ratio 地址典型结尾比例（号/栋/室/楼/层，与PERMIT区分）
    address_typical_end_ratio = sum(
        1 for t in cleaned
        if re.search(r'(号|栋|室|楼|层)$', t.strip())
    ) / len(cleaned)

    # ==============================
    # （28）NAME 中文姓名
    # ==============================
    # 111 → name_length_reasonable_ratio 合理长度比例（2~3）
    name_length_reasonable_ratio = sum(
        1 for t in cleaned
        if 2 <= len(t.strip()) <= 3
    ) / len(cleaned)


    # 112 → name_all_chinese_ratio 全为中文比例
    name_all_chinese_ratio = sum(
        1 for t in cleaned
        if len(t) >= 2 and all('\u4e00' <= c <= '\u9fff' for c in t)
    ) / len(cleaned)


    # 113 → name_surname_dict_ratio 首字或复姓前两字在姓氏字典中的比例
    name_surname_dict_ratio = sum(
        1 for t in cleaned
        if len(t) >= 2 and _surname_head_in_dict(t)
    ) / len(cleaned)


    # 114 → name_no_digit_ratio 不含数字比例
    name_no_digit_ratio = sum(
        1 for t in cleaned
        if not any(c.isdigit() for c in t)
    ) / len(cleaned)


    # 115 → name_short_length_stability 列内长度稳定性（2或3居多）
    short_lengths = [len(t) for t in cleaned if len(t) in (2, 3)]
    if short_lengths:
        name_short_length_stability = len(short_lengths) / len(cleaned)
    else:
        name_short_length_stability = 0

    # 116 → name_han_char_ratio 列内字符全为汉字占比（100% 才适合判 NAME，与 CNY 等区分）
    total_name_chars = sum(len(t) for t in cleaned)
    han_name_chars = sum(1 for t in cleaned for c in t if '\u4e00' <= c <= '\u9fff')
    name_han_char_ratio = han_name_chars / total_name_chars if total_name_chars > 0 else 0.0

    # 117 → name_2_or_3_han_ratio 每行取值恰为 2 或 3 个汉字的比例（区分姓名 vs 永昌路支行等）
    name_2_or_3_han_ratio = sum(
        1 for t in cleaned
        if 2 <= len(t) <= 3 and all('\u4e00' <= c <= '\u9fff' for c in t)
    ) / len(cleaned)

    # 118 → name_surname_head_dict_ratio 首字或复姓前两字在姓氏字典中的比例（f129，与 f109 规则一致、强化姓名列信号）
    name_surname_head_dict_ratio = sum(
        1 for t in cleaned if _surname_head_in_dict(t)
    ) / len(cleaned)

    # ==============================
    # （29）MONEY 金额
    # ==============================

    # 116 → money_numeric_ratio 纯数字或数字+小数比例
    money_numeric_ratio = sum(
        1 for t in cleaned
        if re.match(r'^[+-]?\d+(\.\d+)?$', t.replace(",", ""))
    ) / len(cleaned)


    # 117 → money_decimal_ratio 含小数比例
    money_decimal_ratio = sum(
        1 for t in cleaned
        if "." in t and re.match(r'^[+-]?\d+(\.\d+)?$', t.replace(",", ""))
    ) / len(cleaned)


    # 118 → money_currency_symbol_ratio 含货币符号比例
    money_currency_symbol_ratio = sum(
        1 for t in cleaned
        if any(sym in t for sym in ["¥", "￥", "$", "€", "£"])
    ) / len(cleaned)


    # 119 → money_reasonable_length_ratio 合理长度（1~15）
    money_reasonable_length_ratio = sum(
        1 for t in cleaned
        if 1 <= len(t.strip()) <= 15
    ) / len(cleaned)


    # 117 →
    # 120 → money_unit_ratio
    money_unit_ratio = sum(
        1 for t in cleaned
        if re.match(
            r'^[+-]?\d+(,\d{3})*(\.\d+)?\s*(元|万元|万|亿|USD|RMB|CNY)?$',
            t.replace("¥", "").replace("￥", "").strip(),
            re.IGNORECASE
        )
    ) / len(cleaned)

    # （已移除 not_character_length_16_ratio：与 character_length_16 线性完全相关 1−x）

    # default_like_keyword_ratio（含 unknown/config/test 等 DEFAULT 常见关键词，与车牌等区分）
    DEFAULT_LIKE_KEYWORDS = ["unknown", "config", "test", "default", "value", "null", "param", "data", "meta"]
    default_like_keyword_ratio = sum(
        1 for t in cleaned
        if any(k in t.lower() for k in DEFAULT_LIKE_KEYWORDS)
    ) / len(cleaned)
    # f119 槽位已改为 landline_phone_ratio（见 PHONE 段）；拼音名仍由 pinyin_* 多维特征覆盖
    # 128 → unique_value_ratio 列内取值多样性（唯一值数/总数），区分护照等高多样性 vs C10001002 等系统代码低多样性
    unique_value_ratio = len(set(t.strip() for t in cleaned)) / len(cleaned)
    # 129 → all_same_value_flag 整列全部相同值的标志（1=全部相同，0=有不同值），强信号区分系统代码列
    _unique_count = len(set(t.strip() for t in cleaned))
    all_same_value_flag = 1.0 if _unique_count == 1 else 0.0

    (
        mixed_embed_phone_ratio,
        mixed_embed_id_valid_ratio,
        mixed_embed_passport_ratio,
        mixed_embed_credit_valid_ratio,
        mixed_long_cn_digit_token_ratio,
    ) = _mixed_embedding_ratios(cleaned)

    # 133 → column_mixed_kind_diversity_ratio 列内单一敏感行种类多样性（≥2 类时 >0）
    column_mixed_kind_diversity_ratio = _column_mixed_kind_diversity_ratio(cleaned)
    # 134 → column_mixed_single_type_row_ratio 每格为单一敏感形态的行占比
    column_mixed_single_type_row_ratio = _column_mixed_single_type_row_ratio(cleaned)
    # 135 → column_mixed_intra_cell_multi_row_ratio 单格内多类型混合行占比（高则更像 MIXED 非 COLUMN_MIXED）
    column_mixed_intra_cell_multi_row_ratio = _column_mixed_intra_cell_multi_row_ratio(cleaned)

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
        bank_bin_prefix_ratio,
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

        permit_wenzi_pattern_ratio,
        permit_year_hao_ratio,
        permit_long_digit_ratio,
        permit_contains_zheng_ratio,
        permit_no_road_keyword_ratio,
        permit_not_address_pattern_ratio,
        permit_parenthesis_ratio,

        driving_length_18_ratio,
        driving_all_digit_ratio,
        ipv4_regex_ratio,
        ipv6_regex_ratio,
        informix_ip_ratio,

        mac_regex_ratio,
        mac_colon_format_ratio,
        mac_dash_format_ratio,
        mac_uppercase_ratio,
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
        vin_check_digit_ratio,
        vin_region_prefix_ratio,
        vin_no_colon_ratio,


        plate_regex_ratio,
        plate_province_ratio,
        plate_length_ratio,


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
        country_ends_with_guo_ratio,

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
        pinyin_name_format_ratio,
        pinyin_valid_syllables_ratio,

        enterprise_keyword_ratio,
        enterprise_length_reasonable_ratio,
        enterprise_suffix_ratio,

        address_region_ratio,
        address_road_keyword_ratio,
        address_number_structure_ratio,
        address_length_reasonable_ratio,
        address_multi_region_ratio,
        address_strong_pattern_ratio,
        address_no_permit_keyword_ratio,
        address_road_density,
        address_digit_tail_ratio,
        address_no_di_ratio,
        address_contains_qu_ratio,
        address_typical_end_ratio,


        name_length_reasonable_ratio,
        name_all_chinese_ratio,
        name_surname_dict_ratio,
        name_no_digit_ratio,
        name_short_length_stability,

        money_numeric_ratio,
        money_decimal_ratio,
        money_currency_symbol_ratio,
        money_reasonable_length_ratio,

        money_unit_ratio,

        default_like_keyword_ratio,
        landline_phone_ratio,
        unique_value_ratio,
        all_same_value_flag,

        mixed_embed_phone_ratio,
        mixed_embed_id_valid_ratio,
        mixed_embed_passport_ratio,
        mixed_embed_credit_valid_ratio,
        mixed_long_cn_digit_token_ratio,

        name_han_char_ratio,
        name_2_or_3_han_ratio,
        phone_digit_len_13_11_8_ratio,
        name_surname_head_dict_ratio,

        compact_date_yy_lt_21_ratio,
        compact_date_mm_lt_24_ratio,
        compact_date_dd_lt_24_ratio,

        column_mixed_kind_diversity_ratio,
        column_mixed_single_type_row_ratio,
        column_mixed_intra_cell_multi_row_ratio,
    ]

# ==============================
# （3）构造列级训练数据
# ==============================

grouped = df.groupby("column_id") #按照 column_id 把数据分组

X = []
y = []

# DEFAULT 过采样倍数：若为 2 则每个 DEFAULT 列会重复 2 次，提高 DEFAULT 样本量，减轻“总预测到相近类”
DEFAULT_OVERSAMPLE = 2

for column_id, group in grouped:
    texts = group["text"].tolist()
    label = group["label"].iloc[0]

    features = extract_column_features(texts)

    # print(f"{column_id} -> {features}")

    X.append(features)
    y.append(label)
    # 对 DEFAULT 过采样，让模型多见“不确定/杂项”样本，更倾向在模糊时预测 DEFAULT
    if label == "DEFAULT":
        for _ in range(DEFAULT_OVERSAMPLE - 1):
            X.append(features)
            y.append(label)

X = np.array(X)
y = np.array(y)

# 特征维数必须与 extract_column_features 返回值长度一致（与 Java ColumnFeatureExtractor 同步）
N_FEATURES = X.shape[1]
assert N_FEATURES == 136, f"特征维数应为 136（121 基础 + 5 MIXED + 3 姓名 + 1 电话数字长度 + 3 紧凑日期 + 3 COLUMN_MIXED，与 mask-sdk Java 一致），当前为 {N_FEATURES}，请检查 extract_column_features 的 return 长度"
feature_names = [f"f{i}" for i in range(N_FEATURES)]

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
# 类别权重：在 balanced 基础上提高 DEFAULT 权重，使模型在“不确定”时更倾向预测 DEFAULT
from sklearn.utils.class_weight import compute_class_weight
_classes = np.unique(y_train)
_balanced = compute_class_weight("balanced", classes=_classes, y=y_train)
_class_weight_dict = dict(zip(_classes, _balanced))
if "DEFAULT" in _class_weight_dict:
    _class_weight_dict["DEFAULT"] *= 1.8  # 可调 1.5~2.5，越大越容易预测 DEFAULT

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight=_class_weight_dict
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
_feature_indices = [int(n[1:]) for n in feature_names]
print("=" * 60)

# ==============================
# （7.5）保存模型
# ==============================
import os
# 主输出：mask-sdk 内置 PMML 推理资源（Java JPMML 加载）
# 可通过环境变量 MASK_SDK_RECOGNIZE_MODEL_DIR 覆盖
_DEFAULT_SDK_MODEL_DIR = r"D:\___workspace\workspace_2025_18_w_java_\datasharingplatform\mask-sdk\src\main\resources\recognize_model"
_model_dir = os.environ.get("MASK_SDK_RECOGNIZE_MODEL_DIR", _DEFAULT_SDK_MODEL_DIR).strip()
os.makedirs(_model_dir, exist_ok=True)

# joblib：备份（Java 不读；便于 Python 侧对比）
joblib.dump(model, os.path.join(_model_dir, "recognize_rf_model.joblib"))
print(f"已保存 joblib 模型: {_model_dir}/recognize_rf_model.joblib")

# PMML：Java SDK 推理必需（sklearn2pmml 在 Windows 上对目标路径敏感，先写系统临时文件再复制到 model 目录）
import shutil
import tempfile

_pmml_final = os.path.join(_model_dir, "recognize_rf_model.pmml")
_pmml_staging = None
try:
    from sklearn2pmml import sklearn2pmml
    from sklearn2pmml.pipeline import PMMLPipeline

    _X_train_df = pd.DataFrame(X_train, columns=feature_names)
    _y_train_s = pd.Series(y_train, name="label")
    _pmml_pipe = PMMLPipeline([("classifier", model)])
    _pmml_pipe.fit(_X_train_df, _y_train_s)
    try:
        _pmml_pipe.verify(_X_train_df)
    except Exception:
        pass
    with tempfile.NamedTemporaryFile(suffix=".pmml", delete=False) as tmp:
        _pmml_staging = tmp.name
    # 路径用正斜杠传给 Java，避免 D:\xxx 变成 D:xxx
    _pmml_java_path = os.path.abspath(_pmml_staging).replace("\\", "/")
    sklearn2pmml(_pmml_pipe, _pmml_java_path, with_repr=True)
    shutil.copy2(_pmml_staging, _pmml_final)
    print(f"已保存 PMML 模型: {_pmml_final}")
    print("可选后处理: python D:/___workspace/workspace_2025_18_w_java_/datasharingplatform/mask-sdk/scripts/merge_funds_into_stock_pmml.py")
except ImportError:
    print("未安装 sklearn2pmml，跳过 PMML 导出（Java 推理需要）。pip install sklearn2pmml")
except Exception as _pmml_err:
    print(f"PMML 导出失败: {_pmml_err}")
    print("提示: 若 IDE 打开了 recognize_model 目录，请先关闭相关文件后重试；或设置 MASK_SDK_RECOGNIZE_MODEL_DIR 到短路径目录。")
finally:
    if _pmml_staging and os.path.isfile(_pmml_staging):
        os.remove(_pmml_staging)

# ==============================
# 保存字典（与特征提取逻辑一致）
# ==============================
_dict_dir = os.path.join(_model_dir, "dicts")
os.makedirs(_dict_dir, exist_ok=True)

def _to_list(s):
    lst = list(s) if isinstance(s, set) else list(s)
    try:
        return sorted(lst, key=str)
    except TypeError:
        return lst

_dicts_to_save = {
    "address_region_keyword_dict": _to_list(address_region_keyword_dict),
    "address_road_keyword_dict": _to_list(address_road_keyword_dict),
    "enterprise_keyword_dict": _to_list(enterprise_keyword_dict),
    "enterprise_suffix_dict": _to_list(enterprise_suffix_dict),
    "permit_strong_keyword_dict": _to_list(permit_strong_keyword_dict),
    "province_abbr_dict": _to_list(province_abbr_dict),
    "stock_dict": _to_list(stock_dict),
    "fund_dict": _to_list(fund_dict),
    "fund_name_dict": _to_list(fund_name_dict),
    "city_dict": _to_list(city_dict),
    "surname_dict": _to_list(surname_dict),
    "country_dict": _to_list(country_dict),
    "region_dict": _to_list(region_dict),
    "FUND_KEYWORDS": FUND_KEYWORDS,
    "CREDIT_CODE_CHARS": CREDIT_CODE_CHARS,
    "WEIGHTS": WEIGHTS,
    "ID_WEIGHTS": ID_WEIGHTS,
    "ID_CHECK_MAP": {str(k): v for k, v in ID_CHECK_MAP.items()},
    "VIN_WEIGHTS": VIN_WEIGHTS,
    "VIN_TRANS": {str(k): v for k, v in VIN_TRANS.items()},
    "pinyin_syllables": sorted(PINYIN_SYLLABLES),
    "bank_bin_prefixes": sorted(bank_bin_prefixes),
}
with open(os.path.join(_dict_dir, "all_dicts.json"), "w", encoding="utf-8") as f:
    json.dump(_dicts_to_save, f, ensure_ascii=False, indent=2)
print(f"已保存字典: {_dict_dir}/all_dicts.json （特征提取与推理侧加载）")
# 银行卡 BIN 前缀同步保存到训练侧字典（与 all_dicts 内容一致）
_bank_bin_training_dir = os.path.join(_dict_root, "bank_bin")
os.makedirs(_bank_bin_training_dir, exist_ok=True)
with open(os.path.join(_bank_bin_training_dir, "bank_bin_prefixes.json"), "w", encoding="utf-8") as f:
    json.dump(sorted(bank_bin_prefixes), f, ensure_ascii=False, indent=2)
print(f"已保存银行卡BIN前缀: {_bank_bin_training_dir}/bank_bin_prefixes.json （供训练使用）")

# feature_names.json：与 extract_column_features 维顺序一致
_feature_names_path = os.path.join(_model_dir, "feature_names.json")
with open(_feature_names_path, "w", encoding="utf-8") as f:
    json.dump(feature_names, f, ensure_ascii=False, indent=2)
print(f"已保存 feature_names.json: {_feature_names_path} （共 {len(feature_names)} 维）")
print("=" * 60)

# ==============================
# （7.6）概率校准 + 用验证集选阈值，保存 confidence_thresholds.json
# ==============================
# 使用测试集作为验证集做阈值搜索（原始 predict_proba）
_proba = model.predict_proba(X_test)
model_classes = model.classes_
_default_idx = np.where(model_classes == "DEFAULT")[0]
default_idx = int(_default_idx[0]) if len(_default_idx) > 0 else -1

# 部署按类阈值：默认 0.55，ADDRESS / LANDLINE 单独 0.4（与 Java confidence_thresholds.json 一致）
DEPLOY_GLOBAL_CONFIDENCE_THRESHOLD = 0.55
DEPLOY_CLASS_CONFIDENCE_THRESHOLD = 0.55
DEPLOY_RELAXED_CLASS_THRESHOLDS = {"ADDRESS": 0.4, "LANDLINE": 0.4}
DEPLOY_DEFAULT_MIN_MARGIN = 0.08

# 全局 margin 仍用验证集搜索；按类阈值固定部署值，不再用 P10 压每类
best_global_margin = 0.08
best_acc_err = 1.0
for _margin in [0.10, 0.08, 0.05]:
    pred_label = model_classes[np.argmax(_proba, axis=1)]
    max_prob = np.max(_proba, axis=1)
    default_prob = _proba[:, default_idx] if default_idx >= 0 else 0.0
    reject = (max_prob < DEPLOY_GLOBAL_CONFIDENCE_THRESHOLD) | ((max_prob - default_prob) < _margin)
    accept = ~reject
    if accept.sum() == 0:
        continue
    accepted_correct = (pred_label[accept] == y_test[accept]).sum()
    accepted_err = 1.0 - accepted_correct / accept.sum()
    if accepted_err < best_acc_err:
        best_acc_err = accepted_err
        best_global_margin = _margin

print("（7.6）验证集 margin 搜索：default_min_margin=%.2f（接受后错误率≈%.2f%%）"
      % (best_global_margin, best_acc_err * 100))
print("（7.6）部署全局阈值：confidence_threshold=%.2f" % DEPLOY_GLOBAL_CONFIDENCE_THRESHOLD)

per_class_threshold = {c: DEPLOY_CLASS_CONFIDENCE_THRESHOLD for c in model_classes}
for _cls, _thresh in DEPLOY_RELAXED_CLASS_THRESHOLDS.items():
    if _cls in per_class_threshold:
        per_class_threshold[_cls] = _thresh

confidence_thresholds = {
    "global_confidence_threshold": DEPLOY_GLOBAL_CONFIDENCE_THRESHOLD,
    "global_default_min_margin": best_global_margin,
    "per_class_confidence_threshold": per_class_threshold,
}
with open(os.path.join(_model_dir, "confidence_thresholds.json"), "w", encoding="utf-8") as f:
    json.dump(confidence_thresholds, f, ensure_ascii=False, indent=2)
print(f"已保存 confidence_thresholds.json: {_model_dir}/confidence_thresholds.json （可按类或全局读取阈值）")

# 说明文件：避免与同级 Paddle model_freeze 混淆
_readme_path = os.path.join(_model_dir, "README.txt")
with open(_readme_path, "w", encoding="utf-8") as _rf:
    _rf.write(
        "recognize_model — mask-sdk 列类型识别模型包（RandomForest + PMML）\n"
        "============================================================\n"
        "本目录由 E 盘 rklink_002.py 训练输出，供 Java mask-sdk JPMML 本地推理。\n"
        "主要文件：\n"
        "  recognize_rf_model.pmml      — Java 推理（必需）\n"
        "  recognize_rf_model.joblib    — 备份\n"
        "  dicts/all_dicts.json         — 特征用字典\n"
        "  feature_names.json           — f0..f135（136 维）\n"
        "  confidence_thresholds.json   — 可选阈值\n"
    )
print(f"已写入说明: {_readme_path}")

# （可选）概率校准：用 CalibratedClassifierCV 在验证集上得到更接近真实置信度的概率，再跑一遍阈值搜索，仅供参考
try:
    cal = CalibratedClassifierCV(model, cv=3, method="sigmoid")
    cal.fit(X_train, y_train)
    cal_proba = cal.predict_proba(X_test)
    _best_t, _best_m, _best_e = 0.40, 0.08, 1.0
    for _t in [0.35, 0.40, 0.45, 0.50, 0.55]:
        for _m in [0.05, 0.08, 0.10]:
            _pl = model_classes[np.argmax(cal_proba, axis=1)]
            _mp = np.max(cal_proba, axis=1)
            _dp = cal_proba[:, default_idx] if default_idx >= 0 else 0.0
            _rej = (_mp < _t) | ((_mp - _dp) < _m)
            _acc = ~_rej
            if _acc.sum() == 0:
                continue
            _err = 1.0 - ( (_pl[_acc] == y_test[_acc]).sum() / _acc.sum() )
            if _err < _best_e:
                _best_e, _best_t, _best_m = _err, _t, _m
    print("（可选）若使用校准概率，推荐全局阈值≈%.2f、margin≈%.2f（接受后错误率≈%.2f%%）" % (_best_t, _best_m, _best_e * 100))
except Exception as _e:
    print("（可选）概率校准未运行:", _e)
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
# 样本数据在 test_sample/ 目录：每种类型一个文件（如 PHONE、LANDLINE）。
# JSON 格式：单组 flat list，或多组 list[list]。
# ==============================

_test_sample_dir = os.path.join(_rk002_dir, "test_sample")


def _load_test_sample_groups(type_name):
    """读取 test_sample/{type_name} 或 test_sample/{type_name}.json。"""
    for suffix in ("", ".json"):
        path = os.path.join(_test_sample_dir, type_name + suffix)
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data is None:
            return []
        if isinstance(data, list):
            return data
        raise ValueError("test_sample/%s 必须是 JSON 数组" % type_name)
    return []


def _load_all_test_columns():
    groups = {}
    if not os.path.isdir(_test_sample_dir):
        print("警告: 未找到 test_sample 目录:", _test_sample_dir)
        return groups
    for fname in sorted(os.listdir(_test_sample_dir)):
        path = os.path.join(_test_sample_dir, fname)
        if not os.path.isfile(path):
            continue
        type_name = fname[:-5] if fname.lower().endswith(".json") else fname
        groups[type_name] = _load_test_sample_groups(type_name)
    return groups


all_test_columns = _load_all_test_columns()
print("已加载 test_sample 测试列: %d 种类型, 目录=%s" % (len(all_test_columns), _test_sample_dir))


def _iter_test_column_groups(all_groups_dict):
    """支持单组 flat list 或多组 list[list]（与 MaskSdkDemo2 一致）。"""
    for label_name, groups in all_groups_dict.items():
        if not groups:
            continue
        if isinstance(groups[0], (list, tuple)):
            total = len(groups)
            for idx, column in enumerate(groups, start=1):
                yield label_name, idx, total, column
        else:
            yield label_name, 1, 1, groups


# ==============================
# 推理后处理（与 Java RecognizeOverrideSupport.applyPythonAligned 对齐）
# ==============================

def _looks_like_chinese_name_column(text_list):
    """整列 2~3 字中文、无数字、无公司/集团后缀，首字或复姓前两字在姓氏字典命中率 ≥75%。"""
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return False
    n = len(cleaned)
    surname_hit = 0
    for t in cleaned:
        if len(t) < 2 or len(t) > 3:
            return False
        if any(x in t for x in ("公司", "有限", "集团")):
            return False
        if any(c.isdigit() for c in t):
            return False
        if not all("\u4e00" <= c <= "\u9fff" for c in t):
            return False
        if _surname_head_in_dict(t):
            surname_hit += 1
    return surname_hit / n >= NAME_SURNAME_HEAD_MIN_RATIO


def _name_column_han_char_ratio(text_list):
    """列内所有字符中汉字占比（0~1）。"""
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return 0.0
    total = sum(len(t) for t in cleaned)
    if total <= 0:
        return 0.0
    han = sum(1 for t in cleaned for c in t if '\u4e00' <= c <= '\u9fff')
    return han / total


def _name_column_2_or_3_han_row_ratio(text_list):
    """列内「恰为 2 或 3 个汉字」的取值占比（0~1）。"""
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return 0.0
    hit = sum(
        1 for t in cleaned
        if 2 <= len(t) <= 3 and all('\u4e00' <= c <= '\u9fff' for c in t)
    )
    return hit / len(cleaned)


def _name_column_surname_head_dict_ratio(text_list):
    """列内首字或复姓前两字在姓氏字典中的占比（0~1）。"""
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return 0.0
    hit = sum(1 for t in cleaned if _surname_head_in_dict(t))
    return hit / len(cleaned)


NAME_2_OR_3_HAN_MIN_RATIO = 0.75
# 姓名列：每一行首字或复姓前两字均须在姓氏字典中 → 列级占比须 100%
NAME_SURNAME_HEAD_MIN_RATIO = 1.0
# 非姓名排除：民族「X族」、性别/占位等 + country_dict 纯汉字国名
EXCLUDED_NAME_MANUAL_EXACT_TOKENS = frozenset({
    "男", "女", "未知", "不详", "其他", "无", "暂无", "成功", "法人", "法人股", "法官证",
    "银丰", "海南", "金融", "在营", "行政区", "银行", "行业", "金额",
    "年龄", "年度", "年月", "年份", "年薪", "年金", "年报", "年限",
    "是", "是否", "是非", "是的", "是这样", "是对", "是对的", "是吗", "是有", "是在", "是不是",
    "水电费", "归档", "兰州", "查证", "国债", "国债券", "成都",
})
# 「是」开头时第二字为下列字符则视为明显非人名（保留姓「是」+ 名如「是伟」）
_SHI_PREFIX_NON_NAME_SECOND_CHARS = frozenset("否非对这吗有的不在因真还就也都只可被从要会能应该")
EXCLUDED_NAME_EXACT_TOKENS = EXCLUDED_NAME_MANUAL_EXACT_TOKENS | COUNTRY_NAME_HAN_EXACT_TOKENS
# 列内任一黑名单取值单独占比 ≥ 此值时整列不按 NAME（与 Java NameRecognizeHeuristics 一致）
EXCLUDED_NAME_COLUMN_MIN_RATIO = 0.5


def _is_shi_prefix_excluded_non_name(text):
    t = str(text).strip()
    if t == "是":
        return True
    if len(t) >= 2 and t[0] == "是" and t[1] in _SHI_PREFIX_NON_NAME_SECOND_CHARS:
        return True
    return False


def _is_excluded_name_like_value(text):
    t = str(text).strip()
    if not t:
        return False
    if t in EXCLUDED_NAME_EXACT_TOKENS:
        return True
    if len(t) >= 2 and t.endswith("族") and all("\u4e00" <= c <= "\u9fff" for c in t):
        return True
    if _is_shi_prefix_excluded_non_name(t):
        return True
    return False


def _looks_like_excluded_name_column(text_list):
    """列内是否存在单个黑名单取值，其出现次数占非空行数 ≥ EXCLUDED_NAME_COLUMN_MIN_RATIO。"""
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if not cleaned:
        return False
    n = len(cleaned)
    freq = {}
    for t in cleaned:
        freq[t] = freq.get(t, 0) + 1
    for value, count in freq.items():
        if _is_excluded_name_like_value(value) and count / n >= EXCLUDED_NAME_COLUMN_MIN_RATIO:
            return True
    return False

# 部署置信度阈值（与 Java masks.recognize-confidence-threshold / RecognizeThresholdProvider 默认 0.55 一致）
# 训练后会写入 confidence_thresholds.json；测试推理优先读该文件，可用环境变量覆盖
DEFAULT_DEPLOY_CONFIDENCE_THRESHOLD = 0.55
DEFAULT_DEPLOY_MIN_MARGIN = 0.08


def apply_confidence_gate(predicted, probability, classes, confidence_threshold=0.55, default_min_margin=0.08,
                          per_class_threshold=None):
    """
    置信度回退：与 Java RKLinkMaskSdkImpl 一致。
    按预测类读取 per_class_threshold，缺失时用 confidence_threshold（全局默认 0.55）。
    当预测类概率 < 类阈值，或 (预测类概率 - DEFAULT 概率) < default_min_margin 时 → DEFAULT。
    """
    if predicted is None or predicted == "DEFAULT":
        return predicted
    proba = np.asarray(probability, dtype=float)
    class_list = list(classes)
    if predicted not in class_list:
        return predicted
    pred_p = float(proba[class_list.index(predicted)])
    default_p = 0.0
    if "DEFAULT" in class_list:
        default_p = float(proba[class_list.index("DEFAULT")])
    thresh = confidence_threshold
    if per_class_threshold and predicted in per_class_threshold:
        thresh = float(per_class_threshold[predicted])
    if pred_p < thresh or (pred_p - default_p) < default_min_margin:
        return "DEFAULT"
    return predicted


def _load_deploy_confidence_config(model_dir=None):
    """读取 confidence_thresholds.json；缺失时回退默认（与 Java RecognizeModelLoader 一致）。"""
    thresh = DEFAULT_DEPLOY_CONFIDENCE_THRESHOLD
    margin = DEFAULT_DEPLOY_MIN_MARGIN
    per_class = dict(DEPLOY_RELAXED_CLASS_THRESHOLDS)
    env_thresh = os.environ.get("MASK_SDK_RECOGNIZE_CONFIDENCE_THRESHOLD", "").strip()
    if env_thresh:
        try:
            thresh = float(env_thresh)
        except ValueError:
            pass
    path = None
    if model_dir:
        path = os.path.join(model_dir, "confidence_thresholds.json")
    if path and os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            if not env_thresh and cfg.get("global_confidence_threshold") is not None:
                thresh = float(cfg["global_confidence_threshold"])
            if cfg.get("global_default_min_margin") is not None:
                margin = float(cfg["global_default_min_margin"])
            pc = cfg.get("per_class_confidence_threshold")
            if isinstance(pc, dict):
                per_class = {str(k): float(v) for k, v in pc.items()}
        except (OSError, ValueError, TypeError):
            pass
    return thresh, margin, per_class


def apply_recognize_overrides(predicted, text_list):
    cleaned = [str(t).strip() for t in text_list if t is not None and str(t).strip()]
    if cleaned:
        if _looks_like_strict_mobile_column(text_list) and predicted in (
                "IP", "DEFAULT", "DATE", "DATE_TIME", "MAC", "CAR_VIN", "LANDLINE"):
            return "PHONE"
        if _looks_like_strict_landline_column(text_list) and predicted in (
                "IP", "DEFAULT", "DATE", "DATE_TIME", "MAC", "CAR_VIN", "PHONE"):
            return "LANDLINE"
    if predicted == "PHONE" and not _looks_like_strict_mobile_column(text_list):
        return "DEFAULT"
    if predicted == "LANDLINE" and not _looks_like_strict_landline_column(text_list):
        return "DEFAULT"
    if predicted == "DATE" and not _looks_like_strict_date_column(text_list):
        return "DEFAULT"
    if predicted == "DATE_TIME" and not _looks_like_strict_datetime_column(text_list):
        return "DEFAULT"
    if predicted == "ID_CARD" and not _looks_like_strict_id_card_column(text_list):
        return "DEFAULT"
    if cleaned:
        if _looks_like_column_mixed_column(text_list) and predicted in (
                "DEFAULT", "PHONE", "LANDLINE", "ID_CARD", "PASSPORT", "CREDIT_CODE", "EMAIL", "MIXED"):
            return "COLUMN_MIXED"
    if predicted == "COLUMN_MIXED" and not _looks_like_column_mixed_column(text_list):
        return "DEFAULT"
    if predicted == "NAME" and _looks_like_excluded_name_column(text_list):
        return "DEFAULT"
    if predicted == "NAME" and _name_column_han_char_ratio(text_list) < 1.0:
        return "DEFAULT"
    if predicted == "NAME" and _name_column_2_or_3_han_row_ratio(text_list) < NAME_2_OR_3_HAN_MIN_RATIO:
        return "DEFAULT"
    if predicted == "NAME" and _name_column_surname_head_dict_ratio(text_list) < NAME_SURNAME_HEAD_MIN_RATIO:
        return "DEFAULT"
    if predicted == "DEFAULT" and _looks_like_chinese_name_column(text_list) and not _looks_like_excluded_name_column(text_list):
        return "NAME"
    return predicted

# ==============================
# 循环预测（与 Java SDK：PMML → 置信度门控 → apply_recognize_overrides）
# ==============================

_deploy_confidence_threshold, _deploy_default_min_margin, _deploy_per_class_threshold = _load_deploy_confidence_config(_model_dir)
print("=" * 60)
print("测试推理部署参数：global_threshold=%.2f, default_min_margin=%.2f, ADDRESS=%.2f, LANDLINE=%.2f（与 Java SDK 一致）"
      % (_deploy_confidence_threshold, _deploy_default_min_margin,
         _deploy_per_class_threshold.get("ADDRESS", _deploy_confidence_threshold),
         _deploy_per_class_threshold.get("LANDLINE", _deploy_confidence_threshold)))

for label_name, group_idx, group_total, test_column in _iter_test_column_groups(all_test_columns):

    feature = extract_column_features(test_column)
    feature_subset = [feature[i] for i in _feature_indices]
    probability = model.predict_proba([feature_subset])[0]
    raw_prediction = model.predict([feature_subset])[0]
    after_gate = apply_confidence_gate(
        raw_prediction, probability, model.classes_,
        _deploy_confidence_threshold, _deploy_default_min_margin,
        _deploy_per_class_threshold,
    )
    prediction = apply_recognize_overrides(after_gate, test_column)

    print("\n==============================")
    if group_total > 1:
        print("测试类型:", "%s#%d/%d" % (label_name, group_idx, group_total))
    else:
        print("测试类型:", label_name)
    print("模型预测:", raw_prediction)
    if after_gate != raw_prediction:
        print("置信度门控后:", after_gate)
    if prediction != after_gate:
        print("规则后处理:", prediction)
    print("预测类别(最终):", prediction)
    print("姓名特征 f129 name_surname_head_dict_ratio: %.4f（须=1.0 才保留 NAME）"
          % feature[129])
    print("手机严格校验 looks_like_strict_mobile_column: %s"
          % _looks_like_strict_mobile_column(test_column))
    print("固话严格校验 looks_like_strict_landline_column: %s"
          % _looks_like_strict_landline_column(test_column))
    print("身份证严格校验 looks_like_strict_id_card_column: %s"
          % _looks_like_strict_id_card_column(test_column))
    print("日期严格校验 looks_like_strict_date_column: %s"
          % _looks_like_strict_date_column(test_column))
    print("多行混合严格校验 looks_like_column_mixed_column: %s"
          % _looks_like_column_mixed_column(test_column))
    if len(feature) >= 136:
        print("紧凑日期 f130/f131/f132: %.4f / %.4f / %.4f"
              % (feature[130], feature[131], feature[132]))
        print("多行混合 f133/f134/f135: %.4f / %.4f / %.4f"
              % (feature[133], feature[134], feature[135]))
    elif len(feature) >= 133:
        print("紧凑日期 f130/f131/f132: %.4f / %.4f / %.4f"
              % (feature[130], feature[131], feature[132]))

    # 打印概率排序（从高到低）—— 仍为模型原始 predict_proba，不随后处理改变
    sorted_probs = sorted(
        zip(model.classes_, probability),
        key=lambda x: x[1],
        reverse=True
    )

    print("置信度,概率分布:")
    for cls, prob in sorted_probs[:5]:   # 只显示前5个最高概率
        print(f"{cls}: {prob:.4f}")


