
#【4】
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
