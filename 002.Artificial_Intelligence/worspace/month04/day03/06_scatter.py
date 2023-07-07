'''
scatter
'''

import numpy as np
import matplotlib.pyplot as plt

n = 2000

height = np.random.normal(172, 10, n)   #身高
weight = np.random.normal(60, 10, n)    #体重


plt.scatter(height, weight,
            # color=height,
            c=height,
            cmap='cool'
            )
            #让身高根据数据产生变化
plt.colorbar()


plt.show()
