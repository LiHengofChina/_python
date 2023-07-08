'''
直方图
'''

import numpy as np
import matplotlib.pyplot as plt

#生成正太分布的身高数据
# height = np.random.normal(175, 10, 1000)
height = np.random.normal(175, 10, 100000) # （数据越多规律越明显）

plt.hist(height,bins=100)

plt.show()

