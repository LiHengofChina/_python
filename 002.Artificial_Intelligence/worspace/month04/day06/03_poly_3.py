'''
多项式回归、API

"最高次幂"是一个超参数，它的值是多少合适 在所以不能给太高
可以使用for循环的方式，看看哪个得分高，再决定

'''

import pandas as pd
import sklearn.preprocessing as sp   # 数据预处理
import sklearn.pipeline as pl        # 管线模块
import sklearn.linear_model as lm    # 线性模型
import sklearn.metrics as sm         # 评估模块


import  numpy as np

data = pd.read_csv('../data_test/Salary_Data.csv', sep=',')

#整理输入
x = data.iloc[:, :-1]
y = data.iloc[:, -1]


params = np.arange(1,100,1)




scores = []
for i in params:
    model = pl.make_pipeline(sp.PolynomialFeatures(i), lm.LinearRegression())
    model.fit(x, y)
    pred_y = model.predict(x)
    scores.append(sm.r2_score(y, pred_y))

#求列表的最大值索引
max_value = max(scores)
max_index = scores.index(max_value)


print('{}---------{}'.format(max_index ,scores[max_index]))
# 11次时得分最高


