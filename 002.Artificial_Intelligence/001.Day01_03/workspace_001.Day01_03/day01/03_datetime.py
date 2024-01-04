
'''
测试时间日期类型
'''

import numpy as np



# 字符串的np数组
print("==" * 20)
ary = np.array(['2021-01-01',
                '2021',
                '2023-06-21 14:55:23',
                '1970-01-01 00:00:00',
                '1970-01-02 00:00:00'
                ])
print(ary)
print(ary.dtype)



# string --->转成datetime64类型
print("==" * 20)
# liheng = ary.astype('datetime64')  # 以元素 “精度最高的为” 准进行转换，
liheng = ary.astype('datetime64[D]')  # [D]指定精确到天
print(liheng)
print(liheng.dtype)  # datetime64[s] [s]表示精确要秒  [Y]年[M]月[D]日   [h]时[m]分[s]秒


print("==" * 20)
# datetime64 ---> 转int转成数值类型
xiaoxiao = liheng.astype('int32')
print(xiaoxiao)
print(xiaoxiao.dtype)  # 返回的时间戳表示：时间距离计算机元年的天数，这和上面的[D]有关，如果是[s]，则返回的是秒数



