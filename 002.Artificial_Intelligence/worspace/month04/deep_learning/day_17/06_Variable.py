'''
变量： 可以进行持久化
变量在执行前需要进行初始化
'''

import tensorflow as tf


#权重#生成了3行4列的，符合标准正太分布的随机数，作为w权重的初始值。
init_val = tf.random.normal(shape=(3, 4),
                            mean=1.8,
                            stddev=1.0)
w = tf.Variable(initial_value=init_val)

#偏置
init_b = tf.ones(shape=(4,)) #4个1
b = tf.Variable(initial_value=init_b)

# init_op = tf.global_variables_initializer()           # 1.14的写法
# with tf.Session() as sess:
#     sess.run(init_op)
#     w_res, b_res = sess.run([w, b])
#     print(w_res)
#     print(b_res)

# 2.x运行 ，2.x无需初始化
w_res, b_res = w.numpy(), b.numpy()

print(w_res)    #3行4列的权重
print(b_res)    #1行4列的偏置





