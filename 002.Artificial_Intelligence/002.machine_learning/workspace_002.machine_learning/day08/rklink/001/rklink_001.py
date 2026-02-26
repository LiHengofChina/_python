
'''

脱敏识别 —— 手机号 vs 身份证（二分类）
只使用一个特征：长度

'''

import numpy as np
import pandas as pd
import sklearn.model_selection as ms
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

# ==============================
#（1）加载数据
# ==============================
df = pd.read_csv("phone_id_data.csv", dtype={"text": str})
# print("原始数据：")
# print(df)
# print("-" * 50)


# ==============================
#（2）特征提取函数（只提取长度）
# ==============================
def extract_features(text):
    length = len(text)
    return [length]

# 构造特征矩阵
X = np.array([extract_features(t) for t in df["text"]])
y = df["label"].values
# print("特征矩阵 X：")
# print(X)
# print("-" * 50)

# ==============================
#（3）划分训练 / 测试集
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y  # 按照 "y值(类别)"进行等比划分
)


# ==============================
#（4）构建随机森林模型
# ==============================
model = RandomForestClassifier(
    n_estimators=100, #100棵决策树
    random_state=42
)


# ==============================
#（5）在训练集上做交叉验证（此时不要先 fit）
# 它只是评估工具
# 交叉验证得分可以用来判断：
# ==============================
# 做5次交叉验证，评估模型是否可用
score = ms.cross_val_score(
    model,
    X_train,
    y_train,
    cv=5,
    scoring="f1_weighted"
)

print("交叉验证得分:", score)
print("平均得分:", score.mean())
print("-" * 50)

# ==============================
#（5）训练模型
# ==============================

model.fit(X_train, y_train)

print("特征重要性：")
print(model.feature_importances_)
print("=" * 50)


# ==============================
#（6）预测
# ==============================

pred = model.predict(X_test)
print("测试集真实值：", y_test)
print("测试集预测值：", pred)
print("-" * 50)

# ==============================
#（7）置信度
# ==============================

prob = model.predict_proba(X_test)
print("测试集预测概率（置信度）：")
print(prob)
print("-" * 50)

# ==============================
#（8）分类报告
# ==============================

print("分类报告：")
print(classification_report(y_test, pred))

# ==============================
#（9）F1得分
# ==============================

print("-" * 50)
print("F1得分（weighted）:", f1_score(y_test, pred, average="weighted"))

# ==============================
#（10）手动测试几个样本
# ==============================
print("-" * 50)
print("-" * 50)

test_sample = "13888888888"  # 手机号


# 提取特征
feature = np.array([extract_features(test_sample)])

# 预测类别和置信度
prediction = model.predict(feature)[0]
probability = model.predict_proba(feature)[0]

# 输出结果
print(f"输入：{test_sample}")
print(f"预测类别：{prediction}")

print("置信度（每颗树的观点）：")

for cls, prob in zip(model.classes_, probability):
    print(f"  {cls} : {prob:.4f}")