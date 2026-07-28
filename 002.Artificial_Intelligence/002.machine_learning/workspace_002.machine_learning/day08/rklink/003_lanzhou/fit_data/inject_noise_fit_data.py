"""
按列注入随机噪音（Uniform 10%~50%），标签不变。

约束：
1) 每列噪音占比随机 10%~50%
2) 其余行必须是当前 label 的正确样本（通过 purify）
3) 整文件 text 不重复（正确样本与噪音均唯一）

仅处理正类 8 种；DEFAULT 不改。
可重复执行：优先从 _legacy/before_noise/ 恢复干净样本再重建，避免叠噪音。
"""
import os
import random
import shutil

import pandas as pd

from augment_fit_data import (
    _gen_candidate as _gen_positive_candidate,
    _load_dicts,
    is_positive,
)
from purify_fit_data import purify_row

_FIT_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKUP_DIR = os.path.join(_FIT_DIR, "_legacy", "before_noise")

POSITIVE_LABELS = [
    "NAME",
    "PHONE",
    "LANDLINE",
    "CREDIT_CODE",
    "ID_CARD",
    "OFFICER_CARD",
    "PASSPORT",
    "ENTERPRISE_NAME",
]

NOISE_RATIO_MIN = 0.10
NOISE_RATIO_MAX = 0.50
GEN_MAX_TRIES = 3000
RNG = random.Random(20260728)
_SEQ = 0


def _next_seq():
    global _SEQ
    _SEQ += 1
    return _SEQ


def _is_noise_for(label, text):
    ok, _ = purify_row(label, text)
    return not ok


def _gen_noise_candidate(label):
    """现场脏值；一律带序号，避免文件内重复。"""
    kind = RNG.randint(0, 9)
    s = _next_seq()
    if kind == 0:
        return f"N/A-{s}"
    if kind == 1:
        return f"cfg_{s}"
    if kind == 2:
        return f"test_{s}"
    if kind == 3:
        return f"{RNG.randint(2018, 2026)}-{RNG.randint(1, 12):02d}-{RNG.randint(1, 28):02d}#{s}"
    if kind == 4:
        return f"{RNG.randint(1000, 99999999)}_{s}"
    if kind == 5:
        return f"IDX{s:08d}"
    if kind == 6:
        return f"unknown_{s}"
    if kind == 7:
        return f"{RNG.choice(['已删除', '待核实', '系统导入', '历史数据', '空值占位', '备注信息'])}_{s}"
    if kind == 8:
        return f"param.{s}.value"
    if label in ("NAME", "ENTERPRISE_NAME"):
        return f"1{RNG.randint(3, 9)}{RNG.randint(100000000, 999999999)}"
    return f"noise_{label}_{s}"


def _gen_unique_positive(label, used):
    for _ in range(GEN_MAX_TRIES):
        t = _gen_positive_candidate(label)
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


def _gen_unique_noise(label, used):
    for _ in range(GEN_MAX_TRIES):
        t = _gen_noise_candidate(label)
        t = str(t).strip() if t is not None else ""
        if not t or t in used:
            continue
        if not _is_noise_for(label, t):
            continue
        used.add(t)
        return t
    # 兜底唯一噪音
    t = f"N/A-fallback-{_next_seq()}"
    used.add(t)
    return t


def _restore_or_backup():
    any_bak = any(os.path.isfile(os.path.join(_BACKUP_DIR, f"{lb}.csv")) for lb in POSITIVE_LABELS)
    os.makedirs(_BACKUP_DIR, exist_ok=True)
    if any_bak:
        n = 0
        for label in POSITIVE_LABELS:
            bak = os.path.join(_BACKUP_DIR, f"{label}.csv")
            dst = os.path.join(_FIT_DIR, f"{label}.csv")
            if os.path.isfile(bak):
                shutil.copy2(bak, dst)
                n += 1
        print(f"已从干净备份恢复 {n} 个正类 CSV: {_BACKUP_DIR}")
    else:
        for label in POSITIVE_LABELS:
            src = os.path.join(_FIT_DIR, f"{label}.csv")
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(_BACKUP_DIR, f"{label}.csv"))
        print(f"已备份当前正类样本到: {_BACKUP_DIR}")


