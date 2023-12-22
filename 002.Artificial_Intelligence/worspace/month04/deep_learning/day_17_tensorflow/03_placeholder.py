'''

    占位符：一般用于样本数据

    #如果把数据传入 “训练集” ，就是对 “训练集” 进行计算
    #如果把数据传入 “测试集” ，就是对 “测试集” 进行计算

'''
import tensorflow as tf
import numpy as np

plhd = tf.placeholder('float32', shape=[None, 3])  # None不管有多少行，特征数一样就行，特征数量必须一样。
with tf.Session() as sess:
    data = np.arange(1, 7).reshape(2, 3)
    res = sess.run(plhd,
                   feed_dict={plhd: data})  # 给占位符号传参
    print(res)
