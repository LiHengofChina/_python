"""
将 fit_data 各类型正例补齐到 TARGET_ROWS（默认 540），且每文件内 text 全局唯一。
仅生成新样本，不从已有池抽样复制；每列约 ROWS_PER_COL 行。
"""
import json
import os
import random
import re
from datetime import date, timedelta

import pandas as pd

from purify_fit_data import CREDIT_CODE_CHARS, purify_row

_FIT_DIR = os.path.dirname(os.path.abspath(__file__))
_RK002_DIR = os.path.dirname(_FIT_DIR)
_DICT_ROOT = os.path.join(_RK002_DIR, "dict")

TARGET_ROWS = 540
ROWS_PER_COL = 10
GEN_MAX_TRIES = 500
RNG = random.Random(42)

PHONE_REGEX = re.compile(r"^1[3-9]\d{9}$")
ID_REGEX = re.compile(r"^\d{17}[\dXx]$")
PLATE_REGEX = re.compile(r"^[\u4e00-\u9fa5][A-Z][A-HJ-NP-Z0-9]{5,6}$")
VIN_REGEX = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")
MAC_REGEX = re.compile(
    r"^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$|^[0-9A-Fa-f]{12}$"
)
IP_REGEX = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)
URL_REGEX = re.compile(r"^https?://[^\s]+", re.I)
AO_REGEX = re.compile(r"^[JK]\d{12,14}$")
OFFICER_REGEX = re.compile(r"^[军海空武]字第\d{4,6}号$")
GIVEN_CHARS = "伟芳娜敏静丽强磊洋勇军杰明华建国国强志强秀英玉兰桂英丽娟秀兰"
CITIES = [
    "北京市", "上海市", "深圳市", "广州市", "杭州市", "成都市", "南京市", "武汉市",
    "重庆市", "天津市", "苏州市", "西安市", "厦门市", "青岛市", "大连市", "长沙市",
]
DISTRICTS = ["朝阳区", "浦东新区", "南山区", "天河区", "西湖区", "高新区", "鼓楼区", "渝北区", "福田区", "武侯区"]
ROADS = ["建国路", "世纪大道", "科技园路", "体育西路", "文三路", "天府大道", "中山北路", "人民路", "解放路"]
ENT_SUFFIX = ["有限公司", "股份有限公司", "集团有限公司", "科技有限公司", "实业有限公司"]
ENT_CORE = ["华夏", "恒远", "博瑞", "智汇", "云联", "信达", "鸿泰", "博雅", "英迪", "瑞达", "腾迅", "中科"]
PLATE_PROV = ["粤", "京", "沪", "浙", "川", "苏", "赣", "津", "渝", "闽", "鲁", "豫"]
FUND_SUFFIX = ["混合", "债券A", "债券C", "股票", "ETF", "货币", "精选混合", "成长混合", "纯债债券C"]
PINYIN_SUR = [
    "Zhang", "Li", "Wang", "Chen", "Liu", "Zhao", "Sun", "Zhou", "Wu", "Xu",
    "Huang", "Lin", "He", "Gao", "Luo", "Zheng", "Tang", "Feng", "Yu", "Dong",
    "Xiao", "Cheng", "Yuan", "Deng", "Fu", "Shen", "Lu", "Ding", "Ren", "Yao",
]
PINYIN_GIVEN = [
    "San", "Si", "Wei", "Hao", "Yang", "Lei", "Li", "Jie", "Min", "Fang",
    "Jun", "Yan", "Ping", "Tao", "Bo", "Qiang", "Na", "Lin", "Xin", "Kai",
    "Lan", "Hong", "Jing", "Ting", "Xue", "Mei", "Long", "Peng", "Chao", "Bin",
]
MIXED_TEMPLATES = [
    "联系人{name} 手机{phone} 证件{id}",
    "{city}{ent} 经办{name} {phone} {passport} 主体{credit}",
    "{name} {phone} {passport}",
    "客户{name}，护照号{passport}，统一码{credit}",
    "{city}{ent} {phone} {credit}",
    "申请人{name} 电话{phone} 护照{passport}",
    "{ent} 联系人{name} {phone} 统一社会信用代码{credit}",
]
_SEQ = 0


