
'''
简单的数学指标
        两数组取大值形成集合或小值形成集合
'''

import numpy as np
import pandas as pd

x = np.arange(1, 10)
y = x[::-1]

print(np.maximum(x,y))
print(np.minimum(x,y))

