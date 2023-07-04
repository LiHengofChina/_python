'''
简单的数学指标
'''

import numpy as np
import pandas as pd

data = pd.read_json('../data_test/ratings.json')
print(data)

print(data.mean(axis=0))        #求平均值
print(type(data.mean(axis=0)))  #返回Series


###对1维数据求平均值
fracture = data.loc['Fracture']
# print(fracture)
#平均值
print(np.mean(fracture))
print(np.mean(data, axis=0))
print(np.mean(data, axis=1))

print("===" * 30)
print(fracture.mean())
print(data.mean(axis=0))
