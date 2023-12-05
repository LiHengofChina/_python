'''

芯片瑕疵检测： 自己版本

'''

import cv2
import numpy as np
import math

# （1）加載圖片
img = cv2.imread('../data/CPU3.png')
# cv2.imshow('img',img)

# （2）灰度化处理
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray', gray)

# （3）去除噪声（模糊）
blured = cv2.GaussianBlur(gray,(5,5),1)
# cv2.imshow('blured',blured)

# （4）二值化处理
t, im_bin  = cv2.threshold(blured,
                           150, #阈值
                           500, #最大值
                           cv2.THRESH_BINARY #二值化
                           )
print(t)
# cv2.imshow('im_bin', im_bin)

# （5）画出 "一样大小背景为黑色的图片b"
res = np.zeros_like(im_bin)
# print(res)
# print(res.shape)
# cv2.imshow('res',res)

# （6）并在 a图上提取轮廓画在b图片上面 ：查找轮廓 并绘制
cnts,hierarchy=cv2.findContours(im_bin,
                                          cv2.RETR_EXTERNAL,    #只检测外轮廓
                                          cv2.CHAIN_APPROX_NONE #存储所有的轮廓点
                                          )
# print(len(cnts)) #轮廓数量
# for cnt in cnts:
#     print(cnt.shape)
#直接在灰度图上面绘制
cv2.drawContours(       res,         # 在哪个图画:注意:这种方式会在原图画,修改原图
                        cnts,                       # 要画的轮廓坐标点
                        -1,                         # 轮廓索引
                        255,              # 颜色
                         -1                         # 线条粗细,单位:px  ,-1表示用实心画
                        )
# cv2.imshow('res', res)

# （7）b图 - a图 拿到差异c
print(im_bin.shape)
print(res.shape)

img_c = cv2.subtract(res, im_bin)
# cv2.imshow('img_c',img_c)


# （8）对c图查找轮廓，并拟合圆形
#查找轮廓
cnts,hierarchy=cv2.findContours(img_c,
                                          cv2.RETR_EXTERNAL,    #只检测外轮廓
                                          cv2.CHAIN_APPROX_NONE #存储所有的轮廓点
                                          )
print(len(cnts))   #轮廓数量
#生成轮廓拟合参数
center,radius=cv2.minEnclosingCircle(cnts[0])
center = ( int(center[0]), int(center[1]) )
radius = int(radius)
print(center)
print(radius)
#绘制拟合的圆形
img_d = cv2.circle(  img,              #
                   center,           #
                   radius + 5,           #
                   (0,0,255),        #
                   2)                #
cv2.imshow('img_d', img_d)






cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口

