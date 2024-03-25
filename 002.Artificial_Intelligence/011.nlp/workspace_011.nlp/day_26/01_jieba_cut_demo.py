
import jieba

'''
————————————————  分词

'''
text = "吉林市长春药店"

seg_list = jieba.cut(text,#待分词文本
                     cut_all=False)#全模式：否
print(type(seg_list)) # 打印返回值类型
for word in seg_list:
    print(word, end="/")
print("")

seg_list = jieba.cut(text,#待分词文本
                     cut_all=True)#全模式：是
for word in seg_list:
    print(word, end="/")
print("")

seg_list = jieba.cut_for_search(text)#搜索引擎模式
for word in seg_list:
    print(word, end="/")



