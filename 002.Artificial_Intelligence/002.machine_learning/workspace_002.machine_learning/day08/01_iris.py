'''

分类问题：
        鸢尾花分类

		鸢尾花：4个特征
			花瓣的长度
			花瓣的宽度
			萼片的长度
			萼片的宽度

        --观察原始数据
'''

import sklearn.datasets as sd #数据集合

iris = sd.load_iris()
print(iris.keys())
print(iris.DESCR) # 4个特征 150 个样本 3个类别
print(iris.feature_names)
print(iris.target_names)
print(iris.data)
print(iris.data.shape)
print(iris.target)


