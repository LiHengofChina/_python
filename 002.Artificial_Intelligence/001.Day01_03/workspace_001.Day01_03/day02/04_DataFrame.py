'''
DataFrame 示例
'''
import pandas as pd

# 从(一维列表)创建DataFrame
data = [1,2,3,4,5,]  #一维列表，里面有5元素，每个元素是一个样本，
df = pd.DataFrame(data) #所以转换之后变成5行一列的DataFrame
print(df)
print(df.shape)


# 从(二维列表)创建DataFrame
print("##" * 20)
data = [['Alex',10],
        ['Bob',12],
        ['Clarke',13]] #二维列表
df = pd.DataFrame(data,columns=['Name','Age'])
print(df)
print(df.shape)


# 创建时指定索引
print("##" * 20)
data = [['Alex',10],
        ['Bob',12],
        ['Clarke',13]] #二维列表
df = pd.DataFrame(data,
                  index= ['s01','s02','s03'], #指定行级索引
                  columns = ['Name','Age'])   #指定列级索引
print(df)
print(df.shape)

