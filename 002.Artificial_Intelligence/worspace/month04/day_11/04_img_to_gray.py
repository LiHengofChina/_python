'''
图像灰度化处理

        一般是显示 “彩色图像”：
        计算的是灰度图像

        转换彩色空间：imread读取的图像默认为BGR

        bgr ---> gray



'''
import cv2

im = cv2.imread('../data/Linus.png')
print(im.shape)
cv2.imshow('imread', im)

#彩色转灰度：灰度化处理
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
print(im_gray.shape)
cv2.imshow('im_gray', im_gray)

cv2.waitKey() #等待用户敲击按键。
cv2.destroyAllWindows()  #销毁所有窗口


