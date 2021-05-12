# coding=utf-8
from configuration import *

try:
    engine = create_engine('mysql+mysqldb://root:13579@localhost:3306/stock_index?charset=utf8')
    print('Connect success.')
except Exception as e:
    print('数据库连接失败，3s后重试')
    print(e)
    time.sleep(3)

# IC中证500, IF沪深300,IH上证50
# 分别为当月，下月，下季，隔季连续合约
table_names = ["IC00.CFE", "IC01.CFE", "IC02.CFE", "IC03.CFE",
               "IF00.CFE", "IF01.CFE", "IF02.CFE", "IF03.CFE",
               "IH00.CFE", "IH01.CFE", "IH02.CFE", "IH03.CFE",]
start_date = datetime.date(2010,1,1)

try:
    max_date = \
        [engine.execute("SELECT max(日期) FROM {0};".format(i)).fetchall()[0][0] for i in table_names]
    max_date = min(max_date)
    if not max_date == None:
        start_date = w.tdaysoffset(-251, max_date).Data[0][0]
except:
    pass

for table in table_names:
    result = w.wsd(table, "close,if_basis", start_date, today_date, "")
    df=pd.DataFrame(result.Data, columns=result.Times).transpose()
    df.set_axis(['收盘价', '基差'], axis='columns', inplace=True)
    df.index.name = '日期'
    df['指数']=df['收盘价']-df['基差']  # 基差=期货-现货
    df['贴水率']=df['基差']/df['指数']
#    df.dropna(inplace=True)
    save_(engine, table.split('.')[0]+'_'+table.split('.')[1].lower(), df)
