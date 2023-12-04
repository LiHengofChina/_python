'''

二值化 与 反二值化

二值化一定是在灰度图像上面进行的

'''

import cv2
from matplotlib import pyplot as plt
# import matplotlib.pyplot as plt

im = cv2.imread('../data/lena.jpg', 0)
cv2.imshow('imread', im)

#（1）二值化
t, im_bin  = cv2.threshold(im,
                           127, #阈值
                           255, #最大值
                           cv2.THRESH_BINARY #二值化
                           )
print(t)
cv2.imshow('THRESH_BINARY', im_bin)



#（2）反二值化
t, im_bin  = cv2.threshold(im,
                           100, #阈值
                           255, #最大值
                           cv2.THRESH_BINARY_INV #反二值化
                           )
print(t)
cv2.imshow('THRESH_BINARY_INV', im_bin)



cv2.waitKey()            #等待用户敲击按键。
cv2.destroyAllWindows()  #销毁所有窗口

