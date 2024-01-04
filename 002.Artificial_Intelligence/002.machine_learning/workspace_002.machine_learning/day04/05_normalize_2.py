'''
归一化 normalize
        将数值转成  0~1  的占比

        使用 sklearn 框架里面的接口来实现

'''
import numpy as np
import sklearn.preprocessing as sp
raw_sample = np.array([[10.0, 20.0, 5.0],
                       [8.0, 10.0, 1.0]])

nor_sample = sp.normalize(raw_sample,norm='l1') #范数是 l1 或者 l2
print(nor_sample)




