#【4】加载模型，执行预测
################# 加载模型，执行预测##############################################################################


import numpy as np
import paddle
from multiprocessing import cpu_count
import paddle.fluid as fluid
import os

# 启用静态图模式
paddle.enable_static()


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


texts = [] # 存放待预测句子
# 拿到一组带预测数据
data1 = get_data("在获得诺贝尔文学奖7年之后，莫言15日晚间在山西汾阳贾家庄如是说")
data2 = get_data("综合'今日美国'、《世界日报》等当地媒体报道，芝加哥河滨警察局表示")
data3 = get_data("中国队2022年冬奥会表现优秀")
data4 = get_data("中国人民银行今日发布通知，降低准备金率，预计释放4000亿流动性")
data5 = get_data("10月20日,第六届世界互联网大会正式开幕")
data6 = get_data("同一户型，为什么高层比低层要贵那么多？")
data7 = get_data("揭秘A股周涨5%资金动向：追捧2类股，抛售600亿香饽饽")
data8 = get_data("宋慧乔陷入感染危机，前夫宋仲基不戴口罩露面，身处国外神态轻松")
data9 = get_data("此盆栽花很好养，花美似牡丹，三季开花，南北都能养，很值得栽培")  # 不属于任何一个类别

texts.append(data1)
texts.append(data2)
texts.append(data3)
texts.append(data4)
texts.append(data5)
texts.append(data6)
texts.append(data7)
texts.append(data8)
texts.append(data9)

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
