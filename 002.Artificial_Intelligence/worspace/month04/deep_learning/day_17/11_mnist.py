'''
手写体识别
模型：全连接模型
'''



import tensorflow as tf
import os.path

from tensorflow.examples.tutorials.mnist import input_data


#加载数据
mnist = input_data.read_data_sets('../MNIST_data/', one_hot=True)


#定义占位符
x = tf.placeholder('float32', shape=[None, 784])
y = tf.placeholder('float32', shape=[None, 10])

#定义权重，权重个数 (784,10)
w = tf.Variable(tf.random_normal(shape=[784, 10])) #标准的正太分布
#定义权重，权重个数 (784,10)
b = tf.Variable(tf.zeros(shape=[10]))  #or  shape=(10,)

# 构建模型：全神经连接： x * w + b
pred_y = tf.nn.softmax(tf.matmul(x,w)  +  b)  # 注意顺序x在前x在后，矩阵没有乘法交换率
                                              # tf.matmul(x,w)  +  b得到的神经网络的输出
                                              # softmax 是激活函数

#构建 “损失函数”：交叉熵
loss = -tf.reduce_sum(y * tf.log(pred_y),
                      reduction_indices=1  # 水平方向求和
                      )
cost = tf.reduce_mean(loss)  # 平均交叉熵损失

#梯度下降
train_op = tf.train.GradientDescentOptimizer(0.01 #学习率
                                             ).minimize(cost)

batch_size = 100 #批次大小

saver = tf.train.Saver()

#执行
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())#初始化



    #开始训练之前，检查是否有模型保存
    if os.path.exists('../../model/mnist/checkpoint'):
        saver.restore(sess,'../../model/mnist/') #加载模型,

    # 60000 万个样本，假如我训练10轮
    #开始训练，小批量梯度下降
    for epoch in range(10):  # 外层控制轮数
        #计算总的批次数
        total_batch = int(mnist.train.num_examples /batch_size)

        total_cost = 0.0
        for i in range(total_batch):# 内层控制 "总批次数" ，每个批次100个样本，600*100=60000# # 这样每轮才能每轮训练完6万个样本
            train_x, train_y = mnist.train.next_batch(batch_size)
            params = {x: train_x, y: train_y}
            o, c = sess.run([train_op, cost],
                            feed_dict=params)
                            # c 是100个样本损失值的平均值
            total_cost += c
        avg_cost = total_cost / total_batch #每一轮的平均损失值
        print('轮数：{},cost：{}'.format(epoch, avg_cost))
        #可以看到损失值是在不断的减小


        #=====   每训练一轮，进行一次评估：评估、精度，#或者移动到外层循环，保打印一次
        tf.argmax(y, axis=1)      #真实类型
        tf.argmax(pred_y, axis=1) #预测类别

        corr = tf.equal(tf.argmax(y, axis=1),       # 真实类型
                        tf.argmax(pred_y, axis=1))  # 预测类别

        # 计算精度
        accuracy = tf.reduce_mean(tf.cast(corr, 'float32'))  # 求和除以n

        acc = sess.run(accuracy,
                       feed_dict={x: mnist.test.images,  # 测试集的全部图像
                                  y: mnist.test.labels  # 测试集的全部标签
                                  })
        print('测试集精度：', acc)

    saver.save(sess, '../../model/mnist/')

