'''
测试 窗口、以及它的参数

'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.figure('liheng',
           figsize=(16, 9),
           facecolor='lightgray'
           )

# 使用pandas读取数据 #薪资和工作年限的关系图
data = pd.read_csv('../../data_test/Salary_Data.csv')

x = data['YearsExperience']
y = data['Salary']


# plt.plot(x, y)      # 用连线来绘图
plt.scatter(x, y)     # 用点来绘图
        #这组数据大致符合线性分布


#设置标题，
plt.title('YearsExperience-Salary', fontsize=24)
#x轴标签
plt.xlabel('YearExpe', fontsize=18)
#y轴标签
plt.ylabel('Salary', fontsize=18)

#设置网格
plt.grid(linestyle=':')

#紧凑式布局
plt.tight_layout()


plt.show()


