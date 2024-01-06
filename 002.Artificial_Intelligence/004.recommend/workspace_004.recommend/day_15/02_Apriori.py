'''


协同过滤推荐==>关联规则==>Apriori


（自己用代码实现）

'''


def loadData():
    with open('./item.txt','r') as f:
        data = f.readlines()
        res = []
        for i in data:
            res.append(i.strip().split(','))
        return res


def createC1(dataSet):
    '''
    遍历每一项的每个商品保存越来就可以了。
    '''

    C1 = []
    for transation in dataSet:
        # transation 表示每一条购买记录
        for item  in transation:
            if [item] not in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1)) #让每一个项是一个固定的集合，方便K项集判断是否包含
                                    #[{‘物品1’},{‘物品2’},{‘物品3’}]  列表套集合


def scanD(D, Ck, min_support):
    '''
    生成频繁项集
    :param D:           [{xx,xx,xx},{xx,xx},...]
    :param Ck:          [{xx}]
    :param min_support:
    :return:
    '''
    ssCnt = {}

    for tid in D:
        for can in Ck:
            if can.issubset(tid): #判断 "候选集中的项集" 是不是 "购买记录的子集"
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1


    #计算支持度
    numItems = float(len(D))

    # 遍历候选集中每一项出现的次数
    retList = []        #保存频繁项集
    supportData = {}    #记录每一项的支持度
    for key in ssCnt:
        support = ssCnt[key] / numItems  #  出现次数 / 总数
        if support >= min_support:       #   过滤最小支持度
            retList.insert(0,key)
        supportData[key] = support

    return retList,supportData


def aprioriGen(Lk, k):
    '''
    根据上一个项集的 "频繁项集" 生成下一个项集的 "候选项集"
    :param Lk: k-1 项的 "频繁项集"
    :param k : 新的候选项集的个数
    :return: k 项集的候选项集
    针对 “1项集”，它里面只有一个物品，所以它可以直接组成生成2项级
    但是针对  ”2项集“ 生成 ”3项集“时，两个组合之间，必须要有一个是相同的才可以。
    ”3项集“生成 ”4项集“ 必须要有两个相同的
    ”4项集“ 生成 "5项集" 必须要有4个相同的

    求 ”它们的交集“ 就是相同的部分，求 ”它们的交集“ 的元素个数。
    '''
    retList = []
    for i in range(len(Lk) - 1):
        for j in range(i + 1, len(Lk)):
            if len(Lk[i] & Lk[j]) == (k-2): #交集
                retList.append(Lk[i] | Lk[j])
    retList = list(set(retList)) #转集合转列表，去重复
    return retList #返回 ”候选项集“

def apriori(dataSet,min_support):

    #根据  “样本数据”  生成  “1项集的候选集”
    C1 = createC1(dataSet)


    #原始数据集合
    D = list(map(frozenset,dataSet))
    # print(D)

    #过滤 ”最不支持度“，得到频繁项集
    L1,supportData = scanD(D, C1, min_support)


    L = [L1] #存放每一个项集的 "频繁项集"
    k = 2    # 要生成下一个项集的个数


    #根据上一个项集的 "频繁项集" 生成下一个项集的 "候选项集"
    while len(L[k-2]) > 0:  #上一个频繁项集的项大于0，才循环
        Ck = aprioriGen(L[k-2],k) #拿到k项集的候选项集
        #计算支持度，进行最小支持度过滤

        Lk,supK = scanD(D,Ck,min_support)

        L.append(Lk)

        supportData.update(supK)

        k+=1

    return L,supportData





if __name__ == '__main__':
    dataSet = loadData()


    L,sup_data = apriori(dataSet,min_support=0.5)#主逻辑函数
    for i in L:
        print(i)
    # for i, j in sup_data.items():
    #     print(i, ';', j)
