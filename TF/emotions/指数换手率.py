# coding=utf-8
from configuration import *

table_name = '指数换手率_日'

try:
    max_date = engine.execute("SELECT max(日期) FROM {0};".format(table_name)).fetchall()[0][0]
    if not max_date == None:
        start_date = w.tdaysoffset(-1, max_date).Data[0][0]
except:
    pass

# 指数_日
list_2 = ['换手率_上证综合指数', '换手率_深证成份指数',
             '换手率_创业板指数','换手率_上证50指数','换手率_沪深300指数','换手率_中证500指数']
list_2_code = "M0331169,M0331175,M0331181,M0331174,M0331172,M0331184"

result = w.edb(list_2_code, start_date, today_date, "Fill=blank")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
# df.dropna(inplace=True)
df.set_axis(list_2,axis='columns', inplace=True)
df.index.name = '日期'

save_(engine, table_name, df)