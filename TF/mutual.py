# coding=utf-8
import pandas as pd
import numpy as np
from WindPy import w
import time
import datetime
import os

def del_eql(df):
    while df.iloc[0][0] == df.iloc[1][0]:
        df = df.drop(df.index[0])
    return df

w.start()
w.isconnected()

today_date = datetime.date.today()
today_date = w.tdaysoffset(-1, today_date).Data[0][0]

def run(fund_code):
    result = w.wsd(fund_code, "NAV_adj,sec_name,fund_fundmanageroftradedate", "2010-01-01", today_date, "Fill=Previous;PriceAdj=F")
    df = pd.DataFrame(result.Data, columns=result.Times).transpose()
    fund_name = df.iloc[0,1]
    manager = df.iloc[-1,2]
    df = df.iloc[:,0:1]
    df.dropna(inplace=True)
    df = del_eql(df)
    df.columns = [fund_name+'('+manager+')']

    df.to_csv('D:\\TF\\公募数据\\'+fund_code+' '+fund_name+'.csv', encoding='gbk')

while True:
    fund_code = input("请输入wind id：")
    if '.' not in fund_code:
        fund_code += '.OF'
    run(fund_code)

# if __name__ == '__main__':
#     files = os.listdir('D:\\TF\\公募数据')
#     for f in files:
#         id = f.split(' ')[0]
#         run(id)
