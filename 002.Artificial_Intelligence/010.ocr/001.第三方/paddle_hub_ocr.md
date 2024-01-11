# 利用PaddleHub实现中文OCR

## 1. 安装库命令

```bash
!pip install paddlehub==1.6.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
!hub install chinese_ocr_db_crnn_server==1.0.0
!pip install shapely
!pip install pyclipper
```



## 2. Paddle代码

```python
import paddlehub as hub
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img_list = ['ticket.jpg']
ocr = hub.Module(name="chinese_ocr_db_crnn_server")
# result = ocr.recognize_text(images=[cv2.imread('./book1.png')])
result = ocr.recognize_text(paths=img_list) # 这种写法也可以
print(result)

print("\n=========================  开始解析结果 ==========================\n")

result_dict = dict(result[0])
rects = []

words = result_dict["data"]
for word in words: # word为字典，result
    print(word["text"])
    print(word["confidence"])

    points = word["text_box_position"]
    # print(points)
    rects.append(points) # 添加到列表

# 在原图上绘制矩形
im = cv2.imread(img_list[0], 1)
for rect in rects:
    p1 = (rect[0][0], rect[0][1])
    p2 = (rect[1][0], rect[1][1])
    p3 = (rect[2][0], rect[2][1])
    p4 = (rect[3][0], rect[3][1])
    cv2.line(im, p1, p2, (0, 0, 255), 2)
    cv2.line(im, p2, p3, (0, 0, 255), 2)
    cv2.line(im, p3, p4, (0, 0, 255), 2)
    cv2.line(im, p4, p1, (0, 0, 255), 2)

cv2.imwrite("ticket_result.jpg", im)
```

