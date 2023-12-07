
'''
ndarray 的基本属性
查看数组维度，修改数组维度

'''
import numpy as np


ary = np.arange(1, 9)
print(ary)


#查看数组的维度
print("==" * 20)
print(ary.shape)  # (8,)，查看它是几维数组


# 修改数组的维度
print("==" * 20)
ary.shape = (4, 2)
print(ary)


print("==" * 20)
ary.shape = (2, 2, 2)
print(ary)


print("==" * 20)
ary.shape = (1, 1, 1, 1, 1, 1, 1, 8)  # 8维
print(ary)


print("==" * 20)
ary.shape = (1, 1, 1, 1, 1, 2, 2, 2)  # 8维
print(ary)
