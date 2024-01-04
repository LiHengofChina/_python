
'''
	"波士顿房屋价格" 数据预测
    分别构建 "线性回归"、"岭回归"、"多项式回归" 看谁更好
    # 评估每一个模型的R2得分
    //=============================================== 本示例变化：
    在多项式回归的时候使用 "岭回归"
    再怎么调也调不上去了
因为 "这组数据分布" 对当前模型分布就不合适，所以可以  "更换其它模型"


    //==================================================== 更换模型：
    使用 单颗决策树 模型：


'''

import sklearn.model_selection as ms #模型选择
import pandas as pd
import sklearn.linear_model as lm
import matplotlib.pyplot as plt
import sklearn.metrics as sm
import  numpy as np
import sklearn.pipeline as pl
import sklearn.preprocessing as sp
import sklearn.tree as st #决策树

# 数据来自：data_url = "http://lib.stat.cmu.edu/datasets/boston"
data = pd.read_csv('../day06/04_boston_data.csv', sep=',', header=None)

##==========================================
x = data.iloc[:, :-1]
y = data.iloc[:, -1]

train_x,test_x,train_y,test_y = ms.train_test_split(x,y,
                        test_size=0.2,
                        random_state= 7)

##==========================================  # （3）根据 "训练集" 训练模型
def get_model(name,model):
    print('-------------------',name,'-------------------')
    model.fit(train_x,train_y)
    #训练集的预测值
    pred_train_y = model.predict(train_x)
    #测试集的预测值
    pred_test_y =  model.predict(test_x)
    #评估
    print('训练集', sm.r2_score(train_y, pred_train_y))
    print('测试集', sm.r2_score(test_y, pred_test_y))


# 创建模型字典
model_dic = {
    '线性回归':lm.LinearRegression(),
    '岭回归':lm.Ridge(),
    '多项式回归': pl.make_pipeline(sp.PolynomialFeatures(2),
                                   lm.Ridge(alpha=292)
                                  ),
    '单颗决策树': st.DecisionTreeRegressor(max_depth=8)
                    #回归器：如果不添加参数，就会过拟合，训练是1，测试可能0.64.
                    # 就算是 决策树 ，效果也不是很好，因为它是弱模型，预测结果不会很好


}

for name,model in model_dic.items():
    get_model(name,model)

'''
------------------- 单颗决策树 -------------------
 算是 决策树 ，效果也不是很好，因为它是弱模型，预测结果不会很好
'''

