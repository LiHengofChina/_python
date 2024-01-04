'''


multlpte2.txt  ， 一个二分类的问题


支持 "向量机"
        -使用散点图，查看数据分布

'''

import pandas as pd
import matplotlib.pyplot as plt


#（1）加载数据
data = pd.read_csv('../../data_test/multiple2.txt',
                   header=None,
                   names=['x1','x2','y'])
print(data.head())



#（2）打印一下看看是不是 “线性可分”
plt.scatter(data['x1'],
            data['x2'],
            c=data['y'],
            cmap='brg'
            )
            #它是一个x1和一个x2对应一个类别
            #所以用 (x1,x2) 来表示一个点，
            #然后用颜色来区别它们的类型
            #就是说：x1 x2 ==> y 这是这它的三个属性，都在图中表示出来

plt.colorbar()
plt.show()


