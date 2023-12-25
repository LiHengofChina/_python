# 人脸（水果）识别示例：数据预处理
import paddle.fluid as fluid
import os
import json
from global_var import *

name_data_list = {}  # 记录每个人多少张训练图片、多少张测试图片


def get_file_lines(file_path, type):  # 获取文件行数
    with open(file_path) as f:
        i = 0
        for line in f.readlines():
            line = line.strip().replace("\n", "")
            tmp = line.split("\t")
            if len(tmp) < 2:
                continue
            else:
                if int(tmp[1]) == type:
                    i += 1
    return i


def save_train_test_file(path, name):
    if name not in name_data_list:  # 未在字典中
        img_list = []
        img_list.append(path)  # 将图片添加到列表
        name_data_list[name] = img_list  # 存入字典
    else:  # 已经在字典中
        name_data_list[name].append(path)  # 加入


# 获取所有类别保存的文件夹名称
dirs = os.listdir(data_root_path)
for d in dirs:
    full_path = os.path.join(data_root_path, d)  # 完整路径

    if os.path.isdir(full_path):  # 目录
        full_path = os.path.join(full_path, "Imgs")
        imgs = os.listdir(full_path)
        for img in imgs:
            # print(img + "," + d)
            save_train_test_file(os.path.join(full_path, img), d)
    else:  # 文件
        pass

# 清空数据文件
with open(test_file_path, "w") as f:
    pass
with open(train_file_path, "w") as f:
    pass

for name, img_list in name_data_list.items():
    i = 0
    num = len(img_list)
    print("%s: %d张" % (name, num))

    for img in img_list:
        if i % 10 == 0:  # 每10笔取一笔测试数据
            with open(test_file_path, "a") as f:
                line = "%s\t%d\n" % (img, name_dict[name])
                # print(line)
                f.write(line)
        else:  # 其它作为训练数据
            with open(train_file_path, "a") as f:
                line = "%s\t%d\n" % (img, name_dict[name])
                # print(line)
                f.write(line)
        i += 1

print('生成数据列表完成！')
