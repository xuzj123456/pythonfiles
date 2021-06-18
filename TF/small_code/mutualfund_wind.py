# coding=utf-8
from WindPy import w
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

w.start()
w.isconnected()

file_1 = '行业配置变化.xlsx'
file_2 = '富国天益价值A-重仓持股.xlsx'
file_3 = '富国天益价值A-资产配置.xlsx'
code = '009342.OF'
start_d = datetime.date(2014,4,8)

result = w.wsd(code, "name_official", "2021-01-01", "2021-01-04")
name = result.Data[0][0]
today_d = datetime.date.today()


# 换手率
df = pd.DataFrame(columns=['年份', '换手率'])
for y in range(start_d.year, today_d.year+1):
    result = w.wsd(code, "style_rpt_turn", "2021-01-01", "2021-03-31", "year={0};Intervaltype=3;Period=Q".format(y))
    data = result.Data[0][0]
    if data != None:
        df=df.append(pd.Series([int(y), data], index=df.columns), ignore_index=True)

if not os.path.exists('result/'+name):
    os.mkdir('result/'+name)

df.to_excel('result/'+name+'/换手率.xlsx', index=False)
plt.plot(df['年份'], df['换手率'])
plt.title('年换手率')
plt.savefig('result/'+name+'/换手率.png')
plt.close()


#十大重仓行业
df_1 = pd.read_excel('data/'+file_1).iloc[1:-2, [0,3,5]]
df_1 = df_1.pivot(index='行业名称', columns='报告期')
df_1.columns = [c[1] for c in df_1.columns]
df_1.sort_values(by=df_1.columns[-1], ascending=False, inplace=True)
df_1 = df_1.replace(np.nan, '--')

writer = pd.ExcelWriter('result/'+name+'/十大重仓行业.xlsx')
df_1.to_excel(writer, sheet_name='sheet1')
df_1_ = df_1.loc[:,[c for c in df_1.columns if c[5:7] == '12']]
df_1_.to_excel(writer, sheet_name='sheet2')
writer.save()


# 十大重仓个股
df_3 = pd.read_excel('data/'+file_2).iloc[:-2]
df_3_ = pd.DataFrame([['']*3*len(set(df_3['报告期']))]*10,
                     columns=pd.MultiIndex.from_product([df_3['报告期'].drop_duplicates(),['股票名称', '所属行业', '占基金净值比(%)']]))

df_3 = df_3.loc[:, ['报告期', '股票名称', '所属行业', '占基金净值比(%)']]
for i in df_3['报告期'].drop_duplicates():
    df_ = df_3[df_3['报告期']==i]
    for j in range(10):
        df_3_._set_value(j, (i, '股票名称'), df_['股票名称'].values[j])
        df_3_._set_value(j, (i, '所属行业'), df_['所属行业'].values[j])
        df_3_._set_value(j, (i, '占基金净值比(%)'), df_['占基金净值比(%)'].values[j])

df_3_.to_excel('result/'+name+'/十大重仓股.xlsx')


#持仓集中度
df_2 = df_3[df_3['股票名称']=='--'].loc[:,['报告期', '占基金净值比(%)']]
df_2.columns = ['日期', '持仓集中度']
df_2.to_excel('result/'+name+'/持仓集中度.xlsx')

# 资产配置
df_4 = pd.read_excel('data/'+file_3).iloc[:-2].transpose()
df_4.columns = df_4.iloc[0]
df_4.drop(['报告期'], inplace=True)
df_4 = df_4.loc[:,['公告日期', '基金资产净值(元)', '        股票市值占基金资产净值比例(%)',
     '        债券市值占基金资产净值比例(%)', '        银行存款占基金资产净值比例(%)', '        其他资产占基金资产净值比例(%)']]
df_4.columns = ['公告日期', '总净值（亿元）', '股票占净比', '债券占净比', '银行存款占净比', '其他资产占净比']
df_4['总净值（亿元）'] = df_4['总净值（亿元）']/100000000
df_4.to_excel('result/'+name+'/资产配置.xlsx', index=False)
