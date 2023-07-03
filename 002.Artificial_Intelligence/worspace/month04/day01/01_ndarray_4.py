'''
数组的基本创建
'''
import numpy as np

ary = np.arange(0.1, 1.2, 0.1)
print(ary)



print("==" * 20)
zero_like = np.zeros_like(ary, dtype='int32')
print(zero_like)



print("==" * 20)
one_like = np.ones_like(ary, dtype='int32')
print(one_like)





