'''

图像的对应位置的像素值相加，

---按照权重进行相加
    并保证
    两张相加的图像的尺寸shape要一致

'''

import cv2

#（1）加載圖片
lena = cv2.imread('../data/lena.jpg', 0 )
lily = cv2.imread('../data/lily_square.png',0 )
cv2.imshow('lena',lena)
cv2.imshow('lily',lily)


#（2）相加-按照權重
add = cv2.addWeighted(lena, 0.8, lily, 0.2, # 0.8 +0.2 =1，可以不為1，可以為1，一般為1，好計算
                      100 #亮度調節值 ，正數，增加亮度，負數減小亮度。
                      )
cv2.imshow("add", add)

cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口
