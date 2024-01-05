
'''

  如何 ： 划分 "训练集"和"测试集"
    //=====================================
    常用的 "训练集"和 "测试集" 划分比例
    9:1 8:2 7:3

    这些常用的划分比例，sklearn也准备也相关的接口
    在 sklearn.model_selection 里面

    sklearn.model_selection 里面主要是放置的是优化的接口
    网络搜索、调参、划分、“训练集“ 和 ”测试集”

    训练集    train
    测试集    test
    划分叫    split

'''


import sklearn.model_selection as ms #模型选择
import pandas as pd
import matplotlib.pyplot as plt

# 数据来自：data_url = "http://lib.stat.cmu.edu/datasets/boston"
data = pd.read_csv('04_boston_data.csv', sep=',', header=None)


##==========================================  # （1）整理输入和输出
x = data.iloc[:, :-1]
y = data.iloc[:, -1]


##==========================================  # （2）划分 "训练集"和"测试集"
# 注意： “训练数据” 不能有顺序（随机打乱），因为它可能会学到顺序
# data = ms.train_test_split(x,y,
#                         test_size=0.2,
#                         random_state= 7
#                         )
                        # 0.2 表示测试集占比 20%
                        # x 和 y都会被分成两份
                        # 默认会随机打乱顺序，
                        #=========================================
                        # 使用 random_state 随机种子，固定某一种随机方式
                        # random_state=7，这样每次顺序不同，但是数据不会变。
                        # 种子取值必须是：0 到 2**23-1之间，uint32的值，42亿
# print(len(data))  # 4 两个训练集，两个测试集
#
# print(data[0].shape)  #训练集x
# print(data[1].shape)  #测试集x
# print(data[2].shape)  #训练集y
# print(data[3].shape)  #测试集y
#==========================================

train_x,test_x,train_y,test_y = ms.train_test_split(x,y,
                        test_size=0.2,
                        random_state= 7)
print(train_x.shape)
print(test_x.shape)
print(train_y.shape)
print(test_y.shape)


##==========================================  # （3）根据 "训练集" 训练模型
# 选择模型： 很多模型都能解决这个问题，哪个预测的准就使用哪一个
# 分别构建 "线性回归"、"岭回归"、"多项式回归" 看谁更好
# 评估每一个模型的R2得分






