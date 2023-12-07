
'''
    基本的绘图
        正弦函数
'''

import numpy as np
import matplotlib.pyplot as plt

#使用线性拆分
x = np.linspace(-np.pi, np.pi, 200)
y = np.sin(x)                        # 对边与斜边的比值
                                     # np.sin 是一个矢量化的方法，
                                     # 参数x是一个数组，那么np.sin会求每一个值的sin值是多少。

plt.plot(x, y)  # 绘图

plt.show()  # 显示图片，阻塞方法
