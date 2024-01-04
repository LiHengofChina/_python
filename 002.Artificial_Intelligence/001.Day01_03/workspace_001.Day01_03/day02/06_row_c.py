'''
行级操作
    添加
'''
import pandas as pd

df1 = pd.DataFrame([['Tom', 18],
                    ['Jerry', 18]],
                   columns=['Name', 'Age'])
df2 = pd.DataFrame([['Jack', 20],
                    ['Rose', 20]],
                   columns=['Name', 'Age'])

# 增加 concat
print("==" * 20)
df3 = pd.concat([df1, df2], axis=1)  # 列索引是横向的，所以1是从右边连接
df3.columns = ['a', 'b', 'c', 'd']   # 重新指定列级索引
print(df3)

print("==" * 20)
df3 = pd.concat([df1, df2],axis=0)  #行索引是垂直的的，所以0是从下面边连接
df3.index = [0, 1, 2, 3]            #重新指定行级索引
print(df3)



