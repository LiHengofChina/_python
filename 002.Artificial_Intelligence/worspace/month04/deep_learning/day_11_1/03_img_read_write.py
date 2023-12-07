'''
图像：读取、显示、保存
    # 说明：
        （1） 图像在内存中是 "数组" ，ndarray，多维数组
        （2） #216行 、160列、3个通道

        （3） imshow 是非阻塞函数。

        （4）  三种等待方式
              #等待用户敲击按键。
              cv2.waitKey()

              #等待用户敲击按键 或 5秒以后
              cv2.waitKey(5000)

              #按下esc才退出
              while True:
                key  = cv2.waitKey(5000)  #
                if key == 27:
                    break



'''
import cv2
im = cv2.imread('../../data/Linus.png')
                #路径中不能有中文

print(type(im)) #<class 'numpy.ndarray'>
                # numpy 里面的数组类型


print(im.shape)  #(216, 160, 3)
                 #216行 、160列、3个通道
print(im)


cv2.imshow('TestImg', #名字不能重复
          im)




#保存图像：
cv2.imwrite("../../data/Linus_new.png", im)


# cv2.waitKey() #等待用户敲击按键。

# cv2.waitKey(5000)  #

while True:
    key  = cv2.waitKey(5000)  #
    if key == 27:
        break

cv2.destroyAllWindows()  #销毁所有窗口


