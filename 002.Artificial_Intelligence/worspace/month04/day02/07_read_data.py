'''
读取数据 CSV
'''



import pandas as pd

data = pd.read_csv('../data_test/aapl.csv',
                   sep=',',
                   header=None,
                   names=['name', 'date', '_', 'open', 'high', 'low', 'close', '__'],
                   index_col='date',
                   usecols=['date','open', 'high', 'low', 'close'])
print(data)

print("====" * 20)

data = pd.read_csv('../data_test/保健品问卷数据/保健品字段介绍.csv',
                   header=None,
                   encoding='gbk'
                   )
print(data)