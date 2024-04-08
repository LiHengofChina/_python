#【1】
################# 上传数据集#############################################################################


#【2】
################# 数据预处理##############################################################################
################# （这段代码，可以本机运行，但是为了目录方便，还是在AIStudio上面运行）#############################

#每个中文转换成数值类型，并划分训练集和测试集

'''
    中文新闻资讯分类 ———————————————— 根据 "亲闻标题"
    模型：文本卷积神经网络 TextCNN ，这里设计为 "字符级别" 模型


'''

data_root = 'data/news_classify/'
data_file = 'news_classify_data.txt'
train_file = 'train_list.txt'  #训练集
test_file = 'test_list.txt'    #测试集
dict_file = 'dict_txt.txt'     #编码字典文件,每一个汉字对应的数值
                                #在"字符级别" 工作，所以{'灯': 1, '茬': 2, '援': 3, '懦': 4,}


#拼接路径
data_file_path = data_root + data_file
train_file_path = data_root + train_file
test_file_path = data_root + test_file
dict_file_path = data_root + dict_file

#生成编码字典文件：把每一个字编码成唯一的数字，存入字典中
def create_dict():

    dict_set = set()#定义一个空集合
    with open(data_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    #遍历每一行
    for line in lines:
        title = line.split('_!_')[-1].replace('\n', '')

        #遍历每一个字
        for w in title:
            dict_set.add(w) #把所有字加入了集合了

    # print(len(dict_set))#4733

    # 遍历集合中的每个文字，分配一个编码
    i = 1
    dict_list = []
    for s in dict_set:
        dict_list.append([s, i])
        i += 1
    dict_txt = dict(dict_list)  # 转字典
    end_dict = {'<unk>': i}  # 有可能要预测的字，在这测试集没有，所以再加一个key vale
    dict_txt.update(end_dict)

    # 将字典对象写入到文件中
    with open(dict_file_path, 'w', encoding='utf-8') as f:
        f.write(str(dict_txt))
    print('字典文件生成完成')



#利用上面的字典，对 "一行标题" 进行编码。
def line_encoding(title, dict_txt, label):
    new_line = ''
    for w in title:
        if w in dict_txt:
            code = str(dict_txt[w])
        else:
            code = str(dict_txt['<unk>'])
        new_line = new_line + code + ','
    new_line = new_line[:-1]  # 去掉最后一个逗号

    # 编码结果\t类别
    new_line = new_line + '\t' + label + '\n'
    return new_line

# 对原始数据进行编码，将编码之后的结果存入到训练集和测试集中

def create_data_list():

    #创建文件
    with open(train_file_path, 'w') as f:
        pass
    with open(test_file_path, 'w') as f:
        pass

    #打开字典编码文件，读取出编码字典
    with open(dict_file_path, 'r', encoding='utf-8') as f:
        dict_txt = eval(f.readlines()[0])

    #打开原始的样本数据，取出标题部分进行编码
    with open(data_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    #遍历每个样本，取出标题和类别
    i = 0 #样本索引
    for line in lines:
        words = line.replace('\n', '').split('_!_')
        title = words[3]  # 标题
        label = words[1]  # 类别

        new_line = line_encoding(title, dict_txt, label)
        if i % 10 == 0: #写入到测试集
            with open(test_file_path, 'a', encoding='utf-8') as f:
                f.write(new_line)
        else:
            with open(train_file_path, 'a', encoding='utf-8') as f:
                f.write(new_line)

        i += 1
    print('编码完成，划分训练集和测试集完成！')




create_dict()
create_data_list()
