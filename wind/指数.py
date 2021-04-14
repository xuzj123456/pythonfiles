# coding=utf-8
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
result = w.edb("M0331169,M0331175,M0331181,M0331174,M0331172,M0331184", "2010-01-01", t,"Fill=Previous")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
df.dropna()
df.set_axis(['换手率:上证综合指数', '换手率:深证成份指数',
             '换手率:创业板指数','换手率:上证50指数','换手率:沪深300指数','换手率:中证500指数'],
            axis='columns', inplace=True)

def handle_sql(sql):
    try:
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)

for i in range(len(df.index)):
    sql = "INSERT INTO 指数_日 VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}');".format(df.index[i],
                                                                                      df.iloc[i:i+1, 0].values[0],
                                                                                      df.iloc[i:i+1, 1].values[0],
                                                                                      df.iloc[i:i+1, 2].values[0],
                                                                                      df.iloc[i:i+1, 3].values[0],
                                                                                      df.iloc[i:i+1, 4].values[0],
                                                                                      df.iloc[i:i+1, 5].values[0])
    handle_sql(sql)
