# coding=utf-8
from configuration import *

table_names = ['上证指数_arbr', '上证50_arbr', '沪深300_arbr', '深证成指_arbr', '中证500_arbr']
max_date = \
    [engine.execute("SELECT max(日期) FROM {0};".format(i)).fetchall()[0][0] for i in table_names]
max_date = min(max_date)
if not max_date == None:
    start_date = w.tdaysoffset(-26, max_date).Data[0][0]

# 上证指数
result = w.wsd("000001.SH", "pre_close,open,close,high3,low3", start_date, today_date, "PriceAdj=F")
szzs = pd.DataFrame(result.Data, columns=result.Times).transpose()
szzs.set_axis(['前收盘价','开盘价','收盘价','最高价','最低价'], axis='columns', inplace=True)
szzs.index.name = '日期'

# 沪深300
result = w.wsd("399300.SZ", "pre_close,open,close,high3,low3", start_date, today_date, "PriceAdj=F")
hs300 = pd.DataFrame(result.Data, columns=result.Times).transpose()
hs300.set_axis(['前收盘价','开盘价','收盘价','最高价','最低价'], axis='columns', inplace=True)
hs300.index.name = '日期'

# 上证50
result = w.wsd("000016.SH", "pre_close,open,close,high3,low3", start_date, today_date, "PriceAdj=F")
sz50 = pd.DataFrame(result.Data, columns=result.Times).transpose()
sz50.set_axis(['前收盘价','开盘价','收盘价','最高价','最低价'], axis='columns', inplace=True)
sz50.index.name = '日期'

# 深证成值
result = w.wsd("000016.SH", "pre_close,open,close,high3,low3", start_date, today_date, "PriceAdj=F")
szcz = pd.DataFrame(result.Data, columns=result.Times).transpose()
szcz.set_axis(['前收盘价','开盘价','收盘价','最高价','最低价'], axis='columns', inplace=True)
szcz.index.name = '日期'

# 中证500
result = w.wsd("159982.SZ", "pre_close,open,close,high3,low3", max(start_date, datetime.datetime(2020,2,20)),
               today_date, "PriceAdj=F")
# 中证500最早数据从2020-2-20开始
zz500 = pd.DataFrame(result.Data, columns=result.Times).transpose()
zz500.set_axis(['前收盘价','开盘价','收盘价','最高价','最低价'], axis='columns', inplace=True)
zz500.index.name = '日期'

for df in [szzs, hs300, sz50, szcz, zz500]:
    df['HO']=df['最高价']-df['开盘价']
    df['OL']=df['开盘价']-df['最低价']
    df['HCY']=df['最高价']-df['收盘价'].shift(1)
    df['CYL']=df['收盘价'].shift(1)-df['最低价']

    df['AR']=ta.SUM(df.HO, timeperiod=26)/ta.SUM(df.OL, timeperiod=26)*100
    df['BR']=ta.SUM(df.HCY, timeperiod=26)/ta.SUM(df.CYL, timeperiod=26)*100
    df.dropna(inplace=True)

def plot_ARBR(df):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plot1 = ax1.plot(df['AR'], color='y', label='AR')
    plot2 = ax1.plot(df['BR'], color='r', label='BR')

    ax2 = ax1.twinx()
    plot3 = ax2.plot(df['收盘价'], color='b', label='close(right)')
    lines = plot1 + plot2 + plot3
    plt.legend(lines, [l.get_label() for l in lines])

# 首次运行创建表运行：
# df.to_sql(table_name, con=engine, if_exists='append')

for df, table_name in zip([szzs, hs300, sz50, szcz, zz500], table_names):
    try:
        data = engine.execute("SELECT * FROM {0};".format(table_name)).fetchall()
        data = pd.DataFrame(data)[0]
        l = [i not in list(data) for i in df.index]
        df_insert = df[l]
        df_insert.to_sql(table_name, con=engine, if_exists='append')
    except Exception as e:
        print(e)
