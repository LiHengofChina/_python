'''
DataFrame 示例
        常用属性
'''
import pandas as pd

#通过字典创建
print("##" * 20)
# data = {'Name': ['Tom', 'Jerry', 'Jack', 'Rose'],   # 为列表时，列表长度必须相同
#         'Age': [18, 18, 20, 20]}                    # 为列表时，列表长度必须相同

data = {'Name': pd.Series(['Tom', 'Jerry', 'Jack', 'Rose'], index=['a', 'b', 'c', 'd']),
        'Age': pd.Series([18, 18, 20], index=['a', 'b', 'd'])}  # 通过索引来调整
df = pd.DataFrame(data)
print(df)

print("##" * 20)
print(df.axes)
print(df.index)         #行索引
# print(type(df.index))         #行索引
print(df.columns)             #列索引
# print(type(df.columns))       #


print("==" * 30)
print(df.dtypes)             #
print(type(df.dtypes))       #返回Series


print("==" * 30)
print(df.empty)

print("==" * 30)
print(df.ndim)
print(df.shape)

print("==" * 30)
print(df.size)

print("==" * 30)
print(df.values)

print("==" * 30)
print(df.head(2))

print("==" * 30)
print(df.tail(2))