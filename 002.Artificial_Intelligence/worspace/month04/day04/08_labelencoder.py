'''
标签编码
将字符串转成数值类型
'''
import numpy as np

import sklearn.preprocessing as sp

#标签编码只能转换一维数据


raw_samples = np.array(['bmw','BYD','bmw',
						'benz','BYD','audi'])

lb_encoder = sp.LabelEncoder() #定义标签编码对象
lb_samples = lb_encoder.fit_transform(raw_samples) #执行标签编码#训练并转换
print(lb_samples)


print(lb_encoder.inverse_transform(lb_samples)) #逆向转换


