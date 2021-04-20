# coding=utf-8
from configuration import *

table_name = '指数_日'

max_date = engine.execute("SELECT max(日期) FROM {0};".format(table_name)).fetchall()[0][0]
if not max_date == None:
    start_date = w.tdaysoffset(-1, max_date).Data[0][0]

# 指数_日
list_2 = ['换手率:上证综合指数', '换手率:深证成份指数',
             '换手率:创业板指数','换手率:上证50指数','换手率:沪深300指数','换手率:中证500指数']
list_2_code = "M0331169,M0331175,M0331181,M0331174,M0331172,M0331184"

result = w.edb(list_2_code, start_date, today_date, "Fill=blank")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
df.dropna(inplace=True)
df.set_axis(list_2,axis='columns', inplace=True)
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