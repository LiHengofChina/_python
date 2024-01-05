'''

#  “彩色图像的” 的 “亮度通道”  的“均衡化处理”

# 转换YUV色彩空间

# imshow 要求BGR色彩空间

图像太亮 或 太暗 ：特征会变弱，不便于识别。

'''
import cv2
from matplotlib import pyplot as plt
# import matplotlib.pyplot as plt

im = cv2.imread('../data/sunrise.jpg')
                            # 不加0，读取出来才是3通道的
print(im.shape)
cv2.imshow('imread', im)


#（1）BRG空间转换为YUV空间
# YUV：亮度，色度，饱和度，其中Y通道为亮度通道
yuv = cv2.cvtColor(im, cv2.COLOR_BGR2YUV)
print("yuv.shape:", yuv.shape)

#（2）把亮度通道 ：取出亮度通道，均衡化并赋回原图像
yuv[ : , : , 0 ] = cv2.equalizeHist(yuv[ : , : , 0 ]) #


#（3）转回BGR
equalized_color = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
cv2.imshow('Equalized Color', equalized_color)

cv2.waitKey()            #等待用户敲击按键。
cv2.destroyAllWindows()  #销毁所有窗口

