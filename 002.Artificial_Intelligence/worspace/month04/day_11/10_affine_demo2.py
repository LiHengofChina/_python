'''


        旋转

'''
import numpy as np
import cv2


def rotate( img, angle, center=None, scale=1.0):
    '''
    旋转
    :param img:     原图
    :param angle:   旋转角度
    :param center:  旋转中心
    :param scale:   缩放比例
    :return:        返回 旋转后的图像
    '''

    #（1）获取高宽
    h, w = img.shape[0:2] #取图像高度、宽度

    #（2）处理中心
    if center is None: #如果center没有传值，以原图中心作为中心
        center = (int(w/2), int(h/2))

    #（3）计算旋转矩阵，2D的一个旋转矩阵
    M = cv2.getRotationMatrix2D(center, angle, scale)

    #（4）执行 仿射变换
    rotated = cv2.warpAffine(img,   #原图
                             M,     #仿射变换矩阵
                             (w, h) #输出图像：高度、宽度
                             )
    return rotated

if __name__ == "__main__":
    im = cv2.imread('../data/lena.jpg')
    cv2.imshow('imread', im)

    rotate1 = rotate(im,45) #角度为正，逆时针旋转
    cv2.imshow('rotate1', rotate1)

    rotate2 = rotate(im,-45) #角度为负，顺时针旋转
    cv2.imshow('rotate2', rotate2)

    cv2.waitKey()  # 等待用户敲击按键。
    cv2.destroyAllWindows()  # 销毁所有窗口

