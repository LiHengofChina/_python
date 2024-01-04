'''
行级操作
    修改
'''
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

df = pd.DataFrame([['Tom', 18],
                   ['Jerry', 18],
                   ['Jack', 20],
                   ['Rose', 20]], columns=['Name', 'Age'])
print(df)

# 修改某一个元素
print("==" * 20)
df.loc[2,'Age'] = 34
df.loc[2,'Name'] = 'liheng'
print(df)

# 修改某一个元素
print("==" * 20)
df.loc[2,'Age'] = 22
df.loc[2,'Name'] = 'liheng'
print(df)

##############################################不建设
# 通过列找行
print("==" * 20)
df['Age'][1] = 313        #通过列索引，拿到一列， 这种方式会产生警告
print(df)

# 也可以通过行找列
print("==" * 20)
df.iloc[1]['Age'] = 44
            #修改不成功，因为pandas底层编写时，通过列找元素有赋值的过程
            #通过行找这个元素时，底层没有赋值过程，你就修改不了
            #列操作时也有提示，不建议这样做，
print(df)

