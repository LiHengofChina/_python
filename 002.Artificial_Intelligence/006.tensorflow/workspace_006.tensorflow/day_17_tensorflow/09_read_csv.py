

import tensorflow as tf

import os

'''
    tf—————————————— 文本读取
        说明：
            （1）数据分散在多个文件中，A.txt、B.txt、C.txt
            （2）每个文件中是 “特征” 和 “真实值”

'''

def read_csv(filelist):


    #（1）构建队列
    file_queue = tf.train.string_input_producer(filelist)

    #（2）构建数据读取器
    reader = tf.TextLineReader()

    #（3）用读取器从文件队列中读取数据
    k,v = reader.read(file_queue)
            #k是文件名，v是值

    #（4）解码，将字符串转成张量
    records= [['None'],['None']] #自动将 records 转成逗号分隔的内容
    x,y = tf.decode_csv(v,record_defaults=records)
            #解出来之后，x就是特征，y就是类别


    #（5）批处理
    x_bat, y_bat = tf.train.batch([x, y],
                                  batch_size=6,  # 每个批次要几条数据
                                  num_threads=1  # 线程数量
    )
    #这种方式：A.txt、B.txt、C.txt 这三个文件是乱序的，但是 A.txt、B.txt、C.txt里面各自内容是有序的

    return x_bat, y_bat  # 返回 的是两个op


if __name__ == '__main__':

    # （1）准备文件列表
    dir_name = '../test_data'
    file_names = os.listdir(dir_name)  # 把目录下的文件，转成一个列表
    file_list = []  # 文件列表
    for f in file_names:
        file_list.append(os.path.join(dir_name, f))

    # （2）加载文件，返回的是两个OP，所以需要运行这两个OP
    # file_list ['../test_data\\A.txt', '../test_data\\B.txt', '../test_data\\C.txt']
    x_bat, y_bat = read_csv(file_list)

    #执行
    with tf.Session() as sess:

        #【1】定义线程协调器
        coord = tf.train.Coordinator() #回收线程
        #开启队列运行的线程（重要）
        threads =  tf.train.start_queue_runners(sess, coord=coord)

        x_res, y_res = sess.run([x_bat, y_bat])#运行两个op，拿到的就是返回的数据
        print(x_res)
        print(y_res)

        #【2】回收停止线程
        coord.request_stop()#请求停止
        coord.join(threads) #等待指定的线程终止。



