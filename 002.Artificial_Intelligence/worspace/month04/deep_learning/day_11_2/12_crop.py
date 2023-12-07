'''

:图像的裁剪： 通过对数组进行切片来实现

        随机裁剪


'''


import cv2
import numpy as np


#随机裁剪
def random_crop(img,cw,ch):
    #（1）生成随机坐标
    start_x = np.random.randint(0,              #随机开始值
                                img.shape[1]-cw #随机结束值
                                )
    start_y = np.random.randint(0,              #随机开始值
                                img.shape[0]-ch #随机结束值
                                )

    #（2）切片
    new_img = img[start_y:start_y+ch,
        start_x:start_x+cw
        #,:  通道全部都要，所以不写最好，因为不写，可以处理灰度和彩色图，写了只能处理彩色图
       ]
    return new_img


if __name__ == "__main__":
    im = cv2.imread('../../data/banana_1.png')
    cv2.imshow('imread', im)

    #
    random_res = random_crop(im,200 ,200 )
    cv2.imshow('random_res',random_res)



    cv2.waitKey()  # 等待用户敲击按键。
    cv2.destroyAllWindows()  # 销毁所有窗口

