

import tensorflow as tf

import os

'''
    tf—————————————— 图像读取
        说明：
            （1）多张大小不同的图片，读取过程中可以 resize 成 "全部一样的大小"
            （2）一张图就是一个样本数据

'''
def read_img(filelist):

    #（1）构建队列
    file_queue = tf.train.string_input_producer(filelist)

    #（2）构建数据读取器
    reader = tf.WholeFileReader()#全文件读取器

    #（3）用读取器从文件队列中读取数据
    k,v = reader.read(file_queue)
            #k是文件名，v是值

    #（4）解码，#自动统一转成张量
    imgs = tf.image.decode_jpeg(v)
    resized_img = tf.image.resize(imgs, [250, 250])  # 所有图片固定大小 250 * 250
    resized_img.set_shape([250, 250, 3]) #修改 “张量” 和 “通道”

    #（5）批处理
    imgs = tf.train.batch([resized_img],
                   batch_size=10,#每次读取10张图像
                   num_threads=1
                   )
    return imgs #返回的是op


if __name__ == '__main__':

    # （1）准备文件列表
    dir_name = '../test_img'
    file_names = os.listdir(dir_name)  # 把目录下的文件，转成一个列表
    file_list = []  # 文件列表
    for f in file_names:
        file_list.append(os.path.join(dir_name, f))

    # （2）加载文件，返回的是两个OP，所以需要运行这两个OP
    img = read_img(file_list) #

    #执行
    with tf.Session() as sess:

        #定义线程协调器
        coord = tf.train.Coordinator() #回收线程
        #开启队列运行的线程（重要）
        threads =  tf.train.start_queue_runners(sess, coord=coord)

        res = sess.run(img)
        print(res)
        print(res.shape) #读取的是四维数据，(10, 250, 250, 3)#表示10个三维数组




        coord.request_stop()#请求停止
        coord.join(threads) #等待指定的线程终止。


#显示图像
import matplotlib.pyplot as plt

for i in range(1, 11):
    plt.subplot(2, 5, i)
    plt.imshow(res[i - 1].astype('int32'))
    plt.xticks([])
    plt.yticks([])

plt.show()
