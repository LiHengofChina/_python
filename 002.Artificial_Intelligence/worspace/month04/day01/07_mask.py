'''
掩码操作
布尔掩码
'''

import numpy as np

ary = np.arange(1,10)
print(ary)

#布尔掩码
mask = [True, False, True, False, True, False, True, False, True]
#用  “数组” 索引  “列表”
res = ary[mask]
print(res)






print("==" * 20)
################################## 求100以内3的倍数
ary = np.arange(1, 101)
# print(ary % 3 )#利用广播机器求余数，形成的结果，依然是一个数组
# print(ary % 3  == 0) #再判断等于0，形成的结果，依然是一个数组
print(ary[ary % 3  == 0]) #依然是一个数组






################################## 求100以内能被3 和7同时整除的数，解法1：求21也行
print("==" * 20)
ary = np.arange(1, 101)
print(ary[(ary % (21) == 0)])

################################## 求100以内能被3 和7同时整除的数，解法2：分两步
print("==" * 20)
ary = np.arange(1, 101)
res = ary[(ary % 3 == 0)]
res = res[(res % 7 == 0)]
print(res)

################################## 求100以内能被3 和7同时整除的数，解法3：使用&
print("==" * 20)
ary = np.arange(1, 101)
print(ary[(ary % 3 == 0) & (ary % 7 == 0)])





##################################  将分数表中及格和不及格分别 修改为1 和0
score = np.array([[100.0, 99.0, 66.6],
                 [56.8, 92.1, 18.3],
                 [45.6, 78.9, 34.5]])
score[score < 60] = 0
score[score >= 60] = 1
print(score)

