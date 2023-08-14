
'''
	"波士顿房屋价格" 数据预测
    分别构建 "线性回归"、"岭回归"、"多项式回归" 看谁更好
# 评估每一个模型的R2得分

自己写的

'''

import sklearn.model_selection as ms #模型选择
import pandas as pd
import sklearn.linear_model as lm
import matplotlib.pyplot as plt
import sklearn.metrics as sm
import  numpy as np
import sklearn.pipeline as pl
import sklearn.preprocessing as sp


# 数据来自：data_url = "http://lib.stat.cmu.edu/datasets/boston"
data = pd.read_csv('04_boston_data.csv', sep=',', header=None)

##==========================================
x = data.iloc[:, :-1]
y = data.iloc[:, -1]

train_x,test_x,train_y,test_y = ms.train_test_split(x,y,
                        test_size=0.2,
                        random_state= 7)

##==========================================  # （3）根据 "训练集" 训练模型
#创建线性模型
model = lm.LinearRegression()
#使用线性模型训练
model.fit(train_x, train_y)
#预测
pred_tets_y = model.predict(test_x)
#评估
print('r2_score：', sm.r2_score(test_y, pred_tets_y))


#岭回归创建线性模型
ridge = lm.Ridge() #alpha=291
ridge.fit(train_x, train_y)
ridge_test_y = ridge.predict(test_x)
print('r2_score_ridge: {}'.format( sm.r2_score(test_y, ridge_test_y)))



#多项式回归
model = pl.make_pipeline(sp.PolynomialFeatures(2), lm.LinearRegression())
model.fit(train_x, train_y)
poly_test_y = model.predict(test_x)
print(str(sm.r2_score(test_y, poly_test_y)))

