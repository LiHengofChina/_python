
'''
ndarray 的基本属性
查看元素类型，修改元素类型

'''
import numpy as np

print("==" * 20)
ary = np.arange(1, 10)
print(ary.dtype)

print("==" * 20)
print(type(ary),
      ary,
      ary.dtype)
# ary.dtype = 'float32'  #这种方式，只是暴力修改了它的解析方式
liheng = ary.astype('float64')  # 不能修改原来数组，所以要一个变量接收
print(type(liheng), liheng, liheng.dtype)
