# coding=utf-8
from configuration import *

table_name = 'factors1'

try:
    max_date = engine.execute("SELECT max(日期) FROM {0};".format(table_name)).fetchall()[0][0]
    if not max_date == None:
        start_date = w.tdaysoffset(-1, max_date).Data[0][0]
        # 如果只有一天，之后取数据时容易报错
except:
    pass

list_c = ['中证全指','中证500','中证100','中证800价值','中证800成长']

result = w.wsd("000985.CSI,000905.SH,000903.SH,H30356.CSI,H30355.CSI", "close", start_date, today_date, "")
df = pd.DataFrame(result.Data, columns=result.Times).transpose()
df.columns = list_c
df.index.name = '日期'

for c in df.columns:
    df[c+'收益率'] = df[c].pct_change()

result_ = w.edb("S0059749", start_date, today_date,"Fill=blank")
df_ = pd.DataFrame(result_.Data, columns=result_.Times).transpose()
df_.columns = ['10年国债收益率']

df=df.join(df_)

df['10年国债收益率'] = df['10年国债收益率']/(252*100)
df['MKT']=df['中证全指收益率']-df['10年国债收益率']
df['SMB']=df['中证500收益率']-df['中证100收益率']
df['HML']=df['中证800价值收益率']-df['中证800成长收益率']

save_(engine, table_name, df)