'''
拟合轮廓的 "外接矩形"
'''

import cv2
import numpy as np

#（1）读取图像
img = cv2.imread('../../data/cloud.png')
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

#（5）生成轮廓拟合参数
x,y,w,h = cv2.boundingRect(cnts[0])
points = np.array([  #矩形的四个顶点
    [[ x,   y   ]],  #左上角
    [[ x,   y+h ]],  #左下角
    [[ x+w, y+h ]],  #右下角
    [[ x+w, y   ]]   #右上角
])


#（6）绘制拟合的矩形
res = cv2.drawContours(img,              # 在哪个图画:注意:这种方式会在原图画,修改原图
                       [points],         # 要画的轮廓坐标点
                       -1,               # 索引
                       (0,0,255),        # 颜色
                       2                # 线条粗细,单位:px  ,-1表示用实心画
                       )
cv2.imshow('res', res)





cv2.waitKey()            # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口



