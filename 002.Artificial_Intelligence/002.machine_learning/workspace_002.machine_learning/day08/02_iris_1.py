
'''

分类问题： 鸢尾花分类

    逻辑回归，本质上是二分类， 但是它也能做多分类
        ----------- 这里演示做 “二分类”，做 1 和 2分类

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

x = data.iloc[:, :-1]
y = data.iloc[:, -1]



#（2）在数据中，取出 1类别 和 2类型的数据（二分类）
# 筛选出 y 值为 1 和 2 的行
selected_rows = y.isin([1, 2])
x = x[selected_rows]
y = y[selected_rows]

'''
这里我的 x 进行了x = data.iloc[:, :-1]，它已经没有最后一列了，
为什么 x_selected = x[selected_rows] 还是能找出来

想象一下，你有两个列表，一个是 x（包含了一些特征数据），另一个是 y（包含了对应的分类标签，也就是目标变量）。这两个列表是并排放置的，每一行数据在 x 和 y 中的位置都是对应的。换句话说，x 的第一行数据对应着 y 的第一行标签，x 的第二行数据对应着 y 的第二行标签，以此类推。
现在，你想从这两个列表中只挑选出那些 y 为 1 或 2 的行。为了做到这一点，你首先检查 y 中的每一行，看它是不是 1 或 2。这就是 selected_rows = y.isin([1, 2]) 这行代码的作用。它会给你一个新的列表，这个列表里的每一行都是 True 或 False，代表着 y 的相应行是否为 1 或 2。
最后，你用这个新的 True/False 列表去选择 x 中的对应行。因为 x 和 y 是并排放置的，所以 True 或 False 的位置在 x 中也是一样的。这就是 x_selected = x[selected_rows] 这行代码的作用。它从 x 中选择了所有在 selected_rows 中标记为 True 的行，也就是那些 y 值为 1 或 2 的对应行。

'''



#（3）划分训练集和测试集
train_x,test_x,train_y,test_y = ms.train_test_split(x,y,
                                                    test_size=0.1,
                                                    random_state=7 #样本的随机种子
                                                    );
#（4）构建模型
model = lm.LogisticRegression(solver='liblinear', C=1)


#（4）训练
model.fit(train_x,train_y)

#（6）将测试集带入预测
pred_train_y = model.predict(train_x)
pred_test_y = model.predict(test_x)

#（7）评估
print('测试集真实值：', test_y.values)
print('测试集预测值：',pred_test_y)

#求比例
# print( (test_y.values  ==  pred_test_y).sum() / len(test_y)) #实际它是平均值
# print( (test_y.values  ==  pred_test_y).mean() ) #实际它是平均值

#使用 评估模块来  求精度
print(sm.accuracy_score(test_y,pred_test_y))



