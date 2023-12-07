'''
 子图:
        矩阵式布局
'''

import matplotlib.pyplot as plt

#在默认的窗口中

#（1）3行3列，第5个位置
plt.subplot(3, 3, 5)
# 第一条线
plt.plot([1, 2, 3], [1, 2, 3])
# 第三条线
plt.plot([1, 2, 3], [3, 2, 1])


#（1）3行3列，第1个位置
plt.subplot(3, 3, 1)
# 第一条线
plt.plot([1, 2, 3], [1, 2, 3])
# 第二条线
plt.plot([1, 2, 3], [3, 2, 1])

plt.show()


