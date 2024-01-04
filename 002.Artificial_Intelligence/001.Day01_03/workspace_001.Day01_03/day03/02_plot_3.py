'''
    基本的绘图
        1/2 余弦函数
'''

import numpy as np
import matplotlib.pyplot as plt

# 使用线性拆分
x = np.linspace(-np.pi, np.pi, 200)
y = np.cos(x) / 2
plt.plot(x, y)  # 绘图

plt.show()  # 显示图片，阻塞方法
