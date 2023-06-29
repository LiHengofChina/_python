'''
数组的基本创建
'''
import numpy as np




print("==" * 20)
arr = np.zeros(10)  # 生成值全部是0的数组,dtype是指0的元素类型，默认是float64
print(arr)

print("==" * 20)
arr = np.zeros(10, dtype='int32')  # shape为10，所以是一个一维数组
print(arr)

print("==" * 20)
arr = np.zeros(shape=(3, 2), dtype='int32')  # 二维数组，3行2列，3表示二维数组中有几个一维数组，2表示一组数组中有几个元素
print(arr)  # 最左边有几个方括号，就代表是几维数据

print("==" * 20)
arr = np.zeros(shape=(5, 4, 9), dtype='int32')  # 三维数组，5表示三维数组中有几个二维数组，4表示二组数组中有一维数组，9表示一维数组中有几个元素
print(arr)      #三维数组，叫法，5页4行9列





print("==" * 20)
one = np.ones(shape=(3, 2), dtype='int32')
print(one) #生成值全是1的数组，和zero的区别就是值全是1
