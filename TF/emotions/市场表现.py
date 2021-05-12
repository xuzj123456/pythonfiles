# coding=utf-8
from configuration import *

table_name = '市场表现_日'

try:
    max_date = engine.execute("SELECT max(日期) FROM {0};".format(table_name)).fetchall()[0][0]
    if not max_date == None:
        start_date = w.tdaysoffset(-1, max_date).Data[0][0]
        # 如果只有一天，之后取数据时容易报错
except:
    pass

# 市场表现_日
list_3 = ['上证所_市场总成交金额',
             '深交所_市场总成交金额']
list_3_code = "G8324475,G8324488"

result = w.edb(list_3_code, start_date, today_date, "Fill=blank")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
#df.dropna(inplace=True)
df.set_axis(list_3,axis='columns', inplace=True)
df['上证成交变化']=df.iloc[:,0].diff()
df['深交成交变化']=df.iloc[:,1].diff()
df['沪深成交总额']=df.iloc[:,0]+df.iloc[:,1]
df['沪深成交变化']=df['沪深成交总额'].diff()
df.dropna(inplace=True)
df.index.name = '日期'

save_(engine, table_name, df)
