
'''
自定义复合类型
列与列之前可以是不同的类型，
但是在同一列内类型必须相同

示例：求平均值
'''

import numpy as np

# 数组套元祖的类型
data = [('zs', [100, 100, 100], 18),
        ('ls', [90, 90, 90], 19),
        ('ww', [80, 80, 80], 20)
        ]

# 转换成数组
# ary = np.array(data, dtype=[('name', 'U10'), ('scores', '3int'), ('age', 'int')])  #分数指定为3int

# ary = np.array(data, dtype=[('name', 'U2'), ('scores', 'object'), ('age', 'int')])  #分数指定为一个对象，会变成列表

ary = np.array(data, dtype='U2,3int32,int32')                                       #另一种指定方式
print(ary)



#年龄的平均值
print("==" * 20)
print(ary['f2'])
print((ary['f2']).mean())


#分数的平均值
print("==" * 20)
print(ary['f1'])
print("==" * 20)
print((ary['f1']).mean(axis=1))         #每个样本的平均值(每一行的平均值) ，axis表示轴# 而axis=1表示沿着行轴计算平均值。
print((ary['f1']).mean(axis=0))         #求每一列的平均值 ，# axis=0表示沿着列轴计算平均值，
print((ary['f1']).mean())               #全部的平均值
