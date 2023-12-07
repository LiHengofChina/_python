'''

翻转（镜像）

'''

import cv2
# import matplotlib.pyplot as plt


im = cv2.imread('../../data/lena.jpg')
cv2.imshow('imread', im)


#（1）垂直镜像，第二个参数是 0
im_flip_0 = cv2.flip(im, 0 )
cv2.imshow("im_flip_0",im_flip_0)


#（2）水平镜像，第二个参数是 1
im_flip_1 = cv2.flip(im, 1 )
cv2.imshow("im_flip_1",im_flip_1)



cv2.waitKey()            #等待用户敲击按键。
cv2.destroyAllWindows()  #销毁所有窗口
