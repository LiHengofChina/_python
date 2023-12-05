'''
    边沿检测:

'''

import cv2
import numpy as np

img = cv2.imread('../data/lily.png',0)
cv2.imshow('img',img)

#（1）Sobel
sobel = cv2.Sobel(img,
                  cv2.CV_64F,#图像深度
                  dx=1,     #x方向求导导除数
                  dy=1,     #y方向求导阶数
                  ksize=5   #算子的尺寸大小
                  )
cv2.imshow('sobel',sobel)

#（2）Laplacian
Laplacian = cv2.Laplacian(img,
                          cv2.CV_64F)
cv2.imshow('Laplacian',Laplacian)

#（3）Canny
canny = cv2.Canny(img,
                  60, #低阈值
                  240 #高阈值   1:2  1:3
                  )
cv2.imshow('canny',canny)



cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口

