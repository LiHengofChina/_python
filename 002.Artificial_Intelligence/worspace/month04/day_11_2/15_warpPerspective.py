'''
透视变换
'''
import cv2

img3 = cv2.imread('../data/3.png', 0)
img4 = cv2.imread('../data/4.png', 0)
cv2.imshow('img3',img3)
cv2.imshow('img4',img4)



cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口

