'''
基于决策树 实现：波士顿房屋价格

并使用图来展示它

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

##==========================================  决策树 可视化

plt.figure('tree',figsize=(10,6))

#画
st.plot_tree(model,
             fontsize=6
             # ,feature_names=boston.feature_names
             ,filled=True # 颜色填充
             )
plt.savefig("02_tree.png")





#显示
plt.show()
