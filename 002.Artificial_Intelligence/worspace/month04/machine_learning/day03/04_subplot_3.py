'''
 子图:
        练习，在每个子图里面写上自己的编号
'''

import matplotlib.pyplot as plt

#
plt.figure('liheng',
           facecolor='lightgray' )

# （1）3行3列，第1个位置
for i in range(1, 10):
    plt.subplot(3, 3, i)
    plt.text(0.5, 0.5, i, fontsize=35, ha='center', va='center')
    plt.xticks([])
    plt.yticks([])

#紧凑式布局
plt.tight_layout()

plt.show()
