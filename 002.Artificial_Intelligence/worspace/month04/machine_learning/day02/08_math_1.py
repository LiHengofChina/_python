'''
简单的数学指标
        加权平均值
'''

import numpy as np
import pandas as pd

data = pd.read_json('../../data_test/ratings.json')
print(data)
# print(type(data)) #读取到的是一个 DataFrame ，

print("================3" * 20)
fracture = data.loc['Fracture'] #拿到一列数据
print(fracture)
'''
John Carson          3.5
Michelle Peterson    5.0        #这是专业评论员，它占10分，其他人1分
William Reynolds     3.5
Jillian Hobart       4.0
Melissa Jones        3.0
Alex Roberts         5.0        #这是专业评论员，它占10分，其他人1分
Michael Henry        4.0
'''
print("================3" * 30)
print(np.mean(fracture))     # 使用np接口，求 Series 的平均值，它是一个1维数组。  #返回Series   # 这一列的算术平均值


print("================3" * 30)
ap = np.average(fracture,weights=[1, 10, 1, 1, 1, 10, 1])#权重数组列表，有两个人的评分更高  # fracture是一个Series，一维数据
print(ap)  # 4.72，这个值，更加偏向于 5，因为打5分的人权重值更高
           # 所以我们可以根据业务要求对每一个样本 “赋予不同的权重”

