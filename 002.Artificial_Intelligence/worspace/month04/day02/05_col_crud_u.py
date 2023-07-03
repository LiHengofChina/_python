'''
dataframe 列级操作（增删改查）

修改数据
'''

import pandas as pd
#这是一个4行3列的数据，Series中最长的是4个元素，所以是4行    ，一般不设置index，这里设置是为了列举特殊的情况
data = {'one': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        'two': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd']),
        'three': pd.Series([1, 3, 4], index=['a', 'c', 'd'])}

df = pd.DataFrame(data)
print(df)

#修改一行数据
#最常用的修改方式：
#              通过一个掩码操作取出来，直接进行赋值就可以了

#修改前两列值为100
print("==" * 20)
df[df.columns[:-1]] = 100
print(df)

# 修改第一列为:5 6 7 8
print("==" * 20)
df[df.columns[0]] = pd.Series([5, 6, 7, 8], index=['a', 'b', 'c', 'd'])
print(df)



