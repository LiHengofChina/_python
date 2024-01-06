
import pandas as pd
import numpy as np

'''

协同过滤推荐==>基于内存==>ICF
    数据准备
     
    
'''

data = pd.read_csv('../data_test/movielens电影数据/ratings.dat',
                   sep='::',
                   engine='python',
                   header=None)
data = data.head(1000)
data.to_csv('../data_test/movielens电影数据/data.cvs',
            header=None,index=False)
print(data)

