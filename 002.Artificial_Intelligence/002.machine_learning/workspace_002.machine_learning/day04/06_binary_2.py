'''
二值化
    设定一个阈值，
        用1表示该元素大于阈值，
        用0表示该元素小于等于阈值

        使用 sklearn 框架里面的接口来实现
'''

import numpy as np
import sklearn.preprocessing as sp
raw_sample = np.array([[66.6,59.9,22.3],
                       [99.9,18.8,88.8],
                       [12.3,34.5,78.9]])


bin = sp.Binarizer(threshold=59.9)  # 创建 "二值化对象"（注意边界值）
# threshold是域值
bin_samples = bin.transform(raw_sample)

print(bin_samples)



