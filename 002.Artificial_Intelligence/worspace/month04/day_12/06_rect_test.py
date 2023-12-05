'''

图像的矫正：
    透视变换
'''

import cv2
import numpy as np
import math

#（1）加載圖片
img = cv2.imread('../data/paper.jpg')
# cv2.imshow('img',img)

#（2）灰度化
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray', gray)


#（3）去除噪声（模糊）
blured = cv2.GaussianBlur(gray,(5,5),1)
# cv2.imshow('blured',blured)


#（4）闭运算
kernel = np.ones(shape=(3,1),dtype=np.uint8)
close = cv2.morphologyEx(blured,
                        cv2.MORPH_CLOSE,
                        kernel,
                        iterations=3)
# cv2.imshow('close', close)



#（5）边缘检测
canny = cv2.Canny(close,
                  60, #低阈值
                  200 #高阈值   1:2  1:3
                  )
# cv2.imshow('canny',canny)

#（6）查找轮廓
cnts,hierarchy=cv2.findContours(canny,
                                          cv2.RETR_EXTERNAL,    #只检测外轮廓
                                          cv2.CHAIN_APPROX_NONE #存储所有的轮廓点
                                          )
print(len(cnts))            #轮廓数量

#（7）绘制轮廓
# res = cv2.drawContours(img,          # 在哪个图画:注意:这种方式会在原图画,修改原图
#                        cnts,         # 要画的轮廓坐标点
#                        -1,           # 轮廓索引
#                        (0,0,255),    # 颜色
#                        1            # 线条粗细,单位:px  ,-1表示用实心画
#                        )
# cv2.imshow('res', res)


#（8）通过 条件，找到自己需要的轮廓：找到面积最大的四边形，拿到它的四个点
docCnt = None #保存多边形的点
if len(cnts) > 0 :
    cnts = sorted(cnts,
           key=cv2.contourArea,
           reverse=True         #根据面积倒序排序
           )
    for c in cnts:
        eps = cv2.arcLength(c, True) * 0.02  #精度
        approx = cv2.approxPolyDP(c,
                                  eps,  # 精度
                                  True)  # 是否闭合
        if len(approx) == 4:
                docCnt = approx
                break
# print(docCnt)
#（9）验证：将四个点画出来，看看有没有对
img_copy = img.copy()
points = []
for peak in docCnt:
    peak = tuple(peak[0])
    points.append(peak)
    cv2.circle(img_copy,
               peak,
               10,
               (0,0,255),
               2)
cv2.imshow('img_copy',img_copy)


#（10）计算原来的4个点
src =  np.array(points,dtype='float32') #这就是变换之前的四个点，逆时针
# print(src)
#根据勾股定理求宽高
h = int(math.sqrt((src[0][0] - src[1][0]) ** 2 + (src[0][1] - src[1][1]) ** 2))
w = int(math.sqrt((src[0][0] - src[3][0]) ** 2 + (src[0][1] - src[3][1]) ** 2))
# print(h)
# print(w)

#（11）计算变换后的4个点
dst =  np.array([
                    [0 ,0 ],
                    [0 ,h ],
                    [w ,h ],
                    [w ,0 ]
                ],dtype='float32')

#（12）透视变换


#生成透视变换的矩阵
M = cv2.getPerspectiveTransform(src,dst)

#执行 透视变换
res = cv2.warpPerspective(img,
                    M,
                    dsize=(w,h))
cv2.imshow('res',res)


cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口

