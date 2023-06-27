'''
归一化 normalize
将数值转成0-1占比
'''
import numpy as np

raw_sample = np.array([[10.0, 20.0, 5.0],
                       [8.0, 10.0, 1.0]])

# 复制一份
nor_sample = raw_sample.copy()

for row in nor_sample:
    row /= abs(row).sum()

print(nor_sample)
print(nor_sample.sum())
print("==" * 30)
