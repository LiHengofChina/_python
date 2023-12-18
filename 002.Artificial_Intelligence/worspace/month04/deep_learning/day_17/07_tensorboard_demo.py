import tensorflow as tf

x = tf.constant(100.0, name='xxx')
y = tf.constant(200.0, name='yyy')
res = tf.add(x, y, name='add')

with tf.Session() as sess:
    print(sess.run(res))

    tf.summary.FileWriter('../summary/',
                         graph=sess.graph) #将sess.graph中的op，全部写到事件文件当中去。






#================================================
import numpy as np
import tensorflow as tf
print("NumPy version:", np.__version__)
print("TensorFlow version:", tf.__version__)

