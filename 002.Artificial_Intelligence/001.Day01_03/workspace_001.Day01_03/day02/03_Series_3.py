'''
Series示例
Series 常用属性（新版规范写法）
'''

import pandas as pd

s01 = pd.Series([100, 90, 80, 70], index=['zs', 'ls', 'ww', 'zl'])

# ===============================
# 常用属性
# ===============================

print(s01.values)
print(type(s01.values))   # 它是一个 ndarray
print(type(s01))
print(s01.index)
print(s01.dtype)
print(s01.size)
print(s01.ndim)
print(s01.shape)


# ===============================
# 不要最后一个元素
# ===============================

print("##" * 20)

# 1️⃣ 布尔掩码（推荐）
print(s01.iloc[[True, True, True, False]])

# 2️⃣ 位置掩码（必须用 iloc）
print(s01.iloc[[0, 1, 2]])

# 3️⃣ 标签掩码（必须用 loc）
print(s01.loc[['zs', 'ls', 'ww']])


print("##" * 20)

# 如果数据量非常大，推荐这种写法

# 对索引进行切片
idx = s01.index[:-1]
print(idx)
print(type(idx))  # 还是 Index 类型

# 用标签索引取值（必须用 loc）
print(s01.loc[idx])