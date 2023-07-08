'''
 条形图，柱状图
'''

import matplotlib.pyplot as plt
import matplotlib.gridspec as mg

import numpy as np
import matplotlib.pyplot as plt


plt.figure('liheng', facecolor='lightgray')

# 1到12个月月份
x = np.arange(1, 13)

#苹果
# 随机产生，期望值是60，标准差为20，数量为12
apples = np.random.normal(60, 20, 12)

#橘子
# 随机产生，期望值是60，标准差为20，数量为12
oranges = np.random.normal(60, 20, 12)

#梨子
# 随机产生，期望值是60，标准差为20，数量为12
pear = np.random.normal(60, 20, 12)


# plt.bar(x, apples)
# plt.bar(x, oranges)

# -表示左移， + 表示右移， 0.1 是单个柱子的宽度
plt.bar(x - 0.2, apples, 0.1)
plt.bar(x, oranges, 0.1)
plt.bar(x + 0.2, pear, 0.1)

#在柱子上面定文字
for i in  x:
    plt.text(i - 0.2, apples[i - 1], int(apples[i - 1]), fontsize=8, ha='center', va='bottom')
    plt.text(i, oranges[i - 1], int(oranges[i - 1]), fontsize=8, ha='center', va='bottom')
    plt.text(i + 0.2, pear[i - 1], int(pear[i - 1]), fontsize=8, ha='center', va='bottom')






# 紧凑式布局
plt.tight_layout()

plt.show()
