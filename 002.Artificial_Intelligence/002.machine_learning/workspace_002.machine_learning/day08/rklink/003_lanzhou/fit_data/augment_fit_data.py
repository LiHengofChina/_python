"""
兰州 fit_data 扩充：
1) 每列固定 ROWS_PER_COL=20（对齐现场 recognize-sample-rows）
2) 正类至少 TARGET_COLS 列（默认 100 列 → 2000 行/类）
3) DEFAULT：现有列全部扩到 20，并保证至少 TARGET_COLS_DEFAULT 列

文件内 text 尽量全局唯一；仅追加/截断列内行，不删列。
"""
import json
import os
import random
import re

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

ROWS_PER_COL = 20  # 对齐现场采样行数
TARGET_COLS = 100  # 正类目标列数 → 约 2000 行/类
TARGET_COLS_DEFAULT = 1500  # DEFAULT 目标列数 → 约 30000 行
GEN_MAX_TRIES = 2000
RNG = random.Random(42)

GIVEN_CHARS = "伟芳娜敏静丽强磊洋勇军杰明华建国国强志强秀英玉兰桂英丽娟秀兰"
ENT_SUFFIX = ["有限公司", "股份有限公司", "集团有限公司", "科技有限公司", "实业有限公司"]
ENT_CORE = ["华夏", "恒远", "博瑞", "智汇", "云联", "信达", "鸿泰", "博雅", "英迪", "瑞达", "腾迅", "中科"]
OFFICER_HEAD = list("职文广军兵士武")
ID_AREAS = [
    "110101", "110105", "310101", "310115", "440106", "440305",
    "330106", "330102", "510104", "510107", "320102", "320104",
    "420102", "420106", "610102", "610103",
]
_SEQ = 0
SURNAME_LIST = []


def _load_dicts():
    global SURNAME_LIST
    path = os.path.join(_DICT_ROOT, "chinesename", "surname_dict.json")
    with open(path, encoding="utf-8") as f:
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
    # 生成 2~4 个汉字姓名（复姓优先短名）
    sur = RNG.choice(SURNAME_LIST) if SURNAME_LIST else "张"
    if len(sur) >= 2:
        given_n = RNG.choice([1, 1, 2])
    else:
        given_n = RNG.choice([1, 2, 2, 3])
    given = "".join(RNG.choice(GIVEN_CHARS) for _ in range(given_n))
    name = sur + given
    return name[:4] if len(name) > 4 else name


def _rand_id():
    area = RNG.choice(ID_AREAS)
    y = RNG.randint(1960, 2008)
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
    return "91" + "".join(RNG.choice(CREDIT_CODE_CHARS) for _ in range(16))


def _rand_passport():
    head = RNG.choice("GE")
    second = RNG.choice("123456789ABCDEFGHJKLMNPQRSTUVWXY")
    return head + second + "".join(str(RNG.randint(0, 9)) for _ in range(7))


def _rand_landline():
    r = RNG.random()
    if r < 0.4:
        return f"0{RNG.randint(10, 29)}-{RNG.randint(10000000, 99999999)}"
    if r < 0.75:
        return f"0{RNG.randint(310, 999)}-{RNG.randint(1000000, 9999999)}"
    if r < 0.9:
        return f"400-{RNG.randint(100, 999)}-{RNG.randint(1000, 9999)}"
    return f"{RNG.randint(2, 8)}{RNG.randint(1000000, 9999999)}"


def _rand_enterprise():
    return RNG.choice(ENT_CORE) + str(_next_seq() % 10000) + RNG.choice(ENT_SUFFIX)


