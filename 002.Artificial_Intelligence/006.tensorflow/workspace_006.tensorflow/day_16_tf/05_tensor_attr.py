
import tensorflow as tf

'''
    ———————————————————— 
    查看张量的： 属性
        （1） 名称
        （2） 数据类型
        （3） 形状
'''

#定义
x = tf.constant(100.0,
                name='my_tensor',
                dtype='float64',
                shape=(2,3))


print('dtype:',x.dtype)
print('shape:', x.shape)
print('name:', x.name)

