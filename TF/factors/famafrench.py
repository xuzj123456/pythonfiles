# coding=utf-8
import pandas as pd
import statsmodels.api as sm

fund_file = '110011.OF 易方达中小盘.csv'

df = pd.read_csv('data\\factors\\factors1.csv', encoding='gbk', index_col=0)
df_ = pd.read_csv('data\\净值\\'+fund_file, encoding='gbk', index_col=0)
df = df.join(df_)
df['超额收益']=df.iloc[:,-1].pct_change()-df['10年国债收益率']
df.dropna(inplace=True)

for y in ['2013','2014','2015','2016','2017','2018','2019','2020']:
    df_=df[[True if i.split('-')[0]==y else False for i in df.index]]
    #df_=df
    x1 = df_[["MKT","SMB","HML"]]
    y1 = df_.iloc[:,-1]
    X = sm.add_constant(x1)
    model = sm.OLS(y1,X).fit()

    #l = df_['超额收益']-model.params['MKT']*df_['MKT']-model.params['SMB']*df_['SMB']-model.params['HML']*df_['HML']
    #l = df_['超额收益']-model.params['MKT']*df_['MKT']
    l = df_['超额收益']-model.params['SMB']*df_['SMB']-model.params['HML']*df_['HML']
    p = 1
    for i in range(len(l)):
        p *= 1+l[i]
    print(y, p-1)
