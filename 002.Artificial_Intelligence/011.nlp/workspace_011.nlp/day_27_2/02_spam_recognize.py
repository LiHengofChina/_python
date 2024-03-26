

import numpy as np
import re
import string
import sklearn.model_selection as ms
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn import metrics




import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

'''
———————————————————— 垃圾邮件识别
# 【综合】垃圾邮件识别：它是一个划层的语义，所以在机器学习里面，效果也还可以。

会用到分词等等技术

垃圾邮件识别案例说明 

（1）数据集：5000个正常邮件，5001个垃圾邮件
（2）特征表示：TF-IDF向量作为特征表示
（3）模型选择：朴树贝喹斯、支持向量机

'''



label_name_map = ["垃圾邮件", "正常邮件"]


def tokenize_text(text):  # 分词
    tokens = jieba.cut(text)  # 分词
    tokens = [t.strip() for t in tokens]
    return tokens


def remove_special_char(text):  # 去特殊符号
    tokens = tokenize_text(text)  # 分词

    # compile：编译正则表达式
    # escape: 对需要转义的字符做转义处理
    pattern = re.compile("[{}]".format(
        re.escape(string.punctuation)
    ))
    # 匹配，如何符合正则 的规则，则替换为空字符
    # sub :利用正则 表达 式匹配并替换，
    # filter:序列过滤，过滤不符合条件的元素，返回符合条件元素的列表，filter会把空字符丢弃
    filter_tokens = filter(None,
                           [pattern.sub("", t) for t in tokens])

    filter_text = " ".join(filter_tokens) #每个元素间用空格连接
    return filter_text


def remove_stopwords(text):  # 过滤停用词
    tokens = tokenize_text(text)  # 分词
    filtered_tokens = [t for t in tokens
                       if t not in stopword_list]
    filtered_text = " ".join(filtered_tokens)
    return filtered_text

#
def normalize_corpus(corpus):  # 规范化处理
    result = []  # 处理结果
    for text in corpus:
        text = remove_special_char(text) #去标点
        text = remove_stopwords(text) #过滤停用词
        result.append(text)
    return result


def tfidf_extractor(corpus):
    vec = TfidfVectorizer(min_df=1,  # 最小词频
                          norm="l2",  # 正则化方法
                          smooth_idf=True,  # 是否做平滑
                          use_idf=True  # 是否使用idf指标
                          )
    features = vec.fit_transform(corpus)
    return vec, features


def get_data():  # 读取语料库
    corpus = []  # 邮件内容
    labels = []  # 类别(0:垃圾邮件  1:正常邮件)

    # 读取正常邮件
    with open("spam_data/ham_data.txt", encoding="utf-8") as f:
        for line in f.readlines():
            corpus.append(line)
            labels.append(1)  # 1: 正常邮件

    with open("spam_data/spam_data.txt", encoding="utf-8") as f:
        for line in f.readlines():
            corpus.append(line)
            labels.append(0)  # 1: 垃圾邮件

    return corpus, labels

#过滤空文档
def remove_empty_docs(corpus, labels):
    filtered_corpus = []  # 过滤后的邮件内容
    filtered_labels = []  # 标签

    for doc, label in zip(corpus, labels):
        if doc.strip():  # 去空格后非空
            filtered_corpus.append(doc)
            filtered_labels.append(label)
    return filtered_corpus, filtered_labels


def print_metrics(lables, pred):  # 计算并打印分类指标

    # accuracy
    acc = metrics.accuracy_score(lables, pred)

    # precision
    precision = metrics.precision_score(lables,
                                        pred,
                                        average="weighted")

    # Recall
    recall = metrics.recall_score(lables,
                                  pred,
                                  average="weighted")

    # F1
    f1 = metrics.f1_score(lables,
                          pred,
                          average="weighted")

    print("正确率:%.4f, 查准率:%.4f,召回率:%.4f,F1:%.4f" %
          (acc, precision, recall, f1))


if __name__ == '__main__':
    global stopword_list

    #读取停用词表
    with open("spam_data/stop_words.utf8", encoding="utf-8") as f:
        stopword_list = f.readlines()

    print("读取信用词表结束!")

    #读取数据集
    corpus, labels = get_data()
    corpus, labels = remove_empty_docs(corpus, labels)
    print("读取数据集结束.")

    #划分训练集、测试集
    train_x, test_x, train_y, test_y = ms.train_test_split(
        corpus,          # 邮件内容
        labels,          # 标签
        test_size=0.3,   # 测试集比例
        random_state=32  # 随机种子
    )
    print("划分训练集、测试集结束。")

    #规范化处理
    norm_train_x = normalize_corpus(train_x)
    norm_test_x = normalize_corpus(test_x)
    print("规范化处理")

    #计算TF-IDF
    vec, train_features = tfidf_extractor(norm_train_x)
    test_features = vec.transform(norm_test_x)
    print("计算TF-IDF结束.")


    print("贝叶斯模型：")
    nb_model = MultinomialNB()  # 定义模型
    nb_model.fit(train_features, train_y)  # 训练
    nb_pred = nb_model.predict(test_features) #预测

    print_metrics(test_y, nb_pred)  # 打印分类指标
    print("")

    print("支持向量机：")
    svm_model = SGDClassifier()                     # 默认情况下使用SVM分类 器
    svm_model.fit(train_features, train_y)          # 训练
    svm_pred = svm_model.predict(test_features)     # 预测
    print_metrics(test_y,svm_pred)                  # 打印分类指标


