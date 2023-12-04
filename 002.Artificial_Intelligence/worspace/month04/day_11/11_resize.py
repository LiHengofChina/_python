'''


缩放: 放大和缩小
    即能放大，也能缩小


'''

import cv2


img = cv2.imread('../data/lena.jpg')
cv2.imshow('imread', img)
h, w = img.shape[:2] #切片


#缩小
dst_size = ( int(w/2) , int(h/2) )
reduce = cv2.resize(img, dst_size)
cv2.imshow("reduce",reduce)


#放大  # 默认：双线性插值法 ，精度低
dst_size = (w*2, h*2)
res = cv2.resize(img, dst_size)
cv2.imshow("res",res)



#放大2  # 最邻近插值法 ，精度低
dst_size = (w*2, h*2)
near = cv2.resize(img,
                  dst_size,
                  interpolation=cv2.INTER_NEAREST #最邻近插值法
                  )
cv2.imshow("near",near)



cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口

