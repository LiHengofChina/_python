'''

【本地运行】
第一个paddle程序， 需要paddle 1.8.4 版本运行

使用paddle实现相加
'''
import paddle.fluid as fluid

# 定义：创建张量
x = fluid.layers.fill_constant(shape=[1], #1维的一个元素
                               dtype='float32',
                               value=100.0
                               )

y = fluid.layers.fill_constant(shape=[1],
                               dtype='float32',
                               value=200.0)

# fluid.layers.elementwise_add(x, y)  # 指定维度求和
res = x + y  #更简单的写法：

#执行：
place = fluid.CPUPlace()  #选择要执行的设备，这个和你机器 环境 和安装的paddlepaddle版本有关
exe = fluid.Executor(place=place) #可以指定这段代码在哪里执行，GPU，还是CPU

result = exe.run(program=fluid.default_main_program()
                # program :选择执行哪个程序，和tensorflow一样， 选择要执行哪个图， 这里选择的是哪个program
                # 不写执行默认的主程序

                , fetch_list=[res]  #
                                # 和tensorflow有点像，但是不一样。
                                # tensorflow 是选择要运行的op,其它op不会执行。
                                # 而这里是：“选择要哪个op的执行结果”
                                # 当exe.run运行program时，当前program中的所有op全都会执行

                                #而这里选择要 要哪个res的执行结果，所以返回的是它的结果
                                #返回列表套数组

                )
print(result)
print(result[0])
print(result[0][0])
