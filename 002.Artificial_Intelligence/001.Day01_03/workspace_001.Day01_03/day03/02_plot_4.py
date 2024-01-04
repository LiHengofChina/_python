
'''
    基本的绘图（两条线在一张图）
        正弦函数、余弦同时画
'''

import numpy as np
import matplotlib.pyplot as plt

#使用线性拆分
x = np.linspace(-np.pi, np.pi, 200)
sinx = np.sin(x)
cosx = np.cos(x)


plt.plot(x, sinx)  # 绘图
plt.plot(x, cosx)  # 绘图

plt.show()  # 显示图片，阻塞方法
