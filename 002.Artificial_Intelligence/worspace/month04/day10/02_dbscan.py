
'''
聚类问题：
        噪声密度
'''
import pandas as pd
import sklearn.cluster as sc #聚类模块
import matplotlib.pyplot as mpl
import numpy as np

#加载数据
data = pd.read_csv(
        '../data_test/perf.txt',
        header=None,
        names=['x1','x2'] )
# print(data)

eps = 0.8 #邻域半径
min_samples = 5 #最少样本数量

model =  sc.DBSCAN(eps=eps,
                   min_samples=min_samples)
model.fit(data) #执行聚类

 # 获取聚类标签（聚类结果）
pred_y = model.labels_
# print(pred_y)
# print(model.core_sample_indices_) # 打印所有核心样本索引



# 核心样本
core_mask = np.zeros(len(data), dtype=bool)
core_mask[model.core_sample_indices_] = True  # 核心样本下标
# print(core_mask)
# （噪声）孤立样本
offset_mask = (pred_y == -1)
# print(offset_mask)
# 边界点：核心样本、孤立样本之外的样本
periphery_mask = ~(core_mask | offset_mask)
# print(periphery_mask)





# 可视化
mpl.figure('DBSCAN Cluster', facecolor='lightgray')
mpl.title('DBSCAN Cluster', fontsize=20)
mpl.xlabel('x1', fontsize=14)
mpl.ylabel('x2', fontsize=14)
mpl.tick_params(labelsize=14)
mpl.grid(linestyle=':')
labels = set(pred_y)
print(labels)
cs = mpl.get_cmap('brg', len(labels))(range(len(labels)))
print("cs:", cs)


# 核心点
mpl.scatter(data[core_mask].values[:, 0],
            data[core_mask].values[:, 1],
            c=cs[pred_y[core_mask]],
            s=80, label='Core')

# 边界点
mpl.scatter(data[periphery_mask].values[:, 0],
           data[periphery_mask].values[:, 1],
           edgecolor=cs[pred_y[periphery_mask]],
           facecolor='none', s=80, label='Periphery')
# 噪声点
mpl.scatter(data[offset_mask].values[:, 0],
           data[offset_mask].values[:, 1],
           marker='D', c=cs[pred_y[offset_mask]],
           s=80, label='Offset')

mpl.legend()
mpl.show()