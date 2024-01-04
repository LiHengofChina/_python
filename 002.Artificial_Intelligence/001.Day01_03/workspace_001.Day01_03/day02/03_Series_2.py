'''
Series示例
访问 Series
'''

import numpy as np
import pandas as pd

s01 = pd.Series([100, 90, 80, 70])
print(s01[0])
# print(s01[-1]) #没有反向索引

print("##" * 20)
s01 = pd.Series([100, 90, 80, 70], index=['zs', 'ls', 'ww', 'zl'])
print(s01[0])

print("##" * 20)
print(s01[-1])  # 但是当你设置了index，之后就可以拿到了，这是因为此时它拿的是index中的-1索引





# 位置索引
print("##" * 20)
print(s01[0])  # 索引

print("##" * 20)
print(s01[:2])  # 切片，开始到第二个 100 90 ,不包括第2个，切出来还是Series

print("##" * 20)
print(s01[[0, 1, 3]])  # 掩码，[0, 1, 3] 是一个掩码列表（回顾：掩码分为 '位置掩码' 和 '布尔掩码' ），切出来还是Series





# 标签索引
print("##" * 20)
print(s01['zs'])  # 索引

print("##" * 20)
print(s01[:'ls'])  # 切片，开始到'ls'即 100 90 ,（注意：包括结束的位置），切出来还是Series

print("##" * 20)
print(s01[['zs', 'ls', 'zl']])  # 掩码，['zs', 'ls', 'zl'] 是一个掩码列表（回顾：掩码分为 '位置掩码' 和 '布尔掩码' ），切出来还是Series


