
'''
"查找" 并 "绘制" 轮廓

虽然：cv2.imread('../data/3.png',0) 可以直接读取灰度图像，
但是为了后续保留彩色信息，所以一般读取成彩色图像，再转成灰色。
用灰色读取，使用彩色查找。

'''

import cv2


#（1）读取图像
img = cv2.imread('../data/3.png')
cv2.imshow('img',img)
# print(img.shape)


#（2）彩色转灰度：灰度化处理
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print(gray.shape)
cv2.imshow('gray', gray)


#（3）二值化处理：这里不需要，但是流程中有这一步 *************** 怎么把背景变成黑色,物品变成白色,这是最难的
t, im_bin  = cv2.threshold(gray,
                           127, #阈值
                           255, #最大值
                           cv2.THRESH_BINARY #二值化
                           )
# print(t)
cv2.imshow('THRESH_BINARY', im_bin)


#（4）查找轮廓
cnts,hierarchy=cv2.findContours(im_bin,
                                          cv2.RETR_EXTERNAL,    #只检测外轮廓
                                          cv2.CHAIN_APPROX_NONE #存储所有的轮廓点
                                          )
print(len(cnts))
for cnt in cnts:
    print(cnt.shape)



#（5）绘制轮廓
res = cv2.drawContours(img,          # 在哪个图画:注意:这种方式会在原图画,修改原图
                       cnts,         # 要画的轮廓坐标点
                       -1,           # 轮廓索引
                       (0,0,255),    # 颜色
                       -1            # 线条粗细,单位:px  ,-1表示用实心画
                       )
cv2.imshow('res', res)

cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口

