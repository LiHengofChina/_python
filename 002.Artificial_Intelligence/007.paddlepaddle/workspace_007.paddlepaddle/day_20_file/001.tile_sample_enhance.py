#【1】 第一步：数据增强
import cv2
import numpy as np
import os
import random
import matplotlib.pyplot as plt
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


def do_rotate(im, angle, center=None, scale=1.0):
    """
    图像旋转变换
    :param im: 原始图像数据
    :param angle: 旋转角度
    :param center: 旋转中心，如果为None则以原图中心为旋转中心
    :param scale: 缩放比例，默认为1
    :return: 返回旋转后的图像
    """
    h, w = im.shape[:2]  # 获取图像高、宽

    # 旋转中心默认为图像中心
    if center is None:
        center = (w / 2, h / 2)

    # 计算旋转矩阵
    M = cv2.getRotationMatrix2D(center, angle, scale)

    # 使用openCV仿射变换实现函数旋转
    rotated = cv2.warpAffine(im, M, (w, h))

    return rotated  # 返回旋转后的矩阵


def rotate_all():
    dirs = os.listdir(data_root_path)  # 列出所有子目录
    for d in dirs:
        dir_path = os.path.join(data_root_path, d)  # 拼接路径
        if not os.path.isdir(dir_path):  # 不是目录
            continue

        sub_dir_path = os.path.join(dir_path, "Imgs")  # 子目录下的Imgs目录

        imgs = os.listdir(sub_dir_path)  # 列出所有子目录下的原始样本
        for img_file in imgs:  # 遍历
            img_full_path = os.path.join(sub_dir_path, img_file)  # 拼接完整路径
            print(img_full_path)

            im = cv2.imread(img_full_path)  # img_full_path

            pos = img_file.find(".")  # 返回.的位置
            name = img_file[0:pos]  # 取出名称部分
            suffix = img_file[pos:]  # 取出后缀名

            # 旋转45/90/135/180/225/270/315度
            for i in range(1, 8):
                img_new = remote(im, 45 * i)
                # 拼一个新的文件名，格式如：AIBJ-KG-00001_rotate_1.jpg
                img_new_name = "%s_rotate_%d%s" % (name, i, suffix)

                cv2.imwrite(os.path.join(sub_dir_path, img_new_name), img_new)  # 将裁剪后的图片保存至新文件
                print("save ok:", os.path.join(sub_dir_path, img_new_name))


if __name__ == "__main__":
    # 图像旋转
    rotate_all()

    print("图像预处理结束")
