'''

将car.txt中的字符串通过 "标签编码" 的形式转成数值类型

'''
import pandas as pd
import sklearn.preprocessing as sp

data = pd.read_csv('../data_test/car.txt',
                   sep=',',
                   names=['a', 'b', 'c', 'd', 'e', 'f', 'g']
                   )

# print(data['a'].unique()) # unique 其实是查看它的离散值
# print(data['c'].unique())
# print(data.dtypes) #查看每一列的数据类型，这里都是字符串



#创建一个新的 DataFrame
df = pd.DataFrame()

for col in data: # col 是列索引
    lb_encoder = sp.LabelEncoder()  #为每一列数据单独构建自己的标签编码器
    lb_samples = lb_encoder.fit_transform(data[col])  # 训练每一列数据
    df[col] = lb_samples #加入新的df

print(df)


