
#【1】
################# 数据预处理##############################################################################

#每个中文转换成数值类型，并划分训练集和测试集

'''
    中文新闻资讯分类 ———————————————— 根据 "亲闻标题"
    模型：文本卷积神经网络
'''

data_root = 'data/news_classify/'
data_file = 'news_classify_data.txt'
train_file = 'train_list.txt'  #训练集
test_file = 'test_list.txt'    #测试集
dict_file = 'dict_txt.txt'     #编码字典文件

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


#【2】
#################  模型的搭建、训练、评估、保存##############################################################################【2】
########## 模型的搭建，训练，评估和保存 ########
import numpy as np
import paddle
from multiprocessing import cpu_count
import paddle.fluid as fluid
import os


# 数据准备
def data_mapper(sample):
    data, label = sample
    # data: '89,56,89,34,12,32,56'
    # val: [89,56,89,34,12,32,56]
    val = [int(w) for w in data.split(',')]

    return val, int(label)


def train_reader(train_file_path):
    def reader():
        with open(train_file_path, 'r') as f:
            lines = f.readlines()
            # 将样本数据打乱
            np.random.shuffle(lines)

            for line in lines:
                data, label = line.strip().split('\t')
                yield data, label

    return paddle.reader.xmap_readers(data_mapper,
                                      reader,
                                      cpu_count(),
                                      1024)


def test_reader(test_file_path):
    def reader():
        with open(test_file_path, 'r') as f:
            lines = f.readlines()

            for line in lines:
                data, label = line.strip().split('\t')
                yield data, label

    return paddle.reader.xmap_readers(data_mapper,
                                      reader,
                                      cpu_count(),
                                      1024)


# 搭建网络结构模型
def Text_CNN(data, dict_dim, emb_dim=128, hid_dim=128,
             hid_dim2=98):
    '''
    TextCNN
    :param data:原始输入数据
    :param dict_dim: 编码字典长度
    :param emb_dim: 词嵌入的参数
    :param hid_dim: 第一组卷积核数量
    :param hid_dim2: 第二组卷积核数量
    :return: 运算结果
    '''
    # 词嵌入层
    emb = fluid.layers.embedding(input=data,
                                 size=[dict_dim, emb_dim])

    # 并列两组，卷积池化
    conv1 = fluid.nets.sequence_conv_pool(input=emb,  # 输入数据，词嵌入层的输出
                                          num_filters=hid_dim,  # 卷积核数量
                                          filter_size=3,  # 卷积核的尺寸
                                          act='tanh',  # 激活函数
                                          pool_type='sqrt')  # 池化类型

    conv2 = fluid.nets.sequence_conv_pool(input=emb,
                                          num_filters=hid_dim2,
                                          filter_size=4,
                                          act='tanh',
                                          pool_type='sqrt')

    # 全连接(输出层)
    pred_y = fluid.layers.fc(input=[conv1, conv2],
                             size=10,
                             act='softmax')
    return pred_y


# 占位符
words = fluid.layers.data(name='words',
                          shape=[1],
                          dtype='int64',
                          lod_level=1)  # 张量层级
label = fluid.layers.data(name='label',
                          shape=[1],
                          dtype='int64')


# 获取字典的长度
def get_dict_len(dict_path):
    with open(dict_path, 'r', encoding='utf-8') as f:
        line = eval(f.readlines()[0])

    return len(line.keys())


dict_dim = get_dict_len(dict_file_path)
pred_y = Text_CNN(words, dict_dim)
# 损失函数
cost = fluid.layers.cross_entropy(input=pred_y,  # 预测值
                                  label=label)  # 真实值
avg_cost = fluid.layers.mean(cost)

# 精度
acc = fluid.layers.accuracy(input=pred_y,
                            label=label)

# 在优化之前克隆program用于模型的评估
test_program = fluid.default_main_program().clone(for_test=True)

# 梯度下降优化器
optimizer = fluid.optimizer.AdagradOptimizer(0.001)
optimizer.minimize(avg_cost)

