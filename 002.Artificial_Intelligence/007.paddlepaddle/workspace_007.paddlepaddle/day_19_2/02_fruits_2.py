

'''
paddlepaddle：
    利用CNN实现水果分类
     __执行预测
'''



import paddle
import paddle.fluid as fluid

###############################加载模型 预测


name_dict = {'apple': 0,  #注意，要按字母顺序
             'banana': 1,
             'grape': 2,
             'orange': 3,
             'pear': 4
             }
# 保存模型 路径
model_save_path = '../model/fruits'


import numpy as np

place = fluid.CPUPlace()
infer_exe = fluid.Executor(place=place)

test_img = 'apple1.png'
#测试数据也必须先resize，再归一化

def load_img(path):
    #加载并转换
    img = paddle.dataset.image.load_and_transform(path,
                                            resize_size=128,
                                            crop_size=128,
                                            is_train=False,
                                            is_color=True
                                            )
    img = img.astype('float32') / 255.0
    return img


infer_imgs = []  # 存放待预测的数据
infer_imgs.append(load_img(test_img))
infer_imgs = np.array(infer_imgs)

# 加载模型
infer_program, feed_namse, target_var = fluid.io.load_inference_model(model_save_path,
                                                                      infer_exe  # 把模型加载到 infer_exe 执行器
                                                                      )
result = infer_exe.run(program=infer_program,
                       feed={feed_namse[0]: infer_imgs},
                       fetch_list=target_var)  # 返回5个类别的相对概率
result = np.argmax(result[0])
for k,v in name_dict.items():
    if result == v:
        print('预测类别：',k)
