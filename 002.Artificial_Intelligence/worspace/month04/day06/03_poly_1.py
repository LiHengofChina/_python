'''
多项式回归、API
        -查看训练后的结果
'''

import pandas as pd
import sklearn.preprocessing as sp


data = pd.read_csv('../data_test/Salary_Data.csv', sep=',')

x = data.iloc[:,:-1]

#========================== 如果需要查看训练后的结果
# 扩展器，其实它属于扩展器
encoder = sp.PolynomialFeatures(2)
res = encoder. fit_transform(x)
print(res)
#==========================




