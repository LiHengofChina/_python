
'''
数组的维度操作

//共享数据
视图变维 ravel，数组降成1维,拉伸

'''

import numpy as np


liheng = np.arange(5, 35).reshape(5, 6)
print(liheng)

print("==" * 20)
ary = liheng.ravel()
print(ary)
