import math

import pandas as pd
import numpy as np

'''
    ICF ，数据量太大， 取1000行放在一小文件中。
    
    
    
'''
class ItemCF:
        #初始化对象
    def __init__(self,data_file):
        self.data_file = data_file
        self.readData() #读取数据

    #加载数据
    def readData(self):
        #用一个字典套字典的方式存储
        # {
        #   user:{item:score,item:score},
        #   user:{item:score,item:score},
        #   ...
        # }
        # 哪个用户看了哪个电影，对哪个电影打了多少分
        self.data = {}
        for line in open(self.data_file):
            user,item,score,time = line.strip().split(',') #对每一行数据处理，strip()去掉第一行的结束
            self.data.setdefault(user, {})#必须设置默认值，防止覆盖
            #添加数据
            self.data[user][item] = int(score)

    #计算：物品相似度
    def ItemSimlarity(self):
        ######################################## 构建数据
        C = {}
        '''
            记录物品与物品 "共同出现的矩阵"，也就是共现矩阵
            {
            电影1：{电影2：次数，电影3：次数}
            电影2：{电影1：次数，电影3：次数}
            电影3：{电影1：次数，电影2：次数}
            .....
            }
        '''
        N = {}
        '''
            每个物品 "单独出现的次数"，每个电影单独出现了几次
            {电影1：次数}
        '''
        for user,items in self.data.items():  # data.items() 为：user:{item:score,item:score},
                                              # 用户 和 每个电影的评分
            for i in items.keys(): #遍历当前用户看过的所有电影， i 表示电影
                N.setdefault(i,0)  #，没值才设置为0，有值不会设置
                N[i]  += 1         #电影每出现一次 加一次，N = {}统计每个电影单独出现 的次数

                C.setdefault(i, {}) #也给C设置默认值，防止它覆盖，
                                    # {}表示：i这个电影和其它每个电影共同出现的次数
                #再次遍历 “当前用户看过的所有电影”
                for j in items.keys():
                    if i == j:  #如果 "是自己" 则不记录，因为要记录和 "其它电影"，共同出现的次数
                        continue
                    #到这里说明这个电影不是自己，但是它(j)和(i)共同出现在了user用户的目录中。
                    C[i].setdefault(j,0) #给C[i]也设置默认值，防止它覆盖
                    C[i][j] += 1    #

        ######################################## 计算相似度
        #计算相似度
        self.W = {}
        '''
            记录电影与电影品 "相似度"，使用和"共现矩阵"类似的格式：
            当 “前这部电影” 和 “其它每部电影单独” 的相似度
            {
            电影1：{电影2：相似度，电影3：相似度}
            电影2：{电影1：相似度，电影3：相似度}
            电影3：{电影1：相似度，电影2：相似度}
            .....
            }
        '''
        for i,related_items in C.items(): # C.items()里面是共现矩阵，如：电影1：{电影2：次数，电影3：次数}
            self.W.setdefault( i, {} ) #设置默认值
            #遍历 “i物品” 和  “其它物品”的 “共同出现的次数”
            for j,cij in related_items.items():
                #余弦相似度
                self.W[i][j] = cij / (math.sqrt( N[i] * N[j] ))  #共同出现次数 / sqrt(（单独出现次数） *(单独出现次数）)
        return self.W


    #计算推荐列表：
    def Recommend(self,user,K=3,N=10):
        '''

        :param user: 给谁推荐
        :param K: 推荐相似度最高的K个商品
        :param N: 推荐分最高的N部电影，默认是10
        :return:
        '''

        rank = {}
        action_item = self.data[user] #拿到 ”指定用户“ 看过的 ”所有电影“
        for item,score in action_item.items(): #遍历行为商品，找到和行为商品相似度比较高的商品
                                               #遍历 "这个用户看过的所有电影"，找到与 ”这此电影“ 相似度高的电影
                                               # score 是用户 "对已经看过的电影item" 的打分

            for j, wj in sorted(self.W[item].items(),
                                key=lambda x: x[1],
                                reverse=True)[0:K]:  # 从 "相似度矩阵" 拿到最相似的3个电影
                                                     # 先拿到 ”这部电影“ 与 ”所有电影“ 的相似度值，从大到小排序，截取K个值。
                if j in action_item.keys():#排除这个当前用户已经看过的。
                    continue

                rank.setdefault(j,0)
                rank[j] += score * wj  # score 是用户 "对已经看过的电影item" 的打分
                                       # 当前这部电影j 与 ”已经看过的电影item“ 相似，相似度是wj，
                                       # 所以：wj * score 就是当前这部电影j的推荐分。
                                       # 多部分电影都与部电影相似，所以是+=号


        return dict(sorted(rank.items(), #列表套元祖
                      key=lambda x:x[1], #根据推荐值排序
                      reverse=True #倒序
                      )[0:N]) #推荐分最高的前N个商品


if __name__ == '__main__':
    # 实例化
    icf = ItemCF('../../data_test/movielens电影数据/data.cvs')

    icf.ItemSimlarity()

    res = icf.Recommend('3')
    for k,v in res.items():
        print('推荐电影：{}，推荐分：{}'.format(k,v))




