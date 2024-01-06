'''
张量形状的惊变
    静态形状
    动态形状
'''
import tensorflow as tf
plhd = tf.placeholder('float32',(None,3))

############################################################### 静态形状
print(plhd) #可以看到：shape=(?,3)

plhd.set_shape([4,3]) #设置静态形状
print(plhd)  #现在看到shape=(4,3)

# plhd.set_shape([3,4]) #设置静态形状，只能设置一次，这一行会报错

############################################################### 动态形状

res = tf.reshape(plhd,1,4,3)
print(res) # shape=(1,4,3)

print(plhd) #原始数据来是shape=(4,3)，因为它不修改原始数据

with tf.Session() as sess:
    pass


