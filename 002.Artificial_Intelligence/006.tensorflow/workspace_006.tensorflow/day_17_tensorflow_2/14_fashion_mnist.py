'''
使用卷积神经网络：实现服务识别
'''
import tensorflow as tf

from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets

class FashionMnist:

    #定义几个成员变量：超参数
    out_feature1 = 12  # 第一组卷积核的数量
    out_feature2 = 24  # 第二组卷积核的数量
    con_nuerons = 512  # 全连接层神经元的数量

    def __init__(self,path):

        #加载数据，这行代码会自动从网上下载数据
        self.data = read_data_sets(path,
                                   one_hot=True)
        #创建 sess 对象
        self.sess = tf.Session()

    #初始化权重变量
    def init_weight_var(self, shape):

        # truncated_normal 截尾正太分布，如（-3，3）的范围，会生成（-2，2）范围的数，波动更小
        init_val = tf.truncated_normal(shape,
                                       mean=0, #期望值是0
                                       stddev=0.1)
        return tf.Variable(init_val)
    #初始化权重偏置
    def init_bais_var(self, shape):
        init_val = tf.constant(1.0, shape=shape)  # 偏置的值，一般是0或1
        return tf.Variable(init_val)


    #二维卷积
    def conv2d(self, x, w):  # x是输入数据，w是权重，使用w去卷x

        '''
            输入张量 x 是一个四维的张量
                    batch 表示批次中的样本数。
                    height 表示输入特征图的高度。
                    width 表示输入特征图的宽度。
                    channels 表示输入特征图的通道数，也即每个位置的像素值对应的数值。

            w是使用 四维形状 生成的 “权重矩阵”
                它的四个维度分度是 ：
                    5: 卷积核的高度（height）。
                    5: 卷积核的宽度（width）。
                    input_feature: 输入通道的数量，也就是输入数据的深度（input channels）。
                    out_feature: 输出通道数（卷积核数量，有几个卷积核就有几个输出），


            所以  tf.nn.conv2d 卷积之后也是有 “四个维度”，分别是：
                    batch 表示批次中的样本数。
                    height 表示输出特征图的高度。
                    width 表示输出特征图的宽度。
                    channels 表示输出特征图的通道数，即卷积核的数量。
        '''

        return tf.nn.conv2d(x,  # 输入数据
                            w,  # 卷积核的权重
                            strides=[1, 1, 1, 1],  # 步长、步幅
                            # 步长 [1,1,1,1],  NHWC,数量、高度、宽度、通道数
                            # 四个值指：样本数量、高度、宽度、通道，都步长为1
                            padding='SAME'  # 同维卷积：SAME表示输入数据和输出数据结果一样，不用自己算
                            # ,use_cudnn_on_gpu=True#是否使用GPUT加载，默认True

                            )

    #二维池化
    def max_pool_2x2(self, x):  # x ：表示对谁进行池化
        return tf.nn.max_pool(x,  # 输入数据（卷积激活之后的结果）
                       ksize=[1, 2, 2, 1],  # 池化窗口的大小、池化区域大小 NHWC 中间两个2表示高度和宽度
                       strides=[1, 2, 2, 1]  # 池化步长 NHWC 中间两个2表示高度和宽度
                       , padding='SAME'  #、池化操作中的填充方式： 'SAME' 表示在输入的边缘补零，使输出的尺寸与输入的尺寸相同。
                       )  # 最大池化

    #卷积池化组（卷积+激活+池化）
    def create_conv_pool_layer(self, input, input_feature, out_feature):
        '''
        :param input:
        :param input_feature: 输入通道数（输入图像的通道数）
        :param out_feature: 输出通道数（卷积核数量，有几个卷积核就有几个输出）
        :return:
        '''

        #（1）卷积
        # 权重
        filter_w = self.init_weight_var([5, 5, input_feature, out_feature])
        '''
            调用时，传了一个四维的形状，
                5: 卷积核的高度（height）。
                5: 卷积核的宽度（width）。
                input_feature: 输入通道的数量，也就是输入数据的深度（input channels）。
                
                out_feature: 输出通道数（卷积核数量，有几个卷积核就有几个输出），
                             //out_feature这个其实表示的是卷积核的个数
                             所以 权重filter_w里面是知道卷积核个数的 
                             

            所以它会生成一个四维的权重张量，
            且，这个权重矩阵会在训练过程中不断更新，

           #另外： 卷积层权重个数 = 输入通道数 * 卷积核尺寸 * 输出通道数            
        '''
        # 偏置
        b_conv = self.init_bais_var([out_feature])#偏置和 "输出通道数相同" ：out_feature
        # 执行卷积
        res = self.conv2d(input, filter_w) + b_conv

        #（2）激活
        h_conv = tf.nn.relu(res)

        #（3）池化
        h_pool = self.max_pool_2x2(h_conv)

        return h_pool


    # 全连接层（指中间的隐藏层，不包括输出层）
    def create_fc_layer(self, input, input_feature, con_neurons):
        '''
        :param input:
        :param input_feature: "全连接层" 输入特征数量
        :param con_neurons: 神经元数量
        :return:
        '''

        # 权重 = 卷积后的特征个数 * 神经元个数
        w_fc = self.init_weight_var([input_feature, con_neurons])
        # 偏置 = 神经元数量相同
        b_fc = self.init_bais_var([con_neurons])

        # 全连接
        res = tf.matmul(input, w_fc) + b_fc

        # 激活
        h_fc = tf.nn.relu(res)
        return h_fc

    #搭建卷积神经网络
    def build(self):
        #定义占位符
        self.x = tf.placeholder('float32', shape=[None, 784])  # 数据已经拉伸成一维了
        x_image = tf.reshape(self.x, [-1, 28, 28, 1]) #因为卷积需要4维数据

        self.y = tf.placeholder('float32', shape=[None, 10])  #



        # （1）第一组: 卷积激活池化组
        h_pool1 = self.create_conv_pool_layer(x_image,  # 输入数据，原始图像
                                              1,  # 输入图像通道数是1
                                              self.out_feature1  # 输出通道数
                                              )
        # （2）第二组: 卷积激活池化组
        h_pool2 = self.create_conv_pool_layer(h_pool1,  # 输入数据
                                              self.out_feature1,  # 输入图像通道数是
                                              self.out_feature2  # 输出通道数
                                              )

        # （3）全连接
        # 输出特征数量
        h_pool2_flat_feature = 7 * 7 * self.out_feature2
        # 拉伸成一维的特征（全连接需要一维数据）
        h_pool2_flat = tf.reshape(h_pool2, [-1, h_pool2_flat_feature])
        # 创建全连接
        h_fc = self.create_fc_layer(
            h_pool2_flat,
            h_pool2_flat_feature,
            self.con_nuerons
        )

        # （4）丢弃层
        h_fc_drop = tf.nn.dropout(h_fc, keep_prob=0.5)  # 丢一半,让其中的一半不更新，并不是删除

        # （5）输出层（这里就不封装方法，直接写了）
        #输出层权重
        w_fc = self.init_weight_var([self.con_nuerons, 10])
        b_fc = self.init_bais_var([10])
        pred_y = tf.matmul(h_fc_drop, w_fc) + b_fc

        # （6）损失函数
        # 先计算softmax，再计算交叉熵
        loss = tf.nn.softmax_cross_entropy_with_logits(
            labels=self.y, #真实值
            logits=pred_y  #预测值
        )
        #对损失函数求均值
        cost = tf.reduce_mean(loss)

        # （7）梯度下降，求损失函数的极小值
        # #自适应梯度下降优化器，在梯度下降过程中会 "自动调整学习率"
        optimizer = tf.train.AdamOptimizer(0.001)# 0.001 是初始的学习率
        self.train_op = optimizer.minimize(cost)

        # （8）评估：
        # 准确率
        corr = tf.equal(tf.argmax(self.y, 1),
                        tf.argmax(pred_y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(corr, 'float32'))

    #执行训练
    def train(self):
        # 初始化变量
        self.sess.run(tf.global_variables_initializer())
        batch_size = 100  # 批次大小
        print('开始训练...')
        for i in range(10):
            # 总批次
            total_batch = int(self.data.train.num_examples / batch_size)

            total_acc = 0.0
            for j in range(total_batch):
                train_x, train_y = self.data.train.next_batch(batch_size)
                params = {self.x: train_x, self.y: train_y}
                t, acc = self.sess.run([self.train_op, self.accuracy],
                                       feed_dict=params)
                # acc是当前批次的精度
                total_acc += acc

            avg_acc = total_acc / total_batch

            print('轮数：{},精度：{}'.format(i, avg_acc))



    #评估
    def metrics(self):
        #使用测试集进行评估
        test_x, test_y = self.data.test.next_batch(10000)
        params = {self.x: test_x, self.y: test_y}
        test_acc = self.sess.run(self.accuracy,
                      feed_dict=params)

        print('测试集精度',test_acc)
    def close(self):
        self.sess.close()




if __name__ == '__main__':

    mnist = FashionMnist('../fashion_mnist/')

    mnist.build()  # 搭建网络
    mnist.train()  # 训练
    mnist.metrics()  # 进行评估


    mnist.close()  # 关闭session
