# coding=utf-8
import pandas as pd
import numpy as np

df = pd.read_excel('data/收益率.xlsx')
df_y_return = pd.DataFrame([[np.nan]*len(df.columns)]*20)
j = 0
for i in range(1,len(df.columns)+1, 3):
    df_ = df.iloc[:,[i-1,i]]
    df_.dropna(inplace=True)
    df_y_return.iloc[0, j] = '年份'
    df_y_return.iloc[0, j + 1] = df.columns[i]
    m = 1
    for y in range(df_.iloc[0,0].year, 2022):
        df_.columns = ['日期', '净值']
        l = df_.loc[[d.year == y for d in df_['日期']]]
        r = (l.iloc[-1,1]-l.iloc[0,1])/l.iloc[0,1]
        df_y_return.iloc[m,j] = y
        df_y_return.iloc[m,j+1] = r
        m += 1
    j += 2

df_y_return.to_excel('data/年收益率.xlsx', index=False,
                     header=False,  sheet_name='年收益率')