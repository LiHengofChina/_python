"""
净化 fit_data：列内去重、删除完全相同的列、同类 text 全局唯一（每文件内不重复）。
"""
import os
import re

import pandas as pd

_FIT_DIR = os.path.dirname(os.path.abspath(__file__))


def _col_signature(texts):
    return tuple(sorted(str(t).strip() for t in texts if pd.notna(t) and str(t).strip()))


def dedupe_label(label):
    path = os.path.join(_FIT_DIR, f"{label}.csv")
    if not os.path.isfile(path):
        return None
    df = pd.read_csv(path, dtype={"text": str, "column_id": str})
    before = len(df)

    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"].str.len() > 0]
    df = df.drop_duplicates(subset=["column_id", "text"], keep="first")

    kept_rows = []
    seen_cols = {}
    for col_id, group in df.groupby("column_id", sort=False):
        texts = list(dict.fromkeys(group["text"].tolist()))
        if not texts:
            continue
        sig = _col_signature(texts)
        if sig in seen_cols:
            continue
        seen_cols[sig] = col_id
        for t in texts:
            kept_rows.append({"column_id": col_id, "text": t, "label": label})

    out = pd.DataFrame(kept_rows)
    if out.empty:
        return before, 0, 0, before

    out = out.drop_duplicates(subset=["text"], keep="first")
    after = len(out)
    out.to_csv(path, index=False, encoding="utf-8")
    return before, after, before - after, out["column_id"].nunique()


def main():
    files = sorted(f[:-4] for f in os.listdir(_FIT_DIR) if f.endswith(".csv"))
    print(f"dedupe fit_data -> {_FIT_DIR}")
    print("规则: 列内去重 | 删相同列 | 同类 text 文件内唯一\n")
    total_before = total_after = 0
    for label in files:
        r = dedupe_label(label)
        if r is None:
            continue
        b, a, removed, cols = r
        total_before += b
        total_after += a
        print(f"  {label}: {b} -> {a} rows, cols={cols} (removed {removed})")
    print(f"\ntotal: {total_before} -> {total_after} (removed {total_before - total_after})")


if __name__ == "__main__":
    main()
