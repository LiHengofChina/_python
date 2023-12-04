
'''

04_subtract.py
圖像減法：
        對應樸素值相減
'''

import cv2

#（1）加載圖片
img3 = cv2.imread('../data/3.png', 0 )
img4 = cv2.imread('../data/4.png',0 )
cv2.imshow('img3',img3)
cv2.imshow('img4',img4)

sub3_4 = cv2.subtract(img3,img4)
cv2.imshow('sub3_4',sub3_4)

sub4_3 = cv2.subtract(img4,img3)
cv2.imshow('sub4_3',sub4_3) #全黑：因為負數變成了0


cv2.waitKey()  # 等待用户敲击按键。
cv2.destroyAllWindows()  # 销毁所有窗口
