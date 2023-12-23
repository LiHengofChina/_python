'''

利用paddle实现多元回归

    加载模型，执行预测

'''

import paddle.fluid as fluid
import paddle
import matplotlib.pyplot as plt

import numpy as np
import os

#执行
place = fluid.CPUPlace()#指定执行设备
#加载模型
infer_exe = fluid.Executor(place=place) #定义一个执行器

model_save_path  = '../../model/uci_housing/'

infer_program, fee_names, target_vars = fluid.io.load_inference_model(model_save_path,
                                                                      infer_exe)
# 返回值说明：模型结构 program，执行预测时，需要喂入的参数，预测结果从哪里取

#测试集读取器（不用随机）
test_reader = paddle.batch(paddle.dataset.uci_housing.test(),
                           batch_size=200)
test_date = next(test_reader())

# [(x,y)]
test_x = np.array([i[0] for i in test_date]).astype('float32')
test_y = np.array([i[1] for i in test_date]).astype('float32')

# 执行预测
result = infer_exe.run(program=infer_program,
                       feed={fee_names[0]: test_x},
                       fetch_list=target_vars
                       )
print(result[0])
