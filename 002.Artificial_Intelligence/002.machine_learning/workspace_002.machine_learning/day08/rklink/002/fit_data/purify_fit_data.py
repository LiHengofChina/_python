"""
净化 fit_data/*.csv：每类只保留典型、干净样本。
剔除行写入 _legacy/purged/{LABEL}_removed.csv（含 reason 列）。
"""
import os
import re
from datetime import datetime

import pandas as pd

_FIT_DIR = os.path.dirname(os.path.abspath(__file__))
_PURGED_DIR = os.path.join(_FIT_DIR, "_legacy", "purged")

PHONE_REGEX = re.compile(r"^1[3-9]\d{9}$")
ID_REGEX = re.compile(r"^\d{17}[\dXx]$")
STOCK_CODE_REGEX = re.compile(r"^\d{6}$")
PASSPORT_REGEX = re.compile(r"^[A-Z]{1,2}\d{7,8}$")
DATE_REGEX = re.compile(r"^(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|\d{8})$")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")
CREDIT_CODE_CHARS = "0123456789ABCDEFGHJKLMNPQRTUWXY"
NAME_HAN_REGEX = re.compile(r"^[\u4e00-\u9fff]{2,4}$")


def _strip(t):
    return str(t).strip() if pd.notnull(t) else ""


def valid_date(text):
    try:
        text = _strip(text)
        if "-" in text:
            datetime.strptime(text, "%Y-%m-%d")
        elif "/" in text:
            datetime.strptime(text, "%Y/%m/%d")
        elif "." in text:
            datetime.strptime(text, "%Y.%m.%d")
        elif len(text) == 8 and text.isdigit():
            if int(text[:2]) >= 21:
                return False
            datetime.strptime(text, "%Y%m%d")
        else:
            return False
        return True
    except Exception:
        return False


def is_clean_fund_name(text):
    t = _strip(text)
    if len(t) < 2 or len(t) > 40:
        return False
    if re.fullmatch(r"\d{6,}", t):
        return False
    if re.fullmatch(r"\d{17}[\dXx]", t):
        return False
    if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", t):
        return False
    if "@" in t:
        return False
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", t):
        return False
    if re.fullmatch(r"\d{8}", t):
        return False
    return bool(re.search(r"[\u4e00-\u9fff]", t))


def is_clean_credit_code(text):
    t = _strip(text).upper()
    if not re.fullmatch(r"[0-9A-Z]{18}", t):
        return False
    return all(c in CREDIT_CODE_CHARS for c in t)


def purify_row(label, text):
  t = _strip(text)
  if not t:
      return False, "empty"
  if label == "STOCK_CODE":
      if STOCK_CODE_REGEX.fullmatch(t):
          return True, ""
      return False, "not_6_digit_stock_fund_code"
  if label == "NAME":
      if NAME_HAN_REGEX.fullmatch(t):
          return True, ""
      return False, "not_2_4_han_name"
  if label == "PHONE":
      if PHONE_REGEX.fullmatch(t):
          return True, ""
      return False, "not_strict_11_mobile"
  if label == "ID_CARD":
      if ID_REGEX.fullmatch(t):
          return True, ""
      return False, "not_18_id_format"
  if label == "FUNDS_NAME":
      if is_clean_fund_name(t):
          return True, ""
      return False, "not_fund_name_like"
  if label == "CREDIT_CODE":
      if is_clean_credit_code(t):
          return True, ""
      return False, "not_18_credit_charset"
  if label == "PASSPORT":
      if PASSPORT_REGEX.fullmatch(t.upper()):
          return True, ""
      return False, "not_passport_format"
  if label == "EMAIL":
      if EMAIL_REGEX.fullmatch(t):
          return True, ""
      return False, "not_email_format"
  if label == "DATE":
      if DATE_REGEX.match(t) and valid_date(t):
          return True, ""
      return False, "not_valid_date"
  # 其它类暂不激进清理
  return True, ""


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
    targets = [
        "STOCK_CODE", "NAME", "PHONE", "ID_CARD", "FUNDS_NAME",
        "CREDIT_CODE", "PASSPORT", "EMAIL", "DATE",
    ]
    print("purify fit_data ->", _FIT_DIR)
    print("removed ->", _PURGED_DIR)
    total_before = total_after = total_removed = 0
    for label in targets:
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
