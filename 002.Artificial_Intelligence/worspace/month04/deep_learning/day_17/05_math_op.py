'''
张量的数据计算
'''

import tensorflow as tf

#定义
x = tf.constant([[1,2],
                 [3,4]],
                dtype='float32')
y = tf.constant([[1,2],
                 [3,4]],
                dtype='float32')
add = tf.add(x,y)
mul = tf.matmul(x,y)
# log = tf.log(x)    #求x中每一个元素的自然对数  1.14
log = tf.math.log(x) #求x中每一个元素的自然对数  2.15
sum_x = tf.reduce_sum(x, axis=0)



data    = tf.constant([1,2,3, 4,5,6, 7,8,9])
segment = tf.constant([0,0,0, 1,1,1, 2,2,2])      #0、1、2是三个片段
# res     = tf.segment_sum(data,segment)          #1.14 计算张量片段总和
res       = tf.math.segment_sum(data, segment)    #2.15 计算张量片段总和





# #执行 1.14
# with tf.Session() as sess:
#     print(add.eval())
#     print(mul.eval())
#     print(log.eval())
#     print(sum_x.eval())
#     print(res.eval())

#执行 2.15
print(add.numpy())
print(mul.numpy())
print(log.numpy())
print(sum_x.numpy()) #求每一列的和
print(res.numpy())   #计算张量片段总和



