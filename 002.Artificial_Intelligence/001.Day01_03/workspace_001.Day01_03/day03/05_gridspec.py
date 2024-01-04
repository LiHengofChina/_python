'''
 子图:
    网格式布局
'''

import matplotlib.pyplot as plt
import matplotlib.gridspec as mg

#
plt.figure('liheng', facecolor='lightgray')


# 创建网格布局
# gs = mg.GridSpec(3, 3)   # mg 和 plt 都可以
gs = plt.GridSpec(3, 3)    #3行3列

#拿到子图 # 将  “0行” 与 “0列和1列” 合并
plt.subplot(gs[0, :2])
plt.text(0.5, 0.5, 'python_base', ha='center', va='center', size=20)
plt.xticks([])
plt.yticks([])

#拿到子图 # 将  “0行和1行” 与 “2列” 合并
# plt.subplot(gs[:2, 2])
plt.subplot(gs[:2, -1])
plt.text(0.5, 0.5, 'Socket', ha='center', va='center', size=20)
plt.xticks([])
plt.yticks([])

#拿到子图 # 将  “2行” 与 “1列和2列” 合并
plt.subplot(gs[2, 1:3])
plt.text(0.5, 0.5, 'DadaShop', ha='center', va='center', size=20)
plt.xticks([])
plt.yticks([])

#拿到子图 # 将  “1行2行” 与 “0列“  合并
plt.subplot(gs[1:3, 0])
plt.text(0.5, 0.5, 'AI', ha='center', va='center', size=20)
plt.xticks([])
plt.yticks([])



#拿到子图
# plt.subplot(3,3,5)
plt.subplot(gs[1, 1])
plt.text(0.5, 0.5, 'AID2303', ha='center', va='center', size=25
         ,rotation=-35)#旋转字体
plt.xticks([])
plt.yticks([])

# 紧凑式布局
plt.tight_layout()


plt.show()

