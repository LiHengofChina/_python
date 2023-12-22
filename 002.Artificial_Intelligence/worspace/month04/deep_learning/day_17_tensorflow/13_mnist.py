'''
手写体识别2
        模型：全连接神经网络（1层：这一层直接就是输出层）
        拿两张图进行预测
'''



import tensorflow as tf


from tensorflow.examples.tutorials.mnist import input_data

#加载数据
mnist = input_data.read_data_sets('../MNIST_data/',  # 加载文件路径
                                  one_hot=True)          # 以独热编码的方式表示



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


saver = tf.train.Saver()

#拿到2张图像，执行预测

with tf.Session() as sess:

    sess.run(tf.global_variables_initializer())

    saver.restore(sess, '../../model/mnist/')  # 加载模型


    #从测试集中拿张两图片进行预测
    test_x, test_y = mnist.test.next_batch(2)

    pred_val = sess.run(pred_y, feed_dict={x: test_x})

    print('真实类别：', tf.argmax(test_y, 1).eval())
    print('预测类别：', tf.argmax(pred_val, 1).eval())
    print('概率：', tf.reduce_max(pred_val, 1).eval())


    #显示图像
    import pylab
    img1 = test_x[0]
    img1 = img1.reshape(28, 28)
    pylab.imshow(img1)
    pylab.show()

    img2 = test_x[1]
    img2 = img2.reshape(28, 28)
    pylab.imshow(img2)
    pylab.show()
