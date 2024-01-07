
import tensorflow as tf

'''
张量形状的惊变
    静态形状：  一维只能到一维、二维只能到二维，不能跨维度，只能执行一次

    动态形状：   可以跨维度，可以多次，因为拿到不同的对象
'''

plhd = tf.placeholder('float32',(None,3))

############################################################### 静态形状，指：set_shape 和 get_shape的操作
print(plhd)  # 可以看到：shape=(?,3)

plhd.set_shape([4, 3])  # 设置静态形状
print(plhd)  # 现在看到shape=(4,3)
print(plhd.get_shape())  # 现在看到shape=(4,3)

# plhd.set_shape([3,4]) #设置静态形状，只能设置一次，打开这一行会报错，只能设置一次，上面了

# ############################################################### 动态形状，指：reshape的操作

res = tf.reshape(plhd, [1, 4, 3])
print(res)  # shape=(1,4,3)

res = tf.reshape(plhd, [4, 1, 3]) #
print(res)  # shape=(1,4,3)

print(plhd)  # 原始数据来是shape=(4,3)，因为它不修改原始数据


