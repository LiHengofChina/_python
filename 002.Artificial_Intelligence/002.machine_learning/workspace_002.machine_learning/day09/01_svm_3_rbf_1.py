'''


multlpte2.txt  ， 一个二分类的问题


支持 "向量机"
        -径向机核函数
        - 使用网格搜索寻找最优参数

'''

import pandas as pd
import matplotlib.pyplot as plt
import sklearn.model_selection as ms #模型选择
import sklearn.svm as svm #支持向量机
import sklearn.metrics as sm #评估模块
import numpy as np


#（1）加载数据
data = pd.read_csv('../../data_test/multiple2.txt',
                   header=None,
                   names=['x1','x2','y'])
# print(data.head())



#整理输出 和输出
x = data.iloc[:,:-1]
y = data.iloc[:,-1]

#划分训练集和测试集
train_x,test_x,train_y,test_y = ms.train_test_split(x,y,
                                                    test_size=0.1,
                                                    random_state=7,
                                                    stratify=y #按照 "y值(类别)"进行等比划分
                                                    );
#构建模型
# model = svm.SVC(kernel='rbf',
#                 gamma=1, #
#                 C=1 #精度大泛化能力小， 反之精度小泛化能力大，
#                 )


params = [
          {'kernel':['linear'],'C':[1,10,100,1000]},
          {'kernel':['poly'],'degree':[2,3],'C':[1,10,100,1000]},
          {'kernel':['rbf'],'gamma':[1,0.1,0.01],'C':[1,10,100,1000]},
          ]

#用网格搜索的方式构建模型
model = ms.GridSearchCV(svm.SVC(),params,cv=3)



#训练
model.fit(train_x,train_y)

# ##################################################
# print('最优模型参数：',model.best_params_)
# ################################################## 拿好最好的模型
# model = model.best_estimator_

#预测
pred_test_y = model.predict(test_x)




#评估
print(sm.classification_report(test_y,pred_test_y))




#画出分类边界线
#用反向思维 "画出0类型的点" 和 "画出 1类别的点"，它们的边界就是模型
# 暴力绘制分类边界线



# 1. 将x1的最小值到x1最大值拆分成200个点，np.linspace()
new_x1_values = np.linspace(data['x1'].min(), data['x1'].max(), 200)

# 2. 将x2的最小值到x2最大值拆分成200个点，np.linspace()
new_x2_values = np.linspace(data['x2'].min(), data['x2'].max(), 200)

# 3. 组合x1和x2的所有情况，40000个点（x1,x2）
all_points = []
for x1 in new_x1_values:
    for x2 in new_x2_values:
        all_points.append([x1, x2])
points = pd.DataFrame(all_points,columns=['x1','x2'])

# 4.将40000个点带信模型中，得到预测类别（0，1）
point_label = model.predict(points)
# print(point_label)

# 5. 将40000个点用散点图画出来，颜色随着预测类别变化，0：黑色，1：白色，cmap = gray。
plt.scatter(points['x1'], points['x2'], c=point_label,cmap='gray')

# 6. 将样本的散点图画出来
plt.scatter(data['x1'], data['x2'], c=data['y'], cmap='brg' )

plt.colorbar()
plt.show()
