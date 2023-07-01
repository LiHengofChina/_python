'''
组合与拆分
'''

import numpy as np

x = np.arange(1,7).reshape(2,3)
y = np.arange(7,13).reshape(2,3)
print(x)
print(y)

########################################
#垂直方向--组合
print("==vstack" * 20)
z = np.vstack((x,y))
print(z)

#垂直方向--拆分
print("==vsplit" * 30)
x,y = np.vsplit(z,2)
print(x)
print(y)

########################################
#水平方向--组合
print("==hstack" * 30)
z = np.hstack((x,y))
print(z)

#水平方向--拆分
print("==hsplit" * 30)
x,y = np.hsplit(z,2)
print(x)
print(y)

########################################
#深度方向--组合
print("==dstack" * 30)
z = np.dstack((x,y))
print(z)
print(z.shape)



#深度方向--拆分
print("==dsplit" * 30)
x,y = np.dsplit(z,2)
# print(x)  # 这里需要注意一下
# print(y)  # 这里需要注意一下
print(x.reshape(2,3)) #这里需要注意一下
print(y.reshape(2,3)) #这里需要注意一下
