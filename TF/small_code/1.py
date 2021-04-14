# coding=utf-8
import pandas as pd

df = pd.read_excel('000005 卓识利民.xlsx')

def del_eql(df):
    while df.iloc[0][1] == df.iloc[1][1]:
        df = df.drop(df.index[0])
    return df

df = del_eql(df)

df.to_excel('000005 卓识利民.xlsx', index=False)