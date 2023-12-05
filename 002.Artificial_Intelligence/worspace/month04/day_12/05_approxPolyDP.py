'''

拟合轮廓的 "逼近多边形"
    --精度值越小，越接近轮廓

'''

import cv2
import numpy as np

#（1）读取图像
img = cv2.imread('../data/cloud.png')
# cv2.imshow('img',img)

#（2）彩色转灰度：灰度化处理
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print(gray.shape)
# cv2.imshow('gray', gray)


#（3）二值化处理：这里不需要，但是流程中有这一步 *************** 怎么把背景变成黑色,物品变成白色,这是最难的
t, im_bin  = cv2.threshold(gray,
                           127, #阈值
                           255, #最大值
                           cv2.THRESH_BINARY #二值化
                           )
# print(t)
# cv2.imshow('THRESH_BINARY', im_bin)

#（4）查找轮廓
cnts,hierarchy=cv2.findContours(im_bin,
                                          cv2.RETR_EXTERNAL,    #只检测外轮廓
                                          cv2.CHAIN_APPROX_NONE #存储所有的轮廓点
                                          )
print(len(cnts))            #轮廓数量


#（5）拟合多边形
# ========= (5.1)
adp1 = img.copy()
eps = cv2.arcLength(cnts[0],True) * 0.005  #一般精度：是以周长的多少倍来设置 #周长的 0.005 倍
approx = cv2.approxPolyDP(cnts[0],
                          eps,      #精度
                          True)      #是否闭合
cv2.drawContours(adp1,[approx],-1,(0,0,255),2)  #绘制轮廓
cv2.imshow('adp1',adp1)

# ========= (5.2)
adp2 = img.copy()
eps = cv2.arcLength(cnts[0],True) * 0.01  #一般精度：是以周长的多少倍来设置 #周长的 0.05 倍
approx = cv2.approxPolyDP(cnts[0],
                          eps,      #精度
                          True)      #是否闭合
cv2.drawContours(adp2,[approx],-1,(0,0,255),2)
cv2.imshow('adp2',adp2)


cv2.waitKey()            # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口



