
'''
ndarray 的基本属性
数组的索引
'''

import numpy as np


ary = np.arange(1, 9)
print(ary)

print("==" * 20)
ary.shape = (2, 4)    # 针对二维数组，修改形状
print(ary)

print("==" * 20)
ary.shape = (4, 2)    # 针对二维数组，修改形状
print(ary)



print("==" * 20)


print(ary[0][0])       # 旧写法，拿第1行的第1个元素
print(ary[0, 0])       # 新的写法，拿第1行的第1个元素  ary[列的索引, 行的索引]




print("==" * 20)
ary.shape = (2, 2, 2)  # 针对三维数组，修改形状
print(ary)

print("==" * 20)
print(ary[0][0][0])     # 旧写法，拿第1页的第1行的第1个元素
print(ary[0, 0, 0])     # ary[页的索引, 列的索引, 行的索引]

