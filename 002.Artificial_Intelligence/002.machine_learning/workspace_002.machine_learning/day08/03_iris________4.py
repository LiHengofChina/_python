
'''


————————————————模型评估：性能优化——————>交叉验证法【1】

交叉验证得分：
    （它包含了训练、预测、评估的整体过程）
    创建模型后就开始交叉验证，注释掉后面的代码


//=======================
交叉验证得分：没有问题，
        再打开后面的代码

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


# （3）划分训练集和测试集
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

#（4.1）做5次交叉验证，评估模型是否可用
score = ms.cross_val_score(model,
                           x, y,                        # 样本输入、输出
                           cv=5,                        # 折叠数量，当前 的数量划分成几份
                           scoring="f1_weighted")       # 指定返回的指标 #精度、错误率、查准率、召回率等等 ,f1_weighted得分

print(score)        #打印5次得分

print(score.mean()) #打印平均值
