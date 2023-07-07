'''
 子图:
        矩阵式布局：添加文字
'''

import matplotlib.pyplot as plt

# 在默认的窗口中

# （1）3行3列，第5个位置
plt.subplot(3, 3, 5)
plt.text(0.5, 0.5, 5, fontsize=24, ha='center', va='center')
#去掉刻度显示
plt.xticks([])
plt.yticks([])

# （1）3行3列，第1个位置
plt.subplot(3, 3, 1)
plt.text(0.5, 0.5, 1, fontsize=24, ha='center', va='center')
#去掉刻度显示
plt.xticks([])
plt.yticks([])

#让文件对齐
# ha:left,center,right   #水平控制
# va:top,center,bottom   #垂直控制



#紧凑式布局
plt.tight_layout()

plt.show()
