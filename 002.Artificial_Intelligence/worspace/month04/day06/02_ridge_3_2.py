'''
    使用 "线性回归" 对 Salary_Data2.csv进行建模
    建立模型、执行预测、得到回归线

    //====================
    岭回归
        只是创建模型的过程不一样，其它都是一样的
        for循环去遍历 alpha每一个取值，看谁的得分高，
    //====================
    通过遍历参数，构建模型的方式，寻找最优的模型参数
    //==================
    查看不方便
    把参数作为索引，把分数作为值， 然后拿到最大值的索引，
'''
import pandas as pd
import sklearn.linear_model as lm
import  numpy as np
import sklearn.metrics as sm       # 评估模块

data = pd.read_csv('../data_test/Salary_Data2.csv', sep=',')

# 准备输入和输出数据
x = data.iloc[:, :-1]
y = data.iloc[:, -1]

#创建一个测试集 #这里暂时把训练的数据拿去预测
test_x = x.iloc[:30:4]
# print(type(test_x))
test_y = y[:30:4]
# print(type(test_y))


# params = np.arange(50,501,50)
# params = np.arange(50,150,10)
params = np.arange(90,110,1)


scores = []
# 构建模型  “岭回归模型”
for i in params:
    ridge = lm.Ridge(alpha=i)
    ridge.fit(x, y)                         #训练
    ridge_test_y = ridge.predict(test_x)    #拿 "测试集数据" 进行预测
    scores.append(sm.r2_score(test_y, ridge_test_y))

# print(scores)
#求列表的最大值索引
max_value = max(scores)
max_index = scores.index(max_value)
print(max_index + 90)
