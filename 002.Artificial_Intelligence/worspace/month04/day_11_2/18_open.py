'''
开运算：先腐蚀、再膨胀
'''
import cv2
import numpy as np

img = cv2.imread('../data/5.png', 0)
cv2.imshow('img',img)


kernel = np.ones(shape=(3,3),dtype=np.uint8)


#开运算
open = cv2.morphologyEx(img,
                        cv2.MORPH_OPEN,
                        kernel,
                        iterations=4)
cv2.imshow('open', open)


# open = cv2.morphologyEx(im1, cv2.MORPH_OPEN, k)
# r2 = cv2.morphologyEx(im2, cv2.MORPH_OPEN, k)



cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口


