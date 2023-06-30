
'''
ndarray 的基本属性
查看元素个数 和  数组长度
'''

import numpy as np

print("==" * 20)
ary = np.arange(1, 10)
print(ary)
print(ary.size)  # 9 ，打印元素个数
print(len(ary))  # 9 , len是查看长度


print("==" * 20)
ary.shape = (3, 3) #修改形状之后，再次打印元素个数，还是为9，所以size不管是几维，它都查看的是所有的它有几个元素
print(ary)
print(ary.size)
print(len(ary))  # 3 , 长度是查看二维数组中有几个一维数组，如果是三维数组，则查看的是三维数组中有几个二维数组
