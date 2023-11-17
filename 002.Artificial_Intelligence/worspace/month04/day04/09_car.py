'''

将car.txt中的字符串通过 "标签编码" 的形式转成数值类型

列说明：
（1列）零售价
（2列）维修费用
（3列）车门数
（4列）坐位数
（5列）后备箱空间的大小
（6列）安全系数
（7列）汽车的等级

查看数据，只转是字符串的列，
不是每一列都需要转。

'''
import pandas as pd
import sklearn.preprocessing as sp



#（1）加载数据
data = pd.read_csv('../data_test/car.txt',
                   sep=',',
                   header=None,
                   names=['a', 'b', 'c', 'd', 'e', 'f', 'g']
                   )
print(data.head())
print(data['c'].unique()) #通过 unique  "查看它的离散值"
print(data['d'].unique()) #通过 unique  "查看它的离散值"

print(data.dtypes) #查看 “每一列的数据类型”，这里都是字符串



#创建一个新的 DataFrame
df = pd.DataFrame()

#遍历每一列数据，单独进行标签编码
for col in data: # col 是列索引， DataFrame 遍历，col是列名
    lb_encoder = sp.LabelEncoder()  #为 “每一列数据”单独构建 "自己的标签编码器" ,data[col] 则拿到的是列数据。
    lb_samples = lb_encoder.fit_transform(data[col])  # 训练每一列数据
    df[col] = lb_samples #加入新的df

print(df)


