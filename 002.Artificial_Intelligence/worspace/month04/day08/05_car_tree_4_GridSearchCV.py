
'''
分类问题：
    使用 "决策树模型"
    使用集成学习- 随机森林
    对小汽车进行等级预测。

    //==================================================  网格搜索
    //==================================================  网格搜索
    通过 网格搜索 寻找，最优参数

    //================================================== 
'''

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import sklearn.preprocessing as sp

import sklearn.ensemble as se #集成学习
import sklearn.svm as svm

import sklearn.model_selection as ms #模型选择
import matplotlib.pyplot as plt


#（1）加载数据
data = pd.read_csv('../data_test/car.txt',
                   sep=',',
                   header=None,
                   names=['a', 'b', 'c', 'd', 'e', 'f', 'g']
                   )

#（2）数据预处理

# 保存编码器，用于后面转换 "预测数据"，
'''
在实际工作中，不光是要给模型的参数，还 要告诉别人，模型的数据是如何转换的。
'''
encoders = {}
df = pd.DataFrame()
for col in data: # col 是列索引， DataFrame 遍历，col是列名
    lb_encoder = sp.LabelEncoder()  #为 “每一列数据”单独构建 "自己的标签编码器" ,data[col] 则拿到的是列数据。
    lb_samples = lb_encoder.fit_transform(data[col])  # 训练每一列数据，进行标签编码。
    df[col] = lb_samples #加入新的df
    encoders[col] = lb_encoder  #保存编码器 ，要放在后面，不要放在 fit_transform 之前####注意





# print(df)
# print(encoders)

#（3）整理输入和输出
train_x = df.iloc[:, :-1]
train_y = df.iloc[:, -1]

#（4）划分训练集和测试集 #car.txt已经单独用来抽取了测试数据。
#TODO，这里全部是训练数据，不需要这一步

#（5）构建模型

# #7020个参数组合,太复杂跑不出来
# params =  {'max_depth': np.arange(3,16),
#      'n_estimators': np.arange(50,501,16),
#      'min_samples_split':  np.arange(2,11),
#      'criterion': ['gini','entropy'] }

#使用少量的参数
params =   {'max_depth': np.arange(5,16),
            'n_estimators': np.arange(100,501,100),
            'criterion': ['gini','entropy']}

#先创建基础的model
base_model = se.RandomForestClassifier(random_state=7) # 注意：分类模型，不是回归模型
model = ms.GridSearchCV(base_model, params, cv=3)


#（6）训练模型（全部样本）
model.fit(train_x,train_y)



print("best_params_:\n", model.best_params_)
print("best_score_:", model.best_score_)

#直接拿到最好的模型
best_model = model.best_estimator_




#================================= 开始预测
#（7）测试集数据
test_datav =[
            ['high','med','5more','4','big','low','unacc'],
            ['high', 'high', '4', '4', 'med', 'med', 'acc'],
            ['low', 'low', '2', '4', 'small', 'high', 'good'],
            ['low', 'med', '3', '4', 'med', 'high', 'vgood']
            ]
#（8） 对测试集进行 "标签编码" ， ”测试集“的标签编码，转换规则要一致需要保持一致。
test_df = pd.DataFrame(test_datav, columns=['a', 'b', 'c', 'd', 'e', 'f', 'g'])
for col in test_df.columns:
    # 使用相应的编码器进行转换
    test_df[col] = encoders[col].transform(test_df[col])
                #上面是训练并转换，这里只需要 transform 转换

# print(test_df)

#（9） 准备 "测试集数据" 的输入和输出。
test_x = test_df.iloc[:, :-1]
test_y = test_df.iloc[:, -1]
# print(test_x)
# print(test_y)


# （10）预测#带入模型中，得到预测值
pred_test_y = best_model.predict(test_x)

print('预测值：', pred_test_y)
print('预测值：', encoders['g'].inverse_transform(pred_test_y))

#打印最好模型的置信概率
print(best_model.predict_proba(test_x))


