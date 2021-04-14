import pymysql
import numpy as np
import pandas as pd
import time
import os
os.chdir(r"D:\TF\定量评估\同温层\数据")
# 连接朝阳永续数据库提取产品净值数据
def execude_sql(sql):
    # 创建连接
    try:
        db = pymysql.connect(host = '106.75.45.237', 
                             port = 15630, 
                             user = 'simu_tfzqzg', 
                             passwd = 'nvj64PsxhfN5gHDf', 
                             db = 'CUS_FUND_DB', 
                             charset = 'utf8')
    except:
        print('数据库连接失败，3s后重试')
        time.sleep(3)
    # 创建游标
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    fund_name = result[0][2];
    # 转成dataframe格式
    df = pd.DataFrame(result, columns=["日期",fund_name,'产品名称']).set_index('日期')
    df = df.loc[:,[fund_name]]
    df[fund_name] = df[fund_name].apply(lambda x: np.float(x))
    df.index = pd.to_datetime(df.index)
    # 关闭游标
    db.close()
    while df.iloc[0][0] == df.iloc[1][0]:
        df = df.drop(df.index[0])
    return df

while(True):
    # 读取单个基金净值数据
    fund_id = input("请输入朝阳永续id：")
    sql = "SELECT statistic_date,swanav,fund_name FROM t_fund_nv_data_zyyx WHERE fund_id =" + str(fund_id)
    df = execude_sql(sql)
    # df = df.drop(df.index[0])
    # 存储数据
    df.to_csv(''.join(df.columns)+'.csv',encoding = "utf_8_sig")