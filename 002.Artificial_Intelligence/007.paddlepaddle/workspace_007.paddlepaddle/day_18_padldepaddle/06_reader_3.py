'''
读取数据: 批量读取器
    批量

'''
import paddle.reader


# 原始读取器
def reader_createor(file_path):
    def reader():
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                yield line.strip()  # 去掉后面的\n

    return reader  # 返回生成器函数


# 原始读取器
reader = reader_createor('./data.txt')
# 随机
shuffle_reader = paddle.reader.shuffle(reader, 1024)
# 批量


# （1）拿到全部批次
batch_reader = paddle.batch(shuffle_reader, 3)
for i in batch_reader():  # 4个批次读取完成
    print(i)

# （2）最后 一个批次数量太少
print("==" * 20)
batch_reader = paddle.batch(shuffle_reader, 3,
                            drop_last=True
                            # 最后 一个批次数量太少，不能达到3个，就删除最后 一个
                            # 保证每个批次数量相同
                            )
for i in batch_reader():
    print(i)

# （3）只拿一个批次
print("==" * 20)
batch_reader = paddle.batch(shuffle_reader, 3)
data = next(batch_reader())
print(data)
