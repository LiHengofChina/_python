'''
用python代码实现  “逻辑与”  和  “逻辑或”
通过 "感知机" 来实现 "逻辑与、逻辑或"

'''

def AND(x1,x2):
    '''
    逻辑与
    '''
    w1,w2 = 0.5,0.5
    theta = 0.7   #只有这个参数不同
    temp = w1* x1 + w2 * x2
    if temp <= theta:
        return 0
    else:
        return 1
print(AND(1,1)) #1
print(AND(1,0)) #0
print(AND(0,1)) #0
print(AND(0,0)) #0

def OR(x1,x2):
    '''
    逻辑或
    '''
    w1,w2 = 0.5,0.5
    theta = 0.3        #只有这个参数不同
    temp = w1* x1 + w2 * x2
    if temp <= theta:
        return 0
    else:
        return 1
print(OR(1,1)) #1
print(OR(1,0)) #1
print(OR(0,1)) #1
print(OR(0,0)) #0