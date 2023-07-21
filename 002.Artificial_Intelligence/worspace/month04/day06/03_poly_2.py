'''
多项式回归、API
'''

import pandas as pd
import sklearn.preprocessing as sp   # 数据预处理
import sklearn.pipeline as pl        # 管线模块
import sklearn.linear_model as lm    # 线性模型

import matplotlib.pyplot as plt


data = pd.read_csv('../data_test/Salary_Data.csv', sep=',')

#整理输入
x = data.iloc[:, :-1]
y = data.iloc[:, -1]

#创建模型           #PolynomialFeatures(3)扩展到3次
model = pl.make_pipeline(sp.PolynomialFeatures(3), lm.LinearRegression())
                # 类似于linux的 "管道符号"， 将上一个命令的输出作为下一个命令的输入

                #这里同样可以加入 "岭回归" 和 "Lasso"

#训练
model.fit(x, y) # train_x 会先进行扩展，之后次给LinearRegression,再训练

#预测
pred_y = model.predict(x)

plt.plot(x,pred_y,color= 'orangered')
plt.scatter(x,y)

plt.tight_layout()
plt.show()
