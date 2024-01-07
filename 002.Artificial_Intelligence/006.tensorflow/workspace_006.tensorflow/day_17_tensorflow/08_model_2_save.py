import tensorflow as tf

'''
   tf 的 模型保存
'''

################################################################## 【1】定义
# （1）准备样本数据
x = tf.random_normal(shape=[100, 1],
                     mean=1.75,
                     stddev=0.5
                     )

y = tf.matmul(x, [[2.0]]) + 5.0

# （2）构建模型

# 权重
w = tf.Variable(tf.random_normal(shape=[1, 1]), trainable=True)

# 偏置
b = tf.Variable(0.0, trainable=True)

# 构建模型
pred_y = tf.matmul(x, w) + b

# 损失函数：均方误差 Σ((y-y')^2)/n
loss = tf.reduce_mean(tf.square(y - pred_y))

# 定义梯度下降op
train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

# 收集损失函数的值
tf.summary.scalar('losses', loss)
merged = tf.summary.merge_all()  # 合并变量，把收集下来的损失值，转换成能够写入到事件文件的一个格式
saver = tf.train.Saver()

################################################################## 【2】运行
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())  # 变量初始化

    fw = tf.summary.FileWriter('../summary/', graph=sess.graph)
    for i in range(200):
        sess.run(train_op)

        summary = sess.run(merged)
        fw.add_summary(summary, i + 1)

        print('轮数：{},w:{},b{}'.format(i + 1,
                                        w.eval(),
                                        b.eval()))

    ##保存的是训练200轮之后的模型
    saver.save(sess, '../model/lr/')  # 保存的是训练200轮之后的模型
