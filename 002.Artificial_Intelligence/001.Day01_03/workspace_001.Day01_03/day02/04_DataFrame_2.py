'''
DataFrame 示例
        通过字典创建
'''
import pandas as pd

#通过字典创建
print("##" * 20)
data = {'Name': ['Tom', 'Jerry', 'Jack', 'Rose'],   # 为列表时，列表长度必须相同
        'Age': [18, 18, 20, 20]}                    # 为列表时，列表长度必须相同
df = pd.DataFrame(data)
print(df)


#通过字典创建，将行列转成Series,解决"某些数据无法取到的问题"
print("##" * 20)
data = {'Name': pd.Series(['Tom', 'Jerry', 'Jack', 'Rose']),
        'Age': pd.Series([18, 18, 20])} #转成Series后，列表长度就可以一致了，实际场景中有时候，不能获取全部数据时，可以使用这种方式
                                        #长度不同时，此时出现了一个NaN，它是float，所以其它元素类型也会变成Float
df = pd.DataFrame(data)
print(df)       #显示一个 NaN，表示Not A Number



#通过字典创建，将行列转成Series,"某些数据无法取到"，但是是在中间某个数据没有
print("##" * 20)
data = {'Name': pd.Series(['Tom', 'Jerry', 'Jack', 'Rose'], index=['a', 'b', 'c', 'd']),
        'Age': pd.Series([18, 18, 20], index=['a', 'b', 'd'])}  # 通过索引来调整
df = pd.DataFrame(data)
print(df)  # 显示一个 NaN，表示Not A Number

