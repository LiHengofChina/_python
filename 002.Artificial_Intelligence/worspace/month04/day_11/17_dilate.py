'''
图像膨胀
'''
import cv2
import numpy as np

img = cv2.imread('../data/9.png', 0 )
cv2.imshow('img',img)

#腐蚀
kernel = np.ones(shape=(3,3),dtype=np.uint8)
res = cv2.dilate(img,
                kernel,
                iterations=3)
cv2.imshow('res', res)


cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口
