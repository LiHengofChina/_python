'''
数组的基本创建
'''
import numpy as np
import math


ary = np.arange(0, 10, 3)
print(ary)

print("==" * 20)
ary = np.arange(0.1, 1.2, 0.1)
print(ary)




# 线性拆分
print("==" * 20)
ary = np.linspace(-np.pi, np.pi, 200)
print(ary)
