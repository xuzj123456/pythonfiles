# coding=utf-8
from configuration import *

table_name = '资金流_日'

try:
    max_date = engine.execute("SELECT max(日期) FROM {0};".format(table_name)).fetchall()[0][0]
    if not max_date == None:
        start_date = w.tdaysoffset(-1, max_date).Data[0][0]
except:
    pass

# 资金流_日
list_1 = ['沪市港股通_当日资金净流入_人民币', '深市港股通_当日资金净流入_人民币',
             '沪股通_当日资金净流入_人民币', '深股通_当日资金净流入_人民币', '融资买入额',
             '融券卖出额','融资融券交易金额','融资融券余额']
list_1_code = "M0329501,M0329505,M0329497,M0329499,M0075987,M0075988,M0075989,M0075992"


result = w.edb(list_1_code, start_date, today_date, "Fill=blank")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
# df.dropna(inplace=True)
df.set_axis(list_1,
            axis='columns', inplace=True)
df.index.name = '日期'
df['北上资金净流入']=df['沪股通_当日资金净流入_人民币']+df['深股通_当日资金净流入_人民币']
df['融资融券余额变化率']=df['融资融券余额'].pct_change()

save_(engine, table_name, df)