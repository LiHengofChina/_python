'''

    通过sklearn接口来实现  "线性回归"

    实际工作中，我们使用sklearn的线性回归接口，就可以了
'''

import pandas as pd

import sklearn.preprocessing as sp
import sklearn.linear_model as lm  # 线性模型

import matplotlib.pyplot as plt

'''
什么情况使用线性回归？
        一定是数据符合线性分布，才使用线性回归。
        示例： 一组薪资数据，一列X对应一列Y，正好是二维数据，
              可以用  "散点图"  查看  "数据的分布状态"
            scatter
'''
# （1）. 整理输入和输出
data = pd.read_csv('../../data_test/Salary_Data.csv',
                   sep=',')
# print(data['YearsExperience'])
# print(data['Salary'])
'''
    数据整理过程中，前面所有列都是x,最后一列才是y
'''
#  数据预处理：标准化
res = sp.scale(data)
# 输入集
train_x = res[:, :-1] #行取"所有行"，列 "不要最后一列"
            # 取第一列的方式 ： res[:, 0] 或 res.T[0]
            # train_x.resize(train_x.size, 1)#一维变二维
            # print(train_x.ndim)  # 获取维度数
            # print(train_x.shape)  # 获取形状，一维30行
# 输出集
train_y = res[:, -1] #只要最后一列

# 不标准化：打开这一 行
# train_x = data.iloc[:, :-1]
# train_y = data.iloc[:, -1]

# （2）构建模型
model = lm.LinearRegression()
                    # 两个可选参数：
                    # （1）fit_intercept=True ，是否训练偏置。
                    # （2）normalize=False，是否归一化处理。
                    #  y= w1x1 + w2x2 + ... + wnxn + w0
                    # lm.LinearRegression()生成的这个线性模型，不管有几个 "自变量" 它都可以接收。
                    # 此时，只有模型，并没有参数

                    #相当于创建： y = w1x1 + w2x2 + w3x3 + ... + wnxn + w0


# （3）用已知输入、输出数据集训练回归器，
model.fit(train_x, train_y) #把 "数据" 交给 "模型" 进行 "训练"
					        #此时能得到w1是多少，w0是多少......等等等
    						#此时 "模型参数" 就在 model 上面
        					#此时，就能拿模型，进行新的参数进行预测

                            #相当于：求解模型最优参数

#训练之后，可以打印出权重 和 偏置
print('coef_：',model.coef_) #权重，所有权重，返回列表，几组x就有几组权重
print('intercept_：',model.intercept_) #偏置


# （4）测试模型
pred_y = model.predict(train_x)  # 进行预测，把训练数据拿去预测
                                 # 怎么训练就需要怎么测试，
                                 # 训练的时候是二维的，测试的时候就必须是二维的
                                 # 训练的时候，对数据做了标签编码，测试的时候也必须标榜编码


'''
	学习率 和 训练次数什么的不用我们自己设置，

	因为在sklearn里面并不是使用 "梯度下降法" 来求参数最优值（"极小值"）的
			//所以没有学习率 和 轮数
	但是在后面 "深度学习" 里面使用的就是 "梯度下降法"
	同理：不管使用什么样的方式，只要能把 "最优模型参数" 求出来就可以了。
	所以：上面三行解决就能解决前面所有的问题
'''
# print(pred_y)

#画线
plt.plot(train_x, pred_y, color='orangered') #画出回归线 # 注意：这个是图线，下面是画点
plt.scatter(train_x,train_y) #用散点图，画出样本数据

plt.tight_layout()

plt.show()