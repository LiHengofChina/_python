'''
标准化（均值移除）
    " 每一列的平均值为0" ， "标准差为1"

演示计算过程

'''
import numpy as np

# 构建一个3行3列的数据，人工智能里面数据一般都是浮点数
raw_sample = np.array([[3.0,-100.0,2000.0],
                       [0.0,400.0,3000.0],
                       [1.0,-400.0,2000.0]])

# copy是为了不修改原来的数据
std_sample = raw_sample.copy()

# 把行转列，再遍历
for col in std_sample.T:
    col_mean = col.mean()  # 每列的平均值
    col_std = col.std()    # 每列的标准差  # 或 np.std(col, ddof=0)

    col -= col_mean       # col- col_mean  #  col 是一个列，就是一个数组，减去一个值，会利用广播机制
                          #  col 是数组，通过 -= 就能直接修改数组中的元素 ，但是 col = col -col_mean 是不可以修改数组中元素的
                          #  通过打印 std_sample 数组就可以看到效果
    col /= col_std        #   同理用  /= ,每列变成处理后的值


print(std_sample)

# 变成 了平均值为0，标准差为1的
#验证
print(std_sample.mean(axis=0)) #求每列平均值
                # [ 5.55111512e-17  0.00000000e+00 -2.96059473e-16]
                #  5.55111512e-17 非常接近0 了
                #  -2.96059473e-16 非常接近0 了

print(std_sample.std(axis=0))  #求每列标准差为1


'''

更简单的写法
print((col - col.mean()) / np.std(col, ddof=0))
（1）用当前列的数据 - 当前列的平均值，得到 "离差"
（2）"离差" / 原始数据的每列的标准差，

    col - col.mean() 是离差
     np.std(col, ddof=0)是=标准差

'''



