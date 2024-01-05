
'''
    张量的数据类型转换

'''
import tensorflow as tf
#定义
ones = tf.ones(shape=(2, 3), dtype='int32')

#转换
temp = tf.cast(ones, 'float32')


#执行
print(ones.numpy()) #在 “即时执行模式” 下执行
print(temp.numpy()) #在 “即时执行模式” 下执行


