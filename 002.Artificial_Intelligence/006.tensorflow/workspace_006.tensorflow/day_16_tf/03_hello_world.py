

import tensorflow as tf


import tensorflow as tf
print("TensorFlow 版本:", tf.__version__)


'''
    第一个tensorflow程序
    ———————————————————— 创建张量
'''

#定义：
hello = tf.constant('hello world') #创建 普通张量 #这里相当于计划去创建某个变量


#执行
sess = tf.Session()

res = sess.run(hello)

print(res)


sess.close()
