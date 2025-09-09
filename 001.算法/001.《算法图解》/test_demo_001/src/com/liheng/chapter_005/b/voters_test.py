#encoding=utf-8

#防止重复，投票

def test(name,voted):
    
    if(voted.get(name)):
        print("踢他出去")#kick them out
    else:
        voted[name] = True
        print("让他投")#let them vote


if __name__ == "__main__":
    voted = {}
    test("tome",voted)
    test("mike",voted)
    test("mike",voted)
    
    
    