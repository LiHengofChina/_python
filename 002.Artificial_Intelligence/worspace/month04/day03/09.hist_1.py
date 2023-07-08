import cv2
'''
以灰度方式查看图片像素分布
'''
# img = cv2.imread('./tmp/lena.jpg')
img = cv2.imread('./tmp/lena.jpg', 0)
cv2.imshow('img', img)

#打印出来是二维数组
print(img)
print(type(img))
print(img.shape)
print(img.size)
print(img.min()) #最小值
print(img.max()) #最大值



cv2.waitKey()
cv2.destroyWindow()
