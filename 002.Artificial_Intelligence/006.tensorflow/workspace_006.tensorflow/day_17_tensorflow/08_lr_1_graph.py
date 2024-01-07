
import tensorflow as tf

'''
    使用TensorFlow搭建线性回归
            ---加入tensorboard
            （1）.收集变量
                    #收集损失函数的值
                    tf.summary.scalar('losses',loss)
            （2）.合并变量
                    #把收集下来的损失值，转换成能够写入到事件文件的一个格式
                    merged = tf.summary.merge_all()

'''
################################################################## 【1】定义
# （1）准备样本数据
x = tf.random_normal(shape=[100, 1],
                     mean=1.75,
                     stddev=0.5)
y = tf.matmul(x, [[2.0]]) + 5.0

# （2）构建模型

# 权重
w = tf.Variable(tf.random_normal(shape=[1, 1]), trainable=True)
# 偏置
b = tf.Variable(0.0, trainable=True)

# 构建模型
pred_y = tf.matmul(x, w) + b  #

# 损失函数：均方误差 Σ((y-y')^2)/n
loss = tf.reduce_mean(tf.square(y - pred_y))

# 定义梯度下降op
train_op = tf.train.GradientDescentOptimizer(0.1 ).minimize(loss)

#收集损失函数的值
tf.summary.scalar('losses', loss)
#合并变量，把收集下来的损失值，转换成能够写入到事件文件的一个格式
merged = tf.summary.merge_all()

################################################################## 【2】运行
with tf.Session() as sess:

    sess.run(tf.global_variables_initializer()) #变量初始化

    fw = tf.summary.FileWriter('../summary/',
                          graph=sess.graph)  #
    for i in range(500):

        sess.run(train_op)
        #每运行一次就收集一次，然后加入文件中
        summary = sess.run(merged) #返回的结果才是收集的损失值
        fw.add_summary(summary,i+1)

        print('轮数：{},w:{},b{}'.format(i+1,
                                        w.eval(),
                                        b.eval()))


