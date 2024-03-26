

import jieba.posseg as psg
'''
———————————————— 标记词性 
jieba

'''

def pos(text):
    results = psg.cut(text)  # 分词，记性标注
    for w, t in results:
        print("%s/%s" % (w, t), end=" ")
    print("")

text = "梅兰芳大剧院周六晚上有演出"
pos(text)


