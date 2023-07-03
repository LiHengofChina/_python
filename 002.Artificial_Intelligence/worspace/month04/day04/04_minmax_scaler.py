'''
范围缩放
处理列与列之间差异过大的情况
竞将每列的数据处理成相同的数值区间
将每列的最小值和最大值设置为相同的区间，常用区间是 0-1
'''
import numpy as np

raw_sample = np.array([[3.0,-100.0,2000.0],
                       [0.0,400.0,3000.0],
                       [1.0,-400.0,2000.0]])

mms_sample = raw_sample.copy()

# 1.用当前列的元素 - 当前列的最小值
# 2.用减完之后的结果 / 原始数据的极差
for col in std_sample.T:
    col_mean = col.mean() #每列的平均值
    print(col)
