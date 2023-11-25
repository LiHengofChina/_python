
'''
    使用 "线性回归" 对 Salary_Data2.csv进行建模
    建立模型、执行预测、得到回归线
'''

import pandas as pd
import matplotlib.pyplot as plt
import sklearn.linear_model as lm #线性模型模块


data = pd.read_csv('../data_test/Salary_Data2.csv', sep=',')
print(data.head())


# 准备输入和输出数据
train_x = data.iloc[:, :-1]
train_y = data.iloc[:, -1]


# 构建模型
model = lm.LinearRegression()


# 训练模型
model.fit(train_x,train_y)
print(model.coef_)          #打印出权重(w0)
print(model.intercept_)     #打印偏置


# 使用模型进行预测
pred_y = model.predict(train_x) #这里暂时把训练的数据拿去预测
# print(pre_y)




# 将 “样本数据” 画成散点图
plt.scatter(train_x,train_y)

# 将 “预测结果” 画成一条线
plt.plot(train_x, pred_y, color='orangered')

plt.tight_layout()
plt.show()







