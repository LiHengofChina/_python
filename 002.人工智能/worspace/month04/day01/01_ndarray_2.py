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





print("==" * 20)
pi = math.pi
print(pi)
print(-pi)


print("==" * 20)
#（1）先求步长
setp = pi * 2 / 200
#（2）再通过arange接口求出等差数列
ary = np.arange(-pi, pi, setp)
print(ary)

print("==" * 20)
ary = np.linspace(-np.pi, np.pi, 200)
print(ary)
