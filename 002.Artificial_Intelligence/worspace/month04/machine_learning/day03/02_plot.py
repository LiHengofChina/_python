'''
    基本的绘图
        直接图、拆线、线段
'''

import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 3, 5, 7, 9])  # 一系统的x点
y = np.array([10, 5, 11, 7, 20])  # 一系列的y点
plt.plot(x, y)  # 绘图

plt.show()  # 显示图片，阻塞方法



