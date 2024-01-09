'''

利用paddle实现多元回归
    多元指：多个 “自变量” 实现一个因变量

    波士顿房屋价格矩阵：13个x对应一个y 506个样本

    小批量梯度下降

'''

import paddle.fluid as fluid
import paddle
import matplotlib.pyplot as plt


import os


#数据准备 8: 2
reader = paddle.dataset.uci_housing.train()  # 拿到的是一个原始读取器
random_reader = paddle.reader.shuffle(reader, 1024)
train_reader = paddle.batch(random_reader,
                            20  # 每一次读取20个样本，
                                # 读取到第20批次样本时，就读取了400个，一共404个
                                #最后 4个就舍去了。
                            ,drop_last=True
                            )
#了解数据的结构
# print(next(train_reader())[0]) #[(x,y),(x,y)]
# print(len(next(train_reader())))

#构建模型

x = fluid.layers.data(name='xxx',
                      shape=(13,),  # 13个特征  ,13列1行
                      dtype='float32'
                      )  # 占位符号
y = fluid.layers.data(name='yyy',
                      shape=(1,),  # 1 个y值   ,1列1行
                      dtype='float32'
                      )  # 占位符号

#全连接
pred_y = fluid.layers.fc(input=x, #输出数据
                         size=1 #13个特征对应1个输出，也就是一个神经元
                         )

# 损失函数(均方误差)
cost = fluid.layers.square_error_cost(input=pred_y,  # input表示预测值
                                      label=y
                                      ) # 这一行表示： (y-y')^2
avg_cost = fluid.layers.mean(cost)  # 求和除以 n

#梯度下降优化器
optimizer = fluid.optimizer.SGD(
                learning_rate=0.001#学习率
                )
optimizer.minimize(avg_cost) #求损失函数的极小值



#执行
place = fluid.CPUPlace()#指定执行设备
exe = fluid.Executor(place=place)
#初始化
exe.run(fluid.default_startup_program())


# 参数喂入器，当月拿到 [([x1,x2,x3,x4],[y])] 的时候，x1,x2,x3,x4就传给feed_list=[x, y]的x. y就传给feed_list=[x, y]的y.
feeder = fluid.DataFeeder(feed_list=[x, y],  # 要喂哪个参数
                          place=place  # 喂给谁
                          )

#小批量下降，外层控制轮数，内层控制批次

iters = [] # 收集轮数
costs = [] # 损失值

for pass_id in range(100):  # 外层控制轮数

    train_costs = []  # 用列表存放损失值
    for data in train_reader():  # 拿到一个批次的数量#这里与tensorflow不同
        train_cost = exe.run(
            program=fluid.default_main_program(),   #
            feed=feeder.feed(data),                 # 上面的 “参数喂入器” 已经传入参数了。
            fetch_list=[avg_cost]                   # 每一轮的损失值
        )
        # feed 取值另一种写法
        # # [(x,y)] #把所有x整合到一起传给x，把所有y整合到一起传给y
        # feed = {'xxx': np.array([i[0] for i in data], dtype='float32'),  # 这里是每一个x放在列表中
        #         'yyy': np.array([i[1] for i in data], dtype='float32')  # 把每一个y放在一列表中
        #         },  # 传参数

        train_costs.append(train_cost[0][0]) #拿到值

    #每一轮的平均损失值
    train_avg_cost = sum(train_costs) / len(train_costs)

    iters.append(pass_id)
    costs.append(train_avg_cost)

    print('轮数：{},cost:{}'.format(pass_id,train_avg_cost ))

# 损失函数的可视化
plt.plot(iters, costs, color='orangered')
plt.savefig('train.png')
plt.show()


#保存模型
model_save_path  = '../model/uci_housing/'
if not os.path.exists(model_save_path):
    os.makedirs(model_save_path)

fluid.io.save_inference_model(model_save_path,  # 保存的路径 （保存的是推荐模型）
                              feeded_var_names=['xxx'],  # 喂入变量的名字
                              target_vars=[pred_y],  # 从哪里取结果？pred_y
                              executor=exe  # 要保存的模型
                              )

