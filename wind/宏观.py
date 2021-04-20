# coding=utf-8
from configuration import *

table_name = '宏观_月'

list_m = ['上证所:A股账户新增开户数:合计', '消费者信心指数(月)', '投资者信心指数:总指数']
list_m_code = "M0010401,M0012303,M5452815"

result = w.edb(list_m_code, start_date, today_date, "Fill=blank")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
df.dropna(inplace=True)
df.set_axis(list_m, axis='columns', inplace=True)
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