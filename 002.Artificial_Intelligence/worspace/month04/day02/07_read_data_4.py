'''
读取数据 Json 和 输出Json

'''

import pandas as pd

###################################################输出JSON
#读取json
data = pd.read_json('../data_test/ratings.json',orient='records')
print(data)

print("==" * 20)
data = pd.read_json('../data_test/ratings.json',orient='index')
print(data)

print("==" * 20)
data = pd.read_json('../data_test/ratings.json',orient='columns')
print(data)

print("==" * 20)
data = pd.read_json('../data_test/ratings.json',orient='values')
print(data)

#通过orient控制，怎么将键值对转成DataFrame
#有以下四种值：records    index   coloums     values

###################################################输出JSON 字符串，在没有指定文件路径时，输出字符串
print("==" * 20)
df = pd.DataFrame({'Name': ['zs', 'ls', 'ww', 'sl'],
                   'Age': [18, 19, 20, 21]}
                  )
print(df)

print("==" * 20)
print(df.to_json(orient='records'))

print("==" * 20)
print(df.to_json(orient='index'))

print("==" * 20)
print(df.to_json(orient='columns'))

print("==" * 20) #值的方式，没有索引
print(df.to_json(orient='values'))


