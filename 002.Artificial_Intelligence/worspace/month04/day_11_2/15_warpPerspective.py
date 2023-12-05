'''
透视变换
'''
import cv2
import numpy as np



#（1）加載圖片
img = cv2.imread('../data/pers.png', 0)
cv2.imshow('img',img)

#获取高、宽
h,w = img.shape[:2]

#生成“变换之前的坐标点”，"变换之后"的坐标点。 TODO暂时直接拿到点
src = np.float32([[58, 2], [167, 9], [8, 196], [126, 196]]) # 输入图像四个顶点坐标
dst = np.float32([[16, 2], [167, 8], [8, 196], [169, 196]]) # 输出图像四个顶点坐标

#生成透视变换的矩阵
M = cv2.getPerspectiveTransform(src,dst)

#执行 透视变换
res = cv2.warpPerspective(img,
                    M,
                    dsize=(w,h))
cv2.imshow('res',res)





cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口

