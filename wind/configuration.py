# coding=utf-8
from WindPy import w
import time
import datetime
import pandas as pd
import numpy as np
from scipy.signal import detrend
import pymysql
import talib as ta
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.cross_decomposition import PLSRegression

# 连接数据库
try:
    engine = create_engine('mysql+mysqldb://root:13579@localhost:3306/emotions?charset=utf8')
except Exception as e:
    print('数据库连接失败，3s后重试')
    print(e)
    time.sleep(3)

# 连接数据库
# try:
#     con = pymysql.connect(host='localhost',
#                          port=3306,
#                          user='root',
#                          passwd='13579',
#                          db='emotions',
#                          charset='utf8')
# except Exception as e:
#     print('数据库连接失败，3s后重试')
#     print(e)
#     time.sleep(3)
# # 创建游标
# cursor = con.cursor()


# 连接万得
w.start()
w.isconnected()

start_date = datetime.date(2015,1,1)

# 今天日期
today_date = datetime.date.today()
# 上一个交易日日期  last trading date
last_t_d = w.tdaysoffset(-1, today_date).Data[0][0]
last_t_d = datetime.date(last_t_d.year,last_t_d.month,last_t_d.day)


# 得到所有A股code
def get_allAstock_code(date):
    #所有a股code
    all_a = w.wset("SectorConstituent", date = date ,sector=u"全部A股")
    all_Code = list(pd.Series(all_a.Data[1]))
    #停牌股code
    all_tp = w.wset("TradeSuspend",startdate = date,enddate = date,field = "wind_code,sec_name,suspend_type,suspend_reason")
    all_tp_code = list(pd.Series(all_tp.Data[0]))
    #所有st股code
    all_st = w.wset("SectorConstituent",date=date,sector=u"风险警示股票",field="wind_code,sec_name")
    all_st_code = list(pd.Series(all_st.Data[0]))

    all_Code = set(all_Code)
    all_st_code = set(all_st_code)
    all_tp_code = set(all_tp_code)
    code = all_Code - all_tp_code - all_st_code
    return list(code)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

#####################################################################################

# sql设置主键 primary key
def SQL_PK(table_name):
    SQL = '''
    ALTER TABLE `{0}` 
    CHANGE COLUMN `日期` `日期` DATE NOT NULL ,
    ADD PRIMARY KEY (`日期`),
    ADD UNIQUE INDEX `日期_UNIQUE` (`日期` DESC) VISIBLE;
    '''.format(table_name)
    return SQL

def save_(table_name, df):
    try:
        data = engine.execute("SELECT * FROM {0};".format(table_name)).fetchall()
        data = pd.DataFrame(data)[0]
        l = [i not in list(data) for i in df.index]
        df_insert = df[l]
        df_insert.to_sql(table_name, con=engine, if_exists='append')
    except Exception as e:
        if e.__cause__.args[0] == 1146:
            df.to_sql(table_name, con=engine, if_exists='append')
            engine.execute(SQL_PK(table_name))
            print('\n')
            print('Table {0} created succesfully.'.format(table_name))
        else:
            print(e)