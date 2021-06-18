# coding=utf-8
from Alpha_101 import *

df = pd.read_csv('沪深300.csv', index_col=0, encoding='gbk')
df.vwap = df.vwap*300

df.dropna(inplace = True)

corr = df.corr().iloc[2,27:]
corr.name = 'corr'
corr.sort_values(inplace=True,ascending=False)
corr.to_csv('corr.csv', encoding='gbk')