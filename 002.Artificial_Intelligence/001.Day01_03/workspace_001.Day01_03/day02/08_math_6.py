'''
简单的数学指标
        标准差
'''

import numpy as np
import pandas as pd



data = pd.read_json('../../data_test/ratings.json')
# print(data)



print("================" * 20)
fracture = data.loc['Fracture']
# print(fracture)



#
# pandas的接口         #总体标准差
print(fracture.std())

# numpy的接口中        #样本标准差
print(np.std(fracture, ddof=1))  # ddof 表示贝塞尔校正系数， ddof=1 表示分母减1，  ddof=2 表示分母减2


