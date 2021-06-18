# coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import time
import datetime
import statsmodels.api as sm
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.cross_decomposition import PLSRegression
import numpy as np
from scipy.signal import detrend
import sqlalchemy
import os

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

try:
    engine = create_engine('mysql+mysqldb://root:13579@localhost:3306/emotions?charset=utf8')
    print('Connect success.')
except Exception as e:
    print('数据库连接失败，3s后重试')
    print(e)
    time.sleep(3)

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

def save_(engine, table_name, df):
    try:
        data = engine.execute("SELECT * FROM {0};".format(table_name)).fetchall()
        data = pd.DataFrame(data)[0]
        l = [i not in list(data) for i in df.index]
        df_insert = df[l]
        df_insert.to_sql(table_name, con=engine, if_exists='append')
    except Exception as e:
        if e.__cause__.args[0] in [1146, 1049]:
            df.to_sql(table_name, con=engine, if_exists='append')
            engine.execute(SQL_PK(table_name))
            print('\n')
            print('Table {0} created succesfully.'.format(table_name))
        else:
            print(e)

# 获取列名
# md = sqlalchemy.MetaData()
# table = sqlalchemy.Table('资金流_日', md, autoload=True, autoload_with=engine)
# columns = table.c

