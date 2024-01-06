

import tensorflow as tf
'''
  ————————————————————  优化写法
'''

#【1】定义: 定义了步骤,并没有执行
x = tf.constant(100.0)
y = tf.constant(200.0)
res  = tf.add(x,y)

#【2】执行 ，用 with 创建，
with tf.Session() as sess:
    result = sess.run(res)
    print(result)


