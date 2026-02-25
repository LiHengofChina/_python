'''

回归问题：

正向激励、自适应、增强 : ada_boost

'''


import pandas as pd
import sklearn.model_selection as ms #模型选择
import sklearn.tree as st #决策树
import sklearn.metrics as sm #评估
import sklearn.ensemble as se #集成学习

import matplotlib.pyplot as plt #

import pandas as pd


##========================================== 从文件读取数据
boston = pd.read_csv('../day06/04_boston_data.csv', sep=',', header=None)
# boston = sd.load_boston()

# boston = pd.read_csv('../day07/tmp/training_data.csv',
#                      sep=',',
#                      header=None)

x = boston.iloc[:, :-1] # x = boston.data
y = boston.iloc[:, -1]  # y = boston.target

#划分训练集和测试集
train_x,test_x,train_y,test_y = ms.train_test_split(x,y,
                                                    test_size=0.1,
                                                    random_state=7 #样本的随机种子
                                                    );

##========================================== （1）先创建一个 单棵决策树
sub_model = st.DecisionTreeRegressor(max_depth=6,
                                 random_state = 7  # #模型的随机种子
                                 );

model  = se.AdaBoostRegressor(sub_model,
                              n_estimators = 400, #弱模型数量
                              random_state = 7#模型的随机种子
                              )



model.fit(train_x,train_y)

#预测
pred_train_y = model.predict(train_x)
pred_test_y = model.predict(test_x)

# 评估
print('训练集：',sm.r2_score(train_y, pred_train_y))
print('测试集：',sm.r2_score(test_y, pred_test_y))




#注意： 这里有400棵树，不方便可视化，但是 特征重要性 在集成学习中是可以可视化的
