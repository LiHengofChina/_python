'''
dataframe 列级操作（增删改查）

查询数据

'''

import pandas as pd
#这是一个4行3列的数据，Series中最长的是4个元素，所以是4行
data = {'one': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        'two': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd']),
        'three': pd.Series([1, 3, 4], index=['a', 'c', 'd'])}

df = pd.DataFrame(data)
print(df)


# 拿到一列数据，
print("==" * 20)
print(df['one']) #直接索引列名，索引会降维，变成Series

# 拿到几行数据
#  注意： “列级索引” 没有 “位置索引”，而它的 0 1 2 实际 上也是 "标签"
#  “列级”  说的是维度方向，而 “位置” 指的是 [0] [1] [2] 这种，
#  而且，列级访问可以直接索引，但是不能切片
#  所以“拿几行数据”，只能掩码
print("==" * 20)
print(df[['one','two']]) #掩码操作（索引是一个列表或数组）

# 不要最后一列
print("==" * 20)
print(df[df.columns[:-1]])  # df.columns[:-1]  拿到最后一列，不要最后一个列名，然后再进行索引



