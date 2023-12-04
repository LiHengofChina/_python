'''
闭运算：先膨胀、再腐蚀、
'''
import cv2
import numpy as np

img = cv2.imread('../data/9.png', 0 )
cv2.imshow('img',img)

kernel = np.ones(shape=(1,4),dtype=np.uint8)

#闭运算
close = cv2.morphologyEx(img,
                        cv2.MORPH_CLOSE,
                        kernel,
                        iterations=8)
cv2.imshow('close', close)



cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口


