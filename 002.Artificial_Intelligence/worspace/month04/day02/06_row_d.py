'''
行级操作
    删除
'''
import pandas as pd

df = pd.DataFrame([['Tom', 18],
                   ['Jerry', 18],
                   ['Jack', 20],
                   ['Rose', 20]], columns=['Name', 'Age'])
print(df)


#删除 1 2行，
print("==" * 20)
# df = df.drop([0, 1], axis=0)
df.drop([0, 1], inplace=True, axis=0) # 默认axis=0，垂直轴向，
print(df)


#删除Age列
print("==" * 20)
df = df.drop(['Age'],axis=1)  # 操作列时，只有标签索引，没有位置索引
print(df)
