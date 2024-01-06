

import pandas as pd
import numpy as np
'''

协同过滤推荐==>基于内存/邻域==>UCF

        找到登陆用户的相似用户，
        再找到 "登陆用户的相似用户" 看过我的电影，
        判断并记录登陆是否看过，以及打分和相似度。
        最后用打印 * 相似度 得到推荐分

        电影推荐

'''

ratings = pd.read_json('../data_test/ratings.json')
# print(ratings)


# （1）确定用户：向 Michael Henry 用户推荐
login_user = 'Michael Henry'

# （2）使用 皮尔逊相关系数，看看哪个用户和它比较像 #
# ratings.corr() # 拿到每列与每列的相关系统：ratings.corr()
# print(ratings.corr()) #这样打印出来，"每列" 与 "每列" 的皮尔孙相关系数
sim_mat = ratings.corr()

# （3）登陆用户的 "皮尔逊相关系数"
sim_scores = sim_mat[login_user]
# print(sim_scores)

# （4）使用掩码数组来索引：只拿  “强相关” 的用户 >= 0.6
sim_scores = sim_scores[sim_scores >= 0.6]
# print(sim_scores)

# （5）排除自己
sim_scores = sim_scores.drop(login_user)
# print(sim_scores)


# {‘电影A’:[[打分],[相似度]]}
rec_movies = {}
# （6）遍历相似用户看过的电影
for sim_user, sim_scores in sim_scores.items():
    sim_movies = ratings[sim_user].dropna()  # dropna 去掉 NaN 数据
    # 遍历相似用户看过的：每一个电影，判断当前电影登陆用户是否看过
    for m, s in sim_movies.items():
        if np.isnan(ratings[login_user][m]):
            # 记录相似用户的打分 和 相似度
            if m not in rec_movies.keys():
                rec_movies[m] = [[], []]
            rec_movies[m][0].append(s)
            rec_movies[m][1].append(sim_scores)

# print(rec_movies)

rec_dic = {}
# （7）然后使用打分 和 相似度做加权均值，谁的分越高，就推荐谁
for i in rec_movies:
    rec_val = np.sum(np.array(rec_movies[i])[0] * np.array(rec_movies[i])[1])
    rec_dic[i] = rec_val
# print(rec_dic)
# print(rec_dic.items())  # 列表套元组

# （8）排序 （字典），先排完序，再把列表套元组转回去。
res = dict(sorted(rec_dic.items(),
                  key=lambda x: x[1],
                  reverse=True))

print(res)
