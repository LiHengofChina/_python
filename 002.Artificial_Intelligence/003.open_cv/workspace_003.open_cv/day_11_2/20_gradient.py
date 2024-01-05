'''
#形态学梯度
'''
import cv2
import numpy as np

img = cv2.imread('../data/6.png', 0)
cv2.imshow('img',img)

kernel = np.ones(shape=(2,2),dtype=np.uint8)

#形态学梯度
res = cv2.morphologyEx(img,
                        cv2.MORPH_GRADIENT,
                        kernel,
                        iterations=1)
cv2.imshow('res', res)



cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口


