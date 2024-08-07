'''

【AI_Studio】执行

利用 “中文维基百科语料库”训练词向量

'''
#####################################################################【1】安装gensim
# !pip install gensim==3.8.1 #


#####################################################################【2】 由于wiki数据量太大，我们只读取2万笔数据

import codecs

from gensim.corpora import WikiCorpus

# 这个是中文维基百科语料库，压缩版本它有1.8G左右，太大了，我们只取2万条来训练
inupt_file = 'data/data104767/articles.xml.bz2'

# 从里面取2万条之后，生成到一个新的文件中
out_file = open('data/data104767/wiki.zh.text', 'w', encoding='utf-8')


#WikiCorpus对象 从指定文件中提取文本
wiki = WikiCorpus(inupt_file,  # 输入文件
                  lemmatize=False,  # 词形还原（lemmatization），中文没有记形，在英文文本处理中，词形还原是将词汇还原为其基本形式的过程，
                  dictionary={})


count = 0
for text in wiki.get_texts():
    out_file.write(' '.join(text) + '\n')  # 写入一行
    count += 1
    if count % 200 == 0:
        print('数据量：', count)

    if count >= 20000:  #只读取2万笔数据
        break

out_file.close()

####################################################################【3】生成 分词文件


import jieba
import jieba.analyse
import codecs # python封装的文件工具包
def precoss_wiki_text(src_file,dst_file):
    #同时打开 两个文件
    with codecs.open(src_file, 'r', 'utf-8') as f_in, \
         codecs.open(dst_file, 'w', 'utf-8') as f_out:

         num = 1
         for line in f_in.readlines():
             line_seg = ' '.join(jieba.cut(line))  # 分词后的结果
             f_out.writelines(line_seg)
             num += 1

             if num % 200 == 0:
                 print('处理数据完成：',num)

precoss_wiki_text('data/data104767/wiki.zh.text', 'data/data104767/wiki.zh.text.seg')


####################################################################【4】训练，使用gensim库训练Word2Vec模型
import logging
import sys
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence # 按行读取

logger = logging.getLogger(__name__)
# format: 指定输出的格式和内容，format可以输出很多有用信息，
# %(asctime)s: 打印日志的时间
# %(levelname)s: 打印日志级别名称
# %(message)s: 打印日志信息
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

in_file = "data/data104767/wiki.zh.text.seg" # 输入文件(经过分词后的)
out_file1 = "data/data104767/wiki.zh.text.model" # 模型
out_file2 = "data/data104767/wiki.zh.text.vector" # 权重

# 模型训练
model = Word2Vec(LineSentence(in_file), # 输入
                 size=100, # 词向量维度(推荐25~300之间)
                 window=3, # 窗口大小
                 min_count=5, # 如果语料中单词出现次数小于5，忽略该词，最低词频
                 # ,seg=0 #1=CBOW,0=Skip-gram
                 workers=multiprocessing.cpu_count()) # 线程数量
# 保存模型
model.save(out_file1)
# 保存权重矩阵
model.wv.save_word2vec_format(out_file2, # 文件路径
                              binary=False) # 不保存二进制

print('模型保存成功')

####################################################################【5】预测：给定一个词找到一个相似的词
import gensim
from gensim.models import Word2Vec

# 加载模型
model = Word2Vec.load("data/data104767/wiki.zh.text.model")
count = 0

for word in model.wv.index2word:
    print(word, model[word]) # 打印
    count += 1
    if count >= 10:
        break

print("==================================")

result = model.most_similar(u"铁路")
for r in result:
    print(r)

print("==================================")

result = model.most_similar(u"中药")
for r in result:
    print(r)
