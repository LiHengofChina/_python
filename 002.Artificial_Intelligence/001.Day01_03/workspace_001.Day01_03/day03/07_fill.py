'''
填充图
'''

import numpy as np
import matplotlib.pyplot as plt

n = 1000
x = np.linspace(0, 8 * np.pi, n)  # 返回指定间隔的等距数字
sin_y = np.sin(x)  # 计算sin函数值
cos_y = np.cos(x / 2) / 2  # 计算cos函数


#画出两条线
plt.plot(x, sin_y, c='dodgerblue', label=r'$y=sin(x)$')
plt.plot(x, cos_y, c='orangered', label=r'$\frac{1}{2}cos(\frac{x}{2})$')


# 填充 cos_y < sin_y 的部分
plt.fill_between(x,
                 cos_y,
                 sin_y,
                 cos_y < sin_y,
                 color='dodgerblue',
                 alpha=0.5
                 )
# 填充 cos_y > sin_y 的部分
plt.fill_between(x,
                 cos_y,
                 sin_y,
                 cos_y > sin_y,
                 color='orangered',
                 alpha=0.5
                 )

plt.legend(loc=0)
plt.show()


