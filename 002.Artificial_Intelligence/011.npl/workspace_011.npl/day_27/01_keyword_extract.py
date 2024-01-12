
import math
import jieba
import jieba.posseg as psg
# from gensim import corpora, models
from jieba import analyse
import functools
import numpy as np

'''

—————————————————————————————— 提取关键词
        （1） TF-IDF 算法
        （2） TextRank 算法


corpus.txt          //语料库
stopword.txt        //停用词表

'''


# 读取停用词表

#读取停用词表
def get_stopword_list():
    with open("kw_extract_data/stopword.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    stopwords = [w.replace("\n", "") for w in lines]
    return stopwords

#过滤停用词
def word_fileter(seg_list): # seg_list 是分词后的列表
    filter_list = [] #过滤后的列表
    for word in seg_list: #遍历每个词
        if  word not in stopword_list and len(word) > 1:
                filter_list.append(word)
    return filter_list

#读取语料库
def load_data(corpus_path):
    doc_list = [] #文档列表
    with open(corpus_path,"r",encoding="utf-8") as f:
        for line in f.readlines():
            seg_list = jieba.cut(line.strip()) #分词
            filter_list = word_fileter(seg_list) #过滤停用词
            doc_list.append(filter_list) #添加到文档列表
    return doc_list

# 计算IDF值
def train_idf(doc_list):
    idf_dict = {}             # key:词  value:idf
    tt_count = len(doc_list)  # 总文档数量

    # 先统计每个词在多少个文档中出现过
    for doc in doc_list:
        doc_set = set(doc)  #将词列表推入集合去重
        for word in doc_set: #取出每个词
            if word in idf_dict.keys():#在字典中
                num = idf_dict[word]
                idf_dict[word] = num + 1
            else: #该词第一次出现
                idf_dict[word] = 1
    # 计算IDF
    for word,doc_cnt in idf_dict.items():
        idf_dict[word] = math.log(tt_count / (doc_cnt + 1.0 ) )

    #对于 在语料库中从未出现过的词，计算一个默认的IDF值
    default_iodf = math.log(tt_count / 1.0)

    return idf_dict, default_iodf

class TfIdf(object): #TF-IDF类
    def __init__(self,
                idf_dict,
                default_idf,
                word_list,
                kw_num):
        self.word_list = word_list
        self.idf_dict = idf_dict
        self.default_idf = default_idf
        self.kw_num = kw_num
        self.tf_dict = self.get_tf_dict()  # 计算词频

    def get_tf_dict(self):  # 计算词频
        tf_dict = {}  # key:词     value:词频
        for word in self.word_list:
            if word in tf_dict.keys():  # 在字典中
                num = tf_dict[word]
                tf_dict[word] = num + 1  # 数量+1
            else:
                tf_dict[word] = 1

        total = len(self.word_list)  # 词语总数
        for word, word_cnt in tf_dict.items():
            tf_dict[word] = float(word_cnt) / float(total)

        return tf_dict

    def get_tfidf(self):
        tfidf_dict = {} #key:词  value:TF-IDF
        for word in self.word_list:
            idf = self.idf_dict.get(word, self.default_idf)
            tf = self.tf_dict.get(word, 0)

            tfidf = tf * idf
            tfidf_dict[word] = tfidf

        # 根据TF-IDF值排序
        sorted_list = sorted(tfidf_dict.items(),  # 待排序对象
                             key=lambda x: x[1],  # 排序依据
                             reverse=True         # 倒序排序
                             )

        for k, v in sorted_list[0:self.kw_num]:
            print(k + ", ", end="")
        print("")



#
def tfidf_extract(word_list, kw_num=20):
    doc_list = load_data("kw_extract_data/corpus.txt")  # 读取语料库
    idf_dict, default_idf = train_idf(doc_list)  # 计算IDF

    tfidf_model = TfIdf(idf_dict, default_idf, word_list, kw_num)
    tfidf_model.get_tfidf()

# TextRank
def textrank_extract(text, keyword_num=20):
    keywords = analyse.textrank(text, keyword_num)
    # 输出抽取出的关键词
    for keyword in keywords:
        print(keyword + ", ", end='')
    print()


if __name__ == '__main__':
    global stopword_list

    text = """在中国共产党百年华诞的重要时刻，在“两个一百年”奋斗目标历史交汇关键节点，
    党的十九届六中全会的召开具有重大历史意义。全会审议通过的《决议》全面系统总结了党的百年奋斗
    重大成就和历史经验，特别是着重阐释了党的十八大以来党和国家事业取得的历史性成就、发生的历史性变革，
    充分彰显了中国共产党的历史自觉与历史自信。"""

    # 读取停用词表
    stopword_list = get_stopword_list()
    seg_list = jieba.cut(text)  # 分词
    filter_list = word_fileter(seg_list)  # 过滤停用词

    # （1）TF-IDF提取关键词
    print("TF-IDF提取结果：")
    tfidf_extract(filter_list)

    # （1）TextRank提取关键词
    print('\n TextRank模型结果：')
    textrank_extract(text)


