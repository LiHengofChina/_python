'''
读取数据: 随机读取器
    随机

'''
import paddle.reader


#原始读取器
def reader_createor(file_path):

    def reader():
        with open(file_path,'r') as f:
            lines = f.readlines()
            for line in lines:
                yield line.strip() #去掉后面的\n
    return reader #返回生成器函数

#原始读取器
reader = reader_createor('./data.txt')
shuffle_reader = paddle.reader.shuffle(reader,1024)

for i in shuffle_reader():
    print(i)




