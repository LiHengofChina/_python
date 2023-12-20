'''
文本文件读取
'''

import tensorflow as tf

import os


def read_csv(filelist):

    #（1）构建队列
    file_queue = tf.train.string_input_producer(filelist)

    #（2）构建数据读取器
    reader = tf.TextLineReader()

    #（3）用读取器从文件队列中读取数据
    k,v = reader.read(file_queue)
            #k是文件名，v是值

    #（4）解码，将字符串转成张量
    records= [['None'],['None']] #自动将 records转成逗号分隔的内容
    x,y = tf.decode_csv(v,record_defaults=records)
            #解出来之后，x就是特征，y就是类别

    #（5）批处理
    x_bat, y_bat = tf.train.batch([x, y],
                                  batch_size=9,  # 每个批次要几条数据
                                  num_threads=1  # 线程数量
                                  )
    return x_bat, y_bat  # 返回 的是两个op


if __name__ == '__main__':

    # （1）准备文件列表
    dir_name = '../test_data'
    file_names = os.listdir(dir_name)  # 把目录下的文件，转成一个列表
    file_list = []  # 文件列表
    for f in file_names:
        file_list.append(os.path.join(dir_name, f))

    # （2）加载文件，返回的是两个OP，所以需要运行这两个OP
    x_bat, y_bat = read_csv(file_list)

    #执行
    with tf.Session() as sess:

        #定义线程协调器
        coord = tf.train.Coordinator() #回收线程
        #开启队列运行的线程（重要）
        threads =  tf.train.start_queue_runners(sess, coord=coord)

        x_res, y_res = sess.run([x_bat, y_bat])
        print(x_res)
        print(y_res)


        coord.request_stop()#请求停止
        coord.join(threads) #等待指定的线程终止。



