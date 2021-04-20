# coding=utf-8
from WindPy import w
import time
import datetime
import pandas as pd
import pymysql
import talib as ta
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

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

#####################################################################################

# 数据表创建SQL代码
SQL_create = """
CREATE TABLE `emotions`.`资金流_日` (
  `日期` DATE NOT NULL,
  `沪市港股通:当日资金净流入(人民币)` FLOAT NULL,
  `深市港股通:当日资金净流入(人民币)` FLOAT NULL,
  `沪股通:当日资金净流入(人民币)` FLOAT NULL,
  `深股通:当日资金净流入(人民币)` FLOAT NULL,
  `融资买入额` FLOAT NULL,
  `融券卖出额` FLOAT NULL,
  `融资融券交易金额` FLOAT NULL,
  PRIMARY KEY (`日期`),
  UNIQUE INDEX `日期_UNIQUE` (`日期` ASC) VISIBLE);
"""