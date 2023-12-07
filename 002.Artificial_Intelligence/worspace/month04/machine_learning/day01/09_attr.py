
import numpy as np

#创建一个复数型的多维数组
a = np.array([[1 + 1j, 2 + 4j, 3 + 7j],
              [4 + 2j, 5 + 5j, 6 + 8j],
              [7 + 3j, 8 + 6j, 9 + 9j]])
print(a.shape)
print(a.dtype)
print(a.ndim)
print(a.size)

print("==" * 30)
print(a.itemsize)
print(a.nbytes)


print("==" * 30)
print(a.real, a.imag, sep='\n')

print("==" * 30)
print(a.T)

print("==" * 30)
print([elem for elem in a.flat])  #列表推导式


print("==" * 30)
b = a.tolist()
print(b)

