'''
Series示例
'''


import numpy as np
import pandas as pd

data = [100,90,88,27]



print("==" * 20 )
s01 = pd.Series(data) # 列表转 Series
print(s01)  #打印出来是一个一维数组，左边是一个索引，右边是值



print("==" * 20 )
s02 = pd.Series(data, index=['zs','ls','ww','sl']) # 列表转 Series，同时指定索引
print(s02)  #打印出来是一个一维数据，左边是一个索引，右边是值



#从字典创建一个Series
print("==" * 20 )
data = {'100' : '张三', '101' : '李四','102' : '王五'}
s03 = pd.Series(data)
print(s03)



# 从标量创建一个Series
print("==" * 20 )
s04 = pd.Series(0.2, index=[0, 1, 2, 3])  #在numpy里面利用广播机器，创建全是0.2的数组，这里使用标题达到一样的效果。
print(s04)
print("==" * 20 )
s05 = pd.Series(0.2, index=np.arange(10))  #在numpy里面利用广播机器，创建全是0.2的数组，这里使用标题达到一样的效果。
print(s05)



# 从np数组创建一个Series
print("==" * 20 )
ary = np.zeros(10) + 0.2
s06 = pd.Series(ary)
print(s06)


