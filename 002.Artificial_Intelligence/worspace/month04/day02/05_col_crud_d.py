'''
dataframe 列级操作（增删改查）

删除列数据
'''

import pandas as pd
#这是一个4行3列的数据，Series中最长的是4个元素，所以是4行    ，一般不设置index，这里设置是为了列举特殊的情况
data = {'one': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        'two': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd']),
        'three': pd.Series([1, 3, 4], index=['a', 'c', 'd'])}

df = pd.DataFrame(data)
print(df)

#删除一行数据：one
print("==" * 20)
del(df['one'])
print(df)

#调用pop方法删除一列,弹出并返回，
# 列表和字典都有pop方法
# 列表默认弹出最后最一个元素
# 字典里的pop，必须要给"键"
print("==" * 20)
col = df.pop('two')
print(df)
print(col)




#删除多列数据，df.drop，即可以删除行，又可以删除列
print("==" * 20)
data = {'one': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        'two': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd']),
        'three': pd.Series([1, 3, 4], index=['a', 'c', 'd'])}
df = pd.DataFrame(data)
print(df)
#删除多列
#注意axis的值，1表示水平，0表示垂直，但是我们要删除的是列，而列的排布是水平的，所以这里要写1，写0找不到就要报错。
#所以1指的是在水平方向找索引。找到的是列级索引，
#所以它指的是索引，而不是指数据。
#另外drop方法，默认不会修改原数据，inplace=Flase 不修改原数据
print("==" * 20)
# df = df.drop(['three', 'two'], axis=1, inplace=False)
# print(df)
#为True时，会删除原数据
df.drop(['three', 'two'], axis=1, inplace=True)
print(df)

