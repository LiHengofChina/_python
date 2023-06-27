'''
标准化（均值移除）
'''
import numpy as np

raw_sample = np.array([[3.0,-100.0,2000.0],
                       [0.0,400.0,3000.0],
                       [1.0,-400.0,2000.0]])

std_sample = raw_sample.copy()
for col in std_sample.T:
    col_mean = col.mean() #每列的平均值
    print(col)
