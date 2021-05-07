# coding=utf-8
from configuration import *
### 注意，wset函数只能提取一年数据，从enddate往前一年
### 注意不要再收盘之后马上更新，涨跌停数据有可能会变成0

table_name = '涨跌停_日'

list_ = ['沪深两市上涨家数','沪深两市平盘家数','沪深两市下跌家数', '沪深两市涨停家数','沪深两市跌停家数']

result = w.wset("numberofchangeinshandsz",
                "startdate={0};enddate={1};securitytype=万得全A;field=reportdate,risenumberofshandsz,noriseorfallnumberofshandsz,fallnumberofshandsz,limitupnumofshandsz,"
                "limitdownnumofshandsz".format(start_date, today_date))
df = pd.DataFrame(result.Data[1:], columns=result.Data[0]).transpose()
df.dropna(inplace=True)
df.set_axis(list_,axis='columns', inplace=True)
df.index.name = '日期'

df['沪深两市涨跌家数比例'] = df['沪深两市上涨家数']/df['沪深两市下跌家数']
df['沪深两市总交易家数']=df['沪深两市上涨家数']+df['沪深两市平盘家数']+df['沪深两市下跌家数']
df['沪深两市涨停家数占比']=df['沪深两市涨停家数']/df['沪深两市总交易家数']
df['沪深两市上涨家数占比']=df['沪深两市上涨家数']/df['沪深两市总交易家数']

save_(table_name, df)
