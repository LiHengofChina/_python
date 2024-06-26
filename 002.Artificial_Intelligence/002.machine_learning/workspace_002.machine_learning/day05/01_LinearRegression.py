'''
    LinearRegression 线性回归
    Linear线性
    Regression回归

    使用 "python语言" 基于 "梯度下降" 实现线性回归
    不使用任何框架
    ------------------------------- 注意：
        自己实现梯度下降
    ------------------------------- 注意：
       这里讲的是主 要是梯度下降，而不是 ：均方误差
'''
import numpy as np

import matplotlib.pyplot as plt

#============================== （1）准备数据，就是x和y的数组
'''
例如 :数据这是样的，y 是结果，x是特征
[x y]
[x y]
[x y]

'''
x = np.array([0.5, 0.6, 0.8, 1.1, 1.4])
y = np.array([5.0, 5.5, 6.0, 6.8, 7.1])

#============================== （2）构建模型
#目标函数： y = w1 * x + w0，需要更新w1和w0，
# 所以它们需要一个初始值，基于初始值，还始更新
#             组定初始值
w1 = 1  #权重  #一般设置一个 0到1的随机值，并且不能为0
         # 随机数会导致每次结果不一样，这里衔设置固定值，演示方便
w0 = 1  #偏置   #偏一般设置一个 0 或 1


learning_rate = 0.01 #超参数：学习率，不要设置太大，大大容易放大。

epoch = 200     # 超参数：学习轮数，50能不能达到极小值，100轮能不能达到极小值，
                # 要更新多少轮，也是一个超参数，
                # 如：学习率小了，多更新几轮
                # 如：学习率大了，少更新几轮，在没爆炸前
                # 所以轮数也能决定精度

# print('w1:{},w0:{}'.format(w1, w0))
#============================== （3）开始训练
        #训练200轮，就相当于用 "梯度下降" 去更新200次 "模型参数"，
        #w0更新200次，w1也更新200次。
        #就相当于开启200次循环，更新200次参数
for i in range(epoch):
    '''
         使用 "参数更新公式" 更新
         当前值  -  学习率 * 自变量的偏导
         w1 = w1 - learning_rate * w1的偏导
         w0 = w0 - learning_rate * w0的偏导
         根据前面得到的结论
         w1的偏导：∑( x *(w1*x   + w0 - y) )
         w0的偏导：∑ (w1 * x + w0 - y)   
    '''

    '''
    因为我们使用的是 "梯度下降法"，通过导数来求梯度，
    由于有两个变量： w1 和 w0，所以叫求偏导，也就是局部导数
    '''
    #求偏导
    d1 = (x * (w1 * x + w0 - y)).sum()
    d0 = (w1 * x + w0 - y).sum()


    #沿着负梯度下降(损失函数)，不断更新 "权重" 和  "偏置"
    '''
	求导之后，更新原来权重与偏置，是通过减法， 
	所以最后算法来的均方误差会越来越小 
    '''
    w1 = w1 - learning_rate * d1
    w0 = w0 - learning_rate * d0


    '''
       （重点）注意：参数更新中————>是减去学习率 * 偏导值
    '''

    # print('w1:{},w0:{}'.format(w1, w0))
    '''
    这里 打印的是每次更新后的权重和偏执，
                //这个更新可以是无止境的，
    '''


#到这里就完成了，更新200轮，就完成 了
#打印一下200轮参数更新之后的值（学习了200轮之后的值）
print('w1:{},w0:{}'.format(w1, w0))
#w1:2.7622384144059855,w0:3.6240046382951876
'''
    得到了权重和偏置之后，就可以把这个函数补充完整
    
    y = w1 * x + w0
    y = 2.7622384144059855  * x  + 3.6240046382951876
    
'''

#【1】================================================================  #使用得到得到模型预测
#【1】================================================================  #使用得到得到模型预测

# 但是现在也还不知道这两个参数对不对
# 用200轮更新出来的结果,带到数据里面预测一下
# w1 * x + w0
pred_y = w1 * x + w0
            # x是一个数组, 利用数组的广播机制,x的每一个元素就 * w1
            # 得到也是一个数组,就是预测值,
            # 预测结果是在 线性模型上面得到的,所以它一定是在一条直线上面,
            # 所以我们可以使用 图表的形式画出来,看看这条拟合出来的"回归线"
            # import matplotlib.pyplot as plt

print(type(pred_y)) #得到一个数组，把它画出来。

#【2】============================== 画出得到的模型
#【2】============================== 画出得到的模型

#图一
plt.plot(x, pred_y, color='orangered') #画出回归线
                #x是 "x数组" 的值,y是预测结果pred_y

#图二
plt.scatter(x,y) #用散点图画出原来的样本
plt.show()
        #从图上可以看出，这个模型确实是在拟合我们的样本数据

