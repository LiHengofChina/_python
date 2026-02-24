'''
    基本的绘图
        直接图、拆线、线段
'''




import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 3, 5, 7, 9])
y = np.array([10, 5, 11, 7, 20])

plt.plot(x, y)
plt.show()
