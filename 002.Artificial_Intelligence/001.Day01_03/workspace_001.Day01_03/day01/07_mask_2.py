'''
掩码操作
索引掩码
'''

import numpy as np

car = np.array(['Tesla', 'BMW', 'BYD', 'Benz', 'Audi'])
mask = [0, 2, 1, 4, 3]
print(car[mask])  #利用掩码排序


#个数可以不一致
mask = [0,0,0,2,1,0,2,2,0,0,2,1,4,4,3]
print(car[mask])  # 根据 mask 中的索引值选择 car 数组中的元素

