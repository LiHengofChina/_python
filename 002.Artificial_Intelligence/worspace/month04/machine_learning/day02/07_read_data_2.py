'''
读取数据 CSV
然后写到一个文件
'''

import pandas as pd
import os

data = pd.read_csv('../../data_test/aapl.csv',
                   sep=',',
                   header=None,
                   names=['name', 'date', '_', 'open', 'high', 'low', 'close', '__'],
                   index_col='date',
                   usecols=['date','open', 'high', 'low', 'close'])
print(data)


#写数据到一个文件
output_dir = 'tmp'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
data.to_csv('./tmp/new_data.csv')