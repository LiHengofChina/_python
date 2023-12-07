'''
归一化 normalize
        将数值转成  0~1  的占比

 演示计算过程
'''
import numpy as np

raw_sample = np.array([[10.0, 20.0, 5.0],
                       [8.0, 10.0, 1.0]])

# 复制一份
nor_sample = raw_sample.copy()

for row in nor_sample:
    # 行的  “每一个值” 除以 “每个特殊值绝对值之和”
    # row /= np.sum(np.abs(row))
    row /= abs(row).sum()

print(nor_sample)

#验证一下，它们占比等于1
print(nor_sample.sum(axis=1))






