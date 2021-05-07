# coding=utf-8
from configuration import *

table_name = '宏观_月'

list_m = ['上证所_A股账户新增开户数_合计', '消费者信心指数_月', '投资者信心指数_总指数', '投资者信心指数_买入_BII','工业增加值_当月同比']
list_m_code = "M0010401,M0012303,M5452815,M5452823,M0000545"

result = w.edb(list_m_code, start_date, today_date, "Fill=Previous")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
df.dropna(inplace=True)
df.set_axis(list_m, axis='columns', inplace=True)
df.index.name = '日期'

save_(table_name, df)
