#coding=utf-8

def my_sum(list):
    if list == []:
        return 0
    return list[0] + my_sum(list[1:])  # list[1:]  从脚标1 开始往后截取。
 

if __name__ == "__main__":
    print(my_sum([2 ,3 ,6 ]))
 
