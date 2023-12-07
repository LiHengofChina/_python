'''
        平移

        注意：
            h ,w = img.shape[0:2]  #通过shape：高度在前面，宽度在后面

            在后面一些接口传参数时：(w, h) 宽度在前面，高度在后面。

'''
import numpy as np
import cv2


def translate(img, x, y):
    '''
    平移
    :param img:  原图
    :param x  :  水平方向移动的坐标
    :param y  :  垂直方向移动的坐标
    :return   :  平移后的图像
    '''
    #（1）
    h ,w = img.shape[0:2] #高度和宽度 ，形状的前两个值
    #（2）构建平移矩阵
    M = np.float32([[1, 0, x],
                    [0, 1, y]])
    #（3）执行 仿射变换
    shifted = cv2.warpAffine(img,   #原图
                             M,     #仿射变换矩阵
                             (w, h) #输出图像：高度、宽度
                             )
    return shifted


if __name__ == "__main__":
    im = cv2.imread('../../data/lena.jpg')
    cv2.imshow('imread', im)

    shifted = translate(im,50,30)#右移50、下移30
    cv2.imshow('shifted', shifted)


    shifted2 = translate(im,-50,-30)#左移50、上移30
    cv2.imshow('shifted2', shifted2)

    cv2.waitKey()  # 等待用户敲击按键。
    cv2.destroyAllWindows()  # 销毁所有窗口

