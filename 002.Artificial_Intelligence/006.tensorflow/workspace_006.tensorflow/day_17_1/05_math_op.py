import tensorflow as tf

'''
张量的数学 计算
'''

# 定义
x = tf.constant([[1, 2],
                 [3, 4]],
                dtype='float32')
y = tf.constant([[1, 2],
                 [3, 4]],
                dtype='float32')

add = tf.add(x, y)  # 加法

mul = tf.matmul(x, y)  # x的所有行乘以y的所有列，对应位置相乘，再相加

log = tf.log(x)  # 求x中每一个元素的自然对数  1.14

sum_x = tf.reduce_sum(x, axis=0)

#片段求和
data = tf.constant([1, 2, 3, 4, 5, 6, 7, 8, 9])
segment = tf.constant([0, 0, 0, 1, 1, 1, 2, 2, 2])  # 0、1、2是三个片段
res = tf.segment_sum(data, segment)


with tf.Session() as sess:
    print(add.eval())
    print(mul.eval())
    print(log.eval())
    print(sum_x.eval())
    print(res.eval())
