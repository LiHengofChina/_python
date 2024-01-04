
'''

分类问题： 鸢尾花分类

//=======================使用：决策树模型

单颗决策树

'''

import sklearn.datasets as sd #数据集合
import sklearn.linear_model as lm #
import pandas as pd
import sklearn.model_selection as ms #模型选择
import sklearn.metrics as sm
import sklearn.tree as st # 决策树

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

# #为"单颗决策树"准备数据
selected_rows = y.isin([1, 2])
x = x[selected_rows]
y = y[selected_rows]

# （3）划分训练集和测试集
train_x,test_x,train_y,test_y = ms.train_test_split(x,y,
                                                    test_size=0.1
                                                    , random_state=7 #样本的随机种子
                                                    , stratify=y #按照 "y值(类别)"进行等比划分
                                                    );


#（4）构建模型
# model = lm.LogisticRegression(solver='liblinear', C=1
#                               # ,multi_cass  = 'auto'
#                               # 它自动就是多分类类
#                               # 它会根据类型判断，自动创建多分类器
#                               )

model = st.DecisionTreeClassifier()

#（4.1）做5次交叉验证，评估模型是否可用
score = ms.cross_val_score(model,
                           x, y,                        # 样本输入、输出
                           cv=5,                        # 折叠数量，当前 的数量划分成几份
                           scoring="f1_weighted")       # 指定返回的指标 #精度、错误率、查准率、召回率等等 ,f1_weighted得分

print(score)        #打印5次得分

print(score.mean()) #打印平均值

# ======================== 没有问题，可以使用，再做后面的代码。

#（5）训练
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


