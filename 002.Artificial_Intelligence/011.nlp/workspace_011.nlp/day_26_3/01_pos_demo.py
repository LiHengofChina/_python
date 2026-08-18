

import jieba.posseg as psg
'''
———————————————— 标记词性 
jieba

'''

def pos(text):
    results = psg.cut(text)  # 分词，记性标注

    # pair 对象不能解包，用 word/flag 取词和词性
    for item in results:
        print("%s/%s" % (item.word, item.flag), end=" ")
    print("")

text = "梅兰芳大剧院周六晚上有演出"
pos(text)


