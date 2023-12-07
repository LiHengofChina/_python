
'''
ndarray 的基本属性
数据类型
'''

import numpy as np

#创建布尔类型的元素
ary = np.zeros(shape=(3, 3), dtype='bool')
print(ary)
ary = np.zeros(shape=(3, 3), dtype='bool_')
print(ary)
ary = np.zeros(shape=(3, 3), dtype='?')
print(ary)

print("==" * 20)
ary = np.array([1, 2, 3, 4, 5], dtype='int8')  #
print(ary)

print("==" * 20)
# ary = np.array([100, 200, 300, 400, 500], dtype='int8')  # dtype和实际值的类型不一样，此时就会有问题
ary = np.array([100, 200, 300, 400, 500], dtype='int64')  # dtype和实际值的类型不一样，此时就会有问题
print(ary)




