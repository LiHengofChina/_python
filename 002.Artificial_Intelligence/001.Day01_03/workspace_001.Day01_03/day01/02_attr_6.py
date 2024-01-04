
'''
ndarray 的基本属性
数据类型
'''

import numpy as np


#字符串类型
print("==" * 20)
ary = np.array(['zcm',  # 12 Bytes
                'qwer',  # 16 Bytes
                'zbcdefghi'  # 36 Bytes
                ])
                #由于np里面的数组是同质数组，所以数组中的每个元素要以最多的长度为准，也就是每个元素都是36 Bytes
                #这里浪费空间，所以这里就是典型的  “拿空间” 换 “时间”，
                #类似字典，底层以Hash存储

print(ary.dtype) #U9表示它有9个字符，U10表示它有10个字符，每个字符占4字节
                 #<U9    < 小于号表示小端字节序，计算机底保存数据的一种方式


