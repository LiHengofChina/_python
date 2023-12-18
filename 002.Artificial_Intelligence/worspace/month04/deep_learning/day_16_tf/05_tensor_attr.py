
import tensorflow as tf



#定义
x = tf.constant(100.0,
                name='my_tensor',
                dtype='float64',
                shape=(2,3))

# print(x.name) # 在即时执行模式下，名称并不是一个显式的属性。
print('dtype:',x.dtype)
print('shape:', x.shape)
print('op:', x.op) # 在即时执行模式下，不再构建静态计算图，而是立即执行操作。



#运行
result = x.numpy()
print(result)
