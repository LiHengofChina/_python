
'''
	"波士顿房屋价格" 数据预测
'''


import pandas as pd

# 数据来自：data_url = "http://lib.stat.cmu.edu/datasets/boston"
data = pd.read_csv('./05_boston_data.csv', sep=',', header=None)
x = data.iloc[:, :-1]
print(x)
y = data.iloc[:, -1]
print(y)




