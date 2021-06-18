# coding=utf-8
import pandas as pd
import numpy as np

df = pd.read_excel(r'C:\Users\xuzij\Downloads\兴全社会价值三年持有-行业配置.xlsx')
df.dropna(inplace=True)
df=df.pivot(index='报告期', columns='行业名称', values='本期').transpose()
df.replace()
df.to_csv('1.csv', encoding='gbk')