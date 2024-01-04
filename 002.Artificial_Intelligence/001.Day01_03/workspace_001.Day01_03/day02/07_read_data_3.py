'''
读取数据  EXCEL XLS

'''

import pandas as pd

#读取excel里面的内容，需要安装 xlrd 或者 openpyxl 库
#pip install --upgrade xlrd==1.2.0
#pip install --upgrade openpyxl
data = pd.read_excel('../data_test/电信用户流失数据/CustomerSurvival.xlsx')

print(data)


