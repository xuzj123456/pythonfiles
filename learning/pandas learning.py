# coding=utf-8
import pandas as pd

d = {'one' : pd.Series([1, 2, 3], index=['a', 'b', 'c']),
      'two' : pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])}
df = pd.DataFrame(d)

df['three']=pd.Series([10,20,30],index=['a','b','c'])
df['four']=df['one']+df['three']

print(df['one'])        # 列选择

print(df[1:2])
print(df.loc['a'])
print(df.iloc[1])       # 行选择

print(df[(df.two > 2) & (df.four > 20)])        # 筛选行
