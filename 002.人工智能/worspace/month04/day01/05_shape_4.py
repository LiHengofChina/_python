
'''
数组的维度操作

就地变维

'''

import numpy as np

ary = np.arange(1, 9)
print(ary.shape)
print("==" * 20)


ary.shape = (2, 4)
print(ary.shape)


print("==" * 20)
ary.resize(2, 2, 2)
print(ary.shape)
