# coding=utf-8
from WindPy import w
import time
import datetime
import pandas as pd
import pymysql

# 数据库参数
host='localhost'
port=3306
user='root'
passwd='13579'
db='emotions'
charset='utf8'

# 连接万得
w.start()
w.isconnected()

# 所有交易日期
dates = w.tdays('2010-01-01', Period="D").Data[0]
dates = [datetime.date(d.year,d.month,d.day) for d in dates]

# 今天日期
t = datetime.date.today()

# 连接数据库
try:
    con = pymysql.connect(host=host,
                         port=port,
                         user=user,
                         passwd=passwd,
                         db=db,
                         charset=charset)
except Exception as e:
    print('数据库连接失败，3s后重试')
    print(e)
    time.sleep(3)
# 创建游标
cursor = con.cursor()

# 得到所有A股code
def get_allAstock_code():
    #所有a股
    all_a = w.wset("SectorConstituent",date = datetime.date.today() ,sector=u"全部A股")
    all_Code = list(pd.Series(all_a.Data[1]))
    #停牌股
    all_tp = w.wset("TradeSuspend",startdate = date,enddate = date,field = "wind_code,sec_name,suspend_type,suspend_reason")
    all_tp_code = list(pd.Series(all_tp.Data[0]))
    #所有st
    all_st = w.wset("SectorConstituent",date=date,sector=u"风险警示股票",field="wind_code,sec_name")
    all_st_code = list(pd.Series(all_st.Data[0]))
    all_Code = set(all_Code)
    all_st_code = set(all_st_code)
    all_tp_code = set(all_tp_code)
    code = all_Code - all_tp_code - all_st_code
    return list(code)

#####################################################################################

# 资金流_日
list_1 = ['沪市港股通:当日资金净流入(人民币)', '深市港股通:当日资金净流入(人民币)',
             '沪股通:当日资金净流入(人民币)', '深股通:当日资金净流入(人民币)', '融资买入额',
             '融券卖出额','融资融券交易金额']
list_1_code = "M0329501,M0329505,M0329497,M0329499,M0075987,M0075988,M0075989"

# 指数_日
list_2 = ['换手率:上证综合指数', '换手率:深证成份指数',
             '换手率:创业板指数','换手率:上证50指数','换手率:沪深300指数','换手率:中证500指数']
list_2_code = "M0331169,M0331175,M0331181,M0331174,M0331172,M0331184"

# 市场表现_日
list_3 = ['上证所:市场总成交金额',
             '深交所:市场总成交金额']
list_3_code = "G8324475,G8324488"




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