

import tensorflow as tf


#定义: 定义了步骤,并没有执行
x = tf.constant(100.0)
y = tf.constant(200.0)
res  = tf.add(x,y)


# 1.14 执行
# sess = tf.Session()
# result = sess.run(res)
# print(result)
# sess.close()


# 2.15 执行
result = res.numpy()
print(result)

