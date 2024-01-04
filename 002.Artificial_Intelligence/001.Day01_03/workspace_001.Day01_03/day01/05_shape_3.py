
'''
数组的维度操作

//数据独立
复制变维 flatten，数组降成1维,拉伸，但数据独立

'''

import numpy as np


liheng = np.arange(5, 35).reshape(5, 6)

print(liheng)

ary = liheng.flatten()

print("==" * 20)
liheng[0][0] = 200
print(liheng)
print("==" * 20)
print(ary)
