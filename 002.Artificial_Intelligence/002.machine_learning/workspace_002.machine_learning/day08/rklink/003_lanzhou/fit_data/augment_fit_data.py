"""
将 fit_data 兰州 9 类正例补齐到 TARGET_ROWS（默认 540），且每文件内 text 全局唯一。
仅生成新样本；每列约 ROWS_PER_COL 行。
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

KEEP_LABELS = [
    "DEFAULT",
    "NAME",
    "PHONE",
    "LANDLINE",
    "CREDIT_CODE",
    "ID_CARD",
    "OFFICER_CARD",
    "PASSPORT",
    "ENTERPRISE_NAME",
]

TARGET_ROWS = 540
ROWS_PER_COL = 20  # 对齐现场 recognize-sample-rows=20
GEN_MAX_TRIES = 500
RNG = random.Random(42)

PHONE_REGEX = re.compile(r"^1[3-9]\d{9}$")
GIVEN_CHARS = "伟芳娜敏静丽强磊洋勇军杰明华建国国强志强秀英玉兰桂英丽娟秀兰"
ENT_SUFFIX = ["有限公司", "股份有限公司", "集团有限公司", "科技有限公司", "实业有限公司"]
ENT_CORE = ["华夏", "恒远", "博瑞", "智汇", "云联", "信达", "鸿泰", "博雅", "英迪", "瑞达", "腾迅", "中科"]
OFFICER_HEAD = list("职文广军兵士武")
_SEQ = 0
SURNAME_LIST = []


def _load_dicts():
    global SURNAME_LIST
    with open(os.path.join(_DICT_ROOT, "chinesename", "surname_dict.json"), encoding="utf-8") as f:
        SURNAME_LIST = json.load(f)
    if not isinstance(SURNAME_LIST, list):
        SURNAME_LIST = list(SURNAME_LIST)


def is_positive(label, text):
    ok, _ = purify_row(label, text)
    return ok


def _next_seq():
    global _SEQ
    _SEQ += 1
    return _SEQ


def _rand_phone():
    return "1" + str(RNG.randint(3, 9)) + "".join(str(RNG.randint(0, 9)) for _ in range(9))


def _rand_name():
    sur = RNG.choice(SURNAME_LIST) if SURNAME_LIST else "张"
    n = RNG.choice([1, 2, 2, 3])
    return sur + "".join(RNG.choice(GIVEN_CHARS) for _ in range(n))[: 4 - min(len(sur), 2)]


def _rand_id():
    area = RNG.choice(["110101", "310101", "440106", "330106", "510104"])
    y = RNG.randint(1965, 2005)
    m = RNG.randint(1, 12)
    d = RNG.randint(1, 28)
    birth = f"{y:04d}{m:02d}{d:02d}"
    seq = f"{RNG.randint(0, 999):03d}"
    body = area + birth + seq
    wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check = "10X98765432"
    s = sum(int(body[i]) * wi[i] for i in range(17))
    return body + check[s % 11]


def _rand_credit():
    chars = CREDIT_CODE_CHARS
    return "91" + "".join(RNG.choice(chars) for _ in range(16))


def _rand_passport():
    return "E" + RNG.choice("123456789ABCDEFGHJKLMNPQRSTUVWXYZ") + "".join(
        str(RNG.randint(0, 9)) for _ in range(7)
    )


def _rand_landline():
    if RNG.random() < 0.5:
        return f"0{RNG.randint(10, 29)}-{RNG.randint(10000000, 99999999)}"
    return f"0{RNG.randint(310, 999)}-{RNG.randint(1000000, 9999999)}"


def _rand_enterprise():
    return RNG.choice(ENT_CORE) + str(_next_seq() % 1000) + RNG.choice(ENT_SUFFIX)


def _rand_officer():
    head = RNG.choice(OFFICER_HEAD)
    body = "".join(RNG.choice("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(RNG.randint(4, 8)))
    return f"{head}字第{body}号"


def _rand_default():
    kind = RNG.randint(0, 5)
    if kind == 0:
        return f"cfg_{_next_seq()}"
    if kind == 1:
        return f"N/A-{_next_seq() % 10000}"
    if kind == 2:
        return str(RNG.randint(100000, 999999))
    if kind == 3:
        return f"test_value_{_next_seq()}"
    if kind == 4:
        return f"{RNG.randint(2020, 2025)}-{RNG.randint(1, 12):02d}-{RNG.randint(1, 28):02d}"
    return f"IDX{_next_seq():08d}"


def _gen_candidate(label):
    gens = {
        "NAME": _rand_name,
        "PHONE": _rand_phone,
        "ID_CARD": _rand_id,
        "CREDIT_CODE": _rand_credit,
        "PASSPORT": _rand_passport,
        "LANDLINE": _rand_landline,
        "ENTERPRISE_NAME": _rand_enterprise,
        "OFFICER_CARD": _rand_officer,
        "DEFAULT": _rand_default,
    }
    gen = gens.get(label)
    if not gen:
        return None
    t = gen()
    if label == "CREDIT_CODE":
        t = t.upper()
    elif label == "PASSPORT":
        t = t.upper()
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
    _load_dicts()
    print(f"目标: {TARGET_ROWS} 行/类（兰州9类）, 每列约 {ROWS_PER_COL} 行")
    print(f"目录: {_FIT_DIR}\n")
    total_added = 0
    for label in KEEP_LABELS:
        r = augment_label(label)
        if r is None:
            print(f"  {label}: 文件不存在，跳过")
            continue
        b, a, add = r
        total_added += max(0, add)
        uniq = pd.read_csv(os.path.join(_FIT_DIR, f"{label}.csv"), dtype={"text": str})["text"].nunique()
        flag = " OK" if a == TARGET_ROWS and uniq == a else " WARN"
        print(f"  {label}: {b} -> {a} (+{add}), unique={uniq}{flag}")
    print(f"\n合计净增: {total_added} 行")


if __name__ == "__main__":
    main()
