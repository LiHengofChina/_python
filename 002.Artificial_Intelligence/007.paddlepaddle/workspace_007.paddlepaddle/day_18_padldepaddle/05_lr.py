'''
【本地运行】

使用paddle搭建：简单的线性回归



'''

import paddle.fluid as fluid
import numpy as np
import matplotlib.pyplot as plt

# 数据准备
train_x = np.array([[0.5], [0.6], [0.8], [1.1], [1.4]],
                   dtype='float32')
train_y = np.array([[5.0], [5.5], [6.0], [6.8], [7.1]],
                   dtype='float32')

#搭建模型
#占位符号
x = fluid.layers.data(name='xxx',
                      shape=[1],  # 这里只填 “一个样本的特征数”，一个样本有多少特征
                      dtype='float32')
y = fluid.layers.data(name='yyy',
                      shape=[1],
                      dtype='float32')
#全连接
pred_y = fluid.layers.fc(x,  # 输入数据
                         size=1  # 指神经元个数
                         # param_attr: ParamAttr = None,  #权重 也不指定，使用默认的
                         # bias_attr: ParamAttr = None,   #偏置 也不指定，使用默认的
                         # act: str = None,               #激活函数
                         )

#损失函数（均方误差 ）
#(y-y')^2
cost = fluid.layers.square_error_cost(input=pred_y,  # 预测值
                               label=y  # 真实值
                               )
avg_cost = fluid.layers.mean(cost) #求和除以n

# 梯度下降优化器
optimizer = fluid.optimizer.SGD(  #SGD随机梯度下降
    learning_rate=0.01  # 学习率
)
optimizer.minimize(avg_cost)#求极小值

#执行
place = fluid.CPUPlace()#指定CPU
# place = fluid.CUDAPlace(0)#指定GPU
exe = fluid.Executor(place=place)

#初始化
exe.run(fluid.default_startup_program())

iters = [] #收集每一轮 数量
costs = [] #收集每一轮的损失结果
for i in range(300):
    train_cost = exe.run(
        program=fluid.default_main_program(),
        feed={'xxx': train_x, 'yyy': train_y},
        fetch_list=[avg_cost]
    )
    iters.append(i + 1)
    costs.append(train_cost[0][0])
    print(train_cost)
    print(train_cost[0][0])

plt.plot(iters, costs)
plt.grid(linestyle=':')
# plt.savefig('train.png')
plt.show()
