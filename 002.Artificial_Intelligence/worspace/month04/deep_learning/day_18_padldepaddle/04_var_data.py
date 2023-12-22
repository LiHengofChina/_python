'''
变量类型：占位符
'''
import numpy as np
import paddle.fluid as fluid

#定义：
x = fluid.layers.data(name='xxx',
                      shape=[2, 3],
                      dtype='float32')

y = fluid.layers.data(name='yyy',
                      shape=[2, 3],
                      dtype='float32')

add = fluid.layers.elementwise_add(x, y)  # 对应位置对应相加
mul = fluid.layers.elementwise_mul(x, y)  # 对应位置对应相乘

#执行
place = fluid.CPUPlace()
exe = fluid.Executor(place=place)

#初始化
exe.run(fluid.default_startup_program())


#运行主程序
data = np.arange(1, 7).reshape(2, 3)
add_res, mul_res = exe.run(program=fluid.default_main_program(),
                           feed={'xxx': data, 'yyy': data},
                                            #注意：这里必须使用 xxx、yyy传参，也就是上面对应的名字。
                           fetch_list=[add, mul]
                           )
print(add_res)
print(mul_res)
