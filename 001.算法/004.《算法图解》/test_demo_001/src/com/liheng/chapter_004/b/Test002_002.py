#coding=utf-8

# 编写一个递归函数来计算列表包含的元素数。 python 版

def my_count(list):
    if list == []:
        return 0
    return 1 + my_count(list[1:])  # list[1:]  从脚标1 开始往后截取。
 

if __name__ == "__main__":
    print(my_count([2 ,3 ,6 ]))
 
    