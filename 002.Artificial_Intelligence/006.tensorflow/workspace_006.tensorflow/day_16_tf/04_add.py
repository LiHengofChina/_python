

import tensorflow as tf
'''
  ————————————————————  定义 和 执行 分开
'''

#【1】定义: 定义了步骤,并没有执行
x = tf.constant(100.0)
y = tf.constant(200.0)
res  = tf.add(x,y)

#【2】执行
sess = tf.Session()
result = sess.run(res)
print(result)

#关闭
sess.close()

