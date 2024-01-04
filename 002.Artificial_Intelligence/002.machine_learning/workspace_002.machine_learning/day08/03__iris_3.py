
'''

分类问题： 鸢尾花分类

//=======================
等比划分样本
      , stratify=y #按照 "y值(类别)"进行等比划分
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
                                                    , stratify=y #按照 "y值(类别)"进行等比划分
                                                    );


#（4）构建模型
model = lm.LogisticRegression(solver='liblinear', C=1
                              # ,multi_cass  = 'auto'
                              # 它自动就是多分类类
                              # 它会根据类型判断，自动创建多分类器
                              )

#（5）训练
model.fit(train_x,train_y)

#（6）将测试集带入预测
pred_train_y = model.predict(train_x)
pred_test_y = model.predict(test_x)

#（7）评估

########################## 混淆矩阵
print("\n Confusion Matrix:")
cm = sm.confusion_matrix(test_y, pred_test_y)
print(cm)
# 查准率 = 主对角线上的值 / 该值所在 "列的和"
# 召回率 = 主对角线上的值 / 该值所在  "行的和"


########################## 分类报告
print("\n classification_report:")
cm = sm.classification_report(test_y,pred_test_y)
print(cm)
# support 指的是样本的数量

