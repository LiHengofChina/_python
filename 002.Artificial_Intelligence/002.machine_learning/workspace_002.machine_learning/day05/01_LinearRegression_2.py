'''
    判断损失值是否已经足够小。（重要）

    前面的示例中，我们更新了 “权重” 和 “偏置” 之后，

'''
import numpy as np
import matplotlib.pyplot as plt

x = np.array([0.5, 0.6, 0.8, 1.1, 1.4])
y = np.array([5.0, 5.5, 6.0, 6.8, 7.1])
w1 = 1
w0 = 1
# learning_rate = 0.01
# learning_rate = 0.1

learning_rate = 0.1

# epoch = 200
# epoch = 500
epoch = 300

for i in range(epoch):
    '''
    # 使用0.01的学习率，学习200轮，它到底有没有达到 "极小值"
    打印出每一轮模参数是怎么更新的
    以及它的损失值是多少，我们可以打印出来
    '''



    '''
     # 求损失值: (Y - Y') 的平方 求和 然后除以2
     # 为什么要除以 2，因为我们的梯度是针对  1/2求的 #就是前面 "推导公式" 那里。    
     # (w1 * x + w0)) ** 2 表示的就是预测值
     
     初始的权重和偏置也能计算出一个损失的值
	 在梯度下降的迭代过程中，模型的权重和偏置不断更新，
	 损失值也随之变化。

    '''
    loss = ((y - (w1 * x + w0)) ** 2).sum() / 2
    print('轮数:{:3}, w1:{:.8f}, w0:{:.8f}, loss:{:.8f}'.format(i, w1, w0, loss))
    #:3   格式化输出，占3位
    #:.8f 格式化输出，占8位小数

    '''
            训练200轮的时候，最后得到的  "损失值" 是 0.12402394
            
            如果损失值为0 : 意味着这条线会穿过所有的点,但实际情况不可能是这样的
            损失值为0  是最理想的状态,但实际当中是不可能的.
        
            判断损失值,是否足够小, 
            最后两轮的损失值大不大,或者两轮损失值已经不再变化了.
            
            第198轮 w1 是 2.764     
            第196轮 w1 是 2.763
            
            变化小数已经在第3位了

            loss:0.12436811
            loss:0.12402394
            损失值已经在第4位了，loss是一个平方的结果
            平方结果已经在第4位了，说明 不怎么变化 
             说明这个结果已经差不多了。
             
             //===================================
             这时，可以再加几轮试一下 或者 调整学习率
                learning_rate = 0.1 学习率改成 0.1  ，提高了10倍
                轮数:  0, w1:1.00000000, w0:1.00000000, loss:44.64000000
                轮数:  1, w1:2.92000000, w0:3.10000000, loss:0.58874400
                轮数:  2, w1:3.06736000, w0:3.30520000, loss:0.23682998
                ......
                轮数:198, w1:2.31581748, w0:4.04197097, loss:0.06700837
                轮数:199, w1:2.31575893, w0:4.04202579, loss:0.06700831
                
                这一回的损失值，0.06700837 和 0.06700831 直接不能再动了。接近于没有变化
                
                loss 从 44 直接为变成了0，它的过程就接近 "一个直角转弯"

             //===================================                
             这里，可以再增加一下学习次数
             epoch = 500，修改为 500轮
                轮数:  0, w1:1.00000000, w0:1.00000000, loss:44.64000000
                轮数:  1, w1:2.92000000, w0:3.10000000, loss:0.58874400
                ......
                轮数:282, w1:2.31401889, w0:4.04365492, loss:0.06700731
                轮数:283, w1:2.31401438, w0:4.04365915, loss:0.06700731
                轮数:284, w1:2.31401000, w0:4.04366325, loss:0.06700730
                轮数:285, w1:2.31400575, w0:4.04366722, loss:0.06700730                
                ......
                轮数:497, w1:2.31386883, w0:4.04379542, loss:0.06700730
                轮数:498, w1:2.31386882, w0:4.04379543, loss:0.06700730
                轮数:499, w1:2.31386881, w0:4.04379543, loss:0.06700730

                后面的损失值，几乎没有变化了，变化的是8位以外的值。
                在280轮左右，已经达到了8位以内的极小值。
             //===================================                
             这时，我们修改成300轮，学习率修改成0.2
            轮数:  0, w1:1.00000000, w0:1.00000000, loss:44.64000000
            轮数:  1, w1:4.84000000, w0:5.20000000, loss:30.36297600
            轮数:  2, w1:1.58944000, w0:1.82080000, loss:20.66684927
            轮数:  3, w1:4.18607104, w0:4.68129280, loss:14.08088217
            轮数:  4, w1:1.97004658, w0:2.39625748, loss:9.60663775
            轮数:  5, w1:3.72381882, w0:4.34635901, loss:6.56629647
            轮数:  6, w1:2.21116705, w0:2.80303944, loss:4.49968868

            这时：w0 的值，1 5 1 4 2 4这样变化，
            说明它们的值，开始波动起来了。    
            这时说明学习率的值太大了。
             //===================================                
             这时，我们修改成300轮，学习率修改成0.3
             此时图就显示不正常了，这个主出现了 "梯度爆炸"
             //===================================   
             这时，我们修改成300轮，学习率修改成0.1
    '''



    #求偏导（梯度）
    d1 = (x * (w1 * x + w0 - y)).sum()
    d0 = (w1 * x + w0 - y).sum()
    #沿着负梯度下降(损失函数)，不断更新 "权重" 和  "偏置"
    w1 = w1 - learning_rate * d1
    w0 = w0 - learning_rate * d0

pred_y = w1 * x + w0
#==============================
plt.plot(x, pred_y, color='orangered') #画出回归线
plt.scatter(x,y)
plt.show()





