# coding=utf-8
from configuration import *
### 注意，wset函数只能提取一年数据

table_name = '涨跌停_日'

list_ = ['沪深两市上涨家数' ,'沪深两市下跌家数', '沪深两市涨停家数','沪深两市跌停家数']

result = w.wset("numberofchangeinshandsz",
                "startdate={0};enddate={1};securitytype=万得全A;field=reportdate,risenumberofshandsz,fallnumberofshandsz,limitupnumofshandsz,"
                "limitdownnumofshandsz".format(start_date, today_date))
df = pd.DataFrame(result.Data[1:], columns=result.Data[0]).transpose()
df.dropna(inplace=True)
df.set_axis(list_,axis='columns', inplace=True)
df.index.name = '日期'

df['沪深两市涨跌家数比例'] = df['沪深两市上涨家数']/df['沪深两市下跌家数']

# 首次运行创建表运行：
# df.to_sql(table_name, con=engine, if_exists='append')

try:
    data = engine.execute("SELECT * FROM {0};".format(table_name)).fetchall()
    if len(data) != 0:
        data = pd.DataFrame(data)[0]
        l = [i not in list(data) for i in df.index]
        df_insert = df[l]
        df_insert.to_sql(table_name, con=engine, if_exists='append')
    else:
        df.to_sql(table_name, con=engine, if_exists='append')
except Exception as e:
    print(e)
