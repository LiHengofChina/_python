
'''
    基本的绘图：
            特殊点
'''

import numpy as np
import matplotlib.pyplot as plt

#使用线性拆分
x = np.linspace(-np.pi, np.pi, 200)
sinx = np.sin(x)
cosx = np.cos(x)

plt.plot(x, sinx, linestyle='--', linewidth=3, color='green', alpha=0.2,
         label=r'$y=sin(x)$')
plt.plot(x, cosx, linestyle='-.', linewidth=3, color='red', alpha=0.8,
         label=r'$y=\frac{1}{2}cos(x)$')


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


ax = plt.gca()

# 上 和 右 设置为没有颜色
top = ax.spines['top'].set_color('none')
right = ax.spines['right'].set_color('none')

#移动 左 和 下 的位置
left = ax.spines['left'].set_position(('data',0))
bottom = ax.spines['bottom'].set_position(('data',0))



#（因为移动了位置）重新设置一下字体大小
plt.xticks(fontsize=14)
# 去掉y轴的0，两边重合了
plt.yticks([-1, -1 / 2, 1 / 2, 1])

# plt.legend()
plt.legend(loc=0)

#特殊的点
plt.scatter([0, np.pi / 2, -np.pi / 2],
            [0, 1, -1],
            marker='*',
            s=300,
            edgecolor='green',
            facecolor='red',
            zorder=3
            )


plt.show()  # 显示图片，阻塞方法




