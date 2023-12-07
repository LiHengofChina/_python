'''

图像的对应位置的像素值相加，

并保证
两张相加的图像的尺寸shape要一致

'''

import cv2

#（1）加載圖片
lena = cv2.imread('../../data/lena.jpg', 0)
lily = cv2.imread('../../data/lily_square.png', 0)
cv2.imshow('lena',lena)
cv2.imshow('lily',lily)


#（2）相加
add = cv2.add(lena,lily)
cv2.imshow("add", add)


#（3）“黑白图” -图片直文图均值化
im_equ = cv2.equalizeHist(add)
cv2.imshow("im_equ", im_equ)






cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口

