'''
    判断损失值是否已经足够小。

    把w1、w0、loss的值 收集起来，画出来
    方便观察

'''
import numpy as np
import matplotlib.pyplot as plt

x = np.array([0.5, 0.6, 0.8, 1.1, 1.4])
y = np.array([5.0, 5.5, 6.0, 6.8, 7.1])
w1 = 1
w0 = 1

learning_rate = 0.1

# 比较平缓
learning_rate = 0.01



# learning_rate = 0.2
        # 这时会出现波动



# epoch = 200
# epoch = 500
epoch = 300

'''
收集数据，w1、w0、loss，
分别是权重、偏置、损失值。

用三幅子图把它们分别画出来。

重点观察 "损失值" 的下降曲线

'''
w1s, w0s, losses = [], [], []
epoches = []# 这个是x的值

for i in range(epoch):


    loss = ((y - (w1 * x + w0)) ** 2).sum() / 2
    # print('轮数:{:3}, w1:{:.8f}, w0:{:.8f}, loss:{:.8f}'.format(i, w1, w0, loss))
    # 不打印，收集数据
    w1s.append(w1)
    w0s.append(w0)
    losses.append(loss)
    epoches.append(i)

    d1 = (x * (w1 * x + w0 - y)).sum()
    d0 = (w1 * x + w0 - y).sum()
    w1 = w1 - learning_rate * d1
    w0 = w0 - learning_rate * d0

pred_y = w1 * x + w0

plt.plot(x, pred_y, color='orangered') #画出回归线
plt.scatter(x,y) #画出样本数据

#根据收集的数据画图，及损失值的变化情况




plt.figure('LR',facecolor='lightgray')

################################# 3行1列，第一副子图。
plt.subplot(3,1,1)
plt.plot(epoches,w1s,color= 'dodgerblue',
         label = 'w1')
plt.legend()

################################# 3行1列，第二副子图。
plt.subplot(3,1,2)
plt.plot(epoches,w0s,color= 'dodgerblue',
         label = 'w0')
plt.legend()


################################# 3行1列，第三副子图。
plt.subplot(3,1,3)
plt.plot(epoches,losses,color= 'orangered',
         label = 'loss')
plt.legend()

plt.tight_layout()

plt.show()








