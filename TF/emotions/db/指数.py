# coding=utf-8
from configuration import *

try:
    engine = create_engine('mysql+mysqldb://root:13579@localhost:3306/stock_index?charset=utf8')
    print('Connect success.')
except Exception as e:
    print('数据库连接失败，3s后重试')
    print(e)
    time.sleep(3)

table_names = ['上证指数', '沪深300','上证50', '深证成指', '中证500']
start_date = datetime.date(2001,1,1)
try:
    max_date = \
        [engine.execute("SELECT max(日期) FROM {0};".format(i)).fetchall()[0][0] for i in table_names]
    max_date = min(max_date)
    if not max_date == None:
        start_date = w.tdaysoffset(-251, max_date).Data[0][0]
except:
    pass

# 上证指数
result = w.wsd("000001.SH", "pre_close,open,close,high3,low3,volume,amt,vwap", start_date, today_date,
               "PriceAdj=F")
szzs = pd.DataFrame(result.Data, columns=result.Times).transpose()
szzs.set_axis(['前收盘价','开盘价','收盘价','最高价','最低价', '成交量', '成交额','vwap'], axis='columns', inplace=True)
szzs.index.name = '日期'

# 沪深300
result = w.wsd("399300.SZ", "pre_close,open,close,high3,low3,volume,amt,vwap", start_date, today_date, "PriceAdj=F")
hs300 = pd.DataFrame(result.Data, columns=result.Times).transpose()
hs300.set_axis(['前收盘价','开盘价','收盘价','最高价','最低价', '成交量', '成交额','vwap'], axis='columns', inplace=True)
hs300.index.name = '日期'

# 上证50
result = w.wsd("000016.SH", "pre_close,open,close,high3,low3,volume,amt,vwap", start_date, today_date, "PriceAdj=F")
sz50 = pd.DataFrame(result.Data, columns=result.Times).transpose()
sz50.set_axis(['前收盘价','开盘价','收盘价','最高价','最低价', '成交量', '成交额','vwap'], axis='columns', inplace=True)
sz50.index.name = '日期'

# 深证成值
result = w.wsd("399001.SZ", "pre_close,open,close,high3,low3,volume,amt,vwap", start_date, today_date, "PriceAdj=F")
szcz = pd.DataFrame(result.Data, columns=result.Times).transpose()
szcz.set_axis(['前收盘价','开盘价','收盘价','最高价','最低价', '成交量', '成交额','vwap'], axis='columns', inplace=True)
szcz.index.name = '日期'

# 中证500
result = w.wsd("000905.SH", "pre_close,open,close,high3,low3,volume,amt,vwap", start_date,
               today_date, "PriceAdj=F")
# 中证500最早数据从2020-2-20开始
zz500 = pd.DataFrame(result.Data, columns=result.Times).transpose()
zz500.set_axis(['前收盘价','开盘价','收盘价','最高价','最低价', '成交量', '成交额','vwap'], axis='columns', inplace=True)
zz500.index.name = '日期'

for df in [szzs, hs300, sz50, szcz, zz500]:
    df['HO']=df['最高价']-df['开盘价']
    df['OL']=df['开盘价']-df['最低价']
    df['HCY']=df['最高价']-df['收盘价'].shift(1)
    df['CYL']=df['收盘价'].shift(1)-df['最低价']

    df['涨跌幅']=df['收盘价'].pct_change()

    df['AR']=ta.SUM(df.HO, timeperiod=26)/ta.SUM(df.OL, timeperiod=26)*100
    df['BR']=ta.SUM(df.HCY, timeperiod=26)/ta.SUM(df.CYL, timeperiod=26)*100
    df['MA5']=ta.SUM(df['收盘价'], timeperiod=5)/5
    df['MA10'] = ta.SUM(df['收盘价'], timeperiod=10)/10
    df['MA20'] = ta.SUM(df['收盘价'], timeperiod=20)/20
    df['MA60'] = ta.SUM(df['收盘价'], timeperiod=60)/60
    df['MA120'] = ta.SUM(df['收盘价'], timeperiod=120)/120
    df['MA250'] = ta.SUM(df['收盘价'], timeperiod=250)/250
    for i in df.index:
        df['5日涨跌幅'] = df['收盘价'].pct_change(periods=5)
        df['10日涨跌幅'] = df['收盘价'].pct_change(periods=10)
        df['20日涨跌幅'] = df['收盘价'].pct_change(periods=20)
        df['60日涨跌幅'] = df['收盘价'].pct_change(periods=60)
        df['120日涨跌幅'] = df['收盘价'].pct_change(periods=120)
        df['250日涨跌幅'] = df['收盘价'].pct_change(periods=250)

#    df.dropna(inplace=True)

def plot_ARBR(df, title):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plot1 = ax1.plot(df['AR'], linewidth=0.7, color='y', label='AR')
    plot2 = ax1.plot(df['BR'], linewidth=0.7, color='r', label='BR')

    ax2 = ax1.twinx()
    plot3 = ax2.plot(df['收盘价'], linewidth=0.8, color='b', label='close(right)')
    lines = plot1 + plot2 + plot3
    plt.legend(lines, [l.get_label() for l in lines])
    plt.title(title)


for df, table_name in zip([szzs, hs300, sz50, szcz, zz500], table_names):
    save_(engine, table_name, df)

# plot_ARBR(hs300, '沪深300')
# plot_ARBR(szzs, '上证指数')
# plot_ARBR(sz50, '上证50')
# plot_ARBR(szcz, '深证成指')
# plot_ARBR(zz500, '中证500')
