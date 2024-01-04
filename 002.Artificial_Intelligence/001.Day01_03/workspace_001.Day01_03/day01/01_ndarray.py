'''
数组的基本创建
'''
import numpy as np


lis = [1, 2, 3, 4, 5, 6]
ary = np.array(lis)  # 将列表转成数组
print(ary)  # [1 2 3 4 5 6],看起来像列表，其实它是数组，这就导致它很多计算方式也不相同
print(type(ary))  # 查看它的数据类型 'numpy.ndarray'，
print(type(lis))  # 查看它的数据类型


# print("==" * 20)
# print(lis * 2)  # 将列表中的元素重复生成两次
# print(ary * 2)  # 每个元素*2



# print("==" * 20)
# print(lis == 3) #比较列表，通常返回False，两个不同的类型进行比较
# print(ary == 3) #每个元素进行比较



# print("==" * 20)
# print(lis + lis) #两个列表拼在一起
# print(ary + ary) #对应位置进行相加



# print("==" * 20)
# print(lis * lis) #两个列表不能相乘
# print(ary * ary) #对应位置相乘
#


