#【3】
#################  模型的搭建、训练、评估、保存##############################################################################【2】
########## 模型的搭建，训练，评估和保存 ########
import numpy as np
import paddle
from multiprocessing import cpu_count
import paddle.fluid as fluid
import os

# 启用静态图模式
paddle.enable_static()

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
    emb = fluid.layers.embedding(input=data,size=[dict_dim, emb_dim])
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


##############################################
data_root = 'data/news_classify/'
dict_file = 'dict_txt.txt'

dict_file_path = data_root + dict_file
train_file = 'train_list.txt'  #训练集
test_file = 'test_list.txt'    #测试集

train_file_path = data_root + train_file
test_file_path = data_root + test_file
##############################################

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
batch_test_reader = paddle.batch(ts_reader, batch_size=128)

# 执行训练
place = fluid.CUDAPlace(0)
exe = fluid.Executor(place=place)
exe.run(fluid.default_startup_program())  # 初始化

# 使用小批量梯度下降训练模型
# 训练一轮，验证一轮

# 参数喂入器
feeder = fluid.DataFeeder(feed_list=[words, label], place=place)

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


