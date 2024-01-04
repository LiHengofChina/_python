
'''
    基本的绘图：
            LaTex表达式
'''

import numpy as np
import matplotlib.pyplot as plt

#使用线性拆分
x = np.linspace(-np.pi, np.pi, 200)
sinx = np.sin(x)
cosx = np.cos(x)


plt.plot(x, sinx, linestyle='--',linewidth=3,color='blue',alpha=0.2)
plt.plot(x, cosx, linestyle='-.',linewidth=6,color='red',alpha=0.8)


# 设置刻度
plt.xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]
           , [r'$-\pi$', r'$-\frac{\pi}{2}$',
              '0',
              r'$\frac{\pi}{2}$', r'$-\pi$']
           , fontsize=25
           )
plt.yticks([-1, -1 / 2, 0, 1 / 2, 1]
           , ['-1', r'$-\frac{1}{2}$',
              '0',
              r'$\frac{1}{2}$', '1']
           , fontsize=25
           )


plt.show()  # 显示图片，阻塞方法


