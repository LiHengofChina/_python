'''
简单的数学指标
        ：算术平均值
'''

import numpy as np
import pandas as pd

data = pd.read_json('../../data_test/ratings.json')
print(data)
# print(type(data)) #读取到的是一个 DataFrame ，


print("===" * 30)
print(data.mean(axis=0))        #（axis=0）代表的是纵向，求每一列的平均值
# print(type(data.mean(axis=0)))  #返回Series



fracture = data.loc['Fracture'] #拿到一列数据
# print(fracture)
# print(type(fracture)) #返回 一个 Series

################################## np 接口
print("================3" * 30)
print(np.mean(fracture))     # 使用np接口，求 Seriesr 的平均值，它是一个1维数组。  #返回Series
print("================4" * 30)
print(np.mean(data, axis=0)) # 使用np接口，求 DataFrame 的平均值，每一列的平均值。 #返回Series
print("================5" * 30)
print(np.mean(data, axis=1)) # 使用np接口，求 DataFrame 的平均值，每一行的平均值。 #返回Series



################################## pandas的 接口
print("================6" * 30)
print(fracture.mean())
print(data.mean(axis=0))