def _rand_officer():
    head = RNG.choice(OFFICER_HEAD)
    body = "".join(RNG.choice("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(RNG.randint(4, 8)))
    return f"{head}字第{body}号"


def _rand_default():
    kind = RNG.randint(0, 7)
    if kind == 0:
        return f"cfg_{_next_seq()}"
    if kind == 1:
        return f"N/A-{_next_seq() % 100000}"
    if kind == 2:
        return str(RNG.randint(100000, 99999999))
    if kind == 3:
        return f"test_value_{_next_seq()}"
    if kind == 4:
        return f"{RNG.randint(2018, 2026)}-{RNG.randint(1, 12):02d}-{RNG.randint(1, 28):02d}"
    if kind == 5:
        return f"IDX{_next_seq():08d}"
    if kind == 6:
        return f"unknown_{_next_seq()}"
    return f"param_{_next_seq()}_{RNG.randint(1, 99)}"


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
    if label in ("CREDIT_CODE", "PASSPORT"):
        t = t.upper()
    return t


def _gen_unique(label, used):
    for _ in range(GEN_MAX_TRIES):
        t = _gen_candidate(label)
        if t is None:
            continue
        t = str(t).strip()
        if not t or t in used:
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


def _normalize_column_rows(label, col_id, texts, used):
    """列内去重后截断/补齐到 ROWS_PER_COL。"""
    kept = []
    for t in texts:
        t = str(t).strip()
        if not t:
            continue
        if t in kept:
            continue
        kept.append(t)
        used.add(t)
    if len(kept) > ROWS_PER_COL:
        kept = kept[:ROWS_PER_COL]
    while len(kept) < ROWS_PER_COL:
        t = _gen_unique(label, used)
        if t is None:
            break
        kept.append(t)
    return [{"column_id": col_id, "text": t, "label": label} for t in kept]


def expand_label(label):
    path = os.path.join(_FIT_DIR, f"{label}.csv")
    if not os.path.isfile(path):
        return None

    df = pd.read_csv(path, dtype={"text": str, "column_id": str})
    df["text"] = df["text"].astype(str).str.strip()
    df["column_id"] = df["column_id"].astype(str).str.strip()
    before_rows = len(df)
    before_cols = df["column_id"].nunique()

    used = set()
    new_rows = []
    # 保持原列顺序
    for col_id, group in df.groupby("column_id", sort=False):
        texts = group["text"].tolist()
        new_rows.extend(_normalize_column_rows(label, col_id, texts, used))

    out = pd.DataFrame(new_rows)
    prefix = _infer_col_prefix(out if not out.empty else df)
    col_idx = _max_col_index(out if not out.empty else df, prefix)

    target_cols = TARGET_COLS_DEFAULT if label == "DEFAULT" else TARGET_COLS
    while out["column_id"].nunique() < target_cols:
        col_idx += 1
        col_id = f"{prefix}{col_idx}"
        col_texts = []
        for _ in range(ROWS_PER_COL):
            t = _gen_unique(label, used)
            if t is None:
                break
            col_texts.append(t)
        if len(col_texts) < max(5, ROWS_PER_COL // 2):
            # 生成失败过多则停止加列
            break
        # 不足 20 也尽量补满
        while len(col_texts) < ROWS_PER_COL:
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
    after_rows = len(out)
    after_cols = out["column_id"].nunique()
    sizes = out.groupby("column_id").size()
    return {
        "before_rows": before_rows,
        "after_rows": after_rows,
        "before_cols": before_cols,
        "after_cols": after_cols,
        "min_per_col": int(sizes.min()) if len(sizes) else 0,
        "max_per_col": int(sizes.max()) if len(sizes) else 0,
        "mean_per_col": float(sizes.mean()) if len(sizes) else 0.0,
        "unique_text": int(out["text"].nunique()),
    }


def main():
    global _SEQ
    _SEQ = 0
    _load_dicts()
    print(f"每列固定 {ROWS_PER_COL} 行；正类目标列数={TARGET_COLS}；DEFAULT 目标列数={TARGET_COLS_DEFAULT}")
    print(f"目录: {_FIT_DIR}\n")
    for label in KEEP_LABELS:
        r = expand_label(label)
        if r is None:
            print(f"  {label}: 文件不存在，跳过")
            continue
        ok = (r["min_per_col"] == ROWS_PER_COL and r["max_per_col"] == ROWS_PER_COL)
        flag = " OK" if ok else " WARN"
        print(
            f"  {label}: rows {r['before_rows']}->{r['after_rows']}, "
            f"cols {r['before_cols']}->{r['after_cols']}, "
            f"per_col min/mean/max={r['min_per_col']}/{r['mean_per_col']:.1f}/{r['max_per_col']}, "
            f"unique={r['unique_text']}{flag}"
        )


if __name__ == "__main__":
    main()
