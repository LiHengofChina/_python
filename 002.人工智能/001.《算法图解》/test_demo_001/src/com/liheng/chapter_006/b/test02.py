

#encoding=UTF-8

from collections import deque

# 假设：这个函数检查人的姓名是否以m结尾：如果是，
# 他就是芒果销售商。
def person_is_seller(name):
    return name[-1] == 'm'

def test():

    #定义图
    graph = {}
    graph["you"] = {"alice","bob","claire"}
    
    graph["bob"] = ["anuj", "peggy"]
    graph["alice"] = ["peggy"]
    graph["claire"] = ["thom", "jonny"]
    graph["anuj"] = []
    graph["peggy"] = []
    graph["thom"] = []
    graph["jonny"] = []
    
    
    #实现算法
    #创建队列
    search_queue =  deque()
    
    #字典中的key给这个队列
    search_queue += graph["you"]
    
    while search_queue:
        
        person = search_queue.popleft()     #从队列中取出一个元素

        if person_is_seller(person):   #判断是不是盲果商人
            print(person + " is a mango seller! ")
            return True
        else:
            search_queue += graph[person]   #不是芒果销售商。将这个人的朋友都加入搜索队列
    return False    #如果到达了这里，就说明队列中没人是芒果销售商

if __name__ == "__main__":
    test()

