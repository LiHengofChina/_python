'''
直方图
'''

import numpy as np
import matplotlib.pyplot as plt



import cv2
img = cv2.imread('tmp/lena.jpg', 0)
print(type(img))
print(img.shape)#二维数据

plt.hist(img.ravel(),       #降维处理
         bins=255,          #直方柱数量
         range=(0, 256))    #显示范围
plt.show()