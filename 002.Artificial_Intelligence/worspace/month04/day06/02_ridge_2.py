
'''
    //====================
    岭回归
        只是创建模型的过程不一样，其它都是一样的

'''
import pandas
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.linear_model as lm


data = pd.read_csv('../data_test/Salary_Data2.csv', sep=',')
print(data.head())


# 准备输入和输出数据
train_x = data.iloc[:, :-1]
train_y = data.iloc[:, -1]

# 构建模型  “线性模型”
model = lm.LinearRegression()

# 构建模型  “岭回归模型”
# ridge = lm.Ridge(alpha=120, max_iter=1000)
ridge = lm.Ridge(alpha=98, max_iter=1000)
        #(1) alpha指 "正则化系数"，默认值是1
        # "正则化系数" 设置多大，这个需要自己评估，它也是超参数。
        # alpha为0时，它就是线性回归。

        #(2) solver 指的是使用 "闭式解（最小2乘法）"，还是 "迭代求解（梯度下降法）"
        # solver 意思是使用自动，能用什么用什么

        #(3)max_iter 一般使用默认

# 训练模型
model.fit(train_x,train_y)
ridge.fit(train_x,train_y)



# 使用模型进行预测
pred_y = model.predict(train_x) #这里暂时把训练的数据拿去预测
ridge_y = ridge.predict(train_x) #这里暂时把训练的数据拿去预测
# print(pre_y)




# 将 “样本数据” 画成散点图
plt.scatter(train_x,train_y)

# 将 “预测结果” 画成一条线
plt.plot(train_x, pred_y, color='orangered')
plt.plot(train_x, ridge_y, color='black')

plt.tight_layout()
plt.show()










