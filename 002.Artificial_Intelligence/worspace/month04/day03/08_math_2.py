'''
简单的数学指标
       最大值、最小值、极差
'''
import numpy as np


print("================1" * 10)
# 产生9个介于[10,100) 区间的随机数
a = np.random.randint(10, 100, 9)
print(a)
print(type(a))


print("================1" * 10)
print(np.max(a)) #最大
print(np.min(a)) #最小
print(np.ptp(a)) #极差

