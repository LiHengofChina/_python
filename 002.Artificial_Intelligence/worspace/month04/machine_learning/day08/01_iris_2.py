'''

分类问题： 鸢尾花分类

分析：
        //=================================(1)第一步
        # print(iris.data)
                把数据x直接转成 DataFrame
        # print(iris.target)
                然后把y值直接添加到最后一列。
        //=================================(2)第二步
        以萼片长度作为x，以萼片宽度作为y画出散点图。


'''

import sklearn.datasets as sd #数据集合
import pandas as pd
import matplotlib.pyplot as plt

#（1）加载数据
iris = sd.load_iris()

#（2）转成 DataFrame
data = pd.DataFrame(iris.data,
                    columns=iris.feature_names)
data['target'] = iris.target
print(data)


#（3）萼片 可视化
plt.subplot(2,1,1)
plt.scatter(data['sepal length (cm)'],   #X
            data['sepal width (cm)'],    #Y
            c=data['target'],            #让 “类别不同” 就 "颜色就不同"
            cmap='brg',
            )

plt.colorbar()  #颜色条


#（3）花瓣 可视化
plt.subplot(2,1,2)
plt.scatter(data['petal length (cm)'],   #X
            data['petal width (cm)'],    #Y
            c=data['target'],            #让 “类别不同” 就 "颜色就不同"
            cmap='brg',
            )
plt.colorbar()  #颜色条

plt.show()

#结论： 0 类别很容易区分，而 1 和 2类型稍微有点重合




