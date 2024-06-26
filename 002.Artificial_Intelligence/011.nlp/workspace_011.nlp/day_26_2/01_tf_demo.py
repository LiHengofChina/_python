
import jieba

'''
———————————————— 统计 "文章词频" 示例：
先分词，再统计词频。

'''

#读取文件内容

def get_content(path):
    with open(path,"r",encoding="utf-8") as f:
        content = "" #文件内容
        for line in f.readlines():
            line = line.strip()#去空格
            content += line
    return content

# def get_content(fname):
#     with open(fname, 'r', encoding='utf-8') as f:  # 指定以UTF-8编码方式打开文件
#         return f.read()  # 返回文件的全部内容


#统计词频，打印出现次数最多的前k个词
def get_tf(words, topk=10):
    tf_dict = {}  # key:词，value：出现次数
    for w in words:  # 遍历每个词
        if w not in tf_dict.keys():  # 该词首次出现
            tf_dict[w] = 1  # 次数设置为1
        else:  # 已经出现过了
            num = tf_dict[w]
            tf_dict[w] = num + 1  # 次数+ 更新回去

    #根据value对字典倒序排列
    sorted_list = sorted(tf_dict.items(),  # 待排序对象
                         key=lambda x: x[1],  # 排序依据
                         reverse=True  # 倒序
                         )
    return sorted_list[0:topk] #返回前K个元素

#去除停用词表
def get_stop_words(path):
    with open(path,encoding="utf-8") as f:
        return [ln.strip() for ln in f.readlines()]




if __name__ == '__main__':
    fname = "input.txt"  # 待统计文件
    corpus = get_content(fname)  # 读取文件内容


    tmp_list = list(jieba.cut(corpus)) #分词

    # 过滤停用词表
    stop_words = get_stop_words("stop_words.utf8")
    split_words = []  # 过滤后的词列表
    for w in tmp_list: #取出每个词
        if w not in stop_words: #不是停用词，添加到列表
            split_words.append(w)
        else: #是停用词，丢弃
            continue

    print("分词结果：\n" + "/".join(split_words))

    tf_list = get_tf(split_words)
    print("\nTop_k词:", str(tf_list))

    result = ((1/3 * 1/6 ) + (1/3 * 1/4 ) + (1/3 * 1/8 ) ) * ((1/3 * 1/6 ) + (1/3 * 0 ) + (1/3 * 1/8 )) * ((1/3 * 0 ) + (1/3 * 0 ) + (1/3 * 1/8 ))
    print(result)

