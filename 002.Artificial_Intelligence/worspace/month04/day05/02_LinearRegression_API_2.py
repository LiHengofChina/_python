'''

    通过sklearn接口来实现  "线性回归"
    实际工作中，我们使用sklearn的线性回归接口，就可以了

    划分 "训练集" 和 "测试集"

    用 "训练集" 训练模型
    用 "测试集" 评估模型
'''

import pandas as pd

import sklearn.preprocessing as sp
import sklearn.linear_model as lm  # 线性模型
import sklearn.metrics as sm       # 评估模块

import matplotlib.pyplot as plt


# （1）. 整理输入和输出
data = pd.read_csv('../data_test/Salary_Data.csv',
                   sep=',')

res = sp.scale(data)
train_x = data.iloc[:, :-1]
train_y = data.iloc[:, -1]



# （2）构建模型
model = lm.LinearRegression()

# （3）用已知输入、输出数据集训练回归器
model.fit(train_x, train_y)
#训练之后，可以打印出权重 和 偏置
print('coef_：',model.coef_) #权重，所有权重，返回列表，几组x就有几组权重
print('intercept_：',model.intercept_) #偏置


# （4）测试模型
# pred_y = model.predict(train_x)
# plt.plot(train_x, pred_y, color='orangered') #画出回归线 # 注意：这个是图线，下面是画点
# plt.scatter(train_x,train_y) #用散点图，画出样本数据
# plt.tight_layout()
# plt.show()

#从全部数据中，抽取一部分数据，作为测试集（假设测试集没参加过训练）
test_x = train_x.iloc[::4] #测试集的输入，开始位置和结束位置省略，步长为4
test_y = train_y[::4]      #测试集的输出，开始位置和结束位置省略，步长为4
        # test_y 是真实值，
pred_tets_y = model.predict(test_x)
# 将test_x带到模型中得到的是预测值

#===================
#评估指标

print('平均绝对误差-MAE：', sm.mean_absolute_error(test_y, pred_tets_y))
                                # 第一个参数是真实值，第二个是预测值
                                # 根据实际情况判官模型是否可用
                                # 一般看这个

print('均方误差-MSE：', sm.mean_squared_error(test_y, pred_tets_y))
                                # 第一个参数是真实值，第二个是预测值
                                # 这个值比较大，因为它是平方的结果
                                # 一般不看这个

print('中位数绝对偏差-MAD：', sm.median_absolute_error(test_y, pred_tets_y))
                                # 第一个参数是真实值，第二个是预测值
                                # 这个值和 "平均绝对误差"应该是差不多的
print('中位数绝对偏差-MAD：', sm.median_absolute_error(test_y, pred_tets_y))
                                # 第一个参数是真实值，第二个是预测值
                                # 这个值和 "平均绝对误差"应该是差不多的
print('r2_score：', sm.r2_score(test_y, pred_tets_y))
                                # 第一个参数是真实值，第二个是预测值
                                # 趋向于1，模型越好；趋向于0，模型越差.
# 0.96，这里得分比较高，因为我们的测试数据参加了训练。
# 这个模型能不能用，主要看 MAE
# 分再高也可能有误差，分可以用来比较两个模型的好坏


# 画出图形
# plt.plot(test_x, pred_tets_y, color='orangered') #画出回归线
# plt.scatter(test_x,test_y) #用散点图，画出样本数据
# plt.tight_layout()
# plt.show()
