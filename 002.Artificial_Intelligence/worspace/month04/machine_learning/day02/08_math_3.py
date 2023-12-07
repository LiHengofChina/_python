'''
简单的数学指标
        最值索引
'''

import numpy as np
import pandas as pd

data = pd.read_json('../../data_test/ratings.json')
# print(data)


print("================3" * 20)
fracture = data.loc['Fracture']
print(fracture)


# print(np.max(fracture))     #最大值
# print(np.argmax(fracture))  #最大值的索引()#np返回位置索引
print('对Fracture这部电影最高打了{}分,是:{}打的.'.format(np.max(fracture), np.argmax(fracture)))


# print(fracture.max())       #最大值
# print(fracture.idxmax())    #最大值的索引()#pandas返回的是标签索引
print('对Fracture这部电影最高打了{}分,是:{}打的.'.format(fracture.max(), fracture.idxmax()))
