
import pandas as pd
import numpy as np

'''
    ICF ，数据量太大， 取1000行放在一小文件中。
'''

data = pd.read_csv('../../data_test/movielens电影数据/ratings.dat',
                   sep='::',
                   engine='python',
                   header=None)
data = data.head(1000)
data.to_csv('../../data_test/movielens电影数据/data.cvs',
            header=None,index=False)
print(data)

