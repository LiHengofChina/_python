import numpy as np

ary = np.arange(1, 51).reshape(10, 5)

print(ary)
print("==" * 20)

# 拿到所有行，不要最后一列（要求二维）
print(ary[0:10, 0:4])
print(ary[:, 0:-1])
print("==" * 20)

# 拿到所有行，只要最后一列（要求一维）
print(ary[0:10, 4:].T[0])  # .T 列转行，再拿第一个元素 #这是一种解决方法
print(ary[:, -1]) #反向索引

