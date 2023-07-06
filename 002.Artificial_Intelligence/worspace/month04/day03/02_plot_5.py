
'''
    基本的绘图：
        设置线条样式
'''

import numpy as np
import matplotlib.pyplot as plt

#使用线性拆分
x = np.linspace(-np.pi, np.pi, 200)
sinx = np.sin(x)
cosx = np.cos(x)


plt.plot(x, sinx, linestyle='--',linewidth=3,color='blue',alpha=0.2)
plt.plot(x, cosx, linestyle='-.',linewidth=6,color='red',alpha=0.8)

plt.show()  # 显示图片，阻塞方法
