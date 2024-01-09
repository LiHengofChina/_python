'''

读取数据: 原始读取器

【本地运行】
'''

#原始读取器
def reader_createor(file_path):

    def reader():
        with open(file_path,'r') as f:
            lines = f.readlines()
            for line in lines:
                yield line.strip() #去掉后面的\n
    return reader #返回生成器函数

reader = reader_createor('./data.txt')

for i in reader(): #这里 reader 有小括号()
    print(i)


