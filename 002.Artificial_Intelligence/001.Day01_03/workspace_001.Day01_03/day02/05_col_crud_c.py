'''
dataframe 列级操作（增删改查）

添加列
'''

import pandas as pd
#这是一个4行3列的数据，Series中最长的是4个元素，所以是4行    ，一般不设置index，这里设置是为了列举特殊的情况
data = {'one': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        'two': pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd']),
        'three': pd.Series([1, 3, 4], index=['a', 'c', 'd'])}

df = pd.DataFrame(data)
print(df)

#增加一列数据，和字典添加键值对是一样的     df[列名]  =列值
#注意：值为列表时，列表长度要和index一致
print("==" * 20)
df['four'] = [100, 200, 300, 400]
print(df)

#增加一列数据，值为Series，为Series时，series的index要与dataframe的index一致
print("==" * 20)
df['five'] = pd.Series([666, 888, 999], index=['a', 'b', 'd'])
print(df)