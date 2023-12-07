'''
简单的数学指标
        中位数
'''

import numpy as np
import pandas as pd

data = pd.read_json('../../data_test/ratings.json')
# print(data)


print("================3" * 20)
fracture = data.loc['Fracture']
# print(fracture)

#样本个数为奇数，则为中间元素
#样本个数为偶数，则为中间两个元素的平均值。
print(np.median(fracture))     #最中位数
