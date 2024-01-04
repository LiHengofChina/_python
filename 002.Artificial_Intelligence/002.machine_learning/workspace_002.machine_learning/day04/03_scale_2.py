'''

标准化（均值移除）：" 每一列的平均值为0" ， "标准差为1"

 使用 sklearn 框架来实现

'''
import numpy as np
import sklearn.preprocessing as sp

# 构建一个3行3列的数据，人工智能里面数据一般都是浮点数
raw_sample = np.array([[3.0,-100.0,2000.0],
                       [0.0,400.0,3000.0],
                       [1.0,-400.0,2000.0]])

print(raw_sample)

print("===" * 30)

#使用 sklearn 框架来实现
res = sp.scale(raw_sample)

print(res)
