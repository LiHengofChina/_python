'''
# 06_equalize_hist_demo.py
#  “灰度图像” 的 “直方图” “均衡化处理”
        ：它不是调亮或调暗，它是调像素的分布。

# 过暗 或 过亮的图像 则适用 均衡化处理

# 白纸写黑字，这种就不适合做均衡化处理


另外:opencv,也可以有画直方图的接口

 
'''
import cv2
from matplotlib import pyplot as plt
# import matplotlib.pyplot as plt

im = cv2.imread('../data/sunrise.jpg', 0)
                            # 0表示灰度田图像 和自己转灰度图像是没有区别的
print(im.shape)
cv2.imshow('imread', im)


# （1）直方图均衡化
im_equ = cv2.equalizeHist(im)
cv2.imshow("equ1", im_equ)


# （2）原始直方图
print(im.ravel())
plt.subplot(2, 1, 1)
plt.hist(im.ravel(), #降维：ravel返回一个连续的扁平数组
         256,       #柱体个数
         [0, 256],  #柱体范围
         label="orig")
plt.legend()


## 均衡化处理后的直方图
plt.subplot(2, 1, 1)
# plt.subplot(2, 1, 2)
plt.hist(im_equ.ravel(), #降维：ravel返回一个连续的扁平数组
        256,        #柱体个数
         [0, 256],  #柱体范围
         label="equalize")
plt.legend()
plt.show()

cv2.waitKey() #等待用户敲击按键。
cv2.destroyAllWindows()  #销毁所有窗口

