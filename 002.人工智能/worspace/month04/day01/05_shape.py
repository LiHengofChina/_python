
'''
数组的维度操作

//共享数据
视图变维 reshape


'''

import numpy as np

ary = np.arange(1, 19)


print("==" * 20)

#变维之后
bry = ary.reshape(2, 9)
print(ary)  #原来的不变
print(bry)  #新的变2维

#修改元素
print("==" * 20)
ary[0] = 666  #修改ary的元素
print(bry)    #bry的也会跟着改变

#reshape结合 arange的使用场景
print("==" * 20)
liheng = np.arange(5, 35).reshape(5, 6)
print(liheng)
