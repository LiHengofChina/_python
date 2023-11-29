
'''
聚类问题：
        k-均值聚类
'''

import pandas as pd
import sklearn.cluster as sc #聚类模块
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#加载数据
data = pd.read_csv(
        '../data_test/multiple3.txt',
        header=None,
        names=['x1','x2'] )

#构建模型
model = KMeans(n_clusters=4)
model.fit(data)


 # 获取聚类(几何)中心
centers = model.cluster_centers_
print(centers)
 # 获取聚类标签（聚类结果）
pred_y = model.labels_
print(pred_y)

plt.scatter(data['x1'], data['x2'], c=model.labels_)

#画出几何中心
plt.scatter(centers[:,0], centers[:,-1],color='black',marker='+',s=300)

#预测
print(model.predict([[1.1, 2.2]]))


plt.colorbar()
plt.show()


