#coding=utf-8

#找出列表中最大的数字。

#TODO


def my_max(list):
    if len(list) == 2 :
         return list[0] if list[0] > list[1] else list[1]
    sub_max = max(list[1:])
    return list[0] if list[0] > sub_max else sub_max

if __name__ == "__main__":
    print(my_max([2 ,31 ,6 ]))
    
    

 