

import tensorflow as tf
'''

对   图   操作 

'''

#定义: 定义了步骤,并没有执行
x = tf.constant(100.0)
y = tf.constant(200.0)
res  = tf.add(x,y)

# 1.14
# graph = tf.get_default_graph()
# print('默认的图：',graph)

# 在 TensorFlow 2.x 中，你可以尝试获取默认图，但它可能返回 None
default_graph = tf.compat.v1.get_default_graph()
print('默认的图：', default_graph) # <tensorflow.python.framework.ops.Graph object at 0x0000022494538940

'''
在 TensorFlow 2.x 中，默认启用了 Eager Execution（即时执行），
因此不再需要显式地获取默认图（tf.get_default_graph()）。
在 Eager Execution 模式下，计算会立即执行，而不需要构建和运行图。


print(x.graph)

在 TensorFlow 2.x 中，默认情况下，Eager Execution 是启用的，
因此张量（如 x）没有关联到一个明确的图。
在 Eager Execution 模式下，每个操作都会立即执行而 "不需要构建图"。


'''



result = res.numpy()
print(result)

