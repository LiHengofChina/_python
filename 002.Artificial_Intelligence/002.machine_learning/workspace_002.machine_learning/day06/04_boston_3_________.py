
'''
	"波士顿房屋价格" 数据预测
    分别构建 "线性回归"、"岭回归"、"多项式回归" 看谁更好
    # 评估每一个模型的R2得分


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
def get_model(name,model):
    print('-------------------',name,'-------------------')
    model.fit(train_x,train_y)
    #训练集的预测值
    pred_train_y = model.predict(train_x)
    #测试集的预测值
    pred_test_y =  model.predict(test_x)
    #评估
    print('训练集', sm.r2_score(train_y, pred_train_y))
    print('测试集', sm.r2_score(test_y, pred_test_y))


# 创建模型字典
model_dic = {
    '线性回归':lm.LinearRegression(),
    '岭回归':lm.Ridge(),
    '多项式回归':pl.make_pipeline(sp.PolynomialFeatures(2),
                                  lm.LinearRegression())
}

for name,model in model_dic.items():
    get_model(name,model)

'''

------------------- 线性回归 -------------------
训练集 0.7698532963729757
测试集 0.5785415472763429
            //欠拟合，两个值都低
------------------- 岭回归 -------------------
训练集 0.7681931875788315
测试集 0.570364115734447
            //欠拟合，两个值都低
------------------- 多项式回归 -------------------
训练集 0.9336239312662699
测试集 0.6170018547744414
            //过拟合，训练的高，测试的低


说明：
    一次幂 欠拟合
    二次幂 过拟合

'''


