'''
行级操作
    查询
'''
import pandas as pd

data = {'one': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        'two': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd']),
        'three': pd.Series([1, 3, 4], index=['a', 'c', 'd'])}

df = pd.DataFrame(data)
print(df)

# 访问行级数据，访问行，可以切片，但不能直接索引
print("==" * 20)
print(df[:1])  # 切片访问，切出来还是DataFrame，（不包括1）
# 对于行级，即有标签索引，又有列级索引



# 通过loc使用索引访问一行
print("==" * 20)
print(df.loc['a'])  # 索引


# 通过loc使用切片访问一行
print("==" * 20)
print(df.loc[:'a'])  # 切片，切出来还是切片，（包括a）

# 通过loc使用切片访问三行
print("==" * 20)
print(df.loc['a':'c'])  # 切片，切出来还是切片，（包括c）


# 通过loc使用掩码访问一行
print("==" * 20)
print(df.loc[['a']])

# 通过loc使用掩码访问三行
print("==" * 20)
print(df.loc[['a', 'b', 'c']])



# 访问前两行的前两列
print("==" * 20)
print(df.loc['a':'b', 'one':'two'])



##############################################

# 通过loc使用索引访问一行
print("==" * 30)
print(df.iloc[0])  # 索引


# 通过loc使用切片访问一行
print("==" * 30)
print(df.iloc[:1])  # 切片，切出来还是切片，（不包括1）

# 通过loc使用切片访问三行
print("==" * 30)
print(df.iloc[0:3])  # 切片，切出来还是切片，（不包括3）


# 通过loc使用掩码访问一行
print("==" * 30)
print(df.iloc[[0]])

# 通过loc使用掩码访问三行
print("==" * 30)
print(df.iloc[[0, 1, 2]])



# 访问前两行的前两列
print("==" * 30)
print(df.iloc[:2, 0:2])
