'''

聚类：
    凝聚层次
    ----------
    使用 ”轮廓系数“ 打分，

'''

import pandas as pd
import sklearn.cluster as sc #聚类模块
import matplotlib.pyplot as mpl
import numpy as np
import sklearn.metrics as sm #评估模块

#加载数据
data = pd.read_csv(
    '../data_test/perf.txt',
        header=None,
        names=['x1','x2'] )
# print(data)


model =  sc.AgglomerativeClustering(n_clusters=5)
model.fit(data) #执行聚类

 # 获取聚类标签（聚类结果）
pred_y = model.labels_
# print(pred_y)
# print(model.core_sample_indices_) # 打印所有核心样本索引


#使用 ”轮廓系数“ 打分
score = sm.silhouette_score(data, # 样本
                            pred_y, # 标签
                            sample_size=len(data), # 样本数量
                            metric="euclidean")  # 欧式距离度量
print(score)



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


mpl.scatter(data.values[:, 0], data.values[:, 1],
            s=80, c=pred_y,
            cmap="brg")

mpl.show()

