'''
图像的模糊（平滑）
    ："减小"像素之前的差异

'''
import cv2
import numpy as np

img = cv2.imread('../../data/salt.jpg')
cv2.imshow('img',img)


#（1）均值滤波
mean = cv2.blur(img,(5,5))
cv2.imshow('mean',mean)


#（2）高斯滤波
gaussian = cv2.GaussianBlur(img,(5,5),3)
cv2.imshow('gaussian',gaussian)

#（3）中位滤波
median = cv2.medianBlur(img,5)
cv2.imshow('median', median )

#（4）自定义卷积核
filter_w = np.ones(shape=(5,5),dtype=np.float32) / 25.0  #5*5为25，所以除以25
res = cv2.filter2D(img,
             -1, #图像深度，-1代表和原图值一致
             filter_w
             )
cv2.imshow('res',res)




cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口


