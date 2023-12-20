
'''
    使用TensorFlow搭建线性回归
'''
import tensorflow as tf

################################################################## （1）准备样本数据
#伪造一组样本数据
x = tf.random_normal(shape=[100,1], #100行1列
                     mean=1.75,     #期望值为 1.75
                     stddev=0.5     #标准差为0.5
                     )
#通过 y = 2x+5 得到y值，
# 其实这里我已经知道，权重 和偏置是多少了，因为我们y值是通过 2x+5 得到的
# 所以训练的结果也是 x接近2，2接近5
y = tf.matmul(x,[[2.0]]) + 5.0  # x和 一个 "一行一列的2" 相乘，矩阵相乘

################################################################## （2）构建模型
#现在是输入一个特征，输出一个值，
#一个特征 和 一个神经元进行全连接， 产生一个结果，也只有一个w，它是一行一列，偏置也是一个
#（2.1）权重和偏置
w = tf.Variable(tf.random_normal(shape=[1,1]), trainable=True)
                #trainable=True训练过程中允许变化,默认也是True
b = tf.Variable(0.0,trainable=True)

#（2.2）构建模型
pred_y = tf.matmul(x,w) + b # 一个x与一个神经元进行全连接，再加上偏置，得到一个结果

#损失函数：均方误差 Σ((y-y')^2)/n
loss = tf.reduce_mean(tf.square(y - pred_y))

#梯度下降，求损失函数的极不值#使用 “梯度下降优化器，求损失函数的极小值”
train_op = tf.train.GradientDescentOptimizer(0.1 #学习率
                                  ).minimize(loss)


################################################################## （3）运行
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer()) #变量初始化

    for i in range(500):
        sess.run(train_op)
        print('轮数：{},w:{},b{}'.format(i+1,
                                        w.eval(),
                                        b.eval()))
















