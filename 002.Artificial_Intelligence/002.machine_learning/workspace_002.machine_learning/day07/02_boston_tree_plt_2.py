'''
基于决策树 实现：波士顿房屋价格

特征重要性 可视化

'''


import pandas as pd
import sklearn.model_selection as ms #模型选择
import sklearn.tree as st #决策树
import sklearn.metrics as sm #评估

import matplotlib.pyplot as plt #

import pandas as pd


##========================================== 从文件读取数据
boston = pd.read_csv('../day06/04_boston_data.csv', sep=',', header=None)
# boston = sd.load_boston()


x = boston.iloc[:, :-1] # x = boston.data
y = boston.iloc[:, -1]  # y = boston.target

#划分训练集和测试集
train_x,test_x,train_y,test_y = ms.train_test_split(x,y,
                                                    test_size=0.1,
                                                    random_state=7 #样本的随机种子
                                                    );

#
model = st.DecisionTreeRegressor(max_depth=4,
                                 random_state = 7  # #模型的随机种子
                                 );

model.fit(train_x,train_y)

#预测
pred_train_y = model.predict(train_x)
pred_test_y = model.predict(test_x)

# 评估
print('训练集：',sm.r2_score(train_y,pred_train_y))
print('测试集：',sm.r2_score(test_y,pred_test_y))



##==========================================  特征重要性 可视化
fi = model.feature_importances_
# fi = pd.Series(fi,index = boston.feature_names)
fi = pd.Series(fi)
# 排序  # ascending=False 倒序
fi = fi.sort_values(ascending=False)

# 使用柱状图，来显示特征的和重要性。

# plt.bar(fi.index,fi.values)   # 方式一：plot画图
fi.plot.bar() #方式二： pandas画图 #fi本身就是数据，它会把索引当成x值，value当成y值


plt.xticks(rotation=45)
#显示
plt.show()
