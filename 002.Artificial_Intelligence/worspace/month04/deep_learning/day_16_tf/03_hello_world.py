
import tensorflow as tf


#定义：
hello = tf.constant('hello world') #创建 普通张量 #这里相当于计划去创建某个变量

#执行：
#1.14版本
# sess = tf.Session() #session对象
# res = sess.run(hello)
# print(res)
# sess.close()

#2.15版本
res = hello.numpy()

print(res) #它的机制 和 python程序的运行机制是不一样的
        # tf.Tensor(b'hello world', shape=(), dtype=string)

