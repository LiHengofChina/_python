
'''
自定义复合类型
列与列之前可以是不同的类型，
但是在同一列内类型必须相同
'''

import numpy as np

# 数组套元祖的类型
data = [('zs', [100, 100, 100], 18),
        ('ls', [90, 90, 90], 19),
        ('ww', [80, 80, 80], 20)
        ]

# 转换成数组 #另一种写法，通过字典的方式
ary = np.array(data, dtype={'names': ['name', 'scores', 'ages'],        #名字
                            'formats': ['U3', '3int32', 'int32']})      #元素类型

print(ary[0]['name'], "--", ary[0]['scores'], "--", ary[0]['ages'])
print(ary.itemsize)

#年龄的平均值
print("==" * 20)
print(ary['ages'])
print((ary['ages']).mean())


#分数的平均值
print("==" * 20)
print(ary['scores'])
print("==" * 20)
print((ary['scores']).mean(axis=1))         #每个样本的平均值(每一行的平均值) ，axis表示轴# 而axis=1表示沿着行轴计算平均值。
print((ary['scores']).mean(axis=0))         #求每一列的平均值 ，# axis=0表示沿着列轴计算平均值，
print((ary['scores']).mean())               #全部的平均值
