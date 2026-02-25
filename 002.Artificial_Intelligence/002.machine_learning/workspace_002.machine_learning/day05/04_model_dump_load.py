'''
    保存模型 在训练完成模型之后保存 "模型"

    加载模型，执行预测

'''

import pandas as pd

import sklearn.preprocessing as sp
import sklearn.linear_model as lm  # 线性模型
import sklearn.metrics as sm       # 评估模块

import pickle  #保存模型


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

#================================================================
#从全部数据中，抽取一部分数据，作为测试集（假设测试集没参加过训练）
test_x = train_x.iloc[::4] #测试集的输入，开始位置和结束位置省略，步长为4
test_y = train_y[::4]      #测试集的输出，开始位置和结束位置省略，步长为4
        # test_y 是真实值，


pred_tets_y = model.predict(test_x)
# 将test_x带到模型中得到的是预测值

#================================================================
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

print('r2_score：', sm.r2_score(test_y, pred_tets_y))
                                # 第一个参数是真实值，第二个是预测值
                                # 趋向于1，模型越好；趋向于0，模型越差.

#=================================================================#在最后保存模型

# wb 表示 以 "二进制写入模式" 打开文件
with open('../day05/model.pickle', 'wb') as f :
    pickle.dump(model,f)
    # 把 model 对象保存到f中去
    # 注意是 dump ， 不是 dumps没有s
    #  后缀名可以是任意的，但一般是 .pickle 或 .pkl
    # 注意：保存的是一个二进制文件。
print('save succss')

#======================================#加载模型
with open('../day05/model.pickle', 'rb') as f:
    new_model = pickle.load(f)

# 这种写法支警告
# new_test_x = pd.DataFrame([
#     [1.1],
#     [2.2]
# ])
new_test_x = pd.DataFrame({'YearsExperience': [1.1, 2.2]})

print(type(new_test_x))
res = new_model.predict(new_test_x) # 预测，打印预测结果
print(res)



