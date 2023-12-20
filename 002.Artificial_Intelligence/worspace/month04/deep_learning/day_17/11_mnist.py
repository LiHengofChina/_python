'''
手写体识别
        模型：全连接神经网络（1层：这一层直接就是输出层）

        MNIST_data数据说明：
            训练集有 60000 个，测试集有 10000个
            图像是单通道的灰度图像，大小为 28*28 像素

        类别为： 0~9  10个数字

        它是值是转成了10个类别的：相对概率，


最后这个模型的精度：大约是 91% 或 92% 的样子，不能继续提升，
因为这个模型相对来说比较简单了。


'''



import tensorflow as tf
import os.path

from tensorflow.examples.tutorials.mnist import input_data


#加载数据
mnist = input_data.read_data_sets('../MNIST_data/',      # 加载文件路径
                                  one_hot=True)          # 以独热编码的方式表示


# mnist.train   拿到训练集
# mnist.test    拿到测试集


# （1）定义占位符
x = tf.placeholder('float32', shape=[None, 784]) #这里每个图片 “已经拉伸成了 784” 个特征了。
y = tf.placeholder('float32', shape=[None, 10]) #10列表示每个样本的相对概率

# （2）定义权重，权重个数 (784,10)
w = tf.Variable(tf.random_normal(shape=[784, 10]))  # 标准的正太分布

# （3）定义偏置
b = tf.Variable(tf.zeros(shape=[10]))  # or  shape=(10,)

# （4）构建模型：全神经连接： x * w + b
pred_y = tf.nn.softmax(tf.matmul(x, w) + b)  # 注意顺序x在前x在后，矩阵没有乘法交换率
                                             # tf.matmul(x,w)  +  b得到的神经网络的输出
                                             # softmax 是激活函数，使用 softmax转成相对概率
                                             # 得到的是预测值。


# （5）构建 “损失函数”：交叉熵
loss = -tf.reduce_sum(y * tf.log(pred_y),
                      reduction_indices=1  # 水平方向求和
                      )
cost = tf.reduce_mean(loss)  # 平均交叉熵损失



# （6）梯度下降
train_op = tf.train.GradientDescentOptimizer(0.01 #学习率
                                             ).minimize(cost)


# （7）开始执行
#  由于训练数据量太大，使用 "小批量" 进行训练

batch_size = 100 #批次大小

saver = tf.train.Saver()

#执行
with tf.Session() as sess:

    sess.run(tf.global_variables_initializer())  # 变量初始化

    #开始训练之前，检查是否有模型保存，如果有，就接着上一次的继续训练
    if os.path.exists('../../model/mnist/checkpoint'):
        saver.restore(sess,'../../model/mnist/') #加载模型,

    # 60000 万个样本，假如我训练10轮
    #开始训练，小批量梯度下降
    for epoch in range(10):  # 外层控制轮数
        #计算总的批次数 ，每个批次100个样本，600*100=60000 # # 这样每轮才能每轮训练完6万个样本
        total_batch = int(mnist.train.num_examples / batch_size)

        total_cost = 0.0
        for i in range(total_batch):# 内层控制 "总批次数" ，
            train_x, train_y = mnist.train.next_batch(batch_size) #随机取100个样本
            o, c = sess.run([train_op, cost],
                            feed_dict= {x: train_x, y: train_y})

            total_cost += c   # 返回：c是一个批次的损失值，c 是100个样本损失值的平均值

        avg_cost = total_cost / total_batch # c累加在一起就是 “这一轮” 的 “所有批次” 的平均损失值，
                                            #每一轮的平均损失值
        print('轮数：{},cost：{}'.format(epoch, avg_cost))
        #可以看到损失值是在不断的减小


        #====================
        # 每训练一轮，进行一次评估：评估、精度，#或者移动到外层循环，只打印一次
        tf.argmax(y, axis=1)        # 真实类型
        tf.argmax(pred_y, axis=1)   # 预测类别

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

