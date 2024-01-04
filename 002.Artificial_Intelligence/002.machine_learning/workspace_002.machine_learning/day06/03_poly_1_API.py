'''
多项式回归、API
        -查看 ”训练后的结果“
        就是 x 扩展后的样子

第1列是：1，全是1
第2列是：x的值
第3列是：x^2

'''

import pandas as pd
import sklearn.preprocessing as sp


data = pd.read_csv('../data_test/Salary_Data.csv', sep=',')

x = data.iloc[:,:-1]

#========================== 如果需要查看训练后的结果
# 扩展器，其实它属于扩展器
encoder = sp.PolynomialFeatures(2) #最高次项扩展为 2
res = encoder. fit_transform(x)
print(res)

'''
#结果说明：
第1列是：1，全是1
第2列是：x的值
第3列是：x^2
'''
#==========================




