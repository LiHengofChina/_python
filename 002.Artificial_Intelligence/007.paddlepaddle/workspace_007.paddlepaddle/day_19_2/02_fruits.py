


import  os


'''
【AIStudio运行】
paddlepaddle：
    利用CNN实现水果分类
'''
###############################【1】数据预处理
#把类别转换成字典，也可以使用：'标签编码'
name_dict = {'apple': 0,  #注意，要按字母顺序
             'banana': 1,
             'grape': 2,
             'orange': 3,
             'pear': 4
             }

data_root_path = '../fruits/' #数据集所在目录

train_file_path = data_root_path + 'train.txt' # 训练集，图片路径
test_file_path = data_root_path + 'test.txt'   # 测试集，图片路径




# {
# 'apple':[xx,xx,xx,xx],
# 'banana':[xx,xx,xx,xx]
# ....
#  }
name_data_list = {} #存放所有的图像路径
#遍历每一个子目录，拼据此图像路径，加入 字典当中
dirs = os.listdir(data_root_path)
def save_train_test_file(path,name):
    #如果键值对不存在,新建键值对
    if name not in name_data_list:
        name_data_list[name] = [path]
    #如果存在键值对,则直接拿到值的列表,添加元素
    else:
        name_data_list[name].append(path)

for d in dirs:
    full_path = os.path.join(data_root_path,d)
    if os.path.isdir(full_path):
        imgs = os.listdir(full_path)
        for img in imgs:
            all_path = full_path + '/' + img
            save_train_test_file(all_path,d)

# print(name_data_list)

# 划分训练集和测试集 9：1 ，分类业务要等比例划分，苹果要9：1，梨子也要9：1
with open(train_file_path, 'w') as f:
    pass  #这种写法仅仅是为了创建文件
with open(test_file_path, 'w') as f:
    pass  #这种写法仅仅是为了创建文件

for name,imgs_list in name_data_list.items():
    i = 0
    for img in imgs_list:
        if i % 10 == 0: #分类业务要等比例划分
            #测试集加入
            with open(test_file_path, 'a') as f:
                line = '%s\t%d\n' % (img, name_dict[name])
                f.write(line)
        else:
            #训练集加入
            with open(train_file_path, 'a') as f:
                line = '%s\t%d\n' % (img, name_dict[name])
                f.write(line)
        i+=1
# print(train_file_path)
# print(test_file_path)

print('数据预处理完成')




###############################【2】搭建模型 训练

import paddle
from multiprocessing import cpu_count
import paddle.fluid as fluid
import matplotlib.pyplot as plt

#########训练集读取器（1）
def train_mapper(sample):
    img, label = sample
    #根据路径读取图像数据
    img = paddle.dataset.image.load_image(img,
                                    is_color=True #加载为彩色图像，默认为True
                                    )

    #国类卷积神经网络需要的图像大小是固定的，处理图像
    img = paddle.dataset.image.simple_transform(im=img,          # 要处理哪张图像
                                          resize_size=128,  # 缩放大小
                                          crop_size=128,    # 裁剪大小
                                          is_train=True,    # 训练模式-随机裁剪，测试模式-中心裁剪
                                          is_color=True     # 彩色图像
                                          )

    #归一化，图像处理一般都需要归一化，梯度下降一般都需要归一化
    img = img.astype('float32') / 255.0  # 利用广播机制
    return img, label

#准备数据
def train_r(train_list):
    def reader():
        with open(train_list, 'r') as f:
            lines = [line.strip() for line in f]
            for line in lines:  # '路径\t类别'
                img_path, lab = line.split('\t')
                yield img_path, int(lab)
    # return reader
    return paddle.reader.xmap_readers(
        train_mapper, #指将yield回来的内部交给哪个函数处理，二次处理，需要自己定义
        reader,
        cpu_count(), #进程数
        1024 #缓冲区大小
        )

#########测试集读取器（2）
def test_mapper(sample):
    img, label = sample
    #根据路径读取图像数据
    img = paddle.dataset.image.load_image(img,
                                    is_color=True #加载为彩色图像，默认为True
                                    )

    #国类卷积神经网络需要的图像大小是固定的，处理图像
    img = paddle.dataset.image.simple_transform(im=img,  # 要处理哪张图像
                                          resize_size=128,  # 缩放大小
                                          crop_size=128,    # 裁剪大小
                                          is_train=False,    # 训练模式-随机裁剪，测试模式-中心裁剪
                                          is_color=True     # 彩色图像
                                          )

    #归一化，图像处理一般都需要归一化，梯度下降一般都需要归一化
    img = img.astype('float32') / 255.0  # 利用广播机制
    return img, label

#准备数据
def test_r(test_list):
    def reader():
        with open(test_list, 'r') as f:
            lines = [line.strip() for line in f]
            for line in lines:  # '路径\t类别'
                img_path, lab = line.split('\t')
                yield img_path, int(lab)
    # return reader
    return paddle.reader.xmap_readers(
        test_mapper, #指将yield回来的内部交给哪个函数处理，二次处理，需要自己定义
        reader,
        cpu_count(), #进程数
        1024 #缓冲区大小
        )

#训练集reader（3）
batch_size = 32 #批次大小
train_reader = train_r(train_file_path)
random_train_reader = paddle.reader.shuffle(train_reader,
                                            1024) #随机
batch_train_reader =paddle.batch(random_train_reader,
                                 batch_size=batch_size)

#测试集reader（4）
batch_size = 32  # 批次大小
test_reader = test_r(test_file_path)
batch_test_reader = paddle.batch(test_reader,
                                 batch_size=batch_size)
