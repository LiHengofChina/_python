"""
净化 fit_data/*.csv：仅处理兰州 9 类，每类只保留典型、干净样本。
剔除行写入 _legacy/purged/{LABEL}_removed.csv（含 reason 列）。
"""
import os
import re

import pandas as pd

_FIT_DIR = os.path.dirname(os.path.abspath(__file__))
_PURGED_DIR = os.path.join(_FIT_DIR, "_legacy", "purged")

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

PHONE_REGEX = re.compile(r"^1[3-9]\d{9}$")
ID_REGEX = re.compile(r"^\d{17}[\dXx]$")
PASSPORT_REGEX = re.compile(r"^[GE][0-9A-HJ-NP-Z]\d{7}$", re.I)
CREDIT_CODE_CHARS = "0123456789ABCDEFGHJKLMNPQRTUWXY"
NAME_HAN_REGEX = re.compile(r"^[\u4e00-\u9fff]{2,4}$")
OFFICER_REGEX = re.compile(r"^[职文广军兵士武]字第[0-9A-Za-z]{4,8}号?$")
ENTERPRISE_HINT = re.compile(r"(公司|集团|有限|股份|厂|中心|事务所)")


def _strip(t):
    return str(t).strip() if pd.notnull(t) else ""


def is_clean_credit_code(text):
    t = _strip(text).upper()
    if not re.fullmatch(r"[0-9A-Z]{18}", t):
        return False
    return all(c in CREDIT_CODE_CHARS for c in t)


def purify_row(label, text):
    t = _strip(text)
    if not t:
        return False, "empty"
    if label == "DEFAULT":
        return True, ""
    if label == "NAME":
        if NAME_HAN_REGEX.fullmatch(t):
            return True, ""
        return False, "not_2_4_han_name"
    if label == "PHONE":
        if PHONE_REGEX.fullmatch(t) or re.fullmatch(r"\d{7}", t):
            return True, ""
        return False, "not_mobile_or_short"
    if label == "LANDLINE":
        # 宽松保留：含数字且不像 11 位手机
        digits = re.sub(r"\D", "", t)
        if len(digits) >= 5 and not PHONE_REGEX.fullmatch(digits[-11:] if len(digits) >= 11 else digits):
            return True, ""
        return False, "not_landline_like"
    if label == "ID_CARD":
        if ID_REGEX.fullmatch(t) or re.fullmatch(r"\d{15}", t):
            return True, ""
        return False, "not_id_format"
    if label == "CREDIT_CODE":
        if is_clean_credit_code(t):
            return True, ""
        return False, "not_18_credit_charset"
    if label == "PASSPORT":
        if PASSPORT_REGEX.fullmatch(t.upper()):
            return True, ""
        return False, "not_passport_format"
    if label == "OFFICER_CARD":
        if OFFICER_REGEX.fullmatch(t):
            return True, ""
        return False, "not_officer_format"
    if label == "ENTERPRISE_NAME":
        if 6 <= len(t) <= 40 and ENTERPRISE_HINT.search(t):
            return True, ""
        return False, "not_enterprise_like"
    return False, "unsupported_label"


def purify_file(label):
    path = os.path.join(_FIT_DIR, f"{label}.csv")
    if not os.path.isfile(path):
        return None
    df = pd.read_csv(path, dtype={"text": str, "column_id": str})
    if "text" not in df.columns:
        return None
    kept, removed = [], []
    for row in df.itertuples(index=False):
        ok, reason = purify_row(label, row.text)
        d = row._asdict()
        if ok:
            if label == "CREDIT_CODE":
                d["text"] = _strip(d["text"]).upper()
            kept.append(d)
        else:
            d["reason"] = reason
            removed.append(d)
    out = pd.DataFrame(kept)
    out.to_csv(path, index=False, encoding="utf-8")
    if removed:
        os.makedirs(_PURGED_DIR, exist_ok=True)
        rem = pd.DataFrame(removed)
        rem.to_csv(os.path.join(_PURGED_DIR, f"{label}_removed.csv"), index=False, encoding="utf-8")
    return len(df), len(kept), len(removed)


def main():
    print("purify fit_data（兰州9类）->", _FIT_DIR)
    print("removed ->", _PURGED_DIR)
    total_before = total_after = total_removed = 0
    for label in KEEP_LABELS:
        r = purify_file(label)
        if r is None:
            continue
        before, after, removed = r
        total_before += before
        total_after += after
        total_removed += removed
        print(f"  {label}: {before} -> {after} (removed {removed})")
    print(f"targets total: {total_before} -> {total_after} (removed {total_removed})")


if __name__ == "__main__":
    main()
