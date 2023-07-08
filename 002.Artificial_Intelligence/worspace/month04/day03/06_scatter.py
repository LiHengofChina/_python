'''
scatter
'''

import numpy as np
import matplotlib.pyplot as plt

n = 2000

#颜色期望值为172，标准差为10 数据
height = np.random.normal(172, 10, n)   #身高
#颜色期望值为60，标准差为10 数据
weight = np.random.normal(60, 10, n)    #体重


plt.scatter(height, weight,
            # color=height,
            c=height, #以height列表作为颜色
            # cmap='cool', #显示颜色映射
            cmap='jet' #显示颜色映射
            )
            #让身高根据数据产生变化
plt.colorbar()


plt.show()
