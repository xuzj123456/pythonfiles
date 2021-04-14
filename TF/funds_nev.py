import pymysql
import numpy as np
import pandas as pd
import time
import os
os.chdir(r"D:\TF\定量评估\凯丰\数据")
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
    df.index = pd.to_datetime(df.index, format='YY-mm-dd')
    # 关闭游标
    db.close()
    return df


fundid_all = pd.read_excel('产品及id-全.xlsx', header=0, index_col=None)
fund_name = input("请输入公司或产品类别：")
fundids = fundid_all[fundid_all.iloc[:,0] == fund_name]
fundids = fundids.loc[:,'id'].tolist()


# 读取单个基金净值数据
names = locals()
writer = pd.ExcelWriter(f'{fund_name}.xlsx', datetime_format='YYYY-MM-DD')
for i,fundid in enumerate(fundids):
    sql = "SELECT statistic_date,swanav,fund_name FROM t_fund_nv_data_zyyx WHERE fund_id =" + str(fundid)
    df = execude_sql(sql)
    num = 3*i+1
    df.to_excel(writer, startcol = num)
writer.save()
