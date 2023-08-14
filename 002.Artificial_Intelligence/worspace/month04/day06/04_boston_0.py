
'''
	"波士顿房屋价格" 数据预测
	boston = sd.load_boston();
	"波士顿房价数据集存在道德问题：" 从1.2怎么已经移除
	除非代码的目的是研究和教育

'''

# import sklearn.datasets as sd
# boston = sd.load_boston()
# print(boston)

'''
print(boston)
{
'data': array([[],
               [],
               []]),
'target': array([],
               [],
               []),
'DESCR': ".."

}

//返回一个看上去像字典，但其它是不是字典的结构
//它是sklearn 里面提供的一个 "类似字典" 的结构。
//但它可以当成字字典使用


//=====================================

print(boston.keys)
查看它里面所有的键
dict_keys([ 'data',
            'target',
            'feature_names',
            'DESCR',
            'filename'])

//=====================================
    print(boston.filename)
 
    /ai/lib/python3.7/site-packages/sklearn/datasets/data/boston_house_prices.csv
                    "site-packages" 里面就是所有的第三方库
                    说明：这些数据也是保存在一个CSV文件中的
                    //================这个路径下面还有其它的文件
                    boston_house_prices.csv
                    breast_cancer.csv
                    iris.csv
//=====================================
    print(boston.DESCR)
    describe描述的缩写
        Number of Instances :  506    //当前数据有506个样本
        Number of Attributes:  13 numeric/categorical predictive.     
                               //13个特征//在波士顿地区，影响房屋价格的13个因素
                               Median Value(attribute 14) is usually the target.
                               //以及一个中位数，作为第14列。
        
        //===================================说明：
        前13列是x，最后一列是y
        我们就是要根据前13列，影响房屋价格的因素预测当前房子值多少钱
        
        x 是506行，13列 ，二维的
        y 是506行，y是一维的
        
//=====================================
    print(boston.feature_names)
    //=====================================
    : Attribute Information(in order):
        - CRIM      犯罪率
        - ZN        住宅用地比例，住宅区多，商业区多
        - INDUS     商业用地比例
        - CHAS      是否靠近 查尔斯河，河景房
        - NOX       一氧化氮深度，空气质量，
        - RM        房间数量
        - AGE       房屋的年龄
        - DIS       距离5个就业中心的加权距离
        - RAD       路网密度，交通是否发达。
        - TAX       房产税
        - PTRATIO   学区房，师生占比
        - B         黑人比例
        - LSTAT     低收入人口比例//平民区，还是富人区
        - MEDV      房屋价格的中位数
        //13列数据的具体含义     
        
//=====================================
    print(boston.data)
    print(boston.data.shape)        //506行13列，它就是x数据
 
//=====================================
    print(boston.target)
    print(boston.target.shape)        //506行1列，它就是y数据




'''

import pandas as pd

# 数据来自：data_url = "http://lib.stat.cmu.edu/datasets/boston"
data = pd.read_csv('04_boston_data.csv', sep=',', header=None)
x = data.iloc[:, :-1]
print(x)
y = data.iloc[:, -1]
print(y)


