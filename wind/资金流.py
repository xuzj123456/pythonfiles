# coding=utf-8
from WindPy import w
import time
import datetime
import pandas as pd
import pymysql
from configuration import *

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

w.start()
w.isconnected()

t = datetime.date.today()
result = w.edb("M0329501,M0329505,M0329497,M0329499,M0075987,M0075988,M0075989",
               "2015-01-01", t, "Fill=blank")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
df.fillna(0, inplace=True)
df.set_axis(['沪市港股通:当日资金净流入(人民币)', '深市港股通:当日资金净流入(人民币)',
             '沪股通:当日资金净流入(人民币)', '深股通:当日资金净流入(人民币)', '融资买入额',
             '融券卖出额','融资融券交易金额'],
            axis='columns', inplace=True)

def handle_sql(sql):
    try:
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)

for i in range(len(df.index)):
    sql = "INSERT INTO 资金流_日 VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}');".format(df.index[i],
                                                                                             df.iloc[i:i+1, 0].values[0],
                                                                                             df.iloc[i:i+1, 1].values[0],
                                                                                             df.iloc[i:i+1, 2].values[0],
                                                                                             df.iloc[i:i+1, 3].values[0],
                                                                                             df.iloc[i:i+1, 4].values[0],
                                                                                             df.iloc[i:i+1, 5].values[0],
                                                                                             df.iloc[i:i+1, 6].values[0])
    handle_sql(sql)