def _load_dicts():
    stock_df = pd.read_csv(
        os.path.join(_DICT_ROOT, "stock_fund", "stock_code_dict.csv"), dtype=str
    )
    fund_df = pd.read_csv(
        os.path.join(_DICT_ROOT, "stock_fund", "fund_code_dict.csv"), dtype=str
    )
    city_df = pd.read_csv(os.path.join(_DICT_ROOT, "cities", "city_dict.csv"), dtype=str)
    country_df = pd.read_csv(os.path.join(_DICT_ROOT, "country", "country_dict.csv"), dtype=str)
    with open(os.path.join(_DICT_ROOT, "chinesename", "surname_dict.json"), encoding="utf-8") as f:
        surname_list = json.load(f)
    stock_codes = [c.zfill(6) for c in stock_df["code"].astype(str) if re.fullmatch(r"\d{1,6}", c)]
    fund_names = [n for n in fund_df["基金简称"].astype(str).str.strip().tolist() if n and n != "nan"]
    cities = city_df.iloc[:, 0].astype(str).tolist()
    countries = [c for c in country_df.iloc[:, 0].astype(str).tolist() if c and c != "nan"]
    surnames = [s for s in surname_list if s and isinstance(s, str)]
    return stock_codes, fund_names, cities, countries, surnames


STOCK_CODES, FUND_NAMES, CITY_DICT, COUNTRY_LIST, SURNAMES = _load_dicts()


def is_positive(label, text):
    ok, _ = purify_row(label, text)
    if label in {
        "STOCK_CODE", "NAME", "PHONE", "ID_CARD", "FUNDS_NAME",
        "CREDIT_CODE", "PASSPORT", "EMAIL", "DATE",
    }:
        return ok
    t = str(text).strip()
    if not t:
        return False
    checks = {
        "BANK_CARD": lambda x: bool(re.fullmatch(r"\d{16,19}", x)),
        "LANDLINE": lambda x: (
            not PHONE_REGEX.fullmatch(x)
            and len(x) >= 7
            and bool(re.search(r"\d", x))
            and not ID_REGEX.fullmatch(x)
        ),
        "IP": lambda x: bool(IP_REGEX.fullmatch(x)),
        "MAC": lambda x: bool(MAC_REGEX.fullmatch(x)),
        "URL": lambda x: bool(URL_REGEX.fullmatch(x)),
        "ADDRESS": lambda x: bool(
            re.search(r"[\u4e00-\u9fff]", x)
            and re.search(r"(省|市|区|县|路|街|号|道|园|镇|乡)", x)
        ),
        "ENTERPRISE_NAME": lambda x: bool(
            re.search(r"[\u4e00-\u9fff]", x)
            and re.search(r"(公司|集团|有限|股份)", x)
        ),
        "CAR_VIN": lambda x: bool(VIN_REGEX.fullmatch(x.upper())),
        "PLATE_NUMBER": lambda x: bool(PLATE_REGEX.fullmatch(x)),
        "MONEY": lambda x: bool(
            re.fullmatch(r"-?\d+(\.\d+)?", x)
            or re.fullmatch(r"-?\d+(\.\d+)?万元", x)
            or re.fullmatch(r"[¥$]\d+(\.\d+)?", x)
        ),
        "PINYIN_NAME": lambda x: bool(re.fullmatch(r"[A-Z][a-z]+([A-Z][a-z]+)?", x)),
        "DATE_TIME": lambda x: bool(
            re.fullmatch(r"\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\s+\d{1,2}:\d{2}(:\d{2})?", x)
            or re.fullmatch(r"\d{14}", x)
        ),
        "COUNTRY": lambda x: bool(x) and len(x) <= 40,
        "OFFICER_CARD": lambda x: bool(OFFICER_REGEX.fullmatch(x)),
        "PERMIT": lambda x: bool(re.search(r"(许可|证|卫消证|经营)", x) and len(x) >= 8),
        "ACCOUNT_OPENING": lambda x: bool(AO_REGEX.fullmatch(x)),
        "CHARACTER_CODE": lambda x: bool(
            re.fullmatch(r"[A-Z0-9]{10,20}", x) and re.search(r"[A-Z]", x) and re.search(r"\d", x)
        ),
        "DEFAULT": lambda x: (
            len(x) <= 80
            and not PHONE_REGEX.fullmatch(x)
            and not ID_REGEX.fullmatch(x)
            and not re.fullmatch(r"\d{6}", x)
            and "@" not in x
        ),
        "MIXED": lambda x: (
            len(x) >= 12
            and sum(
                1
                for pat in (r"1[3-9]\d{9}", r"\d{17}[\dXx]", r"[A-Z]\d{7,8}", r"91\d{16}")
                if re.search(pat, x, re.I)
            )
            >= 2
        ),
        "COLUMN_MIXED": lambda x: (
            bool(PHONE_REGEX.fullmatch(x))
            or (bool(re.search(r"[-]\d", x)) and len(x) >= 7 and not PHONE_REGEX.fullmatch(x))
            or bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]{2,}", x))
            or bool(re.fullmatch(r"^\d{17}[\dXx]$", x))
            or bool(re.fullmatch(r"^[A-Z]{1,2}\d{7,8}$", x.upper()))
            or bool(re.fullmatch(r"^[0-9A-Z]{18}$", x.upper()))
            or (len(x) <= 6 and x.isdigit())
        ),
    }
    fn = checks.get(label)
    return fn(t) if fn else True


