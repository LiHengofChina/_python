
'''
    基本的绘图：
        设置轴的显示范围
'''

import numpy as np
import matplotlib.pyplot as plt

#使用线性拆分
x = np.linspace(-np.pi, np.pi, 200)
sinx = np.sin(x)
cosx = np.cos(x)


plt.plot(x, sinx, linestyle='--',linewidth=3,color='blue',alpha=0.2)
plt.plot(x, cosx, linestyle='-.',linewidth=6,color='red',alpha=0.8)

# plt.xlim(0, np.pi) #设置x轴显示范围
# plt.ylim(-1, 1)     #设置y轴显示范围

plt.xlim(0, np.pi + 0.1) #设置x轴显示范围      + 0.1 防止贴边
plt.ylim(-1 , 1 + 0.1 )     #设置y轴显示范围   + 0.1 防止贴边


plt.show()  # 显示图片，阻塞方法


