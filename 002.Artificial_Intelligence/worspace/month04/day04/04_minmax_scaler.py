'''
范围缩放
    演示计算过程
'''
import numpy as np

raw_sample = np.array([[3.0,-100.0,2000.0],
                       [0.0,400.0,3000.0],
                       [1.0,-400.0,2000.0]])

mms_sample = raw_sample.copy()


for clo in mms_sample.T:
    ptp = clo.ptp(); # 极差
    clo -= clo.min()  #列的每个值减去它的最小值
    clo /= ptp  #然后除以它的极差


print(mms_sample)


