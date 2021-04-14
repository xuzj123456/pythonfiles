# coding=utf-8
import pymysql
import numpy as np
import pandas as pd
import time
import datetime
import dateutil.relativedelta
from WindPy import w
w.start()
w.isconnected()

asset_list = ['达尔文明德一号','九坤量化对冲5号A期', '天演6号']

def del_eql(df):
    while df.iloc[0][0] == df.iloc[1][0]:
        df = df.drop(df.index[0])
    return df

# 连接朝阳永续数据库提取产品净值数据
def execude_sql(sql):
    """
    连接朝阳永续数据库
    """  # 创建连接
    try:
        db = pymysql.connect(host='106.75.45.237',
                             port=15630,
                             user='simu_tfzqzg',
                             passwd='nvj64PsxhfN5gHDf',
                             db='CUS_FUND_DB',
                             charset='utf8')
    except:
        print('数据库连接失败，3s后重试')
        time.sleep(3)
    # 创建游标
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    fund_name = result[0][2]
    # 转成dataframe格式
    df = pd.DataFrame(result, columns=["日期", fund_name, '产品名称']).set_index('日期')
    df = df.loc[:, [fund_name]]
    df[fund_name] = df[fund_name].apply(lambda x: np.float(x))
    df.index = pd.to_datetime(df.index)
    # 关闭游标
    db.close()
    return df

def get_zyyx_nev(fundid):
    sql = "SELECT statistic_date,swanav,fund_name FROM t_fund_nv_data_zyyx WHERE fund_id =" + str(fundid)
    df = execude_sql(sql)
    df = df.drop(df.index[0])
    return df
    # df.to_csv(''.join(df.columns)+'.csv',encoding = "utf_8_sig")


def get_wind_nev(windid, fre="日"):
    """
    获取wind基金数据
    """
    date = w.wss(windid, "fund_setupdate,NAV_date").Data
    start_date = date[0][0].strftime('%Y-%m-%d')
    end_date = date[1][0].strftime('%Y-%m-%d')
    fund_name = w.wss(windid, "name_official").Data[0]
    if fre == "周":
        para = "Period=W;Fill=Previous"
    else:
        para = "Period=D;Fill=Previous"
    data = w.wsd(windid, "NAV_adj", start_date, end_date, para)
    df = pd.DataFrame(data.Data[0], index=data.Times, columns=fund_name)
    df.index = pd.to_datetime(df.index)
    return df
    # df.to_csv(''.join(df.columns)+'.csv',encoding = "utf_8_sig")


funds_code = pd.read_excel('产品及id.xlsx', header=0)
asset_code = []
data = pd.DataFrame()
for s in asset_list:
    id = funds_code[funds_code['跟踪产品']==s]['id'].values[0]
    asset_code.append(id)
    df = get_zyyx_nev(id)
    df = del_eql(df)
    if data.empty:
        data = data.append(df)
    else:
        data = data.join(df)
data = data.dropna()

# 读取日期数据
dates_day = pd.read_excel('日期数据.xlsx', sheet_name='日度', index_col=0)
dates_week = pd.read_excel('日期数据.xlsx', sheet_name='周度', index_col=0)
month_end = pd.read_excel('日期数据.xlsx', sheet_name='月末', index_col=0)