# 数据读取器
tr_reader = train_reader(train_file_path)
batch_train_reader = paddle.batch(tr_reader,
                                  batch_size=128)

ts_reader = test_reader(test_file_path)
batch_test_reader = paddle.batch(ts_reader,
                                 batch_size=128)

# 执行训练
place = fluid.CUDAPlace(0)
exe = fluid.Executor(place=place)
exe.run(fluid.default_startup_program())  # 初始化

# 使用小批量梯度下降训练模型
# 训练一轮，验证一轮

# 参数喂入器
feeder = fluid.DataFeeder(feed_list=[words, label],
                          place=place)

for pass_id in range(5):
    # 训练
    train_costs, train_accs = [], []
    for data in batch_train_reader():
        train_cost, train_acc = exe.run(program=fluid.default_main_program(),
                                        feed=feeder.feed(data),
                                        fetch_list=[avg_cost, acc])
        train_costs.append(train_cost[0])
        train_accs.append(train_acc[0])
    train_avg_cost = sum(train_costs) / len(train_costs)
    train_avg_acc = sum(train_accs) / len(train_accs)
    print(f'训练集:{pass_id},cost:{train_avg_cost},acc:{train_avg_acc}')

    # 测试
    test_costs, test_accs = [], []
    for data in batch_test_reader():
        test_cost, test_acc = exe.run(program=test_program,
                                      feed=feeder.feed(data),
                                      fetch_list=[avg_cost, acc])
        test_costs.append(test_cost[0])
        test_accs.append(test_acc[0])

    test_avg_cost = sum(test_costs) / len(test_costs)
    test_avg_acc = sum(test_accs) / len(test_accs)
    print(f'Test:{pass_id},cost:{test_avg_cost},acc:{test_avg_acc}')

# 模型的保存
model_save_path = 'model/news_classify/'

if not os.path.exists(model_save_path):
    os.makedirs(model_save_path)

fluid.io.save_inference_model(model_save_path,
                              feeded_var_names=[words.name],
                              target_vars=[pred_y],
                              executor=exe)
print('模型保存成功')



#【3】
################# 加载模型，执行预测##############################################################################


import numpy as np
import paddle
from multiprocessing import cpu_count
import paddle.fluid as fluid
import os

import paddle.fluid as fluid

data_root = 'data/news_classify/'

dict_file = 'dict_txt.txt'     #编码字典文件
dict_file_path = data_root + dict_file

model_save_path = 'model/news_classify/'

#加载模型
place = fluid.CPUPlace()
infer_exe = fluid.Executor(place=place)
infer_program, \
    feed_names, \
    target_vars = fluid.io.load_inference_model(model_save_path,
                                               executor=infer_exe)

# 对待预测的数据进行编码
def get_data(sentence):
    # 读取编码字典
    with open(dict_file_path, 'r', encoding='utf-8') as f:
        dict_txt = eval(f.readlines()[0])

    ret = []
    for s in sentence:
        if not s in dict_txt.keys():
            s = '<unk>'
        ret.append(int(dict_txt[s]))
    return ret


# 初始化
infer_exe.run(fluid.default_startup_program())

# 拿到一组带预测数据
data1 = get_data('别总盯着帕萨特！曾叫板奥迪A6，现仅19万，开10年只换轮胎')
data2 = get_data('读研3年和工作3年，差别究竟有多大？')
data3 = get_data('黄渤退出爆红的极限男人帮，只为在《忘不了餐厅》给老人当配角')

texts = []
texts.append(data1)
texts.append(data2)
texts.append(data3)

# 生成lodTensor
base_shape = [[len(c) for c in texts]]# 每个个句子的长度，每一个句子的shape
tensor_words = fluid.create_lod_tensor(texts, base_shape, place)

result = infer_exe.run(program=infer_program,
                       feed={feed_names[0]: tensor_words},
                       fetch_list=target_vars)

print(result)

names = ['文化','娱乐','体育','财经','房产','汽车',
         '教育','科技','国际',]

for i in range(len(texts)):
    lab = np.argsort(result)[0][i][-1]  # 取到最大值 的下标
    print('预测结果：', names[lab])