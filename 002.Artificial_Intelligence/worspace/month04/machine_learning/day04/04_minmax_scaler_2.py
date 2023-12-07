'''
范围缩放
        使用sklearn 框架的接口来实现范围缩放
'''
import numpy as np
import sklearn.preprocessing as sp
raw_sample = np.array([[3.0,-100.0,2000.0],
                       [0.0,400.0,3000.0],
                       [1.0,-400.0,2000.0]])




mms = sp.MinMaxScaler(feature_range=(0, 1))    # 定义 "范围缩放器对象"
                                               # feature_range=(0,1) 意思是 最小值0，最大值为1，可以为其它值
                                               # 可以不设置 feature_range=(0,1)， 默认0和1

#合在一起写（方式一）（训练并转换）
# mms_sampeles = mms.fit_transform(raw_sample)  # 缩放
# print(mms_sampeles)

#分开写（方式二）
mms.fit(raw_sample) # "mms模型" 接收数据 "进行训练" ，不用接收返回值，训练后的规则已存在于mms中
res = mms.transform(raw_sample)
print(res)

