
'''

分类问题

————————————————分类任务的 评估指标【1】

//===================================== 打印：
查准率
召回率/查全率
F1得分


'''

import sklearn.datasets as sd #数据集合
import sklearn.linear_model as lm #
import pandas as pd
import sklearn.model_selection as ms #模型选择
import sklearn.metrics as sm

#（1）加载数据，整理输出和输出
iris = sd.load_iris()

data = pd.DataFrame(iris.data,
                    columns=iris.feature_names)
data['target'] = iris.target


# data = pd.read_csv('../day07/tmp/training_data.csv',
#                      sep=',',
#                      header=None)

x = data.iloc[:, :-1]
y = data.iloc[:, -1]


#（3）划分训练集和测试集
train_x,test_x,train_y,test_y = ms.train_test_split(x,y,
                                                    test_size=0.1
                                                    , random_state=7 #样本的随机种子
                                                    );


#（4）构建模型
model = lm.LogisticRegression(  solver='lbfgs'
                              , max_iter=1000
                              , C=1
                              )

#（4）训练
model.fit(train_x,train_y)

#（6）将测试集带入预测
pred_train_y = model.predict(train_x)
pred_test_y = model.predict(test_x)

#（7）评估
print('测试集真实值：', test_y.values)
print('测试集预测值：',pred_test_y)
#使用 评估模块来  求精度
print(sm.accuracy_score(test_y,pred_test_y))


#查准率
print("precision:", sm.precision_score(test_y,  # 真实值
                                       pred_test_y,  # 预测值
                                       average="macro"))  # 计算平均值，macro表示：不考虑权重计算平均值



# 召回率 / 查全率
print("recall:", sm.recall_score(test_y,  # 真实值
                                 pred_test_y,  # 预测值
                                 average="macro"))  # 计算平均值，macro表示：不考虑权重计算平均值



#F1得分
print("F1:", sm.f1_score(test_y,
                         pred_test_y,
                         average="macro")) #macro表示：不考虑权重计算平均值

