'''
 "多项式回归模型" 实现原理

 就是在 "数据里面"增加高次项， 再去求 "解参数的过程"
'''
import pandas as pd
import sklearn.linear_model as lm

import matplotlib.pyplot as plt

data = pd.read_csv('../data_test/Salary_Data.csv',
                   sep=',')

#准备数据
x = data.iloc[:,:-1] # 除最后一列外所有数据，所以是2维
y = data.iloc[:,-1]  # 只要最后一列，所以是1维

#增加高次项
x['x2'] = x['YearsExperience']**2
x['x3'] = x['YearsExperience']**3
# x['x4'] = x['YearsExperience']**4
# x['x5'] = x['YearsExperience']**5
# x['x6'] = x['YearsExperience']**6
# x['x7'] = x['YearsExperience']**7
# x['x8'] = x['YearsExperience']**8
#加的越多， 转弯越凶

'''
    此时相当于
    y = w1*x1 +w2*x2 + w3*x3 + b
    此时求w1、w2、w3就可以了。

    只不过x2的值 是x^2
    只不过x3的值 是x^3
'''
model = lm.LinearRegression()
model.fit(x, y)#x是二维的，y是一维的

print(model.coef_)
# [-718.70841416 2099.35194631 -122.91541434]
# y = -718.70841416*x^3 + 2099.35194631*x^2 + -122.91541434*x^3 + b


pred_y = model.predict(x)


#注意：画图时，要用原来的数据
plt.scatter(x['YearsExperience'],y)
#注意：画图时，要用原来的数据
plt.plot(x['YearsExperience'],pred_y,color='orangered')



plt.tight_layout()
plt.show()


