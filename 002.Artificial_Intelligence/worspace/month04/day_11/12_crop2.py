'''

:图像的裁剪： 通过对数组进行切片来实现

        中心裁剪

'''


import cv2
import numpy as np


#中心裁剪
def center_crop(img,cw,ch):
    #（1）获取高度和宽高、并计算中心的x和y
    h, w = img.shape[0:2] #取图像高度、宽度
    start_x = int(img.shape[1] / 2) - int(cw /2)
    start_y = int(img.shape[0] / 2) - int(cw /2)



    #（2）切片
    new_img = img[start_y:start_y+ch,
        start_x:start_x+cw
       ]
    return new_img


if __name__ == "__main__":
    im = cv2.imread('../data/banana_1.png')
    cv2.imshow('imread', im)


    center_res = center_crop(im ,200 ,200 )
    cv2.imshow('center_res',center_res)



    cv2.waitKey()  # 等待用户敲击按键。
    cv2.destroyAllWindows()  # 销毁所有窗口

