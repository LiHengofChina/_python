'''
    创建张量
'''
import numpy as np
import tensorflow as tf

#========================== 定义
#创建张量
tensor1d = tf.constant([1,2,3,4,6])
tensor2d = tf.constant(np.arange(1,7).reshape(2,3))

ones = tf.ones(shape=(2, 3), dtype='int32')
zeros = tf.zeros(shape=(2, 3), dtype='int32')
zeros_like = tf.zeros_like(tensor1d)

# #随机正太分布
# tensornd = tf.random_normal(shape=(2,2), mean=1.8, stddev=1.0) #1.14写法
tensornd = tf.random.normal(shape=(2, 2), mean=1.8, stddev=1.0)  #2.15写法

print(tensor1d.numpy())  # print(tensor1d.eval()) eval() 方法仍然存在，但它通常与即时执行模式（Eager Execution）结合使用，
                         # 在即时执行模式下，你可以直接调用 numpy() 方法来获取张量的值。
print(tensor1d)          # print(tensor1d.eval())
print(tensor2d.numpy())  #
print(tensornd.numpy())
#执行




