'''
计算N个概率的交叉熵
        --- 验证 交叉熵函数：值越小，概率越高
'''

import math

y_true = [0, 1, 0, 0, 0] #真实类别

y_pred  = [ 0.1, 0.6, 0.1,  0.1,  0.1 ]  #预测概率，和要为1
y_pred1 = [ 0.1, 0.7, 0.1,  0.05, 0.05]  #预测概率，和要为1

y_pred2 = [0.05, 0.8, 0.05, 0.05, 0.05]  #预测概率，和要为1  #这两个相同
y_pred3 = [ 0.1, 0.8, 0.03, 0.04, 0.03]  #预测概率，和要为1  #这两个相同

total_entropy = 0.0
total_entropy1 = 0.0
total_entropy2 = 0.0
total_entropy3 = 0.0

for i in range(len(y_true)):
    total_entropy += y_true[i] * math.log(y_pred[i])
    total_entropy1 += y_true[i] * math.log(y_pred1[i])
    total_entropy2 += y_true[i] * math.log(y_pred2[i])
    total_entropy3 += y_true[i] * math.log(y_pred3[i])
print('交叉熵：', -total_entropy)
print('交叉熵1：', -total_entropy1)
print('交叉熵2：', -total_entropy2)
print('交叉熵3：', -total_entropy3)