def _next_seq():
    global _SEQ
    _SEQ += 1
    return _SEQ


def _rand_phone():
    return "1" + str(RNG.randint(3, 9)) + "".join(str(RNG.randint(0, 9)) for _ in range(9))


def _rand_name():
    s = RNG.choice(SURNAMES)
    n = RNG.randint(1, 2)
    return s + "".join(RNG.choice(GIVEN_CHARS) for _ in range(n))


def _rand_id():
    area = RNG.choice(["110105", "440106", "320311", "330102", "510107", "440305", "310115"])
    birth = date(RNG.randint(1970, 2000), RNG.randint(1, 12), RNG.randint(1, 28))
    seq = RNG.randint(1, 999)
    body = f"{area}{birth.strftime('%Y%m%d')}{seq:03d}"
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_map = "10X98765432"
    s = sum(int(body[i]) * weights[i] for i in range(17))
    return body + check_map[s % 11]


def _rand_credit():
    prefix = RNG.choice(["91110000", "91310000", "91440300", "91510100", "91330100", "91440101"])
    tail_len = 18 - len(prefix)
    tail = "".join(RNG.choice(CREDIT_CODE_CHARS) for _ in range(tail_len))
    return (prefix + tail)[:18]


def _rand_passport():
    letters = RNG.choice(["E", "G", "P", "D", "K"]) + RNG.choice(["", "A", "B", "C"])
    digits = "".join(str(RNG.randint(0, 9)) for _ in range(RNG.choice([7, 8])))
    return letters + digits


def _rand_date():
    base = date(1990, 1, 1) + timedelta(days=RNG.randint(0, 12000))
    fmt = RNG.choice(["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y%m%d"])
    return base.strftime(fmt)


def _rand_email():
    seq = _next_seq()
    domain = RNG.choice(["test.com", "example.org", "mail.cn", "corp.com", "demo.net"])
    return f"user{seq}@{domain}"


def _rand_landline():
    seq = _next_seq()
    kind = seq % 4
    if kind == 0:
        return f"0{RNG.randint(10, 29)}-{RNG.randint(10000000, 99999999)}"
    if kind == 1:
        return f"400-{RNG.randint(100, 999)}-{RNG.randint(1000, 9999)}"
    if kind == 2:
        return f"800-{RNG.randint(1000000, 9999999)}"
    return f"0{RNG.randint(100, 999)}-{RNG.randint(1000000, 9999999)}"


def _rand_bank():
    prefix = RNG.choice(["622202", "622848", "621700", "621226", "622588", "621483"])
    rest = "".join(str(RNG.randint(0, 9)) for _ in range(16 - len(prefix)))
    return prefix + rest


def _rand_address():
    seq = _next_seq()
    city = RNG.choice(CITIES)
    district = RNG.choice(DISTRICTS)
    road = RNG.choice(ROADS)
    return f"{city}{district}{road}{seq}号"


def _rand_enterprise():
    seq = _next_seq()
    return RNG.choice(CITIES) + RNG.choice(ENT_CORE) + f"{seq}" + RNG.choice(ENT_SUFFIX)


def _rand_plate():
    prov = RNG.choice(PLATE_PROV)
    letter = RNG.choice("ABCDEFGHJKLMNPQRSTUVWXYZ")
    tail = "".join(RNG.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(5))
    return prov + letter + tail


def _rand_vin():
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    return "".join(RNG.choice(chars) for _ in range(17))


