"""一次性分析：特征重要性与高相关对，供删减参考。"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# 只导入特征函数所需：复制 rklink_002 前半段会执行太多副作用，改为 exec 最小集
import runpy
ns = runpy.run_path("rklink_002.py", run_name="__not_main__")
extract_column_features = ns["extract_column_features"]

df = pd.read_csv("fit_data.csv", dtype={"text": str}, skipinitialspace=True)
df.columns = df.columns.str.strip()
df["column_id"] = df["column_id"].str.strip()
grouped = df.groupby("column_id")
X, y = [], []
for _, group in grouped:
    texts = group["text"].tolist()
    label = group["label"].iloc[0]
    X.append(extract_column_features(texts))
    y.append(label)
X = np.array(X)
y = np.array(y)
print("X shape", X.shape)

le = LabelEncoder()
yi = le.fit_transform(y)
rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
rf.fit(X, yi)
imp = rf.feature_importances_

idx = np.argsort(imp)
print("\n--- 最低重要性 25 个 ---")
for i in idx[:25]:
    print(f"f{i}: {imp[i]:.6f}")

C = np.corrcoef(X.T)
n = C.shape[0]
pairs = []
for i in range(n):
    for j in range(i + 1, n):
        if abs(C[i, j]) > 0.92:
            pairs.append((i, j, C[i, j], imp[i], imp[j]))
pairs.sort(key=lambda x: -abs(x[2]))
print("\n--- |corr|>0.92 特征对 (前30) ---")
for p in pairs[:30]:
    print(
        f"f{p[0]} vs f{p[1]}: corr={p[2]:.4f} imp=({imp[p[0]]:.5f},{imp[p[1]]:.5f}) drop_lower={p[0] if imp[p[0]]<imp[p[1]] else p[1]}"
    )
print("total pairs |corr|>0.92:", len(pairs))
