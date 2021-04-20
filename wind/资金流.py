# coding=utf-8
from configuration import *

table_name = '资金流_日'

max_date = engine.execute("SELECT max(日期) FROM {0};".format(table_name)).fetchall()[0][0]
if not max_date == None:
    start_date = w.tdaysoffset(-1, max_date).Data[0][0]

# 资金流_日
list_1 = ['沪市港股通:当日资金净流入(人民币)', '深市港股通:当日资金净流入(人民币)',
             '沪股通:当日资金净流入(人民币)', '深股通:当日资金净流入(人民币)', '融资买入额',
             '融券卖出额','融资融券交易金额']
list_1_code = "M0329501,M0329505,M0329497,M0329499,M0075987,M0075988,M0075989"


result = w.edb(list_1_code, start_date, today_date, "Fill=blank")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
df.dropna(inplace=True)
df.set_axis(list_1,
            axis='columns', inplace=True)
df.index.name = '日期'

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
