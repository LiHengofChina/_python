'''
二值化
    设定一个阈值，
        用1表示该元素大于阈值，
        用0表示该元素小于等于阈值

        演示计算过程
'''

import numpy as np

raw_sample = np.array([[66.6,59.9,22.3],
                       [99.9,18.8,88.8],
                       [12.3,34.5,78.9]])

bin_sample = raw_sample.copy()

#当前数据为学生考试成绩，
#将及格的元素转成1，不及格元素转成0



# bin_sample <= 59.9 返回一个掩码数组，然后使用原数组索引掩码数组.
# bin_sample[bin_sample <= 59.9] = 0
# bin_sample[bin_sample > 59.9] = 1
# print(bin_sample)



res = np.where(bin_sample > 59.9, 1.0, 0.0)
print(res)






