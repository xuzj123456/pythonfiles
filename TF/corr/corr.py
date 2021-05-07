# coding=utf-8
import os
import pandas as pd
from WindPy import w
import datetime
from shutil import copyfile

w.start()
w.isconnected()

t_weeks=w.tdays("2015-01-01", datetime.date.today(),"Period=W")
t_weeks = [datetime.date(t.year,t.month,t.day) for t in t_weeks.Data[0]]
t_weeks = [str(t) for t in t_weeks]

date = datetime.date(2019,3,22)
file = 'data/'+'311744 众智对冲一号.csv'

if 'xlsx' in file or 'xls' in file:
    df = pd.read_excel(file, index_col=0)
else:
    df = pd.read_csv(file, index_col=0)
df.index = [str(s).split(' ')[0] for s in df.index]

for t in df.index:
    if t not in t_weeks:
        df.drop(t, axis=0, inplace=True)
df.drop(df.columns[1:],axis=1, inplace=True)

p_data = r'D:\TF\基金净值汇总'
files = os.listdir(p_data)

def str2date(l):
    l=l.to_numpy()
    if '-' in l[0]:
        for i in range(len(l)):
            y = int(l[i].split('-')[0])
            m = int(l[i].split('-')[1])
            d = int(l[i].split('-')[2])
            date = datetime.date(y,m,d)
            l[i] = date
    elif '/' in l[0]:
        for i in range(len(l)):
            y = int(l[i].split('/')[0])
            m = int(l[i].split('/')[1])
            d = int(l[i].split('/')[2])
            date = datetime.date(y,m,d)
            l[i] = date

str2date(df.index)

def cal_corr(df,df2,date):
    df_ = df.join(df2,how='left')
    df_ = df_[df_.index >= max(df.index[0],df2.index[0])]
#    df_ = df_[df_.index >= date]
    x = df_.isnull().sum().sum()
    if x >= 10:
        return 0
    df_.dropna(inplace=True)
    df_['1']=df_.iloc[:,0].pct_change()
    df_['2'] = df_.iloc[:, 1].pct_change()
    df_.dropna(inplace=True)
    return df_.iloc[:,2:].corr().iloc[0][1]

corr_df = pd.DataFrame(columns=['corr'])

for i in range(len(files)):
    df2 = pd.read_csv(os.path.join(p_data, files[i]), index_col=0)
    str2date(df2.index)
    df2['begin_date'] = ''
    if df.columns[0] != df2.columns[0]:
        corr = cal_corr(df,df2,date)
        corr_df.loc[files[i], 'corr'] = corr
        corr_df.loc[files[i],'begin_date'] = df2.index[0]

corr_df.dropna(inplace=True)

f_id = 't_fund_info.xlsx'
df_id  = pd.read_excel(f_id)
corr_df['fund_id'] = [s.split(' ')[0] for s in corr_df.index]
corr_df['name'] = [s.split(' ')[1] for s in corr_df.index]
df_id['fund_id'] = [str(i) for i in df_id['fund_id']]
corr_df=pd.merge(corr_df, df_id, how='left', on='fund_id')

f_type = '产品业绩跟踪 20210325【私募+公募】.xlsx'
df_type = pd.read_excel(f_type, sheet_name='私募')
corr_df=pd.merge(corr_df, df_type, how='left', left_on='fund_name', right_on='跟踪产品')

corr_df.sort_values(by='corr',inplace=True,ascending=False)
corr_df = corr_df.loc[:,['corr','name', 'fund_name', 'fund_id', '策略细分','fund_type_strategy','begin_date']]
print(corr_df.head(30))

type='管理期货复合'
l = corr_df[corr_df['策略细分']==type]
def fun1(type=type):
    l = corr_df[corr_df['策略细分']==type]
    for i in range(min(10,len(l))):
        name = l.loc[l.index[i], 'fund_id']+' '+l.loc[l.index[i], 'name']
        copyfile(os.path.join(p_data, name),
                 r'data2/'+name)

def delete():
    files = os.listdir('data2')
    for f in files:
        os.remove('data2/'+f)

corr_df.drop('fund_name', axis=1).to_csv('corr.csv', encoding='gbk')
