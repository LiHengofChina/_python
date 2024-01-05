'''
    练习：检测出纸张的边沿，
    不能有其他的瑕疵
'''



import cv2
import numpy as np

img = cv2.imread('../data/paper.jpg', 0)
cv2.imshow('img',img)



#（1） 先高斯模糊
blured = cv2.GaussianBlur(img,(5,5),1)
cv2.imshow('blured',blured)

#（2）再提边沿Canny
canny = cv2.Canny(blured,
                  60, #低阈值
                  300 #高阈值   1:2  1:3
                  )
cv2.imshow('canny',canny)



cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口


import cv2

# 打印 OpenCV 版本
print("OpenCV version:", cv2.__version__)
