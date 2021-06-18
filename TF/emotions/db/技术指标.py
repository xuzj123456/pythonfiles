# coding=utf-8
from configuration import *

table_name = '技术指标_日'
start_date = datetime.date(2015,1,1)


try:
    max_date = engine.execute("SELECT max(日期) FROM emotions.{0};".format(table_name)).fetchall()[0][0]
    if not max_date == None:
        start_date = w.tdaysoffset(-1, max_date).Data[0][0]
    # 如果只有一天，之后取数据时容易报错
except:
    pass

# 所有交易日期
dates = w.tdays(start_date, Period="D").Data[0]
dates = [datetime.date(d.year,d.month,d.day) for d in dates]

# 技术指标_日
list_4 = ['20日移动平均', '120日移动平均','与过去52周最高点差距','20日指数移动平均','120日指数移动平均','收盘价']
list_4_code = "tech_MA20,tech_MA120,tech_chgmax,tech_EMA20,tech_EMA120,close"

df = pd.DataFrame(columns=['超过月均线股票占比','超过半年均线股票占比',
                           '超过月指数均线股票占比','超过半年指数均线股票占比',
                           '创新高股票占比','总股票数'])

for d in dates[:-1]:
    code = get_allAstock_code(d)
    try:
        data1 = w.wss(code, list_4_code, "tradeDate={0};priceAdj=F".format(d))
    except Exception as e:
        print('Get data from wind failed.')
        print(d)
        print(e)

    if data1.ErrorCode != 0:
        break

    df1 = pd.DataFrame(data1.Data).transpose()
    df1.set_axis(list_4, axis='columns', inplace=True)
    df1.set_axis(data1.Codes, axis='index', inplace=True)
    df1.sort_index(inplace=True)
    df1.dropna(inplace=True)

    df.loc[d] = [None, None, None, None, None, None]
    df.loc[d]['总股票数'] = len(df1.index)
    # 先计算总数，之后统一算占比
    df.loc[d]['超过月均线股票占比'] = list(df1['20日移动平均']>df1['收盘价']).count(True)/df.loc[d]['总股票数']
    df.loc[d]['超过半年均线股票占比'] = list(df1['120日移动平均']>df1['收盘价']).count(True)/df.loc[d]['总股票数']
    df.loc[d]['超过月指数均线股票占比'] = list(df1['20日指数移动平均']>df1['收盘价']).count(True)/df.loc[d]['总股票数']
    df.loc[d]['超过半年指数均线股票占比'] = list(df1['120日指数移动平均']>df1['收盘价']).count(True)/df.loc[d]['总股票数']
    df.loc[d]['创新高股票占比'] = list(df1['与过去52周最高点差距']==0).count(True)/df.loc[d]['总股票数']

df.index.name = '日期'

save_(engine, table_name, df)