def _rand_mac():
    parts = [f"{RNG.randint(0, 255):02X}" for _ in range(6)]
    sep = RNG.choice([":", "-", ""])
    return sep.join(parts) if sep else "".join(parts)


def _rand_ip():
    return (
        f"{RNG.randint(1, 223)}.{RNG.randint(0, 255)}.{RNG.randint(0, 255)}.{RNG.randint(1, 254)}"
    )


def _rand_url():
    seq = _next_seq()
    host = RNG.choice(["www", "api", "shop", "news", "cdn"])
    tld = RNG.choice(["example.com", "test.cn", "demo.org", "sample.net"])
    return f"https://{host}{seq}.{tld}/p/{seq}"


def _rand_money():
    seq = _next_seq()
    kind = seq % 3
    if kind == 0:
        return str(RNG.randint(1, 999999))
    if kind == 1:
        return f"{RNG.randint(1, 99999)}.{RNG.randint(0, 99):02d}"
    return f"¥{RNG.randint(100, 999999)}"


def _rand_pinyin():
    return RNG.choice(PINYIN_SUR) + RNG.choice(PINYIN_GIVEN)


def _rand_datetime():
    base = date(2015, 1, 1) + timedelta(days=RNG.randint(0, 3600))
    h, m, s = RNG.randint(0, 23), RNG.randint(0, 59), RNG.randint(0, 59)
    if RNG.random() < 0.5:
        return f"{base.strftime('%Y-%m-%d')} {h:02d}:{m:02d}:{s:02d}"
    return f"{base.strftime('%Y/%m/%d')} {h:02d}:{m:02d}"


def _rand_officer():
    prefix = RNG.choice(["军", "海", "空", "武"])
    num = RNG.randint(201500, 202499)
    return f"{prefix}字第{num}号"


def _rand_permit():
    prov = RNG.choice(["粤", "苏", "沪", "川", "浙", "赣", "京", "津"])
    year = RNG.randint(2016, 2024)
    seq = RNG.randint(1, 99999)
    kind = seq % 3
    if kind == 0:
        return f"{prov}食药监械经营许{year}{seq:05d}号"
    if kind == 1:
        return f"{prov}卫消证字({year})第{seq:04d}号"
    return f"经营许可证编号{year}{seq:05d}"


def _rand_account_opening():
    return RNG.choice(["J", "K"]) + "".join(str(RNG.randint(0, 9)) for _ in range(RNG.choice([12, 13, 14])))


def _rand_character_code():
    lead = "".join(RNG.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(RNG.randint(2, 4)))
    digits = "".join(str(RNG.randint(0, 9)) for _ in range(RNG.randint(8, 14)))
    return lead + digits


def _rand_mixed():
    tpl = RNG.choice(MIXED_TEMPLATES)
    return tpl.format(
        name=_rand_name(),
        phone=_rand_phone(),
        id=_rand_id(),
        passport=_rand_passport(),
        credit=_rand_credit(),
        city=RNG.choice(CITIES),
        ent=RNG.choice(ENT_CORE) + str(_next_seq()) + RNG.choice(ENT_SUFFIX),
    )


def _rand_default():
    seq = _next_seq()
    kind = seq % 8
    samples = [
        f"config_key_{seq}",
        f"meta_field_{seq}",
        f"sample_value_{seq}",
        f"debug_item_{seq}",
        f"batch_no_{seq}",
        f"remark_{seq}",
        f"temp_data_{seq}",
        f"row_tag_{seq}",
    ]
    return samples[kind]


def _rand_country():
    pool = list(dict.fromkeys(COUNTRY_LIST + ["中国", "美国", "日本", "英国", "法国", "德国", "韩国", "加拿大"]))
    return RNG.choice(pool)


