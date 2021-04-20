# coding=utf-8
from configuration import *

table_name = '技术指标_日'
max_date = engine.execute("SELECT max(日期) FROM emotions.{0};".format(table_name)).fetchall()[0][0]
if not max_date == None:
    start_date = w.tdaysoffset(-1, max_date).Data[0][0]
    # 如果只有一天，之后取数据时容易报错

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

    df1 = pd.DataFrame(data1.Data).transpose()
    df1.set_axis(list_4, axis='columns', inplace=True)
    df1.set_axis(data1.Codes, axis='index', inplace=True)
    df1.sort_index(inplace=True)
    df1.dropna(inplace=True)

    df.loc[d]['总股票数'] = len(df1.index)
    # 先计算总数，之后统一算占比
    df.loc[d]['超过月均线股票占比'] = list(df1['20日移动平均']>df1['收盘价']).count(True)/df.loc[d]['总股票数']
    df.loc[d]['超过半年均线股票占比'] = list(df1['120日移动平均']>df1['收盘价']).count(True)/df.loc[d]['总股票数']
    df.loc[d]['超过月指数均线股票占比'] = list(df1['20日指数移动平均']>df1['收盘价']).count(True)/df.loc[d]['总股票数']
    df.loc[d]['超过半年指数均线股票占比'] = list(df1['120日指数移动平均']>df1['收盘价']).count(True)/df.loc[d]['总股票数']
    df.loc[d]['创新高股票占比'] = list(df1['与过去52周最高点差距']==0).count(True)/df.loc[d]['总股票数']

df.index.name = '日期'

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


list_5 = ['上证综合指数','沪深300指数','上证50指数','深证成份指数','中证500指数',
          '涨跌幅：上证综合指数','涨跌幅：沪深300指数','涨跌幅：上证50指数',
          '涨跌幅：深证成份指数','涨跌幅：中证500指数']
list_5_code = "M0020188,M0020209,M0020223,M0020251,M0062541," \
              "M0020194,M0020215,M0020229,M0020257,M0062545"

data2 = w.edb(list_5_code, start_date, today_date)
df2 = pd.DataFrame(data2.Data).transpose()
df2.set_axis(list_5, axis='columns', inplace=True)
df2.set_axis(data2.Times, axis='index', inplace=True)
