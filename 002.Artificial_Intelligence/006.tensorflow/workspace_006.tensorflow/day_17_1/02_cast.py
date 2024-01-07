
import tensorflow as tf


'''
    张量的数据类型转换
    整数————>浮点
    浮点————>整数
    布尔————>整数
'''

#定义
ones = tf.ones(shape=(2, 3), dtype='int32')

#转换： 整数————>浮点
# tf.cast 通用转换方法
temp = tf.cast(ones, 'float32')

with tf.Session() as sess:
    # print(ones.eval())
    # print(temp.eval())
    print(sess.run([ones,temp]))



