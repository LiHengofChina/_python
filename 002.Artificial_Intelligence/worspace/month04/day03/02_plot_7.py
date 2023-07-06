
'''
    基本的绘图：
            设置刻度
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
           ,['-π','-π/2','0','π/2','π'] #x文本（可 选）
           )
plt.yticks([-1, -1 / 2, 0, 1 / 2, 1]
           ,['-1','-1/2','0','1/2','1'] #y文本（可 选）
           )


plt.show()  # 显示图片，阻塞方法


