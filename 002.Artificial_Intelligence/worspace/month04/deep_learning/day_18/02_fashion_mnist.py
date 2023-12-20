'''
使用卷积神经网络：实现服务识别
'''
import tensorflow as tf

from tensorflow.contrib.learn.python.learn.datasets.mnist import read_data_sets

class FashionMnist:
    def __init__(self,path):
        #加载数据
        self.data = read_data_sets(path,
                                   one_hot=True)
        #创建 sess 对象
        self.sess = tf.Session()

if __name__ == '__main__':
    mnist = FashionMnist('../fashion_mnist/')
