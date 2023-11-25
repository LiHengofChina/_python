'''
Series示例
 Series 常用属性
'''



import numpy as np
import pandas as pd



s01 = pd.Series([100, 90, 80, 70], index=['zs', 'ls', 'ww', 'zl'])
print(s01.values)
print(type(s01.values))  #它是一个 ndarrsy
print(type(s01))
print(s01.index)
print(s01.dtype)
print(s01.size)
print(s01.ndim)
print(s01.shape)




##  不要最后一个元素
print("##" * 20)  # 直接切片
print(s01[[True, True, True, False]])  # 掩码操作
print(s01[[0, 1, 2]])  # 掩码操作
print(s01[['zs', 'ls', 'ww']])  # 掩码操作

print("##" * 20)#如果数据量非常大的时候，这样做
print(s01.index[:-1])                  # 对索引进行切片操作，
print(type(s01.index[:-1]))            # 对索引进行切片操作，切出来 的还是索引
print(s01[s01.index[:-1]])             # 再进行掩码操作



