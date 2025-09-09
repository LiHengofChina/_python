
#encoding=UTF-8


def test():
    graph = {}
    graph["you"] = {"alice","bob","claire"} 



    graph["bob"] = ["anuj", "peggy"]
    graph["alice"] = ["peggy"]
    graph["claire"] = ["thom", "jonny"]
    graph["anuj"] = []
    graph["peggy"] = []
    graph["thom"] = []
    graph["jonny"] = []
    name = "Python语言程序设计课程"
    print(name[2:-2])
    

if __name__ == "__main__":
    test()