#搭建模型
# （1）占位符
image = fluid.layers.data(name='image',
                          shape=[3, 128, 128],  # 128 * 128 * 3的图像
                          dtype='float32')
label = fluid.layers.data(name='label',
                          shape=[1],  # 只有一个类别，只有一个类别，怎么做相对概率呢？
                          dtype='int64')


def convolution_neural_network(image):
    '''
    3个卷积
    :param image:
    :return:
    '''
    # 卷积池化组1
    conv_pool1 = fluid.nets.simple_img_conv_pool(
        input=image,     #输入数据
        num_filters=32,  #卷积核数量
        filter_size=3,   #卷积核尺寸（大小）
        pool_size=2,     #池化区域
        pool_stride=2,   #池化步长
        pool_type='max', #池化类型：最大池化
        conv_stride=1,   #卷积步长
        act='relu'       #激活函数
    )
    # drop_out1
    drop = fluid.layers.dropout(x=conv_pool1,
                                dropout_prob=0.5)
    # 卷积池化组2
    conv_pool2 = fluid.nets.simple_img_conv_pool(
        input=drop,     #输入数据：上一次的结果 ********
        num_filters=64,  #卷积核数量，深度越深，数量越多 ********
        filter_size=3,   #卷积核尺寸（大小）
        pool_size=2,     #池化区域
        pool_stride=2,   #池化步长
        pool_type='max', #池化类型：最大池化
        conv_stride=1,   #卷积步长
        act='relu'       #激活函数
    )
    # drop_out2
    drop = fluid.layers.dropout(x=conv_pool2,
                                dropout_prob=0.5)
    # 卷积池化组3
    conv_pool3 = fluid.nets.simple_img_conv_pool(
        input=drop,     #输入数据：上一次的结果 ********
        num_filters=64,  #卷积核数量，深度越深，数量越多 ******** 可以不变，但不能变少
        filter_size=3,   #卷积核尺寸（大小）
        pool_size=2,     #池化区域
        pool_stride=2,   #池化步长
        pool_type='max', #池化类型：最大池化
        conv_stride=1,   #卷积步长
        act='relu'       #激活函数
    )
    # drop_out3
    drop = fluid.layers.dropout(x=conv_pool3,
                                dropout_prob=0.5)

    # 全连接
    fc = fluid.layers.fc(input=drop,
                         size=512,  # 512个神经元
                         act='relu'
                         )
    #再次丢弃
    drop = fluid.layers.dropout(x=fc,
                                dropout_prob=0.5)
    # 输出层 #输出层也是一个全连接
    pred_y = fluid.layers.fc(input=drop,
                             size=5,
                             act='softmax'
                             )
    return pred_y

pred_y = convolution_neural_network(image)
#损失函数（交叉熵）
cost = fluid.layers.cross_entropy(input=pred_y,  #预测值
                                  label=label)   #真实值
avg_cost = fluid.layers.mean(cost) #求平均值

#准确率
accuracy = fluid.layers.accuracy(input=pred_y, label=label)

#在优化之前clone一个program，用于测试 ,这样克隆只会有前面的内容，不会有后面的优化，
#包括准确率也会有。
test_program = fluid.default_main_program().clone(for_test=True#for_test 表示用于测试
                                                 )



#梯度下降
optimizer = fluid.optimizer.Adam(learning_rate=0.001  # 学习率
                                 )
optimizer.minimize(avg_cost)



# 执行
# place = fluid.CUDAPlace(0) #
place = fluid.CPUPlace()  # cpu
exe = fluid.Executor(place=place)

#初始化
exe.run(fluid.default_startup_program())

#参数喂入器
feeder = fluid.DataFeeder(feed_list=[image, label],
                          place=place)

# 开始训练
# 收集第一轮的平均损失值 和准确率
costs = []
accs = []
iters = []
for pass_id in range(2):

    ###################训练
    train_costs = []
    train_accs = []
    for data in batch_train_reader():
        train_cost, train_acc = exe.run(program=fluid.default_main_program(),
                                        feed=feeder.feed(data),  # 使用参数喂入器传参
                                        fetch_list=[avg_cost, accuracy])

        # 每一轮的平均损失值和准确率
        train_costs.append(train_cost[0])
        train_accs.append(train_acc[0])

    train_avg_cost = sum(train_costs) / len(train_costs)  # 每一轮的平均值
    train_avg_acc = sum(train_accs) / len(train_accs)  # 每一轮的准确率

    costs.append(train_avg_cost)
    accs.append(train_avg_acc)
    iters.append(pass_id)

    print('轮数:{},cost:{},acc:{}'.format(pass_id,
                                          train_avg_cost,
                                          train_avg_acc,
                                          ))

    ###################测试（每一轮训练完之后，马上测试）
    test_accs = []
    for data in batch_test_reader():
        test_acc = exe.run(program=test_program,
                           feed=feeder.feed(data),  # 这次是喂入测试集的数据
                           fetch_list=[accuracy]  # 测试的时候只求精度
                           )
        test_accs.append(test_acc[0][0])
    test_avg_acc = sum(test_accs) / len(test_accs)
    print('Test:{},Acc:{}'.format(pass_id, test_avg_acc))


# 保存模型（保存推荐模型）
model_save_path = '../model/fruits'
if not os.path.exists(model_save_path):
    os.makedirs(model_save_path)
fluid.io.save_inference_model(model_save_path,
                              ['image'], #执行预测蚨喂入的参数
                              [pred_y],  #预测结果从哪里取
                              exe #模型
                              )
print('模型保存成功')

#训练过程可视化
plt.plot(iters, costs, color='orangered') #损失值
plt.plot(iters, accs, color='dodgerblue') #精度

plt.savefig('train.png')
plt.show()














