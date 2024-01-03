'''
第三方jie库实现分词
'''
import jieba

text = "吉林市长春药店"
#(1)精确模式
seg_list = jieba.cut(text,#待分词文本
                     cut_all=False #是否使用全模式
                     )
print(type(seg_list)) #返回生成器对象
for word in seg_list:
    print(word, end='/')
print('\n')

#(2)全模式
seg_list = jieba.cut(text,#待分词文本
                     cut_all=True #是否使用全模式，凡是可以成词的都会分割成词
                     )
print(type(seg_list)) #返回生成器对象
for word in seg_list:
    print(word, end='/')
print('\n')

#(3)搜索引擎模式，在精确模式基本之上，再次切分
seg_list = jieba.cut_for_search(text)
for word in seg_list:
    print(word, end='/')
print('\n')