def _gen_candidate(label):
    gens = {
        "STOCK_CODE": lambda: RNG.choice(STOCK_CODES).zfill(6),
        "NAME": _rand_name,
        "PHONE": _rand_phone,
        "ID_CARD": _rand_id,
        "FUNDS_NAME": lambda: (
            RNG.choice(FUND_NAMES)
            if FUND_NAMES and RNG.random() < 0.6
            else RNG.choice(["华夏", "易方达", "南方", "广发", "招商", "中欧", "博时", "嘉实", "富国"])
            + str(_next_seq() % 1000)
            + RNG.choice(FUND_SUFFIX)
        ),
        "CREDIT_CODE": _rand_credit,
        "PASSPORT": _rand_passport,
        "EMAIL": _rand_email,
        "DATE": _rand_date,
        "BANK_CARD": _rand_bank,
        "LANDLINE": _rand_landline,
        "IP": _rand_ip,
        "MAC": _rand_mac,
        "URL": _rand_url,
        "ADDRESS": _rand_address,
        "ENTERPRISE_NAME": _rand_enterprise,
        "CAR_VIN": _rand_vin,
        "PLATE_NUMBER": _rand_plate,
        "MONEY": _rand_money,
        "PINYIN_NAME": _rand_pinyin,
        "DATE_TIME": _rand_datetime,
        "COUNTRY": _rand_country,
        "OFFICER_CARD": _rand_officer,
        "PERMIT": _rand_permit,
        "ACCOUNT_OPENING": _rand_account_opening,
        "CHARACTER_CODE": _rand_character_code,
        "DEFAULT": _rand_default,
        "MIXED": _rand_mixed,
        "COLUMN_MIXED": _rand_landline,
    }
    gen = gens.get(label)
    if not gen:
        return None
    t = gen()
    if label == "CREDIT_CODE":
        t = t.upper()
    elif label == "PASSPORT":
        t = t.upper()
    elif label == "STOCK_CODE" and re.fullmatch(r"\d+", str(t)):
        t = str(t).zfill(6)
    return t


def _gen_unique(label, used):
    for _ in range(GEN_MAX_TRIES):
        t = _gen_candidate(label)
        if t is None:
            continue
        t = str(t).strip()
        if t in used:
            continue
        if not is_positive(label, t):
            continue
        used.add(t)
        return t
    return None


def _infer_col_prefix(df):
    sample = str(df["column_id"].iloc[0])
    m = re.match(r"^(.*_)\d+$", sample)
    if m:
        return m.group(1)
    m = re.match(r"^(.+_col_)", sample)
    if m:
        return m.group(1)
    return sample.rsplit("_", 1)[0] + "_"


def _max_col_index(df, prefix):
    mx = 0
    for cid in df["column_id"].astype(str):
        if cid.startswith(prefix):
            tail = cid[len(prefix):]
            if tail.isdigit():
                mx = max(mx, int(tail))
    return mx


def augment_label(label, target=TARGET_ROWS):
    path = os.path.join(_FIT_DIR, f"{label}.csv")
    if not os.path.isfile(path):
        return None
    df = pd.read_csv(path, dtype={"text": str, "column_id": str})
    df["text"] = df["text"].astype(str).str.strip()
    before = len(df)
    used = set(df["text"].tolist())
    if before >= target and len(used) == before:
        return before, before, 0

    prefix = _infer_col_prefix(df)
    col_idx = _max_col_index(df, prefix)
    new_rows = list(df.to_dict("records"))

    while len(new_rows) < target:
        col_idx += 1
        col_id = f"{prefix}{col_idx}"
        need = min(ROWS_PER_COL, target - len(new_rows))
        col_texts = []
        for _ in range(need):
            t = _gen_unique(label, used)
            if t is None:
                break
            col_texts.append(t)
        if not col_texts:
            break
        for t in col_texts:
            new_rows.append({"column_id": col_id, "text": t, "label": label})

    out = pd.DataFrame(new_rows)
    out.to_csv(path, index=False, encoding="utf-8")
    after = len(out)
    return before, after, after - before


def main():
    global _SEQ
    _SEQ = 0
    files = sorted(f[:-4] for f in os.listdir(_FIT_DIR) if f.endswith(".csv"))
    print(f"目标: {TARGET_ROWS} 行/类, 每文件 text 唯一, 每列约 {ROWS_PER_COL} 行")
    print(f"目录: {_FIT_DIR}\n")
    total_added = 0
    for label in files:
        r = augment_label(label)
        if r is None:
            continue
        b, a, add = r
        total_added += max(0, add)
        uniq = pd.read_csv(os.path.join(_FIT_DIR, f"{label}.csv"), dtype={"text": str})["text"].nunique()
        flag = " OK" if a == TARGET_ROWS and uniq == a else " WARN"
        print(f"  {label}: {b} -> {a} (+{add}), unique={uniq}{flag}")
    print(f"\n合计净增: {total_added} 行")


if __name__ == "__main__":
    main()
