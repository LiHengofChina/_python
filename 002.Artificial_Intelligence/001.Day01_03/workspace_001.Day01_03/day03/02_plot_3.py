
'''
基本绘图
1/2 余弦函数
'''

import matplotlib
matplotlib.use("TkAgg")   # 解决 PyCharm 后端问题

import numpy as np
import matplotlib.pyplot as plt

# 生成数据
x = np.linspace(-np.pi, np.pi, 200)
y = np.cos(x) / 2

# 创建图像
plt.figure()

# 绘制曲线
plt.plot(x, y, label="y = cos(x) / 2")

# 添加标题和坐标标签
plt.title("Half Cosine Function")
plt.xlabel("x")
plt.ylabel("y")

# 添加网格和图例
plt.grid(True)
plt.legend()

# 显示图像
plt.show()