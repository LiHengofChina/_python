
import numpy as np
import tensorflow as tf

'''
    (1)创建张量
    (2).eval() ,执行某一个op
'''

#========================== 定义
#创建张量
tensor1d = tf.constant([1, 2, 3, 4, 6])                 #一维张量
tensor2d = tf.constant(np.arange(1, 7).reshape(2, 3))   #二维张量
ones = tf.ones(shape=(2, 3), dtype='int32')
zeros = tf.zeros(shape=(2, 3), dtype='int32')
zeros_like = tf.zeros_like(tensor1d)

# #随机正太分布
tensornd = tf.random_normal(shape=(2, 2), mean=1.8,  # 期望值是1.8
                            stddev=1.0  # 标准差为1
                            )
#执行
with tf.Session() as sess:
    print(tensor1d.eval())
    print(ones.eval())
    print(tensor2d.eval())
    print(zeros_like.eval())
    print(zeros.eval())



