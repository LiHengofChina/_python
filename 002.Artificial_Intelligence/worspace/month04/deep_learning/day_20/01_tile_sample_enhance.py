
'''
瓷砖样本增加处理
'''
import cv2
import numpy as np
import os

from global_var import *
from math import *

# 不切边旋转
def remote(img, angle):
    h, w = img.shape[:2]
    h_new = int(w * fabs(sin(radians(angle))) + h * fabs(cos(radians(angle))))
    w_new = int(h * fabs(sin(radians(angle))) + w * fabs(cos(radians(angle))))

    matRotation = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)

    matRotation[0, 2] += (w_new - w) / 2
    matRotation[1, 2] += (h_new - h) / 2

    imgRotation = cv2.warpAffine(img, matRotation, (w_new, h_new), borderValue=(255, 255, 255))

    return imgRotation


def rotate_all(): #旋转增强处理（不切边的旋转）
    dirs = os.listdir(data_root_path)#列出子目录
    for d in dirs:
        img_dir = os.path.join(data_root_path, d)
        if not os.path.isdir(img_dir):
            continue
        img_dir = os.path.join(img_dir, 'Imgs')
        imgs = os.listdir(img_dir)  # 列出所有图片
        for fn in imgs:
            #拼接图片完整路径
            img_full_path = os.path.join(img_dir, fn)


            #读取图像的数据
            im =cv2.imread(img_full_path)

            pos = fn.find(".")  # 返回.的位置
            name = fn[0:pos]    # 取出文件名
            suffix = fn[pos:]   # 后缀名部分

            # 旋转 45/90/135/180/225/270/315度， 7次
            for i in range(1,8): #从1开始不包含8
                img_new = remote(im, i * 45)  # 旋转

                #拼接新图像名字、路径
                new_name = "%s_rotate_%d%s" % (name, i, suffix)
                new_path = os.path.join(img_dir, new_name)

                #保存
                cv2.imwrite(new_path, img_new)
                print("保存图像成功:", new_path)






if __name__ == '__main__':
    #旋转增强处理
    rotate_all()

    #其它增强处理
    #filp_all()

    print("数据增强处理结束.")