def inject_label(label):
    path = os.path.join(_FIT_DIR, f"{label}.csv")
    if not os.path.isfile(path):
        return None

    df = pd.read_csv(path, dtype={"text": str, "column_id": str})
    df["text"] = df["text"].astype(str).str.strip()
    df["column_id"] = df["column_id"].astype(str).str.strip()

    used = set()  # 整文件唯一
    ratios = []
    noise_rows = 0
    keep_rows = 0
    out_parts = []
    bad_keep = 0

    for col_id, group in df.groupby("column_id", sort=False):
        n = len(group)
        if n <= 0:
            continue

        ratio = RNG.uniform(NOISE_RATIO_MIN, NOISE_RATIO_MAX)
        n_noise = int(round(n * ratio))
        n_noise = max(1, min(n - 1, n_noise)) if n >= 2 else 0
        n_keep = n - n_noise
        ratios.append(n_noise / n if n else 0.0)

        # 优先复用本列已有「正确且未占用」的唯一正例
        originals = []
        for t in group["text"].tolist():
            t = str(t).strip()
            if not t or t in used:
                continue
            if is_positive(label, t):
                originals.append(t)

        keeps = []
        for t in originals:
            if len(keeps) >= n_keep:
                break
            keeps.append(t)
            used.add(t)

        while len(keeps) < n_keep:
            t = _gen_unique_positive(label, used)
            if t is None:
                break
            keeps.append(t)

        # 若正确样本凑不够，减少噪音、尽量保住列长（极端情况）
        if len(keeps) < n_keep:
            n_keep = len(keeps)
            n_noise = n - n_keep
            if n_noise < 0:
                n_noise = 0

        noises = []
        for _ in range(n_noise):
            t = _gen_unique_noise(label, used)
            noises.append(t)

        texts = keeps + noises
        # 列长不足时再补正确样本（仍唯一）
        while len(texts) < n:
            t = _gen_unique_positive(label, used)
            if t is None:
                t = _gen_unique_noise(label, used)
                noises.append(t)
            else:
                keeps.append(t)
            texts.append(t)

        texts = texts[:n]
        RNG.shuffle(texts)
        keep_set = set(keeps)

        for t in texts:
            row = {"column_id": col_id, "text": t, "label": label}
            out_parts.append(row)
            if t in keep_set:
                keep_rows += 1
                if not is_positive(label, t):
                    bad_keep += 1
            else:
                noise_rows += 1

    out = pd.DataFrame(out_parts)
    # 最终唯一性检查
    dup = int(out["text"].duplicated().sum())
    out.to_csv(path, index=False, encoding="utf-8")
    return {
        "cols": int(out["column_id"].nunique()),
        "rows": len(out),
        "keep_rows": keep_rows,
        "noise_rows": noise_rows,
        "noise_row_ratio": noise_rows / len(out) if len(out) else 0.0,
        "col_ratio_min": min(ratios) if ratios else 0.0,
        "col_ratio_mean": sum(ratios) / len(ratios) if ratios else 0.0,
        "col_ratio_max": max(ratios) if ratios else 0.0,
        "dup_text": dup,
        "bad_keep": bad_keep,
        "unique_text": int(out["text"].nunique()),
    }


def main():
    global _SEQ
    _SEQ = 0
    _load_dicts()
    _restore_or_backup()

    print(
        f"按列重建：噪音 Uniform({NOISE_RATIO_MIN:.0%},{NOISE_RATIO_MAX:.0%})；"
        f"其余必须正确；整文件 text 不重复\n"
    )
    for label in POSITIVE_LABELS:
        r = inject_label(label)
        if r is None:
            print(f"  {label}: 文件不存在，跳过")
            continue
        ok = r["dup_text"] == 0 and r["bad_keep"] == 0
        flag = " OK" if ok else " WARN"
        print(
            f"  {label}: cols={r['cols']} rows={r['rows']} "
            f"keep={r['keep_rows']} noise={r['noise_rows']}({r['noise_row_ratio']:.1%}) "
            f"col_noise min/mean/max="
            f"{r['col_ratio_min']:.1%}/{r['col_ratio_mean']:.1%}/{r['col_ratio_max']:.1%} "
            f"unique={r['unique_text']} dup={r['dup_text']} bad_keep={r['bad_keep']}{flag}"
        )
    print("\nDEFAULT.csv 未改动。请重新运行 rklink_003.py 训练。")


if __name__ == "__main__":
    main()
